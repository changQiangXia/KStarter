# Predict Student Performance from Game Play

> 主题：tabular（行为日志）｜ 子类：— ｜ 领域：教育 ｜ 类别：Featured
> 截止：2023-06-28 ｜ 队伍数：2051 ｜ 机制：代码赛 ｜ 指标：Macro F-Score（18 个二分类问题）
> 数据来源：`intel/predict-student-performance-from-game-play/`（120 条主题索引 + 8 篇 write-up 正文）

## 1. 任务与数据

- **预测目标**：由学生在教育游戏中的**操作日志**（事件流、坐标、时间）预测 18 个二分类标签（是否答对/是否完成等）。
- **数据形态**：长事件序列按 session 组织，规模大、噪声高；评测指标是宏平均 F1，**阈值选择对分数影响极大**。
- **构造陷阱：本场存在数据泄漏争议**。参赛者主动上报了测试数据泄漏问题（社区有 "Update on Leaked Competition Data"、"Is Test Data Leak Intentional or Accidental?" 等高票讨论），冠军在 write-up 中专门感谢主办方处理泄漏上报。

## 2. 验证方案

| 方案 | 使用者 | 说明 |
| --- | --- | --- |
| 只用 Kaggle 提供的数据做验证 | 4th | 训练用全量原始数据，验证只在与评测同源的数据上做 |
| 10 袋 × 5 折的重复验证 + 噪声阈值筛选 | 1st | **特征只有在 CV 均值超过"量化后的噪声水平"时才保留** |
| 共识策略 | 1st | 神经网络侧用多数/共识方式确认选择，降低随机性影响 |

## 3. 方案谱系

| 方案 | 名次 | 关键点 |
| --- | --- | --- |
| XGBoost + 自定义 TimeEmbedding 神经网络的融合 | 1st | **时长（duration）是最强信号**；GBDT 侧用多种时间聚合 + 计数，NN 侧用 1D 卷积时间嵌入；特征筛选以"超过噪声水平"为准 |
| Transformer + XGBoost + CatBoost 集成（3 种子 × 5 折）+ 线性回归元模型 | 4th | 通用时间/序号/屏幕坐标差分特征；**阈值影响巨大** |
| 效率优化方案 | 7th（效率第一） | 在同等精度下追求推理效率 |
| 多模型方案 | 9th | 见讨论区 |

## 4. 关键技巧

- **量化噪声水平再决定特征取舍**：把 CV 波动量化成阈值，只有超过噪声的特征才保留——比"凭感觉加特征"稳健得多。
- **时间/时长特征**：事件间隔、累计时长、按类型聚合，是本场的主导信号。
- **自定义时间嵌入**：对时间做 1D 卷积编码，与事件表示结合。
- **阈值选择**：宏 F1 对阈值敏感，必须单独优化。
- **主动报告数据泄漏**：本场社区的处理方式值得记住——发现问题上报而非利用。

## 5. 可迁移性评估

- **可直接迁移**：
  - **把 CV 噪声量化为特征准入阈值**（适用于任何噪声大的比赛）。
  - 时长/间隔类特征在行为日志任务中普遍有效。
  - 宏平均指标必须显式优化每类阈值。
  - 只在与评测同源的数据上验证。
- **需要前提**：
  - 需要大规模事件日志的处理能力（内存/时间）。
- **不建议照搬**：
  - 利用泄漏数据（本场社区选择上报，且规则上通常被禁）。

## 6. 对新手的关键启示

1. **特征是否有效，要用噪声水平来判断**，而不是"CV 涨了 0.000x 就加"。
2. **行为日志类任务先做时间特征**。
3. **阈值是宏平均指标的一半工作**。
4. **发现数据泄漏应上报**——这既是规则要求，也是社区信任的基础。

## 7. 出处

- 讨论区索引：`intel/predict-student-performance-from-game-play/topics.md`（120 条）
- 已收录 write-up（8 篇）：
  - 1st（168 票）：https://www.kaggle.com/competitions/predict-student-performance-from-game-play/discussion/420217
  - 7th 效率第一（102 票）：https://www.kaggle.com/competitions/predict-student-performance-from-game-play/discussion/420119
  - 9th（81 票）：https://www.kaggle.com/competitions/predict-student-performance-from-game-play/discussion/420046
  - 泄漏数据更新（92 票）：https://www.kaggle.com/competitions/predict-student-performance-from-game-play/discussion/396202
  - 泄漏讨论（85 票）：https://www.kaggle.com/competitions/predict-student-performance-from-game-play/discussion/388479
