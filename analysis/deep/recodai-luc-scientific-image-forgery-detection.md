# RECOD.ai-LUC Scientific Image Forgery Detection 轻量深读（Tier B）

> 赛事：Research ｜ 主题 cv（科研图像 copy-move 伪造检测）｜ 1564 队 ｜ 代码赛 ｜ 指标：RecodAI F1（authentic 全对/全错 + 实例 F1 + 多预测惩罚）
> 材料基础：`digests/recodai-luc-scientific-image-forgery-detection.md`（6 篇正文：1st 695702 / 2nd 694397 / 65th 694442 / 29th 694168 / 私榜 3rd 674890 / DCT 综述 613066；80 条主题索引）+ 12 张归档图
> 轻读时间：2026-10（Tier B B12）

## 1. 一句话重述与数字账

检测科研论文图像（Western blot、显微/宏观照片等）中的 copy-move 伪造：authentic 图预测对得 1.0、预测成伪造得 0；伪造图按匈牙利匹配的实例 F1 计分，且多预测实例会被惩罚。本场的核心结论是**"把检测重构成检索"**：前三名都是"面板切分 + 相似检索/特征匹配 + 几何验证"路线（1st 是嵌入检索 + 条带级匹配，2nd/私榜 3rd 甚至是纯经典 SIFT/SAM3 无训练），纯分割模型（65th、29th 的 DINOv2 segmenter）只能排在中游。

| 关键数字 | 值 | 来源 |
| --- | --- | --- |
| 1st（695702） | 公榜推进（250+ 次提交）：0.327 → 0.341 → 0.353 → 0.370 → 0.375 → **0.431** → 0.456–0.458；**条带级（lane）匹配是主引擎（0.375→0.431）**，显微嵌入升级贡献 0.431→0.446；数据 = PubMed Central 约 200 万 tar.gz（14TB）→ 去重后 660 万 blot + 1630 万显微图；面板检测 11.3k–12.3k 标注图；条带检测标注 3,732 图 → 对 ~600 万 blot 生成 **2700 万** 框；匹配：显微 SIFT+LightGlue+RANSAC、blot ALIKED+LightGlue+MAGSAC；检索嵌入 SupCon（温度 0.07–0.09、nextvit_small）；无匹配时退回公共分割 kernel（+0.005–0.01）；最终私榜 0.550（选了公榜 0.450 那版，而非公榜 0.458/私榜 0.541 的版本） | 695702 |
| 2nd（694397） | 纯经典路线（无深度匹配）：YOLOv8-m 面板（3 类）与文本检测（~800 手标 + ~2000 合成，5 模型 WBF）；SIFT `contrast_threshold=0.001`（默认的 1/40）、<1024px 先 4× 放大；**G2NN（α=0.7）+ FLANN KDTree**（O(N²)→O(N log N)）；RANSAC 局部/全局 + HDBSCAN；按三类图像分别设 inlier 阈值；两阶段聚类合并（H 相似 <0.02、IoMin ≥0.3）；凸包 + H 误差细化掩码；公榜 3rd → 私榜 2nd；SURF/ORB/AKAZE/SuperPoint 与深度 CMFD 模型都失败 | 694397 |
| 65th（694442） | DINOv2-base（冻结 + 末 12 层解冻）+ 微型卷积解码器（768→384→192→96），518×518；两阶段训练（解码器预热 lr 1e-5 → 联合微调 backbone lr 5e-7）；翻转 TTA×3；**梯度增强掩码**（alpha=0.45）；面积/概率阈值网格搜索（AREA_MIN≈200、PROB_MIN≈0.20–0.22）；结论：copy-move 本质是"自相似"，DINOv2 自蒸馏特征天然匹配 | 694442 |
| 29th（694168） | DinoV2Segmenter（仅末 5 个 block + LayerNorm 可训）+ 卷积解码器；外部数据 RSIID（39,423 张篡改图 / 2,923 张原图）+ 反事实重构（co 对）→ 合计 51,489 样本（24,300 authentic / 27,189 forged）；StratifiedGroupKFold 5 折；BCE、50 epochs、8×TTA；**指标感知后处理**：q999≥0.95 gate、掩码阈值 0.3、只交单个合并掩码（避免超额实例惩罚）、按 split 跟踪 lift 选"每个 split 都为正"的最保守阈值 | 694168 |
| 私榜 3rd（674890） | 无训练：SAM3 文本提示切面板（两轮提示，第二轮找生物对象；无结果则注入固定切块）→ CLAHE + 文本/箭头遮除 → SIFT+FLANN+Lowe+RANSAC → 收紧到 inlier 包围盒；自述"在合成单图数据上训练的 NN 无法迁移到 figure 级补充测试" | 674890 |
| 文献（613066） | DCT 系数符号 + 元胞自动机特征 + KDTree 匹配的传统 CMFD，对 JPEG/噪声更稳健（38 票） | 613066 |
| 社区争议 | "指标极不公平"（10 票）、"掩码同时包含复制源与目标"（10 票 / 10 评论）、0.303 平台、CV/LB 严重落差、"train 与 supplemental 差异巨大"（7 票）、全 authentic 基线（6 票） | 索引 |

