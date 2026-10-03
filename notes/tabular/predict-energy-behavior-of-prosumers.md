# Enefit - Predict Energy Behavior of Prosumers

> 主题：tabular ｜ 子类：tabular-ts ｜ 领域：能源 ｜ 类别：Featured
> 截止：2024-04-30 ｜ 队伍数：2731 ｜ 机制：代码赛 ｜ 指标：MAE
> 数据来源：`intel/predict-energy-behavior-of-prosumers/`（120 条主题索引 + 8 篇 write-up 正文）

## 1. 任务与数据

- **预测目标**：预测产消者（装有光伏、热泵、电动车的家庭）未来的**电力消耗与生产**，属于多目标多步时间序列预测。
- **数据形态**：历史用电/发电序列 + 气象预报（多来源、多时点）+ 设备与电价元数据。
- **关键陷阱**：
  - **气象预报本身存在系统性偏差**（预报值远高于实际值，53rd 明确指出）；应使用**预报之间的差分**而非预报与实际值的差分。
  - 测试期可获取新数据 → **在线学习成为主要杠杆**（与 Optiver 类似）。
  - 消耗与生产是两类不同目标，需要分别建模。

## 2. 验证方案

| 方案 | 使用者 | 说明 |
| --- | --- | --- |
| 时间留出（前 500 天训练，其余验证） | 1st | 简单 holdout，与排行榜表现一致 |
| 按 data_block 划分在线学习窗口 | 3rd（公开第 3） | 消费每 7 天重训、生产每 4 天重训 |

## 3. 方案谱系

| 方案 | 名次 | 关键点 |
| --- | --- | --- |
| 4 个 XGBoost + 2 个 GRU（共享 600 特征）+ 在线更新 | 1st | 消融显示：不更新 55.6 → 更新一次 54.1 → 更新三次 54.1（测试集 MAE） |
| LightGBM + 在线学习（消费/生产分别重训） | 公开第 3 | 生产端更新更频繁；预测阶段完全不用预训练模型、从 2 月 1 日起在线训练 |
| LightGBM 基线 + 大量实验 | 5th | "对硬件要求低，因此能大量实验"——强调实验次数的重要性 |
| 目标变换 + 多模型平均 | 53rd（公开） | 用预报差分特征、目标变换处理"冲击"后的滞后适应 |

## 4. 关键技巧

- **在线学习（增量更新）**：本场最大杠杆，1st 用消融量化了收益（≈1.5 MAE）。
- **气象预报差分**：用"今天的预报 vs 两天前的预报"的差，而不是预报与实际的差。
- **多目标分开建模**：消费 vs 生产用不同模型/不同更新频率。
- **树模型 + 序列模型的组合**：XGBoost 与 GRU 融合带来稳定增益。
- **低算力友好**：本场用单机即可做大量实验，说明"快迭代"本身是竞争力。

## 5. 可迁移性评估

- **可直接迁移**：
  - 只要赛制允许**用新数据持续更新**，就应把在线学习当第一优先级。
  - 对"预测类特征"（如天气预报）用**预报之间的差分**，是通用技巧。
  - 多目标分别建模 + 不同更新频率。
- **需要前提**：
  - 在线学习依赖测试期数据逐步揭示（代码赛常见，标准赛不成立）。
  - 需要能快速重训的流水线（轻量模型更有优势）。
- **不建议照搬**：
  - 直接用预报值而不做偏差校正/差分。

## 6. 对新手的关键启示

1. **先查预测类特征的偏差**（气象/流量/价格预报都有系统偏差）。
2. **能在线更新就更新**——这是时间序列比赛最稳的提分手段。
3. **轻量模型 + 快速实验循环** 优于重型模型的单次训练。

## 7. 出处

- 讨论区索引：`intel/predict-energy-behavior-of-prosumers/topics.md`（120 条）
- 已收录 write-up（8 篇）：
  - 1st（178 票）：https://www.kaggle.com/competitions/predict-energy-behavior-of-prosumers/discussion/472793
  - 公开第 3（48 票）：https://www.kaggle.com/competitions/predict-energy-behavior-of-prosumers/discussion/472754
  - 公开第 10（78 票）：https://www.kaggle.com/competitions/predict-energy-behavior-of-prosumers/discussion/472537
  - 5th（30 票）：https://www.kaggle.com/competitions/predict-energy-behavior-of-prosumers/discussion/499938
  - 公开第 12（37 票）：https://www.kaggle.com/competitions/predict-energy-behavior-of-prosumers/discussion/472564
