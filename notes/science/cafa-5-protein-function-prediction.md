# CAFA 5 - Protein Function Prediction

> 主题：science ｜ 子类：— ｜ 领域：生物信息 ｜ 类别：Research
> 截止：2023-12-20 ｜ 队伍数：1625 ｜ 机制：标准赛 ｜ 指标：GO 术语多标签（F 值类）
> 数据来源：`intel/cafa-5-protein-function-prediction/`（80 条主题索引 + 6 篇 write-up 正文）

## 1. 任务与数据

- 预测目标：预测蛋白质的 Gene Ontology 功能注释（多标签、层级结构）。
- 数据形态：氨基酸序列 + 已有注释 + 分类本体；类别极多且长尾。
- 构造陷阱：三个本体（BP/MF/CC）指标各异；序列同源是最强的传统信号；长尾极严重。

## 2. 方案谱系

| 方案 | 名次 | 关键点 |
| --- | --- | --- |
| 1st（GOCurator 团队，复旦大学） | 1st | 私榜 0.61623；团队有生物信息背景 |
| 其他方案 | 见讨论区 | |

## 3. 关键技巧（结合 CAFA 系列共性）

- **序列同源迁移**（BLAST/嵌入检索）是基线中的基线。
- **本体层级作为先验**（父→子传播，见 CAFA 6 的做法）。
- **分本体（BP/MF/CC）分别建模与验证**。
- 长尾类别需要专门的采样/损失策略。

## 4. 可迁移性评估

- **可直接迁移**：层级多标签的父子传播；分本体验证；序列相似度基线。
- 需要前提：生物信息工具链。
- 不建议照搬：忽略本体结构。

## 5. 对新手的关键启示

1. **CAFA 系列两年（5/6 届）的方法连续**：序列同源 + 本体层级 + 多方法混合 + 分本体验证。
2. 与 Leash-BELKA、Polymer 对照：**生物分子类比赛的主线是"多表示 + 领域先验"**。

## 6. 轻读结论（2026-10 补）

**一句话**：13k+ 标签的极端多标签 = **多源组件（序列/结构/文本/网络）+ 学习排序集成**；文本与结构组件的单点强度超过经典 BLAST/InterPro 基线（GOXML 0.577 / GORetrieval 0.557 / LR-MEM 0.556 vs BLAST-KNN 0.475），而网络 KNN（0.304）必须**按物种过滤**后才有用。

- 1st（GOCurator，私榜 0.61623）：NetGO 3.0 + 四个新组件（LR-MEM / FoldSeek-KNN 结构 / GOXML 文献 AttentionXML / GORetrieval 两阶段重排）+ 原有 BLAST/InterPro/ESM/Text/Net-KNN；**Learning-to-Rank 融合**（输入含 20 维物种 one-hot）；验证集按测试集物种分布采样 1000 蛋白；Net-KNN 只保留 top-15 物种；"文本/结构组件 + NetGO 3.0 ≈ 90% 最终性能"。
- 2nd 私榜（434064）：T5/esm2-large/ankh + taxa one-hot；自研 **py-boost**（GPU 极端多输出 GBDT，4.5k 输出/1.5h·V100）+ 13k 输出 LogReg + NN；**条件概率重构**（0/1/NaN 目标掩码 → 预测 P(词|父词存在) → 按本体图序还原 `p_raw=p_cond×(1−∏(1−p_parent))`，可预测训练未见词）；简单 5 折最优。
- 3rd（464437）：T5/ESM2-t36/t48 + 90 taxa；**把 11 类非实验证据码标注当特征**（kernel=1 的 1D-CNN）。
- 指标：IA(v)=log2(Pr(Pa)/Pr(v)) + 加 1 平滑（68 票解释帖）。

**裁决**：极端多标签要"分源建模 + 排序融合"；本体层级与 IA 权重必须显式处理；网络/跨物种信息先做收益审计；验证集要匹配测试集物种分布。

**悬案**：4th–12th 方案缺失；1st 的 LTR 特征未展开；2nd 的条件概率方案贡献未独立量化。

## 7. 图表证据

![1st 的组件方法性能](../../intel/cafa-5-protein-function-prediction/bodies/466917_img/01.png)

**图 1**（topic 466917）：九组件 ave.wFmax 排行（GOXML/GORetrieval/LR-MEM 领先，Net-KNN 仅 0.304）。

## 8. 出处

- 讨论区索引：`intel/cafa-5-protein-function-prediction/topics.md`（80 条）
- 已收录 write-up（6 篇）：
  - 1st（34 票）：https://www.kaggle.com/competitions/cafa-5-protein-function-prediction/discussion/466917
  - 私榜 2 / 公开 5：Py-Boost（59 票）：https://www.kaggle.com/competitions/cafa-5-protein-function-prediction/discussion/434064
  - 3rd（31 票）：https://www.kaggle.com/competitions/cafa-5-protein-function-prediction/discussion/464437
  - IA 指标解释（68 票）：https://www.kaggle.com/competitions/cafa-5-protein-function-prediction/discussion/405237
  - ESM2 末层嵌入（47 票）：https://www.kaggle.com/competitions/cafa-5-protein-function-prediction/discussion/406168
  - 蛋白语言模型（41 票）：https://www.kaggle.com/competitions/cafa-5-protein-function-prediction/discussion/402565
- 轻读全本：`analysis/deep/cafa-5-protein-function-prediction.md`（Tier B 轻读：对照矩阵/裁决/证据分级/悬案 + 1 图证）
