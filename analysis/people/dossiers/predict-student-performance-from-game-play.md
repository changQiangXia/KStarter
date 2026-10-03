# Predict Student Performance from Game Play

> `predict-student-performance-from-game-play` ｜ Featured ｜ 指标 F-Score (Macro) ｜ 2051 队 ｜ 截止 2023-06-28

本页汇总该场 **2 条 ≥50 票 GM 主题帖**、**6 条断言**、**0 条高票评论**。

## GM 主题帖

| 票 | 选手 | 日期 | 主题 |
| --- | --- | --- | --- |
| 228 | [@cdeotte](https://www.kaggle.com/cdeotte) | 2023-02-15 | [How The Game Begins - EDA](https://www.kaggle.com/competitions/predict-student-performance-from-game-play/discussion/387864) |
| 52 | [@takoihiraokazu](https://www.kaggle.com/takoihiraokazu) | 2023-06-29 | [13th place solution](https://www.kaggle.com/competitions/predict-student-performance-from-game-play/discussion/420077) |

## 断言（条件→动作→机制→结果）

| 选手 | 等级 | 阶段 | 动作（节选） | 出处 |
| --- | --- | --- | --- | --- |
| @takoihiraokazu | A | 验证设计 | 训练数据 session_id 前 4 位不超过 2200，验证用 2201 及以上；训练集内 5 折，用 5 个模型集成预测验证集；最终提交在全量数据上 5 折 | [predict-student-performance-from-game-play#420077-01](https://www.kaggle.com/competitions/predict-student-performance-from-game-play/discussion/420077) |
| @takoihiraokazu | A | 建模与训练 | level group 0-4 与 5-12 各一个模型（含目标特征、单模型），13-22 每个 target 单独模型；特征为每 session 的类别计数、数值统计量与下一动作 | [predict-student-performance-from-game-play#420077-02](https://www.kaggle.com/competitions/predict-student-performance-from-game-play/discussion/420077) |
| @takoihiraokazu | A | 建模与训练 | NN=Transformer+GRU（加 GRU 明显提升），每个 level group 单独模型、特征更少；NN CV 0.7010；最终 LGB×0.66 + NN×0.34 | [predict-student-performance-from-game-play#420077-03](https://www.kaggle.com/competitions/predict-student-performance-from-game-play/discussion/420077) |
| @cdeotte | B | 数据理解 | 用开局 11 屏强制对话理解点击约束，区分无效点击与真实选择 | [predict-student-performance-from-game-play#387864-01](https://www.kaggle.com/competitions/predict-student-performance-from-game-play/discussion/387864) |
| @cdeotte | B | 数据理解 | 分别建模：room 坐标用房间边界（首房间 -1064<=x<=926、-393<=y<=327）；screen 坐标用弹窗尺寸（95% 用户不缩放，880x660） | [predict-student-performance-from-game-play#387864-02](https://www.kaggle.com/competitions/predict-student-performance-from-game-play/discussion/387864) |
| @cdeotte | C | 特征与数据工程 | 从开局序列提取行为特征：读每段对话耗时、每次点击位置、首个点击对象、是否点 grampa 身体或脸、是否缩放窗口等；可扩展到 19 房间/23 关卡/11 种动作 | [predict-student-performance-from-game-play#387864-03](https://www.kaggle.com/competitions/predict-student-performance-from-game-play/discussion/387864) |

## 高票评论

_无 ≥10 票评论_

## 关联资产

- 深读：`analysis/deep/predict-student-performance-from-game-play.md`
- 结构化摘要：`notes/tabular/predict-student-performance-from-game-play.md`
- 归档讨论区：`intel/predict-student-performance-from-game-play/`（主题 2 条有 ≥50 票帖，图证 7 个）
