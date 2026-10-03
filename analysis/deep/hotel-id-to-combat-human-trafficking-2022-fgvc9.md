# Hotel-ID to Combat Human Trafficking 2022（FGVC9）轻量深读（Tier B）

> 赛事：Research（代码赛）｜ 主题 cv（酒店图像检索/细粒度识别）｜ 82 队 ｜ 指标 MAP@{K} ｜ 截止 2022-05-30
> 材料基础：`digests/hotel-id-to-combat-human-trafficking-2022-fgvc9.md`（6 篇正文：1st 328281 / 公开私榜 3rd 328237 / 往届资源 313362 / 2nd 328345 / 奖牌争议 314885 / 往届实效提问 316799；29 条主题索引）+ 0 张归档图
> 轻读时间：2026-10（Tier B B19）

## 1. 一句话重述与数字账

用房间/酒店照片做**同一酒店检索**（反人口贩卖取证），FGVC9/CVPR workshop 赛。核心难点是测试/查询图有**大面积遮挡掩码**，而训练图没有；三条获奖路线分别用三种方式处理这个域差：1st 造了 **BlendFlip** 遮挡增强（+0.03–0.04 mAP）+ 5 模型嵌入集成；2nd 用**统计掩码生成 + 50K 外部数据 + 子中心 ArcFace**；3rd 干脆改用 **logits 分类**绕开检索。赛事另一条主线是社会公益赛的关注度问题：无奖牌/奖金，参赛仅 82 队，"往届成果有没有真的用于反贩卖"被公开追问但无归档答复。

| 关键数字 | 值 | 来源 |
| --- | --- | --- |
| 规模与机制 | **82 队**；代码赛（MAP@{K}）；无奖牌/积分/奖金/周边；获奖者去 CVPR workshop 展示 | 314885 |
| 1st（328281） | 5 模型集成（1024×1024 与 384×384 两种尺寸），**ArcFace** 训练，嵌入 1536D → 拼接后 **PCA 到 3072D（保留 99% 方差）** → KNN；无后处理/重排；**BlendFlip 贡献约 0.03–0.04 mAP**（作者称 CVPR 论文将补消融）；BlendFlip = 取遮挡区上下/左右最大可用邻域翻转填充，再 50/50 混合 | 328281 |
| 2nd（328345） | 50K+FGVC9；按 **md5 去重**（同 md5 不同类别删除）后保留 **45,769 个类别**；方向模型把图旋正；先全量 10–20 epoch，再对 FGVC9 的 **3116 类微调 40 epoch（+0.03）**；**sub-center ArcFace（k=3，动态 margin）**；swin-base-384 私榜 0.688、swin-large-384 0.692、eca_nfnet_l1 0.688，**集成私榜 0.717 / 公榜 0.732**；FGVC8 伪标签失败 | 328345 |
| 3rd（328237） | 多骨干（Swin、ConvNeXt、ResNet200D、EfficientNet + DOLG，尺寸 384–1024）；用 FGVC8 外部数据 + KNN 伪标签 + 均值聚合；**logits 优于 KNN**；推理约 2 小时；最佳单模 ConvNeXt XLarge 512 私榜 0.672 | 328237 |
| 数据/平台坑 | 重复图（324699）；外部数据规则问询（317922）；掩码用法（313547，12 评论）；notebook 里测试图只挂出 `abc.jpg`（322383）；提交表头要用 `image_id` 而非 `image`（324704）；Hotel-50K 来源（319203） | 索引 |
| 社会影响力追问 | 26 票"这么严肃的议题为什么没有奖牌/积分/奖金"；16 票"往届方法有没有被生产化用于反贩卖"；往届资源汇编 16 票 | 314885 / 316799 / 313362 |

## 2. 逐方案对照矩阵

| 维度 | 1st（检索 + 新增强） | 2nd（分类 + 度量损失） | 3rd（分类 + 外部数据） |
| --- | --- | --- | --- |
| 遮挡处理 | **BlendFlip 增强**（训练 50% 概率，测试全量） | 统计测试掩码分布生成训练掩码 | 用 logits 规避训练/测试掩码不一致 |
| 训练数据 | 竞赛数据 | 50K + 去重 + 方向校正 | 竞赛 + FGVC8 伪标签 |
| 损失/嵌入 | ArcFace，1536D | sub-center ArcFace（k=3，动态 margin） | — |
| 推理 | 拼接嵌入 → PCA → KNN | logits | logits |
| 私榜 | — | **0.717（集成）** | 0.672（最佳单模） |

## 3. 共识、分歧与裁决

### 共识一：遮挡/掩码域差是本场第一问题（328281 / 328345 / 328237；置信度高）

