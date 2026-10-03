# Playground Series S3E15（临界热通量预测）轻量深读（Tier B）

> 赛事：Playground ｜ 主题 tabular（科学实验回归，含大量缺失）｜ 693 队 ｜ 标准赛 ｜ 指标：RMSE
> 材料基础：`digests/playground-series-s3e15.md`（6 篇正文：1st 414048 / 2nd 413826 / 5th 413742 / 14th 413749 / 插补技术 410645 / 资源合集 410613；59 条主题索引）+ 7 张归档图
> 轻读时间：2026-10（Tier B B14）

## 1. 一句话重述与数字账

从实验参数预测临界热通量 CHF（RMSE），数据含大量缺失。本场的关键不是模型而是**插补**：原始数据集里存在大量确定性关系——**每位作者只用一种几何、D_h 与 D_e 一一对应、某些压力/长度组合唯一**——于是前列方案用"查表 + 最近邻回退"做规则插补（5th 的"没有插补器的插补"），再配合**原数据只入训练不入验证**、领域范围裁剪与多样集成。1st 的单模 CV 0.0730、集成后 0.07265；2nd 的未选版本本可夺冠。

| 关键数字 | 值 | 来源 |
| --- | --- | --- |
| 1st（414048） | 多样集成（树/神经网络/线性/KNN，即使单模更弱）；领域知识插补 + **按 author 的取值范围裁剪降噪**；author/geometry 类别编码；迭代树插补；10 折 CV 集成 RMSE **0.07265 ± 0.00202**（单模最好 0.0730）；失败：目标裁剪、author/geometry one-hot、PCA、AE、±3σ 全特征裁剪（CV 0.069 但榜更差）；**有私榜更好但 CV 更差的提交未选** | 414048 |
| 2nd（413826） | 只用 GBDT；先按 author 分组均值插补 + FLAML LGBM（CV 0.0733）；随后发现原始数据的唯一对/三元组 → **按原数据查找插补**；部分剩余缺失用 MICE（miceforest/missingpy/CatBoost-MICE）；把插补值四舍五入到原数据唯一值反而更差；最终 LGBM+XGB 集成；**未选的"原数据过采样"版本本可拿第 1** | 413826 |
| 5th（413742） | "Imputation Without Any Imputers"：用 groupby 发现规则（author↔geometry、D_h↔D_e、chf+length↔geometry、length↔author 等），逐条查原表 + 最近邻回退，迭代补齐；圆柱几何 FE（表面积/体积差、压力·质量流·chf 的无量纲组合）；Ridge（带截距 + 允许负权重）融合；原数据仅训练；Optuna | 413742 |
| 14th（413749） | hillclimbers（负权重爬山）；自己的模型用公开预处理+手动调参；**自己的模型私榜 0.072698 优于最终提交 0.072741（但 CV 更低，未选）**；指出公开 notebook 过度依赖 XGB/CatBoost/LGBM | 413749 |
| 插补与领域资源 | 插补技术 + 代码（47 票）；基础 FE/插补思路（31 票）；CHF 关联式（29 票 / 29 评论）；字段字典（25 票）；"Peculiar Findings"（21 票）；原数据 vs 竞赛数据范围对比 | 410645 / 411353 / 410793 |

## 2. 逐方案对照矩阵

| 维度 | 1st | 2nd | 5th | 14th |
| --- | --- | --- | --- | --- |
| 插补 | 领域裁剪 + 迭代树 | 原数据查表 + MICE | **纯规则查表 + 最近邻** | 公开预处理 |
| 模型 | 树+NN+线性+KNN 多样集成 | LGBM+XGB | 多子集 Ridge 融合 | hillclimbers 负权重 |
| 原数据 | 仅训练 | 查表 + 过采样实验 | 仅训练 | 公开方案 |
| 结果 | CV 0.07265 | 私榜 2nd（未选版可第 1） | 5th | 私 0.072698（未选） |

## 3. 共识、分歧与裁决

### 共识一：用原始数据的关系表做规则插补，远胜通用插补器（5th、2nd、1st；置信度高）

