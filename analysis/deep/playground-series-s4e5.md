# Playground Series S4E5（洪水概率预测）轻量深读（Tier B）

> 赛事：Playground ｜ 主题 tabular（合成数据回归）｜ 2788 队 ｜ 标准赛 ｜ 指标：R² ｜ 同期含 AutoML Grand Prix
> 材料基础：`digests/playground-series-s4e5.md`（5 篇正文：1st 509043 / 2nd Peaky Blenders 509410 / AGP 1st 500700 / AGP 2nd H2O 500549 / 首特征 566 行处；80 条主题索引）+ 6 张图
> 轻读时间：2026-10（Tier B B08）

## 1. 一句话重述与数字账

预测洪水概率（合成数据，R²）。真正的考点是**逆向合成过程**：数据由 **Poisson 生成**，一行特征的和（sum）几乎解释了全部信号；找到 sum 与"行内计数/排序"这类结构特征后，剩下的就是"多 GBM + 稳健 Ridge/线性集成"。

| 关键数字 | 值 | 来源 |
| --- | --- | --- |
| 1st（509043） | EDA 发现"**17 个原始特征中 16 个的和仍是 Poisson**"（18/19/20 个就不是）→ 锁定 **sum 为主信号**；特征：行 sum/std/max、**排序后的原始特征**、计数特征（>6/>7/>8 的个数）、目标编码、**magic feature = `train.groupby("sum")["FloodProbability"].std()`**；明确删掉原始特征/skew/kurtosis；目标变换（减去行均值 ×0.1）分离"强信号 + 噪声偏离"；30+ GBM（CatBoost/XGB/LGBM 不同特征集与 grow_policy）；集成为 **Ridge（positive=False, fit_intercept=False）**，用 **3 次重复 K 折 OOF**；融合 AutoGluon 的 OOF；最后阶段**只提交 2 次**（"CV 从第一天就与公榜高度一致，我信任 CV"）——公私榜双第 1 | 509043 |
| 2nd Peaky Blenders（509410） | 56 个模型的"blends of blends"：公共 notebook 的超参 + 自调（grow_policy/tree_method/objective/sampling_method）；最佳单模仅 0.86933 → 靠集成；LinearRegression 做一级融合，再把"不同特征子集/模型子集"的加权结果加入 OOF 池，最后对**所有特征（含集成子集特征）做前向特征选择**；未拿到 AutoGluon 的 OOF 是遗憾 | 509410 |
| AGP 1st（500700，LightAutoML testers） | 手工特征 = ambrosm 的 `fsum/fstd/fspecial1`（行和、行标准差、**"sum 是否落在 71–76"指示**）+ 行列的 skew/kurtosis + 行内各唯一值计数 + 行分位数；模型 = 近默认的 **LightAutoML TabularAutoML**（含 tuned NN/GBM 全家桶） | 500700 |
| AGP 2nd（500549，H2O DriverlessAI） | 用 H2O DriverlessAI 自动建模（特征工程与模型选择全自动），名次说明 AutoML 在本场也能进前二 | 500549 |
| 首特征帖（499274） | 把"20 个初始特征的和"与目标画散点：均值洪水概率随 sum **单调上升（0.32→0.72）**，但在 **71–76 区间出现偏离**（对应 fspecial1 指示特征）——本场最关键的一张 EDA 图 | 499274 |
| 社区 | "0.844 的一行代码"（60 票）、"沿特征轴排序当特征工程"（47 票）、"关于特征工程的有趣事实"（32 票）、"混合权重的几个迷思"（31 票）、"预测变量来自 Poisson(λ=5)"（31 票） | 社区 |

## 2. 逐方案对照矩阵

| 维度 | 1st | 2nd Peaky | AGP 1st | AGP 2nd |
| --- | --- | --- | --- | --- |
| 特征 | sum/std/max、排序、计数、TE、groupby(sum).std() | 复用 ambrosm/siukeitin + 公共 notebook | fsum/fstd/fspecial1、skew/kurt、计数、分位 | H2O 自动 |
| 模型 | 30+ GBM（多特征集） | 56 模型 | LightAutoML 全家桶 | DriverlessAI |
| 集成 | **Ridge(positive=False, no intercept) + 3×K 折 OOF** | LR + 子集加权入池 + 前向选择 | AutoML 内部 | AutoML 内部 |
| 提交纪律 | 末段仅 2 次提交 | — | — | — |

