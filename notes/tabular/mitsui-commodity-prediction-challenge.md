# MITSUI&CO. Commodity Prediction Challenge

> 主题：tabular ｜ 子类：tabular-ts ｜ 领域：大宗商品/金融 ｜ 类别：Featured
> 截止：2026-01-16 ｜ 队伍数：1700+ ｜ 机制：代码赛 ｜ 指标：加权相关系数类
> 数据来源：`intel/mitsui-commodity-prediction-challenge/`（80 条主题索引 + 6 篇 write-up 正文）

## 1. 任务与数据

- 预测目标：预测大宗商品相关标的的未来收益（多资产时序回归）。
- 数据形态：行情 + 宏观/基本面特征；非平稳、信噪比低。
- 构造陷阱：
  - 市场结构随时间为变化 → 静态模型会失效。
  - 训练/测试的时间划分必须严格（避免未来信息）。

## 2. 验证方案

| 方案 | 使用者 | 说明 |
| --- | --- | --- |
| **CombinatorialPurgedGroupKFold** | 15th | 金融时序的标准做法（分组 + 清洗 + 组合式划分） |
| 多阶段滚动评估 | 多队 | 观察模型在数据更新中的稳定性 |

## 3. 方案谱系

| 方案 | 名次 | 关键点 |
| --- | --- | --- |
| **推理期在线训练**（每 7 天用新标注数据重训）+ 特征工程 + 集成 | 15th | 核心是"动态更新"而非静态模型 |
| 个人方案（学生参赛者） | 5th | 见讨论区；同属时间序列建模路线 |
| 其他方案 | 26th / 89th / 97th | 见讨论区 |

## 4. 关键技巧

- **在线训练（inference-time retraining）**：每 7 天用新数据重训模型以适配市场变化——这已是金融时序赛的**共识级做法**（Optiver、Enefit、Jane Street 均如此）。
- **CombinatorialPurgedGroupKFold**：金融时序的验证标准（组合式划分 + 清洗窗口 + 分组）。
- **集成**：多模型平均提升稳定性。
- **特征工程**：宏观与微观特征结合。

## 5. 可迁移性评估

- **可直接迁移**：
  - **能在线更新就更新**——金融/实时赛制的第一优先。
  - CombinatorialPurgedGroupKFold 作为金融时序验证模板。
  - 低信噪比场景下以集成换稳定性。
- 需要前提：推理期可获取新标签（代码赛机制）；

  需要可快速重训的轻量流水线。
- 不建议照搬：静态训练后不再更新。

## 6. 对新手的关键启示

1. **"模型要不要更新"是金融时序赛的第一个决策**（本场 15th 的核心创新就是这个）。
2. **验证方法要能处理时间清洗**（purge/embargo）。
3. 与 Enefit、Optiver、Jane Street 对照可确认：**在线学习是跨年度的稳定规律**。

## 7. 出处

- 讨论区索引：`intel/mitsui-commodity-prediction-challenge/topics.md`（80 条）
- 已收录 write-up（6 篇）：
  - 15th 在线训练（16 票）：https://www.kaggle.com/competitions/mitsui-commodity-prediction-challenge/discussion/668673
  - 26th：https://www.kaggle.com/competitions/mitsui-commodity-prediction-challenge/discussion/669234
  - 89th：https://www.kaggle.com/competitions/mitsui-commodity-prediction-challenge/discussion/668781
  - 97th：https://www.kaggle.com/competitions/mitsui-commodity-prediction-challenge/discussion/668698
