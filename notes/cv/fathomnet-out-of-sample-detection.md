# FathomNet 2023 - Out-of-Sample Detection（精简）

> 主题：cv ｜ 子类：— ｜ 领域：海洋生物 ｜ 类别：Research ｜ 截止：2023-05-23 ｜ 队伍数：69 ｜ 指标：OSD（分布外检测）得分
> 出处：`intel/fathomnet-out-of-sample-detection/`（80 条主题索引 + 6 篇 write-up 正文）

## 任务

**分布外检测（Out-of-Sample Detection, OSD）**：在海洋生物图像中，不仅要分类已知类别，还要识别出**不属于任何已知类别**的样本（开放集识别的评分形式）。

## 关键要点

- 4th 的做法很直接：训练一个**带标签平滑的分类器集成**，把 `1 - max(各类概率)` 当作 OSD 分数，再对集成取平均。
- **开放集/分布外检测的通用套路**就是"用分类置信度构造异常分数"（最大 softmax 概率的补）。
- 参赛队很少（69），属于研究型小比赛。

## 可迁移要点

- **开放集任务先问"异常分数怎么构造"**（最大概率的补、能量分数、马氏距离等）。
- 标签平滑有助于校准，从而让置信度更可用作异常分数。
- 与该类任务相关的比赛正在增多（AI 安全、医疗罕见病、工业异常检测）。

## 出处

- 讨论区索引：`intel/fathomnet-out-of-sample-detection/topics.md`
- 4th（5 票）：https://www.kaggle.com/competitions/fathomnet-out-of-sample-detection/discussion/413092
- 代码仓库：https://github.com/artem-istranin/FathomNet23
