# Eedi 误区挖掘深读：长尾标签空间的检索级联 × 未见类别分布修复

> 赛事：Featured ｜ 主题 nlp（检索排序/教育诊断）｜ 1446 队 ｜ 代码赛 ｜ 指标：MAP@{K}（从 2.5k+ 误区池推荐 top-25，越高越好）
> 材料基础：`digests/eedi-mining-misconceptions-in-mathematics.md`（6 篇：1st 详版 177 票/tricks 171/1st 摘要 127/5th 76/3rd 63/7th 59；80 条讨论索引）+ 9 张图（可用 8：551688×7 / 551391×1）
> 深读时间：2026-10（Tier A #47）

## 0. 一句话重述：这道题真正在考什么

题面是"给诊断性数学题 + 正确答案 + 错误答案，从 2.5k+ 误区池里推荐最相关的 25 个误区"，实际被考的是**长尾标签空间的覆盖 + 测试分布修复**：

1. **retrieve-rerank 级联是标准骨架**：retriever 出 32–64 候选 → 14B pointwise 选 8 → 32B pointwise 选 5 → 72B listwise 排序；最终 top-25 = 5（72B）+ 3（32B）+ 17（14B）——**每级都有自己的 LB 分数**（1st：0.524→0.611→0.636→0.643）。
2. **测试含大量"未见误区"**：900+ 个误区和多个 subject 从未在训练出现。3rd 用两次单提交探针量化：只预测 seen 误区得 0.154、只预测 unseen 得 0.444 → 测试中 seen:unseen ≈ 1:3；把 unseen 概率乘常数 C 后，公榜 **0.590→0.658**、私榜 **0.564→0.600**（再加列表 shuffle 到 0.670/0.602）。
3. **合成数据是覆盖手段**：1st 用误区共现聚类分组 + 4–8 个参考 MCQ few-shot 生成新题（Claude 3.5 Sonnet），GPT-4o 当裁判过滤（0–10 分）；再与官方池做"字符串归一 + 嵌入相似度 0.995/0.95 双层去重"合并外部误区；最终 1.8k 官方 + 10.6k 合成、4791 个误区。
4. **CoT 蒸馏与伪标是逐级增益**：Claude 生成"学生为什么选错"的推理链 → 微调 Qwen 推理器（7B/14B/32B）→ reranker 可选读取 CoT；14B ranker 的消融链：+few-shot **+0.036** → +蒸馏伪标 **+0.044** → +负样本比 24/合成 2× **+0.021** → +CoT **+0.019**（private 0.495→0.615）。
5. **CV 切分是个三角**：QuestionId 切分太乐观（同题型泄漏）、SubjectId 太悲观（验证全是未见误区）、ConstructId 刚好（1st 的实证）；5th 反过来选 SubjectId 以模拟测试的 unseen 误区现实。
6. **单 token logits 排序**把生成变分类：5th 用 52 个字母选项（A–Z+a–z）取 logits 概率、7th 用 40 选项/binary/9 选项多管线、1st 用 Yes/No token 差作为 pointwise 分数。

一句话：**这是一场"长尾标签空间"的检索排序赛**——模型是 Qwen 系列级联，胜负在合成数据覆盖未见类别与 unseen 后处理（分布修复）上。

## 1. 材料与角色

