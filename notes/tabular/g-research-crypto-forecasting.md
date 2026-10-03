# G-Research Crypto Forecasting

> 主题：tabular ｜ 子类：tabular-ts ｜ 领域：金融 ｜ 类别：Featured
> 截止：2022-05-03 ｜ 队伍数：1946 ｜ 机制：标准赛 ｜ 指标：加权相关系数
> 数据来源：`intel/g-research-crypto-forecasting/`（120 条主题索引 + 8 篇 write-up 正文）

## 1. 任务与数据

- **预测目标**：预测 15 种加密资产未来短周期的收益，按加权相关系数评分（不同资产权重不同）。
- **数据形态**：高频行情数据（分钟级）+ 少量基本面；数据量相对有限（2018 年起）。
- **构造陷阱**：
  - 加密市场波动剧烈、非平稳，**排行榜会随市场阶段大幅变化**（13th 的标题即"最终第 13、六周时第 1"）。
  - 数据集时间跨度短 → 时间是稀缺资源，扩充历史数据价值高。

## 2. 验证方案

| 方案 | 使用者 | 说明 |
| --- | --- | --- |
| 时间序列 CV（滚动/分组） | 多数 | 必须避免未来信息泄漏 |
| 分层时间序列（HTS）建模 | 社区 | 每资产一个模型 + 一个全局模型，再融合 |
| 多阶段更新观察 | 13th | 比赛分多次数据更新，需要观察模型在不同市场阶段的稳定性 |

## 3. 方案谱系

| 方案 | 名次 | 关键点 |
| --- | --- | --- |
| 分层时间序列（HTS）思路的普及 | 社区教程 | "每资产模型 + 全局模型 + 按星期几等切分"再集成，是时间序列金融赛的经典做法 |
| 基于外部全历史数据的自动化数据集 | 社区 | 提供比官方更长的历史（自动每日更新），弥补官方数据时间跨度不足 |
| 直接沿用 Jane Street 获奖方案 | 社区 | 把 Jane Street 的 1st place 方案迁移到本赛 |
| 最终方案 | 2nd / 13th | 见讨论区 |

## 4. 关键技巧

- **分层时间序列（HTS）**：按资产/时间段分别建模再集成，比单一全局模型稳定。
- **外部历史数据**：金融赛的时间跨度就是信息量，自动化数据集（持续更新）是重要素材。
- **跨赛事迁移**：同领域往届比赛的获奖方案可直接改造复用（Jane Street → Crypto）。
- **对排行榜波动保持克制**：多次数据更新会重排榜单，**追求稳健而非单次最高**。
- **横向索引**：社区整理了"Kaggle 时间序列预测赛获奖方案"清单，便于系统学习。

## 5. 可迁移性评估

- **可直接迁移**：
  - **分层时间序列建模**（全局 + 分组 + 个体，再融合）是通用范式。
  - 同领域往届方案迁移。
  - 多阶段评测下以稳健性优先。
- **需要前提**：
  - 需要外部数据源（历史行情）与更新机制。
  - 加权指标的权重结构要理解清楚（不同资产对分数的贡献不同）。
- **不建议照搬**：
  - 依赖单次榜单排名做决策（本场排行榜多次重排）。

## 6. 对新手的关键启示

1. **时间序列金融赛的常规套路是 HTS + 集成**。
2. **同领域历史赛事是最快的方案来源**。
3. **多阶段评测 = 稳健优先**：能活过多次更新比单次登顶更重要。

## 7. 出处

- 讨论区索引：`intel/g-research-crypto-forecasting/topics.md`（120 条）
- 已收录 write-up（8 篇）：
  - 13th（91 票）：https://www.kaggle.com/competitions/g-research-crypto-forecasting/discussion/313386
  - 2nd（87 票）：https://www.kaggle.com/competitions/g-research-crypto-forecasting/discussion/323098
  - 时间序列获奖方案清单（58 票）：https://www.kaggle.com/competitions/g-research-crypto-forecasting/discussion/284884
  - Jane Street 方案迁移（36 票）：https://www.kaggle.com/competitions/g-research-crypto-forecasting/discussion/286676
  - 最终更新分析（12 票）：https://www.kaggle.com/competitions/g-research-crypto-forecasting/discussion/322899
