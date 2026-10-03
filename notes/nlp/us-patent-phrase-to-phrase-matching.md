# US Patent Phrase to Phrase Matching

> 主题：nlp ｜ 子类：— ｜ 领域：专利文本 ｜ 类别：Featured
> 截止：2022-06-27 ｜ 队伍数：1500+ ｜ 机制：代码赛 ｜ 指标：Pearson 相关（语义相似度）
> 数据来源：`intel/us-patent-phrase-to-phrase-matching/`（80 条主题索引 + 6 篇 write-up 正文）

## 1. 任务与数据

- **预测目标**：给定"锚短语 + 上下文字段"，判断两个专利短语的语义相似度（回归到 0–1）。
- **数据形态**：`anchor`（锚短语）、`target`（目标短语）、`context`（技术领域代码）三元组；**同一 anchor+context 下有多个 target**。
- **构造陷阱**：数据按 `anchor + context` 分组，**天然存在组结构**，随机切分会泄漏；相似度标签是人工标注，含噪声。

## 2. 验证方案

| 方案 | 使用者 | 说明 |
| --- | --- | --- |
| 按 `anchor+context` 分组 CV | 多队 | 避免同组样本跨折 |
| 多模型加权平均 | 8th | 6 个模型（BCE 损失）加权融合 |
| 单模型对照 | 10th | 单模型 public 0.8562 / private 0.8717 |

## 3. 方案谱系

| 方案 | 名次 | 关键点 |
| --- | --- | --- |
| 分组构造 + 单模型 | 10th | "魔法"是**按 `anchor + context` 把目标词聚合成一个附件拼在句尾**，让模型同时看到同组候选 |
| **一次性预测整组目标** + 6 模型加权平均 | 8th | 标题即"Predicting Targets at Once Led Us to Gold" |
| 多模型方案 | 1st / 2nd | 见讨论区 |

## 4. 关键技巧

- **利用组结构**：同一 anchor 下的多个 target 一起喂给模型（列表式输入 / 拼接到句尾），比逐对独立预测更有效。
- **损失函数**：BCE 在此类相似度回归上表现良好。
- **多模型加权融合**：权重按验证集确定。
- **分组验证**：按 `anchor+context` 分组是底线。

## 5. 可迁移性评估

- **可直接迁移**：
  - **利用数据中的分组结构做"批量对比"**（把同组候选一起输入），在推荐/检索/相似度任务中通用。
  - 按分组做交叉验证。
  - BCE 损失用于连续相似度目标。
- **需要前提**：
  - 需要能处理列表式输入的结构（长文本或特殊 token 拼接）。
- **不建议照搬**：
  - 随机切分（组结构泄漏会显著虚高）。

## 6. 对新手的关键启示

1. **先看数据的分组结构**：它决定验证方式，也常常提示更好的建模形式。
2. **"把候选一起给模型看"**比"逐对判断"更强（对比学习思想的朴素版本）。
3. 相似度任务优先试 **BCE + 回归头**。

## 7. 出处

- 讨论区索引：`intel/us-patent-phrase-to-phrase-matching/topics.md`（80 条）
- 已收录 write-up（6 篇）：
  - 1st（176 票）：https://www.kaggle.com/competitions/us-patent-phrase-to-phrase-matching/discussion/332243
  - 2nd（154 票）：https://www.kaggle.com/competitions/us-patent-phrase-to-phrase-matching/discussion/332234
  - 8th（78 票）：https://www.kaggle.com/competitions/us-patent-phrase-to-phrase-matching/discussion/332492
  - 10th（99 票）：https://www.kaggle.com/competitions/us-patent-phrase-to-phrase-matching/discussion/332273
