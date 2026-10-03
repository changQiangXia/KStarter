# Konwinski Prize（AI 自动解 Kaggle 竞赛）

> 主题：nlp（agentic）｜ 子类：reasoning ｜ 领域：AI for AI ｜ 类别：Featured
> 截止：2025-XX-XX ｜ 队伍数：617 ｜ 机制：代码赛 ｜ 指标：按"解对数量"计分（$1.2M 奖金）
> 数据来源：`intel/konwinski-prize/`（80 条主题索引 + 6 篇 write-up 正文）

## 1. 任务与数据

- 任务形式：让 LLM/agent **自动解出真实的 Kaggle 竞赛题**（类 SWE-bench 的"AI 解决 ML 任务"设定），在全新数据上评测。
- 关键规则差异（4th/15th 明确总结）：
  1. **完全新数据、无泄漏**；
  2. **答错惩罚重** → 必须设计**跳过（skip）机制**，宁可不答也不要瞎答；
  3. **禁止调用 API** → 只能用开源 LLM 自行部署。

## 2. 方案谱系

| 方案 | 名次 | 关键点 |
| --- | --- | --- |
| Agentless 式流水线：**定位 → 生成测试 → 生成补丁 → 验证** | 公开第 2 | 多道检查决定"是否跳过"；作者坦承"本方案大部分代码由 LLM 写成" |
| 跳过机制 + 开源 LLM 部署 | 公开第 4 / 私榜 15 | 最佳公开成绩 +0.056243（4 对 0 错）——**零错误的取舍策略** |
| 1st / 3rd 方案 | 1st / 3rd | 见讨论区 |

## 3. 关键技巧

- **跳过（abstain）机制**：在"答错重罚"的计分规则下，**判断何时放弃比强行作答更值钱**。
- **阶段性流水线**：定位问题 → 生成验证测试 → 生成补丁 → 自验证（Agentless 范式）。
- **离线部署开源模型**：没有 API 意味着必须自己搭建推理栈（与 AIMO 3 的工程要求同源）。
- **用 LLM 写方案本身**（公开第 2 的方案主要由 LLM 编写）——2025 年的新常态。

## 4. 可迁移性评估

- **可直接迁移**：
  - **"答错重罚"场景下的 abstain 策略**（风控、医疗辅助、自动交易通用）；
  - "定位 → 验证 → 修改 → 再验证"的 agent 流水线；
  - 离线部署与推理预算管理。
- 需要前提：开源 LLM 部署能力、agent 框架与评测沙箱。
- 不建议照搬：无条件给出答案而忽略错误代价。

## 5. 对新手的关键启示

1. **先读计分规则**：答错惩罚重时，**"不答"是最优动作之一**。
2. **Agentless 流水线（定位→测试→补丁→验证）是当前自动解题的主流骨架**。
3. 与 AIMO 3、Rogii 等对照：**AI 辅助已完成从"写代码"到"做研究"的迁移**。

## 6. 出处

- 讨论区索引：`intel/konwinski-prize/topics.md`（80 条）
- 已收录 write-up（6 篇）：
  - 1st（75 票）：https://www.kaggle.com/competitions/konwinski-prize/discussion/568884
  - 公开第 2（42 票）：https://www.kaggle.com/competitions/konwinski-prize/discussion/568888
  - 公开 4 / 私榜 15（23 票）：https://www.kaggle.com/competitions/konwinski-prize/discussion/568799
  - 8th（13 票）：https://www.kaggle.com/competitions/konwinski-prize/discussion/590920
