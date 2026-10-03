# GeoLifeCLEF 2022（LIFECLEF 2022 / FGVC9，精简）

> 主题：cv ｜ 子类：— ｜ 领域：生态/地理 ｜ 类别：Research ｜ 截止：2022-05-24 ｜ 队伍数：52 ｜ 指标：物种分布预测
> 出处：`intel/geolifeclef-2022-lifeclef-2022-fgvc9/`（80 条主题索引 + 6 篇 write-up 正文）

## 任务

由地理位置 + 遥感影像 + 环境变量预测物种分布（与 GeoLifeCLEF 2024 同系列）。

## 关键要点

- 2nd 的方案以**深度卷积网络为骨架**，并说明细节将发表在技术报告（研究型比赛的常规做法：**代码 + 论文双产出**）。
- 与 2024 届对照可见该系列的延续与评估演进。

## 可迁移要点

- 生态/遥感任务的通用输入组合：**影像 + 坐标 + 环境栅格**。
- 研究型比赛常要求技术报告——**写作与可复现性**是产出的一部分。

## 轻读结论（2026-10 补）

- **1st（多模态集成）**：ResNet34(NIRGB) + MobileNetV3(RGBNir) 接环境向量/坐标/landcover dothot 的 FCN，再加 **Random Forest（32 树、深度 12、81 特征含 R/G/B/NIR 分位）**，三模型概率平均 + 5 次 TTA（327055）。
- **2nd（双 CNN + 标签松弛）**：RGB 与 Alt+NIR+NDVI 两分支 → dropout 0.45 → 17,034 类；Inception-v4 比 ResNet50 +2%；ImageNet 预训练最优；**spatial block-label swap（0.01° 网格、10% 邻域换标）+2%**；10 模型伪置信度集成 +2%；长尾"不处理"最好（测试同样长尾）（328637）。
- **纪律**：公榜只占 10% 测试数据，用验证分选模；CLEF working note 强制且不可复现的 run 可能被移出正式发表（325984）。
- 2nd 失败清单：协变量/GPS 直接入 CNN、taxonomy 辅助任务、直方图密度、长尾加权；1st 失败：多标签聚合、其他骨干、GBDT（17k 类内存爆炸）。

## 图表证据

本场归档图 2 张均为装饰性内容（Kaggle 毛衣与摄影图），**无分析价值，未内嵌**；管线图证缺口已登记。

## 出处

- 讨论区索引：`intel/geolifeclef-2022-lifeclef-2022-fgvc9/topics.md`
- 1st（11 票）：https://www.kaggle.com/competitions/geolifeclef-2022-lifeclef-2022-fgvc9/discussion/327055
- 2nd（4 票）：https://www.kaggle.com/competitions/geolifeclef-2022-lifeclef-2022-fgvc9/discussion/328637
- working note 与提交纪律：https://www.kaggle.com/competitions/geolifeclef-2022-lifeclef-2022-fgvc9/discussion/325984
- 资源汇编：https://www.kaggle.com/competitions/geolifeclef-2022-lifeclef-2022-fgvc9/discussion/312283
- .tif 处理：https://www.kaggle.com/competitions/geolifeclef-2022-lifeclef-2022-fgvc9/discussion/311983
- 单标签误导讨论：https://www.kaggle.com/competitions/geolifeclef-2022-lifeclef-2022-fgvc9/discussion/325767
