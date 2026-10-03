# Tabular Playground Series Jan 2022（北欧销量预测）轻量深读（Tier B）

> 赛事：Playground ｜ 主题 tabular（时间序列回归）｜ 1591 队 ｜ 标准赛 ｜ 指标：SMAPE
> 材料基础：`digests/tabular-playground-series-jan-2022.md`（6 篇正文：1st 304355 / 40th 304353 / 16th 304413 / 混合模型 298196 / 方案汇编 304381 / 热帖 298446；80 条主题索引）+ 1 张归档图（社区 meme）
> 轻读时间：2026-10（Tier B B12）

## 1. 一句话重述与数字账

预测 KaggleRama/KaggleMart 在芬兰、挪威、瑞典的产品销量（SMAPE）。本场的最大教训是**"公榜完全无法评估节假日效应"**：公榜只覆盖 2019 年 1–3 月，Easter/Midsummer/国庆/圣诞全在 4 月以后；1st 的公榜分数只有 4.11991（公开榜约第 306 名），却靠按年分组的 CV + 残差分析夺冠。技术主线上，**精心设计的线性模型（Ridge + log 目标 + Fourier + 节假日 + 外生指标）击败了 GBDT**——因为线性模型能精确控制"假期窗口"，树模型只能靠超参逼近。

| 关键数字 | 值 | 来源 |
| --- | --- | --- |
| 1st（304355） | Ridge + log 目标；**GroupKFold（按年分组）**；把 1–3 月与其余月份的 SMAPE 分开评估，只优化后者；公榜 4.11991（约第 306 名）但私榜夺冠；特征 = Fourier 系数（stickers 不给 Fourier）、各假期的精确长度（挪威复活节与其他两国不同）、OECD 消费者信心指数（外生数据）；用 ColumnTransformer 的多个 MinMaxScaler 实现"按特征差异化正则"；KaggleRama/KaggleMart 比例恒定 → 直接计算 | 304355 |
| 5th（304369） | "Minimum linear regression"（最小线性回归）——线性路线再次进前 5 | 主题索引 |
| 16th（304413） | 混合模型 + 网格搜索；一阶 Fourier；自述从公榜跳跃 **277 名**；试过 GDP per capita（人均 GDP），发现普通 GDP 与目标相关性略高，最终弃用 | 304413 |
| 40th（304353） | Boltzmann 集成：每个模型权重 ∝ `exp(b·(S−x))`（x 为公榜分），只有一个可调参数 b（类比 1/kT）；b 在赛程中显著漂移；局限：无负权重、不考虑模型相关性、模型全进全出 | 304353 |
| 方法帖 | 混合模型（线性外推 + GBDT 学交互）的历史先例：Walmart STL+指数平滑、Rossmann ARIMA+GBDT、Web Traffic 堆叠混合（33 票）；"四舍五入为什么提分"（71 票）；SMAPE 计算（81 票）；近似 SMAPE（40 票）；"公榜无法突破 4.00"（11 票） | 索引 |
| 社区 | 热帖 "This is how I feel every day on Kaggle"（224 票 / 153 评论）；"Data leakage in notebooks of top-competitors"（11 票 / 10 评论）；"Overfitting the public lb is sooo easy"（16 票） | 索引 |

## 2. 逐方案对照矩阵

| 维度 | 1st | 5th | 16th | 40th |
| --- | --- | --- | --- | --- |
| 模型 | Ridge（log 目标） | 最小线性回归 | 线性+GBDT 混合 + 网格搜索 | 公开 notebook 的 Boltzmann 加权集成 |
| 关键特征 | Fourier + 精确假期 + OECD 信心指数 | 精简线性特征 | 一阶 Fourier 等 | 无（权重法） |
| 验证 | 按年 GroupKFold；分月段看 SMAPE | — | — | 用公榜分做权重（受公榜偏差影响） |
| 对公榜态度 | 主动忽略（公榜≈无假期信息） | — | 借公榜跳跃 | 完全依赖公榜排序 |
| 结果 | 1st（公榜 306 名） | 5th | 16th | 40th |

## 3. 共识、分歧与裁决

### 共识一：公榜只覆盖 2019Q1，必须用 CV、不能信公榜（1st、社区帖；置信度高）

1st 的公榜分数对应约第 306 名；"Overfitting the public lb is sooo easy"（16 票）与"Leaderboard scores can't break 4.00"（11 票）都在围观同一现象。**裁决**：当评估窗口与目标现象（假期）错位时，公榜就是噪声；应按时间分组交叉验证并分段看指标。置信度：高。

