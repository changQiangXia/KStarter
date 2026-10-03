# Playground Series S3E17（机器故障预测）轻量深读（Tier B）

> 赛事：Playground ｜ 主题 tabular（设备故障二分类，合成数据）｜ 1502 队 ｜ 标准赛 ｜ 指标：ROC AUC
> 材料基础：`digests/playground-series-s3e17.md`（6 篇正文：领域知识 416765 / 11th 419643 / 17th 419648 / 4th 419698 / 3rd 419730 / 赛制反馈 417785；80 条主题索引）+ 2 张归档图
> 轻读时间：2026-10（Tier B B13）

## 1. 一句话重述与数字账

由物理仿真数据（UCI Predictive Maintenance 的合成版）预测机器故障（AUC）。数据 136,429 行 × 14 列：5 个故障类型二元标签（TWF/HDF/PWF/OSF/RNF）+ 总故障标签，产品分 L/M/H 三型。本场的决定性细节是**"把 Product ID 当类别特征正确接入"（17th 单加 +0.013）**与**重复行的行级目标编码**（4th 的"target encoding rows"）；模型侧反而是老结论——单 CatBoost 与 90% AutoML 集成能拿到几乎相同的分数（私榜 0.98426 vs 0.98541）。

| 关键数字 | 值 | 来源 |
| --- | --- | --- |
| 领域知识（416765） | 字段字典；故障计数极端不均：**TWF 134,685** vs HDF 634 / OSF 527 / RNF 305 / PWF 278；RPM 由 2860W 功率 + 正态噪声推出；扭矩非负；产品类型越"高"越耐受故障条件 | 416765 |
| 11th（419643） | **MultilabelStratifiedKFold（10 折）**保证 5 种故障比例在折间保持；原数据/编码/缩放全部放进 CV pipeline（防泄漏）；CatBoostEncoder 用于除 CatBoost 外的全部模型；新特征仅 1 个 `IsFailure`（只给 GaussianNB）；6 模型（GNB/RF/XGB/LGBM/LGBM-dart/CatBoost），GBDT 用 Optuna，NB/RF 只做校准；LR 学投票权重，CV **0.98006**；最佳提交实际只用了部分模型 | 419643 |
| 17th（419648） | **单 CatBoost**：CV 0.98125 / 公 0.97764 / 私 **0.98426**；train+原始 train（+0.002）、去重；3 个比值/乘积特征（温度比、扭矩×转速、扭矩×磨损；公榜 +0.004、私榜约 0）；LabelEncoder、不做不平衡处理、不缩放；80/20 holdout + 全量重训；Optuna+WandB；**Product ID 作为 `cat_features`（+0.013）**；CatBoost CPU（确定性）> GPU；lr=0.025、调大 border_count | 419648 |
| 4th（419698） | 先做 4 个公开 notebook 的排名混合（约前 30）；核心技巧 = **行级 target encoding**：对特征完全相同的重复行（train 内、甚至 train-test 重叠）统计目标均值与出现次数，做成两列新特征，且必须 out-of-sample；只对"测试集中能在训练集找到同特征行"的样本应用 | 419698 |
| 3rd（419730） | 90% 权重来自多个 AutoML（LightAutoML / Statmining ISoft / H2O / LazyClassifier / FLAML，前三个贡献最大）+ 10% 两个最佳公开提交的元模型；4 核 8G 约 6 小时；公 0.97921 / 私 **0.98541**；伪标签略有增益 | 419730 |
| 社区 | 不平衡策略讨论（37 票 / 22 评论）；Product ID 讨论（18 票 / 12 评论）；重复观测（15 票）；`.predict` vs `.predict_proba`（16 票）；"赛制多样性请求"（45 票 / 26 评论，要求加入时序/代码赛/匿名原数据） | 索引 |

## 2. 逐方案对照矩阵

| 维度 | 11th | 17th | 4th | 3rd |
| --- | --- | --- | --- | --- |
| 模型 | 6 模型 + LR 权重 | **单 CatBoost** | 4 公开 notebook 排名混合 + CatBoost | 5 个 AutoML + 公开提交元模型 |
| 关键动作 | 多标签分层 10 折 + pipeline 内编码 | **pid 作 cat_features（+0.013）** | **重复行 TE + 计数** | AutoML 组合（前三个贡献最大） |
| 原数据 | pipeline 内加入 | 加入（+0.002） | 公开方案派生 | — |
| 私榜 | — | 0.98426 | — | **0.98541** |
| 启示 | 折间比例控制 | 类别接口决定成败 | 重复行可挖 | AutoML 也能进前三 |

