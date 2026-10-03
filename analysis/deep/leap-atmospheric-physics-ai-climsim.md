# LEAP ClimSim 深读：数据规模 × 鲁棒损失 × 1D 序列架构（附泄漏治理案例）

> 赛事：Research ｜ 主题 science（大气物理仿真回归）｜ 693 队 ｜ 标准赛 ｜ 指标：R²（368 个目标：6×60 序列 + 8 标量，越高越好）
> 材料基础：`digests/leap-atmospheric-physics-ai-climsim.md`（6 篇：4th/1st/2nd/10th + Two tips 109 票 + 泄漏治理请求 51 票；80 条讨论索引）+ 9 张图（523041×2 / 523055×5 / 523063×2）
> 深读时间：2026-10（Tier A #42）

## 0. 一句话重述：这道题真正在考什么

题面是"1D→1D 回归：由 60 层大气柱状态预测 368 个物理倾向/标量（加热倾向 ptend×6 + 8 标量）"，实际被考的是**数据规模、损失函数与数值保真**，并附带一场教科书级的**泄漏治理事件**：

1. **数据量是第一杠杆**：10th 的消融链显示 1/7 子样本 0.768 → +全量低分数据 0.781 → +伪标+高分数据 0.78620/0.78285；2nd 明确"用全部低分数据 +~0.01"；1st 用 HF 全量 + 高分数据（2:1 混合）。
2. **损失函数是第二杠杆**：1st 称 MAE"每一项都更好"（收敛快/更稳），是最接近"秘密"的技巧；2nd 用 SmoothL1 + 相邻层 diff 辅助损失；10th 用 Huber（>MSE）与 confidence-aware MSE。**在 R² 指标下，MSE 并不是最优训练损失**——数据含极端 outlier（讨论帖标题"max=2523σ"）。
3. **1D 序列架构 + 物理特征**：2nd 发现 LSTM 显著优于 CNN/MHSA/GRU，ResLSTM 单模型私榜最强；1st 用 Squeezeformer（12 块）+ 层级 reshape；4th 用 1D UNet（354M）；10th 的 Phalanx 用 PixelShuffle UNet + 堆叠，并提出**气候不变特征**（RH/羽流浮力/归一化热通量）对抗年际变暖漂移。
4. **数值细节决定生死**：数据为 float64（float32 会下溢——"Two tips"第一条）；1st 用 FP64 编码 → FP32 训练 → 预测后升回 FP64 再反归一化，并做两级 soft clipping。
5. **泄漏事件**：`pbuf_ozone_2` 可反推测试集时间戳/位置 → 衍生 2D→1D 模型与"用未来样本预测过去"；社区发帖请求主办方取消利用泄漏的方案；1st 未用泄漏并公开完整的可复现 pipeline 自证。

一句话：**这是一场"规模 + 损失 + 数值"的回归赛**，模型架构的边际收益远小于前两者；治理层面则是"泄漏识别—自证—裁决"的完整样本。

## 1. 材料与角色

