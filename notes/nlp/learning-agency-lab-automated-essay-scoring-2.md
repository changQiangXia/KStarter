# Learning Agency Lab - Automated Essay Scoring 2.0

> 主题：nlp ｜ 子类：— ｜ 领域：教育 ｜ 类别：Featured
> 截止：2024-07-02 ｜ 队伍数：2706 ｜ 机制：代码赛 ｜ 指标：Cohen's Quadratic Weighted Kappa
> 数据来源：`intel/learning-agency-lab-automated-essay-scoring-2/`（120 条主题索引 + 8 篇 write-up 正文）

## 1. 任务与数据

- **预测目标**：给中学生作文打整体分（1–6 的序数标签）。
- **数据陷阱（本场核心）**：训练集由**两个来源不同的数据集**拼接而成（Persuade 与 Kaggle 自有），
  而**测试集的文本分布更接近其中的 Kaggle 子集**——社区首先发现了这一点，1st/2nd 都把它当作关键。
  两个子集的**评分标准也不一致**，必须让"旧数据"适配"新评分口径"。

## 2. 验证方案

| 方案 | 使用者 | 说明 |
| --- | --- | --- |
| 分层 CV + CV-LB 相关性验证 | 1st | 标题即"Trust CV (and LB a bit)"：以 CV 为主，LB 做辅助确认 |
| 两阶段训练 + 分源验证 | 2nd | 先在 Kaggle-Persuade 上训练，再适配目标分布 |
| 公开基线对照 | 社区 | cdeotte 的 DeBERTa starter 是公认起点（LB 0.800+） |

## 3. 方案谱系

| 方案 | 名次 | 关键点 |
| --- | --- | --- |
| DeBERTa 集成 + **两轮伪标签** + 浮点预测阈值化取整 | 1st | 先用数据分析找出新数据的评分模式，再把"旧数据"通过伪标签赋予"新分数" |
| 5 模型投票 + 两阶段训练 | 2nd | 同样建立在"两个数据集"的发现之上 |
| DeBERTa 入门配置 | 社区 | 单模型即可到 LB 0.800+ |

## 4. 关键技巧

- **发现数据来源差异**：把训练集拆成两个子集分别分析分数分布，是本题最重要的动作。
- **伪标签对齐评分口径**：用模型给旧数据打新分数（两轮），使全量数据与测试口径一致。
- **序数指标的处理**：QWK 对阈值敏感，把连续预测**阈值化**为整数可提升分数。
- **两阶段训练**：先通用预训练数据，再目标分布适配。

## 5. 可迁移性评估

- **可直接迁移**：
  - **先确认训练集是否由多个来源拼接**（分数分布双峰是信号）。
  - 伪标签用于"统一标注口径"而不只是扩充数据。
  - 序数回归指标（QWK 类）要显式优化阈值。
- **需要前提**：
  - 伪标签需要足够强的教师模型与可控的训练预算（代码赛时限内要能跑完）。
- **不建议照搬**：
  - 直接在所有数据上混训而不区分来源（会稀释目标分布信号）。

## 6. 对新手的关键启示

1. **先看分数分布**：本场的双峰分布直接暴露了"两个数据集"的结构。
2. **数据口径不一致时，伪标签是标准解法**。
3. **序数指标要单独处理阈值**，不要只做回归。

## 7. 出处

- 讨论区索引：`intel/learning-agency-lab-automated-essay-scoring-2/topics.md`（120 条）
- 已收录 write-up（8 篇）：
  - 1st（86 票）：https://www.kaggle.com/competitions/learning-agency-lab-automated-essay-scoring-2/discussion/516791
  - 2nd（88 票）：https://www.kaggle.com/competitions/learning-agency-lab-automated-essay-scoring-2/discussion/516582
  - 2nd 详细（57 票）：https://www.kaggle.com/competitions/learning-agency-lab-automated-essay-scoring-2/discussion/516790
  - 4th（95 票）：https://www.kaggle.com/competitions/learning-agency-lab-automated-essay-scoring-2/discussion/516639
  - 6th（40 票）：https://www.kaggle.com/competitions/learning-agency-lab-automated-essay-scoring-2/discussion/516814
