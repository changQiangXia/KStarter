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

## 轻读结论（2026-10 补）

- **4th 配方**：<10 图类别并入 unknown → EfficientNetV2B0（ImageNet 预训练）+ 128 Dense + 不均衡初始化 → 两阶段微调（冻结 base → 解冻 2 顶层）→ label smoothing 0.1 → 6 模型集成；类别取平均概率 >0.4，OSD = 平均(1−max prob) + 5×平均标准差（413092）。
- **数据本质**：290 类中 **157 类无图**；标签存在属/科/目层级错乱；社区用 FathomNet API + marinespecies.org 核验（398752 / 407400）。
- **评测教训**：metric 的 AUC 部分曾有 bug、官方修复重算；另有 MAP@20 与评分代码不一致（404769 / 410140）。
- 下载/规则坑：图片源下载慢、download_images.py 参数报错、外部数据集边界（397071 / 410908 / 407096）。

## 图表证据

![预处理后的类别分布](../../intel/fathomnet-out-of-sample-detection/bodies/413092_img/01.png)

**图**（topic 413092）：合并 <10 图类别后的长尾分布。

![OSD 概率直方图](../../intel/fathomnet-out-of-sample-detection/bodies/413092_img/02.png)

**图**（topic 413092）：集成模型的 OSD 概率分布（多数 0.8–0.95）。

## 出处

- 讨论区索引：`intel/fathomnet-out-of-sample-detection/topics.md`
- 4th（5 票）：https://www.kaggle.com/competitions/fathomnet-out-of-sample-detection/discussion/413092
- 代码仓库：https://github.com/artem-istranin/FathomNet23
- 标签错误讨论：https://www.kaggle.com/competitions/fathomnet-out-of-sample-detection/discussion/407400
- metric 修复与重算：https://www.kaggle.com/competitions/fathomnet-out-of-sample-detection/discussion/404769
- 157/290 类无图：https://www.kaggle.com/competitions/fathomnet-out-of-sample-detection/discussion/398752
- MAP@20 不一致：https://www.kaggle.com/competitions/fathomnet-out-of-sample-detection/discussion/410140
