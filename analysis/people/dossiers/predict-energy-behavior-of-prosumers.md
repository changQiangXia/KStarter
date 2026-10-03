# Enefit - Predict Energy Behavior of Prosumers

> `predict-energy-behavior-of-prosumers` ｜ Featured ｜ 指标 Mean Absolute Error ｜ 2731 队 ｜ 截止 2024-04-30

本页汇总该场 **2 条 ≥50 票 GM 主题帖**、**8 条断言**、**0 条高票评论**。

## GM 主题帖

| 票 | 选手 | 日期 | 主题 |
| --- | --- | --- | --- |
| 178 | [@hydantess](https://www.kaggle.com/hydantess) | 2024-02-02 | [1st place solution](https://www.kaggle.com/competitions/predict-energy-behavior-of-prosumers/discussion/472793) |
| 78 | [@aerdem4](https://www.kaggle.com/aerdem4) | 2024-02-01 | [Public 10th Place Solution (Private 11th)](https://www.kaggle.com/competitions/predict-energy-behavior-of-prosumers/discussion/472537) |

## 断言（条件→动作→机制→结果）

| 选手 | 等级 | 阶段 | 动作（节选） | 出处 |
| --- | --- | --- | --- | --- |
| @aerdem4 | A | 建模与训练 | 按 (is_business, is_consumption) 分 4 组；baseline = max(target_lag2, lag4, lag7)；新目标 = (targe | [predict-energy-behavior-of-prosumers#472537-02](https://www.kaggle.com/competitions/predict-energy-behavior-of-prosumers/discussion/472537) |
| @aerdem4 | A | 后处理 | 对每个 prediction_unit_id 计算 lag2/3/4 误差均值，把 0.2×平均误差加回预测作为修正项 | [predict-energy-behavior-of-prosumers#472537-03](https://www.kaggle.com/competitions/predict-energy-behavior-of-prosumers/discussion/472537) |
| @aerdem4 | A | 工程/流程 | 每 8 天用 GPU 重训 XGB；最后 9 个月切 3 折验证 + public LB 当第 4 折（3 折 CV 35.73 对 public 61.32）；与公开最佳 ker | [predict-energy-behavior-of-prosumers#472537-04](https://www.kaggle.com/competitions/predict-energy-behavior-of-prosumers/discussion/472537) |
| @hydantess | B | 建模与训练 | 4 个 XGBoost（2 目标 × 2 状态）+ 2 个 GRU，共享同一套 600 特征；test 在线更新 1 次到 3 次逐步提升 | [predict-energy-behavior-of-prosumers#472793-01](https://www.kaggle.com/competitions/predict-energy-behavior-of-prosumers/discussion/472793) |
| @hydantess | B | 验证设计 | 前 500 天训练，其余全部作 holdout 验证；只看最终总分不看单模 | [predict-energy-behavior-of-prosumers#472793-02](https://www.kaggle.com/competitions/predict-energy-behavior-of-prosumers/discussion/472793) |
| @hydantess | B | 工程/流程 | 放弃用更多模型冲公开榜，改为每月用更少模型重训，优先保证私有期可更新 | [predict-energy-behavior-of-prosumers#472793-03](https://www.kaggle.com/competitions/predict-energy-behavior-of-prosumers/discussion/472793) |
| @aerdem4 | B | 建模与训练 | 分别训 weather forecast-only 与 weather history-only 模型（目标均为 target/installed_capacity），再用它们的输 | [predict-energy-behavior-of-prosumers#472537-01](https://www.kaggle.com/competitions/predict-energy-behavior-of-prosumers/discussion/472537) |
| @hydantess | C | 复盘与流程 | 记录无效方向：solar features、1dcnn 与 transformer、GRU 多日输入、按 is_business 拆分模型 | [predict-energy-behavior-of-prosumers#472793-04](https://www.kaggle.com/competitions/predict-energy-behavior-of-prosumers/discussion/472793) |

## 高票评论

_无 ≥10 票评论_

## 关联资产

- 深读：`analysis/deep/predict-energy-behavior-of-prosumers.md`
- 结构化摘要：`notes/tabular/predict-energy-behavior-of-prosumers.md`
- 归档讨论区：`intel/predict-energy-behavior-of-prosumers/`（主题 2 条有 ≥50 票帖，图证 0 个）
