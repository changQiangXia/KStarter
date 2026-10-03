# HMS - Harmful Brain Activity Classification

> 主题：tabular（信号处理）｜ 子类：— ｜ 领域：医疗 ｜ 类别：Featured
> 截止：2024-04-08 ｜ 队伍数：2767 ｜ 机制：代码赛 ｜ 指标：KL 散度（多类别概率）
> 数据来源：`intel/hms-harmful-brain-activity-classification/`（80 条主题索引 + 6 篇 write-up 正文）

## 1. 任务与数据

- 预测目标：由脑电图（EEG）判断**有害脑活动**类型（癫痫发作等），输出 6 类概率分布。
- 数据形态：**混合模态**——原始 EEG 时间序列 + 频谱图（spectrogram）；按时间窗口组织。
- 构造陷阱（本场最突出的数据理解问题）：
  - train.csv 有 **106,800 行，但只有 17,089 个 eeg_id、11,138 个 spectrogram_id、1,950 名患者**——每行只是某患者的一个**时间窗口**（社区专门发帖解释了这个结构）；
  - 指标是 **KL 散度**，要求输出校准良好的概率分布（不是硬标签）；
  - 多模态（时序 + 图像）需要融合。

## 2. 方案谱系

| 方案 | 名次 | 关键点 |
| --- | --- | --- |
| **双路线集成**：预训练 2D CNN 处理 Mel 频谱图 + 1D 卷积编码原始 EEG | 3rd | 两条互补表示（频谱图视作图像、原始信号用 1D CNN）再集成；团队分工（3rd 提到队友承担了大部分工作量） |
| "One Mega Model" | 8th 金 | 单一大模型路线 |
| 数据理解 + EfficientNet-B2 起步 | 社区高票 | 先把"每行是一个时间窗"解释清楚，再用频谱图训练 |

## 3. 关键技巧

- **数据结构的正确理解是第一步**：行 ≠ 样本（是时间窗），必须按 eeg_id / 患者聚合后再建模。
- **频谱图当图像处理**（预训练 CNN），**原始信号用 1D 卷积**——同一份数据的两种视角。
- **KL 散度指标要求概率校准**（与 March Mania 的 Brier 同理）。
- **按患者分组验证**（同一患者多个窗口）。

## 4. 可迁移性评估

- **可直接迁移**：
  - **信号 → 频谱图 → 预训练视觉模型**的迁移路线（音频、雷达、振动信号通用，与 BirdCLEF 同源）；
  - 原始信号 + 图像双表示融合；
  - 概率分布指标要校准；
  - 先搞清"一行代表什么"，再做特征工程。
- 需要前提：信号处理与频谱变换的基础。
- 不建议照搬：未理解数据结构就开跑（本场极易踩坑）。

## 5. 对新手的关键启示

1. **先回答"一行数据代表什么"**（本场是时间窗）——这是最容易被忽视的准备动作。
2. **频谱图让信号问题变成图像问题**，可以复用 CV 的全部经验。
3. 与 BirdCLEF、CMI 传感器对照：**信号类比赛的方法论高度一致**（频谱图 + 窗口 + 伪标签 + 概率校准）。

## 6. 出处

- 讨论区索引：`intel/hms-harmful-brain-activity-classification/topics.md`（80 条）
- 已收录 write-up（6 篇）：
  - 数据理解与起步 Notebook（**603 票**，本场最高票）：https://www.kaggle.com/competitions/hms-harmful-brain-activity-classification/discussion/468010
  - 2nd（133 票）：https://www.kaggle.com/competitions/hms-harmful-brain-activity-classification/discussion/492254
  - 3rd 双路线集成（133 票）：https://www.kaggle.com/competitions/hms-harmful-brain-activity-classification/discussion/492471
  - 8th One Mega Model（159 票）：https://www.kaggle.com/competitions/hms-harmful-brain-activity-classification/discussion/492482
