# Google Brain - Ventilator Pressure Prediction

> `ventilator-pressure-prediction` ｜ Research ｜ 指标 Mean Absolute Error ｜ 2605 队 ｜ 截止 2021-11-03

本页汇总该场 **1 条 ≥50 票 GM 主题帖**、**2 条断言**、**1 条高票评论**。

## GM 主题帖

| 票 | 选手 | 日期 | 主题 |
| --- | --- | --- | --- |
| 173 | [@cdeotte](https://www.kaggle.com/cdeotte) | 2021-11-04 | [Single Model Transformer - LB 0.112 - Gold Medal](https://www.kaggle.com/competitions/ventilator-pressure-prediction/discussion/285277) |

## 断言（条件→动作→机制→结果）

| 选手 | 等级 | 阶段 | 动作（节选） | 出处 |
| --- | --- | --- | --- | --- |
| @cdeotte | A | 建模与训练 | 发布 TensorFlow transformer（只用 encoder）单模；32 folds 各用 100% train 推理 | [ventilator-pressure-prediction#285277-01](https://www.kaggle.com/competitions/ventilator-pressure-prediction/discussion/285277) |
| @cdeotte | C | 建模与训练 | 对比 decoder 层加喂 OOF 预测与只用 encoder：后者最好 | [ventilator-pressure-prediction#285277-02](https://www.kaggle.com/competitions/ventilator-pressure-prediction/discussion/285277) |

## 高票评论

| 票 | 选手 | 日期 | 摘录 | 出处 |
| --- | --- | --- | --- | --- |
| 10 | @cdeotte | 2021-11-04 | Yes. First i use a normal 11 fold CV where each validation set has 9% of data. I tune the learning schedule so | [285277](https://www.kaggle.com/competitions/ventilator-pressure-prediction/discussion/285277) |

## 关联资产

- 深读：`analysis/deep/ventilator-pressure-prediction.md`
- 结构化摘要：`notes/science/ventilator-pressure-prediction.md`
- 归档讨论区：`intel/ventilator-pressure-prediction/`（主题 1 条有 ≥50 票帖，图证 1 个）
