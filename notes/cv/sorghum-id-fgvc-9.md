# Sorghum ID - FGVC 9（精简）

> 主题：cv ｜ 子类：— ｜ 领域：农业视觉 ｜ 类别：Research ｜ 截止：2022-05-30 ｜ 队伍数：252 ｜ 指标：细粒度多分类
> 出处：`intel/sorghum-id-fgvc-9/`（80 条主题索引 + 6 篇 write-up 正文）

## 任务

高粱（sorghum）品种的**细粒度图像分类**（FGVC 系列，与 Herbarium 2022 同届）。

## 关键要点

- 3rd 明确总结了本场的两类难点：
  1. **类间视觉相似度高**（细粒度分类的本质困难）；
  2. 数据层面的其他分类难点（需要针对性增强与采样策略）。
- 与 Herbarium 2022 同属 FGVC9 大会赛道：**细粒度分类 + 长尾**是共同主题。

## 可迁移要点

- **细粒度分类先做"类间相似度"分析**（找出最易混淆的类别对），再针对性设计增强/损失（如 triplet、arcface 类度量损失）。
- FGVC 系列（Herbarium、Sorghum、iNaturalist 等）方案可互相借用。

## 出处

- 讨论区索引：`intel/sorghum-id-fgvc-9/topics.md`
- 3rd（12 票）：https://www.kaggle.com/competitions/sorghum-id-fgvc-9/discussion/328593
- 1st（6 票）：https://www.kaggle.com/competitions/sorghum-id-fgvc-9/discussion/329049
- 2nd（5 票）：https://www.kaggle.com/competitions/sorghum-id-fgvc-9/discussion/329414
