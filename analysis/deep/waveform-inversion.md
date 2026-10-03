# Waveform Inversion 深读：正演模拟在环 × 非对齐输入表示 × 分家族专业化

> 赛事：Research ｜ science（地震全波形反演 FWI）｜ 1365 队 ｜ 标准赛 ｜ 指标：MAE（70×70 速度场，越低越好）
> 材料基础：`digests/waveform-inversion.md`（6 篇：1st/2nd/3rd/9th/20th + 数据讲解帖；80 条讨论索引）+ 13 张图（587388×8 / 587950×5）
> 深读时间：2026-10（Tier A #40，**Batch 4 收官**）

## 0. 一句话重述：这道题真正在考什么

题面是"由 5 源 × 1000 时步 × 70 接收器的地震波形反演 70×70 地下速度场"，实际被考的是**物理仿真器在环的工程能力 + 大算力**：

1. **输入与输出不空间对齐**：波形不是图像，速度图像素与波形不对应——U-Net 跳连的直觉失效。1st 把 (5,1000,70) 重排成 (1,350,350) 再喂 ViT，CV 从 46.9 直接降到 32.5；冠军方案是**无解码器的 ViT + 像素重排**（后升级为 encoder+decoder 双 ViT，共享 RoPE）。
2. **正演（forward modeling）是发动机**：四强全部让仿真器进环——数据增强（速度模型变换 → 重算地震）、自训练（预测 → 正演 → 回训，1st 的 Iterative Pseudo / 20th 的 in-batch 回路）、FWI 精修（2nd：DL 先验 28.8 → 物理反演 7.6）。9th 为此写自定义 CUDA 内核（**100× 加速**），1st 把正演从 10 张/分钟提到 **5000+ 张/分钟**。
3. **分家族/分难度专业化**：三大家族（Vel/Fault/Style）×A/B 复杂度；StyleB 的 MAE ~44 而 FlatVel 可 <0.1。1st 发现新增分数主要来自 4/10 个子集 → 去掉一半数据专训 **Top4 模型**（CV 7.5、LB 7.0）；2nd 为每个家族设计不同先验（1D TV / GP+SVD / 2D TV）。
4. **算力门槛**：1st 15 天 4×5090、3rd 13TB 存储 + 5.5 天 4×A100、2nd $700 云成本、9th 2 周极限冲刺——2nd 公开担忧"这样下去很少有人能竞争头部"。

一句话：**这是一场"物理引擎在环 + 算力换 MAE"的反演竞赛**——冠军用纯 ViT + 迭代伪标 + 物理增强打赢了显式 FWI 精修。

## 1. 材料与角色

