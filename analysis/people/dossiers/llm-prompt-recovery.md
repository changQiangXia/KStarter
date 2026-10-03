# LLM Prompt Recovery

> `llm-prompt-recovery` ｜ Featured ｜ 指标 LLM Nerd-Off Sharpened Cosine Similarity ｜ 2175 队 ｜ 截止 2024-04-16

本页汇总该场 **1 条 ≥50 票 GM 主题帖**、**4 条断言**、**0 条高票评论**。

## GM 主题帖

| 票 | 选手 | 日期 | 主题 |
| --- | --- | --- | --- |
| 107 | [@philippsinger](https://www.kaggle.com/philippsinger) | 2024-04-17 | [2nd place solution: Team Danube](https://www.kaggle.com/competitions/llm-prompt-recovery/discussion/494497) |

## 断言（条件→动作→机制→结果）

| 选手 | 等级 | 阶段 | 动作（节选） | 出处 |
| --- | --- | --- | --- | --- |
| @philippsinger | A | 建模与训练 | 对约 32k 个 t5 token 暴力搜索最优均值 prompt；发现 TensorFlow 原版 SentencePiece 有特殊 token 注入保护，eos 标记不会被正 | [llm-prompt-recovery#494497-01](https://www.kaggle.com/competitions/llm-prompt-recovery/discussion/494497) |
| @philippsinger | A | 建模与训练 | 用 768 维输出 embedding 作目标训练分类模型（H2O LLM Studio），并直接实现 cosine similarity loss 对齐指标；local 到 0. | [llm-prompt-recovery#494497-02](https://www.kaggle.com/competitions/llm-prompt-recovery/discussion/494497) |
| @philippsinger | A | 验证设计 | 改用 Kaggle 补充文本（最有价值），用 gemma 生成新原文与改写 prompt；构造约 350 样本验证集，local 与提交均值 prompt 分数相关好；best L | [llm-prompt-recovery#494497-04](https://www.kaggle.com/competitions/llm-prompt-recovery/discussion/494497) |
| @philippsinger | B | 建模与训练 | 用 LLM 原始预测（只预测需要的改动，如 as a shanty）加 few-shot 加好均值 prompt 作为优化起点，再叠加 20 token 的 embedding 优 | [llm-prompt-recovery#494497-03](https://www.kaggle.com/competitions/llm-prompt-recovery/discussion/494497) |

## 高票评论

_无 ≥10 票评论_

## 关联资产

- 深读：`analysis/deep/llm-prompt-recovery.md`
- 结构化摘要：`notes/nlp/llm-prompt-recovery.md`
- 归档讨论区：`intel/llm-prompt-recovery/`（主题 1 条有 ≥50 票帖，图证 1 个）
