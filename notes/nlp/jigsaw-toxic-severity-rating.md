# Jigsaw - Toxic Severity Rating

> 主题：nlp ｜ 子类：— ｜ 领域：内容审核 ｜ 类别：Featured
> 截止：2022-02-07 ｜ 队伍数：2301 ｜ 机制：代码赛 ｜ 指标：与标注者排序的一致性
> 数据来源：`intel/jigsaw-toxic-severity-rating/`（120 条主题索引 + 8 篇 write-up 正文）

## 1. 任务与数据

- **预测目标**：对评论的"毒性严重程度"排序（不是简单二分类，而是排序/相对比较任务）。
- **数据形态**：文本 + 人工标注；标签噪声大（标注者之间本身就不一致），因此**指标定义为"与标注者的一致性"**。
- **构造陷阱**：
  - **公开榜参考价值低**（14th 明确指出），必须依赖本地验证。
  - 数据集跨赛事复用普遍（Jigsaw 系列多届），**文本泄漏**（同一文本出现在不同折）是主要风险。

## 2. 验证方案

| 方案 | 使用者 | 说明 |
| --- | --- | --- |
| **Union-Find 分组切分** | 14th | 把内容相关的样本聚成一组，避免同一文本跨折泄漏 |
| 以验证分数为唯一决策依据 | 14th | "公开榜没用，就最大化验证分" |
| 多数据库交叉验证 | 14th | 合并历届 Jigsaw 数据后仍需防泄漏 |

## 3. 方案谱系

| 方案 | 名次 | 关键点 |
| --- | --- | --- |
| 6 个（5 折）Transformer 的加权平均 | 14th | 训练数据合并了 Jigsaw 1/2、Ruddit、OffensEval2020 等外部数据集 |
| RoBERTa-base + RoBERTa-large + Detoxify 组合 | 4th | 用公开的毒性检测模型作为成员 |
| 多模型融合 | 1st / 7th | 见讨论区 |
| RAPIDS 加速的推理方案 | 52nd 银牌 | 工程侧优化 |

## 4. 关键技巧

- **防泄漏的折划分（Union-Find）**：把可能互相重复/近似的文本分到同一折，是文本赛的通用防泄漏手段。
- **多数据集合并**：历届 Jigsaw 数据 + 外部毒性数据集（Ruddit、OffenseEval）显著增强泛化。
- **现成毒性模型作为集成成员**（Detoxify）可以省下大量训练成本。
- **信任 CV**：公开榜差时不要被带偏。
- **横向索引**：社区整理了"Jigsaw 系列历届全部方案"清单，是跨赛事学习的范例。

## 5. 可迁移性评估

- **可直接迁移**：
  - **Union-Find / 相似度分组做折划分**，防止文本或实体泄漏。
  - 合并同领域历届比赛数据（Kaggle 上极常见）。
  - 排序类任务的评估要用一致性/相关性指标而非准确率。
- **需要前提**：
  - 需要判断样本相似度的手段（文本用 TF-IDF/嵌入均可）。
  - 外部数据的许可与质量。
- **不建议照搬**：
  - 跟踪公开榜（本场公开榜信息量低）。

## 6. 对新手的关键启示

1. **折划分先于建模**：文本赛最常见的自欺就是同一文本跨折泄漏。
2. **同系列历届数据是免费的训练集**，但要用同一套防泄漏策略。
3. **公开榜可能完全没用**——先量化 CV-LB 相关性再决定依据哪个。
4. **善用现成开源模型**作为集成成员，性价比极高。

## 7. 出处

- 讨论区索引：`intel/jigsaw-toxic-severity-rating/topics.md`（120 条）
- 已收录 write-up（8 篇）：
  - 1st（212 票）：https://www.kaggle.com/competitions/jigsaw-toxic-severity-rating/discussion/306274
  - 4th（58 票）：https://www.kaggle.com/competitions/jigsaw-toxic-severity-rating/discussion/306084
  - 14th（64 票）：https://www.kaggle.com/competitions/jigsaw-toxic-severity-rating/discussion/306063
  - 52nd 银牌（57 票）：https://www.kaggle.com/competitions/jigsaw-toxic-severity-rating/discussion/306074
  - Jigsaw 历届全部方案汇总（56 票）：https://www.kaggle.com/competitions/jigsaw-toxic-severity-rating/discussion/286333
