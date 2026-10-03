# AI Mathematical Olympiad Prize 轻量深读（Tier B）

> 赛事：Featured ｜ 主题 nlp/reasoning（奥数题求解）｜ 1161 队 ｜ 标准赛（50 题，答案是整数）｜ 指标：Accuracy
> 材料基础：`digests/ai-mathematical-olympiad-prize.md`（4 篇正文：1st Numina 519303 / 2nd CMU_MATH 518964 / 3rd 517206 / 训练集样例 640 行处；80 条主题索引）+ 6 张图
> 轻读时间：2026-10（Tier B B10）

## 1. 一句话重述与数字账

在 Kaggle 有限算力（T4×2、限时）内解 50 道奥数题（整数答案）。真正的考点是**"让小开源模型学会用 Python 当计算器"（工具集成推理 TIR）+ 少样本条件下的解码/投票策略 + 抗方差的内部验证**。1st 靠两阶段全参微调把 DeepSeekMath-7B 变成"推理 agent"；3rd 甚至**完全不微调**、只靠 vLLM 大候选 + 自研打分规则拿到第 3。

| 关键数字 | 值 | 来源 |
| --- | --- | --- |
| 1st（Numina/AI-MO，519303） | 三件套：① **把 DeepSeekMath-Base-7B 微调成"推理 agent"**（语言 + Python REPL 混合求解）② **带代码执行反馈的 TIR 解码算法** ③ 多套内部验证集；训练配方基于 **MuMath-Code 两阶段**（图 1）：Stage1 大规模 CoT 数学数据微调 → Stage2 用 GPT-4 按 **ToRA 格式**（rationales + Python 程序 + 输出 + 执行反馈）生成的合成 TIR 数据再微调；**全参微调**（不用 LoRA/DoRA）；TRL packing（2048 token）、梯度检查点、**DeepSpeed ZeRO-3**；8×H100 训练 10 小时；验证：AMC12 2022–23 的 83 道整数题（模型解出 60–65%，5–10 个种子波动 1–3%）、AIME 22–24、MATH level 4&5（各约 750 题）；另试过 **on-policy KTO**（对 SFT 采样 4 个补全按对错标注后做 KTO）——内部评估比 SFT 高几个百分点、公榜 27/50，但来不及用于终版；更大的模型（InternLM-20B/CodeLlama-33B/Mixtral-8x7B）反而更差且超时；RLOO 无增益；静态 KV cache + torch compile 提速 2–3× 但在 Kaggle T4 上失败 | 519303 |
| 2nd（CMU_MATH，518964） | **SFT + ORM**：微调两个 DeepSeekMath-7B-RL——一个当**策略模型**（生成解法）、一个当**奖励模型**（给解法打分，用于**加权多数投票**）；数据：AMC/AIME/Odyssey-Math 的整数答案题（去掉选择题选项），用 GPT-4 few-shot 采样代码解法并筛出正确解；策略模型 3 epoch、lr 2e-5；奖励模型用 MATH/AIME/AMC/Odyssey 的非负整数答案题训练；全部代码与数据集开源 | 518964 |
| 3rd（517206） | **不微调**：DeepSeek-Math-7B-RL + **vLLM**（KV cache 用 FP16 提分）；每题生成 **120–160 个候选**、迭代次数 >6；当生成没给出答案时，**追加 "The final answer is \boxed{"** 强制其输出答案；每轮把待执行代码并行批量执行；**自研打分规则**：惩罚两类高频错误——小于 10 的数字（多为代码错误）与**出现在题面里的数字**（模型抄题面的概率远高于题面数字恰为答案） | 517206 |
| 社区/事件 | "SymPy is half you need"（86 票）、"20 分不用 probing"（63 票）、外部数据帖（21k/8.8k 题，68–75 票）、**"On Score Variance（洗牌不可避免）"（70 票 / 63 评论）**、提交一度关闭并要求身份验证（92 票）、"首个公榜 ≥20 的公开 notebook 奖 $10k"（84 票） | 社区 |

## 2. 逐方案对照矩阵

| 维度 | 1st（Numina） | 2nd（CMU_MATH） | 3rd |
| --- | --- | --- | --- |
| 模型 | DeepSeekMath-Base 7B（全参微调） | 两个 DeepSeekMath-7B-RL（策略+奖励） | DeepSeek-Math-7B-RL（**不微调**） |
| 训练 | MuMath-Code 两阶段（CoT→TIR） | SFT（GPT-4 代码解）+ 奖励模型 | 无 |
| 解码 | **带执行反馈的 TIR 解码** | **加权多数投票**（ORM 打分） | vLLM 大候选 + 自研打分规则 |
| 验证 | AMC/AIME/MATH-L4&5 多套 + 多种子 | 未详述 | 自建验证 |

