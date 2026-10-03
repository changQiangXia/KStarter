# Playground Series S3E18（分子多标签，AUC，"不是多标签，是两场比赛"）

> 主题：tabular ｜ 子类：— ｜ 领域：化学（合成数据） ｜ 类别：Playground
> 截止：2023-07-10 ｜ 队伍数：1047 ｜ 机制：标准赛 ｜ 指标：ROC AUC（两个目标）
> 数据来源：`intel/playground-series-s3e18/`（66 条主题索引 + 6 篇 write-up 正文）

## 1. 任务与数据

- 预测目标：分子的两个性质（EC1/EC2）——**名称为"多标签"，但社区论证它其实是"两场共享特征的独立比赛"**：两目标的最优模型/超参完全不一致（KNN 对 EC1 需 1180 邻居、EC2 只需 490；EC1 上 RF 胜过 ET，EC2 相反；EC1 接近线性可分而 EC2 完全非线性）。
- 数据清洗：删除 99% 同值的冗余列（HeavyAtomMolWt、fr_COO2）、剔除 FpDensityMorgan1 = −666 的错误记录、去重后剩约 1.6 万行；`mixed_desc` 需拆分。

## 2. 验证方案

- 多标签分层：`RepeatedMultilabelStratifiedKFold`（1st）；11th 则按两个二分类分别验证——两种口径都有前三/前十一。

## 3. 模型家族

| 方案 | 使用者层次 | 关键点 | 出处 |
| --- | --- | --- | --- |
| XGB+LGBM + MultiOutputClassifier + 分组统计特征 | 1st | 单模型双输出的另一条路 | topic 432011 |
| 两目标分别建模（CatBoost/LGBM/XGB 各调各的） | 11th | "两场比赛"论点的落地 | topic 423642 |
| 论证帖：不要一键预测两个目标 | 社区 | 模型选择证据表 | topic 420127 |

## 4. 关键技巧

- **"两场比赛"判据**：对每个目标单独调参，看最优模型是否不同——本场答案是完全不同（线性 vs 非线性）。
- 反方（1st）用 MultiOutput 也赢了：说明多输出不是死路，但需要重型 FE（groupby 组合特征）兜底；路线之争的结论是"按验证结果选"，而非教条。
- 清洗细节优先级高：常数/近常数冗余列、编码错误值（−666）、重复行——合成分子数据的标准三件套。

## 5. 可迁移性评估

- **可直接迁移**："多目标是否同构"的判定实验（各自调参对比最优模型）；多标签分层 CV；合成数据三件套清洗。
- **需要前提**：两目标样本量足够支撑独立调参；计算预算。
- **不建议照搬**：直接给两目标共用一套超参（证据显示会双输）；跳过错误值/冗余列清洗。

## 6. 对新手的关键启示

- "多标签"是标题，不是约束：先验证两目标是否真的同构，再决定拆不拆。
- 判定方法很便宜：各自跑一遍小调参，比较最优模型差异即可。
- 冗余列与错误值清理在分子数据上是最先到手的分。

## 7. 出处

- 1st：双输出 XGB+LGBM + 重型 FE：https://www.kaggle.com/competitions/playground-series-s3e18/discussion/432011
- 11th：两目标分别建模：https://www.kaggle.com/competitions/playground-series-s3e18/discussion/423642
- "不是多标签，是两场比赛"论证：https://www.kaggle.com/competitions/playground-series-s3e18/discussion/420127
