# Playground Series S5E5 轻量深读（Tier B）

> 赛事：Playground ｜ 主题 tabular（卡路里消耗回归，全数值特征无缺失）｜ 4316 队 ｜ 标准赛 ｜ 指标：RMSLE
> 材料基础：`digests/playground-series-s5e5.md`（6 篇正文：1st 582611 / 2nd 582700 / 6th 582518 / 7th 582591 / RMSLE 集成方法 576111 / 往届方案洞察 576731；80 条主题索引）+ 7 张图
> 轻读时间：2026-10（Tier B B06）

## 1. 一句话重述与数字账

预测运动卡路里消耗（RMSLE）。真正的考点是**"在 log 空间做集成"**（RMSLE = log1p 空间的 RMSE）：选手把预测/权重/Ridge/Hill Climbing 全部搬到 `log1p` 空间，再 `expm1` 还原；以及用**残差堆叠（模型叠模型）**制造多样性。

| 关键数字 | 值 | 来源 |
| --- | --- | --- |
| RMSLE 集成（140 票） | **log1p → 加权平均 → expm1** 是 RMSLE 的正确集成方式（与 MSE 的算术平均、MAE 的中位数对应）；Ridge/Hill Climbing 也应先在 `log1p` 空间用 RMSE 目标拟合，再对 test 预测应用权重并还原 | 576111 |
| 1st（582611） | GPU Hill Climbing：把数百个 GBDT/NN/cuML 模型喂进 HC，最终选 **7 个**（3 个 XGB-cuML-TE 各 1/12、XGB-product 1/4、CatBoost-binned 1/6、NN-over-LR 1/6、XGB-over-NN 1/6）；最终 CV 0.05880 / pub 0.05677 / **priv 0.05841**；**XGB+cuML TargetEncoder 单模 CV 只有 0.06XX 却贡献 25% 权重**（"多样性 > 单模分数"：CV 0.05890→0.05880、priv 0.05847→0.05841）；CatBoost 侧做了 9 等宽分箱 + log1p 分箱 + 两两组合（81 类）+ 26 个 groupby z-score 特征（如"40 多岁男性中该人体重的 z 分数"）；**残差堆叠**：NN 学 LinearRegression 的残差（0.0608→0.0599）、XGB 学 NN 的残差；**"锦上添花"**：用 100% 训练数据重训、迭代数取 5 折早停均值×1.25（=1/(K−1) 更多），沿用 HC 权重 + 多种子平均 | 582611 |
| 2nd（582700） | 两个提交：74 OOF 的 Ridge 版，与 **11 模型 HC（仅正权重）**版——后者含 2 AutoGluon、2 CatBoost（无 FE）、LGBM+TE、CatBoost+TE、LGBM-goss-huber、LinearRegression、ResMLP、LNN，以及"CatBoost 先用分箱目标训分类器概率、再在残差上训第二个 CatBoost"（cdeotte 思路）；主题即"Trust CV and diversity" | 582700 |
| 6th（582518） | 30 模型；**Ridge 集成 CV 0.05884 / pub 0.05669 / priv 0.05846（第 6）击败 HC 集成 CV 0.05879 / 0.05670 / 0.05848（约 10–13 名）**——HC 的 CV 更高但私榜更差；图 1 显示 HC 迭代中含**负权重**（-0.066、-0.057） | 582518 |
| 7th（582591） | 几乎不做预处理（只把 Sex 转整数）；主力 CatBoost；AutoGluon 本场不具竞争力；集成器试验中 HC 的 CV 最好但最终 **Ridge 胜出**；有一个"用 AutoGluon 当集成器"的提交本可第 3，但因 CV 与 LB 都不亮眼而未选；明确反对盲混并指出公开 notebook 的权重调优在过拟合公榜 | 582591 |
| 事件 | "We have LEAK, but there is a Bonus"（31 票）讨论泄漏与加成；"Detailed Insights from Previous Competitions' Solutions"（49 票）；本场发生大洗牌（7th 自述"不意外"） | 社区 |

## 2. 逐方案对照矩阵

| 维度 | 1st | 2nd | 6th | 7th |
| --- | --- | --- | --- | --- |
| 集成器 | GPU Hill Climbing（数百模型→7） | Ridge / HC(正权重) | Ridge vs HC（Ridge 胜） | Ridge 胜（HC 的 CV 更好） |
| 特征 | product/binned/groupby z-score | 多来源（含 TE/huber/ResMLP/LNN） | — | 仅 Sex→int |
| 残差堆叠 | NN-over-LR、XGB-over-NN | CatBoost 分类概率+残差二次训练 | — | — |
| 训练技巧 | 100% 重训 + 迭代×1.25 + 多种子 | — | HC 含负权重 | — |
| 私榜 | 0.05841 | 11 模型版最高 | 0.05846 | — |

