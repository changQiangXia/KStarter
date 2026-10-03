# Playground Series S3E21（Data-Centric AI：只许改数据，不许改模型）

> 主题：tabular ｜ 子类：— ｜ 领域：—（数据质量专项） ｜ 类别：Playground
> 截止：2023-09-11 ｜ 队伍数：955 ｜ 机制：标准赛（固定模型） ｜ 指标：由主办方固定模型在黑箱上评估
> 数据来源：`intel/playground-series-s3e21/`（80 条主题索引 + 6 篇 write-up 正文）

## 1. 任务与数据（Kaggle 罕见的赛制）

- "Improve a Fixed Model the Data-Centric Way"：**模型由主办方固定**，参赛者只能改进数据（清洗/标注纠错/增删样本）；评分来自固定模型在隐藏测试上的表现。
- 理论背景：MIT DCAI 课程 + Andrew Ng 的 data-centric 宣言——"保持模型固定，迭代改进数据质量"；研究显示自适应改数据常胜过用复杂建模拟合噪声。

## 2. 验证方案

- 固定模型 + 固定划分下的"数据改动 → 分数变化"直接对照；4th 的做法简单直接：**按训练误差移除 top-N 离群样本**。

## 3. 模型家族（此处是"数据家族"）

| 方案 | 使用者层次 | 关键点 | 出处 |
| --- | --- | --- | --- |
| 移除 top-N 高误差样本 | 4th | 原想用 cleanlab（不支持回归），退而求其次 | topic 439142 |
| 数据质量论证与 DCAI 资源 | 社区 | 概念与工具链 | topic 433516 |
| 数据清洗清单（66th 等） | 社区 | 纠错/去噪流程 | topic 438609 |

## 4. 关键技巧

- **数据侧操作清单**：纠正标签错误、删除离群/冲突样本、补充困难样本、重标注——本场全部围绕"样本该不该留/改"。
- 回归场景没有现成的 cleanlab 等价工具（4th 的踩坑）→ 用"训练误差排序"近似找出坏样本。
- 与常规比赛的反转：**模型固定时，收益全部来自数据**——检验"清洗到底值多少分"的干净实验台。

## 5. 可迁移性评估

- **可直接迁移**：按误差/置信度排序清洗样本；数据缺陷的假设-验证循环；"先修数据再修模型"的优先级。
- **需要前提**：能观测到数据改动对固定评估的影响；样本量不大（人工/半自动清洗可行）。
- **不建议照搬**：无验证地删样本（可能删掉边界信号）；把清洗当一次性动作而非迭代循环。

## 6. 对新手的关键启示

- 这是最纯粹的"数据质量决定模型上限"的课堂：同一模型，不同数据版本，分数差距就是清洗的价值。
- 学会用训练误差/置信度给样本排序——普遍适用的坏样本发现法。
- DCAI 的技能栈（审计、纠错、覆盖）在真实行业里比调参更常用。

## 8. 轻读结论（2026-10 补）

**一句话**：罕见的"模型固定、只许改数据"赛制：有效手段 = **异常值/错误值处理**（物理范围截断+迭代插补、IsolationForest 行/列过滤、移除 top-N 误差样本）与主动学习/伪标签；但清洗收益高度不确定——66th 自述"原样提交原始数据是第二好"，未修改的 sample_submission 进私榜前 200，且赛中指标从 MAE 改为 RMSE。

- 66th（438609）：Censor（物理范围，`O2_1` 最优 4.5–14.3）+ IterativeImputer + RF，区间当超参搜索。
- 23rd（438824）：IsolationForest 行版私 1.01699（23rd）；逐列版私 1.01535（估 12th）未被选中。
- Missed 2nd（438635）：主动学习私 1.00889，未选中（截图）。
- 4th（439142）：移除 top-N 误差样本；MIT DCAI 课程；cleanlab 不适用回归。
- 社区：伪标签有效（32 票）、原始 train 有危险（32 票）、单样本的力量（31 票）、IsolationForest 评估（30 票）、别信公榜（20/27）。

**裁决**：把清洗策略参数化进 CV；按清洗强度分档提交；指标/公榜不稳时以 CV 为准；主动学习是重要备选路线。

**悬案**：1st–3rd/5th–22nd 未收录；主动学习细节未公开。

## 9. 图表证据

![未选中的主动学习提交](../../intel/playground-series-s3e21/bodies/438635_img/01.png)

**图 1**（topic 438635）：私榜 1.00889 的主动学习提交未被选中。

## 10. 出处

- Data-centric 方法与理论资源：https://www.kaggle.com/competitions/playground-series-s3e21/discussion/433516
- 4th：Objective remove top-N errors：https://www.kaggle.com/competitions/playground-series-s3e21/discussion/439142
- 66th：数据清洗流程：https://www.kaggle.com/competitions/playground-series-s3e21/discussion/438609
- 23rd：IsolationForest：https://www.kaggle.com/competitions/playground-series-s3e21/discussion/438824
- Missed 2nd：主动学习：https://www.kaggle.com/competitions/playground-series-s3e21/discussion/438635
- 伪标签有效（32 票）：https://www.kaggle.com/competitions/playground-series-s3e21/discussion/433531
