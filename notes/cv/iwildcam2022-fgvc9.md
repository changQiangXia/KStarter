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

## 出处

- 讨论区索引：`intel/iwildcam2022-fgvc9/topics.md`
- 1st（4 票）：https://www.kaggle.com/competitions/iwildcam2022-fgvc9/discussion/328965
- 9th（3 票）：https://www.kaggle.com/competitions/iwildcam2022-fgvc9/discussion/328526
