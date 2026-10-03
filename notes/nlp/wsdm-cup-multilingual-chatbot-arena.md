# WSDM Cup - Multilingual Chatbot Arena

> 主题：nlp ｜ 子类：— ｜ 领域：LLM 评测 ｜ 类别：Featured
> 截止：2025-XX-XX ｜ 队伍数：2000+ ｜ 机制：代码赛 ｜ 指标：偏好预测准确率/AUC
> 数据来源：`intel/wsdm-cup-multilingual-chatbot-arena/`（80 条主题索引 + 6 篇 write-up 正文）

## 1. 任务与数据

- 预测目标：给定用户提示与两个模型的回答，预测用户会**偏好哪一个**（多语言）。
- 数据形态：对话三元组（prompt / response_a / response_b）+ 人类偏好标签；多语言混合。
- 构造陷阱：
  - 序列长（多轮 + 双语），需要**截断策略**；
  - 偏好标签含主观噪声，且存在位置偏差（A/B 顺序）；
  - 推理成本高 → 需要高效微调与推理方案。

## 2. 方案谱系

| 方案 | 名次 | 关键点 |
| --- | --- | --- |
| 复用上一届的高效训练框架 + 奖励模型初始化 | 2nd | 基于他人在上一届比赛分享的高效训练/推理框架（有限 GPU 下做全参微调）；**prompt 与两个回答按长度比例从中间截断**；基座 gemma2-9b + ArmoRM-Llama3-8B，并用他人已训模型初始化 |
| 重实现 Eedi Rerank 训练管线 + 用 CausalLM 头加速推理 | 3rd | 关键工程点：**用 AutoModelForCausalLM 而非 AutoModelForSequenceClassification**，以便用 vLLM 高速推理；Qwen2.5-14B-Instruct（后预训练）+ Phi4 |
| 开放数据集贡献 | 社区 | 8.5k 条开放模型样本用于训练 |

## 3. 关键技巧

- **截断策略**：按长度比例截断 prompt/response 的**中部**（保留首尾）——长上下文任务的关键细节。
- **推理加速决定可行性**：改用 CausalLM 接口 + vLLM，使大模型推理成本可控。
- **奖励模型初始化**：用公开奖励模型（ArmoRM）初始化，比从零微调更省算力。
- **跨届复用**：直接采用上一届（同类赛）公开的训练框架。

## 4. 可迁移性评估

- **可直接迁移**：
  - **长文本截断要保留首尾**（中间截断）——对话/文档任务的通用经验；
  - 用 vLLM 等推理框架 + 合适的模型接口压低推理成本；
  - 用领域奖励模型初始化做二次微调；
  - 复用往届同类比赛的公开框架（成本最低的起点）。
- 需要前提：多 GPU 微调环境（或高效微调方案）。
- 不建议照搬：默认用 SequenceClassification 头（推理慢）。

## 5. 对新手的关键启示

1. **推理成本是这类比赛的隐形门槛**，工程选型直接决定能跑多大模型。
2. **截断策略值得单独调**（比例、位置：保留首尾优于一味截尾）。
3. **往届比赛的公开框架是最好的起点**。

## 6. 出处

- 讨论区索引：`intel/wsdm-cup-multilingual-chatbot-arena/topics.md`（80 条）
- 已收录 write-up（6 篇）：
  - 2nd（29 票）：https://www.kaggle.com/competitions/wsdm-cup-multilingual-chatbot-arena/discussion/567948
  - 3rd（52 票）：https://www.kaggle.com/competitions/wsdm-cup-multilingual-chatbot-arena/discussion/567584
  - 6th（28 票）：https://www.kaggle.com/competitions/wsdm-cup-multilingual-chatbot-arena/discussion/567600
  - 7th（32 票）：https://www.kaggle.com/competitions/wsdm-cup-multilingual-chatbot-arena/discussion/567589
  - 开放数据集（54 票）：https://www.kaggle.com/competitions/wsdm-cup-multilingual-chatbot-arena/discussion/552166
