# OTTO 推荐系统深读：候选工程决定 95% 的分数

> 赛事：Featured ｜ 主题 tabular（recsys）｜ 2574 队 ｜ 标准赛 ｜ 指标 WeightedRecall@20（clicks 0.10 / carts 0.30 / orders 0.60）
> 材料基础：`digests/otto-recommender-system.md`（7 节正文：GBT Ranker 教程 + 大数据推荐概念 + 规则第 3 + 第 5 + 3rd(imaginary) + 2nd(ONODERA) + 20th）+ 14 张图
> 深读时间：2026-10（Tier A #14）
> **重要缺口**：本仓未收录 1st place 正文（[384022，207 票](https://www.kaggle.com/competitions/otto-recommender-system/discussion/384022)）。本深读的全部结论来自 2/3/5/20 名与教程帖；"冠军方法"未经一手材料验证。

## 0. 一句话重述：这道题真正在考什么

题面是"预测会话接下来会交互的商品（三目标加权召回@20）"，实际被考的是**在 12.9M 会话 / 2.16 亿事件的规模上，把"候选生成工程"做到极限**，排序模型只在最后加一点点。降解为 5 步：

1. **候选生成 = 本题本体**：共现矩阵（co-visitation）× 变体爆炸（动作对、方向、时间衰减、邻近距离、冷启动、时段）——Chris 用 20 个矩阵把"纯规则"推到 **LB 0.590**，再叠加 XGB 重排只涨 **+0.011**；5th 的候选生成器自排序就已经 0.585（最终 0.604）。**召回上限（0.65–0.68）锁死了所有后续增益的天花板**；
2. **Ranker 训练数据自造**：按时间窗构造（train=前 3 周 / valid=第 4 周切 A/B）、50–200 候选/会话、GroupKFold、per-target 标签——教程帖把这条流水线标准化成社区公共基线；
3. **跨目标结构**：click→cart→order 的意图递进 → "carts 预测作为 orders 的特征"是多人认证的最佳特征；合并 cart+order 标签配权重（Sirius +0.002）；单模型多目标 + rank gain 标签（Orders 6 / Carts 3 / Clicks 1，5th +0.001~0.002）；
4. **异质融合**：各成员候选/模型不同 → **按秩融合**（3rd 四人 0.598–0.600 → 0.603）+ 在 (score, rank) 特征上 stacking（→0.604）；
5. **规模工程**：cuDF 一分钟造一个共现矩阵、numba/polars 特征、int32 降位、分块 groupby、1/20 会话采样做 CV（10–30 分钟/实验）、treelite 推理。

一句话：**这是一场"候选召回率比赛"**——规则负责把正确答案放进候选，学习模型只负责把它挑出来；谁把共现矩阵变体空间探索得更深，谁就赢。

## 1. 材料与角色

| 帖子 | 作者 | 票数 | 角色与独有信息 |
| --- | --- | --- | --- |
| [370210](https://www.kaggle.com/competitions/otto-recommender-system/discussion/370210)（GBT Ranker 教程，335 票） | Chris Deotte | 335 | **社区教科书**：候选 rerank 全流程（候选 DF→item/user 特征→交互特征→目标→GroupKFold 训练→推理选 20）；内存/降位/分块/GPU 细节 |
| [364721](https://www.kaggle.com/competitions/otto-recommender-system/discussion/364721)（大数据推荐概念，275 票） | Ravi Shah | 275 | 漏斗框架：Millions（商品库）→ Thousands（候选生成）→ Hundreds（排序）→ Twenty（提交）；候选生成准则清单 |
| [383013](https://www.kaggle.com/competitions/otto-recommender-system/discussion/383013)（规则第 3，151 票） | Chris Deotte（G&B&D&T 队） | 151 | **20 个共现矩阵全清单 + 规则 0.590 + reranker +0.011 = 0.601 单模**；队友 Theo 0.6029 / Benny 0.601 |
| [382802](https://www.kaggle.com/competitions/otto-recommender-system/discussion/382802)（5th，103 票） | NikhilMishra | 103 | **近乎单模型**：0.604 公开 / 0.603 私榜；80→120 候选；单模型三目标 + rank gain 6/3/1；treelite |
| [382879](https://www.kaggle.com/competitions/otto-recommender-system/discussion/382879)（3rd imaginary，98 票） | Makotu 队四人（Alvor/Makotu/Shimacos/Sirius） | 98 | **四人方案全记录 + 融合账**：秩融合公式 1/r_a+1/r_b+1/r_c；堆叠 0.604；各人召回上限表 |
| [382790](https://www.kaggle.com/competitions/otto-recommender-system/discussion/382790)（2nd ONODERA，90 票） | ONODERA | 90 | **item2item 特征工程**：count/时间差/序列差 + 加权 + 聚合（93→~5k→用 400-500）；两阶段分数管线图 |
| [382771](https://www.kaggle.com/competitions/otto-recommender-system/discussion/382771)（20th，90 票） | kiccho | 90 | **召回全家桶**：Last Inter / Item·User MF(BPR) / Item·User CF / W2V / CoVis；~200 特征；polars；分数路线图 0.5799→0.5985 |

**材料缺口（未扩采，登记备查）**：除 1st（384022）外，还缺 [7th（383769，84 票）](https://www.kaggle.com/competitions/otto-recommender-system/discussion/383769)、[2nd senkin13 部分（382839）](https://www.kaggle.com/competitions/otto-recommender-system/discussion/382839)、[3rd Theo 部分（382975）](https://www.kaggle.com/competitions/otto-recommender-system/discussion/382975)、[6th（384120）](https://www.kaggle.com/competitions/otto-recommender-system/discussion/384120)、[9th（383792/383130）](https://www.kaggle.com/competitions/otto-recommender-system/discussion/383792)、[16th（383382）](https://www.kaggle.com/competitions/otto-recommender-system/discussion/383382)、[H&M 冠军方案汇总（372976）](https://www.kaggle.com/competitions/otto-recommender-system/discussion/372976) 等。

## 2. 逐方案对照矩阵

| 维度 | 规则第 3 (Chris) | 5th Nikhil | 3rd imaginary（四人合成） | 2nd ONODERA 部分 | 20th kiccho |
| --- | --- | --- | --- | --- | --- |
| 候选生成 | **20 个共现矩阵**（动作对/方向/衰减/冷启动/时段）；100 候选 notebook | 类共现矩阵按动作对分类 + 归一化（距离&频次）、Optuna 选 top-k 权重；80→120 候选 | 各成员独立：5–7 个矩阵变体；Alvor 关注矩阵质量（median 67/avg 121）；Makotu 7 pattern；Sirius 224/人 | 用队友 psilogram 的候选 | Last Inter / Item·User MF / Item·User CF / W2V / CoVis 七路召回 |
| 召回上限 | — | 80 候选时 max recall 0.648；前 20 = LB 0.585 | Alvor 0.6630 / Shimacos 0.6762 / Sirius 0.6772 | — | — |
| Ranker | XGB rank:pairwise（教程配方） | 单 LGBM 三目标 + rank gain | 每人 LGBM/CatBoost（各目标） + 堆叠 | XGB + CatBoost；item2item 400–500 特征 | LGBM Ranker + CatBoost Classifier + CatBoost Ranker |
| 跨目标技巧 | — | carts/orders/clicks 合并建模（+0.001~0.002）+ gain 6/3/1 | **carts 预测→orders 特征（Alvor 最佳特征）**；cart+order 合并 + 权重 5/10（Sirius +0.002）；OOF 链（Makotu 点击 2 模型→cart→order） | 1st stage 预测 + 伪事件特征 | — |
| 融合 | 团队各模型按秩相加 | 单模型为主 | **秩融合 1/r_a+1/r_b+1/r_c → 0.603；再堆叠 → 0.604** | 与队友按秩融合 → 0.60446 私榜 | 三模型集成（LGB+CatBoost） |
| 工程 | RAPIDS cuDF 造矩阵（<1 min/个） | numba 候选 + polars 特征 + treelite 推理 | BigQuery 造候选（Shimacos）；w2v/BPR/n2v | cuDF/cuML 全流程 | polars + parquet 特征仓 |
| 成绩 | 规则 0.590；单模 0.601 | 公开 0.604 / 私榜 0.603 | 融合 0.604（LGBM CV 0.59624） | 私榜 0.60446（团队） | 私榜 0.5985（最终 20th） |

## 3. 共识、分歧与裁决

### 共识一：候选召回率决定一切，排序只是微调（全场一致，本场第一定律）

- Chris：公共 notebook（3 矩阵）0.575 → **20 矩阵 0.590**（+0.015）→ reranker **+0.011** → 0.601；
- 5th：候选生成器**自排序前 20** 就 0.585，最终模型 0.604（排序净增 ~0.019）；
- 3rd 四人的候选召回 0.663–0.677（三类加权）；20th 的全家桶与分数路线图（每加一路召回 +0.001–0.010）。

**裁决**：本场应先优化"候选最大可能召回"这一指标，再做排序；候选不好时调 ranker 是浪费。置信度最高（4 家一致 + 可复算的阶梯）。

### 共识二：共现矩阵的"变体空间"就是竞争的主战场

Chris 列了 20 个矩阵的完整构造规则：相邻步/±2 步/±3 步、仅 carts/orders、时间衰减 `(1/2)^(Δt/小时)`、最近 2-3 周、冷启动用户（首行为）、时段（14 点前/后）、历史长度分桶（<6/>6）。Makotu"7 pattern"、5th 的动作对分类 + 距离归一化、Alvor"5 个最佳矩阵（以最大召回为判据）"都是同一思路。

**裁决**：矩阵设计 = 对"会话转移结构"的假设枚举 + 用最大召回筛选；20 个精挑的矩阵 > 更多但冗余的矩阵（Alvor：单纯增加候选量抬高了最大召回却降低了验证分）。置信度高。

### 共识三：跨目标特征（carts→orders）是排序阶段的免费增益

- Alvor："把 carts 预测作为 orders 模型的特征（**最佳特征**）"；反面："clicks 预测作为 orders 特征"失败；
- Sirius：cart/order 标签合并 + 正样本权重 5/10 → CV +0.002；
- Makotu：多模型 OOF 链（click 双模型→cart→order）；
- 5th：单模型三目标 + gain 标签（6/3/1）→ +0.001~0.002。

**裁决**：意图层级越近（cart→order）越有信息，越远（click→order）越弱；标签结构可用"合并+权重"或"OOF 特征链"两种方式利用。置信度高。

### 分歧一：每目标一个模型 vs 单模型多目标

5th 明确单模型 + rank gain 更好（+0.001~0.002，且数据按 session 分组）；3rd/20th 用 per-target 模型 + OOF 链；Sirius 合并 cart+order 保留 click 独立。

**裁决**：两者都行，关键在**是否显式建模目标间序关系**（gain 标签或 OOF 特征）；单纯 per-target 而不做交互会丢掉 cart→order 的免费信息。置信度中高（缺同框架对照）。

### 分歧二：候选数量越多越好吗？

5th：80→120 候选 +0.001，但 **200 候选无增益**；Alvor：增加候选抬高了最大召回却**降低验证分**；Shimacos："模型太多/负样本太多会降分"；Chris：100 候选 notebook 就能 49 名。

**裁决**：候选数量与 ranker 的判别能力、负样本比例耦合；存在"召回↔误报"的平衡点（约 100–200/会话），超过后负样本噪声主导。置信度中高。

### 分歧三：神经网络到底有没有用？

Sirius：MLP（0.598）不进最终融合；GRU/预训练 item embedding 全失败；20th：Transformer/GRU/CDAE/RecVAE/implicit ALS·BPR/聚类 全部失败；2nd：未提 NN。全员最终都是 GBDT（LGBM/CatBoost/XGB）。

**裁决**：在这个"ID-only、特征即候选生成证据"的设定下，GBDT 对稀疏计数型特征的建模优势明显；NN 需要序列建模但本场数据（短会话 + 无侧信息）不足以发挥。置信度高（三家负面 + 全员最终选择一致）。

## 4. 增量数字账

**Chris 的规则阶梯（本场最干净的因果链）**

| 步骤 | LB | 增量 |
| --- | --- | --- |
| 公共 notebook（3 个共现矩阵，规则） | 0.575 | 起点 |
| 共现矩阵 3→20 个（规则） | 0.590 | +0.015 |
| + XGB reranker（50 候选 + 矩阵计数特征） | **0.601** | +0.011 |
| 100 候选生成器单独提交 | 0.590（第 49 名） | — |

**各方案关键数字**

| 方案 | 数字 |
| --- | --- |
| 5th | 80 候选 max recall 0.648；候选自排序前 20 = 0.585；单模公开 0.604 / 私榜 0.603；120 候选 +0.001；单模三目标 +0.001~0.002；gain 6/3/1 +0.0005；倒数第二周数据 +0.0005；~400 特征 + 5% 负采样 |
| 3rd imaginary | 四成员私榜 0.600/0.600/0.598/0.598 → 秩融合 **0.603** → 堆叠 **0.604**（LGBM CV 0.59624、CatBoost 0.59592）；召回：Alvor 0.6315/0.5403/0.7296（总 0.6630）、Makotu order 0.732@190 / cart 0.546@190 / click 0.682@140、Shimacos 0.6799/0.5555/0.7359（总 0.6762，avg 188.69）、Sirius 0.6885/0.5573/0.7353（总 0.6772，avg 224.74）；Sirius 的 bi-gram 特征 +0.006（其最大单笔） |
| 2nd | item2item 93 特征 → 组合出 ~5k → 实用 400–500；与队友秩融合后 0.60446 私榜（自家部分公共 0.60283/私榜 0.60289） |
| 20th | 分数路线：0.5799（2 阶段基线）→0.5830（+Item2Vec/ItemMF）→0.5930（+ItemCF/UserMF）→0.5970（+ItemCF 变体）→0.5985（集成）；CV 1/20 采样 0.536→0.552，与完整 CV 0.569→0.585 同步；~200 特征 |
| 教程 | XGB rank 目标三选（pairwise/ndcg/map）；GroupKFold 按 session；50 候选/组；负采样 2–20×；int32/float32 降位 |

**可复算校验（2 处吻合）**

1. Chris：0.575（3 矩阵）→ +0.015（17 个新矩阵）→ 0.590 → +0.011（reranker）→ **0.601** ✓（与"单模 0.601"自述一致）；
2. 3rd 融合链：0.598–0.600 四人 → 秩融合 0.603（+0.003~0.005）→ 堆叠 0.604（+0.001）✓（与 Shimacos 文字一致）。

## 5. 机制推演

**M1｜为什么共现矩阵是本题的最强候选器**：会话短（多数 <10 事件）、无侧信息，唯一可用信号是"转移统计"。矩阵 `P(aid_B | aid_A)` 及其变体直接估计下一交互分布；方向性（forward only）、时间衰减、动作对（click→cart 与 cart→order 的转移强度不同）都在细化同一个估计。用"单个矩阵的最大可能召回"做筛选，等价于在转移结构假设空间上做贪心特征选择。

**M2｜为什么排序只值 +0.011~0.019**：recall@20 的增益 = "候选集合里正确项的边际" × "ranker 的判别力"。当候选召回 0.60–0.68、候选数 50–200 时，正样本在候选中的基率已足够高，ranker 只需按共现计数/新鲜度/用户-物品交互重排；排序的作用是"从 top-200 里挑 top-20"，其信息增益受候选质量上界约束。**推论：任何本场的改进都应先问"它提高候选召回了吗？"**

**M3｜跨目标 OOF 链的机制**：click/cart/order 是有序意图（买前必先加购或点击），且各目标的最优候选权重不同（order 更靠 cart 转移）。把上游目标的预测作为下游特征，等于把"意图序列的中间状态"显式喂给模型；clicks→orders 失败而 carts→orders 成功，说明**只有直接前驱有增量信息**（马尔可夫性质在意图层级上的体现）。

**M4｜秩融合的数学**：各成员分数不可比（不同候选集/模型/尺度），但"排名"可比。`1/rank` 加权和是 Borda 计数式的共识排序，天然处理"只有一家命中的项"（fill 值 1/50 提供基线），且对极端分数不敏感。堆叠在 (score, rank) 特征上学融合权重，把手工秩融合自动化（+0.001）。

**M5｜为什么负采样与候选数量必须联合调**：候选数 K 增大 → 正样本几乎不变、负样本线性增长；若负采样不够，训练分布偏离评测分布（评测只看 top-20 的排序质量）。5th"200 候选无益"与 Shimacos"模型太多降分"都是负样本稀释效应；合适区间约 K=100–200 + 5–20% 负采样。

**M6｜工程规模如何塑造方法论**：216M 事件 → cuDF 把矩阵计算压到 <1 分钟/个，才使"枚举数百个矩阵"可行（Chris 说"找到这 20 个是计算了数百个矩阵后按 CV 筛的"）；1/20 会话采样让 CV 从小时级降到 10–30 分钟且保持与 LB 的相关性——**实验吞吐本身就是分数**（与 amex 的"迭代速度即分数"同构）。

## 6. 证据分级

| 断言 | 等级 | 说明 |
| --- | --- | --- |
| Chris 规则阶梯 0.575→0.590→0.601 | **可读取（帖内数字）** | 每步有公开 notebook 可复现 |
| 20 个矩阵的构造规则 | **可读取（帖内代码描述）** | 全部 notebook 与 GitHub 公开（261 个） |
| 3rd 四人召回上限/融合链 | **可读取（图+文）** | 各人管线图完整 |
| 5th"单模型 0.604/0.603" | **自述** | 无公开对照表 |
| 2nd 的管线分数图 | **可读取（图）** | 但单目标 public/private 列与 합成口径不完全一致（仅作参考） |
| 20th 分数路线图 | **可读取（表）** | 每步一行，可信 |
| "carts 作 orders 特征是最佳特征" | **自述（Alvor）** | 多人方向一致（Sirius/Makotu/5th 间接支持） |
| "bi-gram 特征 +0.006" | **自述（Sirius）** | 无消融细节 |
| 1st place 方法 | **缺失** | 未收录正文；不得以教程内容代称冠军方案 |

## 7. 边界条件与反事实

- **候选天花板是本场的硬边界**：4 家召回上限 0.663–0.677；若无 1st 的召回结构，0.68+ 是否可达未知。反事实：把召回从 0.67 抬到 0.72，理论上总分可再 +0.02~0.03（排序增益会同比例放大）——这正是各队穷举矩阵的动机。
- **无侧信息（只有 aid）**：所有特征都来自行为序列本身；一旦有商品类目/价格等侧信息，共现矩阵的统治力会下降（对照 H&M 冠军方案）。
- **反事实（Alvor）**："直接增加候选数量"增加最大召回但降验证分——说明**召回上限不是唯一指标，候选的精确分布同样重要**；给 ranker 更多"看似合理"的负样本反而伤害训练。
- **反事实（5th）**：80 候选已 0.585，涨到 120 只 +0.001——候选边际收益递减很快；资源应转向矩阵质量而非数量。
- **完整性风险**：1st（0.？）与 7th/9th/6th 未收录，可能遗漏"非共现矩阵主导"或"NN 成功"的替代路线；本深读的裁决（GBDT + 共现矩阵）存在幸存者偏差——所有收录成员都恰是 GBDT 阵营。
- **作弊争议**：3rd imaginary 因一名队友被疑似作弊而"荣誉降级"；其自述成果无外部影响。提醒：**团队赛的合规审查也是比赛的一部分**。

## 8. 悬案与失败学

**悬案**

1. **1st place 的方法到底是什么**（缺一手材料；只能确认 Chris 队友 Theo 单模 0.6029 拿第 3）；
2. **候选召回上限的理论极限**：0.68 是否接近数据噪声上限（会话随机性）；
3. **NN 在更大侧信息/更长会话下是否会反超**（本场全是负面证据，但边界未探明）。

**失败学**

| 失败 | 来源 | 教训 |
| --- | --- | --- |
| W2V/MF 的 KNN 候选 | Alvor | 抬高最大召回却降验证分；候选"看起来合理"≠有用 |
| 单纯增加候选数量 | Alvor/5th/Shimacos | 负样本稀释 ranker；K≈100–200 是甜区 |
| clicks 预测当 orders 特征 | Alvor | 跨目标只有直接前驱有增量 |
| 对 top-X 做二次重排模型 | Alvor | 二次模型未带来增益（候选+单 ranker 足够） |
| 第二点击加入正样本 | Alvor | 无效 |
| MLP/GRU/预训练 item embedding | Sirius | 不进融合/失败（MLP 0.598） |
| Transformer/GRU/CDAE/RecVAE/implicit ALS·BPR/聚类/流行项/stacking/伪标签 | 20th | 全部失败；GBDT 主导 |
| 训练早期不做负采样 | Alvor | 内存/时间成本爆炸，后期才降到 1/5、1/15 |
| 200 候选实验 | 5th | 无增益 |

## 9. 图表证据

> 路径相对本文件（`analysis/deep/`）：`../../intel/otto-recommender-system/bodies/<topic>_img/NN.ext`

**图 1：候选生成漏斗（Millions → Thousands → Hundreds → Twenty）**（Ravi Shah，topic 364721）——`../../intel/otto-recommender-system/bodies/364721_img/01.PNG`

![funnel](../../intel/otto-recommender-system/bodies/364721_img/01.PNG)

*读图结论*：商品库（百万级）→ 候选生成（千级）→ 排序（百级）→ 提交（20）。这张图是本场方法论的"第一性原理"：所有计算预算应花在"千级"这一步的质量上。

**图 2：Makotu 的四段管线**（3rd imaginary，topic 382879）——`../../intel/otto-recommender-system/bodies/382879_img/01.png`

![makotu](../../intel/otto-recommender-system/bodies/382879_img/01.png)

*读图结论（正文未给全的细节）*：Preprocess（w2v aid 向量、aid 聚类 8 维、BPR 向量）→ Make candidates（**7 种模式共现矩阵**；按 last/top/1 小时内/1 天内动作选候选；**140–180 候选/会话**）→ Features（last aid 的 w2v 距离、BPR——其验证最佳）→ Modeling（单模型 PairLogitPairwise；click 训 2 个模型：预测下一点击+预测全部点击；cart 用 ①② 的 OOF；order 用 ①②③ 的 OOF）。

**图 3：Sirius 的召回→特征→模型全景**（3rd imaginary）——`../../intel/otto-recommender-system/bodies/382879_img/03.png`

![sirius](../../intel/otto-recommender-system/bodies/382879_img/03.png)

*读图结论*：召回四路（已交互项/Co-visit/Bi-gram/BPR）；特征三层（interaction：co-visit 与 bi-gram 的 last/sum/mean/max/min、BPR·w2v·GRU 距离、rank in session、距最后动作时间差、其他动作 OOF；user/item 计数与时间窗）；模型 CatBoost **0.600** / MLP 0.598（未入融合）。**"bi-gram 特征 +0.006"就是这里的 next-action 双元组统计。**

**图 4：item2item 特征的构造语义（2nd）**（topic 382790）——`../../intel/otto-recommender-system/bodies/382790_img/01.png`

![item2item](../../intel/otto-recommender-system/bodies/382790_img/01.png)

*读图结论*：把会话事件表自连接成 (aid_x, aid_y) 对，保留 type_x/type_y、ts_diff、seq_diff；**忽略自配对**。这就是 93 个 item2item 基础特征的生成方式（count/时间差/序列差 + 加权 + 聚合）。

**图 5：2nd 的两阶段分数管线**（topic 382790）——`../../intel/otto-recommender-system/bodies/382790_img/05.png`

*读图结论*：单目标与融合的 CV 演进：1st stage（orders CV 0.669028 / carts 0.440927 / clicks 0.560697）→ 2nd stage（0.670623 / 0.443031 / 0.561895）→ ALL CV 0.59131 / 公开 0.60231 / 私榜 0.60247 → 与队友融合后公开 0.60401 / 私榜 **0.60446**。（注意：图中单目标的 public/private 列与 CV 列口径不同，勿直接加权对照。）

**图 6：kiccho 的召回全家桶与排序层**（20th，topic 382771）——`../../intel/otto-recommender-system/bodies/382771_img/01.png`

![kiccho](../../intel/otto-recommender-system/bodies/382771_img/01.png)

*读图结论*：七路召回（Last Inter / Item MF / User MF / Item CF / User CF / W2V / CoVis）→ 四类特征（User/Item/Interaction/Recall）→ 三个模型（LGBM Ranker、CatBoost Classifier、CatBoost Ranker）。其分数路线图（正文）显示**每加一路召回的边际收益**：Item2Vec/ItemMF +0.003、ItemCF/UserMF +0.010、ItemCF 变体 +0.004、集成 +0.002。

## 10. 对既有笔记/playbook 的修订点

1. `notes/tabular/otto-recommender-system.md` 升级：补齐 7 节作者/票数；
2. **修正误标**：原笔记把"候选生成 + GBT 排序"标为 1st——实际 1st 正文未收录，该行改为"社区教程（非冠军认证）"，并在出处登记 384022 缺口；
3. 方案谱系扩为 5 方案对照矩阵（规则 3 / 5 / 3imaginary / 2 / 20）；
4. 新增：20 矩阵清单的类别化摘要、规则阶梯数字账、跨目标 OOF 链、秩融合公式、失败学与图证。
5. `playbook/sim-agent.md` 或 `playbook/tabular.md` 增补推荐系统专节：
   - **候选召回上限优先**（先量化 max recall，再谈 ranker）；
   - **共现矩阵变体维度清单**（动作对/方向/时间衰减/邻距/冷启动/时段/历史长度）；
   - **意图链 OOF**（只信直接前驱）；
   - **K×负采样联合调参**（甜区 K≈100–200、采样 5–20%）；
   - **秩融合与 (score,rank) 堆叠**；
   - **大规模工程**（cuDF/numba/polars/treelite；会话采样做 CV）。

## 11. 出处

- GBT Ranker 教程（Chris Deotte，335 票）：https://www.kaggle.com/competitions/otto-recommender-system/discussion/370210
- 大数据推荐概念（Ravi Shah，275 票）：https://www.kaggle.com/competitions/otto-recommender-system/discussion/364721
- 规则第 3（Chris Deotte/G&B&D&T，151 票）：https://www.kaggle.com/competitions/otto-recommender-system/discussion/383013
- 5th（NikhilMishra，103 票）：https://www.kaggle.com/competitions/otto-recommender-system/discussion/382802
- 3rd imaginary（Makotu 队，98 票）：https://www.kaggle.com/competitions/otto-recommender-system/discussion/382879
- 2nd ONODERA 部分（90 票）：https://www.kaggle.com/competitions/otto-recommender-system/discussion/382790
- 20th（kiccho，90 票）：https://www.kaggle.com/competitions/otto-recommender-system/discussion/382771
- 未收录缺口（登记备查）：**384022（1st）**｜383769（7th）｜382839（2nd senkin13）｜382975（3rd Theo）｜384120（6th）｜383792/383130（9th）｜383382（16th）｜372976（H&M 汇总）等
