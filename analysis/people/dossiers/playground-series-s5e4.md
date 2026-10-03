# Predict Podcast Listening Time

> `playground-series-s5e4` ｜ Playground ｜ 指标 Mean Squared Error ｜ 3310 队 ｜ 截止 2025-04-30

本页汇总该场 **1 条 ≥50 票 GM 主题帖**、**5 条断言**、**1 条高票评论**。

## GM 主题帖

| 票 | 选手 | 日期 | 主题 |
| --- | --- | --- | --- |
| 234 | [@cdeotte](https://www.kaggle.com/cdeotte) | 2025-05-01 | [1st Place - RAPIDS cuML Stack - 3 Levels!](https://www.kaggle.com/competitions/playground-series-s5e4/discussion/575784) |

## 断言（条件→动作→机制→结果）

| 选手 | 等级 | 阶段 | 动作（节选） | 出处 |
| --- | --- | --- | --- | --- |
| @cdeotte | A | 数据理解 | 用 target 约等于 0.72 x Episode_Length_minutes 建立先验，其余 9 个特征视为对该线性关系的调制 | [playground-series-s5e4#575784-01](https://www.kaggle.com/competitions/playground-series-s5e4/discussion/575784) |
| @cdeotte | A | 集成与融合 | 用非线性 stack 而非 hill climbing/ridge 做 level-2，让融合器按场景选择不同基模型 | [playground-series-s5e4#575784-02](https://www.kaggle.com/competitions/playground-series-s5e4/discussion/575784) |
| @cdeotte | A | 集成与融合 | 12 个基础模型各做约 6 种变体共 75 个模型；level1 CV 11.8-13.2；level2 用 XGB/MLP 在 73 个 level1 模型上训练（11.56）； | [playground-series-s5e4#575784-03](https://www.kaggle.com/competitions/playground-series-s5e4/discussion/575784) |
| @cdeotte | A | 集成与融合 | 五个方向造多样性：不同特征工程、去掉 ELM、预测 ratio（target/ELM）、预测 ELM（可用 test 数据）、伪标签（train+test）；所有模型共用同一套 5 | [playground-series-s5e4#575784-05](https://www.kaggle.com/competitions/playground-series-s5e4/discussion/575784) |
| @cdeotte | B | 工程/流程 | 用 3 台 A100 与 RAPIDS cuDF/cuML，每天构建约 12 个新模型，只保留能提升 stack 的少数模型 | [playground-series-s5e4#575784-04](https://www.kaggle.com/competitions/playground-series-s5e4/discussion/575784) |

## 高票评论

| 票 | 选手 | 日期 | 摘录 | 出处 |
| --- | --- | --- | --- | --- |
| 14 | @cdeotte | 2025-05-01 | Thanks! 😀 ChatGPT suggested the MLP architecture and ChatGPT wrote the vectorized code to normalize numerical  | [575784](https://www.kaggle.com/competitions/playground-series-s5e4/discussion/575784) |

## 关联资产

- 深读：`analysis/deep/playground-series-s5e4.md`
- 结构化摘要：`notes/tabular/playground-series-s5e4.md`
- 归档讨论区：`intel/playground-series-s5e4/`（主题 1 条有 ≥50 票帖，图证 2 个）
