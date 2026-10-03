# Playground Series S5E4 - 播客收听时长预测

> 主题：tabular ｜ 子类：— ｜ 领域：媒体（合成数据） ｜ 类别：Playground
> 截止：2025-04-30 ｜ 队伍数：3310 ｜ 机制：标准赛 ｜ 指标：MSE（RMSE）
> 数据来源：`intel/playground-series-s5e4/`（80 条主题索引 + 6 篇 write-up 正文）

## 1. 任务与数据

- 预测目标：播客单集收听时长（回归 RMSE）。
- 数据主结构：`Listening_Time ≈ 0.72 × Episode_Length`，其余 9 个特征调制这条线性关系；**Episode_Length（ELM）承载 90%+ 信号，但 11.6% 缺失**——这一缺失结构是本场的方法分水岭。

## 2. 验证方案

- 所有模型统一 5 折，TE/伪标签全部折内完成（1st 反复强调"remove all leaks"）。
- 2nd：单 LightGBM + TE，1552 特征、79.5 万行，靠类型转换与避免复制在 **Kaggle CPU** 上 4 小时训完，5 seeds 平均。

## 3. 模型家族

| 方案 | 使用者层次 | 关键点 | 出处 |
| --- | --- | --- | --- |
| RAPIDS cuML 三级栈（75 模型） | 1st | 非线性 Level-2 处理"有/无 ELM"双情景 | topic 575784 |
| 单 LightGBM + TE（1552 特征） | 2nd | CPU 可复现；5 seeds | topic 575840 |
| TE + 三级结构 | 3rd | 同族配方 | topic 575862 |
| 100 OOF 的懒人集成 | 5th | 复盘两处失误 | topic 575839 |

## 4. 关键技巧

- **为什么要非线性栈**（1st 的核心论证）：数据存在"有 ELM / 无 ELM"两个情景，各自最优模型不同；**爬山/Ridge 这类线性 Level-2 只能做加权平均，而非线性栈能按情景选用不同模型的预测**。这是"深栈 vs 浅集成"的教科书案例。
- **多样性 ×5 训练矩阵**：同一批 12 个模型各训练 6 种变体——(1) 不同特征工程/超参；(2) **全行删掉 ELM** 训练（专攻缺失情景）；(3) 预测 `target/ELM` 比值再乘回；(4) 用 train+test 预测 ELM 再回填/替换/相乘；(5) 伪标签；(6) 特征子集差异。
- **用 test.csv 的列**：预测 ELM 时 train+test 联用（两边的列齐全）——无标签数据的合法用法。
- 平台期方法：每天用 3×A100 + cuDF/cuML 造一打新模型，只留能提升栈的少数。
- 2nd 的工程：1552 特征 + 精心 dtype 转换，让单模型在 CPU 上可训——**复现门槛也是竞争力**。

## 5. 可迁移性评估

- **可直接迁移**：缺失主特征的双情景建模（删特征专门训一组模型）；比值目标法；用无标签数据预测协变量再回填；多样性训练矩阵；深栈适配复杂交互。
- **需要前提**：GPU + RAPIDS（cuDF/cuML）用于规模化；大量 OOF 管理。
- **不建议照搬**：无差别堆三级栈（本场因交互深才值得）；忽视 TE 泄漏检查。

## 6. 对新手的关键启示

- **先找主特征与其缺失率**：本场一句"ELM 占 90% 信号且缺 11.6%"就决定了所有高分解法的形态。
- 集成器要匹配数据结构：线性加权 vs 非线性栈不是口味问题，而是"情景差异存在与否"的问题。
- 2nd 证明单模型+海量 TE 也能亚军——特征工程到位时，集成不是必需品。

## 7. 出处

- 1st：RAPIDS cuML 三级栈与多样性 ×5：https://www.kaggle.com/competitions/playground-series-s5e4/discussion/575784
- 2nd：单 LightGBM + 目标编码：https://www.kaggle.com/competitions/playground-series-s5e4/discussion/575840
- 3rd：TE 与三级结构：https://www.kaggle.com/competitions/playground-series-s5e4/discussion/575862
- 5th：100 OOF 与复盘：https://www.kaggle.com/competitions/playground-series-s5e4/discussion/575839
