# Autonomous Agent Prediction Beta 轻量深读（Tier B）

> 赛事：Playground（meta-agent 赛）｜ 主题 sim-agent（自律 agent 做表格预测）｜ 570 队 ｜ 指标 Autonomous Agent Prediction Beta Metric ｜ 截止 2026-08-06
> 材料基础：`digests/autonomous-agent-prediction-beta.md`（6 篇正文：起步与 Discord 723664 / 提交失败原因 723907 / 3rd 方案 737407 / 月度系列询问 723810 / 反馈征集 732744 / $2 预算 723806；30 条主题索引）+ 0 张归档图
> 轻读时间：2026-10（Tier B B21）

## 1. 一句话重述与数字账

一场"元比赛"：**提交的不是模型，而是一个自主 agent 的配置**（agent.yaml 等），由评测系统把它编译成 Google ADK agent，让它在**每 session 60 分钟**与 **$2.00 LLM token 预算**内自己读数据、写代码、训模型并产出预测。3rd（首次参赛）的方案证明了最稳的路线：**预算感知的工作流**（先定向数据集 → 正规 CV → 尽早交一个快基线拿锚点 → 迭代特征工程并复查 blending 是否仍最优）+ LGBM/XGB/CatBoost/LR 的 OOF 选择。真正的门槛不是建模而是**Agent 工程**：schema 校验、工具兼容性、失败模式排查——官方整理的"提交失败原因"帖是本场最有价值的文档。

| 关键数字 | 值 | 来源 |
| --- | --- | --- |
| 规模与约束 | **570 队**；每 session **60 分钟**；LLM 预算 **$2.00**（`max_budget_usd`）；提交 = Agent Config；评测把提交编译成 Google ADK agent | 723806 / 737407 / 723907 |
| 3rd 方案（6 票） | 训练并融合 **LightGBM + XGBoost + CatBoost**（原生类别处理，不做 one-hot）+ LogisticRegression 基线；用**诚实的 OOF** 在"最佳单模 vs blend"间选择；流程：先定向 → CV → **早交快基线拿真实锚点** → 特征迭代后重查 blending；作者建议先用 `validate_submission.py` 本地校验，别烧提交次数 | 737407 |
| 官方失败清单（9 票 / 11 评论） | ① 多工具只支持全是 search 工具（gemini-2.5-* 仅单工具；deepseek-r1-0528 不支持工具）② skill 名必须 lowercase kebab-case ③ agent 没交有效预测（思考死循环烧 token、脚本吃满 session、直接终止）④ ADK 会把 `{x}` 当会话变量注入（LaTeX `\sqrt{x}` 报错，`\sqrt{x }` 可以）⑤ 新版 Anthropic 传 temperature 会失败 | 723907 |
| 预算讨论 | "LLM 预算只有 $2？"（11 票）；能否用 Kaggle Benchmarks 额度加预算；超预算怎么办；每 session 60 分钟 | 723806 / 727794 / 724387 |
| 系列化 | 官方奖品描述暗示系列赛（每人只发一次周边）；"会是月度系列吗"（10 票 / 4 评论） | 723810 |
| 社区技巧/坑 | LB 0.823 模板（利用 "freeroll" fallback 规则 + Gemini Pro，2 票）；`select_submission` 实测收益上限 +0.0005、最差 −0.0166（0 票 / 5 评论）；本地评测 `run_local_eval.py`；Qwen 托管模型在 episode 前失败；提交 PENDING/ERRORS；模型别名不在 registry | 730539 / 730605 / 730578 / 727397 / 729897 / 724397 |

## 2. 逐方案对照矩阵

| 维度 | 3rd（OOF 选模） | 0.823 模板（规则套利） | 失败模式 |
| --- | --- | --- | --- |
| 策略 | 多模型 + honest OOF 选择 | 利用 fallback 规则 | 死循环/空跑 |
| 交付 | 稳健 agent 配置 | 快速锚点 | schema/工具错误 |
| 风险 | 时间/预算不够 | 规则变动 | 0 有效预测 |

## 3. 共识、分歧与裁决

