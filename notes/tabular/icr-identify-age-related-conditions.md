# ICR - Identify Age-Related Conditions

> 主题：tabular ｜ 子类：— ｜ 领域：医疗 ｜ 类别：Featured
> 截止：2023-08-10 ｜ 队伍数：6430 ｜ 机制：代码赛 ｜ 指标：Balanced Log Loss（加权多分类损失）
> 数据来源：`intel/icr-identify-age-related-conditions/`（120 条主题索引 + 8 篇 write-up 正文）

## 1. 任务与数据

- **预测目标**：由匿名医疗特征预测受试者是否患病（二分类概率），另有 Alpha/Beta/Gamma/Delta 四个辅助标签（俗称 "greeks"）可做辅助建模。
- **数据规模**：约 600 行训练数据、几十个匿名数值/类别特征，带大量缺失值。**小样本 + 高噪声**是本质约束。
- **构造陷阱（本场比赛的核心）**：
  - 测试集在**时间上晚于**训练集，且存在明显的分布漂移（同一特征在不同时间段的判别力不同）。
  - 把 `time` 当特征会变成"最重要特征"——这是漂移的信号，不是可用的信号。
  - 一部分类别特征在 train/public/private 三段的分布显著不同（如 EJ 特征中 B 类占比 64% / 62% / 50%）。
  - 测试集有两列在训练集中完全不存在缺失，且存在"没有时间戳"的样本聚成独立簇。

## 2. 验证方案

这是本场比赛胜负的分水岭，三类方案都出现在 write-up 里：

| 方案 | 做法 | 结果 |
| --- | --- | --- |
| **滑动时间 CV**（silver medal） | 按时间排序，缺失时间随机填充，用滑动窗口切 25 折；验证集是连续时间段 | 本地 CV 0.27，与 private 0.39 的难度关系一致；CV 的提升能反映到两个榜 |
| 分层 K 折 / 重复分层 | RepeatedStratifiedKFold(5×5) | 在漂移数据上会系统性高估，5th place 因此吃了暗亏 |
| 无 CV、直接看公开榜 | 依赖 public LB | 公开榜仅约 200 样本，是最危险的路径 |

**公开榜风险已被反复验证**：公开榜 ≈ 0.15–0.17，私榜 ≈ 0.34–0.39。用公开榜探针（probing）构造伪标签的参赛者，私榜**明确变差**；作者自己总结为"两种冒险都失败了"。

## 3. 模型家族

| 方案 | 名次 | 关键点 |
| --- | --- | --- |
| 变量选择网络（Variable Selection Network）的 DNN | 1st | 纯 DNN；GBDT 严重过拟合；greeks 无用（测试集没有）；特征工程导致过拟合；配合概率重加权 |
| CatBoost + XGB + TabPFN 简单平均 | 2nd | 时间处理 + UMAP/KMeans 簇特征 + 手工特征置换筛选；LGBM 掉分；**堆叠无增益** |
| CatBoost 全特征交叉 + 比值特征 | 3rd | 模仿体检指标做特征间比值，配合相关系数预筛 |
| CatBoostRegressor 递归填补缺口 + 各 greek 概率做特征 | 4th | 刻意规避公开榜过拟合；`row_id` 按 Epsilon 排序构造 |
| 各 greek 单独建模 + 概率堆叠 + LGBM 插补 | 5th | 强项在 greek 概率堆叠，插补器去掉也不掉分 |
| XGBoost 集成 + 贝叶斯调参 + 投票 | 6th | pandas 线性插值 + RF 重要度筛选 + GridSearch 精调 |
| 多模型 + 过采样 + 常量插补集成 | 9th | 出于对过拟合的恐惧而刻意保守 |

## 4. 关键技巧

- **特征**：greeks（Alpha/Beta/Gamma/Delta）的独立建模与概率堆叠（5th place 认为这是主要收益来源）；匿名特征之间的**比值特征**（3rd place，类比体检指标）；UMAP + KMeans 簇标签（2nd place，小幅增益）。
- **缺失值**：递归回归填补（4th）、线性插值 + RF 重要度（6th）、常量填充（2nd 用 -100）；**Epsilon 的缺失填 `min()` 或 `max()+1`** 反复出现。
- **训练**：过采样平衡类别；重复分层 K 折；TabPFN 在小样本表格上表现突出（多支队伍使用）。
- **后处理**：把低于阈值的预测直接置 0（按 Balanced Log Loss 的构造，压低一部分预测能改善分数）——但 silver medal 的阈值分析显示：**该方法在"容易的时间段"有效、在"困难的时间段"失效**，保守阈值同样伤私榜。
- **明确无效**：堆叠（2nd）、Optuna 调参（2nd）、暴力特征工程（5th、1st）、LGBM（2nd）。

## 5. 可迁移性评估

