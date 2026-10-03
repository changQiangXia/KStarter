# Equity - Post-HCT Survival Predictions

> 主题：science（医疗表格）｜ 子类：— ｜ 领域：医疗 ｜ 类别：Research
> 截止：2025-03-05 ｜ 队伍数：3325 ｜ 机制：代码赛 ｜ 指标：生存分析的排序一致性（C-index 类）
> 数据来源：`intel/equity-post-HCT-survival-predictions/`（80 条主题索引 + 6 篇 write-up 正文）

## 1. 任务与数据

- 预测目标：造血干细胞移植（HCT）后的**生存结局**，含"是否发生事件"与"时间"两类信息（生存分析）。
- 数据形态：临床表格数据（含类别特征、缺失值、种族/社会经济变量）；**公平性（equity）也是主题之一**。
- 构造陷阱：
  - **指标是排序一致性**（C-index 类），不是简单分类或回归；
  - 存在删失（censoring）——必须正确处理；
  - 类别特征多、缺失多。

## 2. 方案谱系

| 方案 | 名次 | 关键点 |
| --- | --- | --- |
| **分类器 + 回归器分别训练，再用"魔法函数"融合** | 1st | 与 2nd/4th 思路一致：若患者"发生事件的概率高"就给高分，否则给较低分并……（核心是把概率与时间组合成排序分数） |
| 同类两段式融合 | 2nd / 4th | 作者明确指出这几支队伍用了相同思路 |

## 3. 关键技巧

- **把生存分析拆成"事件概率 + 时间"两个模型再融合**：这是本场前三名的共同做法。
- **面向排序的融合函数**（"magic function"）：直接优化 C-index 的结构，而不是分别优化两个子任务。
- **类别特征处理与缺失填补**在临床表格中依然是基本功。

## 4. 可迁移性评估

- **可直接迁移**：
  - **"概率模型 + 时间模型 → 排序分数"的两段式**（生存分析、风控、推荐排序通用）；
  - 面向指标结构设计融合函数；
  - 临床表格的缺失/类别处理。
- 需要前提：理解生存分析与删失的语义。
- 不建议照搬：直接用普通回归预测时间（会忽略删失）。

## 5. 对新手的关键启示

1. **先搞清指标是"排序"还是"值"**——本场的胜负在于排序分数怎么构造。
2. **两个子任务分别建模再融合**，比强行端到端更稳。
3. 医疗表格赛的公平性主题值得关注（数据中的社会变量会影响泛化）。

## 6. 出处

- 讨论区索引：`intel/equity-post-HCT-survival-predictions/topics.md`（80 条）
- 已收录 write-up（6 篇）：
  - 1st 两目标 + 集成（186 票）：https://www.kaggle.com/competitions/equity-post-HCT-survival-predictions/discussion/566550
  - 2nd（115 票）：https://www.kaggle.com/competitions/equity-post-HCT-survival-predictions/discussion/566522
  - 4th 因子化建模（55 票）：https://www.kaggle.com/competitions/equity-post-HCT-survival-predictions/discussion/566528
