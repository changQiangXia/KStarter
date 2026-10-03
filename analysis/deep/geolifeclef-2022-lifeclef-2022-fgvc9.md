# GeoLifeCLEF 2022（LIFECLEF/FGVC9 物种分布预测）轻量深读（Tier B）

> 赛事：Research（标准赛）｜ 主题 cv（遥感 + 环境协变量 → 物种分布）｜ 52 队 ｜ 指标 MeanBestError@K（top-30）｜ 截止 2022-05-24
> 材料基础：`digests/geolifeclef-2022-lifeclef-2022-fgvc9.md`（6 篇正文：2nd 328637 / 1st 327055 / 资源汇编 312283 / working note 说明 325984 / .tif 处理 311983 / 往届挑战 312112；23 条主题索引）+ 2 张装饰性归档图
> 轻读时间：2026-10（Tier B B20）

## 1. 一句话重述与数字账

给定位置 + 遥感影像 + 环境协变量，预测该处最可能出现的 **30 个物种**（17,034 类，presence-only 单标签）。两条获奖路线互补：1st 走**多模态集成**——两条 CNN（NIR+RGB / RGB+NIR，ResNet34 与 MobileNetV3）接环境向量 + 坐标 + 土地覆盖编码，再加一个 **Random Forest（81 特征）**，三模型概率平均 + TTA；2nd 只用遥感影像双分支 CNN，但提出关键的 **spatial block-label swap**（同 0.01° 网格内以 10% 概率换邻居标签）解决"未观测 ≠ 不存在"的标签病态问题，单项 +2%。官方特别提醒：**公榜只占 10% 测试数据，噪声大，应以验证分为准**；且赛后必须提交可复现的 working note，否则成绩可能从正式发表中移除。

| 关键数字 | 值 | 来源 |
| --- | --- | --- |
| 规模与任务 | **52 队**；17,034 个物种（top-30 误差）；近 200 万数据点；presence-only 单标签；公榜仅 **10%** 测试数据 | 327055 / 328637 / 325984 |
| 1st 集成 | ① ResNet34 双模态（NIR+G+B）+ 3 层 FCN（环境向量 + lat/lon + country + 海拔均值/极差 + landcover "dothot" 编码）→ 17k 分类层；② MobileNetV3-large（R+G+B+NIR）+ 同款 FCN + 2048 维 Linear/dropout/ReLU；③ **Random Forest（32 树、深度 12、81 特征**：环境 + 坐标 + landcover dothot + R/G/B/NIR 的 25/50/75 分位），并把验证集加入训练；TTA 5 次随机变换，三模型概率平均 | 327055 |
| 2nd 单模配方 | 两条不共享参数的 CNN 分支：RGB；海拔+NIR+NDVI → concat → **dropout 0.45** → 17,034 类 softmax CE；Inception-v4 比 ResNet-50 约 **+2%**；ImageNet 预训练 > MoCo-v2 自监督/MAML/ANIL/从头训；**spatial block-label swap（10% 概率）单项 +2%**；10 模型按 TTA 置信度方差做伪置信度集成再 **+2%** | 328637 |
| 无效尝试 | 2nd：环境协变量与 GPS 直接入 CNN（坐标 MLP 各种编码都欠拟合）、taxonomy 辅助任务、直方图密度预测、长尾专门处理（**"什么都不做"最好**，因为测试集同样长尾）；1st：多标签聚合、其他骨干、无迁移学习、三骨干分工、GBDT（17k 类约需 TB 级内存） | 328637 / 327055 |
| 核算力 | 2nd 用 2×RTX 3090 工作站 + V100 HPC，PyTorch 1.9；1st 用 RTX 3090（24GB）×2 + 大内存跑 RF | 328637 / 327055 |
| 学术交付 | CLEF working note **强制**：6/1 截止，轻审后 6/13 反馈、7/1 终稿；收入 CEUR-WS 并分配 DOI；**无法复现的 run 可能从正式结果中移除** | 325984 |
| 数据/格式 | `.tif` 读取方案（tifffile / PIL / cv2）；环境向量列名编码问题；GDAL 资源；往届 2017–2021 挑战与论文链接 | 311983 / 313558 / 312250 / 312112 |

## 2. 逐方案对照矩阵

| 维度 | 1st（多模态集成） | 2nd（双 CNN + 标签松弛） |
| --- | --- | --- |
| 影像分支 | ResNet34(NIRGB) + MobileNetV3(RGBNir) | ResNet50→Inception-v4(RGB; Alt+NIR+NDVI) |
| 表格/协变量 | FCN/随机森林吃环境向量、坐标、landcover、分位数 | 尝试入 CNN 失败（承认对手用 RF 更对） |
| 标签处理 | 单标签 + 验证集加训 | **block-label swap（10%）** |
| 集成 | 3 模型概率平均 + TTA | 10 模型伪置信度集成 + TTA |
| 关键结论 | 结构化/非结构化各用合适骨干再融合 | 长尾"不处理"最好；ImageNet 预训练最实用 |

