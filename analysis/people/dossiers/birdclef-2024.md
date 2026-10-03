# BirdCLEF 2024

> `birdclef-2024` ｜ Research ｜ 指标 Birdclef ROC AUC ｜ 974 队 ｜ 截止 2024-06-10

本页汇总该场 **1 条 ≥50 票 GM 主题帖**、**5 条断言**、**0 条高票评论**。

## GM 主题帖

| 票 | 选手 | 日期 | 主题 |
| --- | --- | --- | --- |
| 78 | [@cpmpml](https://www.kaggle.com/cpmpml) | 2024-06-12 | [3rd solution](https://www.kaggle.com/competitions/birdclef-2024/discussion/511905) |

## 断言（条件→动作→机制→结果）

| 选手 | 等级 | 阶段 | 动作（节选） | 出处 |
| --- | --- | --- | --- | --- |
| @cpmpml | A | 建模与训练 | 一级大模型（efficientvit、CNN、SED、aves）预测无标注 soundscape 5 秒 clip 标签，加入训练数据训二级小模型（efficientvit-b0  | [birdclef-2024#511905-01](https://www.kaggle.com/competitions/birdclef-2024/discussion/511905) |
| @cpmpml | A | 数据工程 | 今年数据加 Xeno Canto 加往年同物种记录（重名取最新）；每物种上限 500 条保留最新；低频类上采样到每折至少 10 条 | [birdclef-2024#511905-02](https://www.kaggle.com/competitions/birdclef-2024/discussion/511905) |
| @cpmpml | A | 建模与训练 | 二级训练用大 batch 128；策略一：每 batch 加 48×4=192 个带伪标签的 soundscape clip；策略二：每 batch 随机加 128 个伪标签样本； | [birdclef-2024#511905-03](https://www.kaggle.com/competitions/birdclef-2024/discussion/511905) |
| @cpmpml | A | 建模与训练 | 把 secondary labels 的 loss 乘以 0（不回传）；伪标签样本的 secondary 置空 | [birdclef-2024#511905-04](https://www.kaggle.com/competitions/birdclef-2024/discussion/511905) |
| @cpmpml | A | 后处理与选模 | soundscape 级 max 后处理（public 加 0.02，赛后验证变小甚至 -0.002）；时序平滑核 [0.1,0.2,0.4,0.2,0.1]（最佳提交加 0.01 | [birdclef-2024#511905-05](https://www.kaggle.com/competitions/birdclef-2024/discussion/511905) |

## 高票评论

_无 ≥10 票评论_

## 关联资产

- 深读：`analysis/deep/birdclef-2024.md`
- 结构化摘要：`notes/audio/birdclef-2024.md`
- 归档讨论区：`intel/birdclef-2024/`（主题 1 条有 ≥50 票帖，图证 1 个）