## 2. 逐方案对照矩阵

| 维度 | 1st | 2nd | 65th | 29th | 私榜 3rd |
| --- | --- | --- | --- | --- | --- |
| 核心 | 检索 + 条带级匹配 | 经典 SIFT + G2NN | 分割（DINOv2 解码器） | 分割（DinoV2Segmenter）+ 指标工程 | SAM3 + SIFT（无训练） |
| 面板/文本预处理 | YOLO 面板检测 | YOLO 面板 + 文本检测 | 无 | 无 | SAM3 提示切分 + 文本遮除 |
| 外部数据 | 14TB PMC 自建（6.6M+16.3M 图） | 2,000 BioFors 图（合成训练） | 无 | RSIID 51k 样本 | 无 |
| 训练量 | 大（嵌入 + 检测器 + 匹配） | 小（YOLO only） | 中（两阶段） | 中 | 零 |
| 后处理 | 阈值 + 兜底 kernel | 聚类合并 + 掩码细化 | 梯度增强 + 阈值网格 | q999 gate + 单掩码 + per-split lift | inlier 包围盒 |
| 名次 | 1st | 2nd | 65th | 29th | 私 3rd |

## 3. 共识、分歧与裁决

### 共识一：copy-move 检测的本质是"自相似检索"，检索+几何验证 > 纯分割（1st、2nd、私 3rd；置信度高）

前三名的共同结构都是"找重复/重叠区域 + 几何验证"；1st 明说 copy-move 要找的是"语义与纹理相同的两个区域"而非 OOD 物体；2nd/3rd 用纯经典匹配分别拿到私榜 2/3。**裁决**：这类任务的 SOTA 形态是检索匹配（嵌入 or 关键点），分割网络是补充/兜底而非主轴。置信度：高（名次 + 1st 的 +0.056 条带级增益）。

### 共识二：面板/文本预处理是必要模块（1st、2nd、私 3rd；置信度中高）

1st 用 YOLO 检测 blot/显微面板；2nd 用面板+文本双 YOLO（文本误匹配如 "10 mm" 的 "mm"）；3rd 用 SAM3 两轮提示切分并遮除文本/箭头。**裁决**：科研图像的版面结构（多面板、图注文字）会制造大量假匹配，先切分再匹配是标准前置。置信度：中高。

### 共识三：指标感知的后处理/提交选择直接决定名次（1st、65th、29th；置信度高）

authentic 图错报为伪造 = 1.0 直接归零；伪造图按实例 F1 且多预测要乘 `len(gt)/max(len(pred),len(gt))` 惩罚。1st 选了私榜 0.550 而放弃公榜 0.458 的版本；65th 网格搜索 AREA/PROB 阈值；29th 用 q999≥0.95 门控 + 单掩码 + 每个 split 都为正 lift 的保守阈值。**裁决**：在这类"错报代价极高"的指标下，保守判定 + 单实例提交 + 按 split 验证 lift 是必要动作。置信度：高。

### 分歧一：数据驱动分割 vs 经典匹配（65th/29th vs 1st/2nd/3rd；置信度中高）

