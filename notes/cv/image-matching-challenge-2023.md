# Image Matching Challenge 2023（精简）

> 主题：cv ｜ 子类：— ｜ 领域：三维重建 ｜ 类别：Research ｜ 截止：2023-06-12 ｜ 队伍数：494 ｜ 指标：3D 重建精度
> 出处：`intel/image-matching-challenge-2023/`（80 条主题索引 + 6 篇 write-up 正文）

## 任务

多视角图像匹配与三维重建（IMC 系列 2022 → 2023 → 2024 → 2025 的中间届次）。

## 关键要点

- 1st 标题即方法骨架："**稀疏 + 稠密匹配组合**"（Sparse + Dense matching）。
- 2nd 的标题是"**赢过 COLMAP**"——说明该系列的参照系是**经典 SfM 流程 COLMAP**，目标是用学习型方法超越它（这正是本系列设立的初衷）。
- 5th 用 **kNN 短名单 + 旋转增强**。

## 可迁移要点

- **以经典流程为基准并试图超越它**，是该系列一贯的评测思路（与 G2Net 的"深度学习能走多远"、Smartphone GNSS 的经典方法对照同源）。
- 稀疏（关键点）+ 稠密（光流类）匹配的组合是 2023 年的主流。
- 检索（kNN 短名单）先行可大幅降低匹配成本。

## 出处

- 讨论区索引：`intel/image-matching-challenge-2023/topics.md`
- 1st（84 票）：https://www.kaggle.com/competitions/image-matching-challenge-2023/discussion/417407
- 2nd 赢过 COLMAP（49 票）：https://www.kaggle.com/competitions/image-matching-challenge-2023/discussion/416873
- 5th kNN + 旋转（44 票）：https://www.kaggle.com/competitions/image-matching-challenge-2023/discussion/416816
