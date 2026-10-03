# 文本 NLP：前 50 选手决策增量（P3）

> 来源：`people/claims/gm_claims.csv` 中该领域的 181 条断言，按受控标签聚合；每条断言可经 `scripts/people/verify_claims.py` 回链原文。
> 系统方法论见 `playbook/nlp.md`；本页只保留有跨人/跨队复现证据的决策项。

## 目标编码/类别特征（证据单位 24）

- **条件**：闭卷多选题；可检索 Wikipedia；单卡 GPU 内存有限  
- **动作**：Wikipedia 分块 + e5 公开 embedding + 自写 PyTorch 余弦相似度（分块放 GPU，不用 FAISS）；每题 5 个 chunk、max_length 1k；集成 7B 级 LLM（含 1 个 13B）；不同 wiki/分块/embedding 各喂一个 LLM 做 late fusion  
- **机制**：检索质量决定上限；实测 5 chunk/1k 最优；更大模型与 DeBERTa 集成均无增益  
- **结果**：private LB 0.930 提前 30 天达到并最终夺冠；200 样本 CV 0.99+ 被判定不可信  
- **证据**：[kaggle-llm-science-exam#446240-01](https://www.kaggle.com/competitions/kaggle-llm-science-exam/discussion/446240)（@philippsinger｜A）
- 其他案例：[@philippsinger](https://www.kaggle.com/competitions/kaggle-llm-science-exam/discussion/446240)、[@aerdem4](https://www.kaggle.com/competitions/learning-equality-curriculum-recommendations/discussion/394812)、[@wowfattie](https://www.kaggle.com/competitions/jigsaw-toxic-severity-rating/discussion/306274)、[@wowfattie](https://www.kaggle.com/competitions/jigsaw-toxic-severity-rating/discussion/306274)

## 验证设计（证据单位 22）

- **条件**：多语言检索匹配；内容作类别、topic 多标签；有高质量预训练编码器  
- **动作**：content 作类别训练 ArcFace，topic 目标向量 l1 归一化；margin 0.1 到 0.5 线性退火 22 epochs，首尾各 2 epoch 显著降 LR；类别中心用预训练模型抽取的 content 向量初始化；多模型 l2 归一化后拼接  
- **机制**：类别中心预热加 margin 退火让度量学习稳定收敛；拼接保留多语言模型互补信息  
- **结果**：validation 0.764、public LB 0.727、private LB 0.764（private 与 validation 相等）；效率版 MiniLM private 0.740、CPU 约 20 分钟  
- **证据**：[learning-equality-curriculum-recommendations#394812-01](https://www.kaggle.com/competitions/learning-equality-curriculum-recommendations/discussion/394812)（@aerdem4｜A）
- 其他案例：[@philippsinger](https://www.kaggle.com/competitions/kaggle-llm-science-exam/discussion/446240)、[@cdeotte](https://www.kaggle.com/competitions/feedback-prize-2021/discussion/295794)、[@cdeotte](https://www.kaggle.com/competitions/feedback-prize-2021/discussion/295794)、[@wowfattie](https://www.kaggle.com/competitions/jigsaw-toxic-severity-rating/discussion/306274)

## 提交/推理工程（证据单位 21）

- **条件**：10 个模型各取 3/10 folds，推理时限 8.5 小时  
- **动作**：去掉 3 个 fold 后共推理 27 个模型；同模型 folds 先平均再进 WBF  
- **机制**：时限内保留尽量多模型；折内平均减少 WBF 输入数量  
- **结果**：单模平均 CV 约 700；WBF 集成 CV 741 / Public 727 / Private 740  
- **证据**：[feedback-prize-2021#313389-02](https://www.kaggle.com/competitions/feedback-prize-2021/discussion/313389)（@cdeotte｜A）
- 其他案例：[@wowfattie](https://www.kaggle.com/competitions/jigsaw-toxic-severity-rating/discussion/306274)、[@cdeotte](https://www.kaggle.com/competitions/lmsys-chatbot-arena/discussion/527596)、[@cdeotte](https://www.kaggle.com/competitions/feedback-prize-2021/discussion/313389)、[@sayoulala](https://www.kaggle.com/competitions/lmsys-chatbot-arena/discussion/527629)

## 损失设计（证据单位 21）

- **条件**：多语言检索匹配；内容作类别、topic 多标签；有高质量预训练编码器  
- **动作**：content 作类别训练 ArcFace，topic 目标向量 l1 归一化；margin 0.1 到 0.5 线性退火 22 epochs，首尾各 2 epoch 显著降 LR；类别中心用预训练模型抽取的 content 向量初始化；多模型 l2 归一化后拼接  
- **机制**：类别中心预热加 margin 退火让度量学习稳定收敛；拼接保留多语言模型互补信息  
- **结果**：validation 0.764、public LB 0.727、private LB 0.764（private 与 validation 相等）；效率版 MiniLM private 0.740、CPU 约 20 分钟  
- **证据**：[learning-equality-curriculum-recommendations#394812-01](https://www.kaggle.com/competitions/learning-equality-curriculum-recommendations/discussion/394812)（@aerdem4｜A）
- 其他案例：[@cdeotte](https://www.kaggle.com/competitions/learning-agency-lab-automated-essay-scoring-2/discussion/497832)、[@cdeotte](https://www.kaggle.com/competitions/lmsys-chatbot-arena/discussion/527596)、[@cdeotte](https://www.kaggle.com/competitions/feedback-prize-2021/discussion/313389)、[@cdeotte](https://www.kaggle.com/competitions/feedback-prize-2021/discussion/313389)

## 集成/融合（证据单位 20）

- **条件**：NER/span 任务多模型集成；不同模型的 span 边界不同  
- **动作**：用 WBF 对 span 起点与终点分别平均：8-11 与 10-13 合成 9-12；token 概率平均会取并集或交集，BIO 平均会产生两个 B  
- **机制**：按几何位置合并而非按 token 概率合并，得到介于并集与交集之间的合理 span  
- **结果**：示例 8-11 与 10-13 合成 9-12  
- **证据**：[feedback-prize-2021#313389-01](https://www.kaggle.com/competitions/feedback-prize-2021/discussion/313389)（@cdeotte｜A）
- 其他案例：[@wowfattie](https://www.kaggle.com/competitions/jigsaw-toxic-severity-rating/discussion/306274)、[@wowfattie](https://www.kaggle.com/competitions/jigsaw-toxic-severity-rating/discussion/306274)、[@cdeotte](https://www.kaggle.com/competitions/lmsys-chatbot-arena/discussion/527596)、[@cdeotte](https://www.kaggle.com/competitions/lmsys-chatbot-arena/discussion/527596)

## 预训练/域适应（证据单位 17）

- **条件**：多语言检索匹配；内容作类别、topic 多标签；有高质量预训练编码器  
- **动作**：content 作类别训练 ArcFace，topic 目标向量 l1 归一化；margin 0.1 到 0.5 线性退火 22 epochs，首尾各 2 epoch 显著降 LR；类别中心用预训练模型抽取的 content 向量初始化；多模型 l2 归一化后拼接  
- **机制**：类别中心预热加 margin 退火让度量学习稳定收敛；拼接保留多语言模型互补信息  
- **结果**：validation 0.764、public LB 0.727、private LB 0.764（private 与 validation 相等）；效率版 MiniLM private 0.740、CPU 约 20 分钟  
- **证据**：[learning-equality-curriculum-recommendations#394812-01](https://www.kaggle.com/competitions/learning-equality-curriculum-recommendations/discussion/394812)（@aerdem4｜A）
- 其他案例：[@cdeotte](https://www.kaggle.com/competitions/lmsys-chatbot-arena/discussion/527596)、[@sayoulala](https://www.kaggle.com/competitions/lmsys-chatbot-arena/discussion/527629)、[@sayoulala](https://www.kaggle.com/competitions/lmsys-chatbot-arena/discussion/527629)、[@cdeotte](https://www.kaggle.com/competitions/feedback-prize-english-language-learning/discussion/351577)

## 合成/生成数据（证据单位 16）

- **条件**：NER/span 任务多模型集成；不同模型的 span 边界不同  
- **动作**：用 WBF 对 span 起点与终点分别平均：8-11 与 10-13 合成 9-12；token 概率平均会取并集或交集，BIO 平均会产生两个 B  
- **机制**：按几何位置合并而非按 token 概率合并，得到介于并集与交集之间的合理 span  
- **结果**：示例 8-11 与 10-13 合成 9-12  
- **证据**：[feedback-prize-2021#313389-01](https://www.kaggle.com/competitions/feedback-prize-2021/discussion/313389)（@cdeotte｜A）
- 其他案例：[@sayoulala](https://www.kaggle.com/competitions/lmsys-chatbot-arena/discussion/527629)、[@tascj0](https://www.kaggle.com/competitions/feedback-prize-2021/discussion/313424)、[@darraghdog](https://www.kaggle.com/competitions/ai-mathematical-olympiad-progress-prize-2/discussion/574765)、[@darraghdog](https://www.kaggle.com/competitions/ai-mathematical-olympiad-progress-prize-2/discussion/574765)

## Agent/LLM 工具（证据单位 14）

- **条件**：AI 文本检测；需要覆盖多生成器与多 prompt 的多样性  
- **动作**：datamix 约 160k 样本（约 40k 人类写作）：Persuade 全部 prompt + 大量通用文本 + 多 LLM/prompt/生成配置 + 公开数据集  
- **机制**：生成器与语料多样性决定检测模型泛化  
- **结果**：约 160k 样本，其中约 40k 人类写作  
- **证据**：[llm-detect-ai-generated-text#470121-01](https://www.kaggle.com/competitions/llm-detect-ai-generated-text/discussion/470121)（@conjuring92｜A）
- 其他案例：[@darraghdog](https://www.kaggle.com/competitions/ai-mathematical-olympiad-progress-prize-2/discussion/574765)、[@wowfattie](https://www.kaggle.com/competitions/llm-detect-ai-generated-text/discussion/470395)、[@philippsinger](https://www.kaggle.com/competitions/llm-prompt-recovery/discussion/494497)、[@philippsinger](https://www.kaggle.com/competitions/llm-prompt-recovery/discussion/494497)

## 数据清洗/去噪（证据单位 14）

- **条件**：token 级交叉熵训练会产生断裂 span  
- **动作**：规则后处理：修复断裂 span、discourse 上限（Lead/Position/Concluding 各最多一个）、按预测长度调整边界（小于 45 词的 Evidence 起点前移 9 词）  
- **机制**：利用评测只要求 50% overlap 的规则空间修正边界  
- **结果**：后处理整体提升 CV 约 .008（原文写作 ~.008）  
- **证据**：[feedback-prize-2021#313389-03](https://www.kaggle.com/competitions/feedback-prize-2021/discussion/313389)（@cdeotte｜A）
- 其他案例：[@philippsinger](https://www.kaggle.com/competitions/kaggle-llm-science-exam/discussion/446240)、[@cdeotte](https://www.kaggle.com/competitions/lmsys-chatbot-arena/discussion/527596)、[@tascj0](https://www.kaggle.com/competitions/map-charting-student-math-misunderstandings/discussion/612268)、[@tascj0](https://www.kaggle.com/competitions/map-charting-student-math-misunderstandings/discussion/612268)

## 后处理/校准（证据单位 13）

- **条件**：token 级交叉熵训练会产生断裂 span  
- **动作**：规则后处理：修复断裂 span、discourse 上限（Lead/Position/Concluding 各最多一个）、按预测长度调整边界（小于 45 词的 Evidence 起点前移 9 词）  
- **机制**：利用评测只要求 50% overlap 的规则空间修正边界  
- **结果**：后处理整体提升 CV 约 .008（原文写作 ~.008）  
- **证据**：[feedback-prize-2021#313389-03](https://www.kaggle.com/competitions/feedback-prize-2021/discussion/313389)（@cdeotte｜A）
- 其他案例：[@tascj0](https://www.kaggle.com/competitions/feedback-prize-2021/discussion/313424)、[@darraghdog](https://www.kaggle.com/competitions/ai-mathematical-olympiad-progress-prize-2/discussion/574765)、[@conjuring92](https://www.kaggle.com/competitions/eedi-mining-misconceptions-in-mathematics/discussion/551402)、[@cdeotte](https://www.kaggle.com/competitions/feedback-prize-english-language-learning/discussion/369609)

## 检索/RAG（证据单位 11）

- **条件**：闭卷多选题；可检索 Wikipedia；单卡 GPU 内存有限  
- **动作**：Wikipedia 分块 + e5 公开 embedding + 自写 PyTorch 余弦相似度（分块放 GPU，不用 FAISS）；每题 5 个 chunk、max_length 1k；集成 7B 级 LLM（含 1 个 13B）；不同 wiki/分块/embedding 各喂一个 LLM 做 late fusion  
- **机制**：检索质量决定上限；实测 5 chunk/1k 最优；更大模型与 DeBERTa 集成均无增益  
- **结果**：private LB 0.930 提前 30 天达到并最终夺冠；200 样本 CV 0.99+ 被判定不可信  
- **证据**：[kaggle-llm-science-exam#446240-01](https://www.kaggle.com/competitions/kaggle-llm-science-exam/discussion/446240)（@philippsinger｜A）
- 其他案例：[@aerdem4](https://www.kaggle.com/competitions/learning-equality-curriculum-recommendations/discussion/394812)、[@conjuring92](https://www.kaggle.com/competitions/eedi-mining-misconceptions-in-mathematics/discussion/551402)、[@conjuring92](https://www.kaggle.com/competitions/eedi-mining-misconceptions-in-mathematics/discussion/551402)、[@philippsinger](https://www.kaggle.com/competitions/llm-prompt-recovery/discussion/494497)

## 集成权重选择（证据单位 11）

- **条件**：NER/span 任务多模型集成；不同模型的 span 边界不同  
- **动作**：用 WBF 对 span 起点与终点分别平均：8-11 与 10-13 合成 9-12；token 概率平均会取并集或交集，BIO 平均会产生两个 B  
- **机制**：按几何位置合并而非按 token 概率合并，得到介于并集与交集之间的合理 span  
- **结果**：示例 8-11 与 10-13 合成 9-12  
- **证据**：[feedback-prize-2021#313389-01](https://www.kaggle.com/competitions/feedback-prize-2021/discussion/313389)（@cdeotte｜A）
- 其他案例：[@wowfattie](https://www.kaggle.com/competitions/jigsaw-toxic-severity-rating/discussion/306274)、[@cdeotte](https://www.kaggle.com/competitions/lmsys-chatbot-arena/discussion/527596)、[@cdeotte](https://www.kaggle.com/competitions/feedback-prize-2021/discussion/313389)、[@sayoulala](https://www.kaggle.com/competitions/lmsys-chatbot-arena/discussion/527629)

## 伪标签/自训练（证据单位 11）

- **条件**：需要多个异构检测器并选择最优  
- **动作**：方案对照：Mistral-7B (Q)LoRA QKVO r=64 最佳；ghostbuster 变体（llama 7b + tiny llama 1.1B）；从零训练 deberta-v3-small（自定义词表 + MLM + 伪标签）；deberta-v3-large ranking loss；mistral 置信弱标注  
- **机制**：生成模型、判别模型与统计特征三类先验互补  
- **结果**：private/public：mistral 0.984/0.966；ghostbuster 变体 0.974/0.957；从零 deberta 0.943/0.942；deberta-large ranking 0.963/0.961；弱标注变体 0.971/0.957  
- **证据**：[llm-detect-ai-generated-text#470121-04](https://www.kaggle.com/competitions/llm-detect-ai-generated-text/discussion/470121)（@conjuring92｜A）
- 其他案例：[@cpmpml](https://www.kaggle.com/competitions/nbme-score-clinical-patient-notes/discussion/323085)、[@conjuring92](https://www.kaggle.com/competitions/eedi-mining-misconceptions-in-mathematics/discussion/551402)、[@cdeotte](https://www.kaggle.com/competitions/feedback-prize-english-language-learning/discussion/369609)、[@cdeotte](https://www.kaggle.com/competitions/feedback-prize-english-language-learning/discussion/369609)

## 类别不平衡（证据单位 11）

- **条件**：需要把 5 折模型合成一个可提交模型并满足推理时限  
- **动作**：5 折 LoRA 权重直接平均；GPTQ 量化 8bit；提交时 TTA（length 2000）  
- **机制**：同源微调权重可线性平均（LoRA 合并）；量化满足时限  
- **结果**：merge 加 8bit LB 0.882（TTA 0.876）  
- **证据**：[lmsys-chatbot-arena#527629-02](https://www.kaggle.com/competitions/lmsys-chatbot-arena/discussion/527629)（@sayoulala｜A）
- 其他案例：[@cdeotte](https://www.kaggle.com/competitions/lmsys-chatbot-arena/discussion/527596)、[@cdeotte](https://www.kaggle.com/competitions/feedback-prize-2021/discussion/313389)、[@cpmpml](https://www.kaggle.com/competitions/nbme-score-clinical-patient-notes/discussion/323085)、[@cdeotte](https://www.kaggle.com/competitions/feedback-prize-english-language-learning/discussion/369609)

## 泄漏检测/探针（证据单位 10）

- **条件**：token 级交叉熵训练会产生断裂 span  
- **动作**：规则后处理：修复断裂 span、discourse 上限（Lead/Position/Concluding 各最多一个）、按预测长度调整边界（小于 45 词的 Evidence 起点前移 9 词）  
- **机制**：利用评测只要求 50% overlap 的规则空间修正边界  
- **结果**：后处理整体提升 CV 约 .008（原文写作 ~.008）  
- **证据**：[feedback-prize-2021#313389-03](https://www.kaggle.com/competitions/feedback-prize-2021/discussion/313389)（@cdeotte｜A）
- 其他案例：[@wowfattie](https://www.kaggle.com/competitions/jigsaw-toxic-severity-rating/discussion/306274)、[@cdeotte](https://www.kaggle.com/competitions/learning-agency-lab-automated-essay-scoring-2/discussion/496906)、[@cdeotte](https://www.kaggle.com/competitions/learning-agency-lab-automated-essay-scoring-2/discussion/496906)、[@cdeotte](https://www.kaggle.com/competitions/feedback-prize-english-language-learning/discussion/369609)

## 长序列/上下文（证据单位 10）

- **条件**：闭卷多选题；可检索 Wikipedia；单卡 GPU 内存有限  
- **动作**：Wikipedia 分块 + e5 公开 embedding + 自写 PyTorch 余弦相似度（分块放 GPU，不用 FAISS）；每题 5 个 chunk、max_length 1k；集成 7B 级 LLM（含 1 个 13B）；不同 wiki/分块/embedding 各喂一个 LLM 做 late fusion  
- **机制**：检索质量决定上限；实测 5 chunk/1k 最优；更大模型与 DeBERTa 集成均无增益  
- **结果**：private LB 0.930 提前 30 天达到并最终夺冠；200 样本 CV 0.99+ 被判定不可信  
- **证据**：[kaggle-llm-science-exam#446240-01](https://www.kaggle.com/competitions/kaggle-llm-science-exam/discussion/446240)（@philippsinger｜A）
- 其他案例：[@cdeotte](https://www.kaggle.com/competitions/feedback-prize-2021/discussion/295794)、[@cdeotte](https://www.kaggle.com/competitions/learning-agency-lab-automated-essay-scoring-2/discussion/497832)、[@cdeotte](https://www.kaggle.com/competitions/learning-agency-lab-automated-essay-scoring-2/discussion/497832)、[@cdeotte](https://www.kaggle.com/competitions/lmsys-chatbot-arena/discussion/527596)

## CNN/视觉架构（证据单位 9）

- **条件**：长文本 token 分类需要超过 512 的输入长度  
- **动作**：多 backbone 支持长序列：DeBERTa 任意长度、Funnel 改 config 到 1536、BigBird 用 original_full、YOSO 关 lsh_backward；全部 1536 训练与推理（BigBird-base 1024）  
- **机制**：不同架构对长序列的适配方式不同，统一长度便于横向比较  
- **结果**：全部模型 1536 训练与推理；BigBird-base 1024  
- **证据**：[feedback-prize-2021#313389-04](https://www.kaggle.com/competitions/feedback-prize-2021/discussion/313389)（@cdeotte｜A）
- 其他案例：[@cdeotte](https://www.kaggle.com/competitions/feedback-prize-2021/discussion/295794)、[@cdeotte](https://www.kaggle.com/competitions/feedback-prize-2021/discussion/295794)、[@cdeotte](https://www.kaggle.com/competitions/lmsys-chatbot-arena/discussion/527596)、[@cpmpml](https://www.kaggle.com/competitions/nbme-score-clinical-patient-notes/discussion/323085)

## 学习率调度（证据单位 9）

- **条件**：推理约束限制大模型部署，需要小模型达到接近大模型水平  
- **动作**：先用 ut 数据对 3 个模型 post-pretrain 1 epoch（lr=1e-5）；5 折训练 llama3-70b 与 qwen2-72b；再把大模型 logits 蒸馏进 gemma2-9b（lr=5e-5，多损失）  
- **机制**：大模型 logits 提供软监督，小模型继承其排序能力  
- **结果**：蒸馏后的 gemma 9b 5 折 CV 在 0.862 到 0.876 之间  
- **证据**：[lmsys-chatbot-arena#527629-01](https://www.kaggle.com/competitions/lmsys-chatbot-arena/discussion/527629)（@sayoulala｜A）
- 其他案例：[@cdeotte](https://www.kaggle.com/competitions/learning-agency-lab-automated-essay-scoring-2/discussion/497832)、[@tascj0](https://www.kaggle.com/competitions/map-charting-student-math-misunderstandings/discussion/612268)、[@philippsinger](https://www.kaggle.com/competitions/llm-prompt-recovery/discussion/494497)、[@jsday96](https://www.kaggle.com/competitions/llm-detect-ai-generated-text/discussion/470093)

## 知识蒸馏（证据单位 8）

- **条件**：推理约束限制大模型部署，需要小模型达到接近大模型水平  
- **动作**：先用 ut 数据对 3 个模型 post-pretrain 1 epoch（lr=1e-5）；5 折训练 llama3-70b 与 qwen2-72b；再把大模型 logits 蒸馏进 gemma2-9b（lr=5e-5，多损失）  
- **机制**：大模型 logits 提供软监督，小模型继承其排序能力  
- **结果**：蒸馏后的 gemma 9b 5 折 CV 在 0.862 到 0.876 之间  
- **证据**：[lmsys-chatbot-arena#527629-01](https://www.kaggle.com/competitions/lmsys-chatbot-arena/discussion/527629)（@sayoulala｜A）
- 其他案例：[@sayoulala](https://www.kaggle.com/competitions/lmsys-chatbot-arena/discussion/527629)、[@tascj0](https://www.kaggle.com/competitions/lmsys-chatbot-arena/discussion/527685)、[@asalhi](https://www.kaggle.com/competitions/llm-detect-ai-generated-text/discussion/470148)、[@jsday96](https://www.kaggle.com/competitions/llm-detect-ai-generated-text/discussion/470093)

## dtype/内存优化（证据单位 7）

- **条件**：闭卷多选题；可检索 Wikipedia；单卡 GPU 内存有限  
- **动作**：Wikipedia 分块 + e5 公开 embedding + 自写 PyTorch 余弦相似度（分块放 GPU，不用 FAISS）；每题 5 个 chunk、max_length 1k；集成 7B 级 LLM（含 1 个 13B）；不同 wiki/分块/embedding 各喂一个 LLM 做 late fusion  
- **机制**：检索质量决定上限；实测 5 chunk/1k 最优；更大模型与 DeBERTa 集成均无增益  
- **结果**：private LB 0.930 提前 30 天达到并最终夺冠；200 样本 CV 0.99+ 被判定不可信  
- **证据**：[kaggle-llm-science-exam#446240-01](https://www.kaggle.com/competitions/kaggle-llm-science-exam/discussion/446240)（@philippsinger｜A）
- 其他案例：[@cdeotte](https://www.kaggle.com/competitions/learning-agency-lab-automated-essay-scoring-2/discussion/497832)、[@cdeotte](https://www.kaggle.com/competitions/lmsys-chatbot-arena/discussion/527596)、[@cdeotte](https://www.kaggle.com/competitions/lmsys-chatbot-arena/discussion/527596)、[@tascj0](https://www.kaggle.com/competitions/map-charting-student-math-misunderstandings/discussion/612268)

## 规模/Scaling（证据单位 7）

- **条件**：闭卷多选题；可检索 Wikipedia；单卡 GPU 内存有限  
- **动作**：Wikipedia 分块 + e5 公开 embedding + 自写 PyTorch 余弦相似度（分块放 GPU，不用 FAISS）；每题 5 个 chunk、max_length 1k；集成 7B 级 LLM（含 1 个 13B）；不同 wiki/分块/embedding 各喂一个 LLM 做 late fusion  
- **机制**：检索质量决定上限；实测 5 chunk/1k 最优；更大模型与 DeBERTa 集成均无增益  
- **结果**：private LB 0.930 提前 30 天达到并最终夺冠；200 样本 CV 0.99+ 被判定不可信  
- **证据**：[kaggle-llm-science-exam#446240-01](https://www.kaggle.com/competitions/kaggle-llm-science-exam/discussion/446240)（@philippsinger｜A）
- 其他案例：[@cdeotte](https://www.kaggle.com/competitions/lmsys-chatbot-arena/discussion/527596)、[@tascj0](https://www.kaggle.com/competitions/map-charting-student-math-misunderstandings/discussion/612268)、[@cnumber](https://www.kaggle.com/competitions/llm-20-questions/discussion/531106)、[@jsday96](https://www.kaggle.com/competitions/llm-detect-ai-generated-text/discussion/470093)

## 信号/频谱处理（证据单位 7）

- **条件**：标签噪声（主要是 Neither 类）导致验证波动大  
- **动作**：先用 3 seeds 集成稳住验证（5 折 x 5 seeds 实验），再用最难 fold 加 3 runs 做后续实验；最终用 32B/GLM 全量数据 3 seeds  
- **机制**：多种子平均降低方差；multi-seed 集成优于 multi-fold  
- **结果**：原文：单 seed 不可信、3 seeds 稳定、multi-seed 明显优于 multi-fold  
- **证据**：[map-charting-student-math-misunderstandings#612268-03](https://www.kaggle.com/competitions/map-charting-student-math-misunderstandings/discussion/612268)（@tascj0｜A）
- 其他案例：[@darraghdog](https://www.kaggle.com/competitions/ai-mathematical-olympiad-progress-prize-2/discussion/574765)、[@darraghdog](https://www.kaggle.com/competitions/ai-mathematical-olympiad-progress-prize-2/discussion/574765)、[@takoihiraokazu](https://www.kaggle.com/competitions/foursquare-location-matching/discussion/336055)、[@ferdinandlimburg](https://www.kaggle.com/competitions/learning-agency-lab-automated-essay-scoring-2/discussion/516791)

## 混合精度/量化（证据单位 7）

- **条件**：需要把 5 折模型合成一个可提交模型并满足推理时限  
- **动作**：5 折 LoRA 权重直接平均；GPTQ 量化 8bit；提交时 TTA（length 2000）  
- **机制**：同源微调权重可线性平均（LoRA 合并）；量化满足时限  
- **结果**：merge 加 8bit LB 0.882（TTA 0.876）  
- **证据**：[lmsys-chatbot-arena#527629-02](https://www.kaggle.com/competitions/lmsys-chatbot-arena/discussion/527629)（@sayoulala｜A）
- 其他案例：[@tascj0](https://www.kaggle.com/competitions/map-charting-student-math-misunderstandings/discussion/612268)、[@darraghdog](https://www.kaggle.com/competitions/ai-mathematical-olympiad-progress-prize-2/discussion/574765)、[@tascj0](https://www.kaggle.com/competitions/learning-agency-lab-automated-essay-scoring-2/discussion/516639)、[@cdeotte](https://www.kaggle.com/competitions/kaggle-llm-science-exam/discussion/446318)

## 度量学习/ArcFace（证据单位 6）

- **条件**：闭卷多选题；可检索 Wikipedia；单卡 GPU 内存有限  
- **动作**：Wikipedia 分块 + e5 公开 embedding + 自写 PyTorch 余弦相似度（分块放 GPU，不用 FAISS）；每题 5 个 chunk、max_length 1k；集成 7B 级 LLM（含 1 个 13B）；不同 wiki/分块/embedding 各喂一个 LLM 做 late fusion  
- **机制**：检索质量决定上限；实测 5 chunk/1k 最优；更大模型与 DeBERTa 集成均无增益  
- **结果**：private LB 0.930 提前 30 天达到并最终夺冠；200 样本 CV 0.99+ 被判定不可信  
- **证据**：[kaggle-llm-science-exam#446240-01](https://www.kaggle.com/competitions/kaggle-llm-science-exam/discussion/446240)（@philippsinger｜A）
- 其他案例：[@cdeotte](https://www.kaggle.com/competitions/feedback-prize-english-language-learning/discussion/351577)、[@cdeotte](https://www.kaggle.com/competitions/feedback-prize-english-language-learning/discussion/351577)、[@cdeotte](https://www.kaggle.com/competitions/feedback-prize-english-language-learning/discussion/369609)、[@philippsinger](https://www.kaggle.com/competitions/llm-prompt-recovery/discussion/494497)

## 数据增广（证据单位 6）

- **条件**：response A 与 B 的顺序会引入偏置  
- **动作**：把原样本与其 swap 一起训，且两者梯度必须在同一个 optimizer.step 内累积；训练时间翻倍但 gemma2-9b 稳定加 0.003；再加 PAB 与 PAPB 双格式加 0.001  
- **机制**：同一 step 内累积保证等价于对称样本，避免顺序偏置；对称数据正则化模型  
- **结果**：稳定加 0.003；格式增广加 0.001  
- **证据**：[lmsys-chatbot-arena#527685-03](https://www.kaggle.com/competitions/lmsys-chatbot-arena/discussion/527685)（@tascj0｜A）
- 其他案例：[@jsday96](https://www.kaggle.com/competitions/llm-detect-ai-generated-text/discussion/470093)、[@darraghdog](https://www.kaggle.com/competitions/linking-writing-processes-to-writing-quality/discussion/466906)、[@conjuring92](https://www.kaggle.com/competitions/feedback-prize-effectiveness/discussion/347433)、[@conjuring92](https://www.kaggle.com/competitions/feedback-prize-effectiveness/discussion/347433)

## 分组聚合特征（证据单位 6）

- **条件**：需要多个异构检测器并选择最优  
- **动作**：方案对照：Mistral-7B (Q)LoRA QKVO r=64 最佳；ghostbuster 变体（llama 7b + tiny llama 1.1B）；从零训练 deberta-v3-small（自定义词表 + MLM + 伪标签）；deberta-v3-large ranking loss；mistral 置信弱标注  
- **机制**：生成模型、判别模型与统计特征三类先验互补  
- **结果**：private/public：mistral 0.984/0.966；ghostbuster 变体 0.974/0.957；从零 deberta 0.943/0.942；deberta-large ranking 0.963/0.961；弱标注变体 0.971/0.957  
- **证据**：[llm-detect-ai-generated-text#470121-04](https://www.kaggle.com/competitions/llm-detect-ai-generated-text/discussion/470121)（@conjuring92｜A）
- 其他案例：[@tascj0](https://www.kaggle.com/competitions/feedback-prize-2021/discussion/313424)、[@conjuring92](https://www.kaggle.com/competitions/eedi-mining-misconceptions-in-mathematics/discussion/551402)、[@tascj0](https://www.kaggle.com/competitions/lmsys-chatbot-arena/discussion/527685)、[@ebinan92](https://www.kaggle.com/competitions/eedi-mining-misconceptions-in-mathematics/discussion/551391)

## Transformer/注意力（证据单位 5）

- **条件**：需要更多 TTA 又要控制时间  
- **动作**：Choice Permute TTA：随机排列选项后 sentence transformer 得到不同 context，两套 logits 集成有增益；Drop 2 Wrong Choice：先推理几轮确定 2 个错项，只推理 top3 选项（5/3=1.6x 提速，未用选项 logit 设为第 3 项），总提速 7x  
- **机制**：用已验证的预测裁剪推理空间，换更多 TTA 预算  
- **结果**：1.6x 提速；总 7x  
- **证据**：[kaggle-llm-science-exam#446318-04](https://www.kaggle.com/competitions/kaggle-llm-science-exam/discussion/446318)（@cdeotte｜A）
- 其他案例：[@cdeotte](https://www.kaggle.com/competitions/learning-agency-lab-automated-essay-scoring-2/discussion/497832)、[@cdeotte](https://www.kaggle.com/competitions/feedback-prize-english-language-learning/discussion/351577)、[@hydantess](https://www.kaggle.com/competitions/AI4Code/discussion/360501)

## 线性/简单模型（证据单位 5）

- **条件**：多语言检索匹配；内容作类别、topic 多标签；有高质量预训练编码器  
- **动作**：content 作类别训练 ArcFace，topic 目标向量 l1 归一化；margin 0.1 到 0.5 线性退火 22 epochs，首尾各 2 epoch 显著降 LR；类别中心用预训练模型抽取的 content 向量初始化；多模型 l2 归一化后拼接  
- **机制**：类别中心预热加 margin 退火让度量学习稳定收敛；拼接保留多语言模型互补信息  
- **结果**：validation 0.764、public LB 0.727、private LB 0.764（private 与 validation 相等）；效率版 MiniLM private 0.740、CPU 约 20 分钟  
- **证据**：[learning-equality-curriculum-recommendations#394812-01](https://www.kaggle.com/competitions/learning-equality-curriculum-recommendations/discussion/394812)（@aerdem4｜A）
- 其他案例：[@darraghdog](https://www.kaggle.com/competitions/ai-mathematical-olympiad-progress-prize-2/discussion/574765)、[@conjuring92](https://www.kaggle.com/competitions/eedi-mining-misconceptions-in-mathematics/discussion/551402)、[@cdeotte](https://www.kaggle.com/competitions/kaggle-llm-science-exam/discussion/446318)、[@takoihiraokazu](https://www.kaggle.com/competitions/commonlit-evaluate-student-summaries/discussion/446539)

## 多种子平均（证据单位 4）

- **条件**：标签噪声（主要是 Neither 类）导致验证波动大  
- **动作**：先用 3 seeds 集成稳住验证（5 折 x 5 seeds 实验），再用最难 fold 加 3 runs 做后续实验；最终用 32B/GLM 全量数据 3 seeds  
- **机制**：多种子平均降低方差；multi-seed 集成优于 multi-fold  
- **结果**：原文：单 seed 不可信、3 seeds 稳定、multi-seed 明显优于 multi-fold  
- **证据**：[map-charting-student-math-misunderstandings#612268-03](https://www.kaggle.com/competitions/map-charting-student-math-misunderstandings/discussion/612268)（@tascj0｜A）
- 其他案例：[@tascj0](https://www.kaggle.com/competitions/learning-agency-lab-automated-essay-scoring-2/discussion/516639)、[@ferdinandlimburg](https://www.kaggle.com/competitions/learning-agency-lab-automated-essay-scoring-2/discussion/516791)、[@ferdinandlimburg](https://www.kaggle.com/competitions/learning-agency-lab-automated-essay-scoring-2/discussion/516791)、[@ferdinandlimburg](https://www.kaggle.com/competitions/learning-agency-lab-automated-essay-scoring-2/discussion/516791)

## 外部数据（证据单位 4）

- **条件**：train 含 12,875 条 persuade 与 4,432 条 non-persuade  
- **动作**：加数据源 tag（如 [A]/[B] 前缀）、加数据源分类头、部分模型按数据源分别用分类头、按 non-persuade 分数早停；作者假设两源分数采集方式不同，混合训练损害拟合  
- **机制**：显式区分数据源，避免模型把两套评分机制混在一起  
- **结果**：12,875 persuade；4,432 non-persuade  
- **证据**：[learning-agency-lab-automated-essay-scoring-2#516639-01](https://www.kaggle.com/competitions/learning-agency-lab-automated-essay-scoring-2/discussion/516639)（@tascj0｜A）
- 其他案例：[@tascj0](https://www.kaggle.com/competitions/learning-agency-lab-automated-essay-scoring-2/discussion/516639)、[@tascj0](https://www.kaggle.com/competitions/learning-agency-lab-automated-essay-scoring-2/discussion/516639)、[@darraghdog](https://www.kaggle.com/competitions/linking-writing-processes-to-writing-quality/discussion/466906)、[@conjuring92](https://www.kaggle.com/competitions/feedback-prize-effectiveness/discussion/347433)

## 时间/分组切分（证据单位 4）

- **条件**：测试文本使用了哪些 prompt 未知  
- **动作**：用 LogisticRegression 预测 prompt_name，从 9000+ 测试文本里取重复次数最高的 Top N（N 等于唯一 prompt 数，已知为 5）→ 确知测试 prompt，再只从 Train 中挑对应文本训练；LLM 数据与老数据保持通用  
- **机制**：用测试集本身推断题源，避免训练分布与测试错配  
- **结果**：N=5；9000+ 测试文本  
- **证据**：[llm-detect-ai-generated-text#470148-02](https://www.kaggle.com/competitions/llm-detect-ai-generated-text/discussion/470148)（@asalhi｜A）
- 其他案例：[@tascj0](https://www.kaggle.com/competitions/lmsys-chatbot-arena/discussion/527685)、[@ferdinandlimburg](https://www.kaggle.com/competitions/learning-agency-lab-automated-essay-scoring-2/discussion/516791)、[@takoihiraokazu](https://www.kaggle.com/competitions/commonlit-evaluate-student-summaries/discussion/446539)

## 优化器（证据单位 3）

- **条件**：t5 指标对均值 prompt 极敏感；手工调 prompt 低效  
- **动作**：对约 32k 个 t5 token 暴力搜索最优均值 prompt；发现 TensorFlow 原版 SentencePiece 有特殊 token 注入保护，eos 标记不会被正确分词，排除特殊 token 后优化器偏好接近 eos 的 token（如 lucrarea），LB 到约 0.65  
- **机制**：排除不可注入的特殊 token 后，暴力搜索才能反映真实可提交的字符串  
- **结果**：约 32k tokens；LB 约 0.65  
- **证据**：[llm-prompt-recovery#494497-01](https://www.kaggle.com/competitions/llm-prompt-recovery/discussion/494497)（@philippsinger｜A）
- 其他案例：[@tascj0](https://www.kaggle.com/competitions/map-charting-student-math-misunderstandings/discussion/612268)、[@tascj0](https://www.kaggle.com/competitions/lmsys-chatbot-arena/discussion/527685)、[@tascj0](https://www.kaggle.com/competitions/lmsys-chatbot-arena/discussion/527685)

## 缺失值/NAN（证据单位 3）

- **条件**：测试 prompt 只来自 Persuade 且素材文章缺失，AI 文本可能与人写文本太像  
- **动作**：用 llm-studio 对学生作文做 LM 微调，让 LLM 生成含引用与拼写错误的模仿学生写作文本，再用这些文本适配分类器  
- **机制**：缩小生成分布与真实测试分布的差距  
- **结果**：适配后 public/private 提升到约 0.94/0.98  
- **证据**：[llm-detect-ai-generated-text#470395-02](https://www.kaggle.com/competitions/llm-detect-ai-generated-text/discussion/470395)（@wowfattie｜A）
- 其他案例：[@ebinan92](https://www.kaggle.com/competitions/eedi-mining-misconceptions-in-mathematics/discussion/551391)

## 公开榜策略（证据单位 2）

- **条件**：测试数据存在已讨论的泄漏  
- **动作**：作者赛后才知道泄漏（论坛早有讨论）；期间选择被泄漏偏置（更长训练、更强过拟合在该数据上有效），但确保长训不伤 CV；赛后分析显示方案在无重叠数据上仍有竞争力  
- **机制**：用公开榜选模会把泄漏红利当成信号；需在无重叠数据上复核  
- **结果**：原文反思  
- **证据**：[foursquare-location-matching#338112-04](https://www.kaggle.com/competitions/foursquare-location-matching/discussion/338112)（@philippsinger｜A）
- 其他案例：[@cdeotte](https://www.kaggle.com/competitions/jigsaw-toxic-severity-rating/discussion/306074)

## 序列模型（证据单位 2）

- **条件**：缺少可用外部数据  
- **动作**：训练 seq2seq T5-large：输入为效果标签加 discourse 类型加 prompt 加左右上下文，输出为 discourse 文本；生成样本按 0-50% 比例混入微调；另有非标签保持 T5 增广只用于 MLM  
- **机制**：按标签与上下文条件生成同风格作文，等价于可控数据增广  
- **结果**：混入比例 0-50%  
- **证据**：[feedback-prize-effectiveness#347433-03](https://www.kaggle.com/competitions/feedback-prize-effectiveness/discussion/347433)（@conjuring92｜A）
- 其他案例：[@darraghdog](https://www.kaggle.com/competitions/linking-writing-processes-to-writing-quality/discussion/466906)

