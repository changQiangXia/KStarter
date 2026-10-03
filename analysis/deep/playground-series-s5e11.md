# Playground Series S5E11（贷款偿付预测）轻量深读（Tier B）

> 赛事：Playground ｜ 主题 tabular（二分类，合成数据）｜ 3724 队 ｜ 标准赛 ｜ 指标：ROC AUC
> 材料基础：`digests/playground-series-s5e11.md`（6 篇正文：1st 647362 / 2nd 647288 / 4th 647417 / 5th 647359 / 6th 647305 / 盲混讨论 614986；70 条主题索引）+ 0 张归档图
> 轻读时间：2026-10（Tier B B12）

## 1. 一句话重述与数字账

贷款偿付二分类（AUC），是本系列里少见的"**特征工程统治 + CV-LB 高度一致**"的一届：前六名全部把重心放在**数字位（digit）特征、分箱后的目标编码（TE）、原数据 TE**上，集成器则一致地选择 Ridge / Hill Climbing 这类线性方案（非线性堆叠普遍过拟合）。1st 的 100 模型集成里，最强单模（CV 0.92818 / LB 0.92923）本身就能排到第 2；2nd 的"7 模型 Ridge"里单看一个 LGBM 也够第 2。

| 关键数字 | 值 | 来源 |
| --- | --- | --- |
| 1st（647362） | FE 清单：base 两两组合 + TE/CE；数值列的**各位数字**；**数字之间**的两两/三元/四元交互 + TE/CE；round 特征；数字×base 组合；原数据上的 TE/CE；用 `employment_status` 当目标的 TE；用 `employment_status + debt_to_income_ratio` 当目标的 TE；分位分箱等；**最佳单模 CV 0.92818 / LB 0.92923**；集成共 **100 个模型**，Ridge/HC 最佳，非线性堆叠明显更差；XGB 私榜 0.92923、LGBM 0.92920、RealMLP 0.92906、TabM 0.92895、CatBoost 0.92899…Extra Trees 0.92549 | 647362 |
| 2nd（647288） | Ridge 集成 7 模型（5×LGBM + TabM + RealMLP）；另有一份"最佳单 LGBM"同样拿到第 2；特征 = 基数 >7 的列全部 TE + CE + **用原数据目标做 TE**；高基数 `annual_income`/`loan_amount` 用**分位/均匀分箱、round、整除、astype(int)** 多种离散化再编码；数值列的数字位及其组合；**train/原数据的计数比**（过采样率）；自述"交互特征与把原始数据当行加入都没有提升 CV"；LGBM 靠强正则（低 max_depth、小 colsample）大幅改善 | 647288 |
| 4th（647417） | LGBM + DNN 双模型；晚进场，先用早期 8 模型的集成预测做**伪标签**（CV +0.0004）；约 100 个新特征；自述 n-way 交互无帮助；5 seeds；用**差分进化爬山**求 5 个 seed 的最优凸组合（DNN CV +0.0004、LGBM +0.0002）；最终两模型加权；LGBM CV 0.9284 / LB 0.9279；私榜 0.92915 | 647417 |
| 5th（647359） | XGB + LGBM + TabM 各 5 seeds + AutoGluon，Ridge 回归融合；FE = 数字位、round/分箱、数字类内的 2/3/4 元交互、原数据均值/计数编码；特征按"逐个加入看 CV"筛选（`train_test_split` 0.2 代 CV 省算力）；Optuna 调参；**不训练全量数据**（早期实验全量公榜更差）；CatBoost/xRFM/RealMLP 被弃 | 647359 |
| 6th（647305） | "把全部特征当类别"：`loan_amount` 取整到 10、`annual_income` 取整到 100，降低基数后用 Keras **FM（因子分解机）**≈0.926、加 bi-gram 到 0.9265；单轮爬山把 CV 0.9275 → 0.928；CatBoost/Keras 堆叠在**大集成上过拟合**；RealMLP/Trompt 加入后公榜下降被剔除 | 647305 |
| 社区 | "How to blend models correctly"（90 票 / 37 评论）、"Blind blending fails in practice"（71 票 / 20 评论）、"Stable CV-LB Relationship"（42 票）、"单模 vs 集成"（36 票）、"boosting over residuals"提议（118 票 / 86 评论）、"模型正交性"（22 票） | 索引 |

## 2. 逐方案对照矩阵

| 维度 | 1st | 2nd | 4th | 5th | 6th |
| --- | --- | --- | --- | --- | --- |
| 模型 | 100 模型大集成 | 7 模型（5 LGBM+TabM+RealMLP） | LGBM + DNN | XGB+LGBM+TabM ×5 seeds + AG | 多 NN + GBM（FM 为亮点） |
| FE 核心 | 数字位交互 + 多目标 TE | 多方式分箱 + TE/CE + 计数比 | ~100 特征 + 伪标签 | 数字位 + 交互 + 原数据编码 | 全类别化 + FM bi-gram |
| 集成器 | Ridge / HC | Ridge | 差分进化爬山 | Ridge | Hill Climbing |
| CV-LB 使用 | 信 CV | 信 CV | CV+LB 混合 | 全程信 CV（不训全量） | 信 CV（但堆叠过拟合） |
| 私榜 | 1st | 2nd | 0.92915（4th） | 0.92912（5th） | 6th |

