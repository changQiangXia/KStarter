# Google - Isolated Sign Language Recognition

> 主题：tabular（关键点序列）｜ 子类：— ｜ 领域：无障碍 ｜ 类别：Research
> 截止：2023-05-01 ｜ 队伍数：1165 ｜ 机制：代码赛 ｜ 指标：多分类准确率
> 数据来源：`intel/asl-signs/`（80 条主题索引 + 6 篇 write-up 正文）

## 1. 任务与数据

- 预测目标：由手部/姿态**关键点序列**识别孤立手语词（单标签分类）。
- 数据形态：MediaPipe 关键点序列（坐标 + 置信度）；每段视频一个词。
- 构造陷阱：关键点缺失/抖动；序列长度不一；类别较多。

## 2. 方案谱系

| 方案 | 名次 | 关键点 |
| --- | --- | --- |
| **把关键点序列当"频谱图"处理**（EfficientNet-B0）+ BERT/DeBERTa 辅助 | 2nd | 明确借鉴**音频频谱图分类**的思路：把时间 × 关键点维度视为图像；输入 160×80；多增强；8 折随机划分中选单折 + 全量训练的文本模型辅助 |

## 3. 关键技巧

- **序列 → 图像化**（时间 × 维度当 2D 输入）——跨模态迁移（音频 → 手语）。
- **强增强**对抗关键点抖动。
- **异构辅助模型**（BERT/DeBERTa 处理关键点序列的"类文本"结构）。
- 折数与单折选择的权衡（作者报告单折模型即可接近最优）。

## 4. 可迁移性评估

- **可直接迁移**：
  - **把时序/骨架数据转成 2D 表示**再用图像模型（与时序频谱图同源）；
  - 强增强处理关键点噪声；
  - 异构模型辅助提升。
- 需要前提：关键点提取工具与图像模型经验。
- 不建议照搬：只用 1D 序列模型（图像化表示往往更强）。

## 5. 对新手的关键启示

1. **"表示转换"常比模型创新更有效**（关键点 → 图像、信号 → 频谱图）。
2. 与 ASL Fingerspelling、HMS-EEG 对照：**序列任务的通用套路 = 表示转换 + 强增强 + 分组验证**。
3. 手语/无障碍是 Kaggle 的稳定赛题方向（Google 系列已办两届）。

## 6. 出处

- 讨论区索引：`intel/asl-signs/topics.md`（80 条）
- 已收录 write-up（6 篇）：
  - 1st 1DCNN + Transformer（191 票）：https://www.kaggle.com/competitions/asl-signs/discussion/406684
  - 2nd 频谱图式方案（118 票）：https://www.kaggle.com/competitions/asl-signs/discussion/406306
  - 44th 银牌（73 票）：https://www.kaggle.com/competitions/asl-signs/discussion/406302