## 3. 共识、分歧与裁决

### 共识一：presence-only 单标签是病态问题，需要标签松弛或概率融合（328637 / 325767 / 327055；置信度中高）

2nd 的 block-label swap 明确针对"未观测≠不存在"，+2%；1st 提到同一地点可有数百个正确标签、存在理论 top-30 下限。**裁决**：先用网格邻域标签松弛/温度 softmax/多标签聚合等手段建模不确定性，并在验证集上对比；不要用硬 CE 直接拟合单标签。置信度：中高。

### 共识二：图像与环境协变量要用各自合适的模型族（327055 / 328637；置信度中高）

1st 的 RF 在环境协变量上贡献被 2nd 明确认可；2nd 把协变量塞进 CNN 全部失败。**裁决**：遥感影像走 CNN/预训练骨干，环境/坐标走树模型或自注意力；在最终层或概率层融合，避免强行端到端。置信度：中高。

### 事件一：长尾"不处理"反而最优（328637；置信度中）

由于测试集与训练同样长尾，加权稀有类会伤害整体 top-30 误差。**裁决**：先确认评测集的类别分布再决定是否重加权；top-K 指标下"分布匹配"比"均衡"更重要。置信度：中（单一强自述 + 解释合理）。

### 事件二：公榜只占 10%，必须信验证分（325984；置信度高）

官方直接提醒公榜噪声大、私榜可能翻盘。**裁决**：模型选择以本地验证（与官方 top-30 口径一致）为准，公榜只做格式 sanity check。置信度：高。

### 事件三：working note 是"成绩是否被承认"的门槛（325984；置信度高）

CLEF 要求可复现的技术报告，未通过可能被移出正式结果；同时提供 DOI 与检索。**裁决**：把 working note 当第二交付物，从第一天维护可复现的实验日志。置信度：高。

## 4. 证据分级

| 断言 | 等级 | 说明 |
| --- | --- | --- |
| 1st 的三模型集成细节 | 冠军自述（327055） | 中高（无分数表） |
| 2nd 的 +2%/+2% 消融与失败清单 | 亚军自述（328637） | 中高 |
| working note 强制与 DOI | 官方帖（325984） | 高 |
| 公榜 10% 提醒 | 官方帖（325984） | 高 |
| .tif 读取方法 | 社区帖（311983） | 中高（技术常识） |
| 标签病态问题 | 2nd + 讨论帖（328637 / 325767） | 中高 |

## 5. 悬案与缺口（登记）

- 1st/2nd 的私榜分数未在正文给出；完整技术报告在站外；
- 多标签聚合的最优实现（1st 尝试失败）仍未解决；
- 环境协变量与坐标的最优融合方式（2nd 建议进一步研究）未定论；
- 本场没有 3rd 及以后方案的归档正文；
- **图证缺口**：归档图仅 2 张装饰性图片（Kaggle 毛衣与风景照），无分析证据，未内嵌；分析图证缺口已登记。

## 6. 图表证据

本场归档图 2 张均为装饰性内容（topic 312283 的 Kaggle 毛衣与摄影图），**无分析价值，未内嵌**；管线/模型图证缺口已登记（1st 预告过图形化管线但未归档）。

## 7. 出处

- 1st 方案（11 票 / 5 评论）：https://www.kaggle.com/competitions/geolifeclef-2022-lifeclef-2022-fgvc9/discussion/327055
- 2nd 方案（4 票 / 0 评论）：https://www.kaggle.com/competitions/geolifeclef-2022-lifeclef-2022-fgvc9/discussion/328637
- working note 与纪律（3 票 / 0 评论）：https://www.kaggle.com/competitions/geolifeclef-2022-lifeclef-2022-fgvc9/discussion/325984
- 资源汇编（8 票 / 2 评论）：https://www.kaggle.com/competitions/geolifeclef-2022-lifeclef-2022-fgvc9/discussion/312283
- .tif 处理（11 票 / 3 评论）：https://www.kaggle.com/competitions/geolifeclef-2022-lifeclef-2022-fgvc9/discussion/311983
- 往届挑战与论文（10 票 / 1 评论）：https://www.kaggle.com/competitions/geolifeclef-2022-lifeclef-2022-fgvc9/discussion/312112
- 单标签误导讨论（3 票 / 6 评论）：https://www.kaggle.com/competitions/geolifeclef-2022-lifeclef-2022-fgvc9/discussion/325767
