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

## 6. 轻读结论（2026-10 补）

**一句话**：孤立手语词分类的胜负点 = **输入表示（序列 vs 类频谱图像）× 强正则 × 变长/掩码处理**。

- 1st（191 票）：1D CNN+Transformer（1.85M）；drop_path0.2+dropout **0.8**+AWP 缺一掉分；causal padding 保持 mask 并让 BN/GAP 感知；lag1/2 运动特征；4 seed；CV/公 0.80、私 **0.88**（图证在 deep 文件的 2nd 图）。
- 2nd Google（118 票）：关键点插值成 160×80×3"频谱"→ EfficientNet-B0 + BERT/DeBERTa helpers；finger-tree rotate、mixup、时频掩码；单折 CV 0.898/LB ~0.8。
- 6th（406537）：MLP+帧 Transformer 双模型；去无手指帧；landmark 类型嵌入；首个 Transformer 缩小+输出缩放（便于融合）；**预训练 DeBERTa 权重无效**。

**裁决**：三种表示都能到前 3；显式几何特征提升注意力路；变长一致性必须处理；预训练迁移不适用。

**系列延续**：同系列下一届（Fingerspelling）转向序列解码，1st 为同一位选手（Christof Henkel）。

**悬案**：44th/实验帖未细读；公私榜 gap 成因与指标实现未入库。

## 7. 图表证据

![2nd 的关键点图像化](../../intel/asl-signs/bodies/406306_img/01.jpg)

**图 1**（topic 406306）：9 帧骨架 → 160×80×3 类频谱张量。

## 8. 出处

- 讨论区索引：`intel/asl-signs/topics.md`（80 条）
- 已收录 write-up（6 篇）：
  - 1st 1DCNN + Transformer（191 票）：https://www.kaggle.com/competitions/asl-signs/discussion/406684
  - 2nd 频谱图式方案（118 票）：https://www.kaggle.com/competitions/asl-signs/discussion/406306
  - 44th 银牌（73 票）：https://www.kaggle.com/competitions/asl-signs/discussion/406302
- 轻读全本：`analysis/deep/asl-signs.md`（Tier B 轻读：对照矩阵/裁决/证据分级/悬案 + 1 图证）
