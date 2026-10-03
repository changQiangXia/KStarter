# Playground Series S4E4（鲍鱼年龄回归）轻量深读（Tier B）

> 赛事：Playground ｜ 主题 tabular（生物测量回归，RMSLE）｜ 2606 队 ｜ 标准赛 ｜ 指标：RMSLE（MSLE）
> 材料基础：`digests/playground-series-s4e4.md`（6 篇正文：1st 499174 / 2nd 499698 / 3rd 499747 / 4th 499341 / 5th 499204 / 起步资源 488067；80 条主题索引）+ 0 张归档图
> 轻读时间：2026-10（Tier B B15）

## 1. 一句话重述与数字账

从长度/重量/性别等生物测量预测鲍鱼环数（年龄，RMSLE）。本场是**"AutoFE + 重集成"**的范本：1st 用 OpenFE 自动生成特征 + 逐模型序列选择（SFS）约 20 个附加特征 + WandB 贝叶斯调参 + **49 个模型的 Nelder-Mead 加权（允许负权重）**，CV 0.14514；2nd 的全自动工作流（两样本检验决定是否并入原数据 + OpenFE + AutoGluon 特征剪枝 + 最多 6 层 stacking）直接拿第 2；3rd/4th 也都是 OpenFE/AutoGluon 路线。

| 关键数字 | 值 | 来源 |
| --- | --- | --- |
| 1st（499174） | OpenFE 生成 + Sequential Feature Selection（每模型约 20 个附加特征，例：`freq(Shell_weight)`、`Whole_weight/Shucked_weight`、`log(Whole_weight)`、`residual(Whole_weight)`）；WandB Sweeps 贝叶斯调 LGBM/XGB/CatBoost/HistGB/RF；10 折；原始鲍鱼数据只进训练；AutoGluon；**49 模型 Nelder-Mead 权重（含负系数，权重和 0.997，优于非负归一化）**；单模最佳 LGBM CV 0.14611 / AutoGluon 0.14592 / 集成 **0.14514**；第二份提交不含公开 notebook，公/私榜 **0.14372/0.14379（同样第一）**；RMSLE 处理：LGBM 自定义 MSLE、XGB `reg:squaredlogerror`、其余 `log1p/expm1`；"XGB 分类器 + softmax 回归头"意外有效；失败：多项式特征、复杂 stacking、StratifiedKFold、Sex 的各种编码 | 499174 |
| 2nd（499698） | 全自动工作流：①**两样本检验**（AutoGluon 分类器 + Mann-Whitney U）判断原数据是否可分/是否该并入；②**OpenFE + AutoGluon 特征剪枝**（默认设置约 200 个特征 → 1 小时筛完，作者认为这是第 2 名的主因）；③定制 AutoGluon 自动选模，**动态 stacking 最多 6 层（实际用 5 层；3 层同样分数、5 层也不过拟合）** | 499698 |
| 3rd（499747） | 6 模型集成：AutoGluon（原始特征 / OpenFE 30 特征 / OpenFE+伪标签）+ XGB/LGB/CAT（Optuna 权重）+ 投票融合 + 公开 LGBM 集成；OpenFE 改造成 RMSLE 友好；**折内 RFE 选 30 个特征**；失败：分类代替回归、给原数据更高权重 | 499747 |
| 4th（499341） | OpenFE + log 目标 + AutoGluon（自定义 RMSLE、仅树模型）+ 与一个公开 notebook 的 50-50 平均；观察：AutoGluon 在 5–6 万行以上的数据上表现出色 | 499341 |
| 5th（499204） | 领域特征（表面积、失水率、测量比值、密度、BMI）；**15/20 折 > 5 折**；重视超参调优；融合只用**调和平均**以抗过拟合 | 499204 |
| 社区 | 起步资源（77 票）；常见坑与提示（63 票 / 22 评论）；集成权重讨论（52 票 / 14 评论）；log1p+MSE vs MSLE（42 票）；RMSLE 指标解释（37 票）；"数据与模型都可能存在系统性误差"（29 票） | 索引 |

## 2. 逐方案对照矩阵

