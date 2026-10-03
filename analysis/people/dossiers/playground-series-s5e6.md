# Predicting Optimal Fertilizers

> `playground-series-s5e6` ｜ Playground ｜ 指标 MAP@{K} ｜ 2648 队 ｜ 截止 2025-06-30

本页汇总该场 **1 条 ≥50 票 GM 主题帖**、**4 条断言**、**0 条高票评论**。

## GM 主题帖

| 票 | 选手 | 日期 | 主题 |
| --- | --- | --- | --- |
| 193 | [@cdeotte](https://www.kaggle.com/cdeotte) | 2025-07-01 | [1st Place - Fast GPU Experimentation with RAPIDS cuDF cuML](https://www.kaggle.com/competitions/playground-series-s5e6/discussion/587393) |

## 断言（条件→动作→机制→结果）

| 选手 | 等级 | 阶段 | 动作（节选） | 出处 |
| --- | --- | --- | --- | --- |
| @cdeotte | A | 特征与数据工程 | 先做 1/2/3/4 阶组合共 162 列，再用 cuML Target Encoder 对 7 个二值目标编码（1134 列），对原始数据再编码一次（再 1134 列），共 22 | [playground-series-s5e6#587393-01](https://www.kaggle.com/competitions/playground-series-s5e6/discussion/587393) |
| @cdeotte | A | 验证设计 | 同一模型用不同种子训练后先平均概率再选 top3；作者训练 100 个 5-fold XGB | [playground-series-s5e6#587393-03](https://www.kaggle.com/competitions/playground-series-s5e6/discussion/587393) |
| @cdeotte | A | 集成与融合 | 9 个模型（含公开 notebook 模型）各训练多种子，合计约 300 组预测，权重用 GPU hill climbing 搜索 | [playground-series-s5e6#587393-04](https://www.kaggle.com/competitions/playground-series-s5e6/discussion/587393) |
| @cdeotte | B | 数据工程 | 两种用法：作为新行（多数公开 notebook）或作为新列（用原始数据对类别组合做 target encoding）；最终集成同时需要两种 | [playground-series-s5e6#587393-02](https://www.kaggle.com/competitions/playground-series-s5e6/discussion/587393) |

## 高票评论

_无 ≥10 票评论_

## 关联资产

- 深读：`analysis/deep/playground-series-s5e6.md`
- 结构化摘要：`notes/tabular/playground-series-s5e6.md`
- 归档讨论区：`intel/playground-series-s5e6/`（主题 1 条有 ≥50 票帖，图证 1 个）
