# Open Problems Single-Cell Perturbations 深读：极弱输入 × 18k 目标 × 榜单哲学

> 赛事：Featured ｜ 主题 science（单细胞扰动响应）｜ 1097 队 ｜ 标准赛 ｜ 指标：Weighted Rowwise RMSE（MRRMSE；越低越好；public 与 private 刻度不同）
> 材料基础：`digests/open-problems-single-cell-perturbations.md`（6 篇：#13 U900 长文/1st/2nd/3rd + 指南 + 提问帖；80 条讨论索引）+ 12 张图（458750×8 / 459258×4）
> 深读时间：2026-10（Tier A #37）

## 0. 一句话重述：这道题真正在考什么

题面是"输入只有 `(cell_type, sm_name)` 两个短关键词，输出 18211 个基因的差分表达（DE，Limma log-p 预处理）"，实际被考的是**在信息极弱的输入端做特征富集、在超高维输出端做降维/多目标建模、在不可靠的 CV 下做选择**：

1. **输入富集是胜负手**：两个关键词没有任何结构信息，四强分别用 ChemBERTa/SMILES 嵌入（1st/#13）、目标编码 mean/std（2nd/#13/3rd）、统计量（1st）；而 Wikipedia 描述与通路先验被证明不如"通用表示 + 目标编码"（1st 0.614→0.656 变差；#13 明确"纯 ML 方法优于先验知识特征"）。
2. **18k 目标的两种处理**：TSVD 降到 ~70 维再反变换（#13 的 boosting、3rd），或直接多目标预测（PyBoost 原生多目标、NN/Transformer）。#13 的洞见：**降维反而常涨分，因为丢掉的主要是噪声**。
3. **小样本训练技巧**：固定 epoch 数（禁用早停）→ 在"almost entire"训练子集上重训多次平均（#13 的 CV 与提交解耦策略）；train duplication（#13：0.600+→0.580+）；多损失加权（1st：MSE/MAE/LogCosh/BCE = 0.32/0.24/0.24/0.2）。
4. **CV 与榜单的错位**：#13 实测 local MRRMSE 与 LB 近零相关、row-wise 相关也只有 ~0.5；但 public-private 相关高达 0.98——最终"混权靠 LB、模型靠 CV"。同时 MRRMSE+log-p 对离群值敏感，催生榜单探针甚至"乘 1.2"式套利，#13 直接建议重设评测协议。

一句话：**这是一场"弱输入富集 + 多目标建模 + 验证哲学"的比赛**；方法论产出 PYBOOST（多目标梯度提升）比名次更被社区记住。

## 1. 材料与角色