## 3. 共识、分歧与裁决

### 共识一：RMSLE 要在 log 空间集成（社区 + 全员）

140 票帖给出数学对应关系（MSE→算术平均、MAE→中位数、RMSLE→log 空间平均），1st/2nd/6th/7th 的 Ridge/HC 全部在 log1p 空间运作。**裁决**：指标是 RMSLE 时，任何"平均/加权/线性堆叠"都必须先 `log1p`；这是本场最通用的可迁移结论。置信度：高。

### 共识二：多样性来自"不同错误结构"，不是更高分数（1st/2nd）

1st 的 cuML-TE XGB 单模 CV 0.06XX（明显弱）仍占 25% 权重；2nd 的 11 模型版刻意混入 LinearRegression/ResMLP/LNN 等异质模型。**裁决**：在 log 空间等权/加权集成时，**弱但错误模式不同的成员**能提升整体；要把"成员选择"与"单模排名"解耦。置信度：高（有明确分数链）。

### 共识三：残差堆叠是低成本多样性来源（1st/2nd）

1st 的 NN-over-LR（0.0608→0.0599）与 XGB-over-NN；2nd 的"分类概率 + 残差二次 CatBoost"。**裁决**：让第二个模型只学第一个模型的残差（而非原目标）能同时提升分数与集成多样性；适合线性/树/NN 之间互补。置信度：中高。

### 分歧一：Hill Climbing vs Ridge

1st 用 HC（GPU、数百候选）夺冠；6th 的 HC CV 更高但 Ridge 私榜更好；7th 同样发现"HC 的 CV 最好但 Ridge 胜出"。**裁决**：HC 会在 OOF 上过拟合（尤其允许负权重时——6th 的日志里出现 -0.066）；**在噪声较大的 playground 赛，Ridge（或非负约束 HC）是更稳的默认**。置信度：中高。

### 事件：训练数据重训与迭代数（1st 的"icing"）

用 100% 训练数据重训、迭代数取"5 折早停均值 × 1.25"（因为数据多了 1/(K−1)），再复用 HC 权重 + 多种子平均。**裁决**：折内训练的模型在推理时"少训了 20% 数据"；按比例放大迭代数是低成本修正。置信度：中高（1st 称"在每个比赛都有效"）。

## 4. 证据分级

| 断言 | 等级 | 说明 |
| --- | --- | --- |
| RMSLE 的 log 空间集成 | 数学推导（绝对值） + 多队实践 | 高 |
| 1st 的 7 模型权重与重训技巧 | 自述 + 权重表 + 公开 notebook | 高 |
| 6th 的 Ridge vs HC 双分数 | 自述 + HC 日志截图 | 中高 |
| 2nd 的 11 模型清单 | 自述 + 公开 notebook | 中高 |
| 7th 的"AutoGluon 集成本可第 3" | 自述（事后） | 中 |

## 5. 悬案与缺口（登记）

- 3rd/4th/5th 的方案未入库；"We have LEAK, but there is a Bonus"（31 票）与"往届方案洞察"（49 票）未细读；
- 本场洗牌的幅度与原因（与 S4E11 的正例率漂移类似？）未量化；
- 1st 的数百候选模型清单与 cuML TE 的具体实现只给了 notebook 链接；
- 归档 7 图中 6 张为 6th 的提交/权重截图（含负权重日志），1 张为 RMSLE 公式图。

## 6. 图表证据

![6th 的 Hill Climbing 迭代日志](../../intel/playground-series-s5e5/bodies/582518_img/03.png)

**图 1**（topic 582518）：HC 逐轮加入模型与权重——第 3、6 轮出现**负权重**（-0.066、-0.057），CV 从 0.05885 降到 0.05881；这正是"HC 会在 OOF 上过拟合、Ridge 反而更稳"的直观证据。

## 7. 出处

- 1st GPU Hill Climbing（582611）：https://www.kaggle.com/competitions/playground-series-s5e5/discussion/582611
- 2nd Trust CV and diversity（582700）：https://www.kaggle.com/competitions/playground-series-s5e5/discussion/582700
- 6th（582518）：https://www.kaggle.com/competitions/playground-series-s5e5/discussion/582518
- 7th（26 票）：https://www.kaggle.com/competitions/playground-series-s5e5/discussion/582591
- How To Ensemble with RMSLE（140 票）：https://www.kaggle.com/competitions/playground-series-s5e5/discussion/576111
- 往届方案洞察（49 票）：https://www.kaggle.com/competitions/playground-series-s5e5/discussion/576731
