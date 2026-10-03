# LMSYS - Chatbot Arena Human Preference Predictions

> 主题：nlp ｜ 子类：— ｜ 领域：LLM 评测 ｜ 类别：Research
> 截止：2024-08-12 ｜ 队伍数：1849 ｜ 机制：代码赛 ｜ 指标：对数损失（偏好概率）
> 数据来源：`intel/lmsys-chatbot-arena/`（80 条主题索引 + 6 篇 write-up 正文）

## 1. 任务与数据

- 预测目标：给定用户提问与两个模型的回答，预测人类更偏好哪一个（输出概率，按对数损失评分）。
- 数据形态：三方对话（prompt / response_a / response_b）+ 人类投票结果；**A/B 顺序与长度存在偏差**。
- 构造陷阱：
  - 序列长（多轮 + 双回答）→ 截断策略关键；
  - 人类偏好带噪声与位置偏差；
  - 推理成本高（要跑多个大模型）。

## 2. 方案谱系

| 方案 | 名次 | 关键点 |
| --- | --- | --- |
| 微调大模型（LoRA/QLoRA 路线） | 16th | 作者记录了自己的成长路径：7B → 8B → 72B → 34B 逐步上手大模型微调与推理 |
| 其他方案 | 见讨论区 | |

## 3. 关键技巧

- **LoRA/QLoRA 是平民化微调大模型的标准手段**（16th 的成长路径说明了学习曲线）。
- **截断与拼接策略**决定长对话任务的上限（与 WSDM Chatbot Arena 同源）。
- **概率输出 + 对数损失**：需要校准而非单纯排序。
- **跨赛事技能迁移**：作者把 Essay、20 Questions、KDD Cup 的经验连续应用于本场。

## 4. 可迁移性评估

- **可直接迁移**：
  - LoRA/QLoRA 微调流程与推理成本管理；
  - 人类偏好数据的噪声处理与概率校准；
  - 跨赛事技能积累（同一作者连续在 4 场 LLM 赛中复用经验）。
- 需要前提：大模型微调环境与 GPU 预算。
- 不建议照搬：忽略位置偏差（A/B 顺序）直接训练。

## 5. 对新手的关键启示

1. **大模型微调的学习曲线是渐进的**（7B → 72B，16th 的路径值得参考）。
2. **偏好预测要输出校准概率**，不是二元判断。
3. 与 WSDM Chatbot Arena 对照：同一类任务的两届比赛，方法演进可对比。

## 6. 出处

- 讨论区索引：`intel/lmsys-chatbot-arena/topics.md`（80 条）
- 已收录 write-up（6 篇）：
  - 1st "Distill is all you need"（196 票）：https://www.kaggle.com/competitions/lmsys-chatbot-arena/discussion/527629
  - 2nd（107 票）：https://www.kaggle.com/competitions/lmsys-chatbot-arena/discussion/527685
  - 16th 成长记录（205 票）：https://www.kaggle.com/competitions/lmsys-chatbot-arena/discussion/527596
