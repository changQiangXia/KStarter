# LLM - Detect AI Generated Text

> `llm-detect-ai-generated-text` ｜ Featured ｜ 指标 Roc Auc Score ｜ 4358 队 ｜ 截止 2024-01-22

本页汇总该场 **4 条 ≥50 票 GM 主题帖**、**16 条断言**、**1 条高票评论**。

## GM 主题帖

| 票 | 选手 | 日期 | 主题 |
| --- | --- | --- | --- |
| 203 | [@conjuring92](https://www.kaggle.com/conjuring92) | 2024-01-23 | [1st place short solution summary [Updated with code link]](https://www.kaggle.com/competitions/llm-detect-ai-generated-text/discussion/470121) |
| 115 | [@wowfattie](https://www.kaggle.com/wowfattie) | 2024-01-24 | [2nd place solution with code and data](https://www.kaggle.com/competitions/llm-detect-ai-generated-text/discussion/470395) |
| 87 | [@asalhi](https://www.kaggle.com/asalhi) | 2024-01-23 | [[21th Solution] Secret Sauce [0.986 Public - Selected Private: 0.932 B](https://www.kaggle.com/competitions/llm-detect-ai-generated-text/discussion/470148) |
| 84 | [@jsday96](https://www.kaggle.com/jsday96) | 2024-01-23 | [5th place solution: 1.7 million training examples + domain adaptation](https://www.kaggle.com/competitions/llm-detect-ai-generated-text/discussion/470093) |

## 断言（条件→动作→机制→结果）

| 选手 | 等级 | 阶段 | 动作（节选） | 出处 |
| --- | --- | --- | --- | --- |
| @conjuring92 | A | 特征与数据工程 | datamix 约 160k 样本（约 40k 人类写作）：Persuade 全部 prompt + 大量通用文本 + 多 LLM/prompt/生成配置 + 公开数据集 | [llm-detect-ai-generated-text#470121-01](https://www.kaggle.com/competitions/llm-detect-ai-generated-text/discussion/470121) |
| @conjuring92 | A | 建模与训练 | 方案对照：Mistral-7B (Q)LoRA QKVO r=64 最佳；ghostbuster 变体（llama 7b + tiny llama 1.1B）；从零训练 deber | [llm-detect-ai-generated-text#470121-04](https://www.kaggle.com/competitions/llm-detect-ai-generated-text/discussion/470121) |
| @wowfattie | A | 建模与训练 | 先用 SlimPajama 造约 50 万 human/AI 对，deberta-v3-large 微调成通用人机分类器（0.916/0.967）；再在 Persuade 学生作文 | [llm-detect-ai-generated-text#470395-01](https://www.kaggle.com/competitions/llm-detect-ai-generated-text/discussion/470395) |
| @wowfattie | A | 特征与数据工程 | 用 llm-studio 对学生作文做 LM 微调，让 LLM 生成含引用与拼写错误的模仿学生写作文本，再用这些文本适配分类器 | [llm-detect-ai-generated-text#470395-02](https://www.kaggle.com/competitions/llm-detect-ai-generated-text/discussion/470395) |
| @asalhi | A | 特征与数据工程 | 用 LogisticRegression 预测 prompt_name，从 9000+ 测试文本里取重复次数最高的 Top N（N 等于唯一 prompt 数，已知为 5）→ 确知 | [llm-detect-ai-generated-text#470148-02](https://www.kaggle.com/competitions/llm-detect-ai-generated-text/discussion/470148) |
| @asalhi | A | 建模与训练 | 拼写纠错（Levenshtein）；BPE vocab 5000；TF-IDF 3 到 7 gram、min_df=2；MaxAbsScaler 加 Ridge 或 LinearS | [llm-detect-ai-generated-text#470148-03](https://www.kaggle.com/competitions/llm-detect-ai-generated-text/discussion/470148) |
| @asalhi | A | 建模与训练 | 对集成打分：最高 X 行当 AI、最低 Y 行当人类加入训练（首轮 X=Y=1000，重复 4 到 5 次、每轮加 200 或 250）；再用中位 50 行在 train 里找最近 | [llm-detect-ai-generated-text#470148-04](https://www.kaggle.com/competitions/llm-detect-ai-generated-text/discussion/470148) |
| @jsday96 | A | 数据工程 | 数据集：Pile completions（512k 对 512k）、SlimPajama（233k 对 233k）、Tricky Crawl（125k 人类）、Persuade（2 | [llm-detect-ai-generated-text#470093-01](https://www.kaggle.com/competitions/llm-detect-ai-generated-text/discussion/470093) |
| @jsday96 | A | 建模与训练 | teacher：1 个 DeBERTa 加 2 个 Mamba（1024 上下文）给测试打软标签（DeBERTa 90% 权重）；训两个短上下文学生（128 与 256 字符）模仿 | [llm-detect-ai-generated-text#470093-02](https://www.kaggle.com/competitions/llm-detect-ai-generated-text/discussion/470093) |
| @jsday96 | A | 特征与数据工程 | vLLM（2×3090 加 1×4090）生成；温度 0 到 2、top-k 在关闭、20、40 间随机、top-p 0.5 到 1、频率惩罚 0 到 0.5 随机；发现温度接近  | [llm-detect-ai-generated-text#470093-03](https://www.kaggle.com/competitions/llm-detect-ai-generated-text/discussion/470093) |
| @jsday96 | A | 建模与训练 | mamba-790m 速度与 DeBERTa-large 相当、显存更低；但取 last-token logits 受 padding 影响，改用最后一个非 pad token 可 | [llm-detect-ai-generated-text#470093-05](https://www.kaggle.com/competitions/llm-detect-ai-generated-text/discussion/470093) |
| @asalhi | B | 数据工程 | 合并 DAIGT V2、Mistral-7B texts、自产 Mistral、Gemini Pro 与比赛数据为 3 个集合：全部数据、仅 LLM 数据（label 1）、仅原始 | [llm-detect-ai-generated-text#470148-01](https://www.kaggle.com/competitions/llm-detect-ai-generated-text/discussion/470148) |
| @jsday96 | B | 特征与数据工程 | 增广：buggy spell check（Persuade 70%、其他 20%）、黑名单字符移除（同概率）、按 typo 库加错字、随机大小写翻转 | [llm-detect-ai-generated-text#470093-04](https://www.kaggle.com/competitions/llm-detect-ai-generated-text/discussion/470093) |
| @conjuring92 | C | 特征与数据工程 | 先在 Persuade 语料上 instruction tune LLM；再用 contrastive decoding 生成作文 | [llm-detect-ai-generated-text#470121-02](https://www.kaggle.com/competitions/llm-detect-ai-generated-text/discussion/470121) |
| @conjuring92 | C | 集成与融合 | 融合前把各模型预测转成 rank 再 blend | [llm-detect-ai-generated-text#470121-03](https://www.kaggle.com/competitions/llm-detect-ai-generated-text/discussion/470121) |
| @wowfattie | C | 复盘与流程 | 初期微调结果 CV 近完美但 public LB 低且不稳，遂放弃该路线转向通用预训练 | [llm-detect-ai-generated-text#470395-03](https://www.kaggle.com/competitions/llm-detect-ai-generated-text/discussion/470395) |

## 高票评论

| 票 | 选手 | 日期 | 摘录 | 出处 |
| --- | --- | --- | --- | --- |
| 13 | @conjuring92 | 2024-01-23 | During our evaluations, we found that our models consistently performed slightly better on private test prompt | [470121](https://www.kaggle.com/competitions/llm-detect-ai-generated-text/discussion/470121) |

## 关联资产

- 深读：`analysis/deep/llm-detect-ai-generated-text.md`
- 结构化摘要：`notes/nlp/llm-detect-ai-generated-text.md`
- 归档讨论区：`intel/llm-detect-ai-generated-text/`（主题 4 条有 ≥50 票帖，图证 0 个）
