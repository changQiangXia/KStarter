# Playground Series S3E12（AUC，"两个特征就够了"与轮廓图诊断）

> 主题：tabular ｜ 子类：— ｜ 领域：—（合成数据） ｜ 类别：Playground
> 截止：2023-04-17 ｜ 队伍数：1088 ｜ 机制：标准赛 ｜ 指标：ROC AUC
> 数据来源：`intel/playground-series-s3e12/`（80 条主题索引 + 6 篇 write-up 正文）

## 1. 任务与数据

- 小数据二分类（AUC）；关键结构：**只用 `cond` 与 `calc` 两个特征即可超过全特征模型**（ExtraTrees：0.817 vs 0.803）。
- 数据点稀少（社区展示全量散点图）——高维下过拟合几乎不可避免，减维是本场主线。

## 2. 验证方案

- **1000 折级验证**：`RepeatedStratifiedKFold(n_splits=10, n_repeats=100)` 让"两特征 vs 全特征"的差异无可争辩。
- "为什么不能用 train_test_split"（社区帖）：小数据下单次划分方差过大，必须用重复 CV。
- 两特征空间的**轮廓图（contour）**可肉眼诊断各分类器的过拟合/欠拟合形态（六图对照）。

## 3. 模型家族

| 方案 | 使用者层次 | 关键点 | 出处 |
| --- | --- | --- | --- |
| 只用 cond+calc 的树模型 + 轮廓诊断 | 社区分析 | 反直觉减维 | topic 400152 |
| 拒绝 train_test_split 的论证 | 社区 | 评估纪律 | topic 401113 |
| 公开方案组合（XGB/LGBM/CAT + Optuna + ROC 曲线） | 24th | 常规线 | topic 402398 |

## 4. 关键技巧

- **先做"最少特征"实验**：在小数据上设定"两特征基线"，往往发现全特征只是噪声来源。
- 2D 投影 + 轮廓图：分类器的决策形态可直接观察；维度一多则无法可视诊断——小数据比赛应尽量保留二维可见性。
- 重复 CV 作为差异的裁判（100 次重复的标准化误差足以区分 0.803/0.817）。

## 5. 可迁移性评估

- **可直接迁移**：最少特征基线；重复 CV（10×100）做显著差异裁判；低维投影诊断；拒绝单次划分。
- **需要前提**：特征数可控、样本量允许重复 CV 的计算。
- **不建议照搬**：大样本高维任务照抄"两特征"（本场是特例）；用单次 train_test_split 下结论。

## 6. 对新手的关键启示

- **特征多 ≠ 模型强**：小数据里"删到最少"往往直接涨分。
- 把分类器画在二维平面上，你会一眼看出谁在过拟合——比看分数更直观。
- 重复 CV 是高性价比的"统计显着性"工具。

## 7. 出处

- 两特征足够 + 轮廓图诊断：https://www.kaggle.com/competitions/playground-series-s3e12/discussion/400152
- 为什么不能用 train_test_split：https://www.kaggle.com/competitions/playground-series-s3e12/discussion/401113
- 24th：常规组合方案：https://www.kaggle.com/competitions/playground-series-s3e12/discussion/402398
