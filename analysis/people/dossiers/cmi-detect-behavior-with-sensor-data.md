# CMI - Detect Behavior with Sensor Data

> `cmi-detect-behavior-with-sensor-data` ｜ Featured ｜ 指标 CMI_2025 ｜ 2657 队 ｜ 截止 2025-09-02

本页汇总该场 **2 条 ≥50 票 GM 主题帖**、**9 条断言**、**1 条高票评论**。

## GM 主题帖

| 票 | 选手 | 日期 | 主题 |
| --- | --- | --- | --- |
| 113 | [@daiwakun](https://www.kaggle.com/daiwakun) | 2025-09-03 | [2nd Place Solution](https://www.kaggle.com/competitions/cmi-detect-behavior-with-sensor-data/discussion/603594) |
| 53 | [@w5833946](https://www.kaggle.com/w5833946) | 2025-09-03 | [12th place solution](https://www.kaggle.com/competitions/cmi-detect-behavior-with-sensor-data/discussion/603564) |

## 断言（条件→动作→机制→结果）

| 选手 | 等级 | 阶段 | 动作（节选） | 出处 |
| --- | --- | --- | --- | --- |
| @daiwakun | A | 数据工程 | 按 IMU rotation 是否缺失乘以 THM/TOF 是否缺失训 4 个模型变体 | [cmi-detect-behavior-with-sensor-data#603594-01](https://www.kaggle.com/competitions/cmi-detect-behavior-with-sensor-data/discussion/603594) |
| @daiwakun | A | 建模与训练 | 每积累一批测试序列就用小 LR（5e-5）做一步伪标签微调 | [cmi-detect-behavior-with-sensor-data#603594-04](https://www.kaggle.com/competitions/cmi-detect-behavior-with-sensor-data/discussion/603594) |
| @daiwakun | A | 后处理 | 把 102 类联合概率加 no-repeat 约束建成分配问题（Hungarian 算法，负对数概率为成本），最大化联合对数概率而非逐条 argmax | [cmi-detect-behavior-with-sensor-data#603594-05](https://www.kaggle.com/competitions/cmi-detect-behavior-with-sensor-data/discussion/603594) |
| @w5833946 | A | 数据工程 | IMU rot 归一化到 rot_w 大于 0，用 dot_product(rot,rot[-1]) 恢复符号；手性翻转：acc_x、rot_y、rot_z 取反；不做归一化而用  | [cmi-detect-behavior-with-sensor-data#603564-01](https://www.kaggle.com/competitions/cmi-detect-behavior-with-sensor-data/discussion/603564) |
| @w5833946 | A | 建模与训练 | IMU 分支两个 1DResBlock 加 SCSE（group conv 只在组内交互）；THM 分支两个 1DResBlock 加 SCSE；TOF 分支三个 3DResBlo | [cmi-detect-behavior-with-sensor-data#603564-02](https://www.kaggle.com/competitions/cmi-detect-behavior-with-sensor-data/discussion/603564) |
| @w5833946 | A | 集成与融合 | K 折类秩平均；用不同模型投票，且只保留 CV 好的模型（作者认为投票优于平均，可能因为部分模型过度自信）；单模最佳 CV IMU/All 0.8364/0.9008、public | [cmi-detect-behavior-with-sensor-data#603564-04](https://www.kaggle.com/competitions/cmi-detect-behavior-with-sensor-data/discussion/603564) |
| @daiwakun | B | 数据工程 | 四元数用 6D 表示避免不连续；左利手对特定通道乘 -1、交换 tof_3/tof_5 并水平翻转 2D TOF；训练集中 SUBJ_019262 与 SUBJ_045235 绕  | [cmi-detect-behavior-with-sensor-data#603594-02](https://www.kaggle.com/competitions/cmi-detect-behavior-with-sensor-data/discussion/603594) |
| @w5833946 | B | 建模与训练 | 主损失 CE + Dice（CE 比例随训练衰减），另加方向分类 CE、gesture 区域比例 MSE 与 MAE（后两者不确定有效）；增广：rot 符号翻转、世界系 x-y 旋 | [cmi-detect-behavior-with-sensor-data#603564-03](https://www.kaggle.com/competitions/cmi-detect-behavior-with-sensor-data/discussion/603564) |
| @daiwakun | C | 建模与训练 | 每个时间步加辅助 3 类相位预测（relax and move / hand at target / perform gesture）；构造 3 个注意力并按相位概率加权 | [cmi-detect-behavior-with-sensor-data#603594-03](https://www.kaggle.com/competitions/cmi-detect-behavior-with-sensor-data/discussion/603594) |

## 高票评论

| 票 | 选手 | 日期 | 摘录 | 出处 |
| --- | --- | --- | --- | --- |
| 15 | @aerdem4 | 2025-06-10 | This could be more impressive if you didnt reach that score by yourself first. It feels like you designed your | [583863](https://www.kaggle.com/competitions/cmi-detect-behavior-with-sensor-data/discussion/583863) |

## 关联资产

- 深读：`analysis/deep/cmi-detect-behavior-with-sensor-data.md`
- 结构化摘要：`notes/tabular/cmi-detect-behavior-with-sensor-data.md`
- 归档讨论区：`intel/cmi-detect-behavior-with-sensor-data/`（主题 2 条有 ≥50 票帖，图证 0 个）
