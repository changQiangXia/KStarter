# Forecasting Sticker Sales

> `playground-series-s5e1` ｜ Playground ｜ 指标 Mean Absolute Percentage Error ｜ 2722 队 ｜ 截止 2025-01-31

本页汇总该场 **2 条 ≥50 票 GM 主题帖**、**6 条断言**、**0 条高票评论**。

## GM 主题帖

| 票 | 选手 | 日期 | 主题 |
| --- | --- | --- | --- |
| 86 | [@cdeotte](https://www.kaggle.com/cdeotte) | 2025-02-01 | [2nd Place - Stacking Transformer and Linear Regression](https://www.kaggle.com/competitions/playground-series-s5e1/discussion/560549) |
| 80 | [@cdeotte](https://www.kaggle.com/cdeotte) | 2025-01-24 | [Transformer Achieves LB=0.052 Without Feature Engineering!](https://www.kaggle.com/competitions/playground-series-s5e1/discussion/559314) |

## 断言（条件→动作→机制→结果）

| 选手 | 等级 | 阶段 | 动作（节选） | 出处 |
| --- | --- | --- | --- | --- |
| @cdeotte | A | 数据理解 | 误差范围正负 6%；可选常数 1.06、1.00 或线性趋势；作者最终提交常数 1.06 与轻微线性上升两版 | [playground-series-s5e1#560549-01](https://www.kaggle.com/competitions/playground-series-s5e1/discussion/560549) |
| @cdeotte | A | 建模与训练 | 全 5 产品共训 15 epochs cosine；加 30 个假日 bool；用 2017/2018 的首轮预测做伪标签训第二轮、再训第三轮；5 seeds 取中位数；不用 mu | [playground-series-s5e1#560549-02](https://www.kaggle.com/competitions/playground-series-s5e1/discussion/560549) |
| @cdeotte | A | 特征与数据工程 | 逐国 EDA 对齐假日窗口并检查销售是否一致升高/降低；线性回归对这些窗口加权提升，Transformer 加 bool 特征；保持 m=1.06 → public 0.04733 | [playground-series-s5e1#560549-03](https://www.kaggle.com/competitions/playground-series-s5e1/discussion/560549) |
| @cdeotte | A | 集成与融合 | 先用线性回归预测 2010 到 2016，再让 transformer 学 truth 减 prediction 的误差，最终提交两者之和 → public 0.04526 / p | [playground-series-s5e1#560549-04](https://www.kaggle.com/competitions/playground-series-s5e1/discussion/560549) |
| @cdeotte | A | 建模与训练 | RNN、CNN、Transformer block 都把 (batch, seq, in_features) 映射为 (batch, seq, out_features)，堆叠生成 | [playground-series-s5e1#559314-01](https://www.kaggle.com/competitions/playground-series-s5e1/discussion/559314) |
| @cdeotte | A | 工程/流程 | 输入 1440 天预测 32 天；第二次把预测拼回最近 2 年 11 个月训练数据再预测；循环 35 次得到 3 年预测 | [playground-series-s5e1#559314-02](https://www.kaggle.com/competitions/playground-series-s5e1/discussion/559314) |

## 高票评论

_无 ≥10 票评论_

## 关联资产

- 深读：`analysis/deep/playground-series-s5e1.md`
- 结构化摘要：`notes/tabular/playground-series-s5e1.md`
- 归档讨论区：`intel/playground-series-s5e1/`（主题 2 条有 ≥50 票帖，图证 9 个）
