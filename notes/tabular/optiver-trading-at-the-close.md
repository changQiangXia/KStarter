# Optiver - Trading at the Close

> 主题：tabular ｜ 子类：tabular-ts ｜ 领域：金融 ｜ 类别：Featured
> 截止：2024-03-22 ｜ 队伍数：4436 ｜ 机制：代码赛 ｜ 指标：Mean Columnwise MAE
> 数据来源：`intel/optiver-trading-at-the-close/`（120 条主题索引 + 8 篇 write-up 正文）

## 1. 任务与数据

- **预测目标**：收盘前最后 10 分钟内，预测每只股票在未来 60 秒的价格变动（多列 MAE）。
- **数据形态**：逐秒的订单簿快照（买一/卖一价量、成交明细等），按 `date_id × seconds_in_bucket × stock_id` 组织，属于**高频金融时序**。
- **构造陷阱**：
  - 公开榜与私榜只差一个时间段，但存在"中期更新"，导致部分依赖在线学习的方案在切换期崩溃（30th place 明确记录）。
  - 目标是对未来价格变化的回归，存在大量噪声，**MAE 的绝对值很小**，容易过度解读微小提升。

## 2. 验证方案

本场比赛的一个罕见特征：**本地 CV 与榜分高度一致**，多位获奖者都明确提到这一点，因此验证策略相对简单。

| 方案 | 使用者 | 说明 |
| --- | --- | --- |
| 单折 holdout（前 400 天训练 / 后 81 天验证） | 1st | CV 与 LB 对齐良好，因此把全部精力放在提升 CV 上 |
| 单折 holdout | 30th | 明确建议"就用单折 holdout" |
| 分股票加权验证 | 7th | 融合权重在验证集上搜索得到（0.5/0.3/0.2） |

**结论**：比赛越"稳定"，验证方案可以越简单；把省下的精力投到特征和融合上。

## 3. 模型家族

| 方案 | 名次 | 关键点 |
| --- | --- | --- |
| CatBoost + GRU + Transformer 加权融合（0.5/0.3/0.2） | 1st | 三个模型共享 300 维特征；权重在验证集上搜索 |
| LightGBM + 神经网络，最小化神经网络侧的特征工程 | 7th | 目的是降低融合方差；偏差特征 + 在线学习带来大幅提升 |
| XGBoost 三种子集成（157 特征，GPU 训练） | 9th | 认为 XGB 与 LGBM 差距不大，但 GPU XGB 更快 |
| Seq2seq Transformer ×3 + GRU ×1，带 stock-wise attention | 6th | 刻意少做特征工程，专注深度学习路线 |
| LGBM + CatBoost 集成（202 / 141 特征，分别筛选） | 30th | 关键细节：同一特征在 CatBoost 有效、在 LGBM 可能有害，需**分模型做特征筛选** |
| XGB + LGB 集成 + 尽量多 refit | 14th | 170 特征，Optuna 调参 |

## 4. 关键技巧

- **在线学习（online learning）** —— 本场比赛的最大杠杆。测试期逐日揭示真实标签，可用新数据增量更新模型；1st / 7th / 30th 都使用了它。1st place 的消融显示：同一模型在线学习 5 次比不学习在测试集上提升约 0.03–0.05 MAE。
- **偏差特征（deviation from group median）**：对每个原始特征按 `stock_id × seconds` 分组减去中位数，树模型和神经网络都受益（7th）。
- **特征工程**：订单簿不平衡（imb1/imb2）、MACD、滚动均值/方差、diff/shift 多窗口、按组中位数归一化的量纲特征、market urgency（公开 notebook 流传）。
- **后处理（PP）**：1st place 的表格显示 PP 在验证集与测试集上都有小幅但稳定的收益。
- **工程效率**：用 numba + multiprocessing 重写因子计算（"Faster solution for building features"），这是在时限内做大规模特征搜索的前提。
- **分模型特征筛选**：树模型之间对特征的偏好差异显著，统一特征集不是最优（30th）。

## 5. 可迁移性评估

- **可直接迁移**：
  - "先判断比赛是否稳定"：如果 CV 与 LB 长期一致，就简化验证、把预算投给特征与融合；这是可复用的**元决策**。
  - 按实体分组的**偏差特征**（减组中位数）在各类结构化时序数据上通用。
  - 分模型做特征筛选，而不是一套特征打天下。
  - 融合权重在验证集上搜索，而不是等权平均。
- **需要前提**：
  - 在线学习依赖"测试期标签分批揭示"的机制，普通比赛不成立。
  - numba 加速需要因子计算密集到值得投入工程时间。
- **不建议照搬**：
  - 中期更新导致的在线学习崩溃是赛制特有风险，不必当作通用教训。
  - 高频金融数据的特征（imb、market urgency）迁移价值低。

## 6. 对新手的关键启示

1. **先确认比赛稳不稳**：稳定性决定了验证成本和策略重心，这是最该先做的一件事。
2. **融合不同家族的模型（树 + 序列模型）比堆同族模型更有效**，且权重要在验证集上定。
3. **在线学习是"机制红利"**：看到测试期逐步揭示标签，第一反应应该是增量训练，而不是只做一次离线训练。
4. **工程效率也是竞争力**：能在同样时间内试 10 倍特征的人，赢面大得多。

## 7. 出处

- 讨论区索引：`intel/optiver-trading-at-the-close/topics.md`（120 条）
- 已收录 write-up（8 篇）：1st / 6th / 7th / 9th / 14th / 30th / 特征加速方案 / 前作 Optiver 比赛回顾
  - 1st（338 票）：https://www.kaggle.com/competitions/optiver-trading-at-the-close/discussion/487446
  - 6th（49 票）：https://www.kaggle.com/competitions/optiver-trading-at-the-close/discussion/486040
  - 7th（43 票）：https://www.kaggle.com/competitions/optiver-trading-at-the-close/discussion/486169
  - 9th（66 票）：https://www.kaggle.com/competitions/optiver-trading-at-the-close/discussion/486868
  - 14th（31 票）：https://www.kaggle.com/competitions/optiver-trading-at-the-close/discussion/485985
  - 30th（25 票）：https://www.kaggle.com/competitions/optiver-trading-at-the-close/discussion/462650
  - 特征加速：https://www.kaggle.com/competitions/optiver-trading-at-the-close/discussion/451735
