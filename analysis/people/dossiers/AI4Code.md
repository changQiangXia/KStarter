# Google AI4Code – Understand Code in Python Notebooks

> `AI4Code` ｜ Featured ｜ 指标 AI4CodeKendallTau ｜ 1135 队 ｜ 截止 2022-11-10

本页汇总该场 **1 条 ≥50 票 GM 主题帖**、**4 条断言**、**0 条高票评论**。

## GM 主题帖

| 票 | 选手 | 日期 | 主题 |
| --- | --- | --- | --- |
| 62 | [@hydantess](https://www.kaggle.com/hydantess) | 2022-10-17 | [1st Place Solution](https://www.kaggle.com/competitions/AI4Code/discussion/360501) |

## 断言（条件→动作→机制→结果）

| 选手 | 等级 | 阶段 | 动作（节选） | 出处 |
| --- | --- | --- | --- | --- |
| @hydantess | A | 建模与训练 | 用单个 list-wise deberta-v3-large 在全部比赛数据上训练；输入为用 [SEP]/[CLS] 分隔的 cell 文本 | [AI4Code#360501-01](https://www.kaggle.com/competitions/AI4Code/discussion/360501) |
| @hydantess | A | 工程/流程 | MLM 15 epochs max_len 1024 需 3 天；训练 10 epochs max_len 2048 需 7 天；作者判断 max_len 5120 会大幅提升但  | [AI4Code#360501-04](https://www.kaggle.com/competitions/AI4Code/discussion/360501) |
| @hydantess | B | 特征与数据工程 | 有效：MLM 预处理（文本更短可吃更长输入）、用 deberta 而非 codebert 加 LSTM 头、更大 cell_cnt 与 seq_length（指标更看重长文本）、后 | [AI4Code#360501-02](https://www.kaggle.com/competitions/AI4Code/discussion/360501) |
| @hydantess | B | 复盘与流程 | 无效：mBART 翻译、code rank 进 dense 层、抽 embedding 再训 transformer、xlm-roberta-large 与 mdeberta-v3 | [AI4Code#360501-03](https://www.kaggle.com/competitions/AI4Code/discussion/360501) |

## 高票评论

_无 ≥10 票评论_

## 关联资产

- 深读：`analysis/deep/AI4Code.md`
- 结构化摘要：`notes/nlp/AI4Code.md`
- 归档讨论区：`intel/AI4Code/`（主题 1 条有 ≥50 票帖，图证 0 个）
