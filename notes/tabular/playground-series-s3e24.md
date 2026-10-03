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

## 8. 轻读结论（2026-10 补）

**一句话**："**暴力特征工程 + 谨慎集成**"的医疗表格赛：头部都在百列级组合特征上做文章，NN/TabNet 只是边际；全场最亮的单点是**潜变量重建**——用外部数据训练 0.997 准确率的性别分类器，把"男性概率"当新特征（性别与目标 MI 24.5%，全场最高）；#4 用多折多 seed 复核的稳健 Hill Climbing 拿第 4。

- #3（455248）：80–120 特征 + permutation importance；10×1 分层 CV；3+5+3 树模型 + RF/LR/TabNet/MLP/GAM；Optuna 权重 + 少量有依据的探榜 → 私 3。
- #4（455296）：25 OOF 选 7；每个模型在所有折都需提升 + 换 seed 复核；并行 HC + numpy AUC 优化；提到公榜第一只交 3 次。
- #7（455271）：XGB+Optuna → 伪标签 → 公开特征/预测平均 → hemoglobin 交互 → seed 42→43；私 0.87926（7th）；未选提交 0.87931 更好。
- #8（455268）：频率离散化 + 暴力组合 + top-N 并集；Optuna 融合 + 公榜排名加权混合；多次运行超时。
- 社区：Be careful with AUC（42 票）、组合示例（41 票）、stacking vs blending（31 票）。

**裁决**：先把组合特征做透；集成用重复 CV 复核增益；有未给出的关键潜变量就做"代理模型概率特征"；探榜只在 CV 支持内；提交保留多条线。

**悬案**：1st/2nd/5th/6th 未收录；探榜风险与 gender 特征权重未量化。

## 9. 图表证据

![#7 的未选提交](../../intel/playground-series-s3e24/bodies/455271_img/01.jpeg)

**图 1**（topic 455271）：私榜 0.87931 的未选版本。

## 10. 出处

- 3rd：简单集成与探测：https://www.kaggle.com/competitions/playground-series-s3e24/discussion/455248
- 4th：稳健爬山：https://www.kaggle.com/competitions/playground-series-s3e24/discussion/455296
- 潜特征：构造 gender 列：https://www.kaggle.com/competitions/playground-series-s3e24/discussion/452379
- 领域信息与特征想法：https://www.kaggle.com/competitions/playground-series-s3e24/discussion/450314
- #7 private / #2 public：https://www.kaggle.com/competitions/playground-series-s3e24/discussion/455271
- #8 private / #7 public：https://www.kaggle.com/competitions/playground-series-s3e24/discussion/455268
- Be careful with AUC（42 票）：https://www.kaggle.com/competitions/playground-series-s3e24/discussion/450764
