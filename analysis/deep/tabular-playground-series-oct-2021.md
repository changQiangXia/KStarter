# Tabular Playground Series Oct 2021（百万行大表）轻量深读（Tier B）

> 赛事：Playground ｜ 主题 tabular（百万行二分类，AUC）｜ 1089 队 ｜ 标准赛 ｜ 指标：ROC AUC
> 材料基础：`digests/tabular-playground-series-oct-2021.md`（6 篇正文：9th 284492 / 3rd 284594 / 4th 284560 / 社区预测 278541 / 大表读取 275669 / 教程汇编 275712；80 条主题索引）+ 1 张归档图
> 轻读时间：2026-10（Tier B B16）

## 1. 一句话重述与数字账

100 万行、2.32GB train 的二分类（AUC）。本场的主题词是**"大表工程 + 强 NN"**：社区的头部帖子集中在如何分块读取（`nrows/skiprows`）、dtype 压缩、`gc`、datatable/dask/cudf 与 GPU LightGBM 的注意点；而榜单上方几乎都在"AutoML/GBDT + 一个强多输入神经网络"的组合上做文章——4th 明确说"深度学习对公榜影响很大"（NN 0.85424，加 **KMeans 特征**到 0.85503），3rd 用 25 seeds 的 NN + 伪标签，9th 则堆了 47 个基模型 + 9 个一级元模型 + LDA 二级。

| 关键数字 | 值 | 来源 |
| --- | --- | --- |
| 9th（284492） | **47 个基模型**（15 个 LightGBM ×20 seeds 平均 + 32 个来自 15 类支撑模型的变体，多数是非树模型）→ **9 个一级元模型**（3 LGBM、LR、ElasticNet、LDA、RidgeCV、CatBoost、XGB）→ **LDA 二级**；逐模型选择缩放方式；部分慢模型只用特征子集（KNN/MLP/AdaBoost/GBM），QDA 只用二元特征；借用社区特征（max/luca/mottchan features） | 284492 |
| 4th（284560） | 多输入 NN（参考公开 notebook）公榜 0.85424；加 **KMeans 方法** → 0.85503；最终集成提交；自述"深度学习对公榜影响很大（与 XGBoost/EDA 的相关性很低但涨分）" | 284560 |
| 3rd（284594） | 公开+私有 AutoML 的 GBDT（XGB/LGB/CAT/HGB）为主；**叠加一个强 NN（25 seeds）** 是"高分的小额外"；最后用**伪标签**（测试概率 <0.05→0、>0.95→1 加进训练）再涨 0.000X | 284594 |
| 大表工程（275669、275712、275930） | 75 票帖：`pd.read_csv(nrows=…)`/`skiprows=range(1,n)` 分块读、`del + gc.collect()`、datatable/dask/cudf；56 票教程汇编；25 票提醒"用 GPU 加速时注意 LightGBM 的坑" | 275669 / 275712 / 275930 |
| 特征与验证 | "不要信内置特征重要性，用 SHAP"（36 票 / 18 评论）；`feature22` 相关性专帖（27 票 / 18 评论）；"在 CV 中忽略部分 fold 等技巧"（28 票 / 14 评论）；社区预测帖（278541，9 票，预言"NN/自监督/对抗增强会出现在获胜方案"） | 索引 |

## 2. 逐方案对照矩阵

| 维度 | 9th | 3rd | 4th |
| --- | --- | --- | --- |
| 主体 | 47 基 + 9 一级 + LDA 二级 | AutoML GBDT + 1 NN | 多输入 NN + KMeans |
| 关键增益 | 极端多样性与多 seed | NN + 伪标签 | KMeans 特征 |
| 缩放/特征 | 逐模型缩放、子集训练 | — | — |
| 结果 | 9th | 3rd | 4th |

## 3. 共识、分歧与裁决

### 共识一：大表的第一道门槛是工程（读取/内存/加速）（275669、275712、275930；置信度高）

