# Playground Series S5E3（降雨预测）轻量深读（Tier B）

> 赛事：Playground ｜ 主题 tabular（二分类，时间序列合成数据）｜ 4381 队 ｜ 标准赛 ｜ 指标：ROC AUC
> 材料基础：`digests/playground-series-s5e3.md`（6 篇正文：2nd 571176 / 54th 571133 / 18th 571021 / 37th 571139 / Linear SVC 568268 / 全方案归档 571015；80 条主题索引）+ 3 张归档图
> 轻读时间：2026-10（Tier B B13）

## 1. 一句话重述与数字账

用 6 年逐日天气预测是否降雨（AUC），**公榜只有 146 行**、私榜是另外两个新年度——本场因此成为"洗牌 + 探榜"的极端案例：公开榜出现过 0.961（RAPIDS KNN starter）甚至 10 份 AUC=1.0 的提交，而真正的胜负手是**"原始数据怎么接入"**。2nd 用同一份原始数据做两种接法：拼成新行（XGB 私榜 0.90317）与 merge 成新列（RAPIDS SVC 单模私榜 0.90610，直接第 2）；他未提交的三模型等权融合私榜 0.90728 本可第 1。

| 关键数字 | 值 | 来源 |
| --- | --- | --- |
| 2nd（571176） | **零特征工程**（小数据防过拟合）；GroupKFold 6 折（按年）；原数据两种接法：① **新行**（concat）→ XGB CV 0.893 / 公 0.848 / 私 **0.90317**；TabPFN CV 0.894 / 公 0.867 / 私 0.90193；两模型等权 → 私 0.90474（11th）；② **新列**（merge）→ RAPIDS SVC（poly、degree=1、C=0.1）CV 0.896 / 公 0.852 / 私 **0.90610**（单模即第 2）；三模型等权 → 私 **0.90728（本可第 1，未提交）**；最终提交的六模型等权 CV 0.900/0.901、私 0.90604/0.90599 → 第 2 | 571176 |
| 54th（571133） | 嵌套式"留一年"分组 CV；对抗验证发现加了原数据后时间特征会让模型区分 train/test → **弃用时间特征**（显著提分）；FE = 比值特征 + 年度相对温度（样本温度−当年均温）等；各模型 CV 0.886–0.896 → 调参后 0.894–0.9003；单 XGB 私 0.90459、LGBM 私 0.90312；**XGB+LGBM 的 rankdata 秩平均私 0.90669（未提交）** | 571133 |
| 18th（571021） | 单 XGBoost + **自定义 AUC 损失**；RFE 太贵 → 用前向特征选择；KFold(6)（≈按年）+ KFold(5, shuffle)；模拟私榜显示加原始数据只有 50% 情况更好 → 放弃原数据；提交选择 = "CV − 公榜" 差异最小的两份 | 571021 |
| 37th（571139） | 只用 TabPFN + 基础 FE + **纯合成数据**（不加原数据）拿最高私榜；次优是加原始数据的 XGB；自述"或许两者集成会更好" | 571139 |
| Linear SVC 帖（568268） | 小数据用带偏置的简单线性模型防过拟合；用前向选择受控加入非线性交互项 | 568268 |
| 公榜与探榜 | 公榜仅 **146 行**（41 票 / 40 评论）；"10 份提交 AUC=1.0"（34 票 / 22 评论）；"Hitchhiker's Guide to LB Probing (AUC edition)"（30 票 / 12 评论）；"Trust Your CV"（37 票 / 32 评论）；"RAPIDS KNN starter LB 0.961"（22 票） | 索引 |
| 数据背景 | 原始数据 = 香港 2015–2016 天气（38 票）；"Time Series Data with Some Mislabeled Days"（41 票 / 21 评论） | 索引 |

## 2. 逐方案对照矩阵

| 维度 | 2nd | 54th | 18th | 37th |
| --- | --- | --- | --- | --- |
| FE | 零 FE | 比值 + 年度相对温度（弃时间特征） | 前向选择（含 cdeotte 特征） | 仅基础 FE |
| 原数据 | 新行 + 新列两种接法 | 对抗验证后谨慎使用 | **不用**（模拟仅 50% 改善） | 不用 |
| 模型 | XGB/TabPFN/SVC 等权平均 | XGB/LGBM/RF/LR 等 | 单 XGB + AUC 损失 | TabPFN |
| CV | GroupKFold 6（按年） | 留一年嵌套 | KFold(6) + KFold(5) | 简单 CV |
| 提交选择 | 六模型等权（未选最强三模型） | 未提交最强秩平均 | CV−公榜最小 | 只信私榜表现 |
| 私榜 | 0.90604/0.90599（2nd） | 0.90459（单 XGB） | 0.90395（后期版） | — |

## 3. 共识、分歧与裁决

### 共识一：146 行的公榜就是噪声，决策必须靠分组 CV（54th、2nd、18th、多帖；置信度高）

公开榜 0.961/1.0 的分数由探榜与极小样本放大；"Trust Your CV"（37 票）与"LB probing guide"（30 票）都在提醒。**裁决**：小公榜 + 新年度私榜的比赛，公榜只用于 sanity check；按年 GroupKFold 是主决策信号。置信度：高。

