# Playground S4E9（二手车价格）轻量深读（Tier B）

> 赛事：Playground ｜ 主题 tabular（回归，MSE）｜ 3066 队 ｜ 标准赛 ｜ 指标：RMSE（六位数尺度，约 63,000）
> 材料基础：`digests/playground-series-s4e9.md`（6 篇正文：#1 95 / 交互+无泄漏 TE 63 / AutoML GP 1st 53 / 81st 51? / #4 48 / AutoML GP 3rd；80 条主题索引）+ 6 张图
> 轻读时间：2026-10（Tier B B01）

## 1. 一句话重述与数字账

合成二手车价格回归：**元集成（Ridge/爬山/NN meta）是主战场，成败取决于 OOF 是否干净（无泄漏 TE）+ 模型家族多样性 + 停止准则的"有效数字"**。指标是六位数 RMSE（~63,000），对细微 CV 过拟合极度敏感。

| 关键数字 | 值 | 来源 |
| --- | --- | --- |
| #1 | 计划中的 Ridge 集成只能第 2；最终用 Vladimir Demidov 的 NN + 4 个 OOF 特征（SVR/LGBM5/CatBoostClassifier/XGB）夺冠；NN CV 72468 < Ridge 集成，但私榜更好；其公开 notebook（CatBoostClf+LGBM1_st+LGBM5_st）私 **62957.8**（前三水平） | #1 |
| 无泄漏 TE | 5 折外层 × 5 折内层嵌套（fit_transform 只在折内），否则 OOF 污染会毁掉元模型 | 63 票帖+图 1 |
| 81st 的容差教训 | tol=1e-5：CV 72081/公 71887/私 63057（81 名）；tol=1：CV 72209/公 71901/私 **63003**（约第 5 名）——CV 更"好"反而更差 | 81st |
| #4 | 32 模型爬山集成；自己模型全用 vs 掺公共模型两套；原始数据 +~20 点；FE 提升 CV 不提升 LB | #4 |
| AutoML GP 3rd | 公共 notebook 加权 + LGBM/HGB/GB bagging；后处理把预测**四舍五入到 5 的倍数** | GP 3rd |

## 2. 逐方案对照矩阵

| 维度 | #1 | 81st | #4 | AutoML GP 3rd |
| --- | --- | --- | --- | --- |
| 集成方式 | Ridge → 最终 NN meta（含 4 个 OOF 特征） | 爬山（110 公共 OOF + 40 自训） | 爬山（32 模型×2 套） | 公共解加权 + bagged GBDT |
| 多样性 | LGBM/CatBoost 分类器/SVR/AutoGluon-FastAI | 分类→回归堆叠（50 bin NN → XGB 回归） | FM/Lasso/CatBoost/LAMA NN/AutoGluon 树 | LGBM/HGB/GB |
| TE/泄漏 | 折内 median TE（分类器用） | 强调 clean OOF | 只收带 OOF 的公共解，忽略 blender | LabelEncoder + 目标标准化 |
| 后处理 | — | — | — | 预测取 5 的倍数 |
| 关键教训 | 最高 CV 集成 ≠ 最优提交 | tol 应匹配有效数字 | "blending works, but 'blending' doesn't" | 公共解权重也可进前排 |

## 3. 共识、分歧与裁决

### 共识一：干净的 OOF 是元集成的先决条件

TE 帖给出嵌套折规范（外层 5 折 × 内层 5 折，测试集用全训练集编码）；#4 明确"没有 OOF 的公共解不用于集成"；81st 以 clean OOF + 爬山为核心。**裁决**：合成数据的 TE 泄漏会让 CV 虚涨、meta 过拟合；嵌套 TE + 只收带 OOF 的模型是硬要求。置信度：高。

### 共识二：多样性来自"家族 + 表示"

#1：树/分类器/SVR/快速 AI NN；#4：FM、xLearn FM、Lasso、AutoGluon 树、FastAI；81st：分类堆叠。**裁决**：同族多 seed 不够，跨家族 + 不同的特征表示（全类别化 vs 数值化）才产生互补。置信度：高。

### 共识三：特征工程在本场的 LB 转化率差

