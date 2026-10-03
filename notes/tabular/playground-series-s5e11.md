# Playground Series S5E11 - 贷款违约预测（合成数据指纹之战）

> 主题：tabular ｜ 子类：— ｜ 领域：金融（合成数据） ｜ 类别：Playground
> 截止：2025-11-30 ｜ 队伍数：3724 ｜ 机制：标准赛 ｜ 指标：ROC AUC
> 数据来源：`intel/playground-series-s5e11/`（70 条主题索引 + 6 篇 write-up 正文）

## 1. 任务与数据

- 预测目标：贷款违约概率（二分类 AUC）；合成金融数据 + 原始生成源数据。
- 本场是"合成器指纹挖掘"的代表作：高基数特征（annual_income、loan_amount 等）的小数位、分箱方式、与原始取值的对应关系都携带信号；数字特征与组合特征的 **TE/CE（目标/计数编码）** 是主要战场。
- 本场往后成为 S6E1/S6E3 的方法源（S6E1 亚军明确引用本场 1st/2nd 的特征工程）。

## 2. 验证方案

- 主流 5 折固定 CV；1st 用 100 模型堆叠；**单模即达亚军水平**（CV 0.92818 / LB 0.92923）。
- 2nd："7 模型 ridge，但 1 个 LGBM 也足够拿第 2"——单模与集成差距极小，说明特征工程吃掉了大部分收益。
- 社区共识：blender notebook 私榜意外地好，但不可依赖；CV 与 LB 相关性良好时以 CV 决策。

## 3. 模型家族

| 方案 | 使用者层次 | 关键点 | 出处 |
| --- | --- | --- | --- |
| 100 模型集成（XGB/LGBM/CatBoost/RealMLP/TabM/DANet/Resnet…） | 1st | 特征工程为核心，单模即亚军 | topic 647362 |
| 7 模型 Ridge（5×LGBM + TabM + RealMLP） | 2nd | 重正则 LGBM；单模同样第 2 | topic 647288 |
| (XGB+LGBM+TabM)×5 seeds + AutoGluon | 5th | 种子平均 + AutoML 多样性 | topic 647359 |
| 多数派：两三大件 + 集成 | 4th/6th | 稳健配方 | topic 647417、647305 |

## 4. 关键技巧

- **特征工程清单**（1st，可当模板）：基特征两两组合 + TE/CE；数字特征的小数位；数字位之间的组合（2/3/4 元）+ TE/CE；round 特征；数字位与基特征的混合组合；在**原数据**上对基特征+数字位做 TE；用 `employment_status`、`debt_to_income_ratio` 等做替代目标的 TE。
- **高基数先分箱再编码**（2nd）：quantile/uniform/round/整除/取整五种离散化，各自做 TE 都涨 CV——编码前的粒度设计比编码器选择更重要。
- **过采样比例特征**：train 频率 / original 频率 = 生成器对该值的过采样程度（2nd 的 ratios）。
- 重正则化 LGBM（低 max_depth、低 colsample）收益显著；原始数据"拼行"本场无帮助（与"拼列/编码"形成对照）。

## 5. 可迁移性评估

- **可直接迁移**：数字位/round 特征族；分箱 × 目标编码的组合矩阵；原数据频率比；单模先压满特征工程再谈集成。
- **需要前提**：原数据可得（合成赛）；高基数特征存在。
- **不建议照搬**：默认原数据拼行有效（本场无效）；在单模已接近上限时继续堆数百模型（收益极小且过拟合 CV 的风险上升）。

## 6. 对新手的关键启示

- 合成数据的竞争越来越像"逆向生成器"：小数位、分箱、频率比都是指纹——学会系统性地枚举特征家族。
- 先做"单模最强"，它常常已经接近最终名次；集成是保险而不是魔法。
- 分箱粒度是超参：同一列做 5 种离散化分别编码，比在一个编码器上调半天更有效。

## 7. 出处

- 1st：A lot of features, a lot of models…：https://www.kaggle.com/competitions/playground-series-s5e11/discussion/647362
- 2nd：7 models, but 1 was also enough：https://www.kaggle.com/competitions/playground-series-s5e11/discussion/647288
- 5th：(XGB+LGBM+TabM)×5 seeds + AutoGluon：https://www.kaggle.com/competitions/playground-series-s5e11/discussion/647359
- 4th：https://www.kaggle.com/competitions/playground-series-s5e11/discussion/647417
- 6th：https://www.kaggle.com/competitions/playground-series-s5e11/discussion/647305
