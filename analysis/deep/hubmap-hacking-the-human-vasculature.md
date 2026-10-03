# HuBMAP Vasculature 深读：噪声标注利用 × bbox-first × dilation 之谜

> 赛事：Research ｜ 主题 cv（医学病理 WSI 实例分割）｜ 1021 队 ｜ 代码赛 ｜ 指标：OpenImagesObjDetectionSegmentationAP（bbox+mask 实例分割 AP，bbox 主导）
> 材料基础：`digests/hubmap-hacking-the-human-vasculature.md`（6 篇正文：3rd/1st/9th/7th + 上届冠军索引帖 + GM 心情帖；80 条讨论索引）+ 9 张图（428447×4 / 429060×1 / 430242×4）
> 深读时间：2026-10（Tier A #32）

## 0. 一句话重述：这道题真正在考什么

题面是"肾活检 WSI 中检测并分割血管（blood_vessel / glomerulus / 其他）"，实际被考的是**三件与模型无关的事**：

1. **dataset2 是带噪数据**：比赛提供"干净小数据（dataset1，wsi1/2 全标注）+ 噪声大数据（dataset2，wsi3/4，标注不全且系统性偏小）"；如何利用 dataset2 是分水岭——3rd 用"多阶段预训练→微调"（+4–6% LB），1st 用"混合 batch + EMA"，9th 重标 dataset2 的 bbox，7th 用伪标签 + 膨胀标注。
2. **bbox 主导指标**：1st 明说"AP 主要靠 bbox，mask 影响次要"，并把精力集中在检测；9th 用 160 个检测结果 + 4 个分割模型的两阶段结构。mask 监督不仅不亏，还能反哺 bbox（1st 对照表 +0.006–0.010）。
3. **dilation 之谜**：公榜显示 mask 膨胀能涨分，但它的本质是补偿 dataset2 的标注尺度偏差——9th 用 dataset1 训练的重标器修正 dataset2 后，dilation 红利消失；7th 曾怀疑这是"对 LB 过拟合"；1st 靠最后一天运气保留了对照提交。

一句话：**这是一场"噪声标注利用 + 检测优先 + 后处理辨伪"的比赛**——名次差距来自对 dataset2 的用法，而非 backbone。

## 1. 材料与角色

