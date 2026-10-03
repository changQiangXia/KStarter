# Playground Series S4E5 - 洪水概率预测（R²，行和特征是胜负手）

> 主题：tabular ｜ 子类：— ｜ 领域：水文（合成数据） ｜ 类别：Playground
> 截止：2024-05-31 ｜ 队伍数：2788 ｜ 机制：标准赛 ｜ 指标：R²
> 数据来源：`intel/playground-series-s4e5/`（80 条主题索引 + 6 篇 write-up 正文）

## 1. 任务与数据

- 预测目标：洪水概率（R²）；数据由 **Poisson 分布求和**生成（1st 的关键洞察）。
- 结构真相：**行内特征求和（sum）承载主要信号**，且 sum 在 72–75 区间时洪水概率显著更高（"魔法特征"）；原数据与训练数据完全不同，原数据特征本身无用。

## 2. 验证方案

- 1st：3 次重复 K 折训练全部模型 → 用 CV 选集成特征；两周内只用默认参数（early stopping），之后才用 Optuna（单次最长 5400 秒）微调少量关键超参。
- 2nd（Team Peaky Blenders）：56 个模型 + AutoGluon，公开 notebook 超参再利用。

## 3. 模型家族

| 方案 | 使用者层次 | 关键点 | 出处 |
| --- | --- | --- | --- |
| 30+ GBM 变体 + Ridge（positive=False, fit_intercept=False） | 1st | 特征筛选驱动的集成 | topic 509043 |
| Blends of Blends（56 模型 + AutoGluon） | 2nd | 公开超参 + 多层混合 | topic 509410 |
| AutoML Grand Prix 系（H2O DriverlessAI 等） | 社区 | 另一条产品线 | topic 500549 |

## 4. 关键技巧

- **手工构造行和特征**（决定胜负）：树模型无法自己想到"20 个特征求和"；一个 `sum ∈ [72,76)` 的二值特征把未调参 CatBoost 从 0.84722 → **0.86840**（社区称"第一个真正有用的特征"）。
- 1st 的特征清单：行内 sum/std/max、排序后的原特征、阈值计数特征（值 >6/>7/>8 的数量）、`groupby("sum")["FloodProbability"].std()`（离散目标的组内标准差 TE）。
- 目标变换：`target − 0.1 × mean(原特征)`（分离强信号 sum 与噪声偏差）。
- 无用小抄：原始特征本身、偏度/峰度、冗余列（置换重要性 + 后向选择剔除）。
- 集成细节：Ridge `positive=False, fit_intercept=False` 略优于正权重版本；AutoGluon 输出当 OOF 供再混合。

## 5. 可迁移性评估

- **可直接迁移**：行级聚合（sum/std/排序/阈值计数）先于一切复杂 FE；离散目标的组内统计编码；目标变换分离信噪；置换重要性的特征淘汰。
- **需要前提**：行内特征同尺度可加（本场 Poisson 和成立）。
- **不建议照搬**：不加验证地把原数据特征拼入（本场原数据分布完全不同）；忽视"简单聚合"直接上深度模型。

## 6. 对新手的关键启示

- **先画"目标 vs 简单聚合"的图**：本场一张 sum–target 图就找出了全赛最强的单特征。
- 树模型不会做加法：行内 sum/max/排序这类"显式算子特征"必须人工给。
- 两周默认参数 + 后两周少量调参，这个时间分配比全程调参更高效。

## 7. 出处

- 1st：Poisson 洞察与行和特征集成：https://www.kaggle.com/competitions/playground-series-s4e5/discussion/509043
- 2nd：Blends of Blends：https://www.kaggle.com/competitions/playground-series-s4e5/discussion/509410
- 第一个真正有用的特征（sum 72–75）：https://www.kaggle.com/competitions/playground-series-s4e5/discussion/499274
