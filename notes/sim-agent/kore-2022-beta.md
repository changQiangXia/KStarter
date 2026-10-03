# Kore 2022 - Beta（规则型 agent 的完整拆解，58 队小赛）

> 主题：sim-agent ｜ 子类：agent-game ｜ 领域：— ｜ 类别：Playground ｜ 截止：2022-04-07 ｜ 队伍数：58 ｜ 指标：kore_fleets（对局积分）
> 出处：`intel/kore-2022-beta/`（35 条主题索引 + 6 篇正文）

## 任务

Kore 2022 的 Beta 阶段：四人/两人房间中控制舰队采矿、建造船厂、对抗其他 agent 的回合制对战环境；提交 TS/JS agent。本场是正式版（Harm Buisman 夺冠，见 `kore-2022`）的预演。

## 关键要点

- **1st 是纯规则 agent**（与正式版同宗），按顺序执行六个模块：
  1. **船厂防御**：推算被攻击时间点，精确计算"需要多少船"；船厂产能足够就地造、不够则从最近船厂调。
  2. **船厂攻击**：同样精确计算所需船只（"不总是奏效"）。
  3. **直接拦截**：拦截敌方舰队的路线，避开敌方路线重叠。
  4. **相邻攻击**：牺牲己方舰队换取对对手的双/三倍伤害。
  5. **扩张**：kore 盈余且产能不足时新建船厂。
  6. **采矿**：在合法路线中选"每回合 kore 最多"的路线，并检查不与敌舰队路线相交（4 人对局尤其重要）。
  7. 补充：**生成（spawn）** 到舰队数量对敌形成数倍优势。
- 社区反思帖（初学 RL 的玩家）：先读官方示例与规则实现；q-learning 实测完全打不过官方示例的微改版；RL 实现难度/时间成本高——**小赛里规则工程的性价比显著高于 RL**。
- 环境细节：采矿速率与指令数随舰船数变化、相撞双方同时受损——规则细节就是策略空间。

## 可迁移要点

- **规则型 agent 的模块化清单**（防御/攻击/拦截/牺牲换伤/扩张/采矿/产能）可直接迁移到其他基地建设类对战环境。
- "精确计算所需兵力"比"直觉进攻"可靠：把战斗方程写出来。
- 小规模 beta 赛是低竞争试验场；正式版规则变化时策略再迭代。
- RL 不是 agent 赛的默认答案（与 Kore 正式版、Orbit Wars 的预算判断一致）。

## 轻读结论（2026-10 补）

- **1st（规则型，58 票）**：七模块顺序——船坞防御（算清最小补兵/从最近船坞调兵）、船坞进攻、直接拦截、相邻攻击（牺牲换 2–3 倍伤害）、扩张、按 kore/turn 选矿线、爆兵；最终开源代码（317737）。
- **DQN tf.js 基线**：输入 2×8 全局摘要（kore/船数/船坞数/阶段标志），输出 4 个宏动作（do nothing/mine/build ship/build shipyard）交规则执行；MLP 16→100→100→4 = 12,204 参数；稳定到 400 回合、偶尔胜简单 bot（317289）。
- **社区反思**：Q-learning 完全没打出成绩，分数主要来自改官方示例；延迟奖励（返航才结算 kore）是 RL 难点（317955）。
- **赛制**：beta 无奖励、4p→2p、延期一周；50+ 队只有 1 个公开 notebook，榜首疑似官方基线（313582 / 316993 / 315572 / 315962）。

## 图表证据

本场 0 张归档图（0/0），**图证缺口已登记**（1st 的示意图为站外图床）。

## 出处

- 1st：规则模块全拆解：https://www.kaggle.com/competitions/kore-2022-beta/discussion/317737
- 社区反思：从 q-learning 到"官方示例微改"：https://www.kaggle.com/competitions/kore-2022-beta/discussion/317955
- DQN tf.js 基线分享：https://www.kaggle.com/competitions/kore-2022-beta/discussion/317289
- 官方欢迎（无奖励 beta 定位）：https://www.kaggle.com/competitions/kore-2022-beta/discussion/313582
- 4p→2p 调整：https://www.kaggle.com/competitions/kore-2022-beta/discussion/316993
- beta 延期一周：https://www.kaggle.com/competitions/kore-2022-beta/discussion/315572
- 公开分享率讨论：https://www.kaggle.com/competitions/kore-2022-beta/discussion/315962
