# NeurIPS Open Polymer 2025 深读：单性质标签事故 × 偏移探针 × 外部数据治理

> 赛事：Featured ｜ 主题 science（聚合物性质预测）｜ 2240 队 ｜ 代码赛 ｜ 指标：open_polymer_2025（5 性质加权 MAE，wMAE，越低越好）
> 材料基础：`digests/neurips-open-polymer-prediction-2025.md`（6 篇：1st/8th/2nd/20th/3rd + 材料帖；120 条讨论索引）+ 3 张图（607947×1 / 608069×2）
> 深读时间：2026-10（Tier A #38）

## 0. 一句话重述：这道题真正在考什么

题面是"由聚合物 SMILES 预测 5 个性质（Tg、FFV、Tc、Density、Rg）"，实际被考的是**一场数据质量事故中的排名博弈**：

1. **Tg 的测试标签系统性偏移**：多名选手独立发现——公榜加 +273.15（开尔文/摄氏度错觉）、再试 +300、+30、+40 都能涨分（2nd）；1st 用提交扫出 V 形曲线拟合最优常数偏移（+0.5644×std）；偏移在私榜更强。2nd 的赛后结论："尽管有 5 个性质，比赛名次由一个性质的分布偏移决定。"
2. **偏移的处理方式成为主变量**：1st 拟合偏移并保留一份 raw 提交对冲；2nd 激进搜参（+40，赛后发现 (9/5)x+32 私榜 0.068 优于 1st）；8th 明确"不做 Tg 后处理"仍拿第 8；3rd/20th 用常规线性校准/分布匹配。
3. **外部数据全是脏的**：1st 用五策略（isotonic 重标、误差过滤、样本加权、手工规则、stacking）清洗六个外部数据集；8th 用 91 个重叠 SMILES 发现 POINT2 的 Tg 系统性低 ~20°C（+20 校正）、Density 偏 0.118——**重叠样本差值分析是外部数据的第一动作**。
4. **通用预训练模型碾压化学专用模型**：同队同流程对照——ModernBERT-base 0.0584 / CodeBERT ~并列最佳 / ChemBERTa 0.0634 / polyBERT 0.592；ModernBERT-large（0.0587）反而比 base 差。
5. **BERT 线的三件套**：PI1M 50k 伪标签上的成对排序预训练（+0.004 LB / +0.01 CV）、随机 SMILES 增强 ×10、TTA 50 次取中位（+0.01 LB）；表格线则被 AutoGluon（best preset，2h/性质）以约 1/20 算力打败手工调参集成 ~2% wMAE。

一句话：**这是一场"数据事故 + 探针套利"的比赛**——建模水平的分差被一个性质的标签 bug 淹没；同时暴露了"外部数据许可与规则"的治理真空。

## 1. 材料与角色

