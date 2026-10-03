# Kaggle - LLM Science Exam

> `kaggle-llm-science-exam` ｜ Featured ｜ 指标 MAP@{K} ｜ 2664 队 ｜ 截止 2023-10-10

本页汇总该场 **2 条 ≥50 票 GM 主题帖**、**7 条断言**、**6 条高票评论**。

## GM 主题帖

| 票 | 选手 | 日期 | 主题 |
| --- | --- | --- | --- |
| 239 | [@philippsinger](https://www.kaggle.com/philippsinger) | 2023-10-11 | [1st place Short Solution Summary](https://www.kaggle.com/competitions/kaggle-llm-science-exam/discussion/446240) |
| 73 | [@cdeotte](https://www.kaggle.com/cdeotte) | 2023-10-11 | [Top 100 Solution - Fast RAPIDS TF-IDF RAG - 2xT4 GPU Acceleration!](https://www.kaggle.com/competitions/kaggle-llm-science-exam/discussion/446318) |

## 断言（条件→动作→机制→结果）

| 选手 | 等级 | 阶段 | 动作（节选） | 出处 |
| --- | --- | --- | --- | --- |
| @philippsinger | A | 建模与训练 | Wikipedia 分块 + e5 公开 embedding + 自写 PyTorch 余弦相似度（分块放 GPU，不用 FAISS）；每题 5 个 chunk、max_lengt | [kaggle-llm-science-exam#446240-01](https://www.kaggle.com/competitions/kaggle-llm-science-exam/discussion/446240) |
| @cdeotte | A | 集成与融合 | 早期单 DeBERTa-v3-large 加多条 RAG pipeline；发现新增 RAG 比加 DeBERTa 更提分 → 加速 RAG 加 DeBERTa：GPU Faiss | [kaggle-llm-science-exam#446318-01](https://www.kaggle.com/competitions/kaggle-llm-science-exam/discussion/446318) |
| @cdeotte | A | 特征与数据工程 | 50% 概率只用 5 个选项（不给问题）检索上下文，DeBERTa 也在无问题输入上训练；最佳 MAP@3 0.470（200 训练样本）、LB 0.904 | [kaggle-llm-science-exam#446318-03](https://www.kaggle.com/competitions/kaggle-llm-science-exam/discussion/446318) |
| @cdeotte | A | 工程/流程 | Choice Permute TTA：随机排列选项后 sentence transformer 得到不同 context，两套 logits 集成有增益；Drop 2 Wrong  | [kaggle-llm-science-exam#446318-04](https://www.kaggle.com/competitions/kaggle-llm-science-exam/discussion/446318) |
| @cdeotte | A | 复盘与流程 | 赛后发现 TF-IDF sublinear_tf=True 加 0.010 CV/LB；OOM 只能集成 7 条 RAG，作者事后认为应重 RAG 质量而非数量 | [kaggle-llm-science-exam#446318-05](https://www.kaggle.com/competitions/kaggle-llm-science-exam/discussion/446318) |
| @philippsinger | B | 验证设计 | 不采用 200 样本的 0.99+ CV，改用 6k 样本 CV 做模型选择；把标注模型的错误率视为理论分数上限 | [kaggle-llm-science-exam#446240-02](https://www.kaggle.com/competitions/kaggle-llm-science-exam/discussion/446240) |
| @cdeotte | B | 特征与数据工程 | RAG 类型：标题与关键词与首段找 6M Wikipedia top5 文章再取 20 句；128k STEM 章节 top5；12M 的 512 token chunks top | [kaggle-llm-science-exam#446318-02](https://www.kaggle.com/competitions/kaggle-llm-science-exam/discussion/446318) |

## 高票评论

| 票 | 选手 | 日期 | 摘录 | 出处 |
| --- | --- | --- | --- | --- |
| 19 | @philippsinger | 2023-10-11 | You can attach kernel outputs and obviously public datasets. There is no actual limit of how much data you can | [446422](https://www.kaggle.com/competitions/kaggle-llm-science-exam/discussion/446422) |
| 16 | @cpmpml | 2023-10-11 | It is great that the competition is not won by a Deberta pipeline. This would have been depressing to me! | [446240](https://www.kaggle.com/competitions/kaggle-llm-science-exam/discussion/446240) |
| 13 | @philippsinger | 2023-10-11 | Out of curiosity, ran our whole ensemble without any context, so completely voiding RAG: I am pleasently surpr | [446422](https://www.kaggle.com/competitions/kaggle-llm-science-exam/discussion/446422) |
| 12 | @philippsinger | 2023-10-11 | We finetuned all LLMs with LORA and classification head with certain types of poolings. Will try to elaborate  | [446240](https://www.kaggle.com/competitions/kaggle-llm-science-exam/discussion/446240) |
| 12 | @philippsinger | 2023-10-23 | We have now added a fully flexible way of training causal classification models in H2O LLM Studio: https://git | [446422](https://www.kaggle.com/competitions/kaggle-llm-science-exam/discussion/446422) |
| 10 | @philippsinger | 2023-10-11 | You can cache the context, the beauty of decoder only models for such use cases. | [446240](https://www.kaggle.com/competitions/kaggle-llm-science-exam/discussion/446240) |

## 关联资产

- 深读：`analysis/deep/kaggle-llm-science-exam.md`
- 结构化摘要：`notes/nlp/kaggle-llm-science-exam.md`
- 归档讨论区：`intel/kaggle-llm-science-exam/`（主题 2 条有 ≥50 票帖，图证 1 个）
