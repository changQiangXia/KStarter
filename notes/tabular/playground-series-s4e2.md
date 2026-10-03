# Playground Series S4E2 - 肥胖风险多分类

> 主题：tabular ｜ 子类：— ｜ 领域：健康（合成数据） ｜ 类别：Playground
> 截止：2024-02-29 ｜ 队伍数：3587 ｜ 机制：标准赛 ｜ 指标：Accuracy
> 数据来源：`intel/playground-series-s4e2/`（80 条主题索引 + 6 篇 write-up 正文）

## 1. 任务与数据

- 预测目标：多分类肥胖风险等级（Accuracy）；数据量小、测试占比高（20/80 划分），大洗牌预期。
- 与同类赛的对照：4th 直接复用 S3E26（肝硬化多分类）的方案；"小数据 + 准确率指标 + 洗牌"是本类 Playground 的固定画像。

## 2. 验证方案

- 主流 5→20 折：**用 5 折做 HPO、用 20 折做最终训练**（2nd）；4th 用 9 份不同版本堆叠提交取"逐行最大类"。
- 70th 的名言：合成 Playground 的 train/test 同分布 → **可以信 CV**；但时序与小样本比赛不能。
- 4th 的洗牌归因：test 占比 20/80，应"重度加权最好的本地 CV"。

## 3. 模型家族

| 方案 | 使用者层次 | 关键点 | 出处 |
| --- | --- | --- | --- |
| XGB 元学习器堆叠（多方案预测当特征）+ 准确率优化 | 4th | 训练用 logloss、最终优化 Accuracy；9 份提交取行级最大类 | topic 480939 |
| XGB+LGBM 两模型 + 概率阈值化 | 2nd | 原数据加 4 次；按 CV 平均阈值权重 | topic 481062 |
| 树集成 + 一个 NN + 网格搜索权重 | 6th | NN 提供不同错误模式；以 CV 与 LB 不偏离为准 | topic 480795 |

## 4. 关键技巧

- **Accuracy 类指标的专门处理**：训练用 logloss（概率），提交前做概率阈值/权重优化（2nd 引用 KULDEEP 的阈值技巧）；4th 用行级"最大类投票"。
- **原数据复用**：拼行有效（2nd 加入 4 次！），同时保留两组不同 FE 轮换训练。
- 反例清单（2nd 实测）：伪标签无效、AutoML（autogluon/flaml）不如简单两模型集成——小数据场 AutoML 未必占优。
- 6th 的选取纪律：把 LB 视为 CV 的"第 N 折"，只交"高 CV 且 LB 不偏离"的模型。

## 5. 可迁移性评估

- **可直接迁移**：HPO 用浅折、最终用深折；Accuracy 指标的概率→阈值转换；行级多方案投票；小数据洗牌场的 CV 至上原则。
- **需要前提**：合成数据分布一致性（信 CV 的前提）；多方案预测存档。
- **不建议照搬**：小数据场盲目上 AutoML/伪标签（本场两个反例）；忽略阈值优化直接用 argmax 交 Accuracy 任务。

## 6. 对新手的关键启示

- Accuracy 不等于 argmax：概率 → 阈值/权重优化是独立的一课。
- 数据越小、洗牌越猛，"选提交"的技能权重越大（4th 直接移动 255 名）。
- 把上一场比赛的获奖方案搬过来并不可耻——4th 明确说这是从 S3E26 迁移的。

## 7. 出处

- 4th：堆叠 + 伪标签 + 指标优化：https://www.kaggle.com/competitions/playground-series-s4e2/discussion/480939
- 2nd：两模型 + 阈值化（含反例清单）：https://www.kaggle.com/competitions/playground-series-s4e2/discussion/481062
- 6th：树 + NN 的稳定性组合：https://www.kaggle.com/competitions/playground-series-s4e2/discussion/480795
- 70th：trust CV is all you need：https://www.kaggle.com/competitions/playground-series-s4e2/discussion/480787
