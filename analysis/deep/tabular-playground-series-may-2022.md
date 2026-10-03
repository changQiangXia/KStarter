# Tabular Playground Series May 2022（特征交互专项赛）轻量深读（Tier B）

> 赛事：Playground ｜ 主题 tabular（二分类，AUC）｜ 1151 队 ｜ 标准赛 ｜ 指标：ROC AUC
> 材料基础：`digests/tabular-playground-series-may-2022.md`（6 篇正文：1st 328336 / 4th 328441 / 5th 328553 / 541th 328355 / 三大交互 323892 / 交互 vs 相关 323766；68 条主题索引）+ 2 张归档图
> 轻读时间：2026-10（Tier B B16）

## 1. 一句话重述与数字账

一份带 `f_27` 字符串（如 "AABDABERCG"）与 f_00–f_30 数值的二分类数据，官方提示"**包含大量特征交互**"。本场的正确解法就是把这个提示做实：社区用 XGBFIR/可视化找出交互图，发现**两个连通分量**；1st 据此设计两分支网络（把交互限制在分量内），并把 `f_27` 拆成字符列与唯一字符数；还有 71 票的高价值帖把三大交互工程化为三值特征。分数高度饱和（前列 0.998+），#4 直言"大家都在 0.998，很快就失去兴趣"。

| 关键数字 | 值 | 来源 |
| --- | --- | --- |
| 1st（328336） | 二分支网络：把特征按 XGBFIR 交互图的**两个连通分量**分到左右分支（左：f_00–f_06/f_19–f_26/f_28/f_30/ch7 等；右：f_07–f_18/f_29/ch0–ch6/ch8/ch9/unique_characters/三个工程交互）；最终实现与公开 Advanced Keras notebook 基本相同；LightGBM 用 `interaction_constraints=[左, 右]` 到 LB 0.99778（未进 blend） | 328336 |
| 三大交互（323892） | 用投影图找出三区域划分：`i_02_21 = (f_21+f_02 > 5.2) − (f_21+f_02 < −5.3)`、`i_05_22 = (f_22+f_05 > 5.1) − (f_22+f_05 < −5.4)`、`i_00_01_26 = (f_00+f_01+f_26 > 5.0) − (… < −5.0)`；把连续交互变成 −1/0/+1 三值类别 | 323892 |
| 4th（328441） | 多分支 **多激活函数** 网络（swish/selu/relu 并行分支）：公 0.99826 / 私 0.99822；与公开 notebook 50-50 混合 → 公 0.99829 / 私 0.99825；自述分数饱和、竞争动力下降 | 328441 |
| 5th（328553） | CatBoost **Langevin** 模型（depth 8 + 极大正则系数，避免陷入驻点）+ Keras 结果融合 | 328553 |
| 541th（328355） | 回归/分类/指标的三重教训：PyCaret OOM → 手写 LGBM/XGB/CatBoost；`f_27` 用 `str.split('')` 拆 10 列（原字符串基数超 LGBM GPU max_bin）；f_29/f_30 实为类别；**回归输出 clip(0,1) 得 0.97952/0.97982，远好于分类的 0.92500/0.92616**；原代码误用 RMSE 指标 | 328355 |
| 社区 | "Interaction vs Correlation"（53 票）展示三区域划分；"f_27 与隐藏信息"（23 票 / 16 评论）；SHAP 交互分析（22 票）；XGB 交互（19 票）；"early stopping 用 loss/AUC/accuracy？"（45 票）；往届二分类 TPS 汇总（40 票） | 索引 |

## 2. 逐方案对照矩阵

| 维度 | 1st | 4th | 5th | 541th |
| --- | --- | --- | --- | --- |
| 交互处理 | 两连通分量分两支 | 多激活分支探索交互 | CatBoost Langevin | 手动三大交互 |
| f_27 | 字符列 + unique_characters | 同左（公开 notebook） | — | 拆 10 字符列 |
| 模型 | 二分支网络 + blend | 多分支网络 + 50-50 blend | CatBoost + Keras | LGBM/XGB/CatBoost |
| 分数 | 1st | 0.99825（私） | 5th | 0.97952 |

