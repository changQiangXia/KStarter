# Happywhale - Whale and Dolphin Identification

> `happy-whale-and-dolphin` ｜ Research ｜ 指标 MAP@{K} ｜ 1588 队 ｜ 截止 2022-04-18

本页汇总该场 **1 条 ≥50 票 GM 主题帖**、**3 条断言**、**0 条高票评论**。

## GM 主题帖

| 票 | 选手 | 日期 | 主题 |
| --- | --- | --- | --- |
| 71 | [@cdeotte](https://www.kaggle.com/cdeotte) | 2022-04-21 | [19th Place - Single Model LB 860 Without Pseudo](https://www.kaggle.com/competitions/happy-whale-and-dolphin/discussion/320298) |

## 断言（条件→动作→机制→结果）

| 选手 | 等级 | 阶段 | 动作（节选） | 出处 |
| --- | --- | --- | --- | --- |
| @cdeotte | A | 建模与训练 | 大 backbone（EffNetB5/6/7、V2-L/XL、ConvNext-L）加大图 512/640/768；两个 ArcFace 头（species 与 individu | [happy-whale-and-dolphin#320298-01](https://www.kaggle.com/competitions/happy-whale-and-dolphin/discussion/320298) |
| @cdeotte | A | 特征与数据工程 | 用 6 个数据集把关键部位（背鳍与全身）裁出后缩放到 512/640/768 | [happy-whale-and-dolphin#320298-02](https://www.kaggle.com/competitions/happy-whale-and-dolphin/discussion/320298) |
| @cdeotte | A | 集成与融合 | 最佳单模 8 折 CV 0.866 / LB 0.859；12 模型 × 8 折 = 96 个模型按每折 5 预测投票集成 LB 0.868；赛后对其中 2 个模型伪标签重训 →  | [happy-whale-and-dolphin#320298-03](https://www.kaggle.com/competitions/happy-whale-and-dolphin/discussion/320298) |

## 高票评论

_无 ≥10 票评论_

## 关联资产

- 深读：`analysis/deep/happy-whale-and-dolphin.md`
- 结构化摘要：`notes/cv/happy-whale-and-dolphin.md`
- 归档讨论区：`intel/happy-whale-and-dolphin/`（主题 1 条有 ≥50 票帖，图证 4 个）
