# CommonLit - Evaluate Student Summaries

> `commonlit-evaluate-student-summaries` ｜ Featured ｜ 指标 Mean Weighted Columnwise Root Mean Squared Error ｜ 2064 队 ｜ 截止 2023-10-11

本页汇总该场 **2 条 ≥50 票 GM 主题帖**、**4 条断言**、**0 条高票评论**。

## GM 主题帖

| 票 | 选手 | 日期 | 主题 |
| --- | --- | --- | --- |
| 129 | [@cpmpml](https://www.kaggle.com/cpmpml) | 2023-08-28 | [Offline pip install](https://www.kaggle.com/competitions/commonlit-evaluate-student-summaries/discussion/435153) |
| 58 | [@takoihiraokazu](https://www.kaggle.com/takoihiraokazu) | 2023-10-12 | [9th Place Solution](https://www.kaggle.com/competitions/commonlit-evaluate-student-summaries/discussion/446539) |

## 断言（条件→动作→机制→结果）

| 选手 | 等级 | 阶段 | 动作（节选） | 出处 |
| --- | --- | --- | --- | --- |
| @takoihiraokazu | A | 验证设计 | 提交两种 CV：排除 814d6b 与包含 814d6b；包含版 private 更好；因单 seed CV 波动，用 3 seeds 集成评估；最终提交用全量数据 ×3 seed | [commonlit-evaluate-student-summaries#446539-01](https://www.kaggle.com/competitions/commonlit-evaluate-student-summaries/discussion/446539) |
| @takoihiraokazu | A | 建模与训练 | text1=summary_text，text2=prompt_question+[SEP]+prompt_text；两个 deberta-v3-large + 一个 LSTM：第 | [commonlit-evaluate-student-summaries#446539-02](https://www.kaggle.com/competitions/commonlit-evaluate-student-summaries/discussion/446539) |
| @takoihiraokazu | A | 报告结果 | CV 0.495（3 seeds 集成）；814d6b 上 0.604982；public 0.456 / private 0.457 | [commonlit-evaluate-student-summaries#446539-03](https://www.kaggle.com/competitions/commonlit-evaluate-student-summaries/discussion/446539) |
| @cpmpml | C | 工程/流程 | 在 notebook 里写 requirements.txt，用 pip download 把依赖下载到当前目录并保存 notebook（输出即包缓存）；把该 notebook 作 | [commonlit-evaluate-student-summaries#435153-01](https://www.kaggle.com/competitions/commonlit-evaluate-student-summaries/discussion/435153) |

## 高票评论

_无 ≥10 票评论_

## 关联资产

- 深读：`analysis/deep/commonlit-evaluate-student-summaries.md`
- 结构化摘要：`notes/nlp/commonlit-evaluate-student-summaries.md`
- 归档讨论区：`intel/commonlit-evaluate-student-summaries/`（主题 2 条有 ≥50 票帖，图证 0 个）