### 共识二：原始数据的"接法"决定名次（2nd、54th、18th、37th；置信度高）

同一份香港原始数据：拼行给 XGB 私榜 0.903、merge 成列给 SVC 私榜 0.906；54th 因对抗验证弃时间特征；18th 干脆不用；37th 用纯合成 TabPFN 也赢。**裁决**：外部数据不是"加不加"，而是"以什么形态、配什么特征、配什么模型"；必须做对抗验证与分组 CV 对照。置信度：高。

### 共识三：小数据 + 洗牌场景，简单模型与等权平均更稳（2nd、37th、18th、SVC 帖；置信度中高）

2nd 零 FE + 等权平均；37th 用 TabPFN；SVC 帖强调简单带偏置模型。**裁决**：样本量小的时候复杂度是负债；等权平均（避免集成过拟合）比权重优化更稳。置信度：中高。

### 事件一：提交选择的代价（2nd、54th；置信度中高）

2nd 的三模型融合私榜 0.90728（本可第 1）未提交；54th 的 XGB+LGBM 秩平均私榜 0.90669 也未提交。**裁决**："选哪两份提交"在本场与建模同等重要；应把候选按 CV 稳健性与来源多样性分组，而不是只看单个分数。置信度：中高。

### 事件二：标签错误与探榜（565634、568718、568865；置信度中）

"部分日期标签错误"（41 票）与"10 份 AUC=1.0"（34 票）、探榜指南（30 票）说明：小公榜 + 合成数据下，噪声与博弈行为会主导表层分数。**裁决**：遇到异常高分先怀疑探榜/标签问题，再检查自己的模型。置信度：中。

## 4. 证据分级

| 断言 | 等级 | 说明 |
| --- | --- | --- |
| 2nd 的两种原数据接法与全部分数 | 自述（含单模/融合明细） | 高 |
| 54th 的对抗验证与秩平均结果 | 自述 + 3 张 EDA 图 | 中高 |
| 18th 的 AUC 损失与 50% 模拟结论 | 自述 | 中 |
| 37th 的 TabPFN 纯合成打法 | 自述 | 中 |
| 公榜 146 行 / 探榜 / 1.0 提交 | 多帖（含量化说明） | 高 |
| 原始数据为香港 2015–2016 | 社区识别帖 | 中高 |

## 5. 悬案与缺口（登记）

- 1st 的最终方案未收录（2nd 帖显示其未提交的三模型融合本可第 1，但真实 1st 的构成未知）；
- 标签错误的成因与官方处理未细读；
- 全方案归档帖（571015）体量极大（1000+ 行），仅读取开头；
- **图证缺口**：无（3 张 EDA 图已内嵌）。

## 6. 图表证据

![温度的长期趋势](../../intel/playground-series-s5e3/bodies/571133_img/01.png)

**图 1**（topic 571133，54th）：温度与 365 日移动平均——6 年周期平稳，支持"按年分组"的 CV 假设。

![各年降雨比例](../../intel/playground-series-s5e3/bodies/571133_img/02.png)

**图 2**（topic 571133，54th）：各年（year_cat 0–5）降雨均值/标准差接近（0.729–0.786），说明年度分布稳定。

![月度降雨分布对比](../../intel/playground-series-s5e3/bodies/571133_img/03.png)

**图 3**（topic 571133，54th）：赛方数据与原始数据的月度降雨均值对照（如 2 月 0.780 vs 0.643）——分布不同，是弃用时间特征、做对抗验证的依据。

## 7. 出处

- 2nd Place（160 票 / 97 评论）：https://www.kaggle.com/competitions/playground-series-s5e3/discussion/571176
- 54th 特征工程与嵌套 CV（8 票）：https://www.kaggle.com/competitions/playground-series-s5e3/discussion/571133
- 18th 单 XGB + AUC 损失（23 票 / 19 评论）：https://www.kaggle.com/competitions/playground-series-s5e3/discussion/571021
- 37th TabPFN（12 票）：https://www.kaggle.com/competitions/playground-series-s5e3/discussion/571139
- Linear SVC + 受控非线性（58 票 / 38 评论）：https://www.kaggle.com/competitions/playground-series-s5e3/discussion/568268
- 全方案归档（10 票）：https://www.kaggle.com/competitions/playground-series-s5e3/discussion/571015
- 公榜只有 146 行（41 票 / 40 评论）：https://www.kaggle.com/competitions/playground-series-s5e3/discussion/568465
- 10 份 AUC=1.0（34 票 / 22 评论）：https://www.kaggle.com/competitions/playground-series-s5e3/discussion/568718
- 探榜指南（30 票）：https://www.kaggle.com/competitions/playground-series-s5e3/discussion/568865
- Trust Your CV（37 票 / 32 评论）：https://www.kaggle.com/competitions/playground-series-s5e3/discussion/570819
- 标签错误（41 票 / 21 评论）：https://www.kaggle.com/competitions/playground-series-s5e3/discussion/565634
- 原始数据来源识别（38 票）：https://www.kaggle.com/competitions/playground-series-s5e3/discussion/566908
