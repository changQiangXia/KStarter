# Santa 2024 - The Perplexity Permutation Puzzle

> `santa-2024` ｜ Featured ｜ 指标 Santa 2024 Metric ｜ 1514 队 ｜ 截止 2025-01-31

本页汇总该场 **1 条 ≥50 票 GM 主题帖**、**2 条断言**、**0 条高票评论**。

## GM 主题帖

| 票 | 选手 | 日期 | 主题 |
| --- | --- | --- | --- |
| 92 | [@cdeotte](https://www.kaggle.com/cdeotte) | 2024-11-25 | [How To Use "Batch_Size>1" and get Correct Perplexity Score!](https://www.kaggle.com/competitions/santa-2024/discussion/548249) |

## 断言（条件→动作→机制→结果）

| 选手 | 等级 | 阶段 | 动作（节选） | 出处 |
| --- | --- | --- | --- | --- |
| @cdeotte | A | 工程/流程 | get_perplexity 支持 batch_size 并按 pad token 位置 mask loss（ignore_index），再按有效 token 数归一；发布 bat | [santa-2024#548249-02](https://www.kaggle.com/competitions/santa-2024/discussion/548249) |
| @cdeotte | B | 工程/流程 | tokenizer 必须 padding_side 设为 right：默认左 padding 时 shift 后会移除 pad token 而不是 bos token，导致分数错误 | [santa-2024#548249-01](https://www.kaggle.com/competitions/santa-2024/discussion/548249) |

## 高票评论

_无 ≥10 票评论_

## 关联资产

- 深读：`analysis/deep/santa-2024.md`
- 结构化摘要：`notes/sim-agent/santa-2024.md`
- 归档讨论区：`intel/santa-2024/`（主题 1 条有 ≥50 票帖，图证 0 个）
