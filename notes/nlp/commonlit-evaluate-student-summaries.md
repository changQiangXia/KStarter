# CommonLit - Evaluate Student Summaries

> 主题：nlp ｜ 子类：— ｜ 领域：教育 ｜ 类别：Featured
> 截止：2023-10-11 ｜ 队伍数：2064 ｜ 机制：代码赛 ｜ 指标：按列加权的 RMSE 均值（内容 + 措辞）
> 数据来源：`intel/commonlit-evaluate-student-summaries/`（120 条主题索引 + 8 篇 write-up 正文）

## 1. 任务与数据

- **预测目标**：对学生的摘要按两个维度打分（内容质量、措辞质量）。
- **决定性特征**：**训练集只有 4 个写作题目（prompt），而测试集有 122 个**——这是一个极端的分布迁移问题，泛化能力决定一切。
- **排行榜特征**：公开榜与私榜大幅抖动，多支队伍提到"幸运的洗牌"。

## 2. 验证方案

| 方案 | 使用者 | 说明 |
| --- | --- | --- |
| 按 prompt 分组验证 | 多队 | 必须按题目分组，否则会严重高估 |
| 关注跨 prompt 稳定性 | 1st | 明确把预算投在"数据质量与多样性"而非技巧 |
| 全量训练 + 多模型集成 | 4th | 用 4 折全量训练的 7 个模型集成 |

## 3. 方案谱系

| 方案 | 名次 | 关键点 |
| --- | --- | --- |
| 4 折 DeBERTa-v3-large + 数据质量优先 | 1st | **只用一个基座模型**，不做花哨技巧；结论是"数据质量与多样性 > 训练技巧" |
| DeBERTa 集成（7 模型全量训练） | 4th | 承认题目数量差异会导致大洗牌 |
| 多模型方案 | 2nd / 5th / 9th | 见讨论区 |

## 4. 关键技巧

- **数据质量与多样性优先**：在只有 4 个题目的条件下，靠扩充/清洗数据提升跨题目泛化。
- **按 prompt 分组做验证**：这是本场唯一的可信验证方式。
- **简单配置 + 稳定训练**：冠军只有一个基座模型，没有复杂技巧。
- **接受不确定性**：多队承认成绩受洗牌影响。

## 5. 可迁移性评估

- **可直接迁移**：
  - **训练/测试的"题目/来源"数量差异**是文本任务最容易被忽略的迁移风险。
  - 分组验证必须按"语义来源"（prompt、作者、主题）而不是随机划分。
  - 数据质量与多样性优于训练技巧（与 Deep Past、LLM Detect 的结论一致）。
- **需要前提**：
  - 需要外部数据或数据增强手段扩充题目覆盖。
- **不建议照搬**：
  - 随机 K 折（会因题目泄漏而虚高）。

## 6. 对新手的关键启示

1. **先看训练集覆盖了多少"来源"**：4 个题目 → 122 个题目是本场全部难度的来源。
2. **验证必须按来源分组**，否则一切指标都是幻觉。
3. **简单模型 + 好数据**依然能赢。
4. 与 LLM Detect、Deep Past 一起看：**"数据质量决定上限"在 NLP 赛里反复出现**。

## 7. 出处

- 讨论区索引：`intel/commonlit-evaluate-student-summaries/topics.md`（120 条）
- 已收录 write-up（8 篇）：
  - 1st（59 票）：https://www.kaggle.com/competitions/commonlit-evaluate-student-summaries/discussion/447293
  - 2nd（142 票）：https://www.kaggle.com/competitions/commonlit-evaluate-student-summaries/discussion/446573
  - 4th（81 票）：https://www.kaggle.com/competitions/commonlit-evaluate-student-summaries/discussion/446524
  - 5th（47 票）：https://www.kaggle.com/competitions/commonlit-evaluate-student-summaries/discussion/446584
  - 9th（58 票）：https://www.kaggle.com/competitions/commonlit-evaluate-student-summaries/discussion/446539
