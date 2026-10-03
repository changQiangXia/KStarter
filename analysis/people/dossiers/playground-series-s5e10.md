# Predicting Road Accident Risk

> `playground-series-s5e10` ｜ Playground ｜ 指标 Mean Squared Error ｜ 4082 队 ｜ 截止 2025-10-31

本页汇总该场 **1 条 ≥50 票 GM 主题帖**、**3 条断言**、**1 条高票评论**。

## GM 主题帖

| 票 | 选手 | 日期 | 主题 |
| --- | --- | --- | --- |
| 58 | [@cdeotte](https://www.kaggle.com/cdeotte) | 2025-11-01 | [5th Place - One Hundred Folds!](https://www.kaggle.com/competitions/playground-series-s5e10/discussion/614079) |

## 断言（条件→动作→机制→结果）

| 选手 | 等级 | 阶段 | 动作（节选） | 出处 |
| --- | --- | --- | --- | --- |
| @cdeotte | A | 集成与融合 | 2×XGB 加 3×TabM 加 2×XGB（stacked over 3×TabM）共 7 模型 hill climbing；TabM 变体含对原始生成函数预测残差的版本；另用他 | [playground-series-s5e10#614079-01](https://www.kaggle.com/competitions/playground-series-s5e10/discussion/614079) |
| @cdeotte | A | 工程/流程 | 所有 TabM 用 100 折重训；XGB 用同样 100 折以便 stacking | [playground-series-s5e10#614079-02](https://www.kaggle.com/competitions/playground-series-s5e10/discussion/614079) |
| @cdeotte | A | 建模与训练 | 先用 7 模型集成给测试打伪标签；把伪标签测试数据加入重训 TabM；再用新的 7 模型集成；最后与最佳公开 notebook 50/50 混合作为其中一个提交 | [playground-series-s5e10#614079-03](https://www.kaggle.com/competitions/playground-series-s5e10/discussion/614079) |

## 高票评论

| 票 | 选手 | 日期 | 摘录 | 出处 |
| --- | --- | --- | --- | --- |
| 16 | @cdeotte | 2025-10-08 | Thanks for this helpful discussion post. And thank you for all your wonderful notebooks. I've read, enjoyed, a | [610983](https://www.kaggle.com/competitions/playground-series-s5e10/discussion/610983) |

## 关联资产

- 深读：`analysis/deep/playground-series-s5e10.md`
- 结构化摘要：`notes/tabular/playground-series-s5e10.md`
- 归档讨论区：`intel/playground-series-s5e10/`（主题 1 条有 ≥50 票帖，图证 0 个）
