# Lux AI 2021（首届）

> 主题：sim-agent ｜ 子类：— ｜ 领域：游戏 ｜ 类别：Featured
> 截止：2022-XX-XX ｜ 队伍数：1000+ ｜ 机制：标准赛（提交 agent）｜ 指标：对战胜率
> 数据来源：`intel/lux-ai-2021/`（80 条主题索引 + 6 篇 write-up 正文）

## 1. 任务与数据

- 对局形式：两人对抗的资源争夺游戏（收集资源、建造单位、夜间/白天循环限制），48×48 地图。
- 特点：**Lux 系列的首届**，游戏规则深度大、观赏性强；每回合有计算时间预算。

## 2. 方案谱系

| 方案 | 名次 | 关键点 |
| --- | --- | --- |
| Toad Brigade 的深度强化学习方案 | 高票 | 端到端 DRL 路线 |
| 其他方案 | 见讨论区 | 社区对策略的公开讨论质量高（主办方也参与交流） |

## 3. 关键技巧（结合 Lux 系列共性）

- **计算预算管理**：每回合时间上限决定方法的可行性。
- **规则理解与资源规划**：资源采集/建造的长期规划是核心。
- **规则 + 学习的混合**（在 Season 2 中被验证为高效路线）。
- **系列赛事经验迁移**：2021 → Season 2 的核心策略与工程可复用（除规则变更部分）。

## 4. 可迁移性评估

- **可直接迁移**：计算预算约束下的架构选择；系列赛事（Lux）经验迁移。
- 需要前提：RL 训练环境与算力，或强规则工程能力。
- 不建议照搬：忽略规则的季节变化。

## 5. 对新手的关键启示

1. 与 Lux Season 2 一起读，可见同一系列中"规则变化 → 策略重写"的实际影响。
2. 社区与主办方的公开讨论是 agent 类比赛的重要学习材料。

## 6. 轻读结论（2026-10 补）

**一句话**：冠军 Toad Brigade 用**纯 RL 自对弈**（单网络对全部单位一次前向、奖励仅终局 ±1）碾压规则/模仿路线（对其他队约 +300 Elo）；其余前列靠 **IL（模仿 TD）+ 手工规则 + MCTS**。

- Toad Brigade（294993）：单网络同时输出所有工人/城市动作；数月夜间自对弈；规则改动后从"焦土"自发转为"保护可再生森林"；用逐格删除状态可视化 value 重要性。
- 5th（293911）：**Conditional UNet**（条件=全局状态 + agent 身份）同时模仿 82 个 agent（~1.6 万场）；承认"300 场不足以复制 TD"（差 ~300 Elo）。
- 6th（293776）：7 动作 + **每回合单前向**；先用多 agent 数据训练、再冻结主干只用 TD 回放微调最后 3 层；transfer 与 citytile 模型是增益点。
- 4th：共享 CNN + 每 agent 独立 FC 头（推理只用 top 头）；FReLU/SE/Transformer；**网络输出后接规则解释器**（否则效果差）。
- 8th：自写 C++ 引擎 + **渐进加宽 MCTS + ProposalPolicy 采样 + TransitionNode 哈希 + 虚拟损失多线程**；省略 transfer 是大错。
- 16th：在 sazuma 的 IL 上补规则（加 center 动作、去宵禁、移动/建造排序等）。

**裁决**：RTS 对抗的架构主流 = 单前向多单位；IL 上限=被模仿者水平，要超越需 RL 或搜索；RL 需要高速引擎与长期自对弈窗口；规则在弱策略期是脚手架、在 RL 收敛后是枷锁。

**悬案**：2nd/3rd/7th/9th–15th 方案缺失；RL 技巧清单（51 票）与在线 RL 帖未细读；TD 的网络规模细节缺失。

## 7. 图表证据

![8th 的同时动作 MCTS 结构](../../intel/lux-ai-2021/bodies/294603_img/02.png)

**图 1**（topic 294603）：StateNode/ActionNode/TransitionNode 结构与渐进加宽、ProposalPolicy 采样、虚拟损失并行——"搜索适配 RTS 动作空间"的具体方案。

## 8. 出处

- 讨论区索引：`intel/lux-ai-2021/topics.md`（80 条）
- 已收录 write-up（6 篇）：
  - Toad Brigade DRL 方案（183 票）：https://www.kaggle.com/competitions/lux-ai-2021/discussion/294993
  - 6th（72 票）：https://www.kaggle.com/competitions/lux-ai-2021/discussion/293776
  - 8th（41 票，DNN + 树搜索）：https://www.kaggle.com/competitions/lux-ai-2021/discussion/294603
  - 5th 条件 UNet IL：https://www.kaggle.com/competitions/lux-ai-2021/discussion/293911
  - 4th 多头 IL + 规则：https://www.kaggle.com/competitions/lux-ai-2021/discussion/296938
  - 16th 规则补丁：https://www.kaggle.com/competitions/lux-ai-2021/discussion/293835
  - 开源引擎 + RL Gym（63 票）：https://www.kaggle.com/competitions/lux-ai-2021/discussion/267351
- 轻读全本：`analysis/deep/lux-ai-2021.md`（Tier B 轻读：对照矩阵/裁决/证据分级/悬案 + 1 图证）
