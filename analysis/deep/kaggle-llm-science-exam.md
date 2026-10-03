# LLM Science Exam 深读：检索侧决定上限（RAG 工程 × 数据共享 × 难例分诊）

> 赛事：Featured ｜ 主题 nlp（开放域科学问答）｜ 2674 队 ｜ 代码赛 ｜ 指标：MAP@3
> 材料基础：`digests/kaggle-llm-science-exam.md`（8 篇：60k 数据集 282 票 / 1st 短 239 / 1st 长 219 / 10th 93 / 3rd 84 / 5th 81 / Top100 73 / 4th 72；120 条讨论索引）+ 6 张图
> 深读时间：2026-10（Tier A #45）

## 0. 一句话重述：这道题真正在考什么

题面是"回答约 4000 道科学多选题（MAP@3）"，实际被考的是**检索侧工程 + 社区数据生态 + 9 小时推理预算的分配**：

1. **这是检索比赛，不是建模比赛**：5th 原话"我意识到这是一场 retrieval 比赛"；1st 从分类方法触顶后转向 RAG、之后"模型几乎不动，只改检索"；Top100："每加一条 RAG 管线带来的 CV/LB 提升都超过加一个 DeBERTa"；3rd 的消融里 **tuned reranker 一项 +0.015**（0.912→0.927），是最大单点。
2. **维基语料质量 = 检索上限**：公开 dump 解析器会丢数字/公式（mwparserfromhell 的已知问题）；cirrussearch 全渲染 dump 无换行，需按 256/512/1024 字符重切；1st 的 512 字符版本单 corpus 最好；3rd 自改 wikiextractor 修复数字。
3. **模型两条路都行，LLM 上限更高**：DeBERTa-v3-large + 60k 数据 + 多 RAG 即可 0.90–0.93（Top100/4th/3rd/10th）；1st 的 7B/13B LLM（binary per-option 头 + late fusion）拿 0.933 私榜。LLM 对选项顺序敏感 → 需要 TTA/二进制化设计。
4. **数据共享是社区上限**：60k 数据集（282 票）把公开数据 + 维基上下文拼好，单模型 LB 0.830+；40k/99k 跟进；官方允许外部数据（有专门澄清帖）。
5. **9 小时预算靠"难例分诊"**：5th：Mistral-7B 全量 → Llama2-70B 处理低置信 40% → 70B 长上下文处理 5%；3rd：小模型出 500 道最难 → 70B（Platypus/Xwin）；1st：5×7B + 1×13B 的 late fusion + past_key_values 缓存，2.5TB 输入恰好卡进 9h。
6. **验证的陷阱**：train.csv 200 题太简单（被训练数据覆盖，0.99+ 不可用）；社区 6k/2k 验证才有效；且 GPT-3.5 生成的数据含标注错误 → **理论天花板**（1st 的"最后 0.01 极难"）。

一句话：**这是一场"RAG 质量 × 数据共享 × 推理工程"的竞赛**——模型只是链条中的一环，检索与语料的边际收益最大。

## 1. 材料与角色

