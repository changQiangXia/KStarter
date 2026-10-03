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

## 轻读结论（2026-10 补）

- **三队都在解决同一个域差**（训练无掩码、测试大遮挡）：1st 用 **BlendFlip**（邻域翻转填充 + 50/50 混合，约 +0.03–0.04 mAP）+ 5 模型/两尺寸/ArcFace 1536D → PCA 3072D（99% 方差）→ KNN；2nd 统计测试掩码生成训练掩码 + md5 去重（45,769 类）+ sub-center ArcFace（k=3 动态 margin），集成私榜 0.717；3rd 用 FGVC8 伪标签 + logits（优于 KNN），最佳单模 0.672（328281 / 328345 / 328237）。
- **检索 vs logits 无定论**：1st 靠嵌入检索夺冠，2nd/3rd 报告 logits 至少不差。需按"掩码强度"建本地验证集再选。
- **工程细节换分**：去重（同图不同类别）、方向旋正、对 FGVC9 的 3116 类微调（+0.03）可复现。
- **影响力缺口**：无奖牌/奖金、82 队；"往届成果有没有真的用于反贩卖"无人回答（314885 / 316799）。

## 图表证据

本场 0 张归档图（目录为空），**图证缺口已登记**（BlendFlip 示意图为站外图床）。

## 出处

- 讨论区索引：`intel/hotel-id-to-combat-human-trafficking-2022-fgvc9/topics.md`
- 1st（30 票）：https://www.kaggle.com/competitions/hotel-id-to-combat-human-trafficking-2022-fgvc9/discussion/328281
- 2nd（11 票）：https://www.kaggle.com/competitions/hotel-id-to-combat-human-trafficking-2022-fgvc9/discussion/328345
- 公开/私榜 3rd（16 票）：https://www.kaggle.com/competitions/hotel-id-to-combat-human-trafficking-2022-fgvc9/discussion/328237
- 奖牌/奖金争议（26 票）：https://www.kaggle.com/competitions/hotel-id-to-combat-human-trafficking-2022-fgvc9/discussion/314885
- 往届实效提问（16 票）：https://www.kaggle.com/competitions/hotel-id-to-combat-human-trafficking-2022-fgvc9/discussion/316799
