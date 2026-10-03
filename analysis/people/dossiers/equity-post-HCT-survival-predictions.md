# CIBMTR - Equity in post-HCT Survival Predictions

> `equity-post-HCT-survival-predictions` ｜ Research ｜ 指标 eefs_concordance_index ｜ 3325 队 ｜ 截止 2025-03-05

本页汇总该场 **1 条 ≥50 票 GM 主题帖**、**4 条断言**、**0 条高票评论**。

## GM 主题帖

| 票 | 选手 | 日期 | 主题 |
| --- | --- | --- | --- |
| 115 | [@aerdem4](https://www.kaggle.com/aerdem4) | 2025-03-06 | [2nd Place Solution](https://www.kaggle.com/competitions/equity-post-HCT-survival-predictions/discussion/566522) |

## 断言（条件→动作→机制→结果）

| 选手 | 等级 | 阶段 | 动作（节选） | 出处 |
| --- | --- | --- | --- | --- |
| @aerdem4 | A | 建模与训练 | AutoGluon Medium/High/Best：OOF 0.6884/0.6910/0.6921；public 0.694/0.694/0.695；private 0.697 | [equity-post-HCT-survival-predictions#566522-03](https://www.kaggle.com/competitions/equity-post-HCT-survival-predictions/discussion/566522) |
| @aerdem4 | B | 建模与训练 | 拆成 efs 分类与 efs_time 回归；回归模型把 efs 当额外特征，推理时设 efs=1 | [equity-post-HCT-survival-predictions#566522-01](https://www.kaggle.com/competitions/equity-post-HCT-survival-predictions/discussion/566522) |
| @aerdem4 | B | 特征与数据工程 | R = p(efs=1) 乘 p(efs_time/efs=1)，其中条件概率等于 sigmoid(-regression_prediction)；再训 NN 用树回归预测加近似指 | [equity-post-HCT-survival-predictions#566522-02](https://www.kaggle.com/competitions/equity-post-HCT-survival-predictions/discussion/566522) |
| @aerdem4 | B | 后处理 | calibrated 等于 1/(1+exp(-beta 乘 (raw-gamma)))：OOF 加 0.002，但 public 减 0.001、private 加 0.001 | [equity-post-HCT-survival-predictions#566522-04](https://www.kaggle.com/competitions/equity-post-HCT-survival-predictions/discussion/566522) |

## 高票评论

_无 ≥10 票评论_

## 关联资产

- 深读：`analysis/deep/equity-post-HCT-survival-predictions.md`
- 结构化摘要：`notes/science/equity-post-HCT-survival-predictions.md`
- 归档讨论区：`intel/equity-post-HCT-survival-predictions/`（主题 1 条有 ≥50 票帖，图证 1 个）