- **可直接迁移**：
  - "先设计能模拟训练/测试关系的验证方案，再谈模型"——尤其是**时间漂移**场景下的滑动窗口 CV。
  - 小样本表格比赛优先试 TabPFN 一类小样本友好模型，再考虑 GBDT。
  - 用**分折分析**（每折最优后处理阈值随时间的分布）来评估后处理风险，而不是只看整体 CV。
  - 公开榜样本量很小时，把 public LB 当作噪声源而非优化目标。
- **需要前提**：
  - greeks 类辅助标签的堆叠收益依赖比赛提供了这些标签，换个数据集未必存在。
  - Epsilon 缺失值填 `min/max±1` 是本题数据结构特有的技巧。
  - 阈值后处理要求指标对"压低预测值"有系统性偏好（Balanced Log Loss 有），换指标会失效。
- **不建议照搬**：
  - 公开榜探针 + 伪标签：本场比赛已被证伪。
  - 任何"公开榜涨了就提交"的选择策略：私榜抖动幅度超过 2 倍。

## 6. 对新手的关键启示

1. **验证方案本身就是解法**。这场比赛 1st–9th 的名次差异，主要来自"谁没有被公开榜带偏"，而不是模型复杂度。
2. **小数据下，模型越复杂越要先怀疑自己**。冠军用 DNN、亚军堆叠无效、6th 用 XGB 集成——都能上榜，但前提是 CV 可信。
3. **分布漂移要主动找证据**：把时间当特征看重要度、对比 train/public/private 的类别占比、检查测试集独有缺失——这些是低成本高回报的检查动作。
4. **后处理要分折验证**，整体 CV 会掩盖"只在部分子集有效"的事实。

## 7. 轻读结论（2026-10 补）

**一句话**：极小样本 + 时间漂移的噪声赛——**按时间验证、控过拟合、拒绝高风险后处理**是唯一可复制心法；名次有巨大运气成分（前三方法族完全不同）。

- Silver（64 票）：滑窗时间 CV：CV 0.27/公 0.17/私 0.39；各时段难度 0.13–0.42（图 1）；25 折阈值分析证明 PP 只在"简单时段"有效，私榜=困难时段 → 保守 PP 与探测伪标的两种激进提交都失败。
- 1st（318 票）：VSN DNN + 每特征 8 神经元线性投影 + 超大 dropout + 概率重加权；10 折重复 10–30 次、每折选 2 模型对抗巨震；自认运气。
- 2nd：**"只是 CV"**（无探测/无 PP）：time 处理 + UMAP/KMeans + 手动特征剔除 + CatBoost/XGB/TabPFN 平均。
- 3rd/4th/9th：特征交叉 CatBoost / 递归填补+类别概率+未调参 CatBoost / XGB+TabPFN 15 折加权；9th 明说 PP 无效。

**裁决**：随机 CV 高估；时间 CV 是必需；PP/阈值/伪标在私榜负期望；Greeks 等"只在训练存在的字段"是陷阱。

**悬案**：382/275/224/195 票的平衡/PP 原帖未入库；官方漂移处置未收录。

## 8. 图表证据

![各时间段验证损失](../../intel/icr-identify-age-related-conditions/bodies/431067_img/02.png)

**图 1**（topic 431067）：Validation Balanced Log-Loss vs Date（约 0.13→0.42）——时间漂移与 PP 失效的机制证据。

## 9. 出处

- 讨论区索引：`intel/icr-identify-age-related-conditions/topics.md`（120 条，含 382 票的平衡训练帖、275 票的指标解释帖）
- 已收录 write-up（8 篇）：
  - 1st（318 票，"How on Earth did I win this competition?"）：https://www.kaggle.com/competitions/icr-identify-age-related-conditions/discussion/430843
  - 2nd（80 票）：https://www.kaggle.com/competitions/icr-identify-age-related-conditions/discussion/430860
  - 3rd（32 票）：https://www.kaggle.com/competitions/icr-identify-age-related-conditions/discussion/430978
  - 4th（22 票）：https://www.kaggle.com/competitions/icr-identify-age-related-conditions/discussion/431173
  - 5th（39 票）：https://www.kaggle.com/competitions/icr-identify-age-related-conditions/discussion/430907
  - 6th（30 票）：https://www.kaggle.com/competitions/icr-identify-age-related-conditions/discussion/431048
  - 9th（20 票）：https://www.kaggle.com/competitions/icr-identify-age-related-conditions/discussion/430906
  - Silver + 滑动时间 CV（64 票）：https://www.kaggle.com/competitions/icr-identify-age-related-conditions/discussion/431067
- 轻读全本：`analysis/deep/icr-identify-age-related-conditions.md`（Tier B 轻读：对照矩阵/裁决/证据分级/悬案 + 1 图证）
