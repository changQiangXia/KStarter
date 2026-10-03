# OTTO - Multi-Objective Recommender System

> 主题：tabular ｜ 子类：recsys ｜ 领域：电商推荐 ｜ 类别：Featured
> 截止：2023-01-31 ｜ 队伍数：2574 ｜ 机制：标准赛 ｜ 指标：Weighted Recall@20
> 数据来源：`intel/otto-recommender-system/`（120 条主题索引 + 8 篇 write-up 正文）

## 1. 任务与数据

- **预测目标**：给定用户会话（session）行为序列，预测接下来可能交互的商品（点击 / 加购 / 下单三类目标），指标为加权召回率。
- **数据形态**：大规模会话点击流（数十亿级事件），候选空间是整个商品库（数十万），因此**必须先生成候选**。
- **核心结构**：与 H&M 类似——**召回（candidate generation）+ 排序（ranking）两阶段**，且"规则型召回"就能拿到很高分数。

## 2. 验证方案

| 方案 | 使用者 | 说明 |
| --- | --- | --- |
| 时间切分（用最后一段会话做验证） | 多队 | 与会话预测窗口对齐 |
| 分目标（点击/加购/下单）分别评估 | 多队 | 三类目标的行为模式差异大 |
| 公开 notebook 对照 | 社区 | 有完整的 "How To Build a GBT Ranker Model" 教程帖作为公共基线 |

## 3. 方案谱系

| 方案 | 名次 | 关键点 |
| --- | --- | --- |
| 候选生成 + GBT 排序 | 1st | 业界标准两阶段；候选来自共现矩阵等规则 |
| 共现矩阵 + 排序 | 2nd | 强调不同目标类型分别建模 |
| **纯规则**（无 ML 排序） | 3rd | 仅用规则型候选与规则打分达到 LB 0.590——本届最反直觉的结果 |
| 多模型排序 + 按秩集成 | 3rd（并列） | 团队各自单模型，最后按用户-目标的**排名**做集成 |
| GBT Ranker 教程 | 社区高票（335 票） | 系统讲解如何构造 ranker 训练数据（共现候选、负采样等） |

## 4. 关键技巧

- **共现矩阵（co-visitation）**：会话内/跨会话的商品共现是本题最强候选生成器。
- **规则也能打**：纯规则方案进前三，说明在该指标下**候选质量 > 排序模型复杂度**。
- **按秩集成（rank averaging）**：不同模型的分数尺度不同，按排名融合更稳健。
- **分目标建模**：点击、加购、下单三种行为分别预测后再合并。
- **训练数据自造**：ranker 的训练样本需要自己按时间窗构造（正负样本、候选集）。

## 5. 可迁移性评估

- **可直接迁移**：
  - **两阶段推荐框架**（召回 → 排序），以及"先做规则基线"的方法论。
  - 共现矩阵作为通用候选生成器。
  - 按秩集成而非直接平均概率。
  - 分目标（多行为类型）建模。
- **需要前提**：
  - 大规模数据的工程能力（数十亿事件）——本题很大程度是工程比赛。
  - 训练数据自造需要正确的时间切分与负采样策略。
- **不建议照搬**：
  - 直接上复杂深度模型而跳过规则基线。

## 6. 对新手的关键启示

1. **先做规则基线**：本场纯规则能进前三，说明"简单但正确"的候选生成价值极高。
2. **推荐比赛的胜负在召回阶段**，排序模型是精修。
3. **集成可以很简单**：按排名融合即可，不需要复杂权重搜索。
4. **注意赛事诚信**：本场有一支队伍因成员作弊被取消成绩（"imaginary 3rd place" 帖），提示组队时需谨慎。

## 7. 出处

- 讨论区索引：`intel/otto-recommender-system/topics.md`（120 条）
- 已收录 write-up（8 篇）：
  - GBT Ranker 教程（335 票）：https://www.kaggle.com/competitions/otto-recommender-system/discussion/370210
  - 1st（207 票）：https://www.kaggle.com/competitions/otto-recommender-system/discussion/384022
  - 2nd（90 票）：https://www.kaggle.com/competitions/otto-recommender-system/discussion/382790
  - 纯规则第三（151 票）：https://www.kaggle.com/competitions/otto-recommender-system/discussion/383013
  - 5th（103 票）：https://www.kaggle.com/competitions/otto-recommender-system/discussion/382802
  - 赛事诚信事件说明（98 票）：https://www.kaggle.com/competitions/otto-recommender-system/discussion/382879