| 帖子 | 作者 | 票数 | 角色与独有信息 |
| --- | --- | --- | --- |
| [523063](https://www.kaggle.com/competitions/leap-atmospheric-physics-ai-climsim/discussion/523063) 1st | — | 82 | Squeezeformer（12 块，256/384/512）；**MAE > MSE**；辅助时空损失（合规确认）；**confidence head**；masked loss；多种数据表示（特征维 1696）；高分数据 2:1；两级 soft clipping；ptend trick；13 模型集成 **0.79410/0.79123**；公开>100 notebook 全流程自证无泄漏 |
| [523055](https://www.kaggle.com/competitions/leap-atmospheric-physics-ai-climsim/discussion/523055) 2nd | 5 人团队 | 47 | 全量低分数据 +~0.01；SmoothL1 + **aux diff loss**（相邻层差分）+ cosine（第 3/9 epoch 衰减）；**group fine-tune**（368 目标分 7 组，各 1 epoch，+0.0005~0.0015）；LSTM 主导（>CNN/MHSA/GRU），LSTM+Mamba 提供集成多样性；hill-climb 权重（含负权重）；0.7955 CV / 0.79211 / 0.78856 |
| [523042](https://www.kaggle.com/competitions/leap-atmospheric-physics-ai-climsim/discussion/523042) 4th | 3 人团队 | 34 | 三路：Kurupical（1D ConvNeXt/Transformer ×7，CV 0.788、私榜 0.779–0.783、训练 16–132h）；Kami（1D UNet 354M、气候相关特征、Adan、EMA）；Takoi（LSTM×12、HF 数据）；共同后处理 ptend_q0002=state/(−1200)；**自认 batch 384 是 lat/lon 泄漏的遗留** |
| [523041](https://www.kaggle.com/competitions/leap-atmospheric-physics-ai-climsim/discussion/523041) 10th | Updraft 4 人 | 33 | 23 模型；**用 1−MSE 代替 R²**（主办换测试集后 R² 失去相关）；**气候不变特征**（子样本 +1%、全量私榜 +0.05%）；confidence-aware MSE（预测方差）；**hard-sample doping**（14% 难样本 + 邻近时间帧）；PixelShuffle 堆叠 UNet；tanh normalization；去 Dropout；per-target×model stacking |
| [506984](https://www.kaggle.com/competitions/leap-atmospheric-physics-ai-climsim/discussion/506984) Two tips | — | 109 | ① **不要转 float32**（下溢）；② 架构决定一切（CV 0.72+ 首 epoch、LB 0.766，无伪标/外部数据） |
| [519249](https://www.kaggle.com/competitions/leap-atmospheric-physics-ai-climsim/discussion/519249) 泄漏治理请求 | — | 51 | `pbuf_ozone_2` 泄漏 → 测试时间/位置可精确恢复 → 2D→1D 与未来数据利用；请求主办方取消基于泄漏的方案（正文为参赛者向主办方请求） |

**材料缺口（受"不扩采"约束，登记备查）**：**[Confirmation Request]: Availability of Reverse-engineered Timestamp & Location**（511911，76 票）、领域知识分享（508630，64）、"secret for beating baseline"（501829，46）、**"max=2523σ: How Extreme this Competition's Setup is"（506490，42）**、"Hack the Planet (Simulator)"（519184，34）、起步资源（494968，43）等未收录——**泄漏确认帖与极值分析是两大缺口**。

## 2. 逐方案对照矩阵

| 维度 | 1st | 2nd（5 人） | 4th（3 人） | 10th（4 人） |
| --- | --- | --- | --- | --- |
| 架构 | Squeezeformer×12（+GLUMlp 头） | ResLSTM / ConvLSTM / LSTM+Transformer / LSTM+Mamba | 1D ConvNeXt、1D Transformer、1D UNet(354M)、LSTM×12 | Conv-Transformer、PixelShuffle 堆叠 UNet、Transformer+CNN+LSTM |
| 损失 | **MAE** + confidence head（MAE）+ masked | **SmoothL1 + aux diff**（层级差分）+ cosine | SmoothL1（beta 调参） | **Huber / confidence-aware MSE** |
| 特征/表示 | 3 种归一化表示（1696 维）+ wind + 两级 soft clip | 原始+差分；标准归一化 | 差分、均值、湿度/冰晶等；气候相关特征 | **气候不变特征**（RH/浮力/热通量）+ 原始 |
| 数据 | LR 全量 + HR（2:1）+ 时空 aux | LR 全量（~75M）+ 分组微调 | LR、HR、伪标（各成员不同） | LR 1–7y / 1–8y、HR、伪标、难样本 doping |
| 验证 | 4 套（LR×2/HR/训练子集）；全量后与 LB 脱钩，按公榜防过拟合 | 8y 下半年 + 9y 1 月；与 LB 完美相关 | 按成员不同；1/6 子采样 | 1−MSE（std 归一化；eps 极小）；R² 换测试集后失相关 |
| 集成 | 13 模型（等权逻辑）0.79410/0.79123 | hill-climb 16 权重（含负）0.7955/0.79211/0.78856 | 3 成员模型合并 | stacking（per target×model）+ 手动权重；late submission 显示 type1 100% 私榜最好 |
| 数值 | FP64 编码→FP32→升 FP64 反归一化；两级 soft clip；目标 soft clip | — | — | tanh normalization、去 Dropout |
| 自证/合规 | 完整可复现 pipeline；未用泄漏 | — | 自认用 lat/lon 泄漏（batch 384） | — |

## 3. 共识、分歧与裁决

### 共识一：数据规模是第一杠杆（1st/2nd/10th 各自量化）

2nd："Utilizing the entire low-resolution dataset can boost performance by almost 0.01"；
10th：1/7 子样本 0.768 → 全量 0.781（+0.013）→ +伪标/HR 0.78620；
1st：LR 全量 + HR（2:1）→ 0.79410/0.79123（低分数据单系 0.79299）。

**裁决**：在 70M 行级仿真数据上，**把数据用满（并叠加 HR）比任何架构/调参都值钱**；"Two tips"帖的 0.766 与头部的 0.79 差距主要不在架构。置信度：高（三队独立数字）。

### 共识二：R² 指标下应使用鲁棒回归损失（MAE/SmoothL1/Huber），而非 MSE（1st 最强表态 + 2nd/10th 同向）

1st：MAE "better than MSE in every way"，为全场"秘密"之一（无 MAE 的消融未给数字，但语气极强）；
2nd：SmoothL1 + 层级 diff 辅助损失；
10th：Huber > MSE；confidence-aware MSE；难样本 doping 有效（14%）。

**裁决**：本场数据含极端 outlier（讨论帖提到 2523σ 级别），MSE 让少数极端样本主导梯度；MAE/SmoothL1 线性/有界梯度更稳。**指标（R²）与训练损失可以不一致**——训练损失的选择要看误差分布，而非指标代数形式。置信度：高。

### 共识三：层级（60 层）要作为序列维度显式建模，并注入物理/位置信息

2nd：ResLSTM 私榜最佳、LSTM 家族全面优于 CNN/GRU/MHSA；
1st：把输入 reshape 回 [60, 44] 再进 Squeezeformer，位置编码/层级结构有效；
4th：1D 序列模型 + 显式"高度关系"；
10th：位置嵌入 + Transformer/CNN/LSTM 组合。

**裁决**：这是 1D 序列回归，层间相邻关系是核心结构；任何"把 60 层打平当特征"的做法都次优。置信度：高。

### 共识四：数值保真与极端值处理是隐形门槛（Two tips + 1st）

Two tips：**float32 下溢**（必须保 float64）；
1st：FP64→FP32→FP64 的双向转换、两级 soft clipping、目标 soft clipping、反归一化顺序；
10th：tanh normalization 防梯度爆炸。

**裁决**：在特征/目标动态范围跨数个数量级的回归赛里，**数值管道是"0 分或高分"级别的工程**；先复现"训练不炸"，再谈技巧。置信度：高。

### 分歧一（治理）：泄漏的利用与裁决

事实：`pbuf_ozone_2` 可反推测试时间戳/位置（511911 确认帖 76 票；519249 请求帖 51 票）；
4th 自认 batch size 是 lat/lon 泄漏的遗留（部分利用）；
1st 明确未用，并用完整可复现 pipeline 自证（>100 notebooks）；
另有"用未来样本预测过去"的变体（利用时间序）。

**裁决**：该泄漏把 1D→1D 任务偷换成 2D/时序任务，违背主办设定；治理结果未收录，但**学习价值明确**：识别泄漏 → 主动不使用 → 公开可复现自证，是顶级选手的可信度策略（对照 T11/T17）。置信度：高（事实层面）。

### 分歧二：置信度/方差头的价值

1st：confidence head（预测每目标误差）让最佳单模型 0.79159/0.78869（无头 0.78945/0.78631），并可筛选样本（丢 10% 低置信 → R² ~0.83）；
10th：confidence-aware MSE（模型同时输出方差）带来稳定性；
2nd/4th：未提类似设计。

**裁决**：异方差式多任务（预测均值+方差）在回归里既是正则，也产出可用于**主动学习/样本路由**的副产品（低置信样本送回模拟器）；成本低，值得默认尝试。置信度：中高（1st 有对照数字）。

### 分歧三：集成权重与榜单选择

2nd：hill-climb 权重（含负权重，去相关）；
10th：per-target×model stacking；但 late submission 显示"type1 100% 权重私榜最好"（0.78536 vs 混合 0.78503）；
1st：13 模型、等权逻辑、承认轻微公榜过拟合。

**裁决**：大集成有效；但**权重搜索在公榜上进行会过拟合**——私榜最优往往更简单（10th 的 late submission 证据）。置信度：中高。

## 4. 增量数字账

| 动作 | 数字 | 来源 |
| --- | --- | --- |
| 1st 集成 | 13 模型 0.79410/0.79123；最佳单模（含 confidence）0.79159/0.78869；无 confidence 0.78945/0.78631；仅 LR 5 模型 0.79299/0.78951；无时空 aux 6 模型 0.79355/0.79092 | 1st |
| 1st 结构 | 特征维：9×60×3 + 60 + 16 = **1696**；HR:LR = 1:2；MAE + confidence MAE + masked；AdamW lr 1e-3、wd=4×lr、half-cosine | 1st |
| 1st 置信度筛选 | 丢弃最低置信 ~10% → R² **~0.83**（单模型） | 1st（图） |
| 1st 成本 | Colab TPU+Kaggle，~$200–300 | 1st |
| 2nd 数据/损失 | 全量 LR +~0.01；SmoothL1 + aux diff；cosine 第 3/9 epoch 衰减；group fine-tune +0.0005~0.0015 | 2nd |
| 2nd 最终 | CV 0.7955 / 公榜 0.79211 / 私榜 0.78856（16 权重，含负权重 −0.09~−0.05） | 2nd |
| 4th 模型群 | ConvNeXt 1D：CV 0.7881–0.7887、私榜 0.7790–0.7828、训练 16–132h（1×4090 或 8×4090）；UNet 354M CV 0.783；batch 384=泄漏遗留 | 4th |
| 10th 消融链 | 1/7 子样本 0.768 → +EMA 0.770 → +全量 LR 0.781 → +drop path 0.782 → +expert 0.7825 → +集成 0.783 → +伪标+HR 0.78620/0.78285 → +val 0.78624/0.78288 | 10th（图） |
| 10th 气候不变特征 | 单模型 0.78231/0.78025/0.77721 → 0.78434/0.7814/0.78017；集成 0.79218/0.78771/0.78618 | 10th |
| 10th 其他 | 难样本 doping 14%；PixelShuffle 替 ConvTranspose +0.x%；tanh normalization；23 模型 | 10th |
| Two tips | CV 0.72+ 首 epoch、LB 0.766；**禁用 float32** | 506984 |
| 泄漏事实 | pbuf_ozone_2 → 测试时间戳/位置可精确恢复 | 511911/519249（标题级） |

**结构校验（2 处吻合）**

1. 1st 的特征维公式 9×60×3+60+16=1696 与其 summary 图一致 ✓；
2. 10th 的消融链每一步单变量递增（数据→EMA→模型→伪标/HR），与其"数据规模优先"的结论自洽 ✓。

## 5. 机制推演

**M1｜为什么 MAE 在 R² 指标下反而更好**：R² 对整体方差解释度敏感，但本场误差由少数极端样本主导（标题级证据"2523σ"）。MSE 给这些样本平方级权重 → 梯度被少数点绑架、训练不稳；MAE 对有界/异常样本线性衰减 → 更接近"对大多数样本负责"。10th 的 hard-sample doping 与 confidence-aware MSE 是同一洞察的不同实现（控制难样本的影响方式）。

**M2｜年际漂移与气候不变特征**：ClimSim 覆盖 1–9 年模拟，全球变暖使输入分布随年份漂移；模型若把"年份温度水平"当信号会学到伪关系（本地好、跨年差）。气候不变特征（相对湿度、羽流浮力、归一化热通量）是**在冷暖条件下都不变的物理量**，把输入映射到时间稳定空间；10th 的 +1% 子样本 / +0.05% 全量私榜增益即其价值。1st 的时空 aux loss 是另一条路（显式给模型时间/位置信息），且被证明"去掉也能赢"。

**M3｜confidence head 的统计学本质**：同时预测目标与它的误差，等价于异方差回归（NLL：err²/var + log var）的近似；方差项自动调低极难样本的权重，均值头因此更稳。副产品是低置信样本识别——1st 的曲线显示，丢弃 10% 低置信样本后 R² 从 ~0.8 升到 ~0.83，并且他提出把低置信样本"送回模拟器重算"，这是**代理模型 + 物理求解器混合**的自然接口。

**M4｜泄漏为什么致命**：`pbuf_ozone_2` 与时间/地点强相关，反推后可以用 2D 邻域或"未来样本"帮助预测当前样本——这不再是 1D 大气柱问题，而是利用了数据划分的时序结构。其收益与"任务承诺"冲突：所有未用泄漏的队伍按 1D 假设投入算力，泄漏队伍获得不公平优势。治理请求与 1st 的自证共同定义了正确姿势：**主动放弃 + 可复现证明**（对照 T11/T17）。

**M5｜数值保真的机制**：目标值范围跨多个数量级（软裁剪前后的 ±3000σ），float32 在归一化/对数/指数变换中容易下溢为 0 或 inf；一旦某批出现 inf/NaN，训练即毁。1st 的 FP64 管道与 soft clipping 保证"极端值被压缩但不被截断丢弃"，同时保留反归一化的一致性。**在回归赛里，能稳定训练 200+ epoch 本身就是竞争力**。

**M6｜为什么"架构不是主差异"**：1st 的 Squeezeformer、2nd 的 ResLSTM、10th 的 UNet 都能到 0.788+；2nd 的组内比较只说"LSTM 显著优于 CNN/MHSA/GRU"，1st 说"每种技巧都可以去掉仍第一"。当数据规模、损失与数值管道到位后，架构更多提供的是**集成多样性**而非单点上限。

## 6. 证据分级

| 断言 | 等级 | 说明 |
| --- | --- | --- |
| 1st 全流程 | **自述 + >100 公开 notebook + GitHub（可复现自证）** | 高 |
| 2nd 权重表/模型清单 | 自述 + GitHub + 权重文件 | 高 |
| 10th 消融链（含 late submission） | 自述 + 图（逐项单变量） | 中高 |
| 4th 三成员方案 | 自述（含泄漏遗留自认） | 中 |
| "MAE > MSE"（1st） | 自述（语气强，无消融数字） | 中（方向与其他队一致） |
| float32 下溢（Two tips） | 自述（LB 0.766 背书） | 中高 |
| 气候不变特征 +1%/+0.05% | 10th 自述 + 消融表 | 中高 |
| 泄漏（pbuf_ozone_2） | 确认帖 + 请求帖（均未收录正文）+ 4th 自认 | 中高（事实层面） |

## 7. 边界条件与反事实

- **反事实 1**：不用全量数据 → 10th：0.768 vs 0.781（−0.013）；2nd：−0.01。数据规模是第一杠杆。
- **反事实 2**：用 MSE 训练 → 1st/10th 均指向更差；极端样本主导梯度。
- **反事实 3**：float32 管道 → 下溢风险（Two tips 的第一条禁令）。
- **反事实 4**：使用泄漏 → 可能短期涨分，但违背任务设定且面临取消；1st 未用仍冠（存在性证明）。
- **边界**：结论依赖大规模仿真数据（70M 行级）与物理特征可得性；"数据规模优先"不适用小数据回归；"损失鲁棒性/数值管道/置信度头"可广泛迁移。

## 8. 悬案与失败学

**悬案**

1. **泄漏的最终裁决**（哪些方案被取消、榜单是否调整）未收录；511911 确认帖与 519249 请求帖的正文均缺失。
2. "secret for beating baseline"（501829）与"max=2523σ"（506490）未收录——极值分析与基线技巧的细节缺失。
3. 1st 的公榜防过拟合细节（哪些模型因"直觉"保留）无法复核；他自认集成对公榜轻微过拟合。
4. 10th 的"低置信样本送回模拟器"只是构想，未验证闭环收益。

**失败学（跨队合集）**

- 架构类：纯 Transformer、其他 1Dconv/transformer 组合、UNet（1st）；更深模型不稳定（10th）；Mixup、EMA（10th 的 Tereka 管线）。
- 损失类：MSE、MSE/MAE 组合、加权损失（1st）；log 归一化。
- 流程类：batch size 等超参遗留泄漏痕迹（4th）——**流程清洁度**是被忽视的合规要点；R² 与 1−MSE 的选择在测试集更换后决定验证有效性（10th）。
- 数据类：HR 预训练未收敛（10th）、无全量数据（多队）。

## 9. 图表证据

> 路径相对本文件（`analysis/deep/`）：`../../intel/leap-atmospheric-physics-ai-climsim/bodies/<topic>_img/NN.png`

**图 1：1st 的完整数据流与双损失结构**（topic 523063）——`../../intel/leap-atmospheric-physics-ai-climsim/bodies/523063_img/01.png`

*读图结论*：特征 556 → 多表示 1636 → +Wind 1696 → reshape [60,44] → Linear+LayerNorm → 12×Squeezeformer → GLUMlp 头 → [60,20] → Reshape 到 374 维；**主损失（MAE，374 目标）+ confidence 损失（MAE，374 误差）双头**；目标侧含 368+6 时空特征（辅助）。这是"1D 序列 + 多表示 + 置信度头"的完整体。

**图 2：置信度筛选曲线（1st）**（topic 523063）——`../../intel/leap-atmospheric-physics-ai-climsim/bodies/523063_img/02.png`

*读图结论*：横轴=保留样本比例，纵轴=R²；丢弃最低置信的 ~10% 后 R² 从 ~0.80 升到 ~0.83，丢到 30% 时到 ~0.93。**置信度头可直接用于样本筛选/路由**（低置信样本送回模拟器）。

**图 3：2nd 的 ResLSTM 块（单模型私榜最强）**（topic 523055）——`../../intel/leap-atmospheric-physics-ai-climsim/bodies/523055_img/05.png`

*读图结论*：LSTM → LayerNorm → 0.7·新值 + 0.3·残差 → GELU；多个 resLSTM 块 + Linear。**极简残差 LSTM 打败复杂模型**——本场"架构不是主差异"的注脚。

**图 4：10th 的数据→模型消融链（Phalanx）**（topic 523041）——`../../intel/leap-atmospheric-physics-ai-climsim/bodies/523041_img/02.png`

*读图结论*：1/7 子样本 0.768 → +EMA 0.770 → +全量 LR 0.781 → +drop path 0.782 → +expert 0.7825 → +集成 0.783 → +伪标+HR 0.78620/0.78285 → +val 0.78624/0.78288；架构为 PixelShuffle UNet（残差堆叠 + SE + 双头 Huber）。**单变量递增的"算力-收益对照表"**。

**图 5：10th（Tereka）的 Transformer+CNN+LSTM 架构**（topic 523041）——`../../intel/leap-atmospheric-physics-ai-climsim/bodies/523041_img/01.png`

*读图结论*：层位置嵌入（0–59）+ 序列特征 + 标量特征 → CNN → 8×（Transformer+CNN）→ LSTM → Linear；输出 6×60 序列 + 8 标量。**层级位置显式编码**的代表实现（与 1st 的 reshape、2nd 的 LSTM 同向）。

## 10. 对既有笔记/playbook 的修订点

1. `notes/science/leap-atmospheric-physics-ai-climsim.md` 升级（现为浅版）：补 6 篇作者/票数、四方案 × 11 维对照、数字账（1696 维、0.79410/0.79123、0.7955/0.78856、0.781→0.786 链、confidence 0.83）与 5 张图证；新增"泄漏治理"与"数值保真"节。
2. `playbook/science.md`（回归/物理仿真节）增补：
   - **鲁棒损失优先**：R²/回归指标下先试 MAE/SmoothL1/Huber；MSE 仅在误差近高斯时使用；
   - **数据规模与漂移**：全量 + 气候/时间不变特征（RH/归一化通量）；HR 数据的 soft clipping；
   - **不确定度头**：预测均值+方差（confidence head），正则 + 样本筛选/主动学习；
   - **数值管道**：FP64 编码 → FP32 → 升 FP64 反归一化；两级 soft clipping；禁止盲目 float32；
   - **集成与权重**：hill-climb/stacking 可用，但权重在公榜上搜索会过拟合（私榜最优常更简单）。
3. `playbook/00-通用方法论.md` 增补：**"泄漏治理三件套"**（识别—放弃—可复现自证）；**"训练损失服从误差分布，而非指标代数形式"**。
4. `analysis/THEORY.md`（Batch 5 末汇总 v0.5）候选：
   - **L62｜回归：鲁棒损失优先于 MSE**（本场 1st/10th + 多场佐证）；
   - **L63｜仿真回归的数据规模与漂移不变量**（10th 消融链 + 气候不变特征）；
   - **L64｜不确定度头 = 正则 + 样本路由**（1st confidence 筛选 + ARIEL 的 sigma 工程同族）；
   - **L65｜数值保真管道**（float 精度/soft clip；跨场通用）。

## 11. 出处

- 4th（34 票）：https://www.kaggle.com/competitions/leap-atmospheric-physics-ai-climsim/discussion/523042
- 1st（82 票）：https://www.kaggle.com/competitions/leap-atmospheric-physics-ai-climsim/discussion/523063
- 2nd（47 票）：https://www.kaggle.com/competitions/leap-atmospheric-physics-ai-climsim/discussion/523055
- 10th（33 票）：https://www.kaggle.com/competitions/leap-atmospheric-physics-ai-climsim/discussion/523041
- Two tips（109 票）：https://www.kaggle.com/competitions/leap-atmospheric-physics-ai-climsim/discussion/506984
- 泄漏治理请求（51 票）：https://www.kaggle.com/competitions/leap-atmospheric-physics-ai-climsim/discussion/519249
- 缺口登记（未收录正文）：511911、508630、501829、506490、519184、494968 等
