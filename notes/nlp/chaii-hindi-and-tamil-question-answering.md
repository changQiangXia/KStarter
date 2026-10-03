# CHAIi - Hindi and Tamil Question Answering

> 主题：nlp ｜ 子类：— ｜ 领域：多语言问答 ｜ 类别：Research
> 截止：2022-XX-XX ｜ 队伍数：1000+ ｜ 机制：代码赛 ｜ 指标：Jaccard / 字符 F1（抽取式问答）
> 数据来源：`intel/chaii-hindi-and-tamil-question-answering/`（80 条主题索引 + 6 篇 write-up 正文）

## 1. 任务与数据

- 预测目标：在印地语与泰米尔语文章中抽取答案片段（抽取式问答）。
- 数据形态：问题 + 上下文 + 答案跨度；**训练数据小且确认有噪声**。
- 构造陷阱：低资源语言的预训练模型有限；标注噪声大；长上下文。

## 2. 方案谱系

| 方案 | 名次 | 关键点 |
| --- | --- | --- |
| **"完全信任公开榜、不追踪本地 CV"** | 1st | 作者明确记录：训练集小且确认噪声大，因此**放弃本地 CV 作为决策依据**，直接用公开榜迭代（他还自嘲这段总结"可能事后变苦涩"） |

## 3. 关键技巧

- **何时可以信公开榜**：当训练数据小且噪声大、本地 CV 无法反映真实泛化时，公开榜可能是更可靠的信号（**前提是评估集足够大**）。
- 多语言模型的选择（XLM-R 类）与长上下文切分。
- 噪声标签的处理（软标签/过滤）。

## 4. 可迁移性评估

- **可直接迁移**：
  - **"信 CV 还是信 LB"是一个需要论证的决策**，不是教条（本场是少见的"信 LB"案例）；
  - 长上下文问答的切分与答案聚合；
  - 噪声标签的处理手段。
- 需要前提：对评估集规模与数据噪声的判断力。
- 不建议照搬：不加论证地盲信任何一侧。

## 5. 对新手的关键启示

1. **"Trust CV"不是教条**——当训练数据小且噪声大时，公开榜可能更可靠（与 ICR/Jigsaw 的两种相反案例对照）。
2. 判断依据是：**评估集大小 + 训练集噪声**。
3. 与 AI4Code、PII Detection 对照：低资源语言任务的通用手段是"多语言预训练模型 + 噪声处理"。

## 6. 出处

- 讨论区索引：`intel/chaii-hindi-and-tamil-question-answering/topics.md`（80 条）
- 已收录 write-up（6 篇）：
  - 1st 只信公开榜（173 票）：https://www.kaggle.com/competitions/chaii-hindi-and-tamil-question-answering/discussion/287923
  - 2nd（59 票）：https://www.kaggle.com/competitions/chaii-hindi-and-tamil-question-answering/discussion/287917
  - 5th（47 票）：https://www.kaggle.com/competitions/chaii-hindi-and-tamil-question-answering/discussion/288049