#1：Deotte 的强特征"对我无效"；#4：FE 提 CV 不提 LB，最终弃用；唯有原始数据有稳定增益（#4 +20 点）。**裁决**：合成数据的伪影让 FE 很容易只拟合 CV；原数据是少有的稳定外部信号。置信度：中高。

### 共识四：元模型的"停止准则"要匹配指标尺度（81st 的量化教训）

同一批模型：tol=1e-5 时 CV 更好、公榜稍好，但私榜差 50 点（约 0.1%），名次从约第 5 掉到 81。**裁决**：以"第 5 位有效数字"为停止阈值（本例 tol=1）；CV 改进低于噪声/有效数字时应视为过拟合。置信度：高（有 A/B 数字）。

### 分歧一：元模型用 Ridge、爬山还是 NN

#1：Ridge 稳，但最终 NN meta 更强；81st/#4：爬山（可用负权重，需控容差）；GP 3rd：加权。**裁决**：三者都有效，关键在 OOF 清洁与候选多样性；NN meta 适合当作"再加一层非线性"，但要防二次过拟合。置信度：中高。

### 分歧二：公共解的使用方式

#4 的立场：使用带 OOF 的公共**单模**是正当集成；"猜权重混合公共提交"（带引号的 blending）是运气游戏；GP 3rd 则直接把公共 notebook 加权进前排。**裁决**：可复用的资产是"OOF + 模型"，不是"提交分数"；使用公共解时优先纳入其 OOF 并重新寻权。置信度：中高。

### 小事实：分类器预测离群价（#1）

用 CatBoost 分类器预测超过 IQR 上界的"离群价格"，OOF 再喂给 LGBM/NN；属于"难点拆解"的回归技巧。置信度：中（单队自述）。

## 4. 证据分级

| 断言 | 等级 | 说明 |
| --- | --- | --- |
| 81st 的 tol A/B（63003 vs 63057） | 自述数字（可复算逻辑） | 中高 |
| 无泄漏 TE 的嵌套折图 | 图证 + 公开 notebook | 高（方法层面） |
| #1 的 CV-私榜散点与提交 | 图证 | 中高 |
| #4 的 32 模型集成与 +20 点 | 自述 | 中 |
| AutoML GP 的公共解加权/取整 | 自述 | 中 |
| 原始数据的增益 | 多队同向（#1 亦用两张原数据） | 中高 |

## 5. 悬案与缺口（登记）

- 2nd/3rd 主赛方案未收录；榜首两名的具体差异只有 #1 的自述（"计划中的集成会是第 2"）。
- 81st 的两套数字（公榜 71901/私 63003 vs 71887/63057）说明公私排序对容差敏感，但最终名次的官方口径未核对。
- 无泄漏 TE 的"内层再 5 折"在 20 折场景的计算成本/收益无消融。
- 原始数据的许可与两次并入（#1 的 LGBM 用了两次原数据）细节缺失。

## 6. 图表证据

![无泄漏 Target Encoding 的嵌套折](../../intel/playground-series-s4e9/bodies/533961_img/02.png)

**图 1**（topic 533961）：TE 规范——测试集用全训练集编码；训练集内部再切 5 折，Fold i 的编码只用 Fold j1..j4。**元集成防泄漏的标准图示**。

![#1 的 CV vs 私榜散点](../../intel/playground-series-s4e9/bodies/537052_img/03.png)

**图 2**（topic 537052）：SVR（最高 CV/最差私榜）→ NN/LGBM/Fastai → Ensemble（较低 CV、最佳私榜）。**"最高 CV 不等于最优提交"的直观证据**。

## 7. 出处

- #1（95 票）：https://www.kaggle.com/competitions/playground-series-s4e9/discussion/537052
- 无泄漏 TE 与交互特征（63 票）：https://www.kaggle.com/competitions/playground-series-s4e9/discussion/533961
- AutoML GP 1st（53 票）：https://www.kaggle.com/competitions/playground-series-s4e9/discussion/531884
- 81st 分类→回归堆叠：https://www.kaggle.com/competitions/playground-series-s4e9/discussion/537202
- #4 集成观：https://www.kaggle.com/competitions/playground-series-s4e9/discussion/536973
- AutoML GP 3rd：https://www.kaggle.com/competitions/playground-series-s4e9/discussion/532758
- 缺口登记：2nd/3rd 主赛方案、Warning: Average Fold RMSE 帖（63 票）