| 帖子 | 作者 | 票数 | 角色与独有信息 |
| --- | --- | --- | --- |
| [428296](https://www.kaggle.com/competitions/hubmap-hacking-the-human-vasculature/discussion/428296) 公榜 1/私榜 3 | Nischay | 219 | 情感帖（无技术内容），但指向 3rd 技术帖 430242；说明"公榜 1 → 私榜 3"的落差 |
| [429060](https://www.kaggle.com/competitions/hubmap-hacking-the-human-vasculature/discussion/429060) 1st | — | 82 | RTMDet-x + **EMA（称 crucial）**；i-split 验证（难但真实）；mask 监督反哺 bbox 的对照表；WBF 5 模型；dilation "最后一天靠运气"；EMA 工程 tips |
| [428295](https://www.kaggle.com/competitions/hubmap-hacking-the-human-vasculature/discussion/428295) 7th | — | 63 | Mask R-CNN（Swin/HTC）伪标签流水线；**dilation 怀疑是 LB 过拟合**；伪标签 + 膨胀 ds2 把有/无 dilation 的差距从 0.1 压到 0.02 |
| [430242](https://www.kaggle.com/competitions/hubmap-hacking-the-human-vasculature/discussion/430242) 3rd | Nischay | 61 | **多阶段**：ds2 高 LR 轻增广预训练 → ds1 低 LR 重增广微调（+4–6% LB）；5 MMdet 异构模型；WBF + erode/dilate（+0.005）；伪标签无增益 |
| [412307](https://www.kaggle.com/competitions/hubmap-hacking-the-human-vasculature/discussion/412307) 上届冠军索引 | — | 44 | HuBMAP 2022 organ、2021 kidney 的冠军方案链接聚合——系列传承与阅读路径 |
| [428447](https://www.kaggle.com/competitions/hubmap-hacking-the-human-vasculature/discussion/428447) 9th | — | 43 | 两阶段（检测 10 模型 × 16 TTA → WBF 160 结果；分割 EffB1/B2-Unet）；**用 ds1 模型修正 ds2 的 bbox 标注**（IoU>0.4、FP/(TP+FP)>0.1）；3% bbox dilation +0.005 |

**材料缺口（受"不扩采"约束，登记备查）**：2nd(429240)、4th(428994)、"[LB 0.481] my experiment results"(419143,70 票)、**"Dilation increases the score, who understands why?"(416901,48 票——本场核心谜题的社区讨论)**、public 9th/private 295th(428392,32 票)、OneFormer/UNet(412316) 等未收录正文。

## 2. 逐方案对照矩阵

| 维度 | 1st | 3rd Nischay | 7th | 9th |
| --- | --- | --- | --- | --- |
| 主模型 | RTMDet-x（bbox 优先） | 2×ViT-Adapter-L + CBNetV2 + DetectoRS-ResNeXt101 + ResNet50（MMdet） | Mask R-CNN（Swin backbone + HTC RoI） | 检测：YOLOv5x6/v7x/v8l/v8x；分割：EffB1/B2-Unet |
| dataset2 用法 | 混合 batch（3 张 ds1 + 5 张 ds2） | **两阶段**：ds2 预训练（~10 epoch，LR 0.02+，轻增广）→ ds1 微调（15–25 epoch，低 LR 至 1e-7，重增广、高分辨率） | 先 ds1 训 5 折 → 给 ds2/ds3 打伪标签 → 用 ds1+ds2+ds3 重训（ds2 同时保留原膨胀标注与伪标签） | 用 ds1 训练检测器**重标 ds2 的 bbox**（IoU>0.4、FP 比>0.1）后再用 |
| 验证策略 | i-split（按 location 'i' 划分，0.43/0.68） | 折内 ds1 | 5 折 | 2 折按 wsi 交换（wsi1↔wsi2） |
| 增广/TTA | 强几何增广（旋转 ±180、scale 0.1–2.0）；无 TTA | 轻/重两套（stage1/stage2）；flip TTA | resize 1024/1536 + hvflip | 16 TTA = 8 组合（h/v flip、rot90）× 2 尺度 |
| 集成 | WBF：3×RTMDet + YOLOX-x + Mask R-CNN（bbox）；mask 用 Mask R-CNN 头 1440 | WBF（TTA 用 NMS）；5 架构异构 | RPN + RoI head 双层集成 | WBF：10 模型 × 16 TTA = **160 检测结果**（NMS 0.6 / WBF 0.7）；分割 4 模型平均 |
| 分割来源 | Mask R-CNN 头（bbox 统一） | 各模型 mask head（loss ×2/×4） | HTC mask 头 | 检测框 + 4ch（RGB+框 mask）输入 UNet，**不用检测结果当 mask 框** |
| 后处理 | 无 dilation（另一提交带） | erode → dilate（+0.005） | dilation、去小 mask、去含 glomerulus 的 mask | 3% bbox dilation（+0.005；另一提交不带） |
| 报告成绩 | 单模型私榜 0.565+；集成私榜 0.589（公榜 0.317，原文如此） | 最佳单模型公榜 0.600 / 私榜 0.589；多阶段 +4–6% LB | 有/无 dilation 差距 0.1 → 0.02 | 带 dilation 0.580/0.549；不带 0.572/0.560 |
| 失败清单 | — | 伪标签（ds3）无增益 | test 伪标签、Mendeley 外部数据、YOLOv8、Puzzle 提交 | ds3 半监督无效 |

## 3. 共识、分歧与裁决

### 共识一：dataset2 是"噪声大数据"，必须换一种用法（4/4）

3rd：先预训练再微调，把 ds2 当弱监督表示来源（+4–6% LB）；
1st：batch 内 3:5 混合，配 EMA 稳定训练；
9th：不直接用 ds2 标注，先用 ds1 模型重标 bbox；
7th：用伪标签替代/补充 ds2 的原始标注。

**裁决**：dataset2 的价值在"数据量与尺度先验"，其标注不能与 ds1 等价对待；三族有效解——**阶段性使用（预训练/微调分离）、修正后使用（重标）、替代性使用（伪标签）**。直接把 ds1+ds2 混在一起监督训练会引入标注尺度/完整性偏差。置信度：高（4 队独立 + 数字）。

### 共识二：bbox 决定分数，mask 是次要项且能反哺 bbox（1st 明说，9th 结构佐证）

1st："AP 主要靠 bbox；mask 精度影响小"——因此集中优化 bbox，mask 交给 Mask R-CNN 头；其对照表显示 mask 监督让 bbox mAP 从 0.424 → 0.430–0.434。
9th：检测用 160 个结果的大集成，分割只 4 个模型、TTA 都不用（运行时约束）。
3rd：HTC 系模型给 mask head loss ×2/×4 权重。

**裁决**：实例分割 AP 的资源分配顺序 = bbox > mask；mask 监督作为 bbox 的正则化项有效（形状边界迫使特征更锐利）。置信度：中高（1st 数字 + 9th 结构 + 3rd 权重）。

### 共识三：WBF 集成 + 异构模型是标准操作（4/4）

3rd：NMS 用于 TTA、WBF 用于集成（分工明确）；CNN + Transformer 混合增加多样性。
9th：160 结果 WBF（NMS 0.6 / WBF 0.7）。
1st：5 模型 WBF（3×RTMDet + YOLOX + Mask R-CNN）。
7th：RPN + RoI head 双层集成（引 Sartorius 方案）。

**裁决**：分割/检测赛的最后 1–2 分来自集成；WBF 比 NMS 更适合跨模型融合，异构比同构有效。置信度：高。

### 分歧一：dilation 到底要不要用（本场核心张力）

支持：公榜普遍显示 mask/bbox 膨胀涨分（3rd erode+dilate +0.005；9th 3% bbox dilation +0.005；7th 首版 +0.1）。
反对/修正：7th 发现 ds1-only 模型 dilation 有害 → 怀疑其来自 ds2 噪声、是 LB 过拟合；9th 重标 ds2 后"dilation 红利几乎消失、不用 dilation 也过 0.5"。
1st：直到最后一天才发现 dilation，最终保留有/无两个提交，"纯属运气"。

**裁决**：dilation 的增益不是模型能力，而是**标注尺度偏差的补偿**——它对"训练含 ds2"的模型有效、对 ds1-only 模型有害；修正 ds2 标注后增益消失（9th 的因果闭环）。纪律结论：对这类"后处理试纸"，必须保留一个不施加该后处理的对照提交（1st 的明示建议）；否则公榜红利会在私榜反噬。置信度：中高（3 队联合证据 + 机制一致）。

### 分歧二：验证划分——要难而真，不要易而虚

1st：i-split（按 location 'i' 划分）比随机划分难——bbox mAP 0.43 vs 0.47、segm 0.68 vs 0.72，但更接近测试分布；公开承认"验证分数更低"仍坚持使用。
9th：2 折按 wsi 交换（train wsi1 + updated-ds2 → val wsi2），直接模拟"新 WSI 泛化"。

**裁决**：本场测试来自未见 WSI，验证必须按 WSI/位置分组；随机划分的高分是虚高（与 L6/T3 一致）。置信度：高。

### 分歧三：伪标签/半监督（dataset3）

3rd：用 ds3 伪标签训练部分模型，**LB 无提升**；
9th：ds3 半监督"does not work"；
7th：用了 ds2/ds3 伪标签，但收益未量化，主要用于缩小 dilation 差距。

**裁决**：在本场，伪标签不是主杠杆；当核心矛盾是"标注尺度偏差"时，重标/多阶段比伪标签更直接（对照 T6：预训练式稳、混训险）。置信度：中。

## 4. 增量数字账

| 动作 | 数字 | 来源 |
| --- | --- | --- |
| 多阶段增益（3rd） | 验证 +2–3%；LB **+4–6%** | 3rd |
| 3rd 单模型 | ViT-Adapter-L 公榜 0.600 / 私榜 0.589（全场最佳单模型）；CBNetV2 0.567；DetectoRS 0.573 / ResNet50 0.558 | 3rd |
| 3rd 后处理 | erode + 单次 dilate：CV/LB **+0.005** | 3rd |
| 1st mask 监督对照（bbox mAP） | 无 mask 0.424 → 仅随机旋转重算框 0.434 → mask 头 0.430（segm60 0.68）→ 两者 0.432（0.688） | 1st |
| 1st 验证划分差异 | random：bbox 0.47 / segm60 0.72；i-split：0.43 / 0.68 | 1st |
| 1st batch 混比 | 8 = 3 张 ds1 + 5 张 ds2 | 1st |
| 1st 单模型 | 单折无 TTA 私榜 0.565+（足够金牌） | 1st |
| 1st 集成 | 私榜 0.589 / 公榜 0.317（原文如此；公榜值异常低，疑为笔误，待核） | 1st |
| 9th 集成规模 | 10 检测模型 × 16 TTA = **160** 结果 WBF（校验：8 flip/rot × 2 尺度 = 16 ✓） | 9th |
| 9th 阈值 | 单模型 NMS IoU 0.6；WBF IoU 0.7；分割二值化 0.5 | 9th |
| 9th ds2 重标条件 | IoU > 0.4 且 FP/(TP+FP) > 0.1；重标后 bbox 变大、数量不变 | 9th |
| 9th 双提交 | 带 3% dilation：0.580/0.549；不带：0.572/0.560 | 9th |
| 7th dilation 差距 | 首版有/无差 **0.1** → 伪标签+膨胀 ds2 后差 **0.02**（双榜带 dilation 仍更好） | 7th |
| EMA 动量对照 | 图 1：momentum 1.0（无 EMA）波动 0.36–0.42；0.001 快升后衰减；0.0005 峰值 ~0.425；0.00025 慢升峰值 ~0.43 | 1st（图 1） |

**结构校验（2 处吻合）**

1. 9th：10 × 16 = 160 ✓，且 16 = 8 × 2 ✓；
2. 9th 双提交的"带 dilation 公榜更好（0.580>0.572）但私榜更差（0.549<0.560）"——与 7th 的"dilation 是公榜红利"怀疑、1st 的"保留对照提交"建议完全一致，三队互证。

## 5. 机制推演

**M1｜为什么"ds2 预训练 → ds1 微调"有效（3rd +4–6%）**：ds2 大而脏，适合提供**表示与尺度先验**（高 LR、轻增广、低分辨率、~10 epoch）；ds1 小而净，适合**重建决策边界**（低 LR 至 1e-7、重增广、高分辨率、15–25 epoch）。两段目标不同：第一段求广度，第二段求精度。把两者混在一起监督，噪声梯度会干扰干净边界的学习。

**M2｜dilation 之谜的因果链**：dataset2 标注由不同标注者/流程产生，边界系统性偏小 → 含 ds2 的模型学到"偏小"的尺度先验 → 推理时膨胀补偿偏差（涨分）。证据链：① ds1-only 时 dilation 有害（7th）；② 用 ds1 模型重标 ds2 后，dilation 红利消失（9th）；③ 1st 只在最后一天尝试，仍是涨分（当时训练混了 ds2）。**后处理的"增益"方向可以反过来诊断训练数据的系统性偏差**——这是本场最可迁移的思维。

**M3｜为什么 bbox 主导实例分割 AP**：指标在多个 IoU 阈值下统计，bbox 定位错误直接杀死所有更高阈值；mask 精度只在较低 IoU 区间做边际调整（1st 的 mask 头让 bbox +0.006，但 segm 提升对总分贡献小）。资源分配因此是"先 bbox 后 mask"；但 mask 监督的副产品（边界感知特征）让 bbox 也受益。

**M4｜EMA 为什么 crucial（1st 的反常观察）**：图 1 显示无 EMA（momentum 1.0）验证曲线波动 0.36–0.42；EMA 动量越小（记忆越长），曲线越平滑、峰值越高（0.00025 峰值 ~0.43）。1st 特别指出 EMA 同时提升验证与**训练**精度——说明它不是普通泛化正则，而是"高 LR 轨迹上的权重降噪/集成"：训练集精度提升来自权重平均消除了训练后期的震荡漂移。工程 tip：单次训练保留多个 EMA 快照（不同动量）= 免费的多模型集成。

**M5｜为什么 160 个检测结果的 WBF 值得（9th）**：测试集很小（WSI 数量有限），推理预算允许把检测精度推到极致；分割被简化为"每个框内的局部任务"（4ch 输入含框 mask），不需要大集成。这是"按指标权重分配算力"的直接体现：检测重、分割轻。

**M6｜公榜/私榜分歧与对照提交纪律**：dilation 在公榜上的收益（+0.005~0.1）远大于私榜差异（甚至反向），因为公榜子集与 ds2/尺度偏差的耦合更强。7th 用伪标签+膨胀 ds2 把"有/无 dilation"的差距从 0.1 压到 0.02，但方向仍是带 dilation 更好；1st 靠保留对照提交对冲风险。**在无法解释后处理增益来源时，"一正一反对照提交"是唯一稳健策略。**

## 6. 证据分级

| 断言 | 等级 | 说明 |
| --- | --- | --- |
| 多阶段 +4–6% LB | 自述 + 流程图 + 开源代码 | 中高 |
| dataset2 标注偏小 | 三队独立行为证据（7th 怀疑/9th 重标/3rd 只在 ds1 上微调） | 中高（无官方声明） |
| mask 监督提升 bbox | 1st 对照表（0.424→0.434） | 中（单队、数字小） |
| i-split vs random 差异 | 1st 数字 | 中 |
| 9th 重标后 dilation 红利消失 | 9th 自述 + 流程图 + 条件定义 | 中高 |
| 公榜 dilation 增益 | 9th/7th/1st 的公榜数字 | 中低（公榜） |
| EMA 曲线 | 图 1 可视化 + 1st 自述 | 中（图为单次实验） |
| 伪标签无增益 | 3rd/9th 自述 | 中 |

## 7. 边界条件与反事实

- **反事实 1**：若不用 dataset2（只 ds1）→ 数据量骤减；7th/9th 显示 ds1-only 时 dilation 反而有害，说明 ds1-only 的尺度先验不同；1st 的 0.565 单模型已是金牌下限，但集成成绩依赖 ds2。
- **反事实 2**：若 ds1+ds2 直接混训（无阶段/重标/伪标签）→ 标注尺度偏差与不完整性直接进入监督信号；三队的不同规避方式即为反证。
- **反事实 3**：若把资源押在 mask 上 → 指标收益有限（1st 明说 mask minor；9th 的分割不设 TTA）。
- **反事实 4**：若全押 dilation → 公榜收益与私榜风险不对称（9th 双提交的 0.580/0.549 vs 0.572/0.560；7th 的 0.1→0.02 收敛）。
- **边界**：本场结构依赖"干净小数据 + 噪声大数据"的双数据集设定；纯干净数据任务不需要多阶段，但 EMA、WBF、mask 监督反哺 bbox、难划分验证仍然通用。

## 8. 悬案与失败学

**悬案**

1. **"Dilation increases the score, who understands why?"（416901，48 票）未收录**：本场核心谜题的社区讨论正文缺失；9th 的重标实验已给出机制，但官方/社区的最终解释未存档。
2. 2nd(429240)、4th(428994) 方案未收录——四强中两强的结构缺失，集成配方的全景不完整。
3. 428392 "public 9th / private 295th"（32 票）未收录——公榜过拟合的极端案例，与 dilation 之谜直接相关。
4. 1st 的公榜 0.317 与私榜 0.589 的巨大反差（原文如此）无法解释，疑为笔误，待核。

**失败学（跨队合集）**

- 半监督/伪标签：ds3 伪标签无增益（3rd）；ds3 半监督失败（9th）；test 图伪标签（7th）。
- 外部数据：Mendeley 数据集无效（7th）。
- 模型选择：YOLOv8 在 7th 处失败；Puzzle 提交不可行（7th）。
- 数据用法：ds1-only + dilation 有害（7th/9th）——**先把"训练集构成"与"后处理方向"对齐，再谈模型**。

## 9. 图表证据

> 路径相对本文件（`analysis/deep/`）：`../../intel/hubmap-hacking-the-human-vasculature/bodies/<topic>_img/NN.png`

**图 1：1st 的 EMA 动量对照曲线**（topic 429060）——`../../intel/hubmap-hacking-the-human-vasculature/bodies/429060_img/01.png`

*读图结论*：无 EMA（momentum 1.0）波动 0.36–0.42；0.001 快速上升后衰减；0.0005 峰值 ~0.425；0.00025 慢升、峰值 ~0.43 且后期稳定。**动量越小（记忆越长）→ 曲线越稳、峰值越高**；1st 建议单次训练保留多个 EMA 快照（不同动量）= 免费集成。

**图 2：3rd 的多阶段训练流程**（topic 430242）——`../../intel/hubmap-hacking-the-human-vasculature/bodies/430242_img/01.png`

*读图结论*：DS1+DS2 → Stage 1（Dataset 2：轻增广、高 LR、低分辨率）→ Stage 2（Dataset 1：重增广、低 LR、高分辨率）→ inference。**"脏数据学表示、净数据学决策"的两段结构图**；正文的 +4–6% LB 就来自这个切换。

**图 3：3rd 的 5 模型集成与 erode→dilate 后处理**（topic 430242）——`../../intel/hubmap-hacking-the-human-vasculature/bodies/430242_img/03.png`

*读图结论*：2×ViT-Adapter + CBNetV2 + ResNeXt101D + ResNet50 → NMS TTA → WBF 集成 → **Erode → Dilate** → Final。分工清晰：NMS 管 TTA 内部去重、WBF 管跨模型融合；erode+dilate 的"开运算"修复集成后 mask 的粘连/毛刺（+0.005）。

**图 4：9th 的两阶段检测→分割管线**（topic 428447）——`../../intel/hubmap-hacking-the-human-vasculature/bodies/428447_img/01.png`

*读图结论*：检测（YOLOv5/7/8）→ WBF → 检测框 → 4ch 图像（RGB + 框 mask）→ 分割（EffB1/B2-Unet）→ 平均 → 每框 mask → 按置信度合并提交。**分割模型不使用检测预测当框，而用原始标注框训练**（把定位与像素任务解耦）；检测 160 结果 vs 分割 4 模型的算力分配是本场"bbox 主导"的直观注脚。

**图 5：9th 用 dataset1 模型重标 dataset2 的流程**（topic 428447）——`../../intel/hubmap-hacking-the-human-vasculature/bodies/428447_img/02.png`

*读图结论*：train = ds1（wsi1+wsi2）、val = ds2（wsi1–4）→ 训练 YOLOv5x/v8l/v8x → 用预测**更新 dataset2 的 bbox 标注**（条件 IoU>0.4 且 FP 比>0.1，框变大、数量不变）。这是"用干净数据校准脏数据"的标准流程；更新后 dilation 红利消失——因果链的关键图证。

**图 6：9th 的 2 折 wsi 交换 CV**（topic 428447）——`../../intel/hubmap-hacking-the-human-vasculature/bodies/428447_img/04.png`

*读图结论*：Fold0 训练 wsi1 + updated-ds2、验证 wsi2；Fold1 交换。**按 WSI 分组、交换验证**，直接模拟"新切片"泛化；与 1st 的 i-split 思想一致（难而真）。

## 10. 对既有笔记/playbook 的修订点

1. `notes/cv/hubmap-hacking-the-human-vasculature.md` 升级：修正指标（实例分割 AP，非 Dice）；补 6 篇作者/票数、四方案 × 10 维对照、数字账（+4–6%、0.424→0.434、160 WBF、0.1→0.02）与 6 张图证。
2. `playbook/cv.md`（医学影像/实例分割节）增补：
   - **噪声大数据的两段用法**：预训练（高 LR/轻增广/低分辨率）→ 干净微调（低 LR/重增广/高分辨率）；
   - **标注尺度偏差异常检测**：把"膨胀/腐蚀"当试纸——增益方向随训练数据来源反转，即为标注偏差信号；
   - **bbox-first 资源分配**：实例分割 AP 先保检测；mask 监督可作为 bbox 正则（+0.006~0.01）；
   - **EMA 配方**：小动量（0.00025–0.0005）+ 固定 LR，单次训练留多个 EMA 快照；
   - **对照提交纪律**：无法解释的后处理收益必须"带/不带"双提交。
3. `playbook/00-通用方法论.md` 增补：**"后处理即数据诊断"**（后处理的增益来源可以反推训练数据的系统偏差）；**"难而真的验证划分"**（i-split/WSI 分组 vs 随机划分的分数差本身就是泄漏量尺）。
4. `analysis/THEORY.md`（Batch 4 收尾扩 v0.4）候选：
   - **L47｜噪声数据的两段用法**：脏数据预训练学表示 + 净数据微调学决策；证据 = HuBMAP 3rd（+4–6% LB）+ isic 预训练 vs 混训；反例边界 = 分布差异过大时预训练也可能无效（isic 域分类器 0.99 下仍有效，但增益小）。
   - **L48｜后处理增益方向 = 训练数据偏差的试纸**：证据 = HuBMAP dilation 三队（7th 反转、9th 修正后消失、1st 运气）；与 godaddy 的"口径修正"同族（先诊断数据，再调后处理）。

## 11. 出处

- 3rd（Nischay，61 票）：https://www.kaggle.com/competitions/hubmap-hacking-the-human-vasculature/discussion/430242
- 1st（82 票）：https://www.kaggle.com/competitions/hubmap-hacking-the-human-vasculature/discussion/429060
- 7th（63 票）：https://www.kaggle.com/competitions/hubmap-hacking-the-human-vasculature/discussion/428295
- 9th（43 票）：https://www.kaggle.com/competitions/hubmap-hacking-the-human-vasculature/discussion/428447
- 上届冠军索引（44 票）：https://www.kaggle.com/competitions/hubmap-hacking-the-human-vasculature/discussion/412307
- GM 心情帖（219 票，指向 3rd）：https://www.kaggle.com/competitions/hubmap-hacking-the-human-vasculature/discussion/428296
- 缺口登记（未收录正文）：2nd(429240)、4th(428994)、419143、**dilation 讨论(416901)**、428392(public 9th/private 295th)、412316 等
