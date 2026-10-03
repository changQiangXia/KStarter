# RSNA 2022 颈椎骨折深读：87 例掩码撬动 2k 例粗标签的标签工程

> 赛事：Featured ｜ 主题 cv（医学 CT 3D）｜ 883 队 ｜ 代码赛 ｜ 指标：Weighted Mean Columnwise Log Loss（8 列：C1–C7 + patient_overall）
> 材料基础：`digests/rsna-2022-cervical-spine-fracture-detection.md`（6 篇：1st/1st-code/3rd/5th/6th + 数据详解帖；80 条讨论索引）+ 10 张图（340612×4 / 362607×4 / 362643×2）
> 深读时间：2026-10（Tier A #34）

## 0. 一句话重述：这道题真正在考什么

题面是"颈椎 CT 逐椎骨 C1–C7 骨折二分类 + patient_overall"，实际被考的是**用极少分割掩码撬动大量粗标签的标签工程**：

1. **数据结构**：2019+ 例 study 只有"哪些椎骨骨折"的 study 级标签；仅 **87 例**有 3D 分割掩码；8 个预测列（C1–C7 + overall）。
2. **主骨架 = 三阶段标签传播**：① 在 87 例上训 3D/2D 分割（并伪标签全量 2k 例）→ ② 用掩码裁剪/可见性把 study 标签传播到切片或椎骨级，训练逐椎骨分类 → ③ 序列模型聚合成 8 列，并专门建模 patient_overall。四强全部如此。
3. **骨折 bbox 标签被全员弃用**：3rd 明说不用 fracture bounding boxes，只用分割的框与体积比——中间监督选择"覆盖广、可伪标"的分割，而非"语义最贴近"的骨折框。
4. **3D vs 2.5D 的实证分歧**：1st 在椎骨 cube 上训 3D CNN 失败 → 2.5D CNN+LSTM；6th 用 X3D-L（64×288×288，z-stride=1）成功。成败在**采样设计**（是否保 z 分辨率），不在"3D 行不行"。

一句话：**这是一场标签工程比赛**——分割、可见性、体积比都是为"把 8 列标签拆到可训练的粒度"服务的；模型差异其次。

## 1. 材料与角色

