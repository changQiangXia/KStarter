# Playground Series S3E5（QWK，回归 + 阈值优化器）

> 主题：tabular ｜ 子类：— ｜ 领域：—（合成数据） ｜ 类别：Playground
> 截止：2023-02-13 ｜ 队伍数：901 ｜ 机制：标准赛 ｜ 指标：Cohen Kappa（Quadratic Weights, QWK）
> 数据来源：`intel/playground-series-s3e5/`（80 条主题索引 + 6 篇 write-up 正文）

## 1. 任务与数据

- 目标：有序类别评分预测，QWK 指标（与二次加权 Cohen Kappa 等价：`cohen_kappa_score(weights='quadratic')`）。
- QWK 的性质：对"隔档错误"按距离平方惩罚；**有序回归 + 阈值切割**是标准解法。

## 2. 验证方案

- 1st：StratifiedKFold（类别不平衡），实测 K=10 比 K=5 可靠；**每折在验证预测上拟合阈值优化器**（OptimizedRounder），测试集用折平均切割值，再四舍五入取整。

## 3. 模型家族

| 方案 | 使用者层次 | 关键点 | 出处 |
| --- | --- | --- | --- |
| 单模型 RAPIDS XGB + 阈值优化 | 1st | 不用集成/外部数据/FE | topic 387882 |
| 6 个公开 notebook 的众数集成 | 3rd | 简单投票 | topic 386683 |
| QWK 指标理解 | 社区 | 等价实现与解释 | topic 382421 |

## 4. 关键技巧

- **回归 + OptimizedRounder**（本场战术核心）：先当回归训（squarederror），再用验证集搜索最优切割点转标签；逐折拟合、折平均后取整。
- 1st 的反潮流三件事：**不用集成（单 XGB）**、不用额外数据（原数据在本场"过度拟合本地 CV"）、不做 FE（尝试后 CV 变差，全部移除）——再次证明"做减法"也能夺冠。
- GPU 加速（RAPIDS）让"单模型快速迭代"成为最优路径。
- 众数集成公开 notebook（3rd）说明本场社区方案高度同质。

## 5. 可迁移性评估

- **可直接迁移**：有序回归的阈值优化流程（QWK/Kappa 类指标的标准件）；逐折拟合切割值的防泄漏细节；"单模型 + 快速迭代"路线。
- **需要前提**：目标有序；指标为 Kappa/QWK 族。
- **不建议照搬**：默认堆集成（本场单模夺冠）；无差别使用外部数据（本场伤 CV）。

## 6. 对新手的关键启示

- QWK 类任务的分数有两段：**回归能力 + 切割点优化**——后者常被忽视却收益显著。
- "少即是多"的又一案例：删掉 FE、集成与外部数据后反而夺冠。
- 阈值必须在验证集上拟合并防泄漏（逐折），不能拿全量 OOF 一刀切。

## 8. 轻读结论（2026-10 补）

**一句话**：QWK + 稀有类（3/4/8）→ **保守预测 + 回归/取整**是最优形态：1st 用单 XGBoost（GPU）+ OptimizedRounder 阈值拿第 1；3rd 用 6 份公开 notebook 的加权众数拿第 3；4th 造了 1,466 个模型、最终用 25 模型 Ridge 栈，却弃用了私榜 0.60201（=第 1）的 CatBoost。

- 1st（387882）：单 RAPIDS XGB、StratifiedKFold 10、无 FE、不用原始数据；每折在验证预测上拟合 Rounder；Optuna 直接优化 QWK。
- 4th（386645）：对抗验证 AUC 0.6321（去重后）→ 混合训练、竞赛评估；FE 用相关"分散评级"（density/alcohol）；混淆矩阵证明保守 > 冒险。
- 3rd（386683）：加权众数（一份 notebook 双权重 + 类别权重）；另一份提交本可第 1。
- 14th（386627）：NN + 类别权重 CE `[1.10,1.5,1,1,1.5,1.5]`。
- 社区：FE 帖（67 票）、QWK 解释（56 票）、"这是彩票吗"（36 票）、4 特征 XGB（31 票）、回归化（29 票）、Rounder（34 票）。

**裁决**：序数指标先回归再拟合切分点；稀有类预测要按期望扣分把关（宁保守）；提交保留"最强保守 + 结构不同"两条线；原始数据先对抗验证。

**悬案**：2nd、5th–13th 未收录；彩票讨论的统计细节未读。

## 9. 图表证据

![Density/Alcohol 的评级分布](../../intel/playground-series-s3e5/bodies/386645_img/02.png)

**图 1**（topic 386645）：density/alcohol 把评级摊开。

![最优模型的混淆矩阵](../../intel/playground-series-s3e5/bodies/386645_img/04.png)

**图 2**（topic 386645）：预测集中在 5/6/7。

## 10. 出处

- 1st：单模型 + 阈值优化（RAPIDS XGB）：https://www.kaggle.com/competitions/playground-series-s3e5/discussion/387882
- 3rd：公开 notebook 众数集成：https://www.kaggle.com/competitions/playground-series-s3e5/discussion/386683
- QWK 指标理解：https://www.kaggle.com/competitions/playground-series-s3e5/discussion/382421
- 4th（48 票）：https://www.kaggle.com/competitions/playground-series-s3e5/discussion/386645
- 14th NN（21 票）：https://www.kaggle.com/competitions/playground-series-s3e5/discussion/386627
- FE 合集（67 票）：https://www.kaggle.com/competitions/playground-series-s3e5/discussion/382698
- 这是彩票吗（36 票）：https://www.kaggle.com/competitions/playground-series-s3e5/discussion/383429
