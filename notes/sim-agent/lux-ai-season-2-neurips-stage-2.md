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

## 轻读结论（2026-10 补）

- **唯一技术正文（459891）**：fork Jux（非 lockstep、统计收集、16×16 相邻工厂 spawn、valid_spawns_mask 修复）→ 16/32/64 地图课程（各 80M 步、权重热启动；1024/1024/512 环境）→ DoubleCone 加深感受野（4.72M 参数，value 14，policy 29/位置）→ 大量行动掩码 + 冲突取消 → 统计量按 5M 步 EMA 标准差归一化 + WinLoss 做 PPO。
- **训练何时停比跑满重要**：64×64 的"赢旧 checkpoint"在 20M 步前停止；32×32 金属产量跌破 100（重机器人成本）后仍在产 winner；32×32 KL 30M 步后 >0.02，64×64 loss 周期性尖刺。
- **工程/社区设施**：1×A10 训练 + A100 大地图；Parametrix.ai PPO 基线 + 往季 episode；第三方统计站（分数/胜率/delta）；延期也因 episode 失败（456054）。
- Stage 2 仅 64 队，属精英赛道；本次归档没有最终排名方案。

## 图表证据

![网络配置表](../../intel/lux-ai-season-2-neurips-stage-2/bodies/459891_img/04.png)

**图**（topic 459891）：网络超参表（3 层、通道 128、4.72M 参数、policy 每位置 29）。

![对局步数曲线](../../intel/lux-ai-season-2-neurips-stage-2/bodies/459891_img/08.png)

**图**（topic 459891）：16×16（约 600 步）vs 32/64（常打满）的对局长度。

![金属产量曲线](../../intel/lux-ai-season-2-neurips-stage-2/bodies/459891_img/09.png)

**图**（topic 459891）：金属产量与"赢旧 checkpoint"的拐点。

## 出处

- 讨论区索引：`intel/lux-ai-season-2-neurips-stage-2/topics.md`
- PPO + Jux 方案：见该比赛讨论区 "PPO using Jux" 帖
- PPO + Jux 方案（链接）：https://www.kaggle.com/competitions/lux-ai-season-2-neurips-stage-2/discussion/459891
- 上手资源汇编：https://www.kaggle.com/competitions/lux-ai-season-2-neurips-stage-2/discussion/442050
- 基线/数据/公开代码：https://www.kaggle.com/competitions/lux-ai-season-2-neurips-stage-2/discussion/438939
- 提交统计站：https://www.kaggle.com/competitions/lux-ai-season-2-neurips-stage-2/discussion/442372
- 延期公告：https://www.kaggle.com/competitions/lux-ai-season-2-neurips-stage-2/discussion/456054
