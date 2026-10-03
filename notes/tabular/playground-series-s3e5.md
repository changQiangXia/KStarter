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

## 7. 出处

- 1st：单模型 + 阈值优化（RAPIDS XGB）：https://www.kaggle.com/competitions/playground-series-s3e5/discussion/387882
- 3rd：公开 notebook 众数集成：https://www.kaggle.com/competitions/playground-series-s3e5/discussion/386683
- QWK 指标理解：https://www.kaggle.com/competitions/playground-series-s3e5/discussion/382421
