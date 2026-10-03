# Playground Series S3E23 - 代码问题函数预测（AUC，"胜利说明书"）

> 主题：tabular ｜ 子类：— ｜ 领域：软件工程（合成数据） ｜ 类别：Playground
> 截止：2023-10-23 ｜ 队伍数：1702 ｜ 机制：标准赛 ｜ 指标：ROC AUC
> 数据来源：`intel/playground-series-s3e23/`（64 条主题索引 + 6 篇 write-up 正文）

## 1. 任务与数据

- 预测目标：由代码度量特征预测函数是否有问题（AUC）；数据良性、洗牌小（与相邻场次形成对照）。
- 数据语义：McCabe 圈复杂度 / Halstead 操作数与操作符等软件度量——**领域解释帖把每个指标讲清**（topic 444627）。

## 2. 验证方案

- "胜利说明书"帖（本场最有名的指导文）把 CV 放在第一步：**CV 比单次划分精确、比 LB 精确，且 21 天 × 5 提交不可能靠榜评估数百模型**；无 CV 的公开 notebook 直接忽略。

## 3. 模型家族

| 方案 | 使用者层次 | 关键点 | 出处 |
| --- | --- | --- | --- |
| 七模型配方（6 树 + 1 非树）+ HC | 社区指导 | Nyström 核近似 LR 作为非树互补 | topic 445245 |
| 6 树模型 + HC（第 2） | 2nd | 对数变换输入带来小幅提升 | topic 450315 |
| 爬山集成教程 | 社区 | 权重搜索实操 | topic 444784 |

## 4. 关键技巧

- **"七模型处方"**：RF / ET / HistGB / XGB / LGBM / CatBoost + 一个非树模型（首选 Nyström 核近似 + 逻辑回归）——树模型之间多样性不足，必须留一个不同家族的成员。
- **输入对数变换**：2nd 实验显示对多数树/提升模型仍有小幅增益（合成数据偏态时的常规操作）。
- 流程化胜利法：CV 策略 → 逐模型调参 → 集成 → CV 上调集成权重 → 提交；把"评估精度"当作第一资源。
- 领域阅读：Halstead/McCabe 指标含义解释了为何某些组合有效（数据理解先于特征工程）。

## 5. 可迁移性评估

- **可直接迁移**：七模型配方 + 权重搜索流程；选择非树成员的思路（核近似/LR）；对数变换输入；"无 CV 的公开笔记本不看"的筛选纪律。
- **需要前提**：良性数据（结论依赖无强漂移）；中等算力。
- **不建议照搬**：把"配方"当排名保证（榜单仍取决于执行细节）；在不理解指标语义时盲调参。

## 6. 对新手的关键启示

- 本场是**新手流程教学场**：按说明书走完全流程（CV→7 模型→权重），比追求奇技淫巧收获更大。
- 集成至少有"一族之外"的成员；全树集成多样性不足。
- 把 CV 当"评估预算"来管理——几百个模型的取舍全靠它。

## 7. 轻读结论（2026-10 补）

- **流程胜利场**：117 票《Instructions for winning》给出七模型配方（RF/ET/HistGB/XGB/LGBM/CatBoost + 一个非树模型，首选 Nyström 核近似 LR）；CV 是唯一评估预算（3 周、5 次提交/天）；"无 CV 的公开 notebook 直接忽略"；集成权重按 CV 调（445245）。
- **量化对比**：Ensemble(HGB+RF+NY) 0.79220 > ET 0.79136 > HistGB 0.79121 > Nyström-LR 0.79112 > RF 0.79107；非树单模型（Poly-LR/SVC/KNN）明显更弱，价值在集成互补（445245）。
- **#2 八模型**：6 树爬山（允许负权重）LB 0.7907（私榜 0.79379）→ +Nyström LR 0.79099 → +NN 0.79101；log 变换输入对树模型有小幅提升；PCA/t-SNE/聚类全部无效（450315 / 444784 / 445015）。
- **数据审计线索**：准重复观测、完全相关特征、原始数据预处理等索引帖存在，但正文未归档，影响未量化（444988 / 445099 / 444640）。

## 8. 图表证据

![单模型与集成 AUC 对比](../../intel/playground-series-s3e23/bodies/445245_img/01.png)

**图**（topic 445245）：Ensemble(HGB+RF+NY) 0.79220 高于最好单模型 ET 0.79136——多样性集成 > 单模型的直接证据。

![爬山集成提交分数](../../intel/playground-series-s3e23/bodies/450315_img/01.png)

**图**（topic 450315，#2）：爬山集成版本 public 0.7907 / private 0.79379。

## 9. 出处

- 胜利说明书（七模型与 CV 论证）：https://www.kaggle.com/competitions/playground-series-s3e23/discussion/445245
- #2：8 模型集成（对数变换输入）：https://www.kaggle.com/competitions/playground-series-s3e23/discussion/450315
- 爬山集成教程：https://www.kaggle.com/competitions/playground-series-s3e23/discussion/444784
- 数据与领域指标解释：https://www.kaggle.com/competitions/playground-series-s3e23/discussion/444627
- McCabe/Halstead 指标：https://www.kaggle.com/competitions/playground-series-s3e23/discussion/444685
- 入门材料：https://www.kaggle.com/competitions/playground-series-s3e23/discussion/444629
- log 变换提示：https://www.kaggle.com/competitions/playground-series-s3e23/discussion/445015