65th（DINOv2+小解码器）与 29th（DinoV2Segmenter + 指标工程）代表分割路线，名次 65/29；1st/2nd/3rd 的检索匹配路线占据前三。**裁决**：纯分割在本任务的天花板更低（伪造=自相似，不是像素异常）；可行的组合是"检索为主 + 分割兜底"（1st 的公共 kernel 兜底仅 +0.005–0.01）。置信度：中高。

### 事件：指标与标签的争议是主要风险（641092、613200、613694、657899；置信度中高）

"指标极不公平"（10 票）、"掩码同时覆盖复制源与目标"（10 票 / 10 评论）、标签错误讨论、"train 与 supplemental 差异巨大"（7 票）说明评测口径与数据分布都需要自行校准。**裁决**：先精确复现指标（含惩罚项与 authentic 规则）再选模型；把不同数据 split 的 lift 分开跟踪。置信度：中高。

## 4. 证据分级

| 断言 | 等级 | 说明 |
| --- | --- | --- |
| 1st 的条带级增益（0.375→0.431）与最终 0.550 | 自述 + 分数截图 + 管线图 | 中高 |
| 2nd 的经典匹配全流程与失败清单 | 自述 + 开源代码 | 高 |
| 29th 的 RSIID 数据规模与指标感知框架 | 自述（含代码片段/表格） | 中高 |
| 65th 的 DINOv2 训练细节 | 自述 | 中 |
| 私榜 3rd 的 SAM3 流程 | 自述 | 中 |
| 指标定义（authentic/F1/惩罚） | 29th 转述官方 metric + 社区争议帖 | 中高 |

## 5. 悬案与缺口（登记）

- 1st 如何把 0.458 与 0.450 版本区分（内部 CV 细节）未展开；
- 官方 metric 文档未归档；社区"指标不公平"的具体诉求未细读；
- 2nd/3rd 的开源实现未运行核对；
- 归档 12 图仅内嵌 3 张（其余留待图像层）；
- **图证缺口**：无（12 张归档图充足）。

## 6. 图表证据

![1st 的三段式流程](../../intel/recodai-luc-scientific-image-forgery-detection/bodies/695702_img/01.png)

**图 1**（topic 695702，1st）：面板检测 → 嵌入检索（相似度表）→ 匹配与定位（红/蓝框标出复制区域）——显微图示例。

![公私榜选择](../../intel/recodai-luc-scientific-image-forgery-detection/bodies/695702_img/02.png)

**图 2**（topic 695702，1st）：两版提交对照——"body img added" 公榜 0.458 / 私榜 0.541；最终提交公榜 0.450 / 私榜 **0.550**。公榜高不等于私榜好。

![条带级掩码合并启发式](../../intel/recodai-luc-scientific-image-forgery-detection/bodies/695702_img/11.png)

**图 3**（topic 695702，1st）：条带级匹配的启发式——当某面板 >50% 的条带命中时，用整条带（全行）替代碎片化小框，把 0.416 推到 0.431。

## 7. 出处

- 1st（37 票）：https://www.kaggle.com/competitions/recodai-luc-scientific-image-forgery-detection/discussion/695702
- 2nd（15 票）：https://www.kaggle.com/competitions/recodai-luc-scientific-image-forgery-detection/discussion/694397
- 65th DINOv2（8 票）：https://www.kaggle.com/competitions/recodai-luc-scientific-image-forgery-detection/discussion/694442
- 29th 分割 + 指标工程（7 票）：https://www.kaggle.com/competitions/recodai-luc-scientific-image-forgery-detection/discussion/694168
- 私榜 3rd / 公榜 8th（7 票）：https://www.kaggle.com/competitions/recodai-luc-scientific-image-forgery-detection/discussion/674890
- DCT copy-move 文献（38 票）：https://www.kaggle.com/competitions/recodai-luc-scientific-image-forgery-detection/discussion/613066
- 指标争议（10 票）：https://www.kaggle.com/competitions/recodai-luc-scientific-image-forgery-detection/discussion/641092
- 掩码含源+目标说明（10 票）：https://www.kaggle.com/competitions/recodai-luc-scientific-image-forgery-detection/discussion/613200
- train vs supplemental 差异（7 票）：https://www.kaggle.com/competitions/recodai-luc-scientific-image-forgery-detection/discussion/657899
