# PlantTraits2024（精简）

> 主题：cv ｜ 子类：— ｜ 领域：植物表型 ｜ 类别：Research ｜ 截止：2024-06-02 ｜ 队伍数：398 ｜ 指标：多性状回归
> 出处：`intel/planttraits2024/`（80 条主题索引 + 6 篇 write-up 正文）

## 任务

由植物照片 + 少量环境数据预测多种**植物性状**（多目标回归，植物表型分析）。

## 关键要点

- 本场高票材料是**分割技术/机器视觉方法综述**（"Machine Vision for Plant Phenotyping"）——与 Mayo 的图像分类检查清单同类：**方法综述类公共材料**。
- 多目标回归（多个性状）+ 图像输入 → 典型"图像 + 表格"混合任务（与 CSIRO 生物量、ISIC 同类）。
- 数据规模较小（398 队）→ 迁移学习与强增强为主。

## 可迁移要点

- 多性状回归可共享主干 + 多头（与 TLVMIC、Equity 的多任务思路一致）。
- 植物表型/农业视觉是 Kaggle 的稳定细分方向（CSIRO、PlantTraits 等）。
- **方法综述帖是快速补领域的捷径**。

## 出处

- 讨论区索引：`intel/planttraits2024/topics.md`
- 1st PlantHydra（29 票）：https://www.kaggle.com/competitions/planttraits2024/discussion/510393
- 6th AutoML 方案（9 票）：https://www.kaggle.com/competitions/planttraits2024/discussion/510143
