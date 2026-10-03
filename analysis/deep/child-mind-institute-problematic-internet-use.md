# CMI Problematic Internet Use 深读：高方差评分下的稳健工程

> 赛事：Featured ｜ 主题 tabular（医疗 + 时序信号）｜ 3559 队 ｜ 代码赛 ｜ 指标 Quadratic Weighted Kappa（QWK）（2024-12-19 截止）
> 材料基础：`digests/child-mind-institute-problematic-internet-use.md`（8 节：1st/2nd/5th/7th/14th/16th/19th + QWK 目标验证帖）+ 2 张图
> 深读时间：2026-10（Tier A #27）

## 0. 一句话重述：这道题真正在考什么

题面是"用儿童活动数据预测问题性网络使用等级"，实际被考的是**在 QWK 这种"阶梯敏感 + 易过拟合"的指标下，把稳健性做到极致**：

1. **标签是人为离散化的连续分数**：官方标签 `sii`（0–3）由 PCIAT 总分按阈值切出 → 用连续总分做回归目标、在评估时再切档，比直接分类保留更多信息（1st/5th）；
2. **阈值优化是双刃剑**：QWK 的分数对切点极敏感；全局最大搜索（19th）、per-fold+百分位（7th）、固定临床阈值 [31,50,80]+10 分箱（5th）、嵌套 CV 后只做一次（16th）——**在 OOF/公开榜上调阈值会过拟合**（5th 亲历不一致）；
3. **缺失值是主战场**：IterativeImputer/Lasso 迭代插补（16th 消融：不做插补私榜 0.470→0.412）、按列语义定制策略（2nd 的 avg/max+1/"Null"）、train+test 联合拟合（14th）；
4. **高方差 → 多种子/多重复/多模型**：5 折 ×10 seeds 投票（7th/14th）、10–20 次 Repeated StratifiedKFold 调参（1st）、10×10 嵌套 CV（16th）、种子扫掠确认稳定性（16th：私榜 0.464–0.472）；
5. **伪标签 + 时序压缩**：unlabeled 数据比例大 → 集成伪标签（5th/7th）；parquet 时序 → KMeans 15 簇均值特征（5th）/统计特征（16th）/PCA（1st）/enmo 周末-时段聚合（14th）。

一句话：**这是一场"高方差下的选择纪律"比赛**——冠军自述"我如何中彩票"，19th 靠洗牌跳 2000+ 名；真正可复用的，是插补、目标工程、种子稳健性与"不追公开榜"的纪律。

## 1. 材料与角色