| 维度 | 1st | 2nd | 3rd | 4th |
| --- | --- | --- | --- | --- |
| 自动 FE | OpenFE + SFS | OpenFE + AutoGluon 剪枝 | OpenFE（RMSLE 改造）+ RFE | OpenFE |
| 原数据 | 只进训练 | 两样本检验后并入 | 用（但高权重失败） | — |
| 模型 | GBDT ×5 家 + AutoGluon | 定制 AutoGluon 5 层栈 | AutoGluon×3 + XGB/LGB/CAT | AutoGluon（树）+ 公开 notebook |
| 融合 | Nelder-Mead（含负权重，49 模型） | 多层 stacking | Optuna 权重 + 投票 | 50-50 平均 |
| CV | 10 折 | AutoGluon 内部 | CV 内 RFE | — |
| 结果 | 1st | 2nd | 3rd | 4th |

## 3. 共识、分歧与裁决

### 共识一：自动特征工程（OpenFE）+ 严格特征选择是本场最大共性（1st–4th；置信度高）

四支队伍都用了 OpenFE（或定制版）并配合 SFS/RFE/代理模型剪枝；2nd 明确把"自动 FE"列为第 2 名的主因。**裁决**：手工想不出特征时，AutoFE + 剪枝是系统解；剪枝必须折内做。置信度：高。

### 共识二：RMSLE 要匹配损失函数（1st、3rd、4th、488283；置信度中高）

1st 为每个库选了对数损失（自定义 MSLE / `reg:squaredlogerror` / log1p），3rd 把 OpenFE 改造成 RMSLE 友好。**裁决**：先在目标域训练再 `expm1` 还原，或直接用 MSLE 损失；不要把 RMSLE 当普通 MSE。置信度：中高。

### 共识三：多折 + 重集成收益稳定（1st、2nd、5th；置信度中高）

1st 的 49 模型 Nelder-Mead、2nd 的 5 层 stacking、5th 的 15/20 折。**裁决**：数据量足够（5–6 万行以上）时，加深折数与集成层数都不过拟合。置信度：中高。

### 事件：负权重与"看起来不合理"的权重（1st、488409；置信度中）

1st 的 49 模型权重含负值、和 0.997，且比非负归一化更好；社区有专门的集成权重讨论（52 票）。**裁决**：权重只要在 OOF 上诚实优化、在提交上复核，就不必强加非负/归一化约束。置信度：中。

### 事件：系统性误差与预测上限（491196、1st；置信度中）

社区帖指出数据与模型都可能存在系统性误差；1st 的模型最多预测 20 环（训练最大 29），SMOTE/增广/剔除异常都让 CV 变差。**裁决**：这类上限问题不要用重采样硬治；登记为数据固有缺陷。置信度：中。

## 4. 证据分级

| 断言 | 等级 | 说明 |
| --- | --- | --- |
| 1st 的 OpenFE+SFS+49 模型权重与分数 | 自述（含具体 CV/权重细节） | 高 |
| 2nd 的自动工作流（两样本检验/多层 stacking） | 自述 | 中高 |
| 3rd/4th/5th 的配方 | 自述 | 中 |
| RMSLE 损失选择 | 多帖互证 + 高票讨论 | 中高 |
| 系统性误差 | 社区帖 | 中 |

## 5. 悬案与缺口（登记）

- 6th–10th 及之后方案未收录；
- 1st 的 49 个模型清单与负权重细节未列出；
- OpenFE 的搜索空间（2nd 的生成器细节）未完整公开；
- **图证缺口**：本场归档 0 图。

## 6. 图表证据

无可用图证（本场归档 0 图，图证缺口已登记）。

## 7. 出处

- 1st（122 票 / 51 评论）：https://www.kaggle.com/competitions/playground-series-s4e4/discussion/499174
- 2nd（12 票）：https://www.kaggle.com/competitions/playground-series-s4e4/discussion/499698
- 3rd（11 票）：https://www.kaggle.com/competitions/playground-series-s4e4/discussion/499747
- 4th（13 票）：https://www.kaggle.com/competitions/playground-series-s4e4/discussion/499341
- 5th（32 票 / 5 评论）：https://www.kaggle.com/competitions/playground-series-s4e4/discussion/499204
- 起步资源（77 票 / 31 评论）：https://www.kaggle.com/competitions/playground-series-s4e4/discussion/488067
- 常见坑与提示（63 票 / 22 评论）：https://www.kaggle.com/competitions/playground-series-s4e4/discussion/488093
- 集成权重（52 票 / 14 评论）：https://www.kaggle.com/competitions/playground-series-s4e4/discussion/488409
- log1p+MSE vs MSLE（42 票）：https://www.kaggle.com/competitions/playground-series-s4e4/discussion/488283
- 系统性误差（29 票 / 8 评论）：https://www.kaggle.com/competitions/playground-series-s4e4/discussion/491196
