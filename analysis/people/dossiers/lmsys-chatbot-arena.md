# LMSYS - Chatbot Arena Human Preference Predictions

> `lmsys-chatbot-arena` ｜ Research ｜ 指标 Log Loss ｜ 1849 队 ｜ 截止 2024-08-12

本页汇总该场 **4 条 ≥50 票 GM 主题帖**、**15 条断言**、**2 条高票评论**。

## GM 主题帖

| 票 | 选手 | 日期 | 主题 |
| --- | --- | --- | --- |
| 205 | [@cdeotte](https://www.kaggle.com/cdeotte) | 2024-08-13 | [16th Place - So Close to Gold Medal 😀](https://www.kaggle.com/competitions/lmsys-chatbot-arena/discussion/527596) |
| 196 | [@sayoulala](https://www.kaggle.com/sayoulala) | 2024-08-13 | [1st Place Solution ➡️ Distill is all you need🔥🔥🔥](https://www.kaggle.com/competitions/lmsys-chatbot-arena/discussion/527629) |
| 107 | [@tascj0](https://www.kaggle.com/tascj0) | 2024-08-13 | [2nd place solution](https://www.kaggle.com/competitions/lmsys-chatbot-arena/discussion/527685) |
| 59 | [@philippsinger](https://www.kaggle.com/philippsinger) | 2024-08-13 | [5th Place Solution: Team Danube](https://www.kaggle.com/competitions/lmsys-chatbot-arena/discussion/527669) |

## 断言（条件→动作→机制→结果）

| 选手 | 等级 | 阶段 | 动作（节选） | 出处 |
| --- | --- | --- | --- | --- |
| @sayoulala | A | 建模与训练 | 先用 ut 数据对 3 个模型 post-pretrain 1 epoch（lr=1e-5）；5 折训练 llama3-70b 与 qwen2-72b；再把大模型 logits 蒸 | [lmsys-chatbot-arena#527629-01](https://www.kaggle.com/competitions/lmsys-chatbot-arena/discussion/527629) |
| @sayoulala | A | 集成与融合 | 5 折 LoRA 权重直接平均；GPTQ 量化 8bit；提交时 TTA（length 2000） | [lmsys-chatbot-arena#527629-02](https://www.kaggle.com/competitions/lmsys-chatbot-arena/discussion/527629) |
| @sayoulala | A | 验证设计 | 记录 5 折 CV：qwen72b 0.875/0.881/0.869/0.880/0.875；llama3-70b 0.874/0.877/0.877/0.873/0.873；d | [lmsys-chatbot-arena#527629-03](https://www.kaggle.com/competitions/lmsys-chatbot-arena/discussion/527629) |
| @tascj0 | A | 建模与训练 | 全参训练：BF16 加支持 Kahan 求和的优化器，单 A100 80G 可训 7B、9B 需 2 张；最后 10 天用 4 张 A100 80G | [lmsys-chatbot-arena#527685-02](https://www.kaggle.com/competitions/lmsys-chatbot-arena/discussion/527685) |
| @tascj0 | A | 特征与数据工程 | 把原样本与其 swap 一起训，且两者梯度必须在同一个 optimizer.step 内累积；训练时间翻倍但 gemma2-9b 稳定加 0.003；再加 PAB 与 PAPB 双 | [lmsys-chatbot-arena#527685-03](https://www.kaggle.com/competitions/lmsys-chatbot-arena/discussion/527685) |
| @tascj0 | A | 建模与训练 | stage1 微调 gemma-2-9b、gemma-2-27b、ArmoRM-8B（val 0.891/0.883/0.899，平均 ensemble 0.876）；stage2 | [lmsys-chatbot-arena#527685-04](https://www.kaggle.com/competitions/lmsys-chatbot-arena/discussion/527685) |
| @philippsinger | A | 建模与训练 | 用公开 reward 数据（主要 UltraFeedback，二分类 win/loss 足够）预训练 gemma-2-9b；以此为起点再微调，CV 与 public 提升最多 20 | [lmsys-chatbot-arena#527669-01](https://www.kaggle.com/competitions/lmsys-chatbot-arena/discussion/527669) |
| @philippsinger | A | 集成与融合 | 不用伪标签/蒸馏/1M 数据；两个 gemma-2-9b 各在全量数据上训 1 epoch（响应顺序不同），推理时一个用原序、一个用交换 A/B 顺序做 TTA；单折约 0.873 | [lmsys-chatbot-arena#527669-02](https://www.kaggle.com/competitions/lmsys-chatbot-arena/discussion/527669) |
| @philippsinger | A | 工程/流程 | 最佳设置：两个 GPU 各跑一半数据并发、按长度排序并优化 batch 组成、bitsandbytes INT8 加 fp16 计算；8k 上下文可容两个模型，最终提交用 4k 保 | [lmsys-chatbot-arena#527669-03](https://www.kaggle.com/competitions/lmsys-chatbot-arena/discussion/527669) |
| @cdeotte | B | 建模与训练 | 用 LoRA/QLoRA：rank=64 只训 200k 参数（rank=16 为 50k），其余权重冻结 | [lmsys-chatbot-arena#527596-01](https://www.kaggle.com/competitions/lmsys-chatbot-arena/discussion/527596) |
| @cdeotte | B | 建模与训练 | 调参顺序：先 target_modules（尽量全模块）→ 定 LR（2e-4/2e-5，full batch 8）→ 固定 r=16 扫 alpha（2 到 64）→ 固定最优  | [lmsys-chatbot-arena#527596-02](https://www.kaggle.com/competitions/lmsys-chatbot-arena/discussion/527596) |
| @cdeotte | B | 集成与融合 | 按顺序叠加：TTA、LoRA 配置调整、加 target modules、外接 33k 去重数据 100% 训练、max 2048、r=1024、8bit 推理、双 Gemma2  | [lmsys-chatbot-arena#527596-03](https://www.kaggle.com/competitions/lmsys-chatbot-arena/discussion/527596) |
| @cdeotte | B | 建模与训练 | 截断左侧（保留结尾）而不是截断右侧（保留开头） | [lmsys-chatbot-arena#527596-04](https://www.kaggle.com/competitions/lmsys-chatbot-arena/discussion/527596) |
| @tascj0 | B | 建模与训练 | StratifiedGroupKFold by prompt、留 20%；加入 21k 去重 33k 数据；输入格式 PAB 与 PAPB（1.5B 用后者更好、7B 以上无差）； | [lmsys-chatbot-arena#527685-01](https://www.kaggle.com/competitions/lmsys-chatbot-arena/discussion/527685) |
| @sayoulala | C | 复盘与流程 | 把蒸馏作为主轴：大模型转小模型；该赛 CV 与 LB 一致性好 | [lmsys-chatbot-arena#527629-04](https://www.kaggle.com/competitions/lmsys-chatbot-arena/discussion/527629) |

## 高票评论

| 票 | 选手 | 日期 | 摘录 | 出处 |
| --- | --- | --- | --- | --- |
| 11 | @cdeotte | 2024-08-14 | UPDATE: I published code to reproduce my best single model. See links in last section of my discussion post. T | [527596](https://www.kaggle.com/competitions/lmsys-chatbot-arena/discussion/527596) |
| 11 | @cdeotte | 2024-08-25 | It's called Auxilliary learning. By challenging the LLM to learn more related tasks, we make the LLM smarter i | [527596](https://www.kaggle.com/competitions/lmsys-chatbot-arena/discussion/527596) |

## 关联资产

- 深读：`analysis/deep/lmsys-chatbot-arena.md`
- 结构化摘要：`notes/nlp/lmsys-chatbot-arena.md`
- 归档讨论区：`intel/lmsys-chatbot-arena/`（主题 4 条有 ≥50 票帖，图证 2 个）
