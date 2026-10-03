# NeurIPS - Ariel Data Challenge 2025

> `ariel-data-challenge-2025` ｜ Featured ｜ 指标 Ariel Gaussian Log Likelihood ｜ 860 队 ｜ 截止 2025-09-24

本页汇总该场 **1 条 ≥50 票 GM 主题帖**、**5 条断言**、**0 条高票评论**。

## GM 主题帖

| 票 | 选手 | 日期 | 主题 |
| --- | --- | --- | --- |
| 56 | [@jeroencottaar](https://www.kaggle.com/jeroencottaar) | 2025-09-30 | [1st place solution: Bayesian Inference, of course](https://www.kaggle.com/competitions/ariel-data-challenge-2025/discussion/609888) |

## 断言（条件→动作→机制→结果）

| 选手 | 等级 | 阶段 | 动作（节选） | 出处 |
| --- | --- | --- | --- | --- |
| @jeroencottaar | A | 建模与训练 | 预处理（counts 到幅度信号 S(λ,t)）→ 贝叶斯推断（transit depth D(λ) 与不确定度 σ(λ)）→ fudging（在训练集上拟合后处理修正） | [ariel-data-challenge-2025#609888-01](https://www.kaggle.com/competitions/ariel-data-challenge-2025/discussion/609888) |
| @jeroencottaar | A | 特征与数据工程 | jitter 形状在色散轴近似求和为零（所以简单求和可用）；需处理无效像素、非泊松噪声、jitter 不完全归零、常数背景；作者花一半以上时间，仍只比简单求和提升约 0.01 | [ariel-data-challenge-2025#609888-02](https://www.kaggle.com/competitions/ariel-data-challenge-2025/discussion/609888) |
| @jeroencottaar | A | 建模与训练 | 迭代线性化：BI 求解 → 在新后验均值处线性化 → 重复，每步用梯度下降更新唯一超参（深度缩放）；起点：深度与 mid-time 网格搜索 → BFGS 拟合漂移与参数（只用 A | [ariel-data-challenge-2025#609888-03](https://www.kaggle.com/competitions/ariel-data-challenge-2025/discussion/609888) |
| @jeroencottaar | A | 复盘与流程 | 按传感器拟合 depth 均值（常数偏移、乘子、依赖 u0）与不确定度（12 参数）；无 fudging 今年约 20 名、去年能第一 → 说明先验没有准确描述合成过程；作者怀疑  | [ariel-data-challenge-2025#609888-04](https://www.kaggle.com/competitions/ariel-data-challenge-2025/discussion/609888) |
| @jeroencottaar | A | 复盘与流程 | 简化 loader（无 jitter/背景处理）-0.013；不裁剪可疑 transit 首尾 -0.002；去掉 GP -0.007；去掉 PCA -0.011；关闭全部 fud | [ariel-data-challenge-2025#609888-05](https://www.kaggle.com/competitions/ariel-data-challenge-2025/discussion/609888) |

## 高票评论

_无 ≥10 票评论_

## 关联资产

- 深读：`analysis/deep/ariel-data-challenge-2025.md`
- 结构化摘要：`notes/science/ariel-data-challenge-2025.md`
- 归档讨论区：`intel/ariel-data-challenge-2025/`（主题 1 条有 ≥50 票帖，图证 5 个）