## 3. 共识、分歧与裁决

### 共识一：官方提示"特征交互"就是主线，交互图应当显式建模（1st、4th、323892、323766；置信度高）

1st 的图把交互限制在两个连通分量内；323892 把最强交互变成三值特征；541th 也把手写的三大交互注入特征工程。**裁决**：先找交互结构（XGBFIR/SHAP/二维投影），再用"分支/约束/显式特征"把它编码进模型。置信度：高。

### 共识二：f_27 字符串必须被拆解（1st、541th、322534；置信度中高）

拆成字符列、字符计数或唯一字符数是标准处理。**裁决**：高基数短字符串先做字符级编码，别整串进模型。置信度：中高。

### 共识三：饱和分数下模型差异极小（4th、5th、社区；置信度中）

前列全在 0.998+；4th 说"失去兴趣"。**裁决**：本场区分度低，工程细节（交互约束、blend 权重）比大改架构重要。置信度：中。

### 事件：回归 vs 分类与指标误用在 AUC 任务上的代价（541th；置信度中高）

同一集成，回归输出 0.97952、分类输出 0.92500；作者还差点用 RMSE 指标。**裁决**：AUC 任务要输出概率（回归式），并核对官方指标。置信度：中高。

### 技巧：LightGBM `interaction_constraints`（1st；置信度中）

用 [左, 右] 约束把树交互限制在分量内，LB 0.99778。**裁决**：交互约束是低成本注入先验的手段。置信度：中。

## 4. 证据分级

| 断言 | 等级 | 说明 |
| --- | --- | --- |
| 1st 的两分支结构与交互图 | 自述 + 两张图 | 高 |
| 三大交互公式 | 高票帖 + 可复现代码 | 高 |
| 4th 的多激活分支与分数 | 自述 + 结构图 | 中高 |
| 541th 的回归/分类对照 | 自述 | 中 |
| 5th 的 CatBoost Langevin | 自述（简短） | 中 |

## 5. 悬案与缺口（登记）

- 2nd/3rd 方案未收录；
- f_27 字符串的真实含义（隐藏信息）未定论；
- 饱和分数下各方案的统计显著性未评估；
- **图证缺口**：无（2 张图，本深读内嵌 1 张）。

## 6. 图表证据

![4th 的多激活分支网络](../../intel/tabular-playground-series-may-2022/bodies/328441_img/01.png)

**图 1**（topic 328441，4th）：多分支网络——三路并行全连接分支分别用 swish/selu/relu，再接第二层三路分支，拼接后收敛到单输出；不同激活函数给网络带来不同的交互探索能力。

## 7. 出处

- 1st 二分支网络（54 票 / 20 评论）：https://www.kaggle.com/competitions/tabular-playground-series-may-2022/discussion/328336
- 三大交互工程化（71 票 / 26 评论）：https://www.kaggle.com/competitions/tabular-playground-series-may-2022/discussion/323892
- 4th 多激活分支（19 票 / 2 评论）：https://www.kaggle.com/competitions/tabular-playground-series-may-2022/discussion/328441
- 5th CatBoost+Keras（17 票 / 2 评论）：https://www.kaggle.com/competitions/tabular-playground-series-may-2022/discussion/328553
- 541th 方法论复盘（6 票 / 0 评论）：https://www.kaggle.com/competitions/tabular-playground-series-may-2022/discussion/328355
- Interaction vs Correlation（53 票 / 8 评论）：https://www.kaggle.com/competitions/tabular-playground-series-may-2022/discussion/323766
- f_27 与隐藏信息（23 票 / 16 评论）：https://www.kaggle.com/competitions/tabular-playground-series-may-2022/discussion/322534
- SHAP 交互分析（22 票 / 2 评论）：https://www.kaggle.com/competitions/tabular-playground-series-may-2022/discussion/323595
- early stopping 指标选择（45 票 / 8 评论）：https://www.kaggle.com/competitions/tabular-playground-series-may-2022/discussion/326116
