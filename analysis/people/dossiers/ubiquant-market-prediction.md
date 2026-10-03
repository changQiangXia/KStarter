# Ubiquant Market Prediction

> `ubiquant-market-prediction` ｜ Featured ｜ 指标 MeanPearson ｜ 2893 队 ｜ 截止 2022-07-19

本页汇总该场 **1 条 ≥50 票 GM 主题帖**、**4 条断言**、**0 条高票评论**。

## GM 主题帖

| 票 | 选手 | 日期 | 主题 |
| --- | --- | --- | --- |
| 69 | [@hydantess](https://www.kaggle.com/hydantess) | 2022-07-21 | [3rd Place Solution - 5 seeds ensemble transformer](https://www.kaggle.com/competitions/ubiquant-market-prediction/discussion/338561) |

## 断言（条件→动作→机制→结果）

| 选手 | 等级 | 阶段 | 动作（节选） | 出处 |
| --- | --- | --- | --- | --- |
| @hydantess | A | 建模与训练 | 6 层 transformer、max_seq_length 3500、直接优化 PCCLoss；训练 10 epochs 比赛数据加 3 epochs 补充数据 | [ubiquant-market-prediction#338561-01](https://www.kaggle.com/competitions/ubiquant-market-prediction/discussion/338561) |
| @hydantess | A | 特征与数据工程 | 增广：特征级 random zero 加序列级 random mask；验证用最后 k 段（k=100、200、300） | [ubiquant-market-prediction#338561-02](https://www.kaggle.com/competitions/ubiquant-market-prediction/discussion/338561) |
| @hydantess | A | 集成与融合 | 5 seeds 集成；public LB 从 900+ 经过失败后到 7、7、4、3 | [ubiquant-market-prediction#338561-03](https://www.kaggle.com/competitions/ubiquant-market-prediction/discussion/338561) |
| @hydantess | B | 复盘与流程 | 无效：feature clipping、avg features、按 time_id groupby、按 corr 特征选择、样本选择或权重、target 归一化或裁剪；LGB、M | [ubiquant-market-prediction#338561-04](https://www.kaggle.com/competitions/ubiquant-market-prediction/discussion/338561) |

## 高票评论

_无 ≥10 票评论_

## 关联资产

- 深读：`analysis/deep/ubiquant-market-prediction.md`
- 结构化摘要：`notes/tabular/ubiquant-market-prediction.md`
- 归档讨论区：`intel/ubiquant-market-prediction/`（主题 1 条有 ≥50 票帖，图证 0 个）
