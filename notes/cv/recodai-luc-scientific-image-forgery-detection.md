# RECOD.ai LUC - Scientific Image Forgery Detection

> 主题：cv ｜ 子类：— ｜ 领域：科研诚信 ｜ 类别：Research
> 截止：2026-04-22 ｜ 队伍数：1564 ｜ 机制：代码赛 ｜ 指标：伪造检测（混合指标）
> 数据来源：`intel/recodai-luc-scientific-image-forgery-detection/`（80 条主题索引 + 6 篇 write-up 正文）

## 1. 任务与数据

- 预测目标：检测科研论文图像中的伪造/重复使用（如 Western blot 条带复制、显微图像重叠）。
- 数据形态：论文图像（多面板拼图）+ 伪造标注。
- 构造陷阱：
  - 伪造往往是局部复制/镜像/旋转，需要细粒度几何比对；
  - 面板结构复杂（一张图含多个子图）；
  - 正样本稀少（多数图是干净的）。

## 2. 方案谱系

| 方案 | 名次 | 关键点 |
| --- | --- | --- |
| 四段式流水线：YOLO 面板检测 → 分数据类型的嵌入检索候选对 → 关键点匹配 + 几何验证 → 兜底策略 | 1st | 把"检测伪造"重构为"检索可疑配对 + 几何验证"，与实体匹配/查重思路同构 |

## 3. 关键技巧

- 面板检测（panel detection）先做版面拆分，不同数据类型分别处理（Western blot / 显微）。
- 嵌入检索找候选对，再做关键点匹配与几何验证（复制/旋转/镜像都能抓到）。
- 分层兜底：检索不到匹配时退回基础模型判定。

## 4. 可迁移性评估

- 可直接迁移：检索候选 + 几何验证的重复检测范式（图像查重、文档抄袭、实体匹配通用）；分层流水线 + 兜底策略；按子类型分别建模。
- 需要前提：目标检测 + 图像检索（嵌入/关键点）技术栈。
- 不建议照搬：端到端分类（难以捕捉局部复制）。

## 5. 对新手的关键启示

1. "找相似 → 验证几何关系"比直接分类更适合伪造/重复检测。
2. 按数据类型分支建模（本场 Western blot 与显微图像分开处理）。
3. 科研诚信类比赛（RECOD.ai 系列）是 Kaggle 的新方向，社会价值明确。

## 6. 出处

- 讨论区索引：`intel/recodai-luc-scientific-image-forgery-detection/topics.md`（80 条）
- 已收录 write-up（6 篇）：
  - 1st（37 票）：https://www.kaggle.com/competitions/recodai-luc-scientific-image-forgery-detection/discussion/695702
  - 2nd（15 票）：https://www.kaggle.com/competitions/recodai-luc-scientific-image-forgery-detection/discussion/694397
  - 65th DINOv2 方案（8 票）：https://www.kaggle.com/competitions/recodai-luc-scientific-image-forgery-detection/discussion/694442
