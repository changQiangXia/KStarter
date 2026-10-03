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

## 8. 轻读结论（2026-10 补）

**一句话**："**复杂 ≠ 更好**"的极端案例：测试集仅 276 条的极小数据上，只用 `cond + calc` 两特征的 ExtraTrees 1000 次重复 CV = 0.817，而全特征只有 0.803；社区统计 16 个公开 notebook 里只有 3 个做了正确 CV——train_test_split 可让模型对差值因种子反转 0.137 AUC。

- 400152（77 票）：两特征 > 全特征；六分类器二维轮廓图直接暴露 RF 过拟合；GAM 平滑稳健。
- 401113（78 票）：8/16 用 train_test_split；Optuna 若用它做目标则超参随机；必须 RepeatedStratifiedKFold。
- #28（402347）：IQR 分位数微调即改变名次；最佳私榜版本未提交（本可第 16）；FE 一动分数就掉。
- #24（402398）：原数据不裁剪 + 逐折 ROC 校准 + 权重/幂平均；按 CV 选提交。
- #8（402416）：两套 FE 双栈（LR 为 L1）平均；"忽略公榜，只看 10 折 CV"。
- 其他：十折不够（47 票）、别忘了 GAM（43 票）、测试集仅 276 条如何防作弊（24 票）。

**裁决**：小样本先做特征删减；验证用重复分层 CV（禁止单一 split 做选择）；用二维决策面诊断；离群规则与提交选择是名次杠杆；复用公开方案前先审计验证协议。

**悬案**：1st–3rd 方案未收录；276 条测试集的探榜风险未定论。

## 9. 图表证据

![六个分类器的二维决策面](../../intel/playground-series-s3e12/bodies/400152_img/01.png)

**图 1**（topic 400152）：cond×calc 的决策面（RF 碎片化=过拟合）。

![公开 notebook 的验证质量](../../intel/playground-series-s3e12/bodies/401113_img/01.png)

**图 2**（topic 401113）：只有 3/16 公开 notebook 验证正确。

## 10. 出处

- 两特征足够 + 轮廓图诊断：https://www.kaggle.com/competitions/playground-series-s3e12/discussion/400152
- 为什么不能用 train_test_split：https://www.kaggle.com/competitions/playground-series-s3e12/discussion/401113
- 24th：常规组合方案：https://www.kaggle.com/competitions/playground-series-s3e12/discussion/402398
- 十折不够（47 票）：https://www.kaggle.com/competitions/playground-series-s3e12/discussion/399869
- 别忘了 GAM（43 票）：https://www.kaggle.com/competitions/playground-series-s3e12/discussion/400005
- #8 双栈（11 票）：https://www.kaggle.com/competitions/playground-series-s3e12/discussion/402416
