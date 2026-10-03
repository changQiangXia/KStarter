# Lux AI 2022 - Beta（赛季二 beta 预览，44 队）

> 主题：sim-agent ｜ 子类：— ｜ 领域：— ｜ 类别：Playground ｜ 截止：2022-12-22 ｜ 队伍数：44 ｜ 指标：Lux AI 2022（对局积分）
> 出处：`intel/lux-ai-2022-beta/`（39 条主题索引 + 6 篇正文）

## 任务

Lux AI Season 2 的**公开测试预览**：无奖金/积分/奖牌，目标是收集反馈、平衡规则；火星工厂/机器人资源对抗环境，提交 Python agent 参与配对对局。

## 关键要点

- 官方资源包：GitHub 主仓（starter kits/API/本地对战）、2022 规则规格、Jupyter 教程、官方 Discord——**beta 场的第一步是读环境文档**。
- Season 2 机制变化（与 Season 1 的差异即策略空间）：
  - 两个阶段、两套动作空间；
  - 机器人执行**动作队列**（move/dig/transfer 的离散序列），而非单步动作；
  - 机器人类别：轻/重两档（各有优劣）；碰撞启用且按重量级裁决。
- 平台实验：**限制活跃提交数为 3**（新提交替换旧提交）——提高对局速率；这是 Lux 系列后来的标准机制。
- 社区工具：Lux Eye 可视替代方案等。

## 可迁移要点

- 环境版本升级 = 策略重估（参见 `lux-ai-season-2` 的"规则变更先重估最优策略"）——beta 里养成的"读变更日志"习惯直接迁移到正式赛。
- 动作队列与两阶段设计对 agent 架构的要求：队列规划与阶段状态机，而非逐帧反应。
- 提交限制类机制（3 活跃提交）引导策略把算力投给更少但更强的方案。

## 出处

- 官方资源与变更清单：https://www.kaggle.com/competitions/lux-ai-2022-beta/discussion/363366
- 欢迎与定位（无奖金反馈场）：https://www.kaggle.com/competitions/lux-ai-2022-beta/discussion/362825
- 活跃提交限制实验：https://www.kaggle.com/competitions/lux-ai-2022-beta/discussion/363479
