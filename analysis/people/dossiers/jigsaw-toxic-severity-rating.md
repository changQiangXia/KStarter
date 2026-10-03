# Jigsaw Rate Severity of Toxic Comments   

> `jigsaw-toxic-severity-rating` ｜ Featured ｜ 指标 Jigsaw Agreement with Annotators ｜ 2301 队 ｜ 截止 2022-02-07

本页汇总该场 **2 条 ≥50 票 GM 主题帖**、**6 条断言**、**1 条高票评论**。

## GM 主题帖

| 票 | 选手 | 日期 | 主题 |
| --- | --- | --- | --- |
| 212 | [@wowfattie](https://www.kaggle.com/wowfattie) | 2022-02-08 | [1st place solution with code](https://www.kaggle.com/competitions/jigsaw-toxic-severity-rating/discussion/306274) |
| 57 | [@cdeotte](https://www.kaggle.com/cdeotte) | 2022-02-08 | [52nd - Silver Medal - RAPIDS Forest Inference Library!](https://www.kaggle.com/competitions/jigsaw-toxic-severity-rating/discussion/306074) |

## 断言（条件→动作→机制→结果）

| 选手 | 等级 | 阶段 | 动作（节选） | 出处 |
| --- | --- | --- | --- | --- |
| @cdeotte | A | 验证设计 | 最终两个提交在 public 排 1500 与 1800，private 都到 52；两者都是 leak-free CV 0.707、public 0.802、private 0. | [jigsaw-toxic-severity-rating#306074-01](https://www.kaggle.com/competitions/jigsaw-toxic-severity-rating/discussion/306074) |
| @cdeotte | A | 特征与数据工程 | 用旧赛数据与标签预训练的 roBERTa-base 提 768 维、roBERTa-large 提 1024 维；用这些特征训 XGB 并用 RAPIDS FIL 推理（每秒最多  | [jigsaw-toxic-severity-rating#306074-02](https://www.kaggle.com/competitions/jigsaw-toxic-severity-rating/discussion/306074) |
| @cdeotte | A | 集成与融合 | 利用极快推理直接预测 14,000 × 14,000 等于 1.96 亿个评论对（cuDF 1.96 亿行 × 3584 列），再把对级概率聚合成每条评论的毒性分数 | [jigsaw-toxic-severity-rating#306074-03](https://www.kaggle.com/competitions/jigsaw-toxic-severity-rating/discussion/306074) |
| @wowfattie | B | 集成与融合 | 15 个模型（roberta/deberta × jigsaw18/jigsaw19/ruddit）做加权秩平均作为最终提交 | [jigsaw-toxic-severity-rating#306274-01](https://www.kaggle.com/competitions/jigsaw-toxic-severity-rating/discussion/306274) |
| @wowfattie | B | 集成与融合 | 对比三个数据源各自的 ensemble 与 all15：jigsaw18 0.7763/0.8103、jigsaw19 0.7509/0.8012、ruddit 0.8235/0. | [jigsaw-toxic-severity-rating#306274-02](https://www.kaggle.com/competitions/jigsaw-toxic-severity-rating/discussion/306274) |
| @wowfattie | B | 复盘与流程 | 对比含重复（-l）与不含重复训练：如 deberta-large jigsaw18 从 0.8139 降到 0.8085、deberta-base 从 0.8030 降到 0.80 | [jigsaw-toxic-severity-rating#306274-03](https://www.kaggle.com/competitions/jigsaw-toxic-severity-rating/discussion/306274) |

## 高票评论

| 票 | 选手 | 日期 | 摘录 | 出处 |
| --- | --- | --- | --- | --- |
| 11 | @cdeotte | 2021-11-11 | Great. Thank you. I really enjoyed the video tutorial. I love all the 3D visuals. | [286655](https://www.kaggle.com/competitions/jigsaw-toxic-severity-rating/discussion/286655) |

## 关联资产

- 深读：`analysis/deep/jigsaw-toxic-severity-rating.md`
- 结构化摘要：`notes/nlp/jigsaw-toxic-severity-rating.md`
- 归档讨论区：`intel/jigsaw-toxic-severity-rating/`（主题 2 条有 ≥50 票帖，图证 0 个）