| 帖子 | 作者 | 票数 | 角色与独有信息 |
| --- | --- | --- | --- |
| [436383](https://www.kaggle.com/competitions/kaggle-llm-science-exam/discussion/436383) 60k 数据集 | — | 282 | 拼接 7 个公开数据集 + 每条加 Wiki 上下文（NUM_TITLES=5/NUM_SENTENCES=20）；**单模型 LB 0.830+**；open-book 训练/推理范式 |
| [446240](https://www.kaggle.com/competitions/kaggle-llm-science-exam/discussion/446240) 1st 短 | — | 239 | RAG 早发现；6k 验证选私榜最高；e5 最佳；自定义 GPU cosine（无需 FAISS）；5 chunks/1k maxlen；5×7B+1×13B 集成；"0.93 易、0.94 难"；天花板来自标注错误 |
| [446422](https://www.kaggle.com/competitions/kaggle-llm-science-exam/discussion/446422) 1st 长 | — | 219 | 300 组（检索×模型×dump）；e5/gte/bge 5 个 embedding；60M chunks 分块 GPU 相似度（2 卡）；cirrussearch 512 字符最佳；训练 3 chunks/推理 5 chunks；**binary per-option 头 + past_key_values 缓存 + 跨选项平均 logits**；H2O LLM Studio；0.933 私榜 |
| [446248](https://www.kaggle.com/competitions/kaggle-llm-science-exam/discussion/446248) 10th | — | 93 | 4 类 wiki 检索（dump/cirrus/270k×2）；滑窗分块；**max-probability 集成**（比平均更抗过拟合）+ TF-IDF (4,7)-gram 后处理 |
| [446358](https://www.kaggle.com/competitions/kaggle-llm-science-exam/discussion/446358) 3rd | — | 84 | 修改 wikiextractor 修复数字；**passage 级单阶段检索**（两阶段会漏检）；reranker 两要点（同分布 pair + 预训练热启动 + hard negatives）；消融 0.894→0.928；70B 只处理 500 难例 |
| [446293](https://www.kaggle.com/competitions/kaggle-llm-science-exam/discussion/446293) 5th | — | 81 | 自解析 Wiki（wikitextparser + 保留 {val}/{math}）；BM25 pyserini/Lucene（74M 段落，200 查询 2min）；instructor-xl（300GB→10GB 量化）+ bge-large-en；**Llama2-70B 逐层量化权重 + xformers（6GB 显存）**；选项轮转 TTA 拼接复用；多阶段推理（私 0.926） |
| [446318](https://www.kaggle.com/competitions/kaggle-llm-science-exam/discussion/446318) Top100 | — | 73 | **RAG 数量 > 模型质量**；7 条 RAG × DeBERTa 集成；GPU 加速（RAPIDS TF-IDF / GPU faiss / fp16 / 双 T4 线程）；`sublinear_tf=True` +0.010；QDO 增强；choice-permute TTA；drop-2-wrong-choice 提速 1.6× |
| [446307](https://www.kaggle.com/competitions/kaggle-llm-science-exam/discussion/446307) 4th | — | 72 | Elasticsearch 句级检索 + 三种排序（ES score/edit distance/semantic → v3/v5/v7 context）；DeBERTa-v3-large 512→768→1280 token；context ensemble；2000 样本验证与 LB 线性相关 |

**材料缺口（受"不扩采"约束，登记备查）**：[LB 0.836] Zero-shot 70B+RAG(440620,182 票)、270K Wiki STEM 检索(442595,137)、6000 新训练样本(426174,159)、Bonus 40k(440908,156)、LLM 微调教程(424519,144)、15k 数据(431786,108)、Simple baseline(424242,95)、MAP@3 加入 Trainer(435602,91)、99k 数据(444202,89)、**Model/Data Use Clarification(425681,86)** 等未收录——**数据使用规则与零样本 70B 路线**是主要缺口。

## 2. 逐方案对照矩阵

| 维度 | 1st（H2O） | 3rd | 4th | 5th | Top100 | 10th |
| --- | --- | --- | --- | --- | --- | --- |
| 检索 | e5/gte/bge 多 embedding，60M chunks GPU 分块相似度；5 种 wiki/dump | miniLM+bge-small 双塔 → top500 → **tuned reranker** → top10 | Elasticsearch 句级 + 3 种排序（v3/v5/v7） | BM25(74M) + instructor-xl + bge-large-en（STEM270k） | 7 条 RAG 管线（文章/段落/chunk/Q-only/Q+choices） | 4 类 wiki + 滑窗 + faiss |
| 语料 | cirrussearch + 多 dump（512 字符最佳） | 自改 wikiextractor（数字修复） | cirrussearch（Elasticsearch） | 自解析（保留数字/公式） | 多种公开 wiki | dump/cirrus/270k |
| 模型 | 7B×5+13B×1 LLM（binary 头） | DeBERTa×5+Electra×3+Roberta×5 + 70B 难例 | DeBERTa-v3-large（768/1280 token） | Mistral-7B 全量 + Llama2-70B 难例 | DeBERTa-v3-large（60k） | DeBERTa-large |
| 集成 | late fusion（每模型不同检索） | 0.5/0.3/0.2 加权 | context ensemble | 多阶段（40%/5%） | 7×3 logits | **max-probability** |
| 成绩 | **0.933 私榜**（单模型 0.932） | 0.928 | 0.925+（val 相关） | 0.926 | 0.90x（30min 单模 0.900） | 金区 |
| 失败清单 | DeBERTa 无用、multi-class/位置偏差、TTA 不稳 | Platypus license 顾虑（后证不用更好） | train.csv 太易 | 自定义 query/embedding fine-tune 无效 | OOM 只能上 7 条 RAG（自省"应重质不重量"） | — |

## 3. 共识、分歧与裁决

### 共识一：检索（RAG）质量决定上限，模型是链条中一环（5/6 明说）

5th："这是 retrieval 比赛"；
1st：分类方法触顶 → 转向 RAG 后大跳，此后"模型几乎不动"；
Top100："每加 RAG 的收益 > 加 DeBERTa"；
3rd：tuned reranker 单项 +0.015（最大）；
4th：检索质量与 context 组织"关键重要"。

**裁决**：开放域 QA 的瓶颈在"证据是否被检索到"；模型容量在证据到位后差异缩小。**提升检索多样性/质量的性价比最高**。置信度：高。

### 共识二：维基语料解析与分块是隐形主变量（1st/3rd/5th/4th）

公开 dump 丢数字/公式（mwparserfromhell 已知问题）→ 5th 换 wikitextparser 并保留 `{val}/{math}`；3rd 改写 wikiextractor 修复数字；1st 用 cirrussearch（全渲染）并重切成 512 字符；4th 用 cirrussearch + 符号链接 I/O。

**裁决**：科学题的关键线索是数字/公式/专名；**解析器丢信息 = 检索召回的硬上限**。自建语料虽贵，但收益直接。置信度：高。

### 共识三：社区数据共享是分数生态的核心（60k/40k/99k + open book）

60k 数据集（282 票）把公开数据 + 维基上下文拼好 → 单模型 0.830+；
1st："训练数据其实不太重要，早期 radek 的数据就够"；
Top100：质量关键的是 RAG，不是 DeBERTa 训练数据的多寡。

**裁决**：本场形成了"数据集共享 → 全员基线抬升 → 竞争转向检索/工程"的社区生态；对学习者，**先吃透社区数据再自研**。置信度：高。

### 共识四：验证必须用"够难"的集合（4/4 提到）

train.csv 200 题被训练数据覆盖（0.99+ 不可用）；
1st：用 6k STEM 题验证并"选私榜最高（也最高 CV）的提交"；
4th：60k 中抽 2000 题，与 LB 线性相关（图）；
5th：冻结 3 个数据集（含自有 1000 题）全程不训练。

**裁决**：开放域 QA 的本地验证要来自**训练分布之外**；否则 0.99 的本地分数毫无意义。置信度：高。

### 分歧一：LLM vs DeBERTa——两条路都能走，上限不同

1st：LLM 明显更优，"DeBERTa 即便集成也无帮助"；
3rd/4th/Top100/10th：DeBERTa + 多 RAG 到 0.90–0.928；
5th：Mistral-7B/70B 混合多阶段到 0.926。

**裁决**：DeBERTa 路线（编码器分类）成本低、易集成，适合 Kaggle 单机预算；LLM 路线（binary per-option + 缓存/TTA）上限更高但工程重（量化、层加载、9h）。选择的本质是**算力/工程 vs 分数上限**的权衡。置信度：高。

### 分歧二：难例分诊结构（小模型全量 + 大模型难例）

5th：Mistral-7B 全量 → 70B 低置信 40% → 70B 长上下文 5%；
3rd：小模型出 500 最难 → 70B（Platypus/Xwin）；
1st：不做显式分诊，而是 5×7B+1×13B late fusion + 缓存。

**裁决**：9h 预算下，"小模型筛 + 大模型精处理"是普遍结构；1st 用工程（缓存/量化/并行）替代分诊同样可行。**推理预算分配是策略变量**。置信度：高。

### 分歧三：集成/解码细节

1st：binary per-option（消除位置偏差）+ 跨选项平均 logits 辅助输入；
5th/Top100：choice 轮转 TTA（5th 拼接复用前缀，5× 成本可控）；
10th：max-probability 集成（比平均更抗过拟合）+ TF-IDF 后处理；
1st/Top100：choices 全用 vs 只用问题检索等多种 query 策略。

**裁决**：选项顺序偏差是 LLM 判别的系统性问题，二进制化 + TTA 是标准解；集成取 max 在噪声标注下更稳（10th）。置信度：中高。

### 特别：天花板与治理

1st：GPT-3.5 生成数据有固有错误 → 分数理论上限；"0.93 易、0.94 难"（数周 grind）；
数据使用澄清帖（425681，86 票）与 Platypus2 license 争议（3rd 注）表明：**外部模型/数据的合规边界**是本场的前置问题。

**裁决**：在本场，天花板由标注噪声与检索召回共同决定；治理层面，使用外部模型前确认许可与官方说明。置信度：中高。

## 4. 增量数字账

| 动作 | 数字 | 来源 |
| --- | --- | --- |
| 1st 最终 | 私榜 **0.933**（单模型 0.932）；5×7B + 1×13B late fusion；2.5TB 输入、9h 用尽 | 1st |
| 1st 检索 | 300 组组合筛选；5 embedding（e5-base/large、gte-base/large、bge-large）；60M chunks；2 GPU 分块相似度；train 3 chunks/推理 5 chunks；cirrussearch 512 字符最佳 | 1st |
| 1st 结构 | context+Q 的 past_key_values 缓存一次、5 答案批量复用；binary 分类头；跨选项平均 logits 辅助 | 1st |
| 3rd 消融 | 5 DeBERTa（未调 reranker）0.894/0.893 → +Platypus 0.91 → +新模型/Electra/Roberta 0.912 → **+tuned reranker 0.927** → +Xwin 0.928；final 0.9284/0.9286；无 reranker 0.9113/0.9130；无 LLM 0.9165/0.9201 | 3rd |
| 3rd 检索 | 112M passages；miniLM-L6-v2 + bge-small 各 80GB embeddings（fp16）；top500 → rerank → top10；reranker 用 70k 数据的同分布 pair + 硬负样本 | 3rd |
| 5th 工程 | BM25（pyserini/Lucene）74M 段落，200 查询 ~2min；instructor-xl 索引 300GB→10GB 量化；Llama2-70B 逐层量化权重 + xformers ≈6GB 显存；选项轮转 5× TTA 拼接复用；多阶段：7B 全量 → 70B 40% → 70B 长上下文 5%；私 0.926 | 5th |
| Top100 | 7 条 RAG × 3 DeBERTa；30 分钟单模型 LB 0.900；`sublinear_tf=True` **+0.010**；QDO 增强；7× 加速（2×T4+fp16+线程+drop-2） | Top100 |
| 4th | 2000 样本验证与 LB 线性相关（图）；token 512→768→1280；三种 context（v3/v5/v7）集成 | 4th |
| 60k 数据集 | 单模型 LB **0.830+**；7 个公开数据集 + Wiki 上下文 | 436383 |
| 赛事 | 2674 队；MAP@3；120 帖 | 元数据 |

**结构校验（2 处吻合）**

1. 3rd 的消融链各步单调（0.894→0.91→0.912→0.927→0.928），与"reranker 为最大单点"的结论自洽 ✓；
2. 1st 的"5×7B+1×13B、2.5TB/9h"与其缓存/量化工程描述一致 ✓。

## 5. 机制推演

**M1｜为什么检索的边际收益大于模型**：题目要求"从维基里找到含答案的证据"；模型只做判别。加一条检索管线 = 换一个"看世界的视角"（不同 embedding/分块/query 构造），能补捉别的管线漏掉的证据；加一个模型只是对同一证据换打分器，误差相关性高。**证据多样性 > 打分器多样性**。

**M2｜语料解析为何是硬上限**：科学问题大量依赖数字（"2 mio."）与公式；mwparserfromhell 丢模板 → 这些句子在索引里根本不存在，任何检索/模型都无法找回。cirrussearch 全渲染修复了缺失但破坏换行 → 需按字符重切并保句完整。

**M3｜binary per-option + 缓存的工程学**：生成式 LLM 对选项顺序敏感（位置偏差），且直接生成答案形式难解析；把问题变成"每个选项独立二分类"消除了顺序依赖，还能用 past_key_values 缓存共享 context+question 的前向（一次算、五路复用），让 70B 在 9h 内可行。

**M4｜难例分诊的信息论**：小模型的低置信题正是证据不足/歧义的样本；把预算集中到这些样本（更长上下文、更大模型、更多检索）比全量用大模型更高效。5th 的 40%/5% 与 3rd 的 500 题都近似"按不确定性分配算力"。

**M5｜TTA 的机制与成本**：选项轮转平均消除位置偏差；5th 用"5 种顺序拼接 + attention mask"把公共前缀（context+question）只算一次 → 5×TTA ≈ 一次长序列前向。这是"用序列打包换推理预算"的通用手法。

**M6｜数据共享生态的正反馈**：60k 数据集让所有人基线抬升，竞争转向检索工程；同时公开数据本身含错（GPT-3.5 生成）→ 分数天花板。**共享抬高下限、标注噪声封顶**，1st 的"0.93→0.94 数周 grind"是天花板的具体刻度。

## 6. 证据分级

| 断言 | 等级 | 说明 |
| --- | --- | --- |
| 1st 结构/成绩（0.933） | 自述 + 公开 kernel（0.933/单模 0.932） | 高 |
| 3rd 消融表 | 自述 + 代码链接（更新版） | 高 |
| Top100 的 RAG>模型论断 | 自述 + notebook | 中高 |
| 5th 多阶段/70B 工程 | 自述 + pipeline 图 | 中高 |
| 4th 验证相关性图 | 自述 + 图 | 中高 |
| 60k 数据集 0.830+ | 公开数据集/notebook（可复现） | 高 |
| "数据不太重要"（1st） | 单队观点（与 Top100 部分冲突） | 中 |
| 数据使用澄清（425681） | 仅标题（未收录） | 低（登记） |

## 7. 边界条件与反事实

- **反事实 1**：闭卷（不用维基检索）→ 分类方法触顶（1st 的经历），分数上限显著更低。
- **反事实 2**：语料解析不修数字 → 检索召回存在硬缺失；5th/3rd 的自建语料是直接反证。
- **反事实 3**：只用单条检索 + 单模型 → Top100 的"加 RAG 比加模型有效"与 3rd 的 reranker +0.015 说明差距可被检索吃掉。
- **反事实 4**：70B 全量推理 → 9h 不可行；必须分诊或用缓存/量化工程（1st/5th）。
- **反事实 5**：用 train.csv 200 做验证 → 0.99+ 的假象；4th 的 2000 题相关图是正确做法。
- **边界**：结论依赖"答案可在维基找到 + 允许外部数据"；闭域/私有知识库任务需替换语料与合规假设。

## 8. 悬案与失败学

**悬案**

1. **数据使用澄清（425681）未收录**：外部模型/数据（含 GPT-3.5 生成、Platypus2）的合规边界结论缺失。
2. 440620（零样本 70B+RAG 0.836）未收录——无微调路线的完整方法缺失；442595（270K STEM 检索）未收录。
3. 1st 提到的"两种 head 架构"细节未展开；"0.94 的最后一分"具体做法未给。
4. GPT-3.5 标注错误的量化（天花板具体数值）未给。
5. MAP@3 不稳定的量化分析（435602 帖）未收录。

**失败学（跨队合集）**

- 模型类：DeBERTa 在 LLM 体系里无帮助（1st）；multi-class/把其他选项当上下文引入位置偏差（1st）；更大 LLM（>13B 除难例外）不划算（1st）。
- 检索类：自定义 query（5th）、embedding fine-tune（5th）、两阶段"先文章后句子"会漏检（3rd）；只管 RAG 数量不管质量 + OOM（Top100 自省）。
- 数据类：train.csv 200 太易不能当验证（4th）；失配/缺失 wiki 解析器（多队）。
- 治理类：license 灰区（3rd 的 Platypus2 顾虑）。

## 9. 图表证据

> 路径相对本文件（`analysis/deep/`）：`../../intel/kaggle-llm-science-exam/bodies/<topic>_img/NN.ext`

**图 1：5th 的检索→LLM 管线**（topic 446293）——`../../intel/kaggle-llm-science-exam/bodies/446293_img/01.jpg`

*读图结论*：自解析维基 dump（+STEM270k 子集）→ 三种检索（BM25 pyserini、instructor-xl、bge-large-en）→ LLM（Mistral-7B/Llama2-70B）→ 预测。**稀疏+稠密混合检索的标准结构**。

**图 2：3rd 的完整系统与消融路径**（topic 446358）——`../../intel/kaggle-llm-science-exam/bodies/446358_img/01.png`

*读图结论*：Wikipedia→112M passages→双 embedding（miniLM/bge-small）→top500→**tuned reranker→top10**→DeBERTa/Electra/Roberta 集成（0.5/0.3/0.2）→500 难例交 70B（Platypus/Xwin）→合并。与消融表（reranker +0.015、LLM +0.012）一一对应。

**图 3：1st 的 binary per-option + 缓存架构**（topic 446422）——`../../intel/kaggle-llm-science-exam/bodies/446422_img/01.png`

*读图结论*：contexts+question 前向一次并缓存 past_key_values；5 个答案各自复用缓存批量前向；logits→分类头→每选项概率（1.5/0.1/-0.5/0.7/-0.2）。**去位置偏差 + 复用 KV 的推理设计**。

**图 4：Top100 的 RAG 集成**（topic 446318）——`../../intel/kaggle-llm-science-exam/bodies/446318_img/01.png`

*读图结论*：question+choices → 7 条检索管线各自取 context → 同一 DeBERTa-v3-large（60k 训练）分别打分 → logits 集成。**"RAG 数量 > 模型质量"的直接图证**（OOM 前只能上 7 条）。

**图 5：4th 的验证与 LB 相关性（2000 样本）**（topic 446307）——`../../intel/kaggle-llm-science-exam/bodies/446307_img/01.png`

*读图结论*：2000 题验证分数与 LB 近似线性（0.906–0.914 对应 0.914–0.933）。**用足够难的公开集合建立可信 CV**——train.csv 200 做不到。

## 10. 对既有笔记/playbook 的修订点

1. `notes/nlp/kaggle-llm-science-exam.md` 升级（现为浅版）：补 8 篇作者/票数、六方案 × 7 维对照、数字账（0.933、reranker +0.015、sublinear_tf +0.010、60k 0.830+）与 5 张图证；新增"语料解析"与"难例分诊"节。
2. `playbook/nlp.md`（RAG/开放域 QA 节）增补：
   - **检索优先**：多 embedding/多分块/多 query 的检索多样性 > 模型多样性；reranker 训练三要点（同分布 pair、预训练热启动、hard negatives）；
   - **语料工程**：解析器审计（数字/公式）、cirrussearch 重切分、passage 级单阶段检索；
   - **LLM 判别设计**：binary per-option（去位置偏差）、past_key_values 缓存、跨选项平均 logits、choice-permute TTA（拼接复用）；
   - **预算分配**：小模型筛+大模型难例的分诊结构；量化/层加载让 70B 上 Kaggle；
   - **验证**：用训练分布之外的 2k–6k 集合；警惕 200 题式假象。
3. `playbook/00-通用方法论.md` 增补：**"RAG 质量优先于模型质量"**（本场 GOAL 的检索侧主题）；**"按不确定性分配推理预算"**；**"共享数据抬高下限、标注噪声封顶"**。
4. `analysis/THEORY.md`（Batch 5 末汇总 v0.5）候选：
   - **L72｜开放域 QA：检索多样性是第一杠杆**（证据 = 1st/Top100/3rd）；
   - **L73｜难例分诊多阶段推理**（5th/3rd；与 ARIEL 的置信度路由同族）；
   - **L74｜选项位置偏差与二进制/TTA 设计**（1st/5th/Top100）。

## 11. 出处

- 60k 数据集（282 票）：https://www.kaggle.com/competitions/kaggle-llm-science-exam/discussion/436383
- 1st 短（239 票）：https://www.kaggle.com/competitions/kaggle-llm-science-exam/discussion/446240
- 1st 长（219 票）：https://www.kaggle.com/competitions/kaggle-llm-science-exam/discussion/446422
- 10th（93 票）：https://www.kaggle.com/competitions/kaggle-llm-science-exam/discussion/446248
- 3rd（84 票）：https://www.kaggle.com/competitions/kaggle-llm-science-exam/discussion/446358
- 5th（81 票）：https://www.kaggle.com/competitions/kaggle-llm-science-exam/discussion/446293
- Top100（73 票）：https://www.kaggle.com/competitions/kaggle-llm-science-exam/discussion/446318
- 4th（72 票）：https://www.kaggle.com/competitions/kaggle-llm-science-exam/discussion/446307
- 缺口登记：440620、442595、426174、440908、424519、431786、424242、435602、444202、425681 未收录正文
