# Autonomous Agent Prediction (Beta) - 元竞赛：提交"会自己建模的 Agent"

> 主题：sim-agent ｜ 子类：agent ｜ 领域：— ｜ 类别：Playground ｜ 截止：2026-08-06 ｜ 队伍数：570 ｜ 指标：主办方评测（Agent 在会话内自主完成预测任务得分）
> 出处：`intel/autonomous-agent-prediction-beta/`（30 条主题索引 + 6 篇正文）

## 任务

**元竞赛**：你不提交模型，而是提交一个 **Agent Config**——由 LLM 驱动的 agent 在受限会话（约 60 分钟、$2 LLM 预算）内自主完成"读数据集 → 验证 → 建模 → 提交流程"的预测任务，最终按隐藏任务上的成绩排名。

## 关键要点

- **3rd（首次参赛者）方案**：构建一个 meta-agent，自动训练并混合 LightGBM/XGBoost/CatBoost（原生处理类别，避免 one-hot 膨胀）+ 逻辑回归基线；**用诚实的 OOF 验证决定"单模还是融合"**；工作流预算感知：先定向数据 → 正确 CV → **尽早交一个快速基线拿锚点分** → 再迭代 FE 并复核融合是否仍胜出。
- **工程即胜负**（失败模式清单）：
  - agent.yaml/子配置路径格式错 → 多次提交失败才通过；**本地用 validate_submission.py 先验证**；
  - 模型工具支持差异（gemini-2.5-* 只支持单工具、deepseek-r1 不支持工具）；
  - skill 命名规范（小写 kebab-case）；
  - agent 陷思考循环烧光 token、脚本超时、无提交退出——对提示词与温度设置的要求很高。
- 生态信号：官方 Discord 支持；社区在问"会不会成为月度系列"、"$2 预算够不够"。

## 可迁移要点

- **"提交一个能自己干活的 agent"是 2026 的新赛制形态**——参赛技能从"建模"扩展到"流程工程 + 预算管理 + schema 验证"。
- 预算感知工作流：先锚点基线，后迭代优化（与人类打榜的节奏同构）。
- 用 OOF 决定融合与否——自动化流程的核心决策仍需统计纪律。
- 任何 agent 提交类任务：**先过本地验证器，再消耗正式提交次数**。

## 出处

- 3rd：首赛即前三的 Agent Config 方案：https://www.kaggle.com/competitions/autonomous-agent-prediction-beta/discussion/737407
- 提交失败常见原因与修复：https://www.kaggle.com/competitions/autonomous-agent-prediction-beta/discussion/723907
- 入门与官方 Discord：https://www.kaggle.com/competitions/autonomous-agent-prediction-beta/discussion/723664
