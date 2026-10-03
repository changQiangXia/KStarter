# Feedback Prize - English Language Learning

> 主题：nlp ｜ 子类：— ｜ 领域：教育 ｜ 类别：Featured
> 截止：2022-11-29 ｜ 队伍数：2654 ｜ 机制：代码赛 ｜ 指标：按列加权的 RMSE 均值（6 个维度）
> 数据来源：`intel/feedback-prize-english-language-learning/`（120 条主题索引 + 8 篇 write-up 正文）

## 1. 任务与数据

- 预测目标：对 ESL 学生作文按 6 个维度打分（衔接、句法、词汇、短语、语法、书写规范），指标是 6 列 RMSE 的均值。
- 数据形态：约 3900 篇作文 + 少量伪标签数据，属于小样本多目标回归。
- 题目特点：多目标之间存在相关性（6 个维度并非独立），且评分本身带主观噪声。

## 2. 验证方案

| 方案 | 使用者 | 说明 |
| --- | --- | --- |
| MultilabelStratifiedKFold | 1st | 多目标分层，匹配 6 个目标的分层需求 |
| 固定 5 折 seed 42 | 2nd | 沿用社区方案，便于横向比较 |
| CV-LB 相关性检验 | 1st | 明确记录 CV 与 LB 近乎完美相关，因此放心用 CV 迭代 |

2nd place 的自我警示：用 Optuna 在全体 OOF 上调参、再按 CV 选权重，会导致二次过拟合——他明确指出"我应该在调参时用新的 OOF 而不是同一份"。

## 3. 方案谱系

| 方案 | 名次 | 关键点 |
| --- | --- | --- |
| 多模型 + 多池化 + 多最大长度 + 3 个嵌入模型融合 | 1st | 训练大量变体；用三种模型抽取嵌入加入集成 |
| 反向翻译 + 排序损失（rank loss） | 2nd | 伪标签训练；明确记录了调参过拟合的教训 |
| 24 个模型的集成（DeBERTa-v3-large 为主）+ 爬山法选权重 | 3rd | 不用伪标签；认为爬山法"像 Lasso 一样能挑出最优子集" |
| 往届 Feedback 系列方案迁移 | 社区帖 | 跨赛事复用（"Top Solutions From Feedback 1 & 2"） |

## 4. 关键技巧

- 多样性比单模型强度更重要：池化方式、最大长度、预训练模型家族的差异都能带来集成增益。
- 爬山法（hill climbing）做模型选择与加权：从最优单模型出发，逐步加入增益最大的模型；支持非负约束以避免过拟合。
- 嵌入模型作为额外特征源：用多个模型的句向量拼接。
- 反向翻译做数据增强，排序损失利用 6 个维度之间的序关系。
- 调参纪律：不要在用于选权重的同一份 OOF 上调参（2nd 的教训）。

## 5. 可迁移性评估

- 可直接迁移：小样本多目标回归的标准配方（多模型多池化 → 爬山法加权 → 检查 CV-LB 相关性）；爬山法融合稳健且可解释；跨届赛事方案复用。
- 需要前提：多张 GPU（1st 训练了大量模型变体）；伪标签需要额外数据源与可信教师模型。
- 不建议照搬：在同一份 OOF 上调参并选权重（过拟合风险，2nd 已明确复盘）。

## 6. 对新手的关键启示

1. 先确认 CV 与 LB 是否一致——本场一致性极好，因此可以放心用 CV 迭代；一致性差就要换策略。
2. 融合的常规做法是爬山法，比手工调权重更稳。
3. 多目标任务要利用目标间的相关性（排序损失、共享主干）。
4. 调参与选权重必须用不同的数据切分，否则会自欺。

## 7. 出处

- 讨论区索引：`intel/feedback-prize-english-language-learning/topics.md`（120 条）
- 已收录 write-up（8 篇）：
  - 1st（129 票）：https://www.kaggle.com/competitions/feedback-prize-english-language-learning/discussion/369457
  - 2nd（112 票）：https://www.kaggle.com/competitions/feedback-prize-english-language-learning/discussion/369369
  - 3rd（141 票）：https://www.kaggle.com/competitions/feedback-prize-english-language-learning/discussion/369609
  - 5th（74 票）：https://www.kaggle.com/competitions/feedback-prize-english-language-learning/discussion/369578
  - 往届方案（83 / 55 票）：https://www.kaggle.com/competitions/feedback-prize-english-language-learning/discussion/348967