5th 完全不用 imputer、自写查表规则即进前 5；2nd 从分组均值升级到唯一对/三元组查找；1st 用 author 范围裁剪。**裁决**：先挖掘原始数据中的确定性映射（作者-几何-尺寸），再做查表插补；通用 MICE 只是兜底。置信度：高。

### 共识二：原数据加入训练、但不参与验证（1st、2nd、5th；置信度中高）

与 S3E3/S4E1/S3E11 同型：原数据只作为训练补充，CV 只在竞赛数据上。**裁决**：标准协议；同时注意原数据与合成数据的分布差异。置信度：中高。

### 共识三：多样集成优于同质 GBDT（1st、14th；置信度中高）

1st 的单模 0.0730 → 集成 0.07265；14th 批评公开 notebook 全是 XGB/CatBoost/LGBM，自己专做多样性。**裁决**：该数据下树+NN+线性+KNN 的异质集成有稳定增益。置信度：中高。

### 事件一：提交选择失血是全场共性（2nd、1st、14th；置信度高）

2nd 的未选版本本可第 1；1st 有私榜更好但 CV 更差的提交未选；14th 的私榜 0.072698 未提交。**裁决**：小数据回归 + 洗牌场景下，"选哪两份"与建模同等重要；应同时保留"CV 最优"与"稳健/异质"两种提交。置信度：高。

### 事件二：过度依赖公开 notebook 的同质化（14th、413749；置信度中）

14th 指出公开方案几乎全是三大 GBDT；本场插补才是差异化来源。**裁决**：当公开方案集中在同质模型时，差异化应投向数据理解（插补/领域裁剪）。置信度：中。

## 4. 证据分级

| 断言 | 等级 | 说明 |
| --- | --- | --- |
| 5th 的规则插补与映射清单 | 自述（可复现规则） | 高 |
| 2nd 的原数据查找插补与未选版本 | 自述 + 分数截图 | 中高 |
| 1st 的多样集成与 CV | 自述 + 提交截图 | 中高 |
| 14th 的负权重 hillclimbers | 自述 + 权重图 | 中 |
| 原数据确定性关系 | 多帖互证（5th/2nd/1st） | 高 |

## 5. 悬案与缺口（登记）

- 3rd/4th、6th–13th 方案未收录；
- 插补技术贴（410645）的完整清单未细读；
- 洗牌幅度的量化未给出；
- **图证缺口**：无（7 张图，本深读内嵌 2 张）。

## 6. 图表证据

![hillclimbers 集成结构](../../intel/playground-series-s3e15/bodies/413749_img/01.png)

**图 1**（topic 413749，14th）：hillclimbers 集成示意——自己的模型（私 0.072698）与三个公开模型融合后最终提交私 0.072741，前者反而更好但被弃选。

![1st 的提交对比](../../intel/playground-series-s3e15/bodies/414048_img/01.png)

**图 2**（topic 414048，1st）：三个候选提交的分数（公/私）与勾选状态——被选中的两份（0.072595/0.075374、0.072485/0.075272）与未选的 0.072429/0.075502。

## 7. 出处

- 1st 多样集成（26 票 / 8 评论）：https://www.kaggle.com/competitions/playground-series-s3e15/discussion/414048
- 2nd 原数据的力量（29 票 / 12 评论）：https://www.kaggle.com/competitions/playground-series-s3e15/discussion/413826
- 5th 没有插补器的插补（26 票 / 16 评论）：https://www.kaggle.com/competitions/playground-series-s3e15/discussion/413742
- 14th hillclimbers（22 票 / 5 评论）：https://www.kaggle.com/competitions/playground-series-s3e15/discussion/413749
- 插补技术与代码（47 票 / 13 评论）：https://www.kaggle.com/competitions/playground-series-s3e15/discussion/410645
- 资源合集（52 票）：https://www.kaggle.com/competitions/playground-series-s3e15/discussion/410613
- 基础 FE/插补思路（31 票 / 16 评论）：https://www.kaggle.com/competitions/playground-series-s3e15/discussion/411353
- CHF 关联式（29 票 / 29 评论）：https://www.kaggle.com/competitions/playground-series-s3e15/discussion/410793