| 帖子 | 作者 | 票数 | 角色与独有信息 |
| --- | --- | --- | --- |
| [551688](https://www.kaggle.com/competitions/eedi-mining-misconceptions-in-mathematics/discussion/551688) 1st 详版 | — | 177 | 4 步级联（动态阈值 +32）；分组合成 10.6k；LLM-judge 过滤；CoT 蒸馏；三段消融链；AWQ 任务校准；CV=ConstructId |
| [543519](https://www.kaggle.com/competitions/eedi-mining-misconceptions-in-mathematics/discussion/543519) tricks | — | 171 | recall@25 0.882→0.928 而 LB 0.353→0.478（CV-LB 脱钩示例）；hard negative/大 batch/LLM 训练参数三点 |
| [551402](https://www.kaggle.com/competitions/eedi-mining-misconceptions-in-mathematics/discussion/551402) 1st 摘要 | — | 127 | retriever 集合（e5-mistral-7b-instruct/bge-en-icl/Qwen-14B）；动态阈值 0.06；vLLM prefix caching |
| [551391](https://www.kaggle.com/competitions/eedi-mining-misconceptions-in-mathematics/discussion/551391) 5th | — | 76 | stella-1.5B biencoder + KD（Qwen2.5-32B-Instruct 生成错误推理）+ **52 单 token listwise**（top104 分两批）；GPTQ+vLLM；3 折集成；成本 ~$350 |
| [551498](https://www.kaggle.com/competitions/eedi-mining-misconceptions-in-mathematics/discussion/551498) 3rd | — | 63 | 6 LoRA 集成；**LB 探针 + unseen 乘 C 的 "Magic Boost"**；列表 shuffle；0.590/0.564 → 0.658/0.600 → 0.670/0.602 |
| [551388](https://www.kaggle.com/competitions/eedi-mining-misconceptions-in-mathematics/discussion/551388) 7th（公 2） | — | 59 | 3 管线投票集成（rank-sum）；40/binary/9 选项三种 reranker；**boost missing misconception rank**；vLLM prefix cache/预计算向量 |

**材料缺口（受"不扩采"约束，登记备查）**：LLM 生成数据集(533764,80)、Initial Concerns(533728,80)、**Logits Processors(546978,78)**、Eedi LLM Benchmark(539458,69)、**私有数据集意外共享(550619,63)**、Qwen2.5-72B & Llama3.3-70B on 2×T4(550223,59)、MalAlgoQA(541222,51)、submission 格式/指标(533790,47) 等未收录——**单 token 排序实现与数据泄漏风波**是主要缺口。

## 2. 逐方案对照矩阵

| 维度 | 1st | 3rd | 5th | 7th（公 2） |
| --- | --- | --- | --- | --- |
| Retriever | e5-mistral/bge-en-icl/Qwen-14B 集成；top32+动态阈值（0.06）；**优化 recall@32** | Qwen-14B embedder ×2（公开 + FlagEmbedding）；35 候选 | stella_en_1.5B_v5 + KD 输入；top104 | SFR-Embedding-2_R；N=100 硬负样本（过滤未见）；60–70 候选 |
| Reranker | 14B pointwise→8；32B pointwise→5；72B listwise（3 份 CoT + 5 参考例） | Qwen-32B-instruct-AWQ + 6 LoRA 集成 | Qwen2.5-32B-Instruct listwise（52 字母单 token，top104 两批） | Qwen2.5-32B AWQ：40 选项/binary/9 选项三管线 |
| 合成数据 | 共现聚类 + 参考 MCQ few-shot + GPT-4o 裁判；外部误区双层去重合并（4791 个误区） | 2000 GPT-4-mini 样本（提升有限） | 按 MisconceptionName 相似 few-shot（gemini-1.5-pro），相似参考 +0.01 | gemma-27B/Qwen2.5-32B 合成未知误区 |
| 蒸馏/CoT | Claude 生成学生 CoT → 微调 7B/14B/32B reasoner；reranker 可选读取 | — | Qwen2.5-32B-Instruct 生成错误推理（biencoder +0.04、reranker +0.01） | — |
| unseen 处理 | 合成覆盖 + 蒸馏（无显式后处理） | **探针：seen-only 0.154 vs unseen-only 0.444 → 乘 C 使 unseen 占 top1 75%** | 生成未见误区的题目 | **boost missing misconception rank** |
| 集成/量化 | AWQ 任务校准；prefix caching | 6 LoRA 集成 | GPTQ+vLLM；3 折 | AWQ+vLLM；投票 rank-sum |
| 成绩（公/私） | 私 **0.638**（级联 0.524→0.611→0.636→0.643 公） | 0.670/0.602（magic 后） | CV .626/LB .633 | 私榜第 7 |
| 失败清单 | hard mining/cross-device negatives/自定义 batch/双向编码器/LoRA merge/QwQ | 自训 retriever 反而降分 | 多种选项编码/QwQ/multi-step rerank/prompt 加参考 | concat/平均向量、full-data model、QwQ |

## 3. 共识、分歧与裁决

### 共识一：retrieve-rerank 级联 + Qwen2.5 系列是标准骨架（4/4）

1st：14B/32B/72B 三段，pointwise→listwise；
5th：biencoder + 52 单 token listwise；
7th：多种 option 格式的 32B 管线；
3rd：Qwen-14B embedder + 32B AWQ。

**裁决**：2.5k+ 类目的排序任务中，级联 + 大模型打分是成熟配方；**每级的候选数与保留位数是关键超参**（1st 的动态阈值 0.06、5th 的 104 两批）。置信度：高。

### 共识二：合成数据要"按误区组"生成并过滤（1st/5th/7th）

1st：共现聚类 → 组内 4–8 参考 MCQ few-shot → 生成新题 → GPT-4o 裁判 0–10；外部误区按字符串 + 0.995/0.95 双阈值去重合并；
5th：对没有题目的 MisconceptionName，用**相似误区名的题目**做 4-shot（+0.01 CV）；
7th：合成未知误区。

**裁决**：避免"孤立生成"（只给一个误区名会产出与近邻混淆的题）；**用语义近邻的参考题约束生成，再用裁判过滤"错答↔误区"的逻辑链**，才能给出高分辨监督。置信度：高。

### 共识三：长尾类别 → 单 token logits 排序（5th/7th/1st）

5th：52 个字母单 token（A–Z+a–z）取 logits，top104 分两批（CE 全词表即可）；
7th：40 选项/binary/9 选项三种；
1st：pointwise 用 Yes/No token 差（logits_yes − logits_no）+ 交叉熵。

**裁决**：把"生成式推荐"转成"候选打分分类"，避免输出解析、可批量化、可精确优化排序；**选项数受模型单 token 词表约束**。置信度：高。

### 共识四：CoT 蒸馏 + 伪标逐级增益（1st 完整消融，5th 同向）

1st 的 14B ranker 消融（private）：baseline .495 → +few-shot .531 → +蒸馏伪标 .575 → +负样本比/合成 2× .596 → +CoT **.615**（CV .555→.646）；
5th：KD 生成错误推理 → biencoder +0.04、reranker +0.01。

**裁决**：**counterfactual reasoning 是 LLM 的弱项**（"学生为什么会选错"），用强模型生成 CoT 并蒸馏，是把弱项外置为数据的最优路径。置信度：高。

### 分歧一：CV 切分（QuestionId 太乐观 / SubjectId 太悲观 / ConstructId 刚好）

1st：QuestionId 乐观 → SubjectId 悲观 → **ConstructId** 的 Val/LB 差距最窄；
5th：选 SubjectId，让验证出现更多"仅验证可见"的误区以逼近测试现实。

**裁决**：切分的目标是**模拟测试的哪一部分漂移**——若测试漂移是"未见误区/subject"，SubjectId 更真实；若想看排序能力，ConstructId 更均衡。**没有普适切分，只有与测试分布对齐的切分**。置信度：中高。

### 分歧二：hard negatives 的价值取决于优化目标

tricks 帖：iterative hard mining + 大 batch 是核心；
1st：hard negatives/蒸馏 reranker 分数提升 map@25，**但不提升 recall@32**（最终按 recall@32 选 retriever）；
5th：hard negatives 无效，用放宽样本。

**裁决**：hard negatives 优化"排序精度"（map@25），但会牺牲"召回广度"（recall@32）；级联的第一级要广度 → 应以 recall 选型。**先明确每级指标，再选负样本策略**。置信度：高。

### 分歧三：unseen 分布修复——激进（探针+乘子）vs 数据覆盖（合成+蒸馏）

3rd：Lambda 探针量化 seen:unseen ≈ 1:3，把 unseen 概率乘 C 使 top1 中 unseen 占 75% → 公榜 +0.068、私榜 +0.036；
1st/5th/7th：用合成数据覆盖 + （7th）ranking 后处理，未使用探针乘子。

**裁决**：两者都在修正"训练先验对 unseen 类别的系统性压制"；探针路线收益最大但依赖多次提交与对测试构成的假设（合规/风险高，看到最后没被处罚——本场灰区），数据覆盖路线稳但成本高。**方法论上应优先做数据覆盖，把探针视为风险选项**（对照 T15/T17）。置信度：中高。

## 4. 增量数字账

| 动作 | 数字 | 来源 |
| --- | --- | --- |
| 1st 级联分数 | 候选 32–64：公 .524/私 .475 → 14B top8：公 .611/私 .615 → 32B top5：公 .636/私 .625 → 72B：公 .643/私 **.638** | 1st（图） |
| 1st 14B 消融（CV/公/私） | baseline .555/.545/.495 → +few-shot .580/.559/.531 → +蒸馏 .626/.601/.575 → +负样本 24&合成 2× .642/.608/.596 → +CoT **.646/.611/.615** | 1st（图） |
| 1st 数据 | 官方 1.8k + 合成 10.6k；外部误区合并后池 4791 个；去重阈值 0.995/0.95 | 1st |
| 1st 训练 | retriever temp 0.01（默认 0.02）；每 batch 每个误区只出现一个 demonstration；LoRA r=64/α=128；32B 保留 top8→5；72B listwise 含 3 份 CoT + 5 参考例 | 1st |
| 3rd 探针 | 只预测 seen：0.154；只预测 unseen：0.444 → 比率 ≈1:3；乘 C 后 unseen 占 top1 75%；公 .590→.658、私 .564→.600；shuffle 后 .670/.602；测试仅 ~685 题 | 3rd |
| 5th | 52 单 token（A–Z+a–z）；top104 两批；52×3 仅 CV 小涨、LB 不涨；CV .626/LB .633；KD +0.04（biencoder）；训练 32B ~7h/A100；成本 ~$350 | 5th |
| 7th | 3 管线投票 rank-sum；40/binary/9 选项；N=100 硬负样本（过滤未见误区） | 7th |
| tricks 帖 | CV recall@25 0.882→0.928 时 LB 0.353→0.478（CV-LB 脱钩示例）；batch 64 + 100 硬负样本 | 543519 |
| 赛事 | 1446 队；MAP@K；80 帖 | 元数据 |

**结构校验（2 处吻合）**

1. 1st 的消融链每一步单独变量（few-shot/蒸馏/负样本比/CoT），与正文百分比一致 ✓；
2. 3rd 的 seen:unseen 1:3 与其"乘 C 使 top1 unseen 占 75%"的设定自洽 ✓。

## 5. 机制推演

**M1｜为什么 unseen 误区主导测试**：误区池是"长尾分类体系"；训练集只覆盖其头部。模型在训练先验下对未见类别给低分（softmax 被见过的类目挤压），而测试中它们约占 3/4 → **不修正先验就会系统性漏掉多数正确答案**。3rd 的探针把这一点量化成 0.154 vs 0.444。

**M2｜为什么合成数据必须"按组 + 裁判"生成**：误区之间高度相似（"平方差公式"相关的十几条），孤立生成会让错答与近邻误区混淆（低分辨性）。用共现聚类分组 + 组内参考题 few-shot，约束生成器在"同组细粒度差异"上做区分；LLM-as-judge 再验证"错答是否逻辑上由该误区产生"。**数据分辨性 = 任务分辨性**。

**M3｜CoT 蒸馏为什么有效**：任务本质是反事实推理（"如果学生有误区 M，他会怎么算错"），而通用 LLM 擅长正向求解、弱于反事实。用 Claude 的 CoT 把推理过程显式化，再蒸馏到小模型；reranker 可选择读 CoT（训练 50% 带、50% 不带）→ 兼顾有无推理的两种模式。

**M4｜单 token 排序的工程优势**：候选项映射为单 token（字母/数字），用 logits/softmax 排序：① 免去自由文本解析；② 一次前向给所有候选打分（52/40/9）；③ 可直接用 CE/排序损失训练；④ 配合 vLLM prefix caching 复用题目前缀。**把生成问题降维成分类问题**是 LLM 排序的通用工程范式。

**M5｜CV 切分的三角关系**：按 QuestionId 切 → 验证题与训练题同主题，分数虚高（泄漏）；按 SubjectId 切 → 验证集几乎没有训练可见的误区，分数虚低；按 ConstructId（知识点）切 → 介于两者之间，Val/LB 差距最窄。选择切分等价于选择"模拟哪种漂移"。

**M6｜分布修复的两种手段与风险**：数据覆盖（合成+蒸馏）改变模型先验；后处理乘子（探针）不改模型只改输出。前者稳、贵；后者便宜、依赖"测试构成可探"的假设与提交次数。本场 3rd 的收益（+0.068 公榜）说明**当测试分布已知与训练不同时，修复分布的收益可以超过所有建模优化之和**（对照 LEAP/ARIEL 的偏移修复案例）。

## 6. 证据分级

| 断言 | 等级 | 说明 |
| --- | --- | --- |
| 1st 级联/消融/数据链 | 自述 + 代码 + 数据集 + 7 张图 | 高 |
| 5th listwise/KD | 自述 + 代码 + 图 | 高 |
| 3rd 探针与 magic boost | 自述具体数字（方法依赖排行榜探针，合规灰区） | 中高 |
| 7th 3 管线 | 自述 + 加速清单 | 中 |
| tricks 帖 CV-LB 数据 | 自述（早期贴，数字自洽） | 中 |
| 私有数据泄漏/Initial Concerns | 仅标题（未收录） | 低（登记） |

## 7. 边界条件与反事实

- **反事实 1**：不生成合成数据 → unseen 误区无法被模型表示（3rd 只能靠后处理补偿，1st/5th 直接覆盖）。
- **反事实 2**：不做 unseen 后处理 → 3rd 停留在 0.590/0.564（乘子后 0.658/0.600）。
- **反事实 3**：用 QuestionId CV → 验证过乐观（1st 的实证）；用 SubjectId → 过悲观（除非刻意模拟 unseen）。
- **反事实 4**：没有 CoT/蒸馏 → 14B private 停在 .495（消融 baseline）；有则 .615。
- **反事实 5**：第一级用 map@25 优化（hard negatives）→ recall@32 受损，级联上限下降（1st 的选型逻辑）。
- **边界**：结论依赖"允许外部 LLM/合成数据 + 可以多次提交探针"的赛制；闭集标签任务不需要 unseen 修复。

## 8. 悬案与失败学

**悬案**

1. **私有数据集意外共享（550619，63 票）与 Initial Concerns（533728）未收录**——数据泄漏风波的处理与影响未知。
2. **Logits Processors（546978，78 票）未收录**——单 token/受限词表打分的实现细节缺失（5th/7th 的核心工程）。
3. 3rd 的探针乘子是否被官方认可（本场未见处罚记录）；若禁止探针，最优解会回到合成数据路线。
4. Eedi LLM Benchmark（539458）未收录——基础模型选择的系统对照缺失。
5. 1st 的"external misconceptions 对泛化的独立贡献"未单独消融。

**失败学（跨队合集）**

- 检索类：iterative hard mining / cross-device negatives / 自定义 batch（1st，对 recall 无益）；自训 retriever 反而降分（3rd）；concat/平均向量（7th）。
- 模型类：QwQ-32B-Preview（1st/5th/7th 均失败）；LoRA merge（1st）；双向编码器改造（1st）；full-data model（7th）。
- 训练类：multi-step rerank（5th）；选项编码用双字母/数字/平假名（5th，均差于 52 字母）；prompt 里加参考示例（5th）。

## 9. 图表证据

> 路径相对本文件（`analysis/deep/`）：`../../intel/eedi-mining-misconceptions-in-mathematics/bodies/<topic>_img/NN.png`

**图 1：1st 的四步级联与每级 LB 分数**（topic 551688）——`../../intel/eedi-mining-misconceptions-in-mathematics/bodies/551688_img/01.png`

*读图结论*：2.5k+ 误区池 + Query（题+错答）→ retriever → 32–64 候选（公 .524/私 .475）→ 14B pointwise top8（.611/.615）→ 32B pointwise top5（.636/.625）→ 72B listwise（.643/.638）；最终 top-25 = 5+3+17。**级联各段的边际收益一目了然**（14B 提升最大）。

**图 2：1st 的 pointwise ranker 输入结构**（topic 551688）——`../../intel/eedi-mining-misconceptions-in-mathematics/bodies/551688_img/03.png`

*读图结论*：system 提示 + 目标误区 + **Few-Shot 示例** + 题目/正误答案 + **CoT "Thought"** + "该误区是否导致该错答？(Yes/No)"。三种技巧（few-shot、CoT、Yes/No logits）都在同一输入模板里。

**图 3：1st 的 14B ranker 消融表**（topic 551688）——`../../intel/eedi-mining-misconceptions-in-mathematics/bodies/551688_img/04.png`

*读图结论*：baseline CV .555/私 .495 → +few-shot .580/.531 → +蒸馏 .626/.575 → +负样本比&额外数据 .642/.596 → +CoT **.646/.615**。**四项技巧逐级递增、无回退**。

**图 4：5th 的 listwise 52 单 token 管线**（topic 551391）——`../../intel/eedi-mining-misconceptions-in-mathematics/bodies/551391_img/01.png`

*读图结论*：知识蒸馏生成"错误推理" → biencoder（stella 1.5B）出 104 候选 → 分两批 52 个字母选项 → 单 token 解码取概率 → 排序。**把排序变成受限词表的分类任务**。

## 10. 对既有笔记/playbook 的修订点

1. `notes/nlp/eedi-mining-misconceptions-in-mathematics.md` 升级：补 6 篇作者/票数、四方案 × 8 维对照、数字账（消融链 .495→.615、探针 0.154/0.444、0.590→0.658）与 4 张图证；新增"未见类别分布修复"节。
2. `playbook/nlp.md`（检索排序/长尾标签节）增补：
   - **级联设计**：每级优化自己的指标（第一级 recall、后级精度）；动态阈值补候选；prefix caching 复用前缀；
   - **合成数据覆盖长尾类别**：聚类分组 + 近邻参考 few-shot + LLM-as-judge 过滤 + 与官方池去重合并；
   - **CoT 蒸馏**：强模型生成反事实推理 → 微调 reasoner → 作为 reranker 可选输入；
   - **单 token logits 排序**：候选映射为单 token，CE 训练，批量打分；
   - **CV 切分三角**：QuestionId/SubjectId/ConstructId 的乐观-悲观谱系，按测试漂移选型；
   - **unseen 分布修复**：合成覆盖优先；探针乘子作为高风险选项（需报告/合规评估）。
3. `playbook/00-通用方法论.md` 增补：**"标签空间的长尾 = 另一种分布偏移"**（修复收益可超过建模）；**"把生成降维成受限分类"**（单 token 打分）。
4. `analysis/THEORY.md`（Batch 5 末汇总 v0.5）候选：
   - **L78｜长尾/未见类别：覆盖 + 分布修复**（证据 = 本场 1st 合成 vs 3rd 探针；与 polymer/LEAP 的偏移修复同族）；
   - **L79｜级联每级优化自己的指标**（recall vs map 的负相关；1st/tricks 帖）；
   - **L80｜反事实推理外置为 CoT 数据**（1st 消融 +0.044/+0.019）。

## 11. 出处

- 1st 详版（177 票）：https://www.kaggle.com/competitions/eedi-mining-misconceptions-in-mathematics/discussion/551688
- tricks 帖（171 票）：https://www.kaggle.com/competitions/eedi-mining-misconceptions-in-mathematics/discussion/543519
- 1st 摘要（127 票）：https://www.kaggle.com/competitions/eedi-mining-misconceptions-in-mathematics/discussion/551402
- 5th（76 票）：https://www.kaggle.com/competitions/eedi-mining-misconceptions-in-mathematics/discussion/551391
- 3rd（63 票）：https://www.kaggle.com/competitions/eedi-mining-misconceptions-in-mathematics/discussion/551498
- 7th（59 票）：https://www.kaggle.com/competitions/eedi-mining-misconceptions-in-mathematics/discussion/551388
- 缺口登记：533764、533728、546978、539458、550619、550223、541222、533790 未收录正文
