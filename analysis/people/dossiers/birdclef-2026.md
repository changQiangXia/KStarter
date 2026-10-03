# BirdCLEF+ 2026

> `birdclef-2026` ｜ Research ｜ 指标 Birdclef ROC AUC ｜ 4094 队 ｜ 截止 2026-06-03

本页汇总该场 **1 条 ≥50 票 GM 主题帖**、**6 条断言**、**0 条高票评论**。

## GM 主题帖

| 票 | 选手 | 日期 | 主题 |
| --- | --- | --- | --- |
| 169 | [@nikitababich](https://www.kaggle.com/nikitababich) | 2026-06-05 | [1st Place Solution: Noisy Student Meets Distillation](https://www.kaggle.com/competitions/birdclef-2026/discussion/704752) |

## 断言（条件→动作→机制→结果）

| 选手 | 等级 | 阶段 | 动作（节选） | 出处 |
| --- | --- | --- | --- | --- |
| @nikitababich | A | 建模与训练 | 第一阶段用 cosine loss 蒸馏 backbone（11 epochs、LR 5e-4、one-cycle、batch 64）；第二阶段低 LR（2e-4）端到端微调（8  | [birdclef-2026#704752-01](https://www.kaggle.com/competitions/birdclef-2026/discussion/704752) |
| @nikitababich | A | 建模与训练 | 跟踪单种子 SED 模型：1 stage 0.935、1 iter 0.946、2 iter 0.950、3 iter 0.949，两轮最优 | [birdclef-2026#704752-05](https://www.kaggle.com/competitions/birdclef-2026/discussion/704752) |
| @nikitababich | A | 集成与融合 | 集成不同 head、label space、输入与 CNN 家族；含 genus-level 专家（训练时同属标签取 max，预测时同属摊平），在 LB 0.96+ 仍提升 0.0 | [birdclef-2026#704752-06](https://www.kaggle.com/competitions/birdclef-2026/discussion/704752) |
| @nikitababich | B | 建模与训练 | 即使同 backbone 换 head 或 label 设计也重新蒸馏；蒸馏 loss 非零带来差异 | [birdclef-2026#704752-02](https://www.kaggle.com/competitions/birdclef-2026/discussion/704752) |
| @nikitababich | B | 特征与数据工程 | 把采样 LSS 的标签和归一化到 0.5（而非每个标签给 1）；注入比例 0.25 到 0.75、每 batch 2 条干净 LSS | [birdclef-2026#704752-03](https://www.kaggle.com/competitions/birdclef-2026/discussion/704752) |
| @nikitababich | C | 建模与训练 | 两个解法：把 PL 标签和上限压到低于 focal 标签和；LSS 与 PL 注入同一 batch 但不同样本、禁止重叠 | [birdclef-2026#704752-04](https://www.kaggle.com/competitions/birdclef-2026/discussion/704752) |

## 高票评论

_无 ≥10 票评论_

## 关联资产

- 深读：`analysis/deep/birdclef-2026.md`
- 结构化摘要：`notes/audio/birdclef-2026.md`
- 归档讨论区：`intel/birdclef-2026/`（主题 1 条有 ≥50 票帖，图证 1 个）