三队都用不同方式正视"训练无掩码、测试有掩码"：BlendFlip、统计掩码、logits 规避。**裁决**：检索类比赛先量化 train/test 的遮挡差；增强要与评测分布对齐（测试掩码统计），不要只做通用增强。置信度：高。

### 分歧：检索（KNN）vs 分类（logits）（328281 vs 328237 / 328345；置信度中高）

1st 用 PCA 嵌入 + KNN 拿冠军（BlendFlip 收益可量化）；2nd/3rd 都报告 logits ≥ 检索，更省事。**裁决**：两条路都要在本地建"带掩码"的验证集对比；若遮挡占主导，嵌入检索更稳；若类别多且掩码可控，logits 更快。置信度：中高。

### 事件一：外部数据与伪标签有效但需验证（328237 / 328345；置信度中）

3rd 用 FGVC8 + 伪标签（KNN 匹配、阈值 <0.5 的样本入训、均值聚合）取得前排；2nd 的 FGVC8 伪标签失败、Hotel50K 也没用上。**裁决**：外部数据先做类别映射与去重审计，再小规模对照 CV；失败案例说明"同源数据"假设要验证。置信度：中。

### 事件二：数据清洗（去重/方向/掩码统计）直接换分（328345；置信度中高）

2nd 的 md5 去重（同图不同类别的冲突删除）、方向模型旋正、3116 类微调 +0.03 都是可复现的工程收益。**裁决**：先做重复图与冲突标签审计，再做方向/掩码分布对齐。置信度：中高。

### 事件三：社会公益赛的关注度与影响力缺口（314885 / 316799；置信度中）

无奖牌与奖金导致参赛规模小（82 队），社区直接质疑"往届方法有没有被生产化"，归档无证据回答。**裁决**：参与此类比赛可积累检索/遮挡方法，但不要假设评审或传播机制完善；若关心影响力，把产出写成可复用工具而不是只交榜。置信度：中。

## 4. 证据分级

| 断言 | 等级 | 说明 |
| --- | --- | --- |
| 1st BlendFlip 与集成细节 | 1st 自述 + 4 张示意图（328281） | 中高（待 CVPR 消融复核） |
| 2nd 分数表与微调收益 | 2nd 自述 + 表格（328345） | 中高 |
| 3rd 外数据/伪标签流程 | 3rd 自述 + 表格（328237） | 中高 |
| 无奖牌与参赛规模 | 官方赛制 + 讨论帖（314885） | 高 |
| 生产化影响力 | 提问帖（316799） | 低（无答复） |

## 5. 悬案与缺口（登记）

- 1st 的 CVPR 论文与完整消融未归档（BlendFlip 增益为自述）；
- 竞赛私有测试集，完整复现不可能；各队验证口径未统一；
- 往届成果是否被反贩卖实务采用：无归档证据（316799）；
- 外部数据（FGVC8/Hotel50K）许可与规则细节未归档；
- **图证缺口**：本场 0 张归档图（目录为空），已登记。

## 6. 图表证据

本场 0/0 张归档图，**图证缺口已登记**；1st 帖中的 BlendFlip 与架构示意图（q8ZAdPK.jpg 等）为站外图床，未下载归档。

## 7. 出处

- 1st：BlendFlip + 5 模型集成（30 票 / 8 评论）：https://www.kaggle.com/competitions/hotel-id-to-combat-human-trafficking-2022-fgvc9/discussion/328281
- 2nd 方案（11 票 / 0 评论）：https://www.kaggle.com/competitions/hotel-id-to-combat-human-trafficking-2022-fgvc9/discussion/328345
- 公开/私榜 3rd（16 票 / 8 评论）：https://www.kaggle.com/competitions/hotel-id-to-combat-human-trafficking-2022-fgvc9/discussion/328237
- 奖牌/奖金争议（26 票 / 8 评论）：https://www.kaggle.com/competitions/hotel-id-to-combat-human-trafficking-2022-fgvc9/discussion/314885
- 往届实效提问（16 票 / 3 评论）：https://www.kaggle.com/competitions/hotel-id-to-combat-human-trafficking-2022-fgvc9/discussion/316799
- 往届资源汇编（16 票 / 1 评论）：https://www.kaggle.com/competitions/hotel-id-to-combat-human-trafficking-2022-fgvc9/discussion/313362
- 掩码用法讨论（6 票 / 12 评论）：https://www.kaggle.com/competitions/hotel-id-to-combat-human-trafficking-2022-fgvc9/discussion/313547
- 重复图（5 票 / 3 评论）：https://www.kaggle.com/competitions/hotel-id-to-combat-human-trafficking-2022-fgvc9/discussion/324699
