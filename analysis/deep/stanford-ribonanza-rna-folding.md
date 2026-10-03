# Stanford Ribonanza 深读：BPP 结构先验注入 × 长度外推 × 相似性 CV

> 赛事：Research ｜ 主题 science（RNA 化学位移/折叠）｜ 755 队 ｜ 标准赛 ｜ 指标：MAE（逐核苷酸反应性 DMS_MaP / 2A3_MaP，越低越好）
> 材料基础：`digests/stanford-ribonanza-rna-folding.md`（6 篇：1st/7th/8th/2nd/4th + best-single 讨论帖；80 条讨论索引）+ 15 张图（460121×7 / 460190×1 / 460203×2 / 460222×3 / 460316×2）
> 深读时间：2026-10（Tier A #39）

## 0. 一句话重述：这道题真正在考什么

题面是"由 RNA 序列预测每个碱基的化学位移反应性（两通道）"，实际被考的是**结构先验注入 + 长度外推 + 相似性感知验证**：

1. **BPP（碱基配对概率矩阵）是核心特征**：五队全部围绕 EternaFold 的 BPP 设计结构——注入 attention logits（1st/2nd/4th）、独立矩阵混合（7th matrix mixer）、注意力提升（7th dual stream）、GNN 邻接（8th）。补充其他 BPP 来源（Vienna/ContraFold/RNA-FM）几乎无增益——**先验的用法比先验的数量重要**。
2. **测试序列比训练长**：位置编码必须能外推——绝对位置嵌入直接失效；1st 的 Dynamic Positional Bias（学"距离→偏置"的函数）优于 xPos/ALiBi/随机相对偏移；2nd/4th 用 ALiBi，7th 用 rotary。
3. **训练集内部高度冗余**：1st 用汉明距离 DBSCAN（阈值 0.2）证明序列成簇（图 3）；随机 KFold 的验证近邻泄漏会高估分数。1st 的裁决：更严格的聚类切分只降低绝对分数、不改变模型相对排序 → 最终仍用简单 KFold 训全量模型；8th 则用聚类 GroupKFold + 把所有 seqlen=206 样本放同一折来持续评测长序列。
4. **信噪比（SN）处理决定训练效率**：权重采样（1st）、加权 MAE（2nd）、SNR 加权 MAE+MSE（8th）、误差加权 + SN 掩码（7th）；1st 明确"数据子集过滤被权重采样取代"；推理时统一把 SN 置 1。
5. **公开测试泄漏的诚信处理**：约 13% 公开测试序列与训练完全重复；1st 在大多数提交中对这些序列**清零预测**，仍拿冠军——分数与诚信可以兼容（对照 T11）。

一句话：**这是一场"结构先验 + 外推工程 + 验证纪律"的序列回归赛**——1st 用 27 模型集成 + dms→2a3 辅助模型收尾。

## 1. 材料与角色

