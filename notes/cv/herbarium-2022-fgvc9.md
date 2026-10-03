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

## 轻读结论（2026-10 补）

- **1st 单模消融链（private）**：Swin-B224 0.78442 → 多级 CE（family/genus/species）0.79544 → LR 5e-4 0.80501 → 5crop 0.80981 → **subcenter-ArcFace 动态 margin 0.82267** → 额外 CE 头 0.82929 → Swin 增强 0.83554 → SwinB384 0.85245 → 5crop@384 0.85654 → 冻结层 100→0 0.86055 → square resize 0.86201 → **SwinV2 0.86282**；8 骨干按公榜分数融合到 **0.87662**（329299）。
- **无效项**：class-aware sampling 与 data cleaning 都没用——长尾靠度量损失/多级监督，而非重采样。
- **规模**：839,772 张训练图、Macro F1；社区有图像重复/泄漏帖（307615 / 323906）。
- 社区设施：往届 notebook 合集 38 票、JSON→Pandas 18 票、往届获奖 18 票、可解释细粒度综述 16 票。

## 图表证据

本场 0 张归档图（0/0），**图证缺口已登记**（1st 的增益均为表格）。

## 出处

- 讨论区索引：`intel/herbarium-2022-fgvc9/topics.md`
- 起步 notebook 清单（15 票）：https://www.kaggle.com/competitions/herbarium-2022-fgvc9/discussion/323794
- 1st（5 票）：https://www.kaggle.com/competitions/herbarium-2022-fgvc9/discussion/329299
- 往届 notebook 合集（38 票）：https://www.kaggle.com/competitions/herbarium-2022-fgvc9/discussion/307745
- JSON→Pandas（18 票）：https://www.kaggle.com/competitions/herbarium-2022-fgvc9/discussion/307804
- 可解释细粒度与 machine teaching（16 票）：https://www.kaggle.com/competitions/herbarium-2022-fgvc9/discussion/308406
- 训练图规模 839,772（11 票）：https://www.kaggle.com/competitions/herbarium-2022-fgvc9/discussion/307615