| 帖子 | 作者 | 票数 | 角色与独有信息 |
| --- | --- | --- | --- |
| [362607](https://www.kaggle.com/competitions/rsna-2022-cervical-spine-fracture-detection/discussion/362607) 1st | haqishen | 222 | 128³ 3D 分割（r18d/effv2s+UNet，7ch）→ 全量 2k 掩码 → 裁 7 椎骨 ×15 切片（5ch+掩码=6ch）→ 2.5D CNN+LSTM；type1 逐椎骨 + type2 逐患者（7×15=105 图学 overall）；**3D CNN 失败**；提交 7.5h |
| [340612](https://www.kaggle.com/competitions/rsna-2022-cervical-spine-fracture-detection/discussion/340612) 数据详解 | — | 179 | DICOM z 轴=矢状位置；分割 nifti 需 `[:, ::-1, ::-1].transpose(2,1,0)`；unique 值→椎骨号（>7 为 Th 等）；提交 8 行结构；作者自纠"其实有矢状位可用" |
| [362787](https://www.kaggle.com/competitions/rsna-2022-cervical-spine-fracture-detection/discussion/362787) 1st code | haqishen | 147 | stage1/type1/type2/inference 全 notebook 公开（可复现性最强的来源） |
| [362643](https://www.kaggle.com/competitions/rsna-2022-cervical-spine-fracture-detection/discussion/362643) 3rd | darraghdog | 59 | **不用骨折 bbox**；只用分割的外接框 + 体积比；EffNetV2 预测框/have_bbox；study 级单框裁剪 512²；3 段模型（切片比→多任务序列→study 微调）；attention-over-RNN 增益大、Transformer 无效；10 权重集成；推理 4.5h |
| [362651](https://www.kaggle.com/competitions/rsna-2022-cervical-spine-fracture-detection/discussion/362651) 6th | i-pan | 59 | 3D DeepLabV3+ X3D 192³（伪标全量）；X3D-L 64×288×288（**z-stride=1**）→ 432D → 7×432；TD-CNN（2D+Transformer）用 class activation sequence 伪标 → 256D；三段 Transformer 融合（CV 0.3205/0.3369/0.2962，权重 0.25/0.25/0.5） |
| [363232](https://www.kaggle.com/competitions/rsna-2022-cervical-spine-fracture-detection/discussion/363232) 5th | Speedrun | 51 | **11 天速通**；2D 可见性（EffNet-B5）+ 2D 分割（EffNet-B3-UNet）→ 伪标全量 + 0.05/0.95 分位框；stage2 2.5D+3D 混合（(3,3,H,W)）；stage3 FFN 直接用竞赛指标优化 mean/min/max；30-70 融合 **+2–3 LB** |

**材料缺口（受"不扩采"约束，登记备查）**：2nd(365115,41 票,"Segmentation + 2.5D CNN + GRU Attention")、4th(364837,34 票,"CSN is all you need for 3D")、8th(362669,45)、32nd(362593,43)、metric weights(340392,65)、3D renderings(350244,85)、anatomy(340439,36)、vertebrae detection(348241,36) 等未收录正文。**4th 标题与 1st 的"3D 失败"直接构成张力**（见 §8）。

## 2. 逐方案对照矩阵

| 维度 | 1st haqishen | 3rd darraghdog | 5th Speedrun | 6th i-pan |
| --- | --- | --- | --- | --- |
| 分割/定位 | 3D 语义分割 128³，r18d / effv2s + UNet，7ch；预测全量掩码 | EffNetV2 回归外接框 + have_bbox；study 级单框裁剪 512²（z 轴 rollmean） | 2D 可见性分类 + 2D 分割（87 例）；0.05/0.95 分位聚合 study 框 | 3D DeepLabV3+（X3D）192³；伪标全量 |
| 标签传播 | 掩码裁 7 椎骨 → 每椎骨单二值标签（2k×7=14k 样本） | 体积比回归（切片/最大体积）→ 乘 study 骨折标签得切片级标签 | 可见性×overall → 2D 切片伪标签 | CAS（分类激活序列）→ 切片伪标签；分割伪标 |
| 序列输入 | 每椎骨 15 切片均匀采样；每片 5ch（中心±2）+ 掩码=6ch | 32×3 切片窗口；study 单框；长序列压缩到 192×3 | 2.5D（3ch）+ 间隔帧 ±5 → (3,3,H,W) | 每椎骨 64 深 ×288×288；study=7 序列 |
| 逐椎骨/切片模型 | 2D CNN（effv2s/convnext-tiny）+ LSTM（type1） | 2.5D CNN+1D RNN（resnest50d/seresnext50）+ attention | 2.5D+3D 混合轻量 effv2 | X3D-L（z-stride=1）+ TD-CNN |
| patient_overall | type2：7×15=105 图联合输入（convnext nano/pico/tiny、nfnet-l0） | model3 study 级微调，直接用竞赛指标损失 | **stage3 FFN**（mean/min/max 输入，直接优化竞赛指标） | 3 段 Transformer：7×432 / 7×256 / 7×688 融合（0.25/0.25/0.5） |
| 集成 | 分割 2 系 ×5 折 + type1 2 系 + type2 4 系 | 10 权重（resnest50d×6 + seresnext50×4） | 30–70（stage2 max 聚合 vs stage3） | 三路输出加权 |
| 训练/推理成本 | 提交 7.5h | ~9h/折；推理 4.5h | 11 天完成全流程 | 2D 预训 288² → 冻结微调 → 端到端 32×288×288 |
| 失败清单 | 椎骨 cube 上的 3D CNN | Transformer、undersampling、骨折 bbox（弃用） | —（速通无消融） | mask 当通道、遮非分割区、切片级特征+2D CNN |

## 3. 共识、分歧与裁决

### 共识一：三阶段骨架（分割/定位 → 椎骨/切片分类 → study 聚合）4/4

1st：3D 分割→椎骨裁剪→type1/type2；3rd：框→切片标签→model1/2/3；5th：可见性+分割→切片伪标签→聚合 FFN；6th：分割→3D CNN 特征→TD-CNN/Transformer。

**裁决**：8 列逐椎骨标签 + study 级粗标签的结构，要求显式引入"椎骨身份"作为中间变量；任何端到端 study 分类都缺归因路径。置信度：高（4 队结构一致 + 1st/3rd 明确失败例）。

### 共识二：骨折 bbox 弃用、分割优先（3rd 明说，4/4 实际未用）

3rd："I did not use the fracture bounding boxes, and only used high level data from the segmentation maps"；
1st/6th：用分割掩码裁剪/通道/伪标；5th：用分割框 ROI。

**裁决**：中间监督的选择标准是"覆盖面 × 可伪标性"而非"语义贴近度"——分割只有 87 例却可通过伪标签覆盖 2k 例，且提供形状先验；骨折 bbox 覆盖与质量不足以支撑全量训练。置信度：中高（四队一致，但 3rd 外无直接消融）。

### 共识三：patient_overall 必须专门建模（4/4 结构差异，方向一致）

1st：type2 把 7 椎骨×15 切片联合输入（105 图）学 overall；5th：stage3 FFN 直接优化竞赛指标（+2–3 LB）；6th：Transformer 输出 8 列；3rd：model3 用竞赛指标损失微调。

**裁决**：overall 不是 C1–C7 的 max/any 的简单函数（列 log-loss 需要校准的联合概率）；需要专门的聚合模型与损失。置信度：高（5th 有量化增益）。

### 共识四：伪标签把 87 例扩到全量（3/4 明说）

1st：预测全部 2k 掩码；5th：threshold 0.5 可见性 × overall；6th：分割伪标 + CAS 伪标（明确不用官方 image-level 标签）。

**裁决**：小标注子集 → 全量的伪标签扩张是标准操作；关键是伪标来源模型要足够干净（1st："87 例足够训练出好分割"）。置信度：高。

### 分歧一：3D CNN vs 2.5D+RNN（本场最大实证分歧）

1st：在椎骨 cube 上训 3D CNN"did not give satisfactory results" → 退回 2.5D（5ch 切片）+LSTM；
6th：X3D-L 3D CNN 直接成功（64 深 ×288×288，**z-stride 全部改为 1**）；
4th（未收录正文）：标题"CSN is all you need for 3D"；
3rd：2.5D+1D RNN + attention；5th：2.5D+3D 混合（近邻 3 帧 + ±5 间隔帧）。

**裁决**：这不是"3D 行不行"的问题，而是**采样设计**：6th 保 z 分辨率（stride=1）+ 高 xy 分辨率 + 64 深度；1st 的失败配置是小 cube 3D CNN。5th 的混合结构（不同 z 间距的多帧堆叠）是折中解。置信度：中（各队单点经验，但方向可解释）。

### 分歧二：序列模型——RNN/attention vs Transformer

3rd：attention 加在 RNN 输出上"helped a lot"，Transformer 无效；
1st：LSTM；
6th：study 级用 3 层 Transformer（三路融合，CV 0.2962 最佳）；
5th：stage3 FFN。

**裁决**：层级不同——切片/椎骨级序列（几十步、强局部性）用 RNN+attention；study 级 7 步序列（椎骨间关系）用 Transformer 有效。把两处结论互斥是"层级混淆"。置信度：中。

## 4. 增量数字账

| 动作 | 数字 | 来源 |
| --- | --- | --- |
| 数据规模 | 2019+ studies（2k）；**仅 87 例**有 3D 分割；8 个预测列 | 数据帖/1st |
| 1st 样本扩张 | 2k × 7 = **14k** 椎骨样本；每椎骨 15 切片 ×5ch + 掩码通道 | 1st |
| 1st 分割 | 128³；resnet18d + effv2s，各 5 折；7ch 输出 | 1st |
| 1st 分类 | type1：effv2s(512²) 5 折、convnext-tiny(384²) 5 折；type2：convnext-nano(512²) 5 折、pico/tiny/nfnet-l0 各 2 折 | 1st |
| 1st 提交耗时 | **7.5 小时** | 1st |
| 3rd 传播 | ratio = 切片椎骨体积 / 该椎骨最大体积；× study 骨折标签 → 切片级标签 | 3rd |
| 3rd 训练 | 窗口 32×3；batch 48（accum 16）；~9h/折；长 study 压缩至 192×3 | 3rd |
| 3rd 集成/推理 | resnest50d×6 + seresnext50×4 权重；推理 **4.5h** | 3rd |
| 3rd 失败配置 | Transformer 无效（attention-over-RNN 有效）；undersampling 无效 | 3rd |
| 5th 速通 | 全流程 **11 天**；stage2 输入 (3,3,H,W)；推理放大 ≥1.125 + center crop | 5th |
| 5th stage3 增益 | 30-70 融合（stage2 max 聚合 vs stage3）→ **+2–3 LB** | 5th |
| 6th 伪标链 | (64,288,288) → (432,64,9,9) → (64,9,9) → (64,) → 原始切片数；阈值 0.5 | 6th |
| 6th CV | 3D CNN 7×432：0.3205；TD-CNN 7×256：0.3369；融合 7×688：**0.2962**；权重 0.25/0.25/0.5 | 6th |
| 6th 训练 | 分割 192³；3D 分类 64×288×288（z-stride=1）；2D 预训 288²；端到端 32×288×288 | 6th |

**结构校验（2 处吻合）**

1. 1st type2：7×15=105 图/study ✓（图上标注 "105 x 512"）；
2. 6th CAS 维度链 64→432 通道→9×9→1 序列→原始切片数，与 (64,288,288) 输入、最终 pooling 后 9×9 的空间大小自洽 ✓。

## 5. 机制推演

**M1｜为什么 87 例掩码足够**：3D 分割是"高对比度、强形状先验"的任务（颈椎在 CT 中亮且结构规则），87 例可让 7 类分割收敛；而骨折分类是"细微纹理+不平衡"的任务，需要大量样本。分割+伪标签把"稀缺的像素监督"转成"充裕的定位监督"，再用它给 2k 例的粗标签做归因。

**M2｜标签传播的误差结构**：study 标签是"哪些椎骨骨折"（多标签），切片级标签=椎骨可见性 × study 标签（3rd/5th）。传播误差来自：① 可见性/ratio 模型误差 → 标签噪声；② study 级标签本身可能漏报。因此 1st 用预测掩码当第 6 通道（让分类器看到"这块是否属于目标椎骨"），3rd 用 RMSE 回归 ratio（比硬阈值柔和平滑）——两者都在抑制传播噪声。

**M3｜patient_overall 为什么不能用 max**：log-loss 需要逐列校准概率；max(C1..C7) 会系统性高估 overall 的置信度（max 分布的方差被高估），且忽略"多椎骨骨折"的联合信息。5th 的 stage3 在 (mean, min, max) 上用竞赛指标直接训练，把聚合校准交给模型（+2–3 LB）；1st 的 type2 通过 105 图联合输入学习椎骨间关系。

**M4｜3D 成败的采样学**：3D CNN 的表达力依赖 z 方向的感受野与分辨率。6th 把 z-stride 全设为 1（不降采样 z），输入 64 深 ×288×288，保留大量 z 细节；1st 的 128³ cube 来自分割裁剪（z 覆盖整个椎骨，但每层信息被压缩）。当 z 分辨率被破坏时，3D 卷积的相对优势消失、显存成本反噬 → 退回 2.5D。5th 的"3 近邻帧 + ±5 间隔帧"混合堆叠是第三种采样设计（多尺度 z）。

**M5｜中间监督的选择函数**：可用的中间标签有三类——分割掩码（87 例）、骨折 bbox（覆盖/质量不明）、study 标签（全量）。理性选择 = argmax(覆盖率 × 可伪标性 × 与目标相关性)。分割在 87 例上可训练→可全量伪标，胜出；bbox 语义虽近，但无法支撑全量训练，被弃用（3rd 明示）。这一"选择函数"可迁移到所有"粗标签+小掩码"的医学赛。

**M6｜速通的复用机制**：5th 用 11 天冲到第 5，依赖往届 RSNA 的模块化积累——2D 分割（segmentation models pytorch）+ 2.5D/3D 堆叠 + stage3 metric 优化 + 集成模板；3rd 同样引用两年前冠军 wowfattie 的 2.5D+RNN 骨架。**同类系列赛的方法复用是速通的核心竞争力**。

## 6. 证据分级

| 断言 | 等级 | 说明 |
| --- | --- | --- |
| 1st 全结构（分割/type1/type2） | **自述 + 全 notebook 公开** | 高（可复现） |
| 3rd 三模型 + 10 权重集成 | 自述 + 代码 + slides + 视频 | 中高 |
| 5th stage3 +2–3 LB | 自述 + 视频/代码 | 中高 |
| 6th 三路 CV（0.3205/0.3369/0.2962） | 自述 + 代码 | 中高 |
| "3D CNN 失败"（1st） | 单队经验（配置依赖） | 低-中（与 6th/4th 冲突） |
| attention 有效 / Transformer 无效（3rd） | 单队经验 | 低-中（层级混淆） |
| 数据帖的转置/翻转公式 | 社区验证 + 官方引文 | 中高 |
| 骨折 bbox 弃用 | 四队行为一致，3rd 明示 | 中（无消融） |

## 7. 边界条件与反事实

- **反事实 1**：若没有 87 例分割 → 无法裁剪/传播，整条流水线不成立；本场可行性建立在该子集上（也解释了为什么"分割质量"是全场最上游的杠杆）。
- **反事实 2**：若直接用 study 多标签训练整卷 CT → 8 列标签无法归因到位置；四队均未尝试端到端（1st/3rd 失败清单方向一致）。
- **反事实 3**：若 patient_overall 用 max 导出 → 5th 的 stage3 增益（+2–3 LB）表明校准/联合建模有实质空间。
- **反事实 4**：若用骨折 bbox 监督定位 → 3rd 明确不用；无消融数字，但四队行为一致。
- **边界**：结论适用于"逐结构多标签 + 小掩码子集"的医学赛；纯患者级标签、无定位需求的任务不需要三阶段。

## 8. 悬案与失败学

**悬案**

1. **4th "CSN is all you need for 3D"（364837）未收录**：与 1st"3D CNN 失败"直接冲突，是本场最重要的待裁决张力（3D 采样设计的又一个数据点）。
2. **2nd "Segmentation + 2.5D CNN + GRU Attention"（365115）未收录**：与本次四强的序列模型变体对照缺失。
3. metric weights 帖（340392，65 票）未收录：加权列 log-loss 的权重细节直接影响所有校准决策（3rd/5th 的损失设计）。
4. 8th/32nd 未收录；3D renderings/vertebrae detection 等工具帖未收录。

**失败学（跨队合集）**

- 模型类：椎骨 cube 上的 3D CNN（1st）；Transformer 替代 RNN（3rd）；切片级特征 + 2D CNN（6th）。
- 数据类：mask 当额外通道（6th 列为无效——与 1st 用 mask 通道有效相反，说明配置依赖）；遮掉非分割区（6th）；undersampling（3rd）；骨折 bbox（全员弃用）。
- 组织类：速通依赖复用；无复用则 11 天不可行。

## 9. 图表证据

> 路径相对本文件（`analysis/deep/`）：`../../intel/rsna-2022-cervical-spine-fracture-detection/bodies/<topic>_img/NN.png`

**图 1：1st 的 3D 分割预测示例（raw CT vs 7 类掩码）**（topic 362607）——`../../intel/rsna-2022-cervical-spine-fracture-detection/bodies/362607_img/01.png`

*读图结论*：上排 x/y/z 三视角原始 CT，下排 C1–C7 分割掩码（彩色)。**87 例训练出的 3D UNet 已能稳定分离 7 节椎骨**——这是"87 例足够"的直接图证，也是整条标签传播链的源头。

**图 2：1st 的 type1 模型（逐椎骨）**（topic 362607）——`../../intel/rsna-2022-cervical-spine-fracture-detection/bodies/362607_img/03.png`

*读图结论*：15 切片（每片 5ch+掩码）→ 2D CNN → 15×512 特征 → LSTM → 逐椎骨骨折概率。**"2D 骨干共享 + 序列头聚合"的 2.5D 范式**（3rd/6th 的同构变体）。

**图 3：1st 的 type2 模型（逐患者 overall）**（topic 362607）——`../../intel/rsna-2022-cervical-spine-fracture-detection/bodies/362607_img/04.png`

*读图结论*：7×15=105 图（图上 "105 x 512"）联合输入 2D CNN → 105×512 → LSTM → 输出 8 列（含 overall）。**用联合输入学椎骨间关系与 overall**；代价是显存只能用小 backbone。

**图 4：3rd 的 study 级裁剪（原始轴位 → 椎骨放大）**（topic 362643）——`../../intel/rsna-2022-cervical-spine-fracture-detection/bodies/362643_img/01.png`

*读图结论*：左=原始轴位 CT，右=按 study 级外接框裁剪并放大后的椎骨。**"单框裁剪整卷 + 放大"把分辨率留给椎骨细节**（3rd 用 512²，1st 用掩码通道，5th 用分位框）。

**图 5：3rd 的标签传播（切片级椎骨比 → 切片级骨折标签）**（topic 362643）——`../../intel/rsna-2022-cervical-spine-fracture-detection/bodies/362643_img/02.png`

*读图结论*：左图 C1–C7 的逐切片体积比曲线（模型 1 回归目标）；右图 = 比值 × study 骨折标签 → 切片级骨折概率（注意 C2 无骨折峰，被 study 标签过滤）。**标签传播的完整机制图**。

**图 6：颈椎解剖与 C1–C7 编号（数据帖）**（topic 340612）——`../../intel/rsna-2022-cervical-spine-fracture-detection/bodies/340612_img/04.png`

*读图结论*：C1–C7 与胸/腰/骶椎的分段着色；数据帖说明分割 unique 值 >7 属于 Th 区段（不参与训练，但常见于切片边缘）。**"椎骨编号=标签对齐"的领域基础**——定位错一节，8 列标签全部错位。

## 10. 对既有笔记/playbook 的修订点

1. `notes/cv/rsna-2022-cervical-spine-fracture-detection.md` 升级：补 6 篇作者/票数、四方案 × 8 维对照、数字账（14k 样本、0.2962、+2–3 LB、7.5h/4.5h/11 天）与 6 张图证。
2. `playbook/cv.md`（医学影像节）增补：
   - **粗标签 + 小掩码的标签工程三段式**：小掩码子集训分割 → 伪标签全量 → 用掩码/可见性把粗标签传播到结构级 → 序列模型聚合；
   - **中间监督选择函数**：覆盖率 × 可伪标性 × 相关性（分割胜骨折 bbox 的理由）；
   - **patient_overall/聚合列的专门建模**：metric-aware 后段（mean/min/max 输入，直接用竞赛损失）；
   - **3D vs 2.5D 的采样判据**：z-stride、z 分辨率、深度、xy 分辨率的组合决定 3D 是否可行；
   - **层级化的序列模型选型**：切片/结构级 RNN+attention；study 级 Transformer。
3. `playbook/00-通用方法论.md` 增补：**"用最少标注撬动最多监督"**（稀缺精确标签 → 全量伪标签 → 传播）；**"系列赛方法复用"**（Speedrun 11 天的基础设施清单）。
4. `analysis/THEORY.md`（Batch 4 收尾扩 v0.4）候选：
   - **L49｜粗标签传播三段式**：小掩码→伪标全量→结构级传播→序列聚合；证据 = 本场 4 队 + rsna-2024 的坐标传播（跨场同构）。
   - **T14｜3D 直训 vs 2.5D 序列（采样设计裁决）**：1st 失败 vs 6th 成功 vs 4th 标题；裁决变量 = z-stride/分辨率/深度。
   - **L50｜聚合列需专门校准**：patient_overall 不能用 max；证据 = 5th stage3 +2–3 LB、1st type2、6th 融合。

## 11. 出处

- 1st（haqishen，222 票）：https://www.kaggle.com/competitions/rsna-2022-cervical-spine-fracture-detection/discussion/362607
- 数据详解（179 票）：https://www.kaggle.com/competitions/rsna-2022-cervical-spine-fracture-detection/discussion/340612
- 1st code（147 票）：https://www.kaggle.com/competitions/rsna-2022-cervical-spine-fracture-detection/discussion/362787
- 3rd（darraghdog，59 票）：https://www.kaggle.com/competitions/rsna-2022-cervical-spine-fracture-detection/discussion/362643
- 6th（i-pan，59 票）：https://www.kaggle.com/competitions/rsna-2022-cervical-spine-fracture-detection/discussion/362651
- 5th Speedrun（51 票）：https://www.kaggle.com/competitions/rsna-2022-cervical-spine-fracture-detection/discussion/363232
- 缺口登记（未收录正文）：2nd(365115)、4th(364837)、8th(362669)、32nd(362593)、metric weights(340392)、3D renderings(350244)、anatomy(340439)、vertebrae detection(348241)
