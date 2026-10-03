# Tabular Playground Series - Nov 2022（Log Loss，"被忽视的信息"：数据是预测不是特征）

> 主题：tabular ｜ 子类：— ｜ 领域：—（合成数据） ｜ 类别：Playground
> 截止：2022-11-30 ｜ 队伍数：689 ｜ 机制：标准赛 ｜ 指标：Log Loss
> 数据来源：`intel/tabular-playground-series-nov-2022/`（74 条主题索引 + 6 篇 write-up 正文）

## 1. 任务与数据（本场最独特的结构）

- 描述原话："给你一个**包含预测结果的文件夹**"——数据列其实是**其它模型给出的概率预测**（质量可疑），而不是普通特征；
- 社区发现（"被忽视的信息"帖）：这些预测的概率**系统性偏高**（可视化呈偏差形态），猜测是生成时正类权重偏高；
- 修复方式：`x' = expit(logit(x) − 1.17)`——**单参数 logit 平移**；对比 isotonic 回归：平移在单模型上更好（0.5281 vs 0.5286），因为 isotonic 会过拟合阶梯而 logit 平移只拟合一个参数；在全数据上 logit 校准 0.5258。

## 2. 验证方案

- 10/20 折 StratifiedKFold（1st）；社区强调：校准类操作要用 CV 验证（本案 isotonic vs logistic 的对照就是范例）。

## 3. 模型家族

| 方案 | 使用者层次 | 关键点 | 出处 |
| --- | --- | --- | --- |
| 多架构多特征集成（LightAutoML/XGB/LGBM/2×NN） | 1st（公开第 7→私榜第 1） | 10-20 折 | topic 369674 |
| logit 平移/校准反演 | 社区分析 | 一个常数带来大提升 | topic 364013 |
| 7th / 3rd / 主机方方案 | 前列 | 集成与堆叠 | topic 369731 |

## 4. 关键技巧

- **反演数据生成者**：发现"输入是预测"后，用 logit 平移/逻辑回归校准修正系统性偏差——对任何"用模型输出当特征"的场景（stacking、蒸馏、伪标签）都通用的校准思维。
- 1st 的路线仍是"多架构 + 不同特征 + 10/20 折"：**校准 + 扎实集成**双管齐下。
- 区分"校准"与"拟合"：本场 isotonic 更灵活却更差；参数越少越稳（偏差是单参数性质的）。

## 5. 可迁移性评估

- **可直接迁移**：logit 平移校准（先估偏差方向与量级）；"输入是概率"时的校准先行；isotonic vs logistic 的偏差-方差对照；大折数（10/20）。
- **需要前提**：能观测到分布形态的偏差；有 OOF 做校准验证。
- **不建议照搬**：直接对概率特征套 GBDT 而不校准（忽略结构）；用过灵活的方法（isotonic）拟合简单偏差。

## 6. 对新手的关键启示

- **读题读数据到"每列本质是什么"**：本场的胜负手在一句话（"给定的是预测"）。
- 看到概率分布"整体偏高/偏低"，先想 logit 平移而不是换模型。
- 校准不是附属步骤，本场它比建模本身更值钱。

## 7. 出处

- 1st：多架构集成（公开 7 → 私榜 1）：https://www.kaggle.com/competitions/tabular-playground-series-nov-2022/discussion/369674
- 被忽视的信息：logit 平移校准：https://www.kaggle.com/competitions/tabular-playground-series-nov-2022/discussion/364013
- 7th：集成路线：https://www.kaggle.com/competitions/tabular-playground-series-nov-2022/discussion/369731
