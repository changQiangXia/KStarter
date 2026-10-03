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

## 6. 轻读结论（2026-10 补）

**一句话**：BirdCLEF 2023 的胜负手在**数据侧审计与整理**（含发现 XC API 每物种 500 文件上限 bug）+ KD/预训练 + 推理加速。

- 1st（132 票）：294 次实验；修复 XC API bug 扩容数据；**padded cmAP 跨折均值、不要 OOF**；CV 0.908/公 0.844/私 0.764；3×SED（nfnet/convnext）+ ONNX；类采样权重 ^0.5；预训练在严格筛选 822 物种后回归有效（+1 公/+2 私）。
- 2nd（67 票）：7 模型 SED+CNN + openvino；手标 ~1800 条 nocall 无提升；ebird 非公开。
- 4th（55 票）：4×eca_nfnet_l0 + **Kaggle Models 强分类器 KD**（cmAP5 0.9479）；私 0.744。
- 7th（38 票）：19 模型 + sumup/sumix 双鸟叠加增广 + KD；私 0.7471；openvino 最快（图 1）。

**裁决**：弱标签声景赛先修数据分布；蒸馏条件性强（数据一变可能失效）；验证看排序不看绝对值；推理加速=集成上限。

**失败学**：Transformer（ECAPA TDNN）、大 chunk、CQT/LEAF、彩色噪声、整库 XC 预训练、复制 2021 2nd 噪声方案。

**悬案**：3rd/5th/6th/8th/9th 未收录；XC bug 现状未知；KD 细节未展开。

## 7. 图表证据

![推理库耗时对比](../../intel/birdclef-2023/bodies/412922_img/01.jpeg)

**图 1**（topic 412922）：openvino/onnx/torch_jit/onnxsim 耗时箱线图——openvino 最快、torch_jit 最慢约 1.7×。

## 8. 出处

- 讨论区索引：`intel/birdclef-2023/topics.md`（80 条）
- 已收录 write-up（6 篇）：
  - 1st "Correct Data is All You Need"（132 票）：https://www.kaggle.com/competitions/birdclef-2023/discussion/412808
  - 2nd SED + CNN 七模型集成（67 票）：https://www.kaggle.com/competitions/birdclef-2023/discussion/412707
  - 4th 知识蒸馏（55 票）：https://www.kaggle.com/competitions/birdclef-2023/discussion/412753
- 轻读全本：`analysis/deep/birdclef-2023.md`（Tier B 轻读：对照矩阵/裁决/证据分级/悬案 + 1 图证）
