# Playground Series S3E25 - 矿物莫氏硬度回归（MedAE，按指标结构加权）

> 主题：tabular ｜ 子类：— ｜ 领域：材料/地质（合成数据） ｜ 类别：Playground
> 截止：2023-12-04 ｜ 队伍数：1632 ｜ 机制：标准赛 ｜ 指标：中位绝对误差（MedAE）
> 数据来源：`intel/playground-series-s3e25/`（74 条主题索引 + 6 篇 write-up 正文）

## 1. 任务与数据

- 预测目标：矿物莫氏硬度（MedAE）；合成数据 + 原数据。
- 指标结构（本场的全部方法都源于此）：**MedAE 只取决于排序后中间那一个样本的误差**——比中位数容易的样本、比中位数难的样本，其误差大小完全不影响得分。

## 2. 验证方案

- 常规 KFold + 按指标特性设计的**样本加权实验**（见下）；分类化视角的中位命中率分析（9 个类别覆盖 89.5% 目标值 ±0.25 内；命中 56% 即可得 MedAE 0.25）。

## 3. 模型家族

| 方案 | 使用者层次 | 关键点 | 出处 |
| --- | --- | --- | --- |
| GBDT + 指标导向样本权重 | 社区分析 | 把模型注意力集中到"可能成为中位数"的样本 | topic 455888 |
| 分类化（分箱）视角 | 社区分析 | 中位指标下分箱命中即满分 | topic 457631 |
| 资源汇编（领域 + 指标 + 往届） | 社区 | 快速入场 | topic 455241 |

## 4. 关键技巧

- **按 MedAE 结构加权训练**：对绝对误差确定性极小（≤0.06）或极大（≥0.7）的样本给 0.01 权重——只让"处于中位附近"的样本主导损失；验证实验 CV 提升 0.03。
- **指标即目标函数**：任何中位/分位类指标（MedAE、median-based）都可以用"按预测误差分层的样本权重"来对齐；与 MAE/RMSE 的直觉不同（后者每个样本都计入）。
- 分箱化思路：把目标当离散等级预测（9 类），命中足够比例即达分位得分——提醒在极端指标下先做"玩法分析"再建模。
- 资源汇编模式（Mohs 硬度领域文档 + MedAE 解释 + 相似比赛）值得作为入场习惯。

## 5. 可迁移性评估

- **可直接迁移**：中位/分位指标的样本加权训练法；"先分析指标数学结构再决定训练目标"的元原则；分箱命中率估算。
- **需要前提**：误差可分层的先验（易/难样本可识别）；指标为分位数类。
- **不建议照搬**：对 RMSE/MAE 类指标做同样的极端加权（完全无效甚至有害）；把分类化当万能（依赖目标密度）。

## 6. 对新手的关键启示

- **读懂指标的数学结构，可能比调模型值钱**：MedAE 只关心一个样本 → 权重设计一下 CV +0.03。
- 遇到罕见指标（MedAE/分位损失），先问"它在奖励什么、忽略什么"，再写第一行代码。
- 社区资源汇编（领域+指标+相似赛）是低成本入场路径。

## 7. 轻读结论（2026-10 补）

- **MedAE 的结构性利用（74 票，455888）**：分数只取决于中位误差那一个样本；对 `AE ≤ 0.06` 或 `≥ 0.7` 的样本给 0.01 权重，同一 LGBM 的 CV **+0.03**。
- **分箱事实（54 票，457631）**：9 个硬度档位覆盖 **89.5%（9533/10406）** 的样本在 ±0.25 内；测试同分布时"猜对约 56% 档位"即可 MedAE=0.25——解释了排行榜大量 0.25 与"零分"讨论。
- **模型/基线**：LAD Stacker LB 0.49737；树模型最低约 0.49；NN 被报告明显更强（455289 / 456721 / 456417 / 458154 引用文化投诉）。
- **CV 与数据**：CV 必须复刻 MedAE 口径（26 票提醒）；准重复/边界样本要审计（17 票）；提交报错帖 36 评论（457338 / 455519 / 456076）。

## 8. 图表证据

![排行榜 Solution 列](../../intel/playground-series-s3e25/bodies/460423_img/01.png)

**图**（topic 460423）：前 8 名分数全部 0.25000，"Solution" 列被标出——分数高度聚集的直接证据。

## 9. 出处

- 别忘记调样本权重（MedAE 加权的证明）：https://www.kaggle.com/competitions/playground-series-s3e25/discussion/455888
- 数据分箱的有趣事实（56% 命中即 0.25）：https://www.kaggle.com/competitions/playground-series-s3e25/discussion/457631
- 入场资源汇编：https://www.kaggle.com/competitions/playground-series-s3e25/discussion/455241
- 引用缺失抱怨：https://www.kaggle.com/competitions/playground-series-s3e25/discussion/458154
- CV 策略提醒：https://www.kaggle.com/competitions/playground-series-s3e25/discussion/457338
- 数据清洗与模型技巧：https://www.kaggle.com/competitions/playground-series-s3e25/discussion/455273
- 准重复/边界警告：https://www.kaggle.com/competitions/playground-series-s3e25/discussion/455519
- LAD Stacker 基线：https://www.kaggle.com/competitions/playground-series-s3e25/discussion/455289
- 200+ 提交卡 0.25：https://www.kaggle.com/competitions/playground-series-s3e25/discussion/459308
