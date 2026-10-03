#  Eedi - Mining Misconceptions in Mathematics

> `eedi-mining-misconceptions-in-mathematics` ｜ Featured ｜ 指标 MAP@{K} ｜ 1446 队 ｜ 截止 2024-12-12

本页汇总该场 **2 条 ≥50 票 GM 主题帖**、**9 条断言**、**2 条高票评论**。

## GM 主题帖

| 票 | 选手 | 日期 | 主题 |
| --- | --- | --- | --- |
| 127 | [@conjuring92](https://www.kaggle.com/conjuring92) | 2024-12-13 | [1st Place Solution Summary](https://www.kaggle.com/competitions/eedi-mining-misconceptions-in-mathematics/discussion/551402) |
| 76 | [@ebinan92](https://www.kaggle.com/ebinan92) | 2024-12-13 | [5th Place Solution](https://www.kaggle.com/competitions/eedi-mining-misconceptions-in-mathematics/discussion/551391) |

## 断言（条件→动作→机制→结果）

| 选手 | 等级 | 阶段 | 动作（节选） | 出处 |
| --- | --- | --- | --- | --- |
| @conjuring92 | A | 建模与训练 | 集成 e5-mistral-7b-instruct、bge-en-icl、Qwen2.5-14B 三个检索器；保留 top32 加相似度在 top 0.06 内的最多 32 个（动 | [eedi-mining-misconceptions-in-mathematics#551402-01](https://www.kaggle.com/competitions/eedi-mining-misconceptions-in-mathematics/discussion/551402) |
| @conjuring92 | A | 建模与训练 | 14B 点式排序到 top8；32B 点式到 top5；72B 列表式最终排序；vLLM enable_prefix_caching=True 提效 | [eedi-mining-misconceptions-in-mathematics#551402-02](https://www.kaggle.com/competitions/eedi-mining-misconceptions-in-mathematics/discussion/551402) |
| @conjuring92 | A | 特征与数据工程 | 对相关 misconception 聚类（如 linear 系列），让 Claude 生成更多例子并附 5 到 8 个相关 MCQ；先用竞赛数据微调两个 72B 点式模型并集成做伪 | [eedi-mining-misconceptions-in-mathematics#551402-04](https://www.kaggle.com/competitions/eedi-mining-misconceptions-in-mathematics/discussion/551402) |
| @ebinan92 | A | 验证设计 | 从 GroupKFold by QuestionId 改为 by SubjectId，让验证集包含更多仅出现在验证的 MisconceptionId，CV 更贴近 LB（例 0.6 | [eedi-mining-misconceptions-in-mathematics#551391-01](https://www.kaggle.com/competitions/eedi-mining-misconceptions-in-mathematics/discussion/551391) |
| @ebinan92 | A | 特征与数据工程 | 对缺失的每个 MisconceptionId，用 gemini-1.5-pro 做 4-shot 生成 QuestionName、SubjectName、ConstructName | [eedi-mining-misconceptions-in-mathematics#551391-02](https://www.kaggle.com/competitions/eedi-mining-misconceptions-in-mathematics/discussion/551391) |
| @ebinan92 | A | 特征与数据工程 | 把 questiontext、正确答案、错误答案喂 Qwen2.5-32B-Instruct 生成解释为什么选错的推理，作为 biencoder 与 listwise rerank | [eedi-mining-misconceptions-in-mathematics#551391-03](https://www.kaggle.com/competitions/eedi-mining-misconceptions-in-mathematics/discussion/551391) |
| @ebinan92 | A | 建模与训练 | 把 biencoder top 52 作为选项（52 个大小写字母），微调 Qwen2.5-32B-Instruct 只生成单个 token 取 logits 排序；推理取 top | [eedi-mining-misconceptions-in-mathematics#551391-04](https://www.kaggle.com/competitions/eedi-mining-misconceptions-in-mathematics/discussion/551391) |
| @ebinan92 | B | 复盘与流程 | 负结果：单 token 选项用双字母、字母加数字、日文假名都差于 52 个字母；QwQ-32B-preview、多步 rerank（7B 到 32B）、在 prompt 里加问题与 | [eedi-mining-misconceptions-in-mathematics#551391-05](https://www.kaggle.com/competitions/eedi-mining-misconceptions-in-mathematics/discussion/551391) |
| @conjuring92 | C | 特征与数据工程 | 先用 Claude 3.5 Sonnet 生成选错答案的理由与推理，再微调 Qwen2.5；推理时用微调模型生成 CoT 交给 reranker | [eedi-mining-misconceptions-in-mathematics#551402-03](https://www.kaggle.com/competitions/eedi-mining-misconceptions-in-mathematics/discussion/551402) |

## 高票评论

| 票 | 选手 | 日期 | 摘录 | 出处 |
| --- | --- | --- | --- | --- |
| 12 | @conjuring92 | 2024-12-13 | Prompt for synthetic data generation: You will be generating Multiple Choice Questions (MCQs) diagnose specifi | [551402](https://www.kaggle.com/competitions/eedi-mining-misconceptions-in-mathematics/discussion/551402) |
| 11 | @conjuring92 | 2024-12-13 | I used the metaprompt notebook to get started | [551402](https://www.kaggle.com/competitions/eedi-mining-misconceptions-in-mathematics/discussion/551402) |

## 关联资产

- 深读：`analysis/deep/eedi-mining-misconceptions-in-mathematics.md`
- 结构化摘要：`notes/nlp/eedi-mining-misconceptions-in-mathematics.md`
- 归档讨论区：`intel/eedi-mining-misconceptions-in-mathematics/`（主题 2 条有 ≥50 票帖，图证 1 个）
