# AI Agent Security - Multi-Step Tool Attacks

> `ai-agent-security-multi-step-tool-attacks` ｜ Featured ｜ 指标 Agents Security Metric ｜ 4186 队 ｜ 截止 2026-09-01

本页汇总该场 **1 条 ≥50 票 GM 主题帖**、**4 条断言**、**0 条高票评论**。

## GM 主题帖

| 票 | 选手 | 日期 | 主题 |
| --- | --- | --- | --- |
| 82 | [@xiaoz259](https://www.kaggle.com/xiaoz259) | 2026-09-03 | [1st place solution](https://www.kaggle.com/competitions/ai-agent-security-multi-step-tool-attacks/discussion/739181) |

## 断言（条件→动作→机制→结果）

| 选手 | 等级 | 阶段 | 动作（节选） | 出处 |
| --- | --- | --- | --- | --- |
| @xiaoz259 | A | 建模与训练 | 目标：保持 hop1 精确工具调用，同时让 hop2 首 token 为 EOG；损失为 hop1 目标 NLL 均值加 λ（非 EOG 最大 logit 减 EOG logit） | [ai-agent-security-multi-step-tool-attacks#739181-02](https://www.kaggle.com/competitions/ai-agent-security-multi-step-tool-attacks/discussion/739181) |
| @xiaoz259 | A | 工程/流程 | 用 BF16 权重跑 GCG 生成候选，用 ridge 模型重排，再只在小子集上用真实 GGUF 评估；最终候选按真实 KV-cache 顺序评测；初始 margin 极大（Gem | [ai-agent-security-multi-step-tool-attacks#739181-03](https://www.kaggle.com/competitions/ai-agent-security-multi-step-tool-attacks/discussion/739181) |
| @xiaoz259 | A | 工程/流程 | 用 GCG 把 hop1 与 hop2 margin 都推到 +5 以上；用 0.3.23 重筛；在真实 KV-cache 下评测大 recipient 池、按 margin 排序 | [ai-agent-security-multi-step-tool-attacks#739181-04](https://www.kaggle.com/competitions/ai-agent-security-multi-step-tool-attacks/discussion/739181) |
| @xiaoz259 | B | 验证设计 | 探针：消息 1 发要测试的工具调用；消息 2 若成功且参数正确就停止，否则数 000 到 999；配合 clock 机制消除排队歧义；结论：参数含 secret 的调用被拦、U2A | [ai-agent-security-multi-step-tool-attacks#739181-01](https://www.kaggle.com/competitions/ai-agent-security-multi-step-tool-attacks/discussion/739181) |

## 高票评论

_无 ≥10 票评论_

## 关联资产

- 深读：`analysis/deep/ai-agent-security-multi-step-tool-attacks.md`
- 结构化摘要：`notes/nlp/ai-agent-security-multi-step-tool-attacks.md`
- 归档讨论区：`intel/ai-agent-security-multi-step-tool-attacks/`（主题 1 条有 ≥50 票帖，图证 0 个）
