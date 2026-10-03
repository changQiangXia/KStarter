# Playground Series S4E12 - 保险保费预测（RMSLE，编码乘法与 GPU 蛮力搜索）

> 主题：tabular ｜ 子类：— ｜ 领域：保险（合成数据） ｜ 类别：Playground
> 截止：2024-12-31 ｜ 队伍数：2390 ｜ 机制：标准赛 ｜ 指标：RMSLE
> 数据来源：`intel/playground-series-s4e12/`（80 条主题索引 + 6 篇 write-up 正文）

## 1. 任务与数据

- 预测目标：保险保费（RMSLE）；合成数据（此数据集后经 S5E9 的检验被判定为"原数据随机"，但合成痕迹仍可挖）。
- 1st 的背景：前两场 FE 无收益、靠大集成；**本场 FE 是主战场**——单模型 611 特征即可赢。

## 2. 验证方案

- 单一 XGB 全网最强（1st）：CV 1.016（完整版 6 小时 A100）；简化版 229 特征 CV 1.019（T4 2 小时）——**算力换分的透明对照**。
- 编码的折内嵌套：TE 需要 nested fold groupby（10 折版本优于 5 折）。
- 7th：10 模型集成；9th：靠社区帮助的组合。

## 3. 模型家族

| 方案 | 使用者层次 | 关键点 | 出处 |
| --- | --- | --- | --- |
| 单 XGB + 611 特征（类别编码乘法） | 1st | GPU cuDF 蛮力搜索组合 | topic 554328 |
| 10 模型集成 | 7th | 小集成 | topic 554746 |
| "朋友相助"的组合流 | 9th | 社区协作 | topic 554377 |

## 4. 关键技巧（类别编码的工厂化）

- **一列变七列**：任何类别列同时提供 label + TE(mean/median/min/max/nunique) + CE 七种表示，让 GBDT 多角度读取同一列。
- **组合爆炸 + GPU 筛选**：23 个原始列的全部 2–6 元组合 = **14.5 万候选列**；对每个组合生成新列 → 嵌套折 TE/CE → 训练小 XGB 评估增量 → 只保留提升 CV 的（数天 GPU 跑出 170 个强组合，公开最佳 20 个）。
- **数值列当类别**：对数值列做 TE/CE 并参与组合——在合成数据上常有效。
- 提示：这正是 cdeotte 一脉的"编码乘法"体系在本系列的标准形态，可直接作为新 Playground 的起手式。

## 5. 可迁移性评估

- **可直接迁移**：七编码模板；类别组合的 GPU 蛮力筛选流程；嵌套折 TE；"算力-分数"透明对照（611 vs 229 特征）。
- **需要前提**：GPU + cuDF（组合搜索开销大）；长时间训练预算。
- **不建议照搬**：无筛选地把全部组合塞进模型（内存与过拟合双风险）；小数据场照抄 611 特征规模。

## 6. 对新手的关键启示

- 合成数据的"可挖性"很大程度在类别编码空间：先把七编码模板跑一遍再谈模型。
- 特征搜索可以工程化：写个 for 循环让 GPU 过夜筛组合，比人工想特征高效一个量级。
- 同一方案给"简化版"是种美德：别人能跑得动，才可能被复用与引用（1st 提供 T4 版）。

## 7. 出处

- 1st：单模型与编码乘法（611 特征）：https://www.kaggle.com/competitions/playground-series-s4e12/discussion/554328
- NAN 与目标的关系分析：https://www.kaggle.com/competitions/playground-series-s4e12/discussion/552165
- 9th：社区互助的组合：https://www.kaggle.com/competitions/playground-series-s4e12/discussion/554377
- 7th：10 模型集成：https://www.kaggle.com/competitions/playground-series-s4e12/discussion/554746
