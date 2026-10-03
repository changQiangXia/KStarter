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

## 6. 出处

- 讨论区索引：`intel/cafa-5-protein-function-prediction/topics.md`（80 条）
- 已收录 write-up（6 篇）：
  - 1st（34 票）：https://www.kaggle.com/competitions/cafa-5-protein-function-prediction/discussion/466917
  - 私榜 2 / 公开 5：Py-Boost（59 票）：https://www.kaggle.com/competitions/cafa-5-protein-function-prediction/discussion/434064
  - 3rd（31 票）：https://www.kaggle.com/competitions/cafa-5-protein-function-prediction/discussion/464437