75/56/25 票的三篇帖子都围绕分块读取、dtype、gc、datatable/dask/cudf 与 GPU 注意事项。**裁决**：百万行级数据先解决 I/O 与内存，再谈模型；原型阶段可先只用 10% 数据。置信度：高。

### 共识二：强 NN 是本届的"小额外"（4th、3rd、1st 转述、278541 预言；置信度中高）

4th/3rd 都把 NN 视为拉开差距的部件；4th 的 KMeans 变体 +0.0006。**裁决**：GBDT 同质化后，异质 NN（多输入/聚类特征）是低成本增益。置信度：中高。

### 共识三：内置特征重要性不可信，用 SHAP/Boruta（276953、feature22 帖；置信度中高）

社区专门开帖警告；feature22 的相关性结构被单独立帖。**裁决**：大特征表先用 SHAP/Boruta 复核重要性，避免被内置打分误导。置信度：中高。

### 事件：极深多级堆叠可行（9th；置信度中）

47 基 → 9 一级 → LDA 二级，配多 seed 平均与逐模型缩放。**裁决**：数据量大时深堆叠不易过拟合；但需要工程化流水线支撑。置信度：中。

### 技巧：极端置信伪标签（3rd；置信度中）

仅把测试概率 <0.05 / >0.95 的样本加进训练，+0.000X。**裁决**：伪标签要只取极端置信样本以控制噪声。置信度：中。

## 4. 证据分级

| 断言 | 等级 | 说明 |
| --- | --- | --- |
| 9th 的 47+9+1 结构与图 | 自述 + 结构图 | 高 |
| 4th 的 NN/KMeans 分数 | 自述（含 notebook 链接） | 中高 |
| 3rd 的 25-seed NN 与伪标签 | 自述 | 中高 |
| 大表读取/内存教程 | 高票帖 + 可复现代码 | 高 |
| SHAP/feature22 | 高票帖 | 中高 |

## 5. 悬案与缺口（登记）

- 1st/2nd、5th–8th 方案未收录（1st 的"深度学习影响大"仅由 4th 转述）；
- KMeans 特征的确切用法未展开；
- feature22 的结构本质未定论；
- **图证缺口**：无（1 张图，本深读内嵌 1 张）。

## 6. 图表证据

![9th 的三级栈](../../intel/tabular-playground-series-oct-2021/bodies/284492_img/01.jpg)

**图 1**（topic 284492，9th）：三级结构——Base 47 模型（15 LightGBM + 15 类支撑模型的 32 个变体）→ Level 1 九个元模型 → Level 2 线性判别分析 → 提交。

## 7. 出处

- 9th（40 票 / 19 评论）：https://www.kaggle.com/competitions/tabular-playground-series-oct-2021/discussion/284492
- 3rd（31 票 / 5 评论）：https://www.kaggle.com/competitions/tabular-playground-series-oct-2021/discussion/284594
- 4th（16 票 / 9 评论）：https://www.kaggle.com/competitions/tabular-playground-series-oct-2021/discussion/284560
- 百万行读取（75 票 / 32 评论）：https://www.kaggle.com/competitions/tabular-playground-series-oct-2021/discussion/275669
- 大表教程汇编（56 票 / 7 评论）：https://www.kaggle.com/competitions/tabular-playground-series-oct-2021/discussion/275712
- SHAP 重要性警告（36 票 / 18 评论）：https://www.kaggle.com/competitions/tabular-playground-series-oct-2021/discussion/276953
- feature22 相关（27 票 / 18 评论）：https://www.kaggle.com/competitions/tabular-playground-series-oct-2021/discussion/275605
- CV 忽略部分 fold（28 票 / 14 评论）：https://www.kaggle.com/competitions/tabular-playground-series-oct-2021/discussion/280661
- GPU LightGBM 注意点（25 票 / 13 评论）：https://www.kaggle.com/competitions/tabular-playground-series-oct-2021/discussion/275930