## 3. 共识、分歧与裁决

### 共识一：先逆向生成过程，再谈模型（1st/AGP 1st/首特征帖）

1st 从"和仍是 Poisson"推断生成机制并锁定 sum；AGP 1st 的 `fsum/fspecial1` 与首特征帖的曲线（含 71–76 偏离）互相印证。**裁决**：合成数据赛的第一小时应做"逐列/逐行统计 → 找与目标的单调关系 → 猜生成式"；本场 sum 是主信号、其余是噪声偏离。置信度：高（图 1 + 多队独立）。

### 共识二：特征工程 > 模型调参（1st/2nd/AGP 1st）

1st 前 10 天不做任何调参、只做特征与集成；2nd 的最佳单模只有 0.86933，靠 blends of blends 提升；AGP 1st 也以手工特征为主。**裁决**：当主信号是"行级聚合量"时，行内排序/计数/分位等结构特征比换模型更值钱。置信度：高。

### 共识三：线性/Ridge 集成是这类合成回归的稳定器（1st/2nd）

1st 用 Ridge(positive=False, fit_intercept=False) + 3 次重复 K 折 OOF；2nd 用 LR + 子集加权 + 前向选择。**裁决**：高相关模型池上做"无截距非负/自由权重"的线性组合是低成本高稳健的方案；K 折重复保证 OOF 稳定。置信度：高。

### 分歧一：AutoGluon 的地位

1st 明确把 AutoGluon 的 OOF 纳入最终 Ridge 集成（并说最后阶段的 3 份 AG OOF 有增益）；2nd 想用但拿不到 OOF。**裁决**：AutoML 的输出应作为"另一个模型"进入集成池而非直接提交；OOF 是前提。置信度：中高。

### 事件：信任 CV 与提交纪律（1st）

1st 说"CV 从第一天就与公榜一致，我信任 CV"，18 日之后**只提交 2 次**仍拿公私双第 1；2nd 则做了较多试提交。**裁决**：当 CV-LB 稳定一致时，把提交次数留给最终选择（避免过拟合榜面）。置信度：高。

## 4. 证据分级

| 断言 | 等级 | 说明 |
| --- | --- | --- |
| 1st 的 Poisson 发现、magic feature 与 Ridge 集成 | 自述 + 公开代码 | 高 |
| 首特征帖的 sum-目标曲线（含 71–76 偏离） | 图 + 数据 | 高 |
| 2nd 的 56 模型 blends-of-blends | 自述 + notebook 引用 | 中高 |
| AGP 1st 的 fsum/fspecial1 特征 | 自述 + 代码 | 中高 |
| "混合权重的迷思" | 社区帖 | 中 |

## 5. 悬案与缺口（登记）

- 3rd–10th 的方案未入库；"0.844 的一行代码"（60 票）与"沿特征轴排序"（47 票）未细读；
- 1st 的 30+ GBM 具体特征组合未逐一列出；
- AutoGluon 的多份 OOF 对最终集成的单独贡献未量化；
- 归档 6 图：首特征帖的 sum-目标曲线（图 1）与 H2O 的 5 张流程图为关键图证。

## 6. 图表证据

![洪水概率 vs 行内特征和](../../intel/playground-series-s4e5/bodies/499274_img/01.png)

**图 1**（topic 499274）：均值洪水概率 vs 20 个初始特征之和——整体单调上升（0.32→0.72），但在 **71–76 区间出现明显偏离**（红点）。这既是"sum 是主信号"的证据，也解释了 `fspecial1`（sum∈[71,76] 指示）为何成为全场通用特征。

## 7. 出处

- 1st（106 票）：https://www.kaggle.com/competitions/playground-series-s4e5/discussion/509043
- 2nd Peaky Blenders（509410）：https://www.kaggle.com/competitions/playground-series-s4e5/discussion/509410
- AGP 1st（35 票）：https://www.kaggle.com/competitions/playground-series-s4e5/discussion/500700
- AGP 2nd H2O（36 票）：https://www.kaggle.com/competitions/playground-series-s4e5/discussion/500549
- 首个有用的特征（499274）：https://www.kaggle.com/competitions/playground-series-s4e5/discussion/499274
- Poisson 讨论（31 票）：https://www.kaggle.com/competitions/playground-series-s4e5/discussion/499244