| 帖子 | 作者 | 票数 | 角色与独有信息 |
| --- | --- | --- | --- |
| [552638](https://www.kaggle.com/competitions/child-mind-institute-problematic-internet-use/discussion/552638)（1st，94 票） | Lennart Haupts | 94 | **"中彩票"自白**：5 模型投票集成；PCIAT 总分目标；Lasso 插补；PCA 15 维；分位数分箱；39 特征；Repeated CV 调参；忽略公开榜 |
| [535052](https://www.kaggle.com/competitions/child-mind-institute-problematic-internet-use/discussion/535052)（QWK 目标验证，89 票） | chumajin | 89 | 对照实验：多分类目标 CV 0.2643/公开 0.265 vs **自定义 QWK 目标 CV 0.45187/公开 0.401**——CV 提升大、公开提升小 |
| [552569](https://www.kaggle.com/competitions/child-mind-institute-problematic-internet-use/discussion/552569)（16th，42 票） | Jack (rsakata) | 42 | **最完整的稳健性证据**：10×10 嵌套 CV、种子扫掠表、插补消融（不做插补私榜 0.412）；自定义 QWK 只助 CV |
| [552712](https://www.kaggle.com/competitions/child-mind-institute-problematic-internet-use/discussion/552712)（2nd，32 票） | Aradhye | 32 | **按列语义定制插补**（数值=均值、整数类别=max+1、字符串="Null"）；20 折；CV 升公开降、私榜惊喜 |
| [552625](https://www.kaggle.com/competitions/child-mind-institute-problematic-internet-use/discussion/552625)（7th，31 票） | — | 31 | Tweedie 损失；伪标签；per-fold + 百分位阈值优化；5 折×10 种子投票；种子方差示例（0.4922 vs 0.4839） |
| [552513](https://www.kaggle.com/competitions/child-mind-institute-problematic-internet-use/discussion/552513)（19th，25 票） | Vladimir Demidov | 25 | 基线 notebook（DeepTables + IterativeImputer + 全局阈值搜索）→ 加 2 个 GBDT 投票：私榜 0.469、**洗牌跳 2000+ 名** |
| [552517](https://www.kaggle.com/competitions/child-mind-institute-problematic-internet-use/discussion/552517)（14th，20 票） | Laura Romar | 20 | **分类（非回归）模型**（源自 ICR 冠军 DNN）；train+test 联合插补；enmo 周末/时段聚合；全量训练；类别权重；10 seed 平均 |
| [552656](https://www.kaggle.com/competitions/child-mind-institute-problematic-internet-use/discussion/552656)（5th，14 票） | peyman | 14 | **KMeans 15 簇时序特征**；伪标签（3 GBDT+Lasso+NN）；固定阈值 [31,50,80]；加弱模型提公开却掉私榜 |

**材料缺口（未扩采，登记备查）**：17 条 write-up 标记中收录 8 节。

## 2. 逐方案对照矩阵

| 维度 | 1st Lennart | 2nd Aradhye | 5th peyman | 7th | 14th Laura | 16th Jack | 19th Vladimir |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 目标 | PCIAT 总分 → 转 sii | 原标签（CatBoost） | PCIAT + 10 分箱，固定阈值 | sii + Tweedie + 分类 | 分类（sii） | sii + 自定义 QWK LGBM | sii + 阈值全局搜索 |
| 插补 | **Lasso**（<40% 缺失特征） | **按列语义**（均值/max+1/"Null"） | 未强调 | 中位数（fold 内） | **IterativeImputer（train+test）** | **IterativeImputer** | IterativeImputer(max_iter=19) |
| 模型 | LGBM+2×XGB+CatBoost+ExtraTrees 投票 | CatBoost | GBDT+NN+Lasso + 时序 GBDT；硬投票 | LGBM+XGB（+分类）5×10 种子 | 分类 DNN（ICR 血统）+10 seed | LGBM（自定义 QWK 目标） | DeepTables NN+CatBoost+LGBM 投票 |
| 时序特征 | PCA 15 维 + 日夜掩码 | — | **KMeans 15 簇均值** | Polars 统计 | enmo 周末×时段 | parquet 特征 | 基线派生 |
| 验证 | 10 折分层 + 10–20 次重复调参 | 20 折 | 5 折固定种子 | 5 折×10 种子投票 | 10 seed 平均 | **10×10 嵌套 CV** + 种子扫掠 | 5 折 |
| 阈值处理 | 分层 binning | — | 固定 [31,50,80]（防过拟合） | per-fold + 百分位 + Optuna | — | 嵌套 CV 后**只做一次** | 全局最大搜索 |
| 结果 | 冠军（自述运气） | 私榜惊喜（CV 升公开降） | 私榜 4.81→4.77（加弱模型） | 第 7 | 14th | 私榜 0.469 稳定 | 私榜 0.469，跳 2000+ 名 |

## 3. 共识、分歧与裁决

### 共识一：缺失值插补是本场第一杠杆（有消融证据）

16th 的消融最硬：原版私榜 0.470 → 不做插补 **0.412**（−0.058）；1st 用 Lasso 迭代插补；2nd 按列语义定制（"CatBoost 不懂每列的含义"）；14th 把 IterativeImputer 拟合在 train+test 上；19th 的基线同样以 IterativeImputer 为核心。**方法各异，但都认为"插补质量 > 模型选择"。**

**裁决**：医学问卷类表格数据的缺失不是噪声而是结构；插补器（尤其迭代式/有监督式）必须进入主流程。置信度高。

### 共识二：连续目标 + 慎重的阈值处理优于直接分类

1st/5th：用 `PCIAT-PCIAT_Total` 连续分数做目标再切档；5th 明确"阈值优化导致过拟合与不一致，改用固定 [31,50,80]"；7th 的阈值在**每折训练数据**上优化并转成百分位；16th 在嵌套 CV 的总体预测上**只优化一次**；19th/基线用全局最大搜索（高风险）。

**裁决**：目标用连续分数（信息保留）；阈值优化的安全姿势 = "在折内/嵌套 CV 上做、转百分位、只做一次"，绝不能按公开榜反复调。置信度高。

### 共识三：QWK 的方差极大，稳健性 = 重复 + 多种子 + 多模型

1st：10–20 次 Repeated StratifiedKFold 调参；16th：10×10 嵌套 CV + 种子扫掠（私榜 0.464–0.472）；7th：5 折×10 种子投票（种子间投票分 0.4922 vs 平均 0.4839）；14th：10 seed 平均；19th：多数投票。冠军直言"选对 notebook 是运气"。

**裁决**：高方差比赛的"分数"应定义为**分布的稳健统计量**（多重复/多种子均值或投票），而不是单次分割的峰值。置信度高。

### 分歧一：回归 vs 分类

14th 用**纯分类** DNN（ICR 冠军血统）；7th 把分类模型放入回归集成；5th 主用回归 + 固定阈值；1st/2nd/16th 以回归为主。两种路线都有前排案例。

**裁决**：QWK 既可由回归+阈值实现，也可由分类的概率期望实现；重要的是与阈值策略配套（分类天然输出等级概率，回归需要切点）。置信度中。

### 分歧二：自定义 QWK 目标到底有没有用

QWK 验证帖：多分类目标 0.2643/0.265 → 自定义目标 0.45187/0.401（**CV +0.19、公开 +0.14**，但差距不对称）；16th 使用自定义目标：消融显示"只贡献 CV，不贡献私榜"（0.4810 vs 0.4884 CV；私榜 0.471 vs 0.470）。

**裁决**：自定义目标把 CV 拉得"更贴近指标"，但它对阈值/切点的依赖更强，容易产生 CV-私榜错位；**作为集成成员可用，作为唯一模型需警惕**。置信度中高（两家对照方向一致）。

## 4. 增量数字账

| 动作 | 数字 | 来源 |
| --- | --- | --- |
| 5th 的单模 CV（无时序） | LGBM 0.4643 / CatBoost 0.4590 / XGB 0.4615 / Lasso 0.43503 / NN 0.4412 | 5th 表 |
| 5th 的最终（自述口径） | CV 4.6 / 私榜 4.81（原文数字疑为 0.46/0.481 口径）；加弱模型后私榜 4.81→4.77 | 5th |
| 16th 的消融（嵌套 CV/公开/私榜） | 原版 0.4884/0.433/0.470；无 parquet 0.4821/0.442/0.464；**无插补 0.4726/0.423/0.438**；两者皆无 0.4602/0.440/0.412；无自定义目标 0.4810/0.436/0.471 | 16th |
| 16th 的种子扫掠（私榜） | 10 个种子 0.464–0.472（公开 0.432–0.447）——本场最完整的"稳定带宽"证据 | 16th |
| 19th | 基线 notebook CV 0.482/公开 0.448/私榜 0.459（≈60 名）→ 集成公开 0.458/私榜 **0.469**（19 名，+2000 位） | 19th |
| 7th 的种子方差 | 同模型不同种子：投票分 0.4922 vs 单模型平均 0.4839 | 7th |
| QWK 目标对照 | 多分类 0.2643/0.265 vs 自定义 0.45187/0.401 | 535052 |
| 1st 的规模 | 10 折；调参用 10–20 次重复；手工筛到 **39 特征**；PCA 15 维 | 1st |
| 2nd 的折数 | 5 → 20 折（收益递减后停止） | 2nd |

**可复算/结构校验（2 处吻合）**

1. QWK 验证帖的对照结构：同一份 5 折、同一模型，只换目标函数——CV 提升 0.187、公开提升 0.136，**两侧提升幅度不一致**（CV 更受益）本身就是要警惕的信号 ✓；
2. 16th 的种子扫掠：公开与私榜的分布中心（~0.44/~0.47）与其单次提交一致，说明其管道没有"单种子幸运" ✓。

## 5. 机制推演

**M1｜为什么连续目标更好**：sii 是把 PCIAT 总分按阈值切出的 4 档；直接分类丢失"离切点多远"的信息，而 QWK 恰好按距离平方惩罚错档——用连续分数回归保留了"接近切点"的梯度信息，再把切点交给阈值优化（1st/5th）。**序数标签的通用处理：回归到连续潜变量 + 评估时切档。**

**M2｜为什么插补是第一杠杆**：本场缺失比例高且与人群特征相关（漏填 = 低参与度信号）；迭代插补用交叉特征结构恢复缺失值，同时避免"删除行"造成的小样本损失；16th 的消融（−0.058 私榜）量化了这一杠杆远大于模型选择。**缺失即信息 + 迭代插补 = 一条完整的特征工程链。**

**M3｜阈值优化的过拟合机制**：QWK 的分数是切点的阶跃函数；在 OOF 上找全局最优切点会"记住"折内噪声的方向（尤其小样本 + 类别不平衡），在私榜上反转。稳健姿势：切点由**折内数据**估计并转移（7th）、用**百分位**表示（7th）、在嵌套 CV 总体预测上只做一次（16th）、或直接用临床阈值（5th）。

**M4｜为什么需要多种子投票**：5 折的分割本身是随机变量；单次 CV 的峰值包含"分割幸运"。多种子投票把预测变成多个分割模型的集成，既提高稳健性也平滑阈值敏感性（7th/14th/19th）。**高方差指标的比赛，集成对象不只是模型，还包括"数据分割"。**

**M5｜伪标签为何有效**：unlabeled 比例大且与训练同分布；用 GBDT+NN+Lasso 集成的软预测当标签，等于把无标签人群的结构注入训练（5th/7th）。风险是伪标签强化集成偏差——需只在原始标签上验证（5th 的明确做法）。

**M6｜为什么"选对提交"像中彩票**：公开/私榜子集小 + 分数台阶化 → 名次的排序由少量样本的匹配状态决定；本场出现 +2000 名的洗牌、冠军的"lottery"自述、2nd"CV 升公开降"——**在评测方差 >> 模型差异时，期望值最大化 = 多提交稳健版本，而非追求单次峰值**。

## 6. 证据分级

| 断言 | 等级 | 说明 |
| --- | --- | --- |
| 插补消融（无插补私榜 0.412） | **可读取（16th 表）** | 单次执行但量级巨大 |
| 种子扫掠（私榜 0.464–0.472） | **可读取（16th 表）** | 10 seeds，全报告 |
| QWK 目标对照 | **可读取（535052）** | 单折实验；CV/公开双列 |
| 5th 的单模 CV 表 | **可读取（图）** | 5 模型同折 |
| 5th 的最终 4.6/4.81 口径 | **存疑（登记）** | 数字与常规 0.46/0.48 量级不符，疑为笔误/内部尺度 |
| 1st 的流程描述 | **自述** | 无消融数字；"lottery"自白为诚实注脚 |
| 2nd/14th/19th 的流程 | **自述** | 2nd 的 CV-公开背离无解释（作者本人在问） |
| 7th 的种子方差示例 | **自述（单例）** | 投票 vs 平均的 0.008 差 |

## 7. 边界条件与反事实

- **前提**：QWK 对小样本的切点敏感 + 公开子集小 → 本场"运气"占名次的很大权重。换 AUC/MAE 等平滑指标，稳健性技巧的收益会显著缩小。
- **反事实（1st）**：若不换用 PCIAT 连续目标，其集成仍可能高分（其模型栈很强），但阈值空间会更难校准；若不忽略公开榜、反复按公开调参，洗牌风险更大。
- **反事实（19th）**：基线 notebook 单独≈60 名；加两个未调参 GBDT 投票 → 19 名（+2000 位）。**收益主要来自洗牌而非模型改进**——典型的高方差场次"期望值策略"案例。
- **反事实（5th）**：若不加弱模型（逻辑回归/决策树）保公开分，私榜会保持 4.81（按原文口径）；**为公开分加模型反而伤私榜**，说明"以公开/LB 一致性选模"在噪声指标下不可靠。
- **边界（14th 的 train+test 插补）**：在允许的代码赛机制下用测试特征改进插补是合法的转导学习；若规则禁止，需回退到折内插补。

## 8. 悬案与失败学

**悬案**

1. **5th 的 4.6/4.81 口径**（与私榜 0.48 量级存疑）与"put me in second place"的表述未解释；
2. **2nd 的 CV-公开背离原因**（作者本人在帖中发问，无解答）；
3. **QWK 自定义目标的机制**：为何 CV 受益远大于 LB（16th 与 535052 一致观察），缺少逐案分析。

**失败学**

| 失败 | 来源 | 教训 |
| --- | --- | --- |
| 在公开榜/单次 OOF 上做全局阈值搜索 | 19th/1st 的风险案例；5th 亲历 | 阈值优化极易过拟合；用折内/嵌套/固定阈值 |
| 按 CV/公开一致性加弱模型 | 5th | 私榜 4.81→4.77；噪声指标下"公开提升"可能是陷阱 |
| 单次 5 折调参 | 1st/16th 的对照 | 用 Repeated CV（10–20 次）或嵌套 CV |
| 依赖 CatBoost 自动处理缺失 | 2nd | 模型不能理解列语义（有序 vs 无序整数） |
| 直接分类 sii 粗标签 | 1st/5th 的对照 | 丢失切点距离信息；连续目标更好 |
| 自定义 QWK 目标当万能药 | 16th/535052 | CV 大涨、私榜不涨甚至更差 |
| 相信单种子分数 | 7th 的方差示例 | 多种子投票才是"分数" |

## 9. 图表证据

> 路径相对本文件（`analysis/deep/`）：`../../intel/child-mind-institute-problematic-internet-use/bodies/552656_img/NN.ext`（本场仅 2 张图）

**图 1：5th 的完整管线（时序聚类 + 伪标签 + 硬投票）**（topic 552656）——`../../intel/child-mind-institute-problematic-internet-use/bodies/552656_img/01.png`

*读图结论*：parquet 时序 → KMeans 15 簇 → 每用户 15 维活动特征；unlabeled+labeled → GBDT+NN+Lasso 伪标签 → 与真实标签合并训练 → GBDT+NN+Linear Regressors 硬投票。**"时序压缩 + 伪标签 + 异质投票"三件套一图说清。**

**图 2：5th 的单模型 CV 表（不含时序的最终线）**（5th）——`../../intel/child-mind-institute-problematic-internet-use/bodies/552656_img/02.jpg`

*读图结论*：固定 5 折下 LGBM 0.4643 / XGB 0.4615 / CatBoost 0.4590 / NN 0.4412 / Lasso 0.43503——**树模型主导但线性/深度模型提供互补**，也解释其伪标签集成选择这五类模型的理由。

## 10. 对既有笔记/playbook 的修订点

1. `notes/tabular/child-mind-institute-problematic-internet-use.md` 升级：补齐 8 节作者/票数；方案谱系扩为 7 方案对照矩阵；新增插补消融、阈值优化三姿势、种子扫掠、QWK 目标陷阱、图证与失败学。
2. `playbook/tabular.md` 增补：
   - **序数目标回归化**（连续潜变量 + 折内阈值/百分位）；
   - **缺失值插补优先级**（迭代插补/有监督插补/按列语义策略；消融显示其权重高于模型选择）；
   - **高方差指标的稳健协议**（Repeated CV/嵌套 CV/多种子投票/种子扫掠报告）；
   - **QWK 类目标的警戒**（CV 与 LB 提升不对称即停）。
3. `playbook/00-通用方法论.md` 增补："**当评测方差 ≥ 模型差异时**"：把分数当分布而非点估计；多提交稳健版本；用期望值策略而非峰值策略（与 rogii 的三把尺子、ubiquant 的多轮口径同族）。

## 11. 出处

- 1st（Lennart Haupts，94 票）：https://www.kaggle.com/competitions/child-mind-institute-problematic-internet-use/discussion/552638
- QWK 目标验证（chumajin，89 票）：https://www.kaggle.com/competitions/child-mind-institute-problematic-internet-use/discussion/535052
- 16th（Jack，42 票）：https://www.kaggle.com/competitions/child-mind-institute-problematic-internet-use/discussion/552569
- 2nd（Aradhye，32 票）：https://www.kaggle.com/competitions/child-mind-institute-problematic-internet-use/discussion/552712
- 7th（31 票）：https://www.kaggle.com/competitions/child-mind-institute-problematic-internet-use/discussion/552625
- 19th（Vladimir Demidov，25 票）：https://www.kaggle.com/competitions/child-mind-institute-problematic-internet-use/discussion/552513
- 14th（Laura Romar，20 票）：https://www.kaggle.com/competitions/child-mind-institute-problematic-internet-use/discussion/552517
- 5th（peyman，14 票）：https://www.kaggle.com/competitions/child-mind-institute-problematic-internet-use/discussion/552656
- 未收录缺口（登记备查）：17 条 write-up 标记中的其余条目
