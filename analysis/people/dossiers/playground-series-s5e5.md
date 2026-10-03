# Predict Calorie Expenditure

> `playground-series-s5e5` ｜ Playground ｜ 指标 Mean Squared Log Error ｜ 4316 队 ｜ 截止 2025-05-31

本页汇总该场 **2 条 ≥50 票 GM 主题帖**、**5 条断言**、**2 条高票评论**。

## GM 主题帖

| 票 | 选手 | 日期 | 主题 |
| --- | --- | --- | --- |
| 155 | [@cdeotte](https://www.kaggle.com/cdeotte) | 2025-06-01 | [1st Place - GPU Hill Climbing!](https://www.kaggle.com/competitions/playground-series-s5e5/discussion/582611) |
| 140 | [@cdeotte](https://www.kaggle.com/cdeotte) | 2025-05-02 | [How To Ensemble with RMSLE](https://www.kaggle.com/competitions/playground-series-s5e5/discussion/576111) |

## 断言（条件→动作→机制→结果）

| 选手 | 等级 | 阶段 | 动作（节选） | 出处 |
| --- | --- | --- | --- | --- |
| @cdeotte | A | 集成与融合 | 用 GPU hill climbing 从数百个 GBDT/NN/cuML 模型中选出 7 个（3 个 TE-XGB、1 个 product-XGB、1 个 CatBoost、NN | [playground-series-s5e5#582611-01](https://www.kaggle.com/competitions/playground-series-s5e5/discussion/582611) |
| @cdeotte | A | 建模与训练 | 先训 cuML LinearRegression，做 OOF；用 new_target = old_target - LR_OOF 训 NN，最终预测为 NN + LR；再用 pr | [playground-series-s5e5#582611-02](https://www.kaggle.com/competitions/playground-series-s5e5/discussion/582611) |
| @cdeotte | A | 集成与融合 | 3 个 CV 0.06XX 的 target-encoder XGB 占最终 25% 权重，却把集成 CV 从 0.05890 提到 0.05880、private 从 0.058 | [playground-series-s5e5#582611-04](https://www.kaggle.com/competitions/playground-series-s5e5/discussion/582611) |
| @cdeotte | B | 工程/流程 | 用 5 折 OOF 做 hill climbing 定权；再用 100% train 重训，迭代数取 5 折早停平均值的 1.25 倍（即 1/(K-1) 额外）；最后按 hill | [playground-series-s5e5#582611-03](https://www.kaggle.com/competitions/playground-series-s5e5/discussion/582611) |
| @cdeotte | B | 集成与融合 | 先把各模型预测转 log1p、加权平均、再 expm1；ridge 与 hill climbing 的 OOF 也转到 log1p 空间用 RMSE 优化 | [playground-series-s5e5#576111-01](https://www.kaggle.com/competitions/playground-series-s5e5/discussion/576111) |

## 高票评论

| 票 | 选手 | 日期 | 摘录 | 出处 |
| --- | --- | --- | --- | --- |
| 11 | @cdeotte | 2025-05-05 | Hill climbing is a form of linear regression. We start with N models and hill climbing finds N weights where s | [576111](https://www.kaggle.com/competitions/playground-series-s5e5/discussion/576111) |
| 10 | @cdeotte | 2025-06-01 | Hi @oscarm524 Thanks! I use a trick in all my Kaggle competitions. My OOF and hill climbing use 5-Kfold to fin | [582611](https://www.kaggle.com/competitions/playground-series-s5e5/discussion/582611) |

## 关联资产

- 深读：`analysis/deep/playground-series-s5e5.md`
- 结构化摘要：`notes/tabular/playground-series-s5e5.md`
- 归档讨论区：`intel/playground-series-s5e5/`（主题 2 条有 ≥50 票帖，图证 1 个）
