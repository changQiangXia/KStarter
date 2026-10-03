# NFL Big Data Bowl 2026 - Prediction

> `nfl-big-data-bowl-2026-prediction` ｜ Featured ｜ 指标 NFL_2025 ｜ 1899 队 ｜ 截止 2026-01-06

本页汇总该场 **1 条 ≥50 票 GM 主题帖**、**5 条断言**、**2 条高票评论**。

## GM 主题帖

| 票 | 选手 | 日期 | 主题 |
| --- | --- | --- | --- |
| 147 | [@chack3](https://www.kaggle.com/chack3) | 2025-12-04 | [1st Place Solution](https://www.kaggle.com/competitions/nfl-big-data-bowl-2026-prediction/discussion/651604) |

## 断言（条件→动作→机制→结果）

| 选手 | 等级 | 阶段 | 动作（节选） | 出处 |
| --- | --- | --- | --- | --- |
| @chack3 | B | 建模与训练 | 主损失用 GaussianNLLLoss（同时预测均值与方差，自动降低大方差样本权重，优于 SmoothL1；帧级加权无益）；辅助损失对预测 xy 的一阶/二阶差分（速度/加速度） | [nfl-big-data-bowl-2026-prediction#651604-03](https://www.kaggle.com/competitions/nfl-big-data-bowl-2026-prediction/discussion/651604) |
| @chack3 | B | 特征与数据工程 | 50% 概率绕平均球员位置随机旋转 0-360°（先高斯 σ=5° 后改均匀更好）；从更早帧开始预测（最多提前 20 帧）并把提前帧数作为静态特征（测试时为 0）；垂直翻转 | [nfl-big-data-bowl-2026-prediction#651604-04](https://www.kaggle.com/competitions/nfl-big-data-bowl-2026-prediction/discussion/651604) |
| @chack3 | B | 集成与融合 | 100+ 个同架构模型简单平均；多样性来自不同特征配置与不同 CV 划分；Group 5-fold 按 game_id，跑 3 次不同划分；RAdam + EMA(0.9995)  | [nfl-big-data-bowl-2026-prediction#651604-05](https://www.kaggle.com/competitions/nfl-big-data-bowl-2026-prediction/discussion/651604) |
| @chack3 | C | 特征与数据工程 | 动态特征=传球前 20 帧 × 10 维（位置、朝向三角、速度三角、相对落点、相对接球手）；静态 12 维；目标是最后一帧起的位移 (Δx, Δy)，累加回轨迹 | [nfl-big-data-bowl-2026-prediction#651604-01](https://www.kaggle.com/competitions/nfl-big-data-bowl-2026-prediction/discussion/651604) |
| @chack3 | C | 建模与训练 | 动态编码：depthwise Conv1d ×7（10 维到 640 维、无 padding 强调最后一帧）；静态编码 Conv1d+BN+SiLU 到 64 维；拼接投影 256 | [nfl-big-data-bowl-2026-prediction#651604-02](https://www.kaggle.com/competitions/nfl-big-data-bowl-2026-prediction/discussion/651604) |

## 高票评论

| 票 | 选手 | 日期 | 摘录 | 出处 |
| --- | --- | --- | --- | --- |
| 14 | @chack3 | 2025-12-14 | I think participating in many competitions definitely helps, but to me that’s not the most essential part. Wha | [651604](https://www.kaggle.com/competitions/nfl-big-data-bowl-2026-prediction/discussion/651604) |
| 13 | @chack3 | 2025-12-11 | My approach is quite simple: even if I have an idea for the final model, I always start with a very simple bas | [651604](https://www.kaggle.com/competitions/nfl-big-data-bowl-2026-prediction/discussion/651604) |

## 关联资产

- 深读：`analysis/deep/nfl-big-data-bowl-2026-prediction.md`
- 结构化摘要：`notes/cv/nfl-big-data-bowl-2026-prediction.md`
- 归档讨论区：`intel/nfl-big-data-bowl-2026-prediction/`（主题 1 条有 ≥50 票帖，图证 3 个）
