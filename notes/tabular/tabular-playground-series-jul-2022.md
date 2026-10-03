# Tabular Playground Series - Jul 2022（聚类赛，ARI，逆向真实簇结构）

> 主题：tabular ｜ 子类：— ｜ 领域：—（合成数据聚类） ｜ 类别：Playground
> 截止：2022-07-31 ｜ 队伍数：1253 ｜ 机制：标准赛 ｜ 指标：Adjusted Rand Index（ARI）
> 数据来源：`intel/tabular-playground-series-jul-2022/`（80 条主题索引 + 6 篇 write-up 正文）

## 1. 任务与数据（罕见的聚类赛）

- 目标：把样本聚成 7 个簇（ARI 评估）；14 个变量有效（7 个整数 f_07–f_13、7 个浮点 f_22–f_28）。
- 真实结构（1st 逆向）：
  - 数据实际由 **42 个簇 = 7 组 × 6 子簇**构成，评估按 7 组给标签；
  - 整数变量只随 7 组变化（组间均值/协方差独立）；浮点变量中 5 个相关块（均值 −1/+1，5×5 协方差）+ 2 个标准正态噪声维；
  - 14×14 协方差 = 7×7 整数块 + 5×5 浮点块 + 2×2 单位阵。

## 2. 验证方案

- ARI 无法用普通 CV 直接优化 → 用"能否复现已知结构"与 LB 反馈驱动；社区帖讲解 ARI 的性质与聚类评估（含 UMAP 可视化簇结构）。

## 3. 模型家族

| 方案 | 使用者层次 | 关键点 | 出处 |
| --- | --- | --- | --- |
| 自定义 EM（按逆向出的混合结构建模） | 1st | 42 组件 GMM 探明结构 | topic 341023 |
| 聚类集成方法讨论 | 社区 | 共识矩阵/投票式聚合 | topic 335078 |
| ARI 与聚类分析入门 | 社区 | 指标性质 | topic 334541 |

## 4. 关键技巧

- **发现路线的可复刻细节**（1st）：对浮点列跑 `GaussianMixture(n_components=42)` 看均值 → 怀疑真实组件数；再读 `BayesianGMMClassifier` 源码发现它用 7×7=49 组件反而更好 → 推断每组 6 子簇、共 42。
- 整数变量的分布被识别为混合 Poisson（无法解析建模）→ 幂变换后按多元正态处理（作者自评"这里最可改进"）。
- 聚类赛的"结构逆向"等价于表格赛的特征工程：一旦结构正确，EM 几乎自动得分。
- 聚类集成（共识/投票）与 UMAP 可视化是常规辅助工具。

## 5. 可迁移性评估

- **可直接迁移**：用 GMM 组件数/均值探结构；读库源码反推设计假设（别人的 bug 可能是你的线索）；块状协方差分解；幂变换处理计数型变量。
- **需要前提**：数据确为"生成自混合模型"；有可用的无监督探索工具。
- **不建议照搬**：把 ARI 当可微指标直接调参；忽略评估语义（按 7 组而不是 42 簇计分）。

## 6. 对新手的关键提示

- 聚类赛的玩法是"逆向数据生成器"：GMM/UMAP 看结构 + 读生成代码，比调聚类参数有效得多。
- "库里看起来怪的地方"（这里是 49 组件）常藏着数据真相。
- 指标不是模型 loss：ARI 类指标需要"结构正确 + 标签映射"两个环节都对。

## 8. 轻读结论（2026-10 补）

**一句话**：Kaggle 首个无监督聚类赛（ARI）：1st 把结构完全逆向出来——**42 个高斯子簇 = 7 组 × 6 子簇**，只有 14 个变量相关（7 整数 + 7 浮点），浮点 5 个相关（均值 ±1）+ 2 个标准正态；据此写"硬编码浮点均值的自定义 EM"夺冠；整数列来自未公开的混合泊松，只能 power transform（作者自评最大改进空间）。

- 1st（341023）：`GaussianMixture(42)` 发现结构；线索来自 BayesianGMMClassifier 源码（7×7=49）；整数均值/协方差只随 7 组变化。
- 收官经验（340874）：ARI 定义、缩放、Elbow、丢特征、分布检验、可视化、聚类算法清单、聚类集成内存难题、伪标签转监督。
- 聚类集成（335078）：共现稀疏矩阵 → 均值/中位数 → 阈值 0.5 → 重建标签。
- 社区：七簇可视化（73 票）、UMAP 更细结构（63 票）、丢 15 列提分（35 票）、ARI 直觉（34 票）。

**裁决**：先诊断真实簇数（Elbow/混合分量）；精简特征；聚类集选用共现矩阵；整数生成机制登记缺口。

**悬案**：2nd–5th 未收录；整数生成模型未定论。

## 9. 图表证据

![聚类集成流程](../../intel/tabular-playground-series-jul-2022/bodies/335078_img/01.png)

**图 1**（topic 335078）：多基聚类 → 集成 → 共识划分 P*。

## 10. 出处

- 1st：逆向结构与自定义 EM：https://www.kaggle.com/competitions/tabular-playground-series-jul-2022/discussion/341023
- 聚类集成方法：https://www.kaggle.com/competitions/tabular-playground-series-jul-2022/discussion/335078
- ARI 与聚类分析：https://www.kaggle.com/competitions/tabular-playground-series-jul-2022/discussion/334541
- 收官经验（66 票）：https://www.kaggle.com/competitions/tabular-playground-series-jul-2022/discussion/340874
- 丢掉 15 个特征（35 票）：https://www.kaggle.com/competitions/tabular-playground-series-jul-2022/discussion/334875
