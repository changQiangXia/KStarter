# iWildCam 2022（FGVC9，精简）

> 主题：cv ｜ 子类：— ｜ 领域：野生动物监测 ｜ 类别：Research ｜ 截止：2022-05-30 ｜ 队伍数：24 ｜ 指标：计数/分类
> 出处：`intel/iwildcam2022-fgvc9/`（80 条主题索引 + 6 篇 write-up 正文）

## 任务

由相机陷阱（camera trap）图像**计数与识别动物**（本年为"仅动物、计数形式"的简化版）。

## 关键要点

- 9th 的吐槽极具代表性："山羊！谁能数得清到处乱走盯着镜头的山羊"——**计数类任务的固有困难：目标移动、遮挡、重复出现**。
- 参赛队极少（24），属研究型小比赛；与此前的 iWildCam 系列构成延续。
- 生态监测类任务的常见设定：**分布偏移（不同地点/季节）+ 长尾物种**。

## 可迁移要点

- 计数任务的常见解法：检测 + 去重（跨帧/跨时间段匹配）+ 计数聚合。
- 与 Biohub（细胞追踪）、DFL（视频事件）对照：**"检测 + 关联 + 计数"是通用骨架**。

## 轻读结论（2026-10 补）

- **1st（无训练）**：只用 MegaDetector 检测过滤 + 每序列取最大计数；按"每图 >8 个框"分高/低密度：高密度用置信度 0.0 + NMS(IoU=0.2) + 抑制小框（public 0.253）；低密度用无重叠框 0.98 / 有重叠框 0.8，再对剩 1–2 框的图做第二轮 0.98 过滤 → **public 0.247**；作者判断用检测器结果训练会误差传播（328965）。
- **9th（重工程）**：MegaDetector v4 → YOLOv5 → WBF 融合（public/private 0.275/0.265）；对 8 类群居物种做 DeepMAC 掩码质心 chip + 自编码器 512 维潜向量的帧间匹配，全量上无收益（328526）。
- **官方资产**：DeepMAC 实例掩码（MegaDetector V4 框）随赛发布（316483）。
- **数据问题**：重复（324436）、序列乱序（324425）。

## 图表证据

本场 0 张归档图（0/0），**图证缺口已登记**。

## 出处

- 讨论区索引：`intel/iwildcam2022-fgvc9/topics.md`
- 1st（4 票）：https://www.kaggle.com/competitions/iwildcam2022-fgvc9/discussion/328965
- 9th（3 票）：https://www.kaggle.com/competitions/iwildcam2022-fgvc9/discussion/328526
- 往届参考合集（16 票）：https://www.kaggle.com/competitions/iwildcam2022-fgvc9/discussion/314736
- 起步 notebook：https://www.kaggle.com/competitions/iwildcam2022-fgvc9/discussion/323139
- DeepMAC 掩码公告：https://www.kaggle.com/competitions/iwildcam2022-fgvc9/discussion/316483
