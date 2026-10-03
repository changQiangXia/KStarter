# BirdCLEF 2025

> 主题：audio ｜ 子类：— ｜ 领域：生物声学 ｜ 类别：Research
> 截止：2025-06-05 ｜ 队伍数：2031 ｜ 机制：代码赛 ｜ 指标：物种识别（mAP 类）
> 数据来源：`intel/birdclef-2025/`（80 条主题索引 + 6 篇 write-up 正文）

## 1. 任务与数据

- 预测目标：由野外录音识别鸟种（多标签、类别多、长尾）。
- 数据形态：长录音 + 弱标签；训练与测试存在地域/设备差异。
- 构造陷阱：弱标签需切窗 + 多实例；类别极不平衡；跨域泛化。

## 2. 方案谱系

| 方案 | 名次 | 关键点 |
| --- | --- | --- |
| **多轮 Noisy Student（迭代自训练）** | 1st | 用多轮半监督自训练提升；作者在 write-up 开头记录了乌克兰战事下从避难所提交作品的处境（Kaggle 社区的人文一面，与 CZII cryo-ET 类似） |
| 其他方案 | 见讨论区 | |

## 3. 关键技巧

- **多轮 Noisy Student 自训练**是弱标签音频任务的主流（2026 届冠军同样用了 Noisy Student + 蒸馏——**系列内方法连续两年被验证**）。
- 切窗 + 多实例学习 + 伪标签。
- 跨域泛化（不同地域/设备的录音）。

## 4. 可迁移性评估

- **可直接迁移**：多轮自训练/伪标签的流程化（弱标签任务通用）；切窗 + 多实例范式。
- 需要前提：音频处理与大量未标注数据。
- 不建议照搬：单轮伪标签即收工（多轮迭代收益明显）。

## 5. 对新手的关键启示

1. **BirdCLEF 系列的年度方法演进清晰**：2025 多轮 Noisy Student → 2026 Noisy Student + 蒸馏，**半监督是主线**。
2. 弱标签音频的通用配方：切窗 → 多实例 → 伪标签 → 多轮迭代。

## 6. 出处

- 讨论区索引：`intel/birdclef-2025/topics.md`（80 条）
- 已收录 write-up（6 篇）：
  - 1st 多轮 Noisy Student（263 票）：https://www.kaggle.com/competitions/birdclef-2025/discussion/583577
  - 2nd 伪标签之路（54 票）：https://www.kaggle.com/competitions/birdclef-2025/discussion/583699
  - 5th 自蒸馏（69 票）：https://www.kaggle.com/competitions/birdclef-2025/discussion/583312