### 共识二：强季节外推任务上，精心设计的线性模型 > GBDT（1st、5th；置信度中高）

1st 明确论证：GBDT 会自动拟合假期长度（9 或 11 天），调参逼到 10 天会在别处过拟合；线性模型让作者能"手工把复活节窗口定为 10 天"。**裁决**：可解释的外推需求 > 自动交互学习时，优先线性 + 特征工程。置信度：中高。

### 共识三：后处理（舍入）与外部数据是有效增益（71 票帖、1st、16th；置信度中高）

"Why rounding improves the score"（71 票）与 "TIP: 一行代码提分"（39 票）说明 SMAPE 下取整预测有系统收益；1st 用 OECD 消费者信心，16th 试 GDP。**裁决**：SMAPE 赛先把舍入/整数化纳入后处理搜索；外生宏观指标可小幅增益但需验证。置信度：中高。

### 分歧一：纯线性 vs 混合模型（1st vs 16th/298196；置信度中）

混合模型帖给出"线性外推趋势 + GBDT 学交互"的标准范式，16th 用它进前 2%；但 1st/5th 用纯线性就夺冠/进前 5。**裁决**：混合不是必需；当趋势/季节结构可显式建模时，纯线性的可控性更好。置信度：中。

### 事件：无奖金的分享文化与被点名的泄漏（304353、305266；置信度中）

40th 承认 Boltzmann 集成可行是因为"很多人分享了接近顶部的 notebook"，这在高奖金比赛里不现实；同时有帖子点名 top-competitors 的 notebook 存在数据泄漏。**裁决**：TPS 这类无奖金赛的免费集成素材不可迁移到高奖金赛；使用公开 notebook 前需做泄漏审计。置信度：中。

## 4. 证据分级

| 断言 | 等级 | 说明 |
| --- | --- | --- |
| 1st 的公榜/私榜反差与特征设计 | 自述（含公榜名次） | 中高 |
| 40th 的 Boltzmann 形式与参数行为 | 自述（公式明确） | 中 |
| 16th 的 277 名跃迁与特征尝试 | 自述 | 中 |
| 舍入提分 | 71 票专帖 + 多方案实践 | 中高 |
| 公榜结构（2019Q1） | 1st 自述 + 社区共识 | 中高 |
| notebook 泄漏指控 | 单帖（未逐条核查） | 低—中 |

## 5. 悬案与缺口（登记）

- 2nd–4th、6th–15th 方案未收录；"Minimum linear regression"（5th）详情仅在索引；
- notebook 泄漏指控未逐条核查；
- 归档唯一图为社区 meme（非分析图）；
- **图证缺口**：无技术/分数类图证。

## 6. 图表证据

![社区热帖 meme](../../intel/tabular-playground-series-jan-2022/bodies/298446_img/01.jpg)

**图 1**（topic 298446，224 票 / 153 评论）：本届最高票帖的社区 meme——TPS 系列的参与氛围注脚，非技术图证（本场无技术类归档图）。

## 7. 出处

- 1st 高级线性模型（111 票 / 42 评论）：https://www.kaggle.com/competitions/tabular-playground-series-jan-2022/discussion/304355
- 40th Boltzmann 集成（16 票）：https://www.kaggle.com/competitions/tabular-playground-series-jan-2022/discussion/304353
- 16th 混合模型（25 票 / 9 评论）：https://www.kaggle.com/competitions/tabular-playground-series-jan-2022/discussion/304413
- 混合模型与往届先例（33 票）：https://www.kaggle.com/competitions/tabular-playground-series-jan-2022/discussion/298196
- 方案汇编（15 票）：https://www.kaggle.com/competitions/tabular-playground-series-jan-2022/discussion/304381
- 舍入为何提分（71 票）：https://www.kaggle.com/competitions/tabular-playground-series-jan-2022/discussion/301249
- SMAPE 计算（81 票）：https://www.kaggle.com/competitions/tabular-playground-series-jan-2022/discussion/298201
- 热帖 meme（224 票 / 153 评论）：https://www.kaggle.com/competitions/tabular-playground-series-jan-2022/discussion/298446
- top notebook 数据泄漏指控（11 票 / 10 评论）：https://www.kaggle.com/competitions/tabular-playground-series-jan-2022/discussion/305266