| 帖子 | 作者 | 票数 | 角色与独有信息 |
| --- | --- | --- | --- |
| [607947](https://www.kaggle.com/competitions/neurips-open-polymer-prediction-2025/discussion/607947) 1st | jsday96 | 116 | BERT/AutoGluon/Uni-Mol 集成；**Tg 偏移探针**（V 曲线 + 0.5644×std）；PI1M 伪标排名预训练；外部数据五策略；1116 组 MD 模拟特征；去重（canonical SMILES + Tanimoto 0.99 防泄漏）；双提交对冲；全部代码公开 |
| [585022](https://www.kaggle.com/competitions/neurips-open-polymer-prediction-2025/discussion/585022) Jump-start | — | 106 | 材料信息学背景与起步材料（数据/思路） |
| [608069](https://www.kaggle.com/competitions/neurips-open-polymer-prediction-2025/discussion/608069) 8th | — | 36 | **拒绝 Tg 后处理**；POINT2 的 Tg +20 校正（91 重叠 SMILES 差值图）、Density −0.118；Butina 聚类 + 0.9 Tanimoto 禁选防泄漏；Mordred+指纹特征；TabM×0.7+XGB×0.3；外部数据规则的公开质疑 |
| [608984](https://www.kaggle.com/competitions/neurips-open-polymer-prediction-2025/discussion/608984) 2nd | — | — | 黑盒公榜集成 + Tg 偏移搜索（+273.15→+300→+30→+40）；赛后发现 **(9/5)x+32 → 私榜 0.068（优于 1st）**、(9/5)x+45 → 0.066；ExtraTrees + 变换即可打平最终提交；"名次由单性质偏移决定" |
| [607803](https://www.kaggle.com/competitions/neurips-open-polymer-prediction-2025/discussion/607803) 20th | — | 32 | 公榜只占测试 8% → 押 CV（0.0436）；1072 特征；逐目标自动权重（XGB/KNN/Cat/Hist/ET/LGB）；Tg mean matching、FFV mean+std matching；私榜 0.085 |
| [607991](https://www.kaggle.com/competitions/neurips-open-polymer-prediction-2025/discussion/607991) 3rd | hongyu Guo | — | 新手：GATv2（8 头/384 维/6 层/残差）+ 逐目标 F-regression 选 Top-50 Morgan bits；链延伸增强；wMAE 自定义损失；两阶段训练+refit；线性校准 **+5.47%**（0.080→0.078）；赛后 RemoveHs 单模型 ~0.083 |

**材料缺口（受"不扩采"约束，登记备查）**：587318 "Data to reach 0.037 on LB"(74 票)、**607784 "Strongly recommend removing Tg and recalculating the scores to rescue"(71 票)**、585884 竞赛更新(58)、588643 数据更新(46)、607769 "Why shakeup? Why Domain Shift? Some Bugs?"(36)、608250 "Potential NeurIPS Code of Ethics violation"(33)、593755 "reverse engineer train data"(29)、607778 "Rerun? BUG? data leak?"(28)——**Tg 事故的官方说明与伦理争议帖全部未收录**，是本次深读最大缺口。

## 2. 逐方案对照矩阵

| 维度 | 1st jsday96 | 2nd | 3rd hongyu Guo | 8th | 20th |
| --- | --- | --- | --- | --- | --- |
| Tg 偏移处理 | 扫参拟合 V 曲线 → +0.5644×std；另一份 raw 对冲；私榜 0.075 | 试 +273.15/+300/+30/+40 → 取 +40；赛后 (9/5)x+32 = 0.068 | 常规线性校准（每目标 y=ax+b） | **不处理**（标题即宣言） | mean matching |
| 外部数据 | 6 个数据集 + 自跑 MD；五策略清洗 | 未展开（黑盒公榜集成） | 未展开 | POINT2 +20 / Density −0.118 校正 | POINT2 启发的特征 |
| 表示/模型 | ModernBERT/CodeBERT + AutoGluon + Uni-Mol 2 84M | 公榜 notebook 黑盒集成 + 后处理搜索 | GATv2 + Morgan Top-50 | Mordred + 指纹；TabM×0.7 + XGB×0.3 | 1072 特征 + 6 类 GBDT/KNN 逐目标加权 |
| 损失/训练 | 回归 + 排名预训练；随机 SMILES ×10；TTA 50 中位 | 不展开 | wMAE 自定义损失；两阶段（找 epoch→全量 refit） | 逐目标 TabM 配置 | 逐目标权重自动搜索 |
| 验证/去泄漏 | 训练=100% 外数据+80% 主办数据；canonical 去重 + Tanimoto 0.99 | 未展开 | 5 折（有偏数据被校准缓解） | Butina 聚类 + >0.9 相似样本禁入训练折 | Stratified 5 折（等频分箱，与公榜最相关） |
| 集成 | 4 系 × 5 目标 = 20 模型 | 公榜集成 | 5 折平均 | TabM+XGB 加权 | 逐目标自动权重 |
| 成绩（同榜比较） | 集成 PP 前 0.058/0.089 → PP 后 0.054/**0.075** | 赛后变换私榜 0.068/0.066 | 校准后 PB 0.078 | 8th（无 PP） | CV 0.0436 / pub 0.065 / priv 0.085 |

## 3. 共识、分歧与裁决

### 共识一：Tg 测试标签存在系统性偏移（5/5 独立确认，处理方式各异）

1st：扫偏系数 → V 形曲线，p<0.01 排除噪声；
2nd：+273.15/+300/+30/+40 阶梯 → 赛后 (9/5)x+32；
3rd：OOF 显示"低估高 Tg、高估低 Tg"→ 线性校准 +5.47%；
8th：明确不处理 Tg（认为外部数据偏移是常态，检验后拒绝套利）；
20th：mean matching。

**裁决**：偏移真实存在且私榜更强（1st/2nd 的赛后数据一致）；**"检测到偏移"是共识，"利用到什么程度"是风险选择**。若比赛期间采用 2nd 赛后的 (9/5)x+32，私榜 0.068 将优于 1st 的 0.075——但当时无法验证该变换的机制正确性。把"偏移量估计"与"物理/单位解释"分开下注（1st 留 raw 对冲）是最稳健的工程姿态。置信度：高（多队独立 + 图上证据）。

### 共识二：外部数据必须先做重叠样本差值分析（1st/8th 都做，2nd/3rd/20th 受益）

8th：91 个重叠 SMILES 的 Tg 差值分布 → POINT2 系统性低 >20°C（+20 校正）；Density −0.118；
1st：isotonic 重标 + 误差过滤 + 样本加权 + 手工规则 + stacking；
20th：POINT2 启发的特征工程。

**裁决**：外部数据集的**标签尺度/口径**与其覆盖一样重要；"同一分子在两份数据中的标签差"是估计系统误差的直接证据（与 HuBMAP 的 dilation 试纸、godaddy 的 census 口径同族）。置信度：高。

### 共识三：通用预训练语言模型 > 化学专用模型（1st 的系统对照；3rd/20th 用 GNN/表格作对照面）

1st 同流程对照：ModernBERT-base **0.0584**、ModernBERT-large 0.0587（更大更差）、ChemBERTa 0.0634、polyBERT **0.592**；CodeBERT 与 ModernBERT 并列最佳；DeBERTa 系列同样不佳。

**裁决**：在小数据化学回归上，**预训练语料的规模/多样性与 tokenizer 匹配度比"领域专用"标签更重要**；SMILES 的随机化增强（非规范 SMILES ×10）弥补了通用 tokenizer 对化学记法的适配。置信度：中高（单队但为同流程大差距对照）。

### 共识四：后处理分布校准是低成本确定收益（3rd/20th/1st/2nd 的共识面）

3rd：线性校准 +5.47%（PB 0.080→0.078）；
20th：Tg mean matching / FFV mean+std matching；
1st：偏移拟合；
2nd：变换搜索。

**裁决**：在 wMAE 类指标下，"把预测分布对齐到训练/已知目标分布"几乎总能小幅涨分；但本场它被放大成主变量，因为偏移来自标签事故而非模型缺陷。置信度：高。

### 分歧一：偏移利用的程度 vs 保守

1st：拟合最优但要留 raw 对冲（"其他提交都带偏移"）；
2nd：激进（+40），赛后证明还可以更优；
8th：拒绝利用（"No Tg Post Processing"）仍第 8；
3rd/20th：常规校准。

**裁决**：在"数据 bug 未知是否会在私榜修复"的不确定性下，**对冲（两份提交）+ 保守校准**给出更稳的期望；激进利用只有在私榜同样损坏时才占优（本场恰好如此）。这也牵出伦理问题（608250 的 Code of Ethics 投诉、607784 的"移除 Tg 重算"倡议）——利用主办方数据缺陷是否越界，社区无共识。置信度：中。

### 分歧二：模型路线的贡献被事故稀释

2nd 的观察：公榜前排水位差距小、复杂模型不比简单好；其 ExtraTrees + 变换即可打平最终提交；
8th：GBDT（CatBoost/LGBM）折间方差大 → 弃用，TabM 为主；
1st：BERT/AutoGluon/Uni-Mol 三线仍有效（PP 之前 0.058）。

**裁决**：低信噪比 + 标签事故下，**模型差异被淹没，清洗/校准/规则理解成为主要分差来源**（与 godaddy "先修口径再修模型"同族）。置信度：中高。

### 分歧三：外部数据使用的合规性（8th 的公开质疑）

8th："No license ≠ free to use"；PI1M 等学术用途数据；组织者对规则询问长期沉默；"几乎所有队伍都违反了……或都没违反（取决于组织者解释）"。

**裁决**：这是竞赛治理问题，不是技术问题；学习者的正确动作是**先确认数据许可与规则，再做技术选型**；把"组织者沉默"当作默认允许是高风险行为。置信度：中（单方陈述 + 未收录官方回应）。

## 4. 增量数字账

| 动作 | 数字 | 来源 |
| --- | --- | --- |
| 1st 单模型（public/private） | ModernBERT 0.059/0.089；CodeBERT 0.058/0.090；AutoGluon 0.062/0.091；Uni-Mol 0.062/0.091 | 1st |
| 1st 集成与后处理 | PP 前 0.058/0.089 → PP 后 0.054/**0.075** | 1st |
| 1st 偏移探针 | 扫 ±0.1σ 起步；V 曲线拟合最优系数 **0.5644**；私榜曲线在系数 1.0–1.5 更低（约 0.069） | 1st（图 1） |
| 1st 伪标预训练 | PI1M 50,000 假想聚合物，多任务成对排序；相对 HuggingFace 权重 +0.004 LB / +0.01 CV；5 个第三方基础模型全部受益；微调后部分超过教师 | 1st |
| 1st 增强/TTA | 随机 SMILES ×10（±30% 内最优）；TTA 50 次取中位（+0.01 LB，早期实验） | 1st |
| 1st 基础模型对照（CV wMAE） | ModernBERT-base 0.0584；large 0.0587；ChemBERTa 0.0634；polyBERT 0.592 | 1st |
| 1st 外部数据五策略 | isotonic 重标（权重按数据集 tuning）、误差过滤（阈值按 MAE 比值）、样本加权、手工规则（RadonPy Tc>0.402 删除）、对 MD 数据用 41×XGBoost stacking | 1st |
| 1st MD 数据 | 1,116 组模拟；RadonPy+LAMMPS；自动构象配置选择；41 个仿真特征对表格 CV 增益 ~0.0005 wMAE；3/5 目标保留全部、Density/Rg 全弃 | 1st |
| 1st 去泄漏 | canonical SMILES 去重；训练-测试 Tanimoto >0.99 剔除（承认源于一个 bug 引起的过度谨慎） | 1st |
| 2nd 偏移阶梯 | +273.15 → +300 → +30 → +40（赛中最佳）；赛后 (9/5)x+32 = 私榜 **0.068**；(9/5)x+45 = **0.066**；ExtraTrees+变换 = 0.077 | 2nd |
| 8th 外部校正 | POINT2 Tg **+20**（91 个重叠 SMILES）；Density **−0.118**；Mordred+指纹特征数：Tg 789 / FFV 836 / Tc 520 / Density 423 / Rg 654；Butina+0.9 相似过滤 | 8th（图 2） |
| 3rd GNN/校准 | GATv2 8 头、384 维、6 层；Top-50 Morgan bits/目标；线性校准 **+5.47%**（PB 0.080→0.078）；RemoveHs 赛后单模型 ~0.083 | 3rd |
| 3rd 训练 | wMAE 自定义损失；两阶段（早停找 epoch → 全量 refit）；batch 64 最优（128/256 更差） | 3rd |
| 20th | CV 0.0436 / pub 0.065 / priv 0.085；1072 特征；逐目标权重（如 Tg：xgb 0.789/knn 0.112/cat 0.052…）；公榜只占测试 **8%** | 20th |

**结构校验（2 处吻合）**

1. 2nd 的赛后结论与 1st 的私榜曲线一致：私榜最优偏置大于公榜（1st 图 1 中私榜在 1.0–1.5 平坦、公榜最优 ~0.56）✓；
2. 8th 的重叠 SMILES 差值分布（峰值 +20~+40）与其 "+20 校正" 叙述方向一致 ✓。

## 5. 机制推演

**M1｜V 形探针的统计逻辑**：若标签被常数 b 污染，则把预测整体加 k 后的分数 S(k) 在 k=b 处最优；S(k) 在最优两侧近似线性且有相同斜率量级（1st 的拟合假设）。用少数提交点拟合 V 形 → 反推 b。1st 的关键不是拟合本身，而是**先做显著性判断**（p<0.01）排除"稀疏标签的随机波动"解释，再投入资源搜索。

**M2｜为什么单性质污染能决定总名次**：wMAE 对 5 性质等权平均（或按行加权）；Tg 的标签整体平移使该性质误差从"可接受"跳到"灾难级"，其余 4 个性质无论多好都无法补偿。**多目标指标的平均结构 + 单目标标签事故 = 排名被单点支配**；诊断时应逐目标看预测-标签关系（1st 的 ±0.1σ 扫描、3rd 的 OOF 线性校准图）而非只看总分。

**M3｜物理变换 vs 纯拟合**：2nd 的 (9/5)x+32 是摄氏→华氏；赛后该变换比常数 +40 更优（0.068 vs 0.075 级别），说明数据生成管道里可能存在**单位/换算类的结构性错误**。方法论：发现偏移后先问"它像哪种已知变换"（单位、坐标、对数），再退化为常数搜索——结构性解释通常给出更好的外推（私榜更严重时依然有效）。

**M4｜为什么通用模型赢**：SMILES 回归需要 tokenizer 处理非自然语言的化学记法；化学专用预训练语料小（ChemBERTa/polyBERT 的表示空间覆盖窄），而 ModernBERT/CodeBERT 的大规模多语料（含代码）提供了更通用的字符级/片段级表示。随机 SMILES 增强（同一分子的多种写法）相当于对 tokenizer 做数据侧的"记法不变性"训练，进一步弥合领域差距。polyBERT 0.592 的灾难提示其 tokenizer 与"未预处理 SMILES"不兼容。

**M5｜伪标签排名预训练为什么强于回归蒸馏**：直接回归伪标签会继承教师集成的数值噪声；成对排序（哪两个聚合物性质更高）+ 忽略相近对，把监督变成**对噪声更鲁棒的顺序信号**，并且天然是多任务（5 性质共享一个编码器）。微调后超过教师 = 学生从"排序结构"里提取了教师未显式表达的规律。这也解释了 +0.01 CV 的稳定增益。

**M6｜AutoGluon 的性价比**：表格特征确定后，AutoGluon 的模型库+多层堆叠+调参自动化把"人工集成工程"压缩成预设；本场 best preset（2h/性质）≈ 手工 20× 算力还差 ~2%。启示：**先跑 AutoGluon 建立基线，再把精力投到特征/数据/表示上**，而不是手工堆 GBDT。

**M7｜外部数据治理的灰色地带**：8th 的质问揭示三层问题——① 组织者对"什么可用"长期沉默；② "No license" 不等于可自由使用；③ 学术用途数据（PI1M）混入竞赛训练的合规性未定义。技术最优（用外部数据）与合规最优（只用官方数据）在本场发生冲突；学习者应把这视为**风险预算**问题：先查许可、留存来源记录，再决定用不用。

## 6. 证据分级

| 断言 | 等级 | 说明 |
| --- | --- | --- |
| Tg 测试标签偏移 | **多队独立 + 图证 + 赛后私榜曲线** | 高 |
| 1st 探针系数与对冲 | 自述 + 图 1 + 赛后私榜（0.075）| 中高 |
| 2nd 的 (9/5)x+32 → 0.068/0.066 | 自述（赛后，同榜可核） | 中高 |
| 8th 的 +20/−0.118 校正 | 自述 + 91 重叠样本图 | 中高 |
| 通用模型 > 化学模型（1st 对照） | 自述数字（同流程，无第三方复现） | 中高 |
| 伪标排名预训练增益（+0.004 LB/+0.01 CV） | 自述 | 中 |
| AutoGluon 打败手工集成 ~2% | 自述（无配置细节） | 中 |
| MD 仿真特征 +0.0005 wMAE | 自述 | 中低 |
| 外部数据合规争议 | 8th 单方陈述 + 伦理帖标题（未收录） | 中（事实层面） |

## 7. 边界条件与反事实

- **反事实 1**：若 Tg 标签完好 → 名次由表示/集成/校准的常规差异决定；2nd 的"ExtraTrees + 变换即可打平"说明当前分差被事故压缩。
- **反事实 2**：若选手中途没有探针工具（或规则禁止多次提交）→ 1st/2nd 的偏移拟合无法实施；8th 的保守路线（第 8）表明不利用也能留在前排。
- **反事实 3**：若用化学专用基础模型且不换 → 1st 的对照显示 CV 差 0.005+（ChemBERTa）到 0.53（polyBERT）。
- **反事实 4**：若外部数据不做重叠校正 → Tg 训练目标与主办标签差 ~20°C、Density 差 0.118，模型系统性偏移。
- **边界**：结论适用于"多目标平均指标 + 主办数据事故 + 外部数据规则模糊"的赛制；其中"偏移探针""重叠差值校正""对冲提交"可迁移，但**探针的合规性因平台规则而异**（参考 open-problems-multimodal 的作弊/泄漏案例）。

## 8. 悬案与失败学

**悬案**

1. **官方对 Tg 数据事故的说明、私榜是否修正、是否重赛**：相关帖（585884/588643/607784/607778/607769）全部未收录。
2. **伦理争议（608250，Code of Ethics）结论未知**：利用探针拟合数据 bug 是否违规，社区无共识。
3. 587318 "Data to reach 0.037 on LB"(74 票) 未收录——公榜低分区间的方法未知。
4. 1st 的 D-MPNN/GMM 增强失败无数字；polyBERT 0.592 的机制解释缺失。
5. 外部数据许可的官方界定始终未给出（8th 明确指出组织者沉默）。

**失败学（跨队合集）**

- 表示类：化学专用基础模型（ChemBERTa/polyBERT）；更大的 ModernBERT-large；DeBERTa 系列；D-MPNN（1st）。
- 增强类：GMM 数据增强（1st）；Isomer generation（3rd，无效）；Kukulized/去立体化学等 SMILES 变体（1st，无效）。
- 训练类：大 batch（3rd 的 64 最优）；把 RDKit descriptors 喂给 GATv2（3rd，伤害）；NNConv 则相反（协同差异）。
- 数据类：外部数据不校正（Tg/−20°C、Density 0.118）；不查许可证（治理风险）。
- 模型选择类：CatBoost/LGBM 折间方差大（8th 弃用）；复杂模型在低信噪比下无优势（2nd 的观察）。

## 9. 图表证据

> 路径相对本文件（`analysis/deep/`）：`../../intel/neurips-open-polymer-prediction-2025/bodies/<topic>_img/NN.ext`

**图 1：1st 的偏置-分数曲线（公榜 V 形 vs 私榜更宽偏移）**（topic 607947）——`../../intel/neurips-open-polymer-prediction-2025/bodies/607947_img/01.png`

*读图结论*：横轴=常数偏移系数（×预测标准差），纵轴=LB 分数（越低越好）。公榜（橙）在 ≈0.55–0.6 处最低（0.054），两侧近线性上升；私榜（蓝）从 0 的 0.085 单调下降到 1.0–1.5 的 ~0.069 平台，2.0 时才回升。**私榜最优偏移远大于公榜**——直接证明偏移在私榜更严重，也解释了 1st 选 0.5644 是"公榜最优但私榜次优"的折中。

**图 2：8th 的重叠 SMILES Tg 差值分布（外部数据校正依据）**（topic 608069）——`../../intel/neurips-open-polymer-prediction-2025/bodies/608069_img/01.png`

*读图结论*：91 个同时存在于 POINT2 与主办数据的 SMILES，其 Tg 差值分布峰值在 +20~+40、带 ±100 以上离群。**"外部 vs 主办"重叠样本差值分析是外部数据校正的标准动作**（8th 据此 +20；密度 −0.118）。

**图 3：8th 的最终模型策略（TabM×0.7 + XGBoost×0.3）**（topic 608069）——`../../intel/neurips-open-polymer-prediction-2025/bodies/608069_img/02.PNG`

*读图结论*：极简结构——TabM 与 XGBoost 按 0.7/0.3 加权（逐目标不同 TabM 配置），无复杂集成。**在标签事故环境下，简单模型 + 保守后处理足以进入前 10**；与 2nd "复杂模型不比简单好"的观察互证。

## 10. 对既有笔记/playbook 的修订点

1. `notes/science/neurips-open-polymer-prediction-2025.md` 升级：补 6 篇作者/票数、五方案 × 8 维对照、数字账（0.5644、+20/−0.118、0.068/0.066、+5.47%、AutoGluon 2h vs 20× 算力）与 3 张图证；新增"数据事故与治理"节。
2. `playbook/science.md`（材料/化学节）增补：
   - **外部数据三步**：重叠样本差值 → 尺度/口径校正 → 样本加权/过滤；记录来源与许可；
   - **化学表示选择**：先试通用预训练模型（ModernBERT/CodeBERT）与随机 SMILES 增强，不要默认领域专用模型；大模型未必更好；
   - **伪标签排名预训练**（成对排序 + 忽略相近对）作为回归蒸馏的鲁棒替代；
   - **表格默认基线**：AutoGluon best preset 先跑，再决定手工集成投入。
3. `playbook/00-通用方法论.md` 增补：**"单目标污染可以支配多目标平均指标"**（逐目标审计预测-标签关系）；**"偏移探针的 V 形拟合 + 对冲提交"**（附合规警示）；**"数据许可与规则先行"**。
4. `analysis/THEORY.md`（Batch 4 收尾扩 v0.4）候选：
   - **L60｜外部数据重叠差值校正**：证据 = 本场（+20/−0.118）+ HuBMAP dilation 试纸 + godaddy census 口径；
   - **L61｜多目标指标的单点支配**：一个被污染的列可以吞掉其余四列的优势；
   - **T16｜偏移利用 vs 保守对冲**：1st/2nd（利用）vs 8th（拒绝）；裁决 = 私榜未知时对冲 + 保守校准，附伦理边界；
   - **L62｜弱数据领域先试通用预训练模型**：证据 = 本场基础模型对照。

## 11. 出处

- 1st（jsday96，116 票）：https://www.kaggle.com/competitions/neurips-open-polymer-prediction-2025/discussion/607947
- Jump-start（106 票）：https://www.kaggle.com/competitions/neurips-open-polymer-prediction-2025/discussion/585022
- 8th（36 票）：https://www.kaggle.com/competitions/neurips-open-polymer-prediction-2025/discussion/608069
- 2nd：https://www.kaggle.com/competitions/neurips-open-polymer-prediction-2025/discussion/608984
- 20th（32 票）：https://www.kaggle.com/competitions/neurips-open-polymer-prediction-2025/discussion/607803
- 3rd（hongyu Guo）：https://www.kaggle.com/competitions/neurips-open-polymer-prediction-2025/discussion/607991
- 缺口登记（未收录正文）：587318、607784、585884、588643、607769、608250、593755、607778 等
