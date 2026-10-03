# AMP®-Parkinson's Disease Progression Prediction

> `amp-parkinsons-disease-progression-prediction` ｜ Featured ｜ 指标 smape_plus_1 ｜ 1805 队 ｜ 截止 2023-05-18

本页汇总该场 **1 条 ≥50 票 GM 主题帖**、**4 条断言**、**0 条高票评论**。

## GM 主题帖

| 票 | 选手 | 日期 | 主题 |
| --- | --- | --- | --- |
| 150 | [@cdeotte](https://www.kaggle.com/cdeotte) | 2023-05-19 | [4th Place Gold - Single Model RAPIDS cuML SVR!](https://www.kaggle.com/competitions/amp-parkinsons-disease-progression-prediction/discussion/411398) |

## 断言（条件→动作→机制→结果）

| 选手 | 等级 | 阶段 | 动作（节选） | 出处 |
| --- | --- | --- | --- | --- |
| @cdeotte | A | 数据理解 | 做 1000 列随机数并用前向选择：随机数带来的 GroupKFold CV 提升与 protein/peptide 特征相同 → 判定蛋白/肽信号太弱 | [amp-parkinsons-disease-progression-prediction#411398-01](https://www.kaggle.com/competitions/amp-parkinsons-disease-progression-prediction/discussion/411398) |
| @cdeotte | A | 特征与数据工程 | 为每个 visit month 建三态 bool：1=确认就诊、0=确认未就诊、-1=未知（预测未来视野时未知）；单 SVR 只用 11 个特征 | [amp-parkinsons-disease-progression-prediction#411398-02](https://www.kaggle.com/competitions/amp-parkinsons-disease-progression-prediction/discussion/411398) |
| @cdeotte | A | 特征与数据工程 | 把每行展开成 4 行（当前 month 减 0/6/12/24），未知历史用 -1；MLP 10 层 × 24 单元、无 dropout/BN、15 epochs lr 1e-3  | [amp-parkinsons-disease-progression-prediction#411398-03](https://www.kaggle.com/competitions/amp-parkinsons-disease-progression-prediction/discussion/411398) |
| @cdeotte | B | 数据理解 | 观察最终榜：前 18 队 SMAPE 不超过 62.5，其余不低于 68.4，据此判断前 18 队都用了就诊日期信号 | [amp-parkinsons-disease-progression-prediction#411398-04](https://www.kaggle.com/competitions/amp-parkinsons-disease-progression-prediction/discussion/411398) |

## 高票评论

_无 ≥10 票评论_

## 关联资产

- 深读：`analysis/deep/amp-parkinsons-disease-progression-prediction.md`
- 结构化摘要：`notes/science/amp-parkinsons-disease-progression-prediction.md`
- 归档讨论区：`intel/amp-parkinsons-disease-progression-prediction/`（主题 1 条有 ≥50 票帖，图证 3 个）
