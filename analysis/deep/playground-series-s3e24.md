# Playground Series S3E24（生物信号判断吸烟状态）轻量深读（Tier B）

> 赛事：Playground ｜ 主题 tabular（医疗二分类，AUC）｜ 1908 队 ｜ 标准赛 ｜ 指标：ROC AUC
> 材料基础：`digests/playground-series-s3e24.md`（6 篇正文：领域信息 450314 / #3 private #8 public 455248 / #4 455296 / gender 特征 452379 / #7 private #2 public 455271 / #8 private #7 public 455268；80 条主题索引）+ 1 张归档图
> 轻读时间：2026-10（Tier B B16）

## 1. 一句话重述与数字账

用血压/血脂/肝功能/口腔等生物信号判断吸烟状态（AUC）。本场是"**暴力特征工程 + 谨慎集成**"的代表：头部方案都在百列级特征上做算术组合与频率离散化，配合 Optuna/Hill Climbing 权重与（有争议的）公榜探榜；最亮的单点是**潜变量重建**——数据里没有性别，但用外部数据集训练一个 0.997 准确率的性别分类器，把"男性概率"当作新特征（性别与目标互信息 24.5%，全场最高）。

| 关键数字 | 值 | 来源 |
| --- | --- | --- |
| #3 private / #8 public（455248） | 暴力特征限制在 **80–120 列**（>130–140 列无增益），用 permutation importance 淘汰；10×1 分层 KFold（10×3 重复无增益）；模型：3 CAT + 5 LGBM + 3 XGB + RF + LR + TabNet + MLP + GAM；三种集成器对比后用 **Optuna 权重 + 少量"有依据的探榜"** 微调 → 私榜第 3；明确反对 blind probing；自评"参数调优远不如特征工程重要" | 455248 |
| #4（455296） | **稳健 Hill Climbing**：从 25 个自有/公开 OOF 中选出 7 个（paddykb 均值 OOF、arunklenin 的 LGB/CAT/NN、自有 LGB+2 XGB）；要求"训练折提升时验证折也提升、且 7 模型在**所有折**都提升"，并用第二组折（换 seed）复核；并行 HC + numpy 优化 AUC（@siukeitin）；提到公榜第一的 @kailai 只提交 3 次、"值得赢" | 455296 |
| 潜变量性别（452379） | 外部数据集含 gender；互信息（Theil's U）显示 **gender 24.53%** 为最高（远高于 hemoglobin 15.65、Gtp 11.39）；用不含 oral/tartar/smoking 的特征训练 XGB 预测性别，**RepeatedStratifiedKFold 准确率 0.99736**；把"男性概率"作为 train/test 新特征 | 452379 |
| #7 private / #2 public（455271） | XGB+Optuna（公 0.87392）→ 伪标签（0.87901）→ arunklenin 派生特征 + 平均公开预测（0.88116）→ hemoglobin 交互特征（公榜 top-2 0.88126）→ **seed 42→43（0.88136）**；私榜 0.87926（第 7）；截图显示一份未选提交私榜 0.87931 更好 | 455271 |
| #8 private / #7 public（455268） | 频次 >2 的特征全当离散并做多种编码；**暴力算术组合搜索**；取 CatBoost/XGB/LGBM 的 top-N（50/100）特征并集；XGB/CAT/LGBM/NN/LR/DT 用 Optuna 融合；再按**公榜排名加权**混合公开预测；多次因运行时间超限中断 | 455268 |
| 社区 | 领域信息与特征想法（74 票 / 35 评论）；"Be careful with AUC"（42 票 / 15 评论）；"制作 gender 特征"（42 票 / 21 评论）；模型组合示例（41 票）；stacking vs blending（31 票）；肝酶含义（29 票）；"几行代码进前 10"（26 票 / 17 评论） | 索引 |

## 2. 逐方案对照矩阵

| 维度 | #3 | #4 | #7 | #8 |
| --- | --- | --- | --- | --- |
| 特征 | 80–120 暴力组合 + 置换重要度 | 基本沿用公开特征 | hemoglobin 交互族 | 频率离散化 + top-N 并集 |
| 集成 | Optuna 权重 + 谨慎探榜 | **多 fold/多 seed 复核的 Hill Climbing** | 加权混合公开预测 | Optuna + 公榜排名权重 |
| 潜变量 | — | — | — | — |
| 结果 | 私 3 | 4 | 私 7 | 私 8 |

