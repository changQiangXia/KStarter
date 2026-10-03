# Parkinson's Freezing of Gait Prediction

> `tlvmc-parkinsons-freezing-gait-prediction` ｜ Research ｜ 指标 sklearn_average_precision_score ｜ 1379 队 ｜ 截止 2023-06-08

本页汇总该场 **1 条 ≥50 票 GM 主题帖**、**4 条断言**、**0 条高票评论**。

## GM 主题帖

| 票 | 选手 | 日期 | 主题 |
| --- | --- | --- | --- |
| 62 | [@takoihiraokazu](https://www.kaggle.com/takoihiraokazu) | 2023-06-09 | [2nd place solution](https://www.kaggle.com/competitions/tlvmc-parkinsons-freezing-gait-prediction/discussion/416057) |

## 断言（条件→动作→机制→结果）

| 选手 | 等级 | 阶段 | 动作（节选） | 出处 |
| --- | --- | --- | --- | --- |
| @takoihiraokazu | A | 建模与训练 | 训练用短序列（tDCS FOG 1000、DeFog 5000）、推理用长序列（3000 到 5000、15000 到 30000），只用预测窗口中间段（如 750 到 2250、 | [tlvmc-parkinsons-freezing-gait-prediction#416057-01](https://www.kaggle.com/competitions/tlvmc-parkinsons-freezing-gait-prediction/discussion/416057) |
| @takoihiraokazu | A | 建模与训练 | GRU + StratifiedGroupKFold by Subject + BCEWithLogits + AdamW 与 linear warmup（比 cosine CV  | [tlvmc-parkinsons-freezing-gait-prediction#416057-02](https://www.kaggle.com/competitions/tlvmc-parkinsons-freezing-gait-prediction/discussion/416057) |
| @takoihiraokazu | A | 建模与训练 | 用 notype 数据与 Event 列构造硬伪标签（三目标最高预测值决定，Event=1 才置 1）；两轮伪标签：CV 从 0.279 到 0.306、0.313，加大 GRU  | [tlvmc-parkinsons-freezing-gait-prediction#416057-03](https://www.kaggle.com/competitions/tlvmc-parkinsons-freezing-gait-prediction/discussion/416057) |
| @takoihiraokazu | A | 验证设计 | 用 public 分数做模型选择，用 CV 指导序列长度；最终 CV 0.548 / public 0.530 / private 0.450 | [tlvmc-parkinsons-freezing-gait-prediction#416057-04](https://www.kaggle.com/competitions/tlvmc-parkinsons-freezing-gait-prediction/discussion/416057) |

## 高票评论

_无 ≥10 票评论_

## 关联资产

- 深读：`analysis/deep/tlvmc-parkinsons-freezing-gait-prediction.md`
- 结构化摘要：`notes/tabular/tlvmc-parkinsons-freezing-gait-prediction.md`
- 归档讨论区：`intel/tlvmc-parkinsons-freezing-gait-prediction/`（主题 1 条有 ≥50 票帖，图证 0 个）