| 帖子 | 作者 | 票数 | 角色与独有信息 |
| --- | --- | --- | --- |
| [460121](https://www.kaggle.com/competitions/stanford-ribonanza-rna-folding/discussion/460121) 1st | — | 147 | 12 层 Transformer；**BPP 注入 6 头注意力** + **Dynamic Positional Bias** + SE-Conv；EternaFold BPPM；SN 权重采样 + SN embedding；DBSCAN 相似性分析；**13% 重复清零**；27 模型集成（15 SE + 10 plain + 2 length-split）+ dms→2a3 模型混合；失败清单最长 |
| [440702](https://www.kaggle.com/competitions/stanford-ribonanza-rna-folding/discussion/440702) best single | — | 66 | 早期基线：LB 0.14895 / CV 0.12516；**警告私榜长度分布不同 + 序列相似性陷阱**（shakeup 预警） |
| [460190](https://www.kaggle.com/competitions/stanford-ribonanza-rna-folding/discussion/460190) 7th | — | 44 | 三种 BPP 注入（injection / matrix mixer / dual stream 注意力提升）；masked Conv1D 替代 MLP；flip 增强 + BPP 重算 **+10–15bps**；MLM 预训练 **+10bps**；SN 掩码 **+10bps**；最终 ~20 模型 0.13604/0.14189 |
| [460316](https://www.kaggle.com/competitions/stanford-ribonanza-rna-folding/discussion/460316) 2nd | — | 42 | Squeezeformer + GRU head；BPP 2DConvNet 做注意力偏置（**−0.002**，per-head bias 另 **−0.0025**）；ALiBi；加权 MAE log1p(sn)；单模型 CV 0.119、30h/4090；大模型/SSL 失败 |
| [460203](https://www.kaggle.com/competitions/stanford-ribonanza-rna-folding/discussion/460203) 4th | tattaka + monnu | 29 | 三系架构（改进 RNAdegformer / 1D Conv+Residual BPP Attention / Transformer BPP bias）；两阶段训练（SN 0.5→1.0）；伪标签带误差预测阈值；CV 0.1198–0.1219 |
| [460222](https://www.kaggle.com/competitions/stanford-ribonanza-rna-folding/discussion/460222) 8th | onodera 等 | 27 | CNN+GNN（LegNet 风格 100d bin 头）；chunk/segment 邻接特征；**聚类 GroupKFold + seqlen=206 全放 fold0**；MAE+MSE SNR 加权；伪标签提升单模型（0.14299→0.14186） |

**材料缺口（受"不扩采"约束，登记备查）**：**3rd(460403,24 票,AlphaFold 风格 Twin Tower)** 未收录、**"How to check if your model generalizes to long sequences"(444653,60 票)** 未收录、宿主方案(460301,23)、ESM2+folding head(460285,23)、2A3/DMS 误差关系(451158,25)、3D 坐标建模(451853,25)、外部 RMDB 数据(454397,19)、0.141 天花板(458478,21)、15th(460130,21) 等未收录——**长序列泛化检测方法**与 3rd 架构是本次深读最大缺口。

## 2. 逐方案对照矩阵

| 维度 | 1st | 2nd | 4th tattaka+monnu | 7th | 8th |
| --- | --- | --- | --- | --- | --- |
| BPP 注入 | 6 头注意力 logits 直加（Conv 块输出 6 通道，与注意力值相加） | BPP → 2DConvNet → 共享注意力偏置；另试 per-head scale | 注意力偏置 / Residual BPP Attention（用 BPP 当注意力权重） | injection / matrix mixer / **dual stream 注意力提升**（scaled tanh 回注） | bpp/chunk/structure/segment 四类邻接 → 独立 CNN+GNN 块 |
| 位置编码 | **Dynamic Positional Bias**（距离→MLP→每头偏置；优于 xPos/ALiBi/随机偏移） | ALiBi | ALiBi（与 bp_matrix 分开作用） | rotary | 无显式 PE（Conv1D + GNN 邻接提供结构/相对信息） |
| 架构 | 12 层 Transformer（192 维，6 头×32） | Squeezeformer（dim192/4 头/kernel17/12 层）+ GRU head | RNAdegformer 改；1D Conv+SE-Residual+Bi-LSTM 两系 | width 384/head64/depth24/droppath0.3；masked Conv1D 替代 MLP | 纯 CNN+GNN（SE-Residual × 3 层组）；100d bin 头 |
| SN 处理 | 权重采样 `0.5*clamp_min(log(sn+1.01),0.01)` + SN embedding（推理置 1） | 加权 MAE `log1p(sn).clip(0,10)` | 两阶段：SN 0.5 → 1.0 微调 | 误差加权 `1/sqrt(1/6+err.clip(100))` + SN 掩码 | SNR 加权 MAE+MSE；掩码按 SN |
| CV | DBSCAN（汉明 0.2）诊断 → 结论"相对排序不变" → 最终简单 KFold | 5 折 | 简单 5 折 | 相似性切分 + 排除测试重叠；val ~20k | **聚类 GroupKFold**；seqlen=206 全放 fold0 |
| 伪标签 | 单模型提升、集成无增益（未进最终集成） | 未用（CV 无提升） | 用误差预测阈值化（sn_pred>0.75/1.0） | 全流程 PL：CV +10bps、最终集成含 PL | 单模型 0.14299→0.14186 |
| 集成 | 27 模型 + dms→2a3 模型（27/28 + 1/28 混合） | 多种子平均 | 少模型集成（"ensemble"项） | ~20 模型 | 队友模型混合 |
| 成绩（private/public） | 冠军（13% 重复清零仍胜） | 单模型 0.142/0.140 → 种子集成 0.140/0.135 | exp072 0.14124/0.13681；三种子模型 0.1412–0.1427 | 最佳单模型 0.14296/0.13697；最终 **0.14189/0.13604** | 单模型 0.14299/0.14012；+PL 0.14186/0.13739；blend 0.14263/0.13626 |
| 失败清单 | LegNet 全卷积、capR、额外 BPP、3D 数据、绝对/相对/xPos/ALiBi、滑动窗口、位置掩码损失、SN 加权损失、伪标签进集成 | SSL、dim>512、多数增强、伪标签（CV） | contrafold_2、距离矩阵、结构特征、BPP 特征工程、SN 权重 | EX 数据私榜无增益、额外 BPP 无增益、30M 序列 MLM、EMA/AWP、Floyd-Warshall、2D U-shape | （未列） |

## 3. 共识、分歧与裁决

### 共识一：BPP 是核心先验，且"注入方式"比"来源数量"重要（5/5）

1st：EternaFold BPPM 进注意力；2nd：BPP 直加偏置 −0.0025、再叠 2DConvNet −0.002；7th：四类注入对比（含 dual stream 最佳）；4th：三种 BPP 注意力方案；8th：四类邻接矩阵独立 GNN；
反面对照：1st/7th 均试过 ContraFold/ViennaRNA/RNA-FM/SQUARNA 等——无显著增益，1st 甚至说"异源 BPPM 反而更差"。

**裁决**：EternaFold BPP 已捕获主要二级结构信息；收益来自"如何让注意力回路使用它"，而不是堆更多来源。置信度：高（全员行为 + 双向对照）。

### 共识二：位置编码必须能外推到更长序列（4/4 明确对比）

1st：绝对 PE 无法泛化（unsolvable）；相对偏移可解外推但效果差；xPos/ALiBi 不如 Dynamic Positional Bias；ALiBi 即使在部分头也较差；
2nd：ALiBi 稳健（单模型 CV 0.119）；
7th：rotary + BPP 注入 + 24 层的组合达到单模型 0.14296；
4th：ALiBi 分开作用于头与 bp_matrix。

**裁决**：本质是**把"位置信息"建模为距离的函数**（可外推），而不是位置 ID 的查表（不可外推）；具体函数族（ALiBi 指数衰减 / MLP 学出的偏置 / rotary）各有适用面，1st 的动态偏置在其实验中最佳。置信度：高。

### 共识三：相似性感知验证是必须的，但"用哪种切分训练最终模型"可以有例外（3/3 分析，2 种结论）

1st：DBSCAN 显示严重冗余（图 6）；聚类切分下绝对分数下降但**相对排序与简单 KFold 一致** → 最终用简单 KFold 训练（把聚类切分当作诊断工具）；
8th：直接用聚类 GroupKFold 训练，并把 206 长度样本放同一折；
7th：相似性切分 + 排除与测试重叠的训练样本（val ~20k）。

**裁决**：相似性切分的价值在于**诊断泄漏与排序可靠性**；是否用它训练最终模型取决于"绝对分数 vs 数据利用率"的权衡。1st 的"诊断用严格切分、训练用 KFold"是自洽的工程折中（但依赖"相对排序不变"这一实证前提）。置信度：中高。

### 共识四：SN 噪声要用"加权/掩码"而非"硬过滤"（4/4）

1st：权重采样取代 subsetting；
2nd：log1p(sn) 加权 MAE；
4th：两阶段 SN 阈值（0.5→1.0 微调）；
7th：误差加权 + SN 掩码；
8th：SNR 加权 + 掩码。

**裁决**：硬过滤丢数据且门槛难调；连续加权（采样或损失）保留全部样本并按测量质量分配影响。7th 的"掩码 vs 过滤"对照（+10bps）与 1st 的"subsetting 被 weight sampling 取代"互相印证。置信度：高。

### 分歧一：伪标签对集成的贡献

1st：单模型更好，加入集成无增益（明确写"not improve ensemble"）；
7th：全流程 PL（含误差预测与再训练）CV +10bps，最终 20 模型集成含 PL；
8th：单模型 0.14299→0.14186（+PL），混合私榜 0.14263；
2nd：CV 无提升 → 放弃；4th：用误差预测阈值化 PL。

**裁决**：PL 的增益是**流程依赖**的——需要"误差预测/置信度筛选 + 与预训练/微调阶段配合"才能兑现集成收益；朴素 PL 只提升单模型（1st）或不动 CV（2nd）。置信度：中。

### 分歧二：架构家族（Transformer vs 混合 vs CNN+GNN）

1st：LegNet 全卷积在 RNA 上失败（长程接触需要注意力）→ Transformer；
2nd：Squeezeformer（Conv+Transformer 混合）收敛快、性能强；
8th：纯 CNN+GNN（用邻接矩阵表达长程/结构关系）CV 0.1336；
4th：RNAdegformer 改（Conv+Transformer）。

**裁决**：关键不是"要不要注意力"，而是**长程结构信息如何进入模型**——注意力（BPP 注入）与图邻接是两条可行路径；混合架构（Squeezeformer）以更少参数获得局部+全局优势。置信度：中。

### 分歧三：外部数据（EX/RMDB）的价值

7th：EX 微调 CV/公榜 +5–10bps，**私榜无增益**（明确）；
1st：公开数据微调无提升；
8th：RMDB 交替训练（预期帮助长序列）；
2nd：未用。

**裁决**：EX 数据与测试分布的一致性存疑（私榜长度分布不同 + 部分数据仅覆盖序列端点）；其收益更可能来自"公榜红利"。参考 13% 重复问题：本场公榜指标被泄漏与分布差污染。置信度：中（对照 T10/T11）。

### 特别裁决：13% 公开测试重复的诚信处理

1st：在大多数提交中把与训练完全重复的测试序列预测**清零**（避免选择"记住重复序列"的模型），有时保留非清零提交用于对比；仍然夺冠。

**裁决**：这是 T11"使用测试数据：合法域适应 vs 违规套利"的正面案例——**主动放弃泄漏红利**可以在不损失名次的前提下提高方案可信度（也反向说明该泄漏对头部竞争者的影响有限）。置信度：中高（结果佐证）。

## 4. 增量数字账

| 动作 | 数字 | 来源 |
| --- | --- | --- |
| 1st 架构 | 12 层 Transformer；embedding 192；SA 6 头×32 维；Dynamic Positional Bias；SE 版/plain 版 Conv 块 | 1st |
| 1st 训练 | one-cycle（pct_start 0.05、lr_max 2.5e-3）+ AdamW wd 0.05、bs 128；最终模型 **270 epoch**、每 epoch 1791 batch；SN 权重 `0.5*clamp_min(log(sn+1.01),0.01)`；追加 SGD 微调 ~15×500 batch | 1st |
| 1st 集成 | **15 SE-Conv + 10 plain Conv + 2 length-split**（其一接受 bracket 特征）；dms→2a3 模型：`(27/28)·avg_2a3 + (1/28)·pred_2a3` | 1st |
| 1st 泄漏处理 | 约 **13%** 公开测试序列与训练完全相同；多数提交对其清零 | 1st |
| 2nd 消融 | BPP 直加注意力偏置 **−0.0025**；BPP 2DConvNet **−0.002**；GRU head 小幅；OpenVaccine 特征仅 **−0.0005** | 2nd |
| 2nd 训练 | 200 epoch、bs 256、lr 2e-3（cosine+warmup）、AdamW wd 0.01；加权 MAE `log1p(sn).clip(0,10)`；单模型 **30h/RTX4090**；CV 0.119 → pub 0.140/priv 0.142；种子集成 0.135/0.140 | 2nd |
| 7th bps 级增益 | flip 增强 + 正确顺序 BPP 重算 **+10–15bps**；MLM 预训练 **+10bps**；SN 掩码（vs 过滤）**+10bps**；EX 微调 CV/pub +5–10bps、priv 无 | 7th |
| 7th 单模型 | bpp injection：0.14013 pub / 0.14375 priv（+PL 0.13973/0.14292）；dual stream：**0.13697 pub / 0.14296 priv**（作者称可进 top10；若跑完 PL 预计 ~0.1419 priv） | 7th |
| 7th 最终 | ~20 模型集成 **0.13604 pub / 0.14189 priv** | 7th |
| 4th 对照表 | exp064–exp072：CV 0.11976–0.12146；最佳 exp072 pub 0.13681/priv 0.14124；1D Conv 分支 CV 0.12161、pub 0.13889/priv 0.1425；Transformer BPP bias CV 0.12188、pub 0.13948/priv 0.14267 | 4th |
| 8th 分数链 | 单模型 scratch CV 0.1336（seqlen206 0.1133）pub 0.14012/priv 0.14299；+PL1 0.14222；+PL2 **0.14186**；blend CV 0.127645、pub 0.13626/priv 0.14263 | 8th |
| 8th 增强 | 同分异构/其他增强无益；100d bin 头稳定回归；MAE+MSE SNR 加权 | 8th |
| 早期基线 | best-single 帖：LB 0.14895 / CV 0.12516（单折） | 440702 |

**结构校验（2 处吻合）**

1. 1st 的 6 头 × 32 维 = 192 = embedding 维 ✓（图 3 标注一致）；
2. 8th 的 100d bin 头 → 加权求和 1d 标量，与 LegNet 设计一致 ✓。

## 5. 机制推演

**M1｜BPP 注入为什么是"加速器 + 上限"**：RNA 反应性由二级结构决定（配对碱基不反应、环区暴露）；BPP 是结构分布的软先验。7th 的对照最有说服力：早期把 BPP 作为**辅助输出**（mean attention 拟合 BPP）需要 200–250 epoch 收敛；改为**输入**后几十个 epoch 达到相当效果——先验放在输入端把"学习结构"变成"使用结构"。同时 1st 的异源 BPPM 对照显示上限由先验质量而非数量决定。

**M2｜先验必须参与可学习回路**：7th 的 matrix mixer 是"无反馈"（No feedback）的独立路径，效果弱于 dual stream——后者把注意力状态投影 + scaled tanh 回注注意力矩阵（attention boosting），让先验与表示互相修正。**静态拼接的先验不如交互式先验**（与 4th 的 residual BPP attention 同向）。

**M3｜长度外推 = 学距离函数**：绝对 PE 是位置 ID 查表，超出训练长度无定义；Dynamic Positional Bias 把相对距离 d=|i−j| 输入 MLP（1→48→48→6）输出每头偏置——同一函数可作用于任意长度（图 4）。ALiBi 用固定指数衰减实现同类思想；rotary 也可外推但在 1st 的对比中较差（可能与 BPP 注入的交互有关）。

**M4｜SN 加权的统计学意义**：低 SN 序列的实验标签是"高方差观测"；硬过滤等价于截断估计（丢数据 + 选择偏差），连续加权等价于对每个样本按其精度加权的最小二乘（逆方差加权）。7th 的"掩码 vs 过滤 +10bps"说明**保留低 SN 的序列上下文、只削弱其监督**优于直接删除。

**M5｜相似性泄漏的机制**：训练集由 RNA 家族构成，同族序列高度相似（图 6 的簇带）；随机 KFold 的验证样本在训练中存在近似同族近邻 → 验证分数反映"记忆近邻"而非泛化。1st 的关键实证：更严格聚类切分下**绝对分数下降、模型排名不变** → 泄漏影响"水平"而非"排序"，因此简单 KFold 仍可用于模型选择；但这个结论需要每个比赛单独验证（本次的宝贵方法论）。

**M6｜13% 重复清零的经济学**：公开测试的重复序列提供免费的（记忆即可得的）分数；清零相当于主动放弃最多 13% 样本的确定性收益。1st 仍夺冠说明：① 头部模型在非重复序列上的差距足够大；② 保留这些分数会让"选择记忆型模型"的风险上升（私榜无重复时反噬）。这是"公榜红利 vs 私榜稳健"的又一案例。

## 6. 证据分级

| 断言 | 等级 | 说明 |
| --- | --- | --- |
| 1st 全结构/数字 | 自述 + GitHub + 7 张图 | 中高 |
| 13% 测试重复 | 1st 自述（行为佐证：清零提交仍夺冠） | 中 |
| 7th bps 级增益与 PL 流程 | 自述 + 代码 + 架构图 | 中高 |
| 2nd 消融数字（−0.0025/−0.002） | 自述 + 代码 | 中高 |
| 8th CV/LB 分数链 | 自述 | 中 |
| 4th 多模型 CV 表 | 自述 + 代码 | 中 |
| "相对排序不变"（1st 聚类切分结论） | 自述（无表格） | 中低 |
| EX 私榜无增益 | 7th 单队 | 中低 |
| LegNet 全卷积失败 | 1st 单队 | 中低 |

## 7. 边界条件与反事实

- **反事实 1**：若只用序列不用 BPP → 7th 的经验：学结构极慢（200+ epoch）且上限低；1st 的异源 BPP 对照说明可用先验不止一种但 EternaFold 足够。
- **反事实 2**：若用绝对位置编码 → 长序列外推失效（1st 明确"unsolvable issues"）。
- **反事实 3**：若把随机 KFold 的绝对分数当真 → 近邻泄漏导致高估；1st 的聚类诊断是标准动作。
- **反事实 4**：若利用 13% 重复冲榜 → 可能获得短期公榜收益，但私榜无重复时风险暴露；1st 的清零策略给出"诚信与冠军可兼得"的存在性证明。
- **边界**：结论依赖"可由外部工具计算的结构先验（BPP）"；纯序列任务与无 `SN` 元数据的任务需替换相应机制（先验注入 → 其他领域先验；SN 加权 → 样本质量加权）。

## 8. 悬案与失败学

**悬案**

1. **3rd place（460403，AlphaFold 风格 Twin Tower + Squeezeformer）未收录**——与 2nd 的 Squeezeformer 路线的关系未知；长序列外推方案缺失一块。
2. **"How to check if your model generalizes to long sequences"（444653，60 票）未收录**——本场最重要的验证方法论帖之一。
3. 私榜长度分布的具体差异未量化（best-single 帖只有警告）；EX 数据私榜无增益的机制未解释。
4. 13% 重复率无官方确认。
5. 0.141 天花板的成因（458478）与 2A3/DMS 误差关系（451158）未收录。

**失败学（跨队合集）**

- 先验类：capR（结论不定）；额外 BPP 来源（ContraFold/Vienna/RNA-FM/SQUARNA）；BPPM 平均；3D 坐标数据（1st 看图后放弃）。
- 位置/长度类：绝对 PE；随机相对偏移；xPos（长序列差）；ALiBi 在 1st 的对比中次优；滑动窗口（生物学上错误且伤训练域表现）。
- 训练类：位置级误差掩码损失；SN 直接加权损失（1st，无提升）；30M 外部序列 MLM（7th）；EMA/AWP（7th）；大模型 dim>512（2nd）；SSL（2nd，结果不定但放弃）；多数增强（2nd/7th 仅 flip+BPP 重算有效）；1st 的全卷积 LegNet；UNet 层级（4th）；距离矩阵/结构特征/BPP 特征工程（4th）。
- 数据类：EX 数据（公榜有效、私榜无效）；伪标签进集成（1st 无增益）；伪标签 CV（2nd 无增益）。

## 9. 图表证据

> 路径相对本文件（`analysis/deep/`）：`../../intel/stanford-ribonanza-rna-folding/bodies/<topic>_img/NN.ext`

**图 1：1st 的 Self-Attention Block（BPP 注入 + 动态位置偏置）**（topic 460121）——`../../intel/stanford-ribonanza-rna-folding/bodies/460121_img/03.png`

*读图结论*：Q(6 头×32) 与 K^T 得到注意力值 → **加上 BPP Conv 块输出（6 头×32）+ 动态位置编码块输出** → softmax → ×V → 拼接头输出；BPP 特征同时传递到下一层。这是"结构先验进注意力 logits"的最清晰实现图（1st 与 4th/2nd 同族）。

**图 2：Dynamic Relative Positional Encoding（学距离函数）**（topic 460121）——`../../intel/stanford-ribonanza-rna-folding/bodies/460121_img/04.png`

*读图结论*：由序列长度生成相对距离矩阵（含负值）→ 每个距离值经 MLP（1→48→48→6）→ 6 通道每头偏置图。**学的是"距离→偏置"的函数而非位置查表**，因此可外推到训练未见长度。

**图 3：1st 的序列相似性聚类（DBSCAN，汉明阈值 0.2）**（topic 460121）——`../../intel/stanford-ribonanza-rna-folding/bodies/460121_img/06.jpg`

*读图结论*：横轴=序列 ID、纵轴=簇代表 ID，对角带 + 大量离对角块 = 训练集存在成片近重复序列。**随机 KFold 的验证近邻泄漏证据**（1st 据此诊断；结论是排名的相对性不受影响）。

**图 4：7th 的三种 BPP 注入架构**（topic 460190）——`../../intel/stanford-ribonanza-rna-folding/bodies/460190_img/01.png`

*读图结论*：左=bpp→Conv1d→加到注意力值（injection）；中=bpp+ALiBi→独立 Matrix mixer（标注"No feedback"）→加偏置；右=**dual stream**：bpp→Conv2d→scaled tanh→回注注意力（attention boosting），并与 Conv1d 主干形成双路。三者的对比说明"先验要参与可学习回路"。

**图 5：2nd 的 Squeezeformer + BPP 2DConvNet 注意力偏置**（topic 460316）——`../../intel/stanford-ribonanza-rna-folding/bodies/460316_img/01.png`

*读图结论*：序列嵌入(192) → 12×Squeezeformer（Conv1DBlock→SwiGLU FFN→MHA→FFN）→ GRU → Linear(L,2)→ 加权 MAE；BPP(L,L)→2 层 2DConv(64/4,k7) → **输出矩阵在所有 Transformer 块间共享**并加入注意力偏置。消融：直加偏置 −0.0025、2DConv 再加 −0.002。

**图 6：8th 的 CNN+GNN 结构与四类邻接矩阵**（topic 460222）——`../../intel/stanford-ribonanza-rna-folding/bodies/460222_img/03.png`

*读图结论*：序列 + loop_type + structure 三类嵌入 → Conv1d；bpp / chunk / structure / segment 四类邻接各自进入独立的 3 层 GNN+CNN 与 SE-Residual 块 → 3 层 CNN → Linear → 每目标 100d bin 向量 → 加权求和为标量。**用图邻接表达长程结构，完全不用注意力**（与 1st/2nd 的注意力路线形成对照）。

## 10. 对既有笔记/playbook 的修订点

1. `notes/science/stanford-ribonanza-rna-folding.md` 升级（现为浅版）：补 6 篇作者/票数、五方案 × 10 维对照、数字账（−0.0025/−0.002、+10–15bps、0.14189、13%）与 6 张图证；新增"长度外推与相似性 CV"节。
2. `playbook/science.md`（序列/RNA 回归节）增补：
   - **结构先验注入四方案**（注意力 logits / 注意力提升 / 独立矩阵混合 / 图邻接）与"先验要参与可学习回路"；
   - **长度外推 = 学距离函数**（Dynamic Positional Bias / ALiBi / rotary 对比；绝对 PE 禁用）；
   - **SN/质量加权三选一**（采样权重、损失权重、掩码）优于硬过滤；
   - **相似性感知 CV**：聚类诊断 + "绝对分数 vs 相对排序"分离；训练切分可例外；
   - **伪标签的分层评估**（单模型 vs 集成）。
3. `playbook/00-通用方法论.md` 增补：**"静态先验 vs 交互式先验"**（先验必须可被表示修正）；**"泄漏红利主动放弃"**（13% 重复清零仍夺冠的存在性证明，补 T11）。
4. `analysis/THEORY.md`（Batch 4 收尾扩 v0.4）候选：
   - **L63｜结构先验要注入可学习回路**：证据 = 本场（BPP 注入/dual stream）+ 4th residual attention；
   - **L64｜长度外推 = 学距离的函数**：证据 = 本场位置编码对比；
   - **L65｜相似性 CV：分离"水平"与"排序"**：证据 = 1st 的聚类诊断结论；
   - **T17｜伪标签：单模型收益 vs 集成收益**：1st（无）vs 7th/8th（有，流程依赖），与 T6 合并；
   - **T11 补强**：13% 重复清零仍夺冠。

## 11. 出处

- 1st（147 票）：https://www.kaggle.com/competitions/stanford-ribonanza-rna-folding/discussion/460121
- best single model（66 票）：https://www.kaggle.com/competitions/stanford-ribonanza-rna-folding/discussion/440702
- 7th（44 票）：https://www.kaggle.com/competitions/stanford-ribonanza-rna-folding/discussion/460190
- 2nd（42 票）：https://www.kaggle.com/competitions/stanford-ribonanza-rna-folding/discussion/460316
- 4th（29 票）：https://www.kaggle.com/competitions/stanford-ribonanza-rna-folding/discussion/460203
- 8th（27 票）：https://www.kaggle.com/competitions/stanford-ribonanza-rna-folding/discussion/460222
- 缺口登记（未收录正文）：3rd(460403)、444653、460301、460285、451158、451853、454397、458478、460130 等
