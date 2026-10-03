# Lux AI Season 2 - NeurIPS Stage 2（精简）

> 主题：sim-agent ｜ 子类：— ｜ 领域：游戏 ｜ 类别：Featured ｜ 截止：2023-11-28 ｜ 队伍数：64 ｜ 指标：对战胜率
> 出处：`intel/lux-ai-season-2-neurips-stage-2/`（80 条主题索引 + 6 篇正文）

## 任务

Lux AI Season 2 的 NeurIPS Stage 2（精英赛阶段，仅 64 队），在既有规则下进一步比拼 agent 强度。

## 关键要点

- 可行的技术路线是 **PPO + Jux**（JAX 生态的 RL 框架）：作者维护了 `rl-algo-impls` 训练仓库，并**fork 了 Jux**，主要改动包括支持**非同步（non-lockstep）环境**、统计收集与"相邻工厂"等游戏特性。
- **框架改造深度决定上限**：Lux 的混合阶段（同时 + 顺序决策）与 Jax 的并行假设不兼容，必须改造框架（与 Season 2 主赛的同类结论一致）。
- 参赛队少（64）说明这是**进阶赛道**：适合已有一版 agent 的队伍冲击极限。

## 可迁移要点

- **RL 框架常需为特定环境改造**（并行假设、统计、环境特性）——预算要为工程改造留出时间。
- 系列赛的"精英阶段"是检验方案上限的低竞争窗口。

## 出处

- 讨论区索引：`intel/lux-ai-season-2-neurips-stage-2/topics.md`
- PPO + Jux 方案：见该比赛讨论区 "PPO using Jux" 帖