## 3. 共识、分歧与裁决

### 共识一：工具集成推理（TIR）是解题核心（1st/2nd/3rd + 86 票 SymPy 帖）

1st 的两阶段 TIR（rationales+Python+输出）；2nd 的策略模型也用代码解采样；3rd 的大候选里每轮并行执行代码。**裁决**：奥数题的"算术/符号计算"应外包给 Python/SymPy，模型只负责规划——这也是小模型能在本场竞争的前提。置信度：高。

### 共识二：解码/投票策略与模型同等重要（1st/2nd/3rd）

1st 专门设计了带执行反馈的解码算法；2nd 用奖励模型做加权多数投票；3rd 靠 120–160 候选 + 惩罚"小题面数字/抄题面"的规则。**裁决**：在固定模型下，"候选生成 + 打分/投票"是独立且高收益的优化维度。置信度：高。

### 共识三：分数方差极大，必须用多种子内部验证（70 票帖 + 1st）

社区专帖论证"洗牌不可避免"；1st 用 5–10 个种子测出 1–3% 波动并据此选模型；公榜早期还出现过提交关闭与身份验证事件。**裁决**：少量题目的准确率指标对采样极敏感；模型选择要看"多种子期望 + 同类验证集"，不看单次公榜。置信度：高。

### 分歧一：微调 vs 不微调

1st/2nd 全参微调（H100×8、10 小时）；3rd 不微调、纯解码策略拿第 3。**裁决**：当基座本身经过数学继续预训练（DeepSeekMath）且算力受限时，"强解码 + 大候选"可逼近微调效果；极端受限时应优先投解码。置信度：中高。

### 事件：KTO 与 RLOO 的对照（1st）

on-policy KTO 让模型比 SFT 好"几个百分点"（公榜 27/50）；RLOO 没有显著增益且迭代慢。**裁决**：离线/近似在线的偏好优化（采样+标注+KTO）比在线 RL 更适合这种"奖励离散 + 生成慢"的场景。置信度：中（单队实验）。

## 4. 证据分级

| 断言 | 等级 | 说明 |
| --- | --- | --- |
| 1st 的两阶段配方、验证集与 KTO 对照 | 自述 + 论文级图 + 公开模型/notebook | 高 |
| 2nd 的 SFT+ORM 与加权投票 | 自述 + 开源代码/数据 | 中高 |
| 3rd 的无微调 + 自研打分规则 | 自述 + 公开代码 | 中高 |
| 分数方差论证 | 社区专帖（63 评论） | 中高 |
| SymPy/TIR 的必要性 | 高票讨论 + 三队实践 | 高 |

## 5. 悬案与缺口（登记）

- 4th–10th 的方案未入库；"SymPy is half you need"（86 票）与"20 分不用 probing"（63 票）未细读；
- "probing"（对公榜的探测）在早期被广泛讨论，其规模与影响未系统整理；
- 提交关闭/身份验证事件的官方结论未记录；
- 归档 6 图：1st 的 MuMath-Code 两阶段图（图 1）与 TIR 示例为关键图证。

## 6. 图表证据

![MuMath-Code 的两阶段训练](../../intel/ai-mathematical-olympiad-prize/bodies/519303_img/01.png)

**图 1**（topic 519303）：Stage 1 = 自然语言推理数据（CoT）微调预训练模型 → MuMath；Stage 2 = 用伪答案→代码嵌套工具交互数据（ToRA 格式：`[Prefix CoT]` + `[Python Code]` + `[Output]`，含执行失败→提示调试→成功→最终答案的循环）再微调 → MuMath-Code。这是"把小模型训练成会用 Python 的推理 agent"的标准配方。

## 7. 出处

- 1st（191 票）：https://www.kaggle.com/competitions/ai-mathematical-olympiad-prize/discussion/519303
- 2nd（352 行处）：https://www.kaggle.com/competitions/ai-mathematical-olympiad-prize/discussion/518964
- 3rd（72 票）：https://www.kaggle.com/competitions/ai-mathematical-olympiad-prize/discussion/517206
- 分数方差（70 票）：https://www.kaggle.com/competitions/ai-mathematical-olympiad-prize/discussion/509388
- SymPy（86 票）：https://www.kaggle.com/competitions/ai-mathematical-olympiad-prize/discussion/494713
- 入门资源（177 票）：https://www.kaggle.com/competitions/ai-mathematical-olympiad-prize/discussion/488264
