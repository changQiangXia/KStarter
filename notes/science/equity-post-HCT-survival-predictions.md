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

## 6. 轻读结论（2026-10 补）

**一句话**：生存排序的通用解法 = **P(事件) 分类 × 条件时间/排名回归 + 合并函数**；删失用 KM 权重/efs 特征显式处理；分层指标下"按组加噪声"是伪增益。

- 1st（186 票）：两目标 + 27 组合 + Optuna 权重（限 0.1–1 正则）→ CV 0.6965；**LGB/XGB 最佳深度=2**（特征交互极少）；GNN(KNN-25+GraphSAGE) 与 rank-loss 变体；race 噪声提 CV 不提 LB（图 1 为 merge 曲面）。
- 2nd（115 票）：依 SurvivalGAN 论文拆成 efs 分类 + efs_time 回归（efs 当特征、推理设 1）；R=p(efs=1)×sigmoid(−reg)；NN pairwise 损失直接逼近指标；AutoGluon Medium 也能金（私 0.697）。
- 4th（55 票）：因子化风险公式 + Kaplan-Meier 删失权重；纯 GBDT、4h 全流程、私 0.69936。
- 指标帖（301 票）：C-index 的配对逻辑 + 两种建模路线（合并目标 vs Cox/AFT）。

**裁决**：分解框架优于端到端；合并规则与子模型同等重要；合成数据的人工结构可反直觉地帮助建模（加入 efs=0 反而提升 efs=1 回归）。

**悬案**：3rd/5th 未细读；公平性评估细节缺失。

## 7. 图表证据

![merge 函数曲面](../../intel/equity-post-HCT-survival-predictions/bodies/566550_img/01.jpg)

**图 1**（topic 566550）：z=f(x=P(efs=0), y=归一化 efs_time) 合并曲面。

## 8. 出处

- 讨论区索引：`intel/equity-post-HCT-survival-predictions/topics.md`（80 条）
- 已收录 write-up（6 篇）：
  - 1st 两目标 + 集成（186 票）：https://www.kaggle.com/competitions/equity-post-HCT-survival-predictions/discussion/566550
  - 2nd（115 票）：https://www.kaggle.com/competitions/equity-post-HCT-survival-predictions/discussion/566522
  - 4th 因子化建模（55 票）：https://www.kaggle.com/competitions/equity-post-HCT-survival-predictions/discussion/566528
- 轻读全本：`analysis/deep/equity-post-HCT-survival-predictions.md`（Tier B 轻读：对照矩阵/裁决/证据分级/悬案 + 1 图证）
