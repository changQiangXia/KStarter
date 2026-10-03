# GoDaddy - Microbusiness Density Forecasting

> 主题：tabular ｜ 子类：tabular-ts ｜ 领域：经济 ｜ 类别：Featured
> 截止：2023-06-16 ｜ 队伍数：3547 ｜ 机制：标准赛 ｜ 指标：SMAPE
> 数据来源：`intel/godaddy-microbusiness-density-forecasting/`（120 条主题索引 + 8 篇 write-up 正文）

## 1. 任务与数据

- **预测目标**：预测美国 3135 个县未来 3/4/5 个月的"小微企业密度"（近似为 GoDaddy 域名数 / 人口）。
- **数据形态**：小规模面板数据（县 × 月），大量缺失与不一致；预测目标含有**疫情后结构性变化**。
- **构造陷阱**：
  - **数据质量是主要矛盾**：缺失值、异常值、跨县统计口径不一致（2nd place 把题目直接称为"数据清洗挑战"）。
  - **SMAPE 是相对误差**：小县的绝对变化会主导分数，因此模型需要在小规模序列上表现好——2nd place 专门质疑了这个指标的商业合理性。
  - 隐藏数据探针（probing）的边界模糊，2nd place 明确指出这是本场最大的不确定性。

## 2. 验证方案

| 方案 | 使用者 | 说明 |
| --- | --- | --- |
| 留出最后若干月做验证 | 1st | 与预测跨度（3–5 月）对齐 |
| 公开榜对照 + 基线校准 | 社区 | 出现"基线纠正"帖（Last-Value 基线从 3.28 修正到 1.46），说明**基线本身就有很大的误用空间** |
| 按县规模分层分析误差 | 2nd | 因 SMAPE 的相对性，需要分规模检查误差来源 |

## 3. 方案谱系

| 方案 | 名次 | 关键点 |
| --- | --- | --- |
| **线性回归 + 泛化导向** | 1st | 强调泛化与透明；用最简单的模型拿到第一 |
| 数据清洗优先的流程 | 2nd | 把大部分精力投入数据质量；对指标与探针边界提出质疑 |
| 用 GRU 预测**倍数（multiplier）**而非绝对值 | 3rd | 相对变化比绝对值稳定，是处理该指标的关键技巧 |
| 线性回归基线（LB 1.092 / CV 1.098） | 公开帖 | 强基线公开共享，成为全社区的起点 |

## 4. 关键技巧

- **预测倍数而非绝对值**：先预测相对变化，再乘回基期水平（3rd 的核心思路，广泛使用）。
- **数据清洗优先**：缺失填补、异常县识别、口径统一。
- **理解 SMAPE 的偏好**：相对误差让"小县预测准"比"大县预测准"更重要，直接影响样本加权与损失设计。
- **简单模型 + 稳健特征**：冠军用线性回归说明，本场不存在必须用深度模型的理由。
- **基线校准意识**：社区发现广泛使用的 Last-Value 基线被算错了近一倍——**不要盲信公开基线**。

## 5. 可迁移性评估

- **可直接迁移**：
  - **相对指标 → 预测相对变化**（倍率建模）是时间序列的通用技巧。
  - 先做数据质量审计，再建模。
  - 自己复算公开基线，确认其正确性。
  - 指标偏好分析：理解指标对哪些样本更敏感，再决定损失与加权。
- **需要前提**：
  - 面板数据的缺失处理需要领域知识（哪些 0 是真 0，哪些是缺失）。
  - 倍率模型要求基期水平可得。
- **不建议照搬**：
  - 依赖隐藏数据探针的策略（边界不明，风险高）。
  - 直接套用公开 notebook 的基线数值。

## 6. 对新手的关键启示

1. **简单模型能赢**：冠军是线性回归——先问"这个问题的难点在模型还是在数据"。
2. **指标要先读懂**：SMAPE 的相对性决定了整个建模方向。
3. **公开基线的数字要自己验证**，本场出现了近一倍的误差。
4. **时间序列的通用套路**：预测变化量/倍率 + 基期回乘。

## 7. 出处

- 讨论区索引：`intel/godaddy-microbusiness-density-forecasting/topics.md`（120 条）
- 已收录 write-up（8 篇）：
  - 1st（线性回归）：见讨论区 1st place 帖与 `kaggle.com/kaggleqrdl/first-place-code`
  - 2nd（19 票，数据清洗）：https://www.kaggle.com/competitions/godaddy-microbusiness-density-forecasting/discussion/395264
  - 3rd（84 票）：https://www.kaggle.com/competitions/godaddy-microbusiness-density-forecasting/discussion/418287
  - 线性回归基线（196 票）：https://www.kaggle.com/competitions/godaddy-microbusiness-density-forecasting/discussion/373099
  - 基线纠正（141 票）：https://www.kaggle.com/competitions/godaddy-microbusiness-density-forecasting/discussion/389215
  - SMAPE 用法（69 票）：https://www.kaggle.com/competitions/godaddy-microbusiness-density-forecasting/discussion/373274
