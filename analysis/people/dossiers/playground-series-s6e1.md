# Predicting Student Test Scores

> `playground-series-s6e1` ｜ Playground ｜ 指标 Root Mean Squared Error ｜ 4317 队 ｜ 截止 2026-01-31

本页汇总该场 **2 条 ≥50 票 GM 主题帖**、**5 条断言**、**0 条高票评论**。

## GM 主题帖

| 票 | 选手 | 日期 | 主题 |
| --- | --- | --- | --- |
| 92 | [@cdeotte](https://www.kaggle.com/cdeotte) | 2026-01-09 | [Improve CV and LB with Pseudo Labels](https://www.kaggle.com/competitions/playground-series-s6e1/discussion/666888) |
| 78 | [@cdeotte](https://www.kaggle.com/cdeotte) | 2026-01-04 | [Basic EDA shows Lots of Linear Relationships!](https://www.kaggle.com/competitions/playground-series-s6e1/discussion/665965) |

## 断言（条件→动作→机制→结果）

| 选手 | 等级 | 阶段 | 动作（节选） | 出处 |
| --- | --- | --- | --- | --- |
| @cdeotte | B | 建模与训练 | 每个 fold 训两次：第一次正常训练并对 val/test 预测；第二次用 X_train 加 X_val 加 X_test 作特征，标签为 y_train 加 oof_pred | [playground-series-s6e1#666888-01](https://www.kaggle.com/competitions/playground-series-s6e1/discussion/666888) |
| @cdeotte | B | 数据理解 | 结论：无 NaN；Age 低基数数值可当类别；许多类别特征有序；除 internet access 外分布近似均匀；study_hours、class_attendance、sle | [playground-series-s6e1#665965-01](https://www.kaggle.com/competitions/playground-series-s6e1/discussion/665965) |
| @cdeotte | C | 建模与训练 | 收益来自更多真实特征：模型（尤其 transformer 的 attention）需要从更多特征组合中学习特征关系；伪标签只是把无标注数据带进训练的手段 | [playground-series-s6e1#666888-02](https://www.kaggle.com/competitions/playground-series-s6e1/discussion/666888) |
| @cdeotte | C | 集成与融合 | 若第二次换模型（如 TabM 到 XGB），除伪标签收益外还叠加热知识蒸馏，让第二个模型达到单独训练难以达到的水平 | [playground-series-s6e1#666888-03](https://www.kaggle.com/competitions/playground-series-s6e1/discussion/666888) |
| @cdeotte | C | 数据理解 | 探索一个特征如何影响另一个特征与目标的关系，用交互复杂度决定 NN、GBDT 与 stacking 的用法 | [playground-series-s6e1#665965-02](https://www.kaggle.com/competitions/playground-series-s6e1/discussion/665965) |

## 高票评论

_无 ≥10 票评论_

## 关联资产

- 深读：`analysis/deep/playground-series-s6e1.md`
- 结构化摘要：`notes/tabular/playground-series-s6e1.md`
- 归档讨论区：`intel/playground-series-s6e1/`（主题 2 条有 ≥50 票帖，图证 1 个）
