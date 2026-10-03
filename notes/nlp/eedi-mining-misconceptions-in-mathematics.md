# EEDI - Mining Misconceptions in Mathematics

> 主题：nlp ｜ 子类：— ｜ 领域：教育 ｜ 类别：Featured
> 截止：2024-06-XX ｜ 队伍数：1400+ ｜ 机制：代码赛 ｜ 指标：MAP@25（排序）
> 数据来源：`intel/eedi-mining-misconceptions-in-mathematics/`（80 条主题索引 + 6 篇 write-up 正文）

## 1. 任务与数据

- 预测目标：给定诊断性数学选择题、正确答案与学生选错的答案，从 **2500+ 个误解（misconception）库**中推荐最相关的 25 个并排序。
- 数据形态：文本（题目 + 选项 + 误解描述）；**标签空间巨大且长尾**。
- 构造陷阱：
  - 大量误解类别在训练集中完全没有样本（长尾极端）。
  - 是典型的"**检索 + 重排**"问题，而非普通分类。

## 2. 验证方案

| 方案 | 使用者 | 说明 |
| --- | --- | --- |
| MAP@25 与训练对齐的留出验证 | 多队 | 排序指标需按 k 截断评估 |
| 按误解类别检查覆盖率 | 5th | 关注训练集未覆盖的类别 |

## 3. 方案谱系

| 方案 | 名次 | 关键点 |
| --- | --- | --- |
| 检索-重排框架的深度改造 | 1st | 指出标准 retrieve-rerank 框架"看似自然但有坑"，并做了针对性改造 |
| **LLM 合成数据补齐长尾类别** | 5th | 对训练集缺失的每个 MisconceptionId 用 few-shot 生成题目；few-shot 样本挑选**语义相近的 MisconceptionName** |
| "Magic Boost" 方案 | 3rd | 见讨论区 |

## 4. 关键技巧

- **检索 + 重排**：2500+ 类别的排序问题必须用检索式架构。
- **合成数据覆盖长尾**：为缺失类别生成样本，且**用语义近邻挑选 few-shot 示例**（不是随机挑）。
- **文本表示**：题目、选项、误解描述需要统一编码后比对。
- 注意：MAP@25 的评价方式决定了"召回靠前"比"精确排序尾部"更重要。

## 5. 可迁移性评估

- **可直接迁移**：
  - **大标签空间 → 检索/重排架构**，而不是分类头。
  - 用 LLM 为缺失类别合成训练样本，并用语义近邻做 few-shot。
  - 排序指标要按 k 截断评估。
- 需要前提：LLM 生成资源；嵌入检索基础设施。
- 不建议照搬：把 2500 类当分类问题处理。

## 6. 对新手的关键启示

1. **类别多到一定程度，问题就从"分类"变成"检索"**。
2. **长尾类别靠合成数据补**，而 few-shot 的挑选策略决定合成质量。
3. 先读清指标（MAP@25）再决定优化重心。

## 7. 出处

- 讨论区索引：`intel/eedi-mining-misconceptions-in-mathematics/topics.md`（80 条）
- 已收录 write-up（6 篇）：
  - 1st 详细（177 票）：https://www.kaggle.com/competitions/eedi-mining-misconceptions-in-mathematics/discussion/551688
  - 1st 摘要（127 票）：https://www.kaggle.com/competitions/eedi-mining-misconceptions-in-mathematics/discussion/551402
  - 3rd（63 票）：https://www.kaggle.com/competitions/eedi-mining-misconceptions-in-mathematics/discussion/551498
  - 5th（76 票）：https://www.kaggle.com/competitions/eedi-mining-misconceptions-in-mathematics/discussion/551391
