# Hotel ID - Combat Human Trafficking（FGVC9，精简）

> 主题：cv ｜ 子类：— ｜ 领域：社会公益 ｜ 类别：Research ｜ 截止：2022-05-30 ｜ 队伍数：82 ｜ 指标：检索类（酒店图像匹配）
> 出处：`intel/hotel-id-to-combat-human-trafficking-2022-fgvc9/`（80 条主题索引 + 6 篇 write-up 正文）

## 任务

由酒店房间/外观照片**识别同一家酒店**（用于反人口贩卖调查的取证匹配），属于图像检索/细粒度识别。

## 关键要点

- 1st 的"秘方"是**针对大面积遮挡的新增强方法**（在保持场景语义一致的前提下模拟遮挡）。
- 方案骨架：**5 模型集成 + 两种图像尺寸 + PCA 降维嵌入**。
- 与 FGVC9 同届其他赛道（Herbarium、Sorghum）共享"细粒度识别"的方法论。

## 可迁移要点

- **遮挡是检索/识别任务的常见干扰**，专用增强（保持语义一致的遮挡）比通用增强更有效。
- 嵌入降维（PCA）在检索任务中常有助于去噪。
- 社会公益类比赛（反人口贩卖、野生动物保护）是 Kaggle 的重要方向。

## 出处

- 讨论区索引：`intel/hotel-id-to-combat-human-trafficking-2022-fgvc9/topics.md`
- 1st（30 票）：https://www.kaggle.com/competitions/hotel-id-to-combat-human-trafficking-2022-fgvc9/discussion/328281
- 2nd（11 票）：https://www.kaggle.com/competitions/hotel-id-to-combat-human-trafficking-2022-fgvc9/discussion/328345
- 公开/私榜 3rd（16 票）：https://www.kaggle.com/competitions/hotel-id-to-combat-human-trafficking-2022-fgvc9/discussion/328237
