# Herbarium 2022 - FGVC9（精简）

> 主题：cv ｜ 子类：— ｜ 领域：植物分类 ｜ 类别：Research ｜ 截止：2022-05-30 ｜ 队伍数：134 ｜ 指标：F1（细粒度多分类）
> 出处：`intel/herbarium-2022-fgvc9/`（80 条主题索引 + 6 篇 write-up 正文）

## 任务

对植物标本图像做**细粒度物种分类**（类别极多、长尾严重，FGVC 系列）。

## 关键要点

- 参赛队伍少（134）但任务难度高（细粒度 + 极小样本类别）。
- 社区提供了**起步 notebook 清单**（含 JAX/Flax 的 K 折训练示例）——与 Mayo 检查清单、PlantTraits 综述同类的公共资产。
- FGVC 系列（Fine-Grained Visual Categorization）是 Kaggle 的常设学术赛道，连续多年举办（如 iNaturalist、Herbarium）。

## 可迁移要点

- **细粒度分类的核心是特征判别力**（局部特征、注意力、多尺度）。
- **长尾类别**需要重采样/损失重加权/分类头调整（与 ISIC、Leap 的不平衡处理同源）。
- FGVC 系列有稳定的往届方案可参考。

## 出处

- 讨论区索引：`intel/herbarium-2022-fgvc9/topics.md`
- 起步 notebook 清单（15 票）：https://www.kaggle.com/competitions/herbarium-2022-fgvc9/discussion/323794
- 1st（5 票）：https://www.kaggle.com/competitions/herbarium-2022-fgvc9/discussion/329299
