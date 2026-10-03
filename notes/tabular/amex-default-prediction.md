# American Express - Default Prediction

> 主题：tabular ｜ 子类：— ｜ 领域：金融 ｜ 类别：Featured
> 截止：2022-08-24 ｜ 队伍数：4874 ｜ 机制：标准赛 ｜ 指标：Amex Custom Gini + Percentage Capture
> 数据来源：`intel/amex-default-prediction/`（120 条主题索引 + 8 篇 write-up 正文）

## 1. 任务与数据

- **预测目标**：根据客户过去 13 个月的月度对账单序列，预测其信用卡违约概率；指标是自定义 Gini，只关心分数最高的一小部分人群（percentage capture）。
- **数据形态**：多变量时间序列 + 高维匿名特征 + 大量缺失；训练集约 55 万客户。
- **构造陷阱**：
  - **短序列（<13 个月）是性能杀手**（10th place 的核心观察），必须单独处理或剔除。
  - 类别与缺失模式高度结构化，部分特征存在"整块缺失"的客户簇（13th place 按 B/D/P/R/S 缺失模式聚类）。
  - 训练集与测试集时间窗不同，**测试期数据（未来）本身可用**（10th place 明确利用），构成半监督机会。
  - 排行榜在最后几天发生剧烈变动（2nd place 提到冠军"最后 3 天巨大跃升"），说明公开榜选择策略风险高。

## 2. 验证方案

| 方案 | 使用者 | 说明 |
| --- | --- | --- |
| 单折 holdout + 公开榜交叉验证 | 多数 | 本地 CV 与 LB 量级接近（如 11th：CV 0.799 / private 0.809） |
| CV 用于选特征、**公开榜用于定融合权重** | 5th | 明确记录："按 CV 定权重会过拟合，按公开榜定更好" |
| 公开数据集 CV 对照 | 13th | 以社区共享的预处理数据集为基线，量化清洗收益（+0.0004~0.0008 CV） |

**注意**：本场比赛的排行榜抖动大（多支队伍的 public→private 排名变化数十位），公开榜权重策略属于高风险选择，新手不宜照搬。

## 3. 模型家族

| 方案 | 名次 | 关键点 |
| --- | --- | --- |
| LGB + NN 重型集成 | 1st | 单模型依赖 RN N 填充；作者自评"有运气成分"，无法完全复现 |
| 四人大团队集成（"简单的就是最好的"） | 2nd/3rd | 3rd place 的结论是 **feature engineering is all you need** |
| LGBM 堆叠 61 模型 + CMA 加权 54 模型 + 加权平均 55 模型 | 13th | 三个集成再平均；核心收益来自**深度数据清洗** |
| NN Transformer + LGBM 知识蒸馏（50/50） | 14th | 用 LGBM 的软标签蒸馏 Transformer，且训练与测试数据都参与蒸馏 |
| XGB + 自回归 RNN 特征 | 10th | 用 RNN 生成序列特征喂给 XGB；先做短序列治理 |
| GBDT + Transformer + 2D-CNN + GRU 混合集成 | 5th | 多模态处理序列的典型组合 |
| LightGBM + 元特征 | 11th | 时间窗聚合（近 3/6 个月的 min/max/mean/std）+ 比率与差分特征 |

## 4. 关键技巧

- **数据清洗 > 模型**：13th place 在公开预处理数据集基础上继续清洗，单模型即提升 0.0004–0.0008 CV——在这个量级上等于若干名次。
- **知识蒸馏做半监督**：用已训练的 LGBM 给 Transformer 提供软标签，并**把测试集也纳入蒸馏**，让模型学习测试分布（14th）。
- **短序列治理**：把序列长度作为诊断变量，单独分析其对指标的影响（10th）。
- **特征工程**：时间窗聚合（近 3 / 6 个月统计量）、序列比率与差分、按缺失模式聚类产生类别特征、去噪（Raddar 的 denoise 思路被多队引用）。
- **融合**：多层次集成（堆叠 + 加权平均 + CMA 权重搜索）在稳定榜上收益明显；权重的确定方式本身就是个风险决策。

## 5. 可迁移性评估

- **可直接迁移**：
  - **把数据清洗当作一等公民**：在表格赛里，清洗 + 特征工程往往比换模型更划算。
  - 用"序列长度 / 分组大小"等结构变量做诊断，找出系统性弱势子群。
  - 知识蒸馏 + 半监督（若允许使用测试特征）在时序数据上通用。
  - 社区共享的数据集可以作为**基线锚点**，用来量化自己清洗的增量收益。
- **需要前提**：
  - "测试数据可用作特征"依赖比赛规则与数据形态（本题成立，很多比赛不成立）。
  - CMA 权重搜索、61 模型堆叠需要大量算力。
- **不建议照搬**：
  - 按公开榜定融合权重：本题抖动极大，风险不可控。
  - 冠军方案自述不可复现（随机波动），说明单点方案不具可复制性。

## 6. 对新手的关键启示

1. **表格赛的第一战场是数据清洗和特征工程**，不是模型结构。3rd place 的总结只有一句："feature engineering is all you need"。
2. **先找"结构性坏样本"**（短序列、整块缺失的客户簇），再谈调参。
3. **公开数据集是你最好的起点，但要量化自己在其上加了什么**。
4. **融合权重怎么定是策略问题**：CV 稳定时用 CV，CV 与 LB 不一致时要意识到自己在赌博。

## 7. 出处

- 讨论区索引：`intel/amex-default-prediction/topics.md`（120 条）
- 已收录 write-up（8 篇）：
  - 1st（303 票）：https://www.kaggle.com/competitions/amex-default-prediction/discussion/348111
  - 2nd（180 票）：https://www.kaggle.com/competitions/amex-default-prediction/discussion/347637
  - 3rd（80 票）：https://www.kaggle.com/competitions/amex-default-prediction/discussion/349741
  - 5th（61 票）：https://www.kaggle.com/competitions/amex-default-prediction/discussion/348097
  - 10th（93 票）：https://www.kaggle.com/competitions/amex-default-prediction/discussion/347668
  - 11th（103 票）：https://www.kaggle.com/competitions/amex-default-prediction/discussion/347786
  - 13th（76 票）：https://www.kaggle.com/competitions/amex-default-prediction/discussion/348014
  - 14th（271 票）：https://www.kaggle.com/competitions/amex-default-prediction/discussion/347641
