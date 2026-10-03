# Optiver - Trading at the Close

> `optiver-trading-at-the-close` ｜ Featured ｜ 指标 Mean Columnwise Mean Absolute Error ｜ 4436 队 ｜ 截止 2024-03-22

本页汇总该场 **1 条 ≥50 票 GM 主题帖**、**3 条断言**、**1 条高票评论**。

## GM 主题帖

| 票 | 选手 | 日期 | 主题 |
| --- | --- | --- | --- |
| 338 | [@hydantess](https://www.kaggle.com/hydantess) | 2024-03-29 | [1st place solution](https://www.kaggle.com/competitions/optiver-trading-at-the-close/discussion/487446) |

## 断言（条件→动作→机制→结果）

| 选手 | 等级 | 阶段 | 动作（节选） | 出处 |
| --- | --- | --- | --- | --- |
| @hydantess | B | 集成与融合 | 三个异构模型按 0.5/0.3/0.2 加权，权重在验证集上搜索；三模型共享同一套 300 特征 | [optiver-trading-at-the-close#487446-01](https://www.kaggle.com/competitions/optiver-trading-at-the-close/discussion/487446) |
| @hydantess | B | 建模与训练 | 每 12 天重训一次共 5 次；训练数据按天存文件、逐天加载；最终因推理超时实际只做 4 次在线更新 | [optiver-trading-at-the-close#487446-02](https://www.kaggle.com/competitions/optiver-trading-at-the-close/discussion/487446) |
| @hydantess | C | 复盘与流程 | 明确放弃四类方向：1dCNN/MLP 与主模型融合、GRU 用多日输入、更大的 Transformer（如 deberta）、用 GBDT 预测目标桶均值 | [optiver-trading-at-the-close#487446-03](https://www.kaggle.com/competitions/optiver-trading-at-the-close/discussion/487446) |

## 高票评论

| 票 | 选手 | 日期 | 摘录 | 出处 |
| --- | --- | --- | --- | --- |
| 14 | @hydantess | 2024-03-31 | I love China. 😀 | [487446](https://www.kaggle.com/competitions/optiver-trading-at-the-close/discussion/487446) |

## 关联资产

- 深读：`analysis/deep/optiver-trading-at-the-close.md`
- 结构化摘要：`notes/tabular/optiver-trading-at-the-close.md`
- 归档讨论区：`intel/optiver-trading-at-the-close/`（主题 1 条有 ≥50 票帖，图证 0 个）