### 共识一：Agent Config 工程是主要成本，先本地校验（737407 / 723907；置信度高）

3rd 反复强调 schema（agent.yaml、子 agent 路径）要靠 `validate_submission.py` 先本地跑通；官方失败清单几乎全是配置/工具/指令问题。**裁决**：把 80% 前两小时花在"本地能跑通 + 能提交"上，再用剩余预算调模型。置信度：高。

### 共识二：预算感知工作流 = 先锚点再迭代（737407；置信度中高）

60 分钟 + $2 的约束下，作者选择"先交快基线拿真实分数，再迭代并复查是否 blend 仍最优"。**裁决**：流程固定为定向 → CV → 快速基线 → 特征迭代 → OOF 重选；每一步都要有时间/ token 预算上限。置信度：中高。

### 事件一：模型-工具兼容性是硬约束（723907；置信度高）

gemini-2.5-* 只支持单工具、deepseek-r1-0528 不支持工具、Anthropic 新版 temperature 报错、ADK 花括号注入。**裁决**：选模型前先读官方兼容表；指令里避免裸 `{identifier}`；失败先看清单再改代码。置信度：高。

### 事件二：单提交/选择策略的风险很小但仍要保守（730605 / 723813；置信度中）

实测 `select_submission` 上限 +0.0005、最差 −0.0166；社区问"一次提交是否太少"。**裁决**：按 OOF 诚实选择（blend 只有在稳定胜出时才用），不要用 LB 反馈调策略。置信度：中。

### 事件三：系列赛（月度）与进阶路线可期（723810 / 732744 / 723664；置信度中低）

官方反馈帖与周边规则暗示系列化。**裁决**：把本次配置沉淀为可复用模板（schema/工具适配/预算策略），为下一轮省时间。置信度：中低。

## 4. 证据分级

| 断言 | 等级 | 说明 |
| --- | --- | --- |
| 赛制与预算（60min/$2/Agent Config） | 官方帖与概述（723806 / 723907） | 高 |
| 3rd 的 OOF 流程与模型 | 作者自述（737407） | 中高 |
| 官方失败原因清单 | 官方整理帖（723907） | 高 |
| 0.823 模板 | 社区帖（730539） | 中低（规则套利） |
| select_submission 实测 | 社区帖（730605） | 低—中 |
| 系列化暗示 | 规则文字 + 讨论（723810） | 中低 |

## 5. 悬案与缺口（登记）

- 最终排名/获奖 agent 正文未归档（3rd 是唯一可读方案）；
- metric 具体公式与 session 内评分细节未归档；
- $2 预算是否可扩展无官方结论；
- "freeroll" fallback 规则是否被后续版本修补未知；
- **图证缺口**：本场 0 张归档图，已登记。

## 6. 图表证据

本场 0/0 张归档图，**图证缺口已登记**。

## 7. 出处

- 3rd 方案（6 票 / 2 评论）：https://www.kaggle.com/competitions/autonomous-agent-prediction-beta/discussion/737407
- 官方失败原因清单（9 票 / 11 评论）：https://www.kaggle.com/competitions/autonomous-agent-prediction-beta/discussion/723907
- $2 预算讨论（11 票 / 7 评论）：https://www.kaggle.com/competitions/autonomous-agent-prediction-beta/discussion/723806
- 月度系列询问（10 票 / 4 评论）：https://www.kaggle.com/competitions/autonomous-agent-prediction-beta/discussion/723810
- 官方反馈征集（6 票 / 13 评论）：https://www.kaggle.com/competitions/autonomous-agent-prediction-beta/discussion/732744
- 0.823 fallback 模板（2 票 / 0 评论）：https://www.kaggle.com/competitions/autonomous-agent-prediction-beta/discussion/730539
- select_submission 实测（0 票 / 5 评论）：https://www.kaggle.com/competitions/autonomous-agent-prediction-beta/discussion/730605
- 本地评测笔记（0 票 / 2 评论）：https://www.kaggle.com/competitions/autonomous-agent-prediction-beta/discussion/730578
