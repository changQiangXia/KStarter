# Playground Series S3E24 - 吸烟状况预测（AUC，探测与潜特征回收）

> 主题：tabular ｜ 子类：— ｜ 领域：医疗（生物信号，合成数据） ｜ 类别：Playground
> 截止：2023-11-13 ｜ 队伍数：1908 ｜ 机制：标准赛 ｜ 指标：ROC AUC
> 数据来源：`intel/playground-series-s3e24/`（80 条主题索引 + 6 篇 write-up 正文）

## 1. 任务与数据

- 预测目标：由生物信号推断吸烟状况（AUC）；合成数据 + 原数据。
- 数据特点：存在"次生特征/辅助原始数据"等额外资源，但用不用要看 CV（3rd：辅助数据反而伤分）；**性别是不在数据里的潜特征**，可用外部数据集回收。

## 2. 验证方案

- 3rd：10×1 分层 K 折（试过 10×3 重复无增益）；置换重要性做特征淘汰（本地机执行，kernel 只做训练）；原数据用、辅助原数据不用。
- 8 Public / 3 Private 的"探测"路线（3rd）：在公开榜上做小步探测以定位提交选择。

## 3. 模型家族

| 方案 | 使用者层次 | 关键点 | 出处 |
| --- | --- | --- | --- |
| 多模型（3 CatBoost + 5 LGBM + 3 XGB + RF/LR/TabNet/MLP/GAM）+ HC/Optuna | 3rd | 简单集成 + 探测 | topic 455248 |
| 稳健爬山集成 | 4th | 对洗牌稳健 | topic 455296 |
| #7 私榜 / #2 公开 | 社区 | 不同选择策略 | topic 455271 |

## 4. 关键技巧

- **潜特征回收**：用外部同源数据集 + 互信息（`mutual_info_classif` 多次迭代取均值/方差）为原数据恢复 gender 列，再映射回竞赛数据——"没有的列"未必不能用（topic 452379）。
- **探测（probing）**：把公开榜当测量仪器做小步探测，但注意规则与私榜风险（3rd 的 8Public/3Private 反差本身说明公开榜不可外推）。
- 特征工程收敛在 80–120 列 + 置换重要性淘汰；重复 K 折（10×3）在噪声有限时无必要。
- 集成器用爬山/Optuna 均可；稳健性优先于再压 CV。

## 5. 可迁移性评估

- **可直接迁移**：外部同源数据回收潜特征（含 MI 评估代码形态）；辅助原始数据的"用/不用"对照；探测的风险意识；80–120 列的特征规模纪律。
- **需要前提**：能找到同源外部数据并验证语义对齐；理解比赛对探测的规则。
- **不建议照搬**：公开榜探测的高频依赖（本场 #8P/#3Private 反差就是警告）；把 10×3 重复折当默认增益。

## 6. 对新手的关键启示

- "数据集里缺的关键列"常能从公开数据找回——学会做语义对齐与 MI 验证。
- 额外数据不是越多越好：本场辅助原数据被实测排除——每个数据源都要过 CV 门槛。
- 特征规模先守住百列级，用置换重要性淘汰，而不是无上限膨胀。

## 7. 出处

- 3rd：简单集成与探测：https://www.kaggle.com/competitions/playground-series-s3e24/discussion/455248
- 4th：稳健爬山：https://www.kaggle.com/competitions/playground-series-s3e24/discussion/455296
- 潜特征：构造 gender 列：https://www.kaggle.com/competitions/playground-series-s3e24/discussion/452379
- 领域信息与特征想法：https://www.kaggle.com/competitions/playground-series-s3e24/discussion/450314