## 3. 共识、分歧与裁决

### 共识一：类别特征接口是本场最大单点（17th、11th、社区 Product ID 帖；置信度高）

17th 把 Product ID 正确传入 CatBoost `cat_features` 单加 0.013；11th 把所有编码（CatBoostEncoder）放进 pipeline 防泄漏。**裁决**：本场"pid/Type 如何编码"比模型选择重要；任何编码都应在折内拟合。置信度：高。

### 共识二：原始数据加入训练有稳定小增益（17th +0.002、11th；置信度中高）

与 S3E3/S4E1 同型：合成数据赛的原始数据集值得并入训练，但要防止 CV 泄漏（折内加入/只在合成折评估）。置信度：中高。

### 共识三：重复行的行级统计是可挖的捷径（4th、社区重复行帖；置信度中）

特征完全相同的行（含 train-test 重叠）标签不一致 → 用 out-of-sample 的行级 TE + 出现次数。**裁决**：合成数据的"重复行"是常见的可利用结构；必须做 out-of-sample 以免泄漏。置信度：中。

### 分歧：单模 vs AutoML 大集成（17th/11th vs 3rd；置信度中）

17th 单 CatBoost 私 0.98426、3rd 的 5 个 AutoML 元模型私 0.98541、11th 的 6 模型 CV 0.98006。**裁决**：差距在千分位量级，主要差异来自特征与编码；AutoML 可以作为省力路径，但不是决定因素。置信度：中。

### 事件：社区对 Playground 赛制同质化的反馈（417785；置信度中高）

45 票帖请求增加多样性（时序、代码赛、匿名原数据、关闭讨论区做实验）。**裁决**：Playground 系列的"原数据→合成数据 + 单一表格任务"模式已被社区认为单调；该反馈与后续赛季（S4/S5/S6 引入代码赛、时序等）方向一致。置信度：中高。

## 4. 证据分级

| 断言 | 等级 | 说明 |
| --- | --- | --- |
| 17th 的 pid +0.013 与全体分数 | 自述（含参数） | 中高 |
| 4th 的重复行 TE 方法 | 自述（含示例表） | 中 |
| 11th 的 CV 协议与 6 模型 | 自述（含代码） | 中高 |
| 3rd 的 AutoML 组合与分数 | 自述 | 中 |
| 领域知识与故障分布 | 高票帖 + 图 | 高 |
| 赛制反馈 | 45 票帖 | 中 |

## 5. 悬案与缺口（登记）

- 1st/2nd、5th–10th 方案未收录；
- 重复行 TE 的量化增益未给出；
- AutoML 的具体权重与特征处理未展开；
- **图证缺口**：无（2 张分布图已内嵌）。

## 6. 图表证据

![产品类型分布](../../intel/playground-series-s3e17/bodies/416765_img/01.png)

**图 1**（topic 416765）：产品类型分布——L 60% / M 30% / H 10%，不同型别对故障条件的耐受度不同。

![故障类型计数](../../intel/playground-series-s3e17/bodies/416765_img/02.png)

**图 2**（topic 416765）：故障点计数极度不均——TWF 约 13.5 万，其余四类仅数百，是多标签分层 CV 的必要性来源。

## 7. 出处

- 领域知识与字段表（65 票 / 29 评论）：https://www.kaggle.com/competitions/playground-series-s3e17/discussion/416765
- 11th 方案（44 票 / 36 评论）：https://www.kaggle.com/competitions/playground-series-s3e17/discussion/419643
- 17th 单 CatBoost（14 票）：https://www.kaggle.com/competitions/playground-series-s3e17/discussion/419648
- 4th 行级 TE（5 票）：https://www.kaggle.com/competitions/playground-series-s3e17/discussion/419698
- 3rd AutoML（31 票）：https://www.kaggle.com/competitions/playground-series-s3e17/discussion/419730
- 赛制多样性请求（45 票 / 26 评论）：https://www.kaggle.com/competitions/playground-series-s3e17/discussion/417785
- 不平衡策略（37 票 / 22 评论）：https://www.kaggle.com/competitions/playground-series-s3e17/discussion/416923
- Product ID 讨论（18 票 / 12 评论）：https://www.kaggle.com/competitions/playground-series-s3e17/discussion/416774
- 重复观测（15 票）：https://www.kaggle.com/competitions/playground-series-s3e17/discussion/416919
