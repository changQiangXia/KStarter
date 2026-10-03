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

## 6. 轻读结论（2026-10 补）

**一句话**：细粒度开集识别 = **多来源裁剪 + ArcFace 度量学习 + knn/logit 混合 + 伪标签**；本场是"伪标签改变名次"的标志性案例（1st 两轮伪标 +0.006~0.011；19th 赛后给 2 个模型加伪标 +0.016 priv）。

- 1st（198 票）：sub-center ArcFace + 动态 margin；bbox 混合 0.60/0.15/0.15/0.05/0.05（backfin 提分）；头 lr=10× 主干 lr；knn_ratio 0.5→0.8；`new_individual` 按"首预测比例 0.165"校准；最终 ~50 模型，但赛后"2 模型也能夺冠"。
- 3rd：YOLOv5 迭代自标检测器（5000 标→训→全量预测→修正→重训）；纹理导向增强（Sharpen/ToGray/CLAHE）+ mixup；逐技巧消融。
- 19th（71 票）：6 个裁剪数据集混合训练 + 逐数据集嵌入贝叶斯加权 + KNN；无伪标单模 LB 0.860、集成 0.868；赛后伪标复验 +0.009/+0.016。

**裁决**：裁剪来源多样性 > 主干选择；伪标签是最大单点增量；knn/logit 权重随分布校正调整；开集阈值按"新个体比例"校准。

**悬案**：2nd/4th–18th 缺失；两篇 CV 技巧帖与 LB probing 帖未细读；Optuna margin 分布未公布。

## 7. 图表证据

![19th 的六数据集嵌入加权](../../intel/happy-whale-and-dolphin/bodies/320298_img/04.png)

**图 1**（topic 320298）：同模型在 6 个裁剪数据集上各出嵌入，贝叶斯优化权重后加权送入 KNN——"多裁剪来源 = 多视角集成"。

## 8. 出处

- 讨论区索引：`intel/happy-whale-and-dolphin/topics.md`（80 条）
- 已收录 write-up（6 篇）：
  - 1st（198 票）：https://www.kaggle.com/competitions/happy-whale-and-dolphin/discussion/320192
  - 19th 单模型（71 票）：https://www.kaggle.com/competitions/happy-whale-and-dolphin/discussion/320298
  - 数据集整理（75 票）：https://www.kaggle.com/competitions/happy-whale-and-dolphin/discussion/315524
  - 3rd（319896）：https://www.kaggle.com/competitions/happy-whale-and-dolphin/discussion/319896
- 轻读全本：`analysis/deep/happy-whale-and-dolphin.md`（Tier B 轻读：对照矩阵/裁决/证据分级/悬案 + 2 图证）
