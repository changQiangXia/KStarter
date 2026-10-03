# MABe Challenge - Social Action Recognition in Mice

> `MABe-mouse-behavior-detection` ｜ Research ｜ 指标 MABe F Beta ｜ 1412 队 ｜ 截止 2025-12-15

本页汇总该场 **1 条 ≥50 票 GM 主题帖**、**4 条断言**、**0 条高票评论**。

## GM 主题帖

| 票 | 选手 | 日期 | 主题 |
| --- | --- | --- | --- |
| 92 | [@cdeotte](https://www.kaggle.com/cdeotte) | 2025-12-16 | [7th Place Gold - CNN Transformer with Invariant Features](https://www.kaggle.com/competitions/MABe-mouse-behavior-detection/discussion/663029) |

## 断言（条件→动作→机制→结果）

| 选手 | 等级 | 阶段 | 动作（节选） | 出处 |
| --- | --- | --- | --- | --- |
| @cdeotte | A | 验证设计 | 只用 host 说明会出现在测试中的 15 个 lab_id 计算 CV；XGB 的 CV 0.475 与 public LB 0.477 近乎一致（private 关系变差） | [MABe-mouse-behavior-detection#663029-01](https://www.kaggle.com/competitions/MABe-mouse-behavior-detection/discussion/663029) |
| @cdeotte | A | 特征与数据工程 | 目标分三态：标注为 1 则 1；标注缺失但在 behavior_labeled 中则 0；两者都不在则 mask（不计 loss）。特征做 lab 不变化：agent 中心坐标系、 | [MABe-mouse-behavior-detection#663029-02](https://www.kaggle.com/competitions/MABe-mouse-behavior-detection/discussion/663029) |
| @cdeotte | A | 建模与训练 | CNN 沿时间卷积学运动特征，再接 cross（agent-target）与 self（同鼠部件）注意力；用 2/4/8/16 秒四种滑窗（64/128/256/512 帧，str | [MABe-mouse-behavior-detection#663029-03](https://www.kaggle.com/competitions/MABe-mouse-behavior-detection/discussion/663029) |
| @cdeotte | A | 集成与融合 | 10 个 NN（3 个特征族）等权集成 CV 0.546/public 0.551/private 0.518（第 8）；再用 3 族 NN 的 OOF 加公开 notebook  | [MABe-mouse-behavior-detection#663029-04](https://www.kaggle.com/competitions/MABe-mouse-behavior-detection/discussion/663029) |

## 高票评论

_无 ≥10 票评论_

## 关联资产

- 深读：`analysis/deep/MABe-mouse-behavior-detection.md`
- 结构化摘要：`notes/science/MABe-mouse-behavior-detection.md`
- 归档讨论区：`intel/MABe-mouse-behavior-detection/`（主题 1 条有 ≥50 票帖，图证 5 个）
