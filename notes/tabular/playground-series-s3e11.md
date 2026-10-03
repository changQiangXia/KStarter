# Playground Series S3E11（MSLE，模型动物园与去重加速）

> 主题：tabular ｜ 子类：— ｜ 领域：零售（合成数据） ｜ 类别：Playground
> 截止：2023-04-03 ｜ 队伍数：952 ｜ 机制：标准赛 ｜ 指标：MSLE
> 数据来源：`intel/playground-series-s3e11/`（79 条主题索引 + 6 篇 write-up 正文）

## 1. 任务与数据

- 目标：销售/成本回归（MSLE）；原数据可并入。
- 结构发现（1st）：**`store_sqft` 只有 20 个唯一值——看似数值实为类别**（偏依赖图形态异常，一刀看不出来）；特征选择后训练集存在**大量重复行**。

## 2. 验证方案

- 1st 的结论：train 与 test 同分布 → **CV 完全可信**；据此把预算投给特征子集与模型多样性。
- 3rd 用 KS 检验（`ks_2samp`）核对 train/test（含并入原数据后）的特征分布一致性，作为特征准入/剔除依据。

## 3. 模型家族

| 方案 | 使用者层次 | 关键点 | 出处 |
| --- | --- | --- | --- |
| "模型动物园" + 特征子集混合 | 1st | 去重分组加速 | topic 399401 |
| KS 检验选特征 + 每模型 LOFO + 伪标签 | 3rd | 特征按模型差异化 | topic 399571 |
| 特征工程 Ideas 合集 | 社区 | 工程清单 | topic 396291 |

## 4. 关键技巧

- **重复行分组加速**（1st）：特征选择后把 36 万行压缩成约 3000 组训练——开发迭代速度数量级提升（与 S5E2 孪生行、S3E17 行级编码同族思想）。
- **数值伪装成类别**：对低基数"数值"列做偏依赖图 → 形态像阶梯 → 改为 one-hot/TE（`store_sqft`）。
- **模型动物园 + 树状图分析**：用层次聚类（dendrogram）区分模型簇（原数据特征模型/RF-ET 簇/NN/GBDT 簇），据此补多样性。
- **KS 检验选特征**（3rd）：衡量每个特征在 train/test（及并入原数据后）的分布一致性，剔除漂移特征；再用 **LOFO 重要性逐模型筛选**（不同库给不同子集，尊重 XGB 深度优先 vs LGBM 叶子优先的结构差异）。
- MSLE 的标准处理：log1p 目标 + expm1 还原。

## 5. 可迁移性评估

- **可直接迁移**：重复行压缩训练；偏依赖图识别伪数值列；KS 检验做特征准入；LOFO 的来源（leave-one-feature-out）用法；log 目标。
- **需要前提**：重复行比例高（本场特征选择后极显著）；可做分布检验的样本量。
- **不建议照搬**：所有模型共用同一特征集（3rd 证明按库差异化更优）；不做去重的暴力训练。

## 6. 对新手的关键启示

- **去重不是清洗癖好，是加速器**：训练集压缩到千级分组后，实验吞吐可以翻数倍。
- 用偏依赖图审"低基数数值列"：它们常是伪装类别。
- KS 检验是"特征能否跨 train/test 使用"的体检工具。

## 7. 出处

- 1st：A Zoo of Models（去重与树状图分析）：https://www.kaggle.com/competitions/playground-series-s3e11/discussion/399401
- 3rd：KS 检验 + LOFO + 伪标签：https://www.kaggle.com/competitions/playground-series-s3e11/discussion/399571
- 特征工程 Ideas 合集：https://www.kaggle.com/competitions/playground-series-s3e11/discussion/396291
