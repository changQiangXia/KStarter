# Playground Series S4E7 - 保险交叉销售（AUC，特征仓库与"单模型够用"）

> 主题：tabular ｜ 子类：— ｜ 领域：保险（合成数据） ｜ 类别：Playground
> 截止：2024-07-31 ｜ 队伍数：2234 ｜ 机制：标准赛 ｜ 指标：ROC AUC
> 数据来源：`intel/playground-series-s4e7/`（80 条主题索引 + 6 篇 write-up 正文）

## 1. 任务与数据

- 预测目标：客户是否购买车险（AUC）；大样本合成数据 + 补充数据集（supplementary）。
- 数据评价（1st）：**CV–LB 近乎完美对应、数据量大到几乎不担心过拟合**——本场是"工程与资源管理"主导的典型。

## 2. 验证方案

- 全场统一 `StratifiedKFold(5, shuffle=True, seed=42)`；所有模型在同一折上比较（1st 强调）。
- 1st 的三态数据方案：只用竞赛数据 / 竞赛+补充数据交替 / **每折整份并入补充数据**（CV 最高）。
- 2nd：分布式 Optuna（4 台机器：2×Kaggle P100、Colab L4、本地 RTX 4070），HPO 时不载入测试集防 OOM。

## 3. 模型家族

| 方案 | 使用者层次 | 关键点 | 出处 |
| --- | --- | --- | --- |
| 多 GPU 环境 + 特征仓库（V1–V12）+ 多架构集成 | 1st | 命名规范/GitHub/实验追踪 | topic 523404 |
| 迭代式单模型推到极限（XGB→LGBM→CatBoost） | 2nd | "One model is all you need" | topic 523489 |
| AutoML GP 1st："One CatBoost Is All You Need" | 社区 | 单 CatBoost 达 0.893+ | topic 516475 |
| LightAutoML testers 3rd | 社区 | AutoML 流水线 | topic 516860 |

## 4. 关键技巧

- **特征仓库（Feature Store）**（1st）：把特征想法集中到 12 个版本（V1–V12），一次整理、反复复用；特征重要性只在一个折上用简单 CatBoost 看——低成本的取舍方式。
- **原数据/补充数据的三态对照**是 Playground 的标准实验（本场"每折全量并入"最优）。
- 交互特征（字符串拼接式类别组合）小步快跑（2nd）；TabNet/GANDALF 等 DL 可训但"贵且不赚"（2nd）——CatBoost 默认参数即 0.895+ 的传说在本场成立。
- 工程管理被提到方法级别：**文件/模型命名规范、代码自动化、GitHub 仓库、实验追踪表**——大样本场次里这直接决定实验吞吐。

## 5. 可迁移性评估

- **可直接迁移**：特征仓库模式；补充数据三态对照；统一折文件与命名规范；分布式 HPO（OOM 防护：HPO 不载测试集）。
- **需要前提**：大样本 + 多 GPU 环境；补充数据可得。
- **不建议照搬**：小数据场照抄"单模型够用"（本场结论依赖数据规模与 CV–LB 质量）；忽略工程管理的蛮力实验。

## 6. 对新手的关键启示

- 当 CV–LB 一致性极好时，比赛变成"实验吞吐之争"——**把特征与实验管理工程化**比多一个模型更值钱。
- "单模型 vs 大集成"取决于数据：2nd 与 AutoML 1st 都用单模型接近上限，但 1st 用资源碾压补足最后 0.001。
- 补充数据的用法要做对照实验（行/列/每折全量），别默认一种姿势。

## 7. 轻读结论（2026-10 补）

**一句话**：大数据 + 24 小时限时赛——**先榨干单模专属超参（CatBoost 的 Newton score_function / XGB 的 max_bin），再谈堆叠**；CV-LB 一致时比赛本质是"实验吞吐 + 资源管理"。

- Cross Sellers（132 票）：三段堆叠（分段 LGBM + LAMA 系 NN + XGB 末级）；12 版特征库；"补充数据整份进每折"CV 最高。
- AGP 1st：**一个 CatBoost，零特征工程**（GPU 全量）→ 0.89505/0.89586。
- 2nd：单 CatBoost 调参至 0.89788/0.89753；关键 = **Newton 系 score_function（NewtonCosine/NewtonL2）+ 12 leaf_estimation_iterations**、lr 0.085、1 万迭代、去重；50 轮分布式 HPO。
- 3rd：按 `Previously_Insured`×`Vehicle_Damage` 分段训 9 个 LGBM + 7 个 NN + OOF 二段堆叠 → 0.89375。
- 4th：**XGB max_bin=2^18−1**（大数据下默认 255 太小），192 vCPU 单模 60 分钟 → 0.89262；自省"先调单模超参而非堆集成"。

**裁决**：大数据赛先用 CV-LB 关系定信任框架；低基数高重要性特征优先分段建模；限时赛把特征库/命名/并行 HPO 当一等公民。

**悬案**：2nd 提到的 @paddykb trick 内容缺失；主榜与 AGP 两条赛道口径在材料中混淆；Cross Sellers 未给三策略分数字。

## 8. 图表证据

![Cross Sellers 的三段堆叠](../../intel/playground-series-s4e7/bodies/523404_img/01.png)

**图 1**（topic 523404）：LGBM/CatBoost 与 LAMA 系 NN 交叉作特征，末级 XGBoost 汇总 + 公开 kernel 并入——"树叠 NN、NN 叠树"的具体结构。

## 9. 出处

- 1st：Team Cross Sellers（特征仓库与资源管理）：https://www.kaggle.com/competitions/playground-series-s4e7/discussion/523404
- 2nd：One model is all you need：https://www.kaggle.com/competitions/playground-series-s4e7/discussion/523489
- AutoML GP 1st：One CatBoost Is All You Need：https://www.kaggle.com/competitions/playground-series-s4e7/discussion/516475
- 3rd：LightAutoML testers：https://www.kaggle.com/competitions/playground-series-s4e7/discussion/516860
- 4th：AutoGluon（max_bin 发现）：https://www.kaggle.com/competitions/playground-series-s4e7/discussion/516265
- 轻读全本：`analysis/deep/playground-series-s4e7.md`（Tier B 轻读：对照矩阵/裁决/证据分级/悬案 + 2 图证）
