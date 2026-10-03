# Maze Crawler（2026，滚动迷宫 agent：规则分层 vs RL 流水线）

> 主题：sim-agent ｜ 子类：— ｜ 领域：游戏 ｜ 类别：Playground ｜ 截止：2026-06-30 ｜ 队伍数：459 ｜ 指标：crawl（对局积分）
> 出处：`intel/maze-crawler/`（23 条主题索引 + 6 篇正文）

## 任务

滚动迷宫中的工厂-单位对抗：在持续南移的地图中采矿、扩张、清障并对抗另一名玩家；能量/生存压力并存，提交 agent 代码参与配对。

## 关键要点

- **1st：分数函数驱动的统一 BFS**（三层架构）：
  1) **移动层**：从工厂做一次 BFS（含跳跃边、记录到达 tick 与跳跃 CD），对每个可达格打分取最大——**行为完全由分数公式塑造**（主项 sbd = "距死亡还有几 tick"，取到达时刻而非当前时刻的值；另有边缘惩罚、跨界一次性奖励等）；同一套 BFS 复用于探索/接近节点/接近敌人，只换评分项。
  2) **经济层**（与多数强队相同）：`node > bfs` 优先级——安全时去矿点、建矿工、蹲矿刷能量；sbd 低时切工人模式往北清墙求生。
  3) **胜负手——碰撞能量平局**：主动管理工厂碰撞的平局判定，**而不是像多数顶层方案那样刷能量等 500 步后的平局**。
- **3rd：完整 RL 流水线**（Genematon 实验特性）：行为克隆（用平台每日数据集）冷启动 → PPO 自我对弈 → 多代进化；**用 LLM 协助写了环境的高速 JAX 移植**——"快速模拟器是一切的前提"。
- **7th：全局任务分配的工程流**：匈牙利匹配给每个单位分配唯一目标（防扎堆）；**地图东西对称**→ 用镜像侧已知布局补雾区；**时间步瓦片预约**（按优先级顺序规划路径并预定未来 tick 的格子）防碰撞；走廊清障与末局调整。

## 可迁移要点

- 规则型 agent 的最高形态：**"一个 BFS + 可插拔评分项"**——把行为差异都收敛到分数公式，维护成本极低。
- RL 路线的三要素：高速模拟器（JAX 移植是门槛）、行为克隆冷启动、PPO 自我对弈。
- 多单位协作先做"全局唯一分配"（匈牙利匹配）再谈个体策略。
- 利用环境对称性（镜像补图）与时间维度的碰撞预约，是工程感很强的通用技巧。
- 本场是 2026 年代 agent 赛生态的切片：人类规则、RL 流水线、LLM 工具链并存。

## 轻读结论（2026-10 补）

- **1st（Maksim Savelev 2006.5）**：三层 = first-move BFS 单一评分函数（jump-aware）+ 节点采矿经济（`node > bfs`，矿工变矿、工厂坐矿）+ **主动逼迫碰撞**；关键常数 `ENERGY_CAP=3000` 一锁存即停止采矿转猎杀、`TIEBREAK_DIST=5` 时在身后放 300 能量矿工、`TIEBREAK_MINER_LOOKAHEAD=2` 预判矿工死亡避免同 tick 双亡（717120）。
- **近镜像教训**：只针对标准能量流调到 ~95% 胜率，未调镜像；对 bunterrrr 约 53/47（估计），最终 2006.5 vs 1953.4。
- **3rd（Genematon 1796.4）**：JAX 环境移植 + 行为克隆 bootstrap + PPO 自对弈（小网络、最小奖励）；自述自对弈池同质导致战斗弱，建议 AlphaStar 式对抗对手（718158）。
- **7th**：匈牙利匹配全局任务分配 + 时间片格子预留 + 对称补全 + 终局北撤（717177）。
- 无奖牌/积分、环境本地与线上不一致、tiebreak 怪异等社区问题密集（696453 / 701737 / 702770）。

## 图表证据

![工厂坐在矿上收能](../../intel/maze-crawler/bodies/717120_img/01.png)

**图**（topic 717120）：工厂停在矿上收能（经济层核心）。

![终局回放](../../intel/maze-crawler/bodies/717120_img/04.png)

**图**（topic 717120）：第 186 步 Maksim Savelev（E=331）击败 Genematon（E=300）。

![最终排行榜](../../intel/maze-crawler/bodies/717120_img/05.png)

**图**（topic 717120）：Maksim Savelev 2006.5 > bunterrrr 1953.4 > Genematon 1796.4。

## 出处

- 1st：分数函数驱动的 BFS 三层架构：https://www.kaggle.com/competitions/maze-crawler/discussion/717120
- 3rd：RL 流水线（JAX 模拟器 + BC + PPO）：https://www.kaggle.com/competitions/maze-crawler/discussion/718158
- 7th：匈牙利匹配 + 时间步预约：https://www.kaggle.com/competitions/maze-crawler/discussion/717177
- 无奖牌/积分询问：https://www.kaggle.com/competitions/maze-crawler/discussion/696453
- 每日 episode 数据集：https://www.kaggle.com/competitions/maze-crawler/discussion/701822
- 环境本地/线上不一致：https://www.kaggle.com/competitions/maze-crawler/discussion/701737
