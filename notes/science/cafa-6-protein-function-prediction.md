# CAFA 6 - Protein Function Prediction

> 主题：science ｜ 子类：— ｜ 领域：生物信息 ｜ 类别：Research
> 截止：2026-06-01 ｜ 队伍数：2259 ｜ 机制：标准赛 ｜ 指标：蛋白质功能（GO 术语）多标签 F 值
> 数据来源：`intel/cafa-6-protein-function-prediction/`（80 条主题索引 + 6 篇 write-up 正文）

## 1. 任务与数据

- 预测目标：预测蛋白质的**功能注释**（Gene Ontology 术语，多标签、层级结构）。
- 数据形态：氨基酸序列 + 已有注释；GO 术语有**本体层级**（父子关系），类别极多且极不平衡。
- 构造陷阱：
  - 标签空间巨大且长尾；
  - 评估分 BP/MF/CC 三个本体，指标各不同；
  - 序列相似性是最强的传统信号（BLAST/同源迁移）。

## 2. 方案谱系

| 方案 | 名次 | 关键点 |
| --- | --- | --- |
| 1st 方案 | 1st | 见讨论区 |
| **py-boost（梯度提升）+ GCN（图卷积）+ 人工规则** | 2nd | 三类方法混合：树模型处理特征、图网络利用 GO 层级/蛋白互作、规则兜底 |
| 序列模型方案 | 3rd | 本地验证分 BP 0.398 / MF 0.712 / CC 0.610（分本体报告） |

## 3. 关键技巧

- **分层多标签**：GO 本体结构可作先验（父节点预测可传播给子节点）。
- **多方法混合**：GBDT + 图网络 + 规则（与 Leash-BELKA、Polymer 的多表示融合同源）。
- **分本体验证**（BP/MF/CC 分别报告）。
- **序列同源信息**是强基线（传统生物信息方法不可忽视）。

## 4. 可迁移性评估

- **可直接迁移**：
  - **层级多标签的父子传播**（商品类目、代码标签体系通用）；
  - 图结构利用（本体、互作网络）；
  - 按子任务（本体）分别验证。
- 需要前提：生物信息工具链（序列比对、GO 本体）。
- 不建议照搬：忽略层级结构的平铺多标签。

## 5. 对新手的关键启示

1. **标签有层级时，把层级当特征**（父→子传播）。
2. **传统方法（序列同源）常常是强基线**，不要一上来就上大模型。
3. 与 CAFA 系列往届、Leash-BELKA 对照：**蛋白质/分子类比赛的主流是"多表示 + 多方法混合"**。

## 6. 出处

- 讨论区索引：`intel/cafa-6-protein-function-prediction/topics.md`（80 条）
- 已收录 write-up（6 篇）：
  - 1st（20 票）：https://www.kaggle.com/competitions/cafa-6-protein-function-prediction/discussion/709383
  - 2nd py-boost + GCN（17 票）：https://www.kaggle.com/competitions/cafa-6-protein-function-prediction/discussion/711635
  - 3rd（15 票）：https://www.kaggle.com/competitions/cafa-6-protein-function-prediction/discussion/709281