| 帖子 | 作者 | 票数 | 角色与独有信息 |
| --- | --- | --- | --- |
| [587388](https://www.kaggle.com/competitions/waveform-inversion/discussion/587388) 1st | harshitsheoran | 194 | 无跨层跳连的 ViT 回归；输入重排 46.9→32.5；EVA02→DINOv2 ViT+RoPE（<26）；10× 速度模型增强（4.7M 样本）；**Iterative Pseudo**（每 epoch 预测→正演→回训）；Top4 子集模型；CV 7.28 / LB 6.9/6.9；15 天 4×5090 |
| [572747](https://www.kaggle.com/competitions/waveform-inversion/discussion/572747) 数据讲解 | tpmeli | 156 | 家族结构（Vel/Fault/Style × A/B）、文件配对、数据形状（(500,5,1000,70) vs (500,70,70)）、正演→反演的物理链条——**领域门槛破除的公共品** |
| [587419](https://www.kaggle.com/competitions/waveform-inversion/discussion/587419) 3rd | — | 60 | 13TB/5.5 天 4×A100；正演优化（float32、6 通道 hflip、PyTorch 批量、末行清零）；数据混合增强；ViT 分段（1/3 通道内 + pool + 2/3）；**Muon 优化器 9.x→7.x**；三阶段分辨率训练；赛后修正 last-row bug（7.96/7.99） |
| [587498](https://www.kaggle.com/competitions/waveform-inversion/discussion/587498) 9th | — | 59 | 2 周冲刺；**自定义 CUDA 批量波动传播（100×）**支持在线增强；flat LR 0.0005 复用训练；困难类加权 + 150 epoch 余弦；最后 10 checkpoints 中位；单次提交的极限风险管理 |
| [587950](https://www.kaggle.com/competitions/waveform-inversion/discussion/587950) 2nd | jeroencottaar | 49 | DL 先验（28.8）→ **正则化 FWI 精修（7.6）**；分家族先验（1D TV / GP+SVD 1073 模 / 2D TV）；BFGS+GN；custom CUDA 前向 30ms / 反向 70ms（V100 双精度）；$700 云成本 |
| [587402](https://www.kaggle.com/competitions/waveform-inversion/discussion/587402) 20th | — | 46 | **物理速度缩放增强**（速度×α ⇔ 时间轴×1/α）+ 测试端 α 中位；正演生成测试数据自训练（含 in-batch：vel→seis→vel2→MAE 回传）；10 类 record 深监督；CV 12 后与 LB 脱钩 |

**材料缺口（受"不扩采"约束，登记备查）**：4th(587500,42)、5th(587443,43)、6th(587460,45)、"All you need know about FWI"(572329,77)、"Tips to speed up training"(583896,66)、"A Better Way To Ensemble"(582801,51)、OpenFWI 数据集(572434,53)、"Beware of Bartley!"(583217,43)、HGNet-V2(578305,45) 等未收录——4–6 名的混合策略与外部数据合规争议是主要缺口。

## 2. 逐方案对照矩阵

| 维度 | 1st | 2nd | 3rd | 9th | 20th |
| --- | --- | --- | --- | --- | --- |
| 核心方法 | 纯 ViT 回归 + 自训练 | DL 先验 + FWI 精修 | ViT + 数据生成 | 复用 CaFormer/ConvNeXt + 在线增强 | CaFormer + 数据生成 |
| 正演用法 | 数据增强 + **Iterative Pseudo**（每 epoch） | 反演内环（梯度/CUDA） | 生成 6 通道/blend 数据 | **在线增强实时重算**（CUDA） | 增强 + 测试自训练（in-batch） |
| 输入表示 | (5,1000,70)→(1,350,350) 重排 | 同左（DL 先验输入） | (5,1000,70)→(5,250,280)→插值到 patch×N | (N,5,1000,70)→(N,1,1000,350) | 1 通道 1000×350 |
| 架构 | EVA02→DINOv2 ViT（+encoder/decoder 双 ViT 共享 RoPE） | DL 初值 + BFGS/GN | ViT 分段（前 1/3 通道内 + pool + 后 2/3） | caformer_b36 + convnextv2_huge | caformer + 线性深监督头（9×9 特征） |
| 物理增强 | FiveCrop + RandomAffine on 速度模型（10×） | —（FWI 本身就是物理） | 同族/跨族 velocity blending（α 0.3–0.7 ×8） | shift/scale/rotate + 强度平移 | 速度缩放 α∈[0.8,1.2]（时间轴物理变换） |
| 伪标签/自训练 | 迭代伪标（~95k/epoch） | —（FWI 替代） | — | 检查点中位数 | 测试自训练（含回路反向传播） |
| 优化/训练 | AdamW + cosine；MAE 损失，sigmoid 映射到 (1500,4500) | BFGS/GN + 先验项 | **MuonWithAuxAdam**（9.x→7.x）；三阶段 | flat LR 0.0005 + 150 epoch 余弦 | AdamW（未展开） |
| 集成/提交 | 单模型 + Top4 专门模型；CV 7.28 | 单套 FWI 管线 | 三阶段 20/30/50 blend；clip+round | 6 模型中位；单提交 | 单模型 + TTA（α 中位） |
| 开销 | 15 天 4×5090 | ~$700 云 | 13TB / 5.5 天 4×A100 | 2 周（含 CUDA 开发） | — |
| 成绩（CV/LB） | CV 7.28；公/私 6.9/6.9 | DL 28.8→7.6 | 公/私 7.96/7.99（修正后） | 单提交金区 | — |
| 失败清单 | SSL、标准增强、UNet/UperNet/Mask2Former/适配器、复杂头、diffusion 造速度 | VAE 先验、预条件、StyleB 高频 | OpenFWI 末行不一致（训练清零） | 未早早发现"每 2 像素预测"、仅 3/8 折 | CV-LB 脱钩、MoE 路由、频域/位置数据训不动 |

## 3. 共识、分歧与裁决

### 共识一：这不是图像分割——输入要重排，跳连无意义（1st 有直接对照，全员同向）

1st：把输入从 (5,1000,70) 重排/缩放到 (1,350,350)，CV **46.9→32.5**；明确"U-Net 对我没意义，因为速度图像素与输入不空间对齐"；
3rd/9th/20th：同样把 5 个源"并排"成单通道 2D 输入（1000×350）；
2nd：DL 模型同样基于重排输入，但只当 FWI 的初值。

**裁决**：当输入与输出无空间对应关系时，**编码器-解码器跳连（UNet）没有物理意义**；把多通道时间序列铺成 2D 网格 + ViT/CNN 回归才是自然解。置信度：高（1st 的定量对照 + 全员行为一致）。

### 共识二：正演模型必须进环，且越快越好（5/5）

1st：增强 + 每 epoch 迭代伪标（正演速度 10→5000+ img/min）；
2nd：FWI 内环（前向 30ms/反向 70ms，custom CUDA）；
3rd：批量数据生成（float32、6 通道、PyTorch GPU）；
9th：**自定义 CUDA 内核 100×** 让在线增强可行；
20th：增强 + in-batch 自训练回路。

**裁决**：在已知（可仿真）的物理生成过程下，"仿真器在环"同时充当数据增强器、自监督信号与先验约束；**仿真速度是本场的隐形主变量**（谁能让环转得动，谁的方法上限就高）。置信度：高。

### 共识三：分家族/分难度处理是必需（4/4 用到不同形式）

1st：Top4 子集专门模型（去掉一半数据，CV 7.5）；
2nd：逐家族先验（FlatVel 1D TV <0.1；StyleA GP 3.4；StyleB 44.4；其余 2D TV 4.9）；
9th：先只在最难的 CurveFault_B 上训练与评测；
20th：10 类 record 深监督 + 困难类加权。

**裁决**：家族间难度差 2 个数量级；混合训练会被简单家族主导。**数据配比/专业化是多家族反演的第一杠杆**（与 cmi/rsna 等"结构异质"场次要领一致）。置信度：高。

### 共识四：算力是硬门槛，风险管理是核心技能（多队自述）

2nd：$700 云成本，公开担忧公平性与环境；3rd：13TB + 5.5 天 A100×4；1st：15 天 4×5090（并强调"没怎么集成"）；9th：因训练慢采用 flat LR 复用实验 + 检查点中位 + backup 提交。

**裁决**：此类物理仿真竞赛已进入"算力 + 工程效率"竞争阶段；可迁移的是**训练协议的可复用性设计**（flat LR、检查点中位、分阶段分辨率、只预测偶像素等），而非单点技巧。置信度：高（多队独立陈述）。

### 分歧一：纯 DL + 自训练（1st，6.9）vs DL + 显式 FWI 精修（2nd，7.6）

1st：不写 FWI，靠 ViT + 物理自训练与数据规模夺冠；
2nd：DL 初值 28.8 + 正则化 FWI → 7.6；在简单家族近乎完美（FlatVel <0.1），但 StyleB 无法捕捉高频（44.4）；
1st 的"未尝试想法"：用正演算梯度（∂seis/∂vel）作为新模型输入做 refinement——即**可微 FWI 头**。

**裁决**：两条路线在"让物理进环"上同源，差别在**显式优化还是隐式学习**；本场纯 DL 胜，但 FWI 在低维/干净家族优势明显。最优形态很可能是"DL 初值 + 轻量物理精修头"（双方都没来得及做全）。置信度：中。

### 分歧二：优化器——Muon 的异军突起

3rd：从 AdamW 换 MuonWithAuxAdam，**9.x→7.x**（自称多年未见的大增益），对除 patch embedding 外的 Linear 权重用 Muon；
1st/9th/20th：AdamW/SGD 为主。

**裁决**：Muon 在大型 ViT 的矩阵权重上有强证据（单队大增益 + 公开代码），但缺跨队复现；值得作为"高优先级对照实验"记录。置信度：中（单队、幅度大）。

### 分歧三：集成 vs 单模型

1st：基本不集成（单大模型 + Top4 专门模型），"可以继续训练到 sub 5"；
3rd：三阶段 blend；9th：检查点中位；20th：TTA 中位。

**裁决**：在"数据 + 自训练 + 长训练"到位时，单模型上限已经很高；集成更多用于弥补训练不足/资源受限。置信度：中高。

## 4. 增量数字账

| 动作 | 数字 | 来源 |
| --- | --- | --- |
| 数据规模 | 约 470k 训练样本；1st 用 440k 训练 / 30k 验证；增强后 **4.7M**（10×） | 1st |
| 输入重排对照 | (5,1000,70)→(5,350,70) CV 46.9；重排 (1,350,350) → CV **32.5** | 1st |
| 架构演进 | EVA02-small 无解码器 ~30 CV（40 epoch）→ encoder+decoder CV 28 → ViT+RoPE **<26** | 1st |
| 训练阶段 | 50 epoch MAE 19.19（欠拟合）→ 总 300+ epoch；最终预训练总 570 epoch | 1st |
| 分阶段分辨率 | 350→476→588→700；MAE 19.19→15.21→13.09→11.77 | 1st（图） |
| Iterative Pseudo | 每 epoch 对验证+测试 ~95k 样本预测 → 正演 → 回训；正演速度 10 img/min → **5000+ img/min** | 1st |
| Top4 专业化 | 仅用 CurveFault_B/CurveVel_B/Style_A/Style_B；模型 CV **7.5**、公/私 **7.0/7.0**；替换预测后最终 CV 7.28、公/私 6.9/6.9 | 1st |
| 2nd FWI | 先验 DL 28.8 → FWI **7.6**；分家族：FlatVel **<0.1**、StyleA 3.4、StyleB 44.4、其余 4.9；前向 30ms/反向 70ms（V100 双精度）；~$700 | 2nd |
| 3rd 数据/训练 | 13TB；5.5 天 4×A100 80G；6 通道 isx=[120,137,154,155,172,189]；blend α∈[0.3,0.7]×8 seed×2 类；Muon 9.x→7.x | 3rd |
| 3rd 阶段 | Stage1 10 epoch val 8.1 → Stage2 val 7.6 → Stage3 全量 1 epoch；blend 20/30/50；clip(1500,4500).round() | 3rd |
| 9th 加速 | CUDA 批量正演相对 CPU **100×**；150 epoch 余弦；最后 10 检查点中位；仅 3/8 折、~6 模型 | 9th |
| 20th 物理增强 | 速度 ×α ⇔ 时间轴 ×1/α；训练 α∈[0.8,1.2]；测试 10 个 α 取中位；in-batch 自训练每 6 批插入测试批 | 20th |
| 家族难度 | StyleB ≈44 vs FlatVel <0.1（相差 2 个数量级） | 2nd |
| 数据形状 | 地震 (500,5,1000,70)；速度 (500,70,70) | 数据帖 |

**结构校验（2 处吻合）**

1. 3rd 的输入 (5,1000,70)→(5,250,280)=70,000 像素 ✓（重排无损）；
2. 9th 的"CUDA 100×"与 1st 的 10→5000 img/min 是同一方向的独立证据（仿真速度决定方法上限）✓。

## 5. 机制推演

**M1｜为什么重排输入能涨 14 个 MAE**：ViT 的归纳偏置是 2D 邻域注意力；原始 (5,1000,70) 中"通道维"是震源、不是空间维，ViT 无法在其上建立有意义的邻接。把 5×1000 铺成 350×350 后，注意力能沿时间/接收器方向建模波形连续性与到时差——**输入表示决定了归纳偏置是否可用**。（同时明确输出与输入不对齐，故不为空间对齐设计解码器。）

**M2｜正演在环的三重身份**：① **增强器**：任意速度模型变换（裁剪/仿射/blend/缩放）都能生成配对的合成样本——相当于无限数据的物理数据增强；② **自监督信号**：预测→正演→与真波形比较，等价于在逆问题里加一致性约束（1st 的 Iterative Pseudo、20th 的 in-batch 回路）；③ **先验/精修**：FWI 用物理方程约束解空间（2nd）。三者共同把"病态逆问题"变成"受约束的学习问题"。

**M3｜物理等变增强 vs 图像增强**：速度×α 对应波场时间轴×1/α（20th），同族/跨族速度 blend 对应地质混合（3rd），FiveCrop/仿射对应空间局部性（1st）。这些增强都**保持前向物理的一致性**（变换后重算波形）；普通图像增强（翻转/裁剪波形本身）会破坏物理关系，因此 1st 明确"标准增强无效"（翻转需配合重算或对速度模型做）。

**M4｜家族混合的梯度支配**：StyleB 的误差量级 ~44 而 FlatVel <0.1；若按样本等权训练，简单家族的梯度占比高但已接近零误差 → 模型学不到 Style 的细节。1st 的"去掉一半数据"与 9th/20th 的困难类加权本质相同：**按家族难度重分配梯度预算**。1st 的 Top4 专门模型再叠加"专业化 + 集成切换"，把最难家族的预测替换为专训模型输出。

**M5｜病态逆问题的三段式**：FWI 目标非凸、多解；2nd 的结构 = **DL 给出靠近真解的初值**（28.8）→ **先验约束解空间**（TV/GP；StyleA 无噪声导致协方差病态 → SVD 截断到 1073 模态）→ **二阶优化收敛**（BFGS/GN + 平滑的可微 TV）。这对应"学习-正则化-优化"三件套，适用于一切病态反演。另：正演里的 min(v) 不可导 → 把最小速度解耦为独立自由度（2nd 的工程细节）。

**M6｜算力如何重塑方法学**：当一次完整训练需要数天多卡时，最优策略从"精细调参"转向"可复用协议"：9th 的 flat LR（随时续训/接新想法）、每 3 epoch 存预测取中位（对冲 checkpoint 噪声）、1st 的分阶段分辨率+预训练（把训练预算结构化）、3rd 的 stage 递减 epoch 数（10→1→1）。**资源受限下的方差控制**（单提交、backup 提交、只测偶像素）也是成绩的一部分。

## 6. 证据分级

| 断言 | 等级 | 说明 |
| --- | --- | --- |
| 输入重排 46.9→32.5 | **自述 + 架构图 + 代码** | 中高（单一数字但机制清晰） |
| 1st Iterative Pseudo/Top4 分数（7.28/6.9） | 自述 + 训练曲线图 + 代码 | 中高 |
| 2nd FWI 分家族分数与成本 | 自述 + 全代码 | 中高（成本无法审计） |
| 3rd Muon 9.x→7.x | 自述 + 代码 | 中（单队、幅度大） |
| 9th CUDA 100× | 自述 | 中 |
| 20th 物理增强/TTA/自训练 | 自述 | 中 |
| 家族难度 StyleB≈44 vs FlatVel<0.1 | 2nd 自述 | 中 |
| 数据形状/家族结构 | 数据帖（156 票）+ 官方文件可核 | 高 |

## 7. 边界条件与反事实

- **反事实 1**：若不重排输入 → CV 46.9（1st 对照），落后 ~14 MAE；输入表示是第一杠杆。
- **反事实 2**：若正演不可用/太慢 → 无法做增强与自训练，只能依赖官方 470k 样本（1st 的 4.7M 数据、20th 的测试自训练、9th 的在线增强全部消失）。
- **反事实 3**：若不分家族 → 简单家族主导梯度，StyleB 等困难家族无法改善（1st 的 Top4 与 2nd 的分先验是反证）。
- **反事实 4**：若纯 FWI 无 DL 初值 → 收敛困难/算力爆炸（2nd："FWI is much easier when you start close to the solution"）。
- **边界**：结论依赖"存在快速、可批量、可微的正演模型"；无仿真器的任务可以迁移"分家族专业化、可复用训练协议"，不能迁移"正演在环"。资源门槛（$700/13TB/多卡周级）对小规模参赛者是硬约束。

## 8. 悬案与失败学

**悬案**

1. **4th/5th/6th 方案（587500/587443/587460）未收录**——季军之后如何组织"物理 + 学习"的混合（尤其 FWI 精修与纯 DL 之间的第三条路）。
2. **OpenFWI/外部数据的合规争议**：讨论区有"Beware of Bartley!"(583217) 等高票帖未收录；使用官方未发布的 OpenFWI 与数据生成的边界不明。
3. 1st 的"梯度精修头"（正演梯度 + 预测速度 → refinement 模型）未实现；2nd 的 StyleB 高频捕捉失败——两端都指向"可微物理层"的未来方向。
4. 3rd 的 last-row/float32 与 OpenFWI 的差异来源（官方生成器细节）未完全澄清。
5. 20th 的 CV 在 12 后与 LB 脱钩的原因未解释（对比 1st 的 CV 7.28 与 LB 6.9 一致性较好）。

**失败学（跨队合集）**

- 表示/架构类：Unet 解码器、UperNet、Mask2Former、ViT-Adapter、复杂头（1st）；VAE 先验（2nd）；其他 backbone 不足训练（20th）；MoE 按数据集路由（20th）。
- 训练/增强类：MAE/MIM 自监督、标准图像增强、diffusion/启发式生成速度模型（1st）；预条件（2nd）。
- 资源/流程类：小 batch 下 Muon 开销（3rd）；单提交/单折风险（9th 自述）；训练集/推理不一致（3rd 的 last-row bug，修正后 7.96/7.99）——**提交前一致性检查**。
- 验证类：CV 与 LB 在高分区间脱钩（20th）→ 高分段的 CV 设计要按家族重估。

## 9. 图表证据

> 路径相对本文件（`analysis/deep/`）：`../../intel/waveform-inversion/bodies/<topic>_img/NN.png`

**图 1：正演易、反演难（任务示意）**（topic 587950）——`../../intel/waveform-inversion/bodies/587950_img/01.png`

*读图结论*：左侧速度剖面（70×70）经正演（Easy）得到右侧地震记录（时间×接收器），反演方向标注 Hard。**本场所有方法都围绕"让反演借用正演的物理信息"**（增强/自训练/FWI）。

**图 2：1st 的 ViT 回归结构（无 UNet 解码器）**（topic 587388）——`../../intel/waveform-inversion/bodies/587388_img/02.png`

*读图结论*：输入 (BS,1,H,W) → ViT → (BS,125.../n_patches,dim) → Linear(dim,patch²) → reshape/permute 回 (BS,H,W)。**像素重排（pixel shuffle）把 ViT 的 patch 表示直接还原成回归图像**——不需要跨层跳连，因为输入与输出不对齐。

**图 3：1st 的最终架构（encoder+decoder 双 ViT，共享 RoPE/Linear）**（topic 587388）——`../../intel/waveform-inversion/bodies/587388_img/04.png`

*读图结论*：编码 ViT → 共享 Linear → 像素重排 → 解码 ViT（接收重排后的图像）→ 共享 Linear → 双线性 resize 到 70×70 → MAE；两个 ViT 共享 RoPE 与 Linear。**"解码"在这里是对重建图像再做一轮 ViT，而非 UNet 上采样**。

**图 4：1st 的分阶段分辨率训练（350→700，MAE 19.19→11.77）**（topic 587388）——`../../intel/waveform-inversion/bodies/587388_img/06.png`

*读图结论*：每阶段"预训练（在 10× 增强数据上，2–5 epoch） + 主训练（50–60 epoch）"，图像尺寸逐步增大；MAE 19.19→15.21→13.09→11.77。**作者称 50 epoch 时严重欠拟合**——分辨率提升 + 继续训练是主要涨分手段。

**图 5：1st 的 Top4 专业化模型**（topic 587388）——`../../intel/waveform-inversion/bodies/587388_img/08.png`

*读图结论*：仅用 Top4 子集（CurveFault_B/CurveVel_B/Style_A/Style_B）训练，700×700、预训练 6 epoch；对应正文 CV 7.5、公/私 7.0/7.0，并在推理时替换主模型对这 4 类的预测。**"去掉一半数据反而涨分"的分家族专业化证据**。

**图 6：Style 家族的样貌（GP 先验的对象）**（topic 587950）——`../../intel/waveform-inversion/bodies/587950_img/03.png`

*读图结论*：StyleA 速度场是无层理的斑块/纹理结构（style transfer 生成）；2nd 用平方指数核高斯过程 + SVD 截断（1073 模态）作为其先验。**家族形态决定了先验选择**（FlatVel 用 1D TV、其余用 2D TV）。

## 10. 对既有笔记/playbook 的修订点

1. `notes/science/waveform-inversion.md` 升级（现为浅版）：补 6 篇作者/票数、五方案 × 10 维对照、数字账（46.9→32.5、28.8→7.6、Muon 9.x→7.x、100×、$700/13TB）与 6 张图证；新增"正演在环"与"分家族专业化"节。
2. `playbook/science.md`（逆问题/物理仿真节）增补：
   - **输入表示**：非空间对齐任务禁用 UNet 跳连直觉；多通道时间序列重排为 2D 网格 + ViT/像素重排回归；
   - **仿真器在环三用法**：物理增强（变换后重算波形）、自训练回路（预测→仿真→回训）、显式反演精修（DL 初值 + 先验 + 二阶）；
   - **物理等变增强**：速度缩放/几何变换 + 正演重算；
   - **分家族专业化**：按难度重分配梯度预算、专训难子集、家族先验（TV/GP）；
   - **可复用训练协议**（flat LR、检查点中位、分阶段分辨率）与资源风险管理。
3. `playbook/00-通用方法论.md` 增补：**"仿真器 = 增强器 + 自监督 + 先验"**；**"输入表示决定归纳偏置可用性"**；**"物理精修的三段式（初值-约束-收敛）"**。
4. `analysis/THEORY.md`（Batch 4 收尾扩 v0.4）候选：
   - **L66｜仿真器在环**：证据 = 本场 5/5 + 1st 的 10→5000 img/min；
   - **L67｜非对齐任务禁用跳连**：证据 = 1st 的 46.9→32.5；
   - **L68｜物理等变增强**：证据 = 20th 的速度缩放、3rd 的 blending；
   - **T18｜纯学习 vs 物理精修**：1st（6.9）vs 2nd（7.6，FlatVel<0.1）；裁决 = 互补，可微物理层是未来；
   - **T5 扩证**：物理先验在本场成为主方法（FWI vs 学习的融合）。

## 11. 出处

- 1st（harshitsheoran，194 票）：https://www.kaggle.com/competitions/waveform-inversion/discussion/587388
- 数据讲解（tpmeli，156 票）：https://www.kaggle.com/competitions/waveform-inversion/discussion/572747
- 3rd（60 票）：https://www.kaggle.com/competitions/waveform-inversion/discussion/587419
- 9th（59 票）：https://www.kaggle.com/competitions/waveform-inversion/discussion/587498
- 2nd（jeroencottaar，49 票）：https://www.kaggle.com/competitions/waveform-inversion/discussion/587950
- 20th（46 票）：https://www.kaggle.com/competitions/waveform-inversion/discussion/587402
- 缺口登记（未收录正文）：587500(4th)、587443(5th)、587460(6th)、572329、583896、582801、572434、583217、578305 等