## 3. 共识、分歧与裁决

### 共识一：FE（数字位/分箱/TE）是本届的决定性投入（1st、2nd、4th、5th、6th；置信度高）

1st 的最佳单模就靠一套数字位 + 多目标 TE 特征达到第 2 名水平；2nd 用多种离散化 + 原数据 TE 让单 LGBM 也进前 2；4th/5th 的清单高度相似。**裁决**：高基数 + 大量数值列的合成数据，核心操作是"离散化成类别 → 目标编码/计数编码 → 数字位交互"；模型选择退居其次。置信度：高。

### 共识二：线性集成器（Ridge/HC）优于非线性堆叠（1st、5th、6th；置信度高）

1st 明确"LGBM/CB/NN 堆叠都远差于线性"；5th 选 Ridge 就是为稳定性；6th 的 CatBoost/Keras 堆叠在大集成上过拟合。**裁决**：当基模型已经很同质（同一套 FE、同族模型）时，L2 层用线性/爬山即可，非线性堆叠会放大过拟合。置信度：高。

### 共识三：CV-LB 关系稳定，应信 CV 并克制"全量训练"（4th、5th、2nd；置信度中高）

5th 明确不训全量数据（早期实验全量公榜更差）；社区有"Stable CV-LB Relationship"（42 票）与"trust the CV score"（17 票）专帖。**裁决**：该届测试集约占 20%（约 5.1 万行），公榜噪声小，CV 可作为主决策信号；但集成选择仍需警惕 CV 虚高（6th 的 0.9289 CV 对应更低的公榜）。置信度：中高。

### 分歧一：交互特征到底有没有用（1st vs 2nd/4th；置信度中）

1st 的数字位多元交互是其最强单模的核心；2nd 明确"interaction features 没有提升 CV"；4th 也说"n-way 交互没帮助"。**裁决**：差别在"对什么做交互"——数字位/离散化编码之间的交互有效，原始连续特征层面的 n-way 交互无效。置信度：中。

### 事件：盲混（blind blending）与集成纪律（614624、614704、636012；置信度中）

"How to blend models correctly"（90 票）与"Blind blending fails in practice"（71 票）构成一对讨论：公开 notebook 的无脑混合在私榜不差，但缺乏方法学保证；1st 也提到盲混 notebook 私榜表现不错。**裁决**：混合权重应有 CV/爬山依据；"盲混"可作为弱基线而非策略。置信度：中。

## 4. 证据分级

| 断言 | 等级 | 说明 |
| --- | --- | --- |
| 1st 的 FE 清单/单模分数/100 模型表 | 自述 + 完整分数表 | 中高 |
| 2nd 的分箱-编码体系与单模型并列第 2 | 自述 + 公开 notebook | 中高 |
| 4th 的伪标签与差分进化权重 | 自述 | 中 |
| 5th 的四个公开 notebook 与分数表 | 自述 + 代码 | 中高 |
| 6th 的 FM/全类别化与爬山增益 | 自述 | 中 |
| CV-LB 稳定性 | 社区多帖 + 多队自述 | 中高 |

## 5. 悬案与缺口（登记）

- 3rd / 7th+ 方案未收录；
- "boosting over residuals"（118 票提议）是否被采纳未验证；
- 1st 的模型清单只给分数没有权重构成；
- 盲混 notebook 的具体流程未细读；
- **图证缺口**：本场归档 0 图（无分数/权重图）。

## 6. 图表证据

无可用图证（本场归档 0 图，图证缺口已登记）。

## 7. 出处

- 1st（95 票 / 54 评论）：https://www.kaggle.com/competitions/playground-series-s5e11/discussion/647362
- 2nd（31 票 / 16 评论）：https://www.kaggle.com/competitions/playground-series-s5e11/discussion/647288
- 4th（17 票）：https://www.kaggle.com/competitions/playground-series-s5e11/discussion/647417
- 5th（19 票 / 11 评论）：https://www.kaggle.com/competitions/playground-series-s5e11/discussion/647359
- 6th（15 票 / 15 评论）：https://www.kaggle.com/competitions/playground-series-s5e11/discussion/647305
- boosting over residuals 提议（118 票 / 86 评论）：https://www.kaggle.com/competitions/playground-series-s5e11/discussion/614986
- How to blend models correctly（90 票）：https://www.kaggle.com/competitions/playground-series-s5e11/discussion/614624
- Blind blending fails in practice（71 票）：https://www.kaggle.com/competitions/playground-series-s5e11/discussion/614704
- Stable CV-LB relationship（42 票）：https://www.kaggle.com/competitions/playground-series-s5e11/discussion/614140
- 单模 vs 集成（36 票）：https://www.kaggle.com/competitions/playground-series-s5e11/discussion/636012
- 模型正交性（22 票）：https://www.kaggle.com/competitions/playground-series-s5e11/discussion/614412
