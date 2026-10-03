# Happywhale - Whale and Dolphin Identification

> 主题：cv ｜ 子类：— ｜ 领域：野生动物识别 ｜ 类别：Research
> 截止：2022-04-18 ｜ 队伍数：1588 ｜ 机制：标准赛 ｜ 指标：MAP@5（个体识别/检索）
> 数据来源：`intel/happy-whale-and-dolphin/`（80 条主题索引 + 6 篇 write-up 正文）

## 1. 任务与数据

- 预测目标：由照片识别鲸/海豚个体（个体级检索，测试可能出现训练未见个体）。
- 数据形态：野生动物照片（姿态、光照、角度差异极大）+ 个体 ID。
- 构造陷阱：
  - 开集识别（需处理 new_individual 这类未见类别）；
  - 背景干扰大，需要先定位主体；
  - 每个体样本数极少（长尾）。

## 2. 方案谱系

| 方案 | 名次 | 关键点 |
| --- | --- | --- |
| 先训鲸体检测器（YOLOv5）再做人脸式识别 | 3rd | 流程：随机标注约 5000 个鲸体 → 训练显著性检测器（刻意关闭 mosaic/mixup 等强增强以避免定位失真）→ 用检测框裁剪 → 训练识别模型 |
| 其他方案 | 见讨论区 | |

## 3. 关键技巧

- 两阶段：检测主体 → 识别个体（把背景干扰降到最低）。
- 检测器的增强策略要克制（3rd 特意关闭 mosaic/mixup，定位任务不需要它们）。
- 开集处理（新个体类别 / 低置信度回退）。
- 度量学习 / 检索式头部（MAP@5 是检索指标）。

## 4. 可迁移性评估

- 可直接迁移：细粒度识别的"检测 + 识别"两阶段；按任务性质选择增强（检测任务不宜用过度几何增强）；开集识别的兜底策略。
- 需要前提：目标检测 + 度量学习技术栈。
- 不建议照搬：直接整图训练识别（背景成为噪声）。

## 5. 对新手的关键启示

1. 细粒度识别先"聚焦主体"——裁剪比换模型更有效。
2. 增强策略要按任务定制（检测 vs 分类需求不同）。
3. 与 Leash-BELKA、Petfinder 对照：细粒度识别类比赛的核心是"表示学习 + 检索"。

## 6. 出处

- 讨论区索引：`intel/happy-whale-and-dolphin/topics.md`（80 条）
- 已收录 write-up（6 篇）：
  - 1st（198 票）：https://www.kaggle.com/competitions/happy-whale-and-dolphin/discussion/320192
  - 19th 单模型（71 票）：https://www.kaggle.com/competitions/happy-whale-and-dolphin/discussion/320298
  - 数据集整理（75 票）：https://www.kaggle.com/competitions/happy-whale-and-dolphin/discussion/315524
