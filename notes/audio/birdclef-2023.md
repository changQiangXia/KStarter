# BirdCLEF 2023

> 主题：audio ｜ 子类：— ｜ 领域：生物声学 ｜ 类别：Research
> 截止：2023-05-24 ｜ 队伍数：1189 ｜ 机制：代码赛 ｜ 指标：物种识别（mAP 类）
> 数据来源：`intel/birdclef-2023/`（80 条主题索引 + 6 篇 write-up 正文）

## 1. 任务与数据

- 预测目标：由野外录音识别鸟种（多标签）。
- 数据形态：长录音 + 弱标签；训练数据有限（本系列早期届次数据规模较小）。
- 构造陷阱：弱标签 + 类别多 + 跨域（地域/设备）差异。

## 2. 方案谱系

| 方案 | 名次 | 关键点 |
| --- | --- | --- |
| **"Correct Data is All You Need"** | 1st | 标题即结论：**数据（与数据处理）决定上限**；作者同样记录了乌克兰战事背景下的参赛处境 |
| 其他方案 | 见讨论区 | |

## 3. 关键技巧（结合该系列共性）

- **数据处理优先**（切窗、去噪、弱标签处理）——与 2025/2026 届的"多轮自训练"一脉相承。
- **频谱图 + CNN/Transformer** 的标准表示。
- **跨域泛化**（地域/设备）。

## 4. 可迁移性评估

- **可直接迁移**：弱标签音频的切窗与数据清洗流程；频谱图表示。
- 需要前提：音频处理能力。
- 不建议照搬：直接端到端训练长录音。

## 5. 对新手的关键启示

1. **BirdCLEF 系列三年的主线是"数据 + 半监督"**：2023 数据为王 → 2025 多轮 Noisy Student → 2026 Noisy Student + 蒸馏。
2. 该系列也是"Kaggle 社区人文面"的见证（多届冠军在战事背景下参赛并在 write-up 中致谢）。

## 6. 出处

- 讨论区索引：`intel/birdclef-2023/topics.md`（80 条）
- 已收录 write-up（6 篇）：
  - 1st "Correct Data is All You Need"（132 票）：https://www.kaggle.com/competitions/birdclef-2023/discussion/412808
  - 2nd SED + CNN 七模型集成（67 票）：https://www.kaggle.com/competitions/birdclef-2023/discussion/412707
  - 4th 知识蒸馏（55 票）：https://www.kaggle.com/competitions/birdclef-2023/discussion/412753