## 3. 共识、分歧与裁决

### 共识一：本场收益主要来自特征工程，NN/TabNet 只是边际（#3、#7、#8；置信度中高）

#3 明确"参数调优远不如 FE 重要"、NN/TabNet 权重很小；#7 的增益几乎全来自派生特征与交互；#8 的框架核心也是暴力组合 + 编码。**裁决**：医疗表格赛优先把组合特征做透，再考虑深度模型。置信度：中高。

### 共识二：集成要"稳健"——多折多 seed 复核增益（#4、#8、450764；置信度中高）

#4 的 HC 要求每个模型在所有验证折都提升并用第二组折复核；#8 也强调权重需要逻辑而非试错。**裁决**：HC/权重搜索必须配重复 CV，否则会买到折内噪声。置信度：中高。

### 事件：潜变量重建（gender）是全场最亮的特征思想（452379；置信度中高）

外部数据训练 0.997 准确率的性别分类器 → 概率特征；MI 分析显示性别与目标关联最强。**裁决**：当已知存在未给出的关键潜变量时，"外部数据训练代理模型 → 概率特征"是强力路线（需注意外部数据许可与分布差）。置信度：中高。

### 分歧：探榜与公开预测加权（#3 vs #4/#8；置信度中）

#3 用少量有 CV 依据的探榜拿私榜第 3，但明确反对 blind probing；#4 完全靠稳健 HC 拒绝探榜；#8 按公榜排名给公开预测加权。**裁决**：探榜只能在 CV 支持的范围内微调；公榜排名加权是弱先验，须记录风险。置信度：中。

### 事件：名次与提交数、种子的敏感性（#4、#7；置信度中）

公榜第一的 @kailai 只提交 3 次；#7 只改 seed 42→43 就改变公榜；未选提交私榜更好。**裁决**：小差异不可信；保留多份结构不同的提交。置信度：中。

## 4. 证据分级

| 断言 | 等级 | 说明 |
| --- | --- | --- |
| gender 潜变量的 MI 与 0.997 重建准确率 | 高票帖 + 可复现代码 | 高 |
| #4 的稳健 HC 流程 | 自述 + 公开 notebook | 中高 |
| #3 的集成与探榜细节 | 自述 | 中 |
| #7/#8 的特征与融合 | 自述（含截图/代码） | 中高 |
| 领域特征想法 | 74 票帖 | 中高 |

## 5. 悬案与缺口（登记）

- 1st/2nd、5th/6th 方案未收录；
- 探榜的收益与风险未量化；
- gender 重建特征在本场的实际权重未给出；
- **图证缺口**：无（1 张图，本深读内嵌 1 张）。

## 6. 图表证据

![#7 的未选提交](../../intel/playground-series-s3e24/bodies/455271_img/01.jpeg)

**图 1**（topic 455271，#7）：`PG-S3-E24-MIR - Version 6` 私榜 0.87931 / 公榜 0.88116——私榜优于作者最终 0.87926 的版本，是"未选提交更好"的又一条证据。

## 7. 出处

- 领域信息与特征想法（74 票 / 35 评论）：https://www.kaggle.com/competitions/playground-series-s3e24/discussion/450314
- #3 private / #8 public（57 票 / 37 评论）：https://www.kaggle.com/competitions/playground-series-s3e24/discussion/455248
- #4 稳健 Hill Climbing（24 票 / 12 评论）：https://www.kaggle.com/competitions/playground-series-s3e24/discussion/455296
- 制作 gender 特征（42 票 / 21 评论）：https://www.kaggle.com/competitions/playground-series-s3e24/discussion/452379
- #7 private / #2 public（17 票 / 5 评论）：https://www.kaggle.com/competitions/playground-series-s3e24/discussion/455271
- #8 private / #7 public（14 票 / 4 评论）：https://www.kaggle.com/competitions/playground-series-s3e24/discussion/455268
- Be careful with AUC（42 票 / 15 评论）：https://www.kaggle.com/competitions/playground-series-s3e24/discussion/450764
- 模型组合示例（41 票 / 7 评论）：https://www.kaggle.com/competitions/playground-series-s3e24/discussion/452123
- stacking vs blending（31 票 / 1 评论）：https://www.kaggle.com/competitions/playground-series-s3e24/discussion/450585
