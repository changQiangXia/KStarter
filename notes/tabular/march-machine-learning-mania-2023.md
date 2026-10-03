# March Machine Learning Mania 2023（精简）

> 主题：tabular ｜ 子类：sports ｜ 类别：Featured ｜ 截止：2023-03-XX ｜ 队伍数：3000+ ｜ 指标：Brier
> 出处：`intel/march-machine-learning-mania-2023/`（80 条主题索引 + 6 篇 write-up 正文）

## 任务

预测 2023 年 NCAA 锦标赛胜负概率（Brier 评分），男女赛合并设题。

## 关键要点

- 5th 方案：私榜 0.17619；作者强调**感谢社区公开的 notebook 与讨论**，并把自己的方案完整公开（Notebook 链接）——该系列赛的公开协作文化非常强。
- 与前后的 2022/2025/2026 届对照可见方法论的高度稳定：**外部评分数据 + 树模型/线性模型 + 概率校准 + 稳健提交**。
- 该类比赛的核心难点始终是：数据量小、赛程短、方差大 → 校准与稳健优先于模型创新。

## 可迁移要点

- 成熟的比赛类型（如 NCAA 系列）中，**复用公开方案 + 微调校准**就是理性打法。
- 概率预测任务的评估要围绕 Brier/对数损失做校准，而不是追求分类准确率。

## 出处

- 讨论区索引：`intel/march-machine-learning-mania-2023/topics.md`
- 5th 方案（含 Notebook 链接）：见该比赛讨论区 5th Place Solution