| 帖子 | 作者 | 票数 | 角色与独有信息 |
| --- | --- | --- | --- |
| [438859](https://www.kaggle.com/competitions/open-problems-single-cell-perturbations/discussion/438859) 综合指南 | — | 65 | 任务与挑战全景：CMap 数据偏癌系、18k 维、技术噪声、细胞类型特异性；既有方法（Dr.VAE/scGEN/ChemCPA/RF/XGBoost）；评测为 MRRMSE |
| [460858](https://www.kaggle.com/competitions/open-problems-single-cell-perturbations/discussion/460858) #13 U900/PYBOOST | A. Vakhrushev 等 | 65 | **本场最完整的方法论长文**：PYBOOST（多目标 boosting + SketchBoost）；Quantile80 目标编码 0.602→0.586；almost-entire 子集 0.584→0.577；排除 CD8 0.586→0.584；多阶段等权 blend 0.575→0.566→0.559→0.558；CV-LB 分析（50+ 模型）；赛后 solo PyBoost 私榜 0.718 优于原 top1 的 0.728 |
| [459258](https://www.kaggle.com/competitions/open-problems-single-cell-perturbations/discussion/459258) 1st | Jean Kouagou | 50 | BioWordVec 0.767 → ChemBERTa SMILES + 统计特征 0.614；Wikipedia 描述反而 0.656（失败）；LSTM/GRU/1d-CNN（GRU 私榜 0.733、1D-CNN 0.745、LSTM 0.839，融合 0.723–0.725）；四损失加权；250 epoch；30% 置零增强；细胞类型难度与数据量鲁棒性曲线 |
| [458738](https://www.kaggle.com/competitions/open-problems-single-cell-perturbations/discussion/458738) 2nd | — | 49 | 4 模型复合（0.551/0.559/0.575/0.554，权重 0.5/0.25/0.25/0.3）；transformer（d=128）+ 目标编码 mean/std（四分四层编码）；KMeans 聚类采样划分；Lion + Huber；20k epoch、early stop 5k、ReduceLROnPlateau(0.9999/500) |
| [458750](https://www.kaggle.com/competitions/open-problems-single-cell-perturbations/discussion/458750) 3rd | — | 33 | **两阶段伪标签**（先用 7 模型产 255 条测试伪标签 → 20 模型重训取中位）；Optuna（4 折×2 重复）；TSVD；列 min/max 裁剪；1 小时 CPU 可复现；列范围/难易基因/切分设计/噪声鲁棒性全套图 |
| [456239](https://www.kaggle.com/competitions/open-problems-single-cell-perturbations/discussion/456239) 评审奖提问 | — | — | 低信息，登记备查 |

**材料缺口（受"不扩采"约束，登记备查）**：#18 Py-boost predicting t-scores(458661,54 票)、PYBOOST 专帖(454700,33)、奇怪数据观察(445883,33)、**Stop spoiling the competition with high scoring notebooks(457753,29)**、Will there be a huge shakeup(456943,28)、SMILES 规则(440177,26)、ChemBERTa v2(441550,24)、Lessons Learned(458916,20) 等未收录——榜单探针争议与 PYBOOST 算法细节是两大缺口。

## 2. 逐方案对照矩阵

| 维度 | #13 U900/PYBOOST | 1st Kouagou | 2nd | 3rd |
| --- | --- | --- | --- | --- |
| 输入特征 | SMILES embedding / 目标编码（Quantile80 最优）/ Morgan 指纹与描述符基准（最终未用）；纯 ML 编码优于生物先验 | ChemBERTa(SMILES) + one-hot + 每 cell/drug 的 mean/std/分位数统计；Wikipedia 描述失败 | 目标编码 mean/std（sm_name 与 cell_type 各拆多层）+ 稀疏特征线性嵌入 | 以 sm_name 为主（SMILES+LSTM 尝试失败）；Optuna 调参 |
| 目标处理 | TSVD ~70 维（boosting）；NN 直接 18k；**降维去噪** | 直接 18k（GRU/CNN/LSTM） | 直接 18k（transformer） | TSVD 降维 + 伪标签两阶段 |
| 模型 | PYBOOST（多目标 boosting）+ CatBoost + MLP(目标编码) + SMILES-NN | GRU / 1d-CNN / LSTM 融合 | 4 个 transformer 变体（含"放大器"模型） | MLP/网络 + Optuna + 多模型 |
| 损失 | boosting 原生；NN 用 MAE/竞赛损失 | **MSE+MAE+LogCosh+BCE 加权 0.32/0.24/0.24/0.2** | Huber；Lion 优化器 | MRRMSE 直接作为损失（替换 MAE 后提升） |
| 小样本技巧 | **固定 epoch 禁用早停 → "almost entire"子集重训平均**；train duplication | 250 epoch；30% 特征置零增强 | 20k epoch + 早停 5k；grad clip 1 | 每模型训 10 次取中位；伪标签 |
| 验证 | 多种 CV 方案对比；最终混权靠 LB（CV-LB 失配） | 5 折（seed 42）+ 折内细胞类型分析 | KMeans 聚类采样划分（val 10%） | 自定义折：每折一种细胞类型 + 仅公/私测出现的 sm_name |
| 集成 | 多阶段等权（0.5/0.5）blend；多样性用预测相关 0.8–0.9 控制 | 0.25×LSTM + 0.65×CNN/GRU | 0.5/0.25/0.25/0.3 加权和 | 7 模型伪标签 → 20 模型加权 + 10 次中位 |
| 分数（注意刻度） | 融合 public 0.558；solo PyBoost 私榜 0.718（优于原 top1 0.728） | GRU 私榜 0.733 / CNN 0.745 / LSTM 0.839；融合 0.723–0.725；全量数据 0.719 | 组件 public 0.551–0.575 | 未给总分；称"最高 CV 的提交拿到最高私榜" |
| 失败清单 | SMILES 增强、LSTM/CNN 替代嵌入、伪标签进最终 blend、直接预测 18k（未调好）、DrugBank 特征（未完成） | Wikipedia 描述嵌入变差；ChemBERTa padding 未去除 | （未列） | 归一化/标准化、chained regression、去噪数据集、去离群、加噪标签、只训易/难列、Huber loss |

**刻度提醒**：本场 public（约 0.55–0.62）与 private（约 0.72–0.84）数值刻度不同，跨榜数字不可直接比较；所有比较必须在同一榜单内进行。

## 3. 共识、分歧与裁决

### 共识一：输入富集是必需项，但"通用表示 + 目标编码"胜过"手工生物先验"（4/4 行为一致）

1st：BioWordVec 0.767 → ChemBERTa 0.614；Wikipedia 描述反降到 0.656；
#13：系统对比 ChemBERTa/Morgan/描述符/one-hot/对照编码——非目标编码里最简单 one-hot 最好；通路/PPI 先验特征"less prominent than pure ML"；
2nd：目标编码 mean/std 是核心；
3rd：主要靠 sm_name 嵌入 + 训练技巧。

**裁决**：在极弱输入场景，**"从数据学到的类别统计（目标编码）+ 预训练通用表示（ChemBERTa/SMILES）"** 是最稳组合；手工生物先验受数据库覆盖、批次效应与噪声拖累，收益不稳定。置信度：中高（多队独立 + 1st 的直接对照）。

### 共识二：小样本下需要"去早停"的训练协议（#13 体系化，其他队部分采用）

#13：固定 epoch（CV 阶段调好，提交阶段禁用早停）→ 才能在"almost entire"子集上重训并平均；boostings 0.584→0.577，MLP 0.580+→0.570+；
1st：固定 250 epoch；
3rd：每模型 10 次训练取中位；
2nd：用早停但辅以大量正则（dropout+wd+clip）。

**裁决**：当样本量小到"留出验证本身都在浪费数据"时，**CV 与提交准备解耦**（CV 定超参 → 全量/近似全量重训）比早停更划算；代价是失去逐模型早停的自适应，需要用固定预算 + 多次重训平均换稳定性。置信度：中高（#13 有系统数字）。

### 共识三：CV 与 LB 的关系不可靠，但公私榜高度相关（#13 量化，1st/3rd 结构佐证）

#13：local MRRMSE 与 LB 近零相关；local row-wise 相关约 0.5；NK 细胞相关 0.2+、CD8 为负；random folds 不比"逻辑切分"差；public-private 相关 0.98；
1st：折间差异巨大（0.86 vs 1.19），由折内主导细胞类型决定；
3rd：设计"每折一种细胞类型 + 只含公/私测出现的 sm_name"的切分，最高 CV 对应最高私榜。

**裁决**：CV 的价值取决于是否复现测试的**结构组成**（细胞类型难度 × 药物覆盖）；本地 MRRMSE 绝对值不可用于跨模型选择，混权只能靠同一榜单内的相对排序（并承担探针污染风险）。置信度：高（#13 的 50+ 模型统计 + 1st 的折间证据）。

### 分歧一：目标降维（TSVD）vs 直接预测 18k

#13：boosting 走 TSVD-70；"降维常涨分，因为丢的是噪声"；NN 直接 18k 也有效；
2nd/1st：直接 18k（transformer/RNN）；
3rd：TSVD。

**裁决**：不是互斥——**TSVD 是 boosting 的必需品（多输出树搜索代价）且对噪声目标有正则作用；NN 有多输出原生能力，可直接学全目标**。两者并存还能提供集成多样性（#13 明确两者互补）。置信度：中高。

### 分歧二：是否使用伪标签

3rd：两阶段伪标签是升到第 3 的关键（第一阶段自评"若停在这里就不是第三"）；
#13：伪标签在 SMILES-NN 上"not giving significant boost"，未进最终 blend；NN 版本用伪标签得 0.571 但未选入；
1st/2nd：未用。

**裁决**：伪标签收益与模型/流程强相关（3rd 用 20 模型 + 中位 + 裁剪把它做稳），不是通用增益。置信度：中。

### 分歧三：评测协议本身（#13 的"元批评"）

#13：MRRMSE + Limma log-p 对离群值过度敏感 → 榜单易探、赛后出现"乘 1.2"的套利解 → 建议先重设评测再谈生产化；
其他队：在协议内竞速（探针/融合）。

**裁决**：这是"指标选择 → 竞争行为"的经典案例：可被尺度平移利用的指标会诱导探针与套利；学习者的正确动作是**先读指标代码与数据预处理，再决定建模策略**（与 L37/先读指标同族）。置信度：中（#13 单队长文，但逻辑自洽且有赛后现象佐证）。

## 4. 增量数字账

| 动作 | 数字 | 来源/榜单 |
| --- | --- | --- |
| #13 特征编码实验 | 目标编码 Quantile80：0.602→0.586（PyBoost/CatBoost 同向）；默认 Quantile50 明显差 | #13（public） |
| #13 almost-entire 重训 | PyBoost 0.584→0.577；MLP 0.580+→0.570+ | #13（public） |
| #13 排除 CD8 | 0.586→0.584（稳定复现） | #13（public） |
| #13 train duplication | NN 0.600+→0.580+；SMILES-NN 0.582→0.574 | #13（public） |
| #13 SMILES-NN | 公开基线 0.607 → 自己改造 0.574（私榜 0.766）；Lion > Adam | #13（public/private） |
| #13 多阶段 blend | 0.575 → 0.566 → 0.559 → 0.558（每步等权 0.5） | #13（public） |
| #13 多样性 | 预测相关 0.8–0.9 的模型加入 blend 一致带来 +0.006~0.01 | #13 |
| #13 赛后复盘 | solo PyBoost 私榜 **0.718**，优于原 top1 的 0.728 | #13（private） |
| #13 CV-LB | local row-corr ≈0.5；local MRRMSE ≈0；NK 0.2+、CD8 为负；random folds 不劣于逻辑切分；public-private 相关 **0.98** | #13 |
| 1st 特征演进 | BioWordVec 0.767（public）→ 调参 0.614 → Wikipedia 描述 0.656（更差） | 1st（public） |
| 1st 模型/融合 | GRU 私榜 0.733；1d-CNN 0.745；LSTM 0.839；0.25×LSTM+0.65×CNN = 0.725；0.25×LSTM+0.65×GRU = 0.723；全量数据 0.719 | 1st（private） |
| 1st 折间差异 | Fold1/3/5 验证 ≈0.86/0.86/0.90；Fold2/4 ≈1.19/1.15（主导细胞类型：CD8/Myeloid 最难） | 1st（local） |
| 1st 数据量鲁棒性 | 25%→0.946、50%→0.815、75%→0.769、100%→0.719（仍在下降，未饱和） | 1st（private） |
| 1st 损失权重 | MSE 0.32 / MAE 0.24 / LogCosh 0.24 / BCE 0.2；lr 1e-3（LSTM/CNN）、3e-4（GRU）；250 epoch | 1st |
| 2nd 组件 | 0.551（std+mean+聚类采样）/0.559（去罕见项）/0.575（聚类采样）/0.554（mean+随机采样去 std）；d=128；lr 1e-5、wd 1e-4；Lion+Huber | 2nd（public） |
| 3rd 流程 | 7 模型产 255 条伪标签 → 20 模型重训；每模型 10 次取中位；列 min/max 裁剪；1 小时 CPU 复现 | 3rd |
| 3rd 噪声鲁棒性 | 标签加 0.01×std 高斯噪声反而略涨；输入加噪完全失败 | 3rd |

**结构校验（2 处吻合）**

1. 1st 折间差异与细胞类型难度排序完全对齐：CD8/Myeloid 折 ≈1.15–1.19，其余 ≈0.86–0.90 ✓；
2. #13 的"几乎全量"重训逻辑与其固定 epoch 记述自洽（无早停才可换子集重训）✓。

## 5. 机制推演

**M1｜为什么通用表示赢过生物先验**：`(cell_type, sm_name)` 的信息量约等于两个类别 ID；BioWordVec/ChemBERTa 提供的是**分布式的术语/分子语义**，与下游回归共享结构；Wikipedia 长描述引入自然语言噪声（嵌入没在该噪声上预训练）；通路/PPI 先验则受数据库覆盖与批次效应污染。目标编码则是"从本数据直接估计的类别均值/方差"，几乎无外部假设。**三者优先级：目标编码 ≥ 预训练通用表示 > 手工先验**。

**M2｜为什么 TSVD 降维会涨分**：18211 个目标里大多数基因的 DE 信号弱、噪声占比高；低秩分解保留共享的"扰动响应因子"，舍弃目标间独立噪声。降维同时降低 boosting 的多输出搜索代价（#13 的 SketchBoost 解决的是同一瓶颈）。这与"目标噪声大时做结构化降维"的通用规律一致。

**M3｜"almost entire"重训为什么稳**：样本极少时，K 折早停会浪费 ~20% 数据；固定 epoch + 全量重训用满数据但只有一份模型；**"去掉 1–5% 样本的多个子集 + 多份模型平均"同时拿到数据量与 bagging 方差削减**。代价是不能早停，需要 CV 阶段先定预算——即"CV 定超参，提交用满数据"的解耦协议。

**M4｜BCE 在回归任务里为什么有用（1st）**：目标近似以 0 为中心的尖峰分布（图 4），大量值在 0 附近；MSE 在 0 附近梯度小，模型对"该为负却预测 0"不敏感（1st 的数值例子：MSE 0.010 vs BCE 0.694）。把输出经 sigmoid 映射到 (0,1) 后用 BCE，等价于对"接近 0 的错误"重新加权。**多损失加权 = 对目标值域不同区域施加不同形状的惩罚**。

**M5｜CV-LB 失配与公私榜 0.98 的共存**：CV 折与 LB 的**组成不同**（细胞类型难度/药物覆盖不同 → 绝对误差不可比），但 public 与 private 由同一数据生成过程采样（组成相似）→ 彼此高度相关。结论：CV 要"复制测试的结构"才有意义（3rd 的每折一种细胞类型 + 公/私测 sm_name 覆盖），而不是随机分组。

**M6｜指标敏感性的经济学**：MRRMSE 的平方项由少数大值目标主导；log-p 预处理的方差异质性放大了这一点。于是：① 榜单探针可用少数提交反推目标；② 常数缩放（×1.2）即可套利。**指标的"可操纵面"决定了竞赛行为**（#13 的元批评）。学习者的防御：复算指标、检查缩放不变性、警惕"只涨公榜"的改动。

## 6. 证据分级

| 断言 | 等级 | 说明 |
| --- | --- | --- |
| #13 全部技术数字 | 自述 + 大量公开 notebook/数据集/Blend 代码 | 中高（社区可复现，赛后 solo 0.718 有旁证） |
| 1st 分数链（0.767→0.614→0.719 等） | 自述 + GitHub | 中高 |
| 1st 折间差异与细胞类型难度 | 自述 + 两张图 | 中高 |
| 2nd 组件分与结构 | 自述 + notebook/GitHub | 中（未给总分） |
| 3rd 两阶段伪标签收益 | 自述（"否则不是第三"），无数值 | 中低 |
| CV-LB 统计（50+ 模型） | #13 自述 + 公开分析帖（正文未收录） | 中 |
| 榜单探针/×1.2 套利 | #13 转述 + 帖标题（457753/456943 未收录） | 中低（待补） |
| 小样本却稳定（公私 0.98） | #13 计算 + 全社区观察 | 中高 |

## 7. 边界条件与反事实

- **反事实 1**：若不富集输入（仅关键词）→ 1st 的 0.767 上限与"低于 0.600 需要非平凡方法"（#13 试 50+ 简单模型全部 >0.600）共同说明弱输入硬拟合的极限。
- **反事实 2**：若坚持早停 → 不能做 almost-entire 重训，#13 的核心增益（0.584→0.577、0.580→0.570）消失。
- **反事实 3**：若用随机 KFold 或以 local MRRMSE 选模 → 折间 0.86 vs 1.19 的组成偏差会误导选择（1st）；应复现测试结构（3rd）。
- **反事实 4**：若指标改为 log-fold-change / 更鲁棒的行级损失 → ×1.2 式套利与探针空间可能被关闭（#13 的建议性结论）。
- **边界**：结论适用于"极弱离散输入 + 超高维输出 + 小样本"的科学赛；目标编码依赖折内类别覆盖（25% 数据时 sm_name 覆盖不足，one-hot 无法运行——1st 实测）。

## 8. 悬案与失败学

**悬案**

1. **PYBOOST 的算法细节（SketchBoost）** 只在 #13 中概述，专帖(454700)与论文未收录——多目标 boosting 的实现是本场最重要的方法论产出。
2. **榜单探针争议**：Stop spoiling(457753)、Will there be a huge shakeup(456943)、奇怪数据观察(445883) 未收录；#13 提到"高公开分 notebook 被点名"的社区冲突。
3. #18 Py-boost predicting t-scores(458661,54 票) 未收录——同一方法的另一种目标表示（t-score）结果未知。
4. 3rd 的"最高 CV 对应最高私榜"缺少分数细节，无法复核。
5. 赛后"乘 1.2"与"1–2 天内出现超过 top1 的解"的具体来源与处理未收录。

**失败学（跨队合集）**

- 表示类：Wikipedia 描述嵌入（1st，更差）；SMILES 增强（#13/1st 均无提升）；生物先验通路特征（#13）；DrugBank 分组特征（#13 未完成）。
- 结构类：SMILES-NN 上的 LSTM/CNN 替代（#13）；一对一化合物 one-hot NN 极不稳定（public 0.599–0.620）。
- 训练类：early stopping 阻断全量重训（#13）；伪标签进 SMILES-NN 无增益（#13）；Huber loss（3rd）；标签归一化/标准化、chained regression、去噪数据集、去离群、只训易/难列（3rd）。
- 验证/治理类：以 local MRRMSE 选模（#13 量化其近零相关）；过度依赖公榜（本场探针/套利背景）。

## 9. 图表证据

> 路径相对本文件（`analysis/deep/`）：`../../intel/open-problems-single-cell-perturbations/bodies/<topic>_img/NN.png`

**图 1：1st 的 5 折训练曲线（折间难度悬殊）**（topic 459258）——`../../intel/open-problems-single-cell-perturbations/bodies/459258_img/01.png`

*读图结论*：Fold1/3/5 验证收敛在 ≈0.86–0.90；Fold2/4 停在 ≈1.15–1.19，且训练/验证差距更大。**同一模型同一数据，折间差异 0.3+**——随机折的 CV 无法用于选择。

**图 2：折内主导细胞类型与验证 MRRMSE**（topic 459258）——`../../intel/open-problems-single-cell-perturbations/bodies/459258_img/02.png`

*读图结论*：Treg 0.86 / B 0.86 / NK 0.90（易）；CD8 1.19 / Myeloid 1.15（难）。1st 由此提出"理想训练集应多放 CD8/Myeloid"，也解释了图 1 的折间差异。**细胞类型难度是 CV 设计的第一约束**。

**图 3：目标值分布近似以 0 为中心的尖峰**（topic 459258）——`../../intel/open-problems-single-cell-perturbations/bodies/459258_img/03.png`

*读图结论*：多基因目标密度高度集中在 0 附近、尾部延伸到 ±60。**这是 1st 在回归中加入 BCE 的理由**：MSE 在 0 附近几乎无梯度（0.010），BCE 能给出 0.694 级别的惩罚。

**图 4：1st 的数据量鲁棒性曲线**（topic 459258）——`../../intel/open-problems-single-cell-perturbations/bodies/459258_img/04.png`

*读图结论*：私榜分数随训练数据比例单调改善：25%→0.946、50%→0.815、75%→0.769、100%→0.719，且 100% 处尚未饱和。**"更多数据仍是最强杠杆"在本场依然成立**（也佐证 almost-entire 重训的价值）。

**图 5：目标列 range 直方图（MRRMSE 的离群敏感来源）**（topic 458750）——`../../intel/open-problems-single-cell-perturbations/bodies/458750_img/01.png`

*读图结论*：多数列 range 在 (4,50)，长尾到 120+；MRRMSE 的平方项被大 range 列主导 → 3rd 用"按列 std 标准化的 MSE"识别难/易基因。**指标对目标尺度的敏感性是建模与榜单行为的根源**。

**图 6：3rd 的自定义 CV 切分（细胞类型 × 药物覆盖）**（topic 458750）——`../../intel/open-problems-single-cell-perturbations/bodies/458750_img/05.png`

*读图结论*：每折包含一种细胞类型（NK/CD4/CD8/Treg）+ 仅公/私测出现的 sm_name（其余为 train/test/missing 覆盖图例）。**让 CV 复现测试的组成结构**，3rd 称"最高 CV 的提交拿到最高私榜"。

## 10. 对既有笔记/playbook 的修订点

1. `notes/science/open-problems-single-cell-perturbations.md` 升级（现为浅版）：补 6 篇作者/票数、四方案 × 10 维对照、数字账（Quantile80 0.602→0.586、almost-entire 0.584→0.577、0.558 blend、public/private 刻度提醒）与 6 张图证。
2. `playbook/science.md`（扰动/多目标回归节）增补：
   - **弱输入富集优先级**：目标编码 ≥ 预训练通用表示（ChemBERTa/SMILES）> 手工生物先验；
   - **18k 目标的两种处理**：TSVD（去噪+降本）与直接多目标（NN/PyBoost）；
   - **小样本训练协议**：固定 epoch、禁用早停、"almost entire"子集重训平均、train duplication；
   - **多损失加权**：对目标值域不同区域用不同形状的损失（含 BCE 用于近零目标的机制）；
   - **CV 设计要复现测试组成**（细胞类型/药物覆盖），而不是随机分组。
3. `playbook/00-通用方法论.md` 增补：**"CV 与提交准备解耦"**（CV 定超参 → 满数据重训）；**"指标可操纵面"**（缩放敏感性 → 探针/套利 → 先复算指标再建模）。
4. `analysis/THEORY.md`（Batch 4 收尾扩 v0.4）候选：
   - **L57｜弱输入富集优先级**：目标编码 ≥ 通用预训练表示 > 手工先验；证据 = 本场多队对照。
   - **L58｜高维噪声目标的结构化降维**：TSVD 去噪 + 多输出 boosting；证据 = #13 0.602→0.586、2nd std 特征有效。
   - **L59｜小样本提交协议：CV 与重训解耦**（固定 epoch + almost-entire 子集平均）；证据 = #13 两组数字 + 1st 数据量曲线。
   - **T15｜伪标签：流程放大 vs 边际无效**（3rd 两阶段 vs #13 匿名），与 T6 合并。

## 11. 出处

- 综合指南（65 票）：https://www.kaggle.com/competitions/open-problems-single-cell-perturbations/discussion/438859
- #13 U900/PYBOOST（65 票）：https://www.kaggle.com/competitions/open-problems-single-cell-perturbations/discussion/460858
- 1st（Jean Kouagou，50 票）：https://www.kaggle.com/competitions/open-problems-single-cell-perturbations/discussion/459258
- 2nd（49 票）：https://www.kaggle.com/competitions/open-problems-single-cell-perturbations/discussion/458738
- 3rd（33 票）：https://www.kaggle.com/competitions/open-problems-single-cell-perturbations/discussion/458750
- 评审奖提问：https://www.kaggle.com/competitions/open-problems-single-cell-perturbations/discussion/456239
- 缺口登记（未收录正文）：458661、454700、445883、457753、456943、440177、441550、458916 等
