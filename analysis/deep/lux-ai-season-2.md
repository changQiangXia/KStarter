# Lux AI Season 2 轻量深读（Tier B）

> 赛事：Featured ｜ 主题 sim-agent（多智能体策略）｜ 646 队 ｜ 标准赛（提交 agent）｜ 指标：lux_ai_s2（对局胜负/评分）
> 材料基础：`intel/lux-ai-season-2/bodies/` 已有 12 篇正文（digest 仅收录 2 篇——按"≤3 篇定点补采"原则已用本地归档补齐；含 1st 407982、4th FLG 406702、5th 409394、10th Deimos 411725、模仿笔记 404842、防诈骗 381975 等）+ 14 张图
> 轻读时间：2026-10（Tier B B02）

## 1. 一句话重述与数字账

48×48 火星改造 1v1（1000 回合、工厂/重型/轻型单位、电力稀缺、**动作队列**）。真正的考点：**逻辑 bot + 前向模拟 vs 深度 RL** 的路线之争；电力效率（动作队列）与开局选址（冰/矿/战斗）决定上限；元游戏极强（conga 线、冰封锁、太阳能、石头剪刀布）。

| 关键数字 | 值 | 来源 |
| --- | --- | --- |
| 1st（Ryan Anderson，逻辑 bot） | 前向模拟 **2.9s/次**（5–50+ 步）；~10 种 role + goal 状态机；优先级动作锁定；**冰冲突**（抢占对手冰区 + 双轻单位封锁运水）+ 偶尔把对手分数从 36k 打到"破坏匹配算法"；自认 conga 线（Tigga/Siesta）更优 | 1st |
| 4th（FLG，RL） | 以 **CPU 性能**为第一约束（Kaggle 单核 VM）；7 类 actor 的简化动作空间（bid/spawn/工厂/轻重单位 Grid(23)）；模仿学习 + 小地图 RL 选架构；小模型 RL → 大模型蒸馏 → CPU 推理优化 | 4th |
| 5th（Harm，逻辑 bot） | 开局选址评分（冰/矿/邻近瓦砾/无瓦砾湖）；优先级方案；中期尝试全太阳能失败；"ryandy>deimos>我>ryandy"的石头剪刀布 | 5th |
| 10th（Deimos，RL） | PPO（RLlib off-policy）；**用 JAX 重写环境**；特征 48×48×30 + 动作队列 48×48×20×6 + 全局 32；ResNet 融合；**完全忽略动作队列、实时控制**（但允许动作重复省电）；条件采样顺序 | 10th |
| 模仿笔记 | 模仿 Deimos（仅重单位、不用队列）~3000 胜局；动作空间简化为 9+1 类；bid=0/选址朴素——自认初始条件分布不一致的隐患 | 模仿帖 |
| 电力算术（4th） | 队列 20 次 dig：逐回合更新 20×60+20×10=1400 vs 一次队列 20×60+10=**1210（省 ~15%）** | 4th |

## 2. 逐方案对照矩阵

| 维度 | 1st（逻辑） | 4th FLG（RL） | 5th（逻辑） | 10th Deimos（RL） | 模仿帖 |
| --- | --- | --- | --- | --- | --- |
| 规划 | 前向模拟 2.9s | 动作队列建模 | 优先级规则 | 实时控制（忽略队列） | 模仿 Deimos |
| 开局 | 邻冰/矿/平地 + 冰冲突 | 简化 bid/spawn 动作 | 选址评分决定 bid | — | bid 0 + 朴素选址 |
| 关键战术 | 冰封锁 + 反运水 | — | 尝试太阳能 | — | — |
| 模型/算法 | 无学习 | CNN + Actor/Critic | 无学习 | ResNet + PPO/RLlib | 监督分类 |
| 私榜 | **1st** | 4th | 5th | 10th | — |
| 教训 | conga 线更强（自认） | CPU 性能优先 | 缺 conga 线是"great miss" | 队列是大 action space 的根源 | 模仿忽略初始条件分布 |

## 3. 共识、分歧与裁决

### 共识一：电力效率是核心资源，动作队列是双刃剑（3/4）

4th 的算术：队列省 ~15% 电力（最稀缺资源）；10th 因此把队列建模为特征但执行时忽略（实时控制）；模仿帖发现"Deimos 不用队列"让模仿可行。**裁决**：队列能省电但把单步问题变成多步规划、放大动作空间；是否使用取决于你会不会用（逻辑 bot 倾向用、部分 RL 选择放弃并承担电力损失）。置信度：高。

### 共识二：开局选址/竞标决定上限（1st/5th/模仿帖）

1st 的"冰冲突"（故意选次优位置去卡对手冰）、5th 的选址评分与 bid、模仿帖的反思（naive placement + 模仿对象在不同初始条件下的策略=隐患）。**裁决**：本场是"开局即战争"的游戏；选址/竞标要与中后期战术耦合。置信度：高。

### 共识三：策略多样性极高，形成石头剪刀布（5th + 1st）

conga 线（Tigga/Siesta）、冰封锁（1st）、全太阳能（philippkostuch/Harm 试）、重单位灵活运冰（FLG 克制 1st）。**裁决**：没有单一统治策略；对阵矩阵决定名次，meta 判断与针对性调整是分数的一部分。置信度：高。

### 共识四：CPU 推理性能是隐藏约束（4th）

Kaggle VM 单核、匹配用 CPU；FLG 的整个方案围绕推理速度设计。**裁决**：在评测用 CPU 的 agent 赛里，模型/搜索的 CPU 预算是与策略质量并列的设计维度。置信度：中高。

### 分歧一：RL vs 逻辑（本场的路线之争）

冠军是逻辑 bot（1st）+ 前向模拟；RL 队伍 4th/10th；逻辑 5th。**裁决**：在规则复杂但可模拟、动作空间巨大的游戏里，**逻辑+搜索可以战胜 RL**（RL 的样本效率被规则复杂度拖累）；但 RL 在特定对局（Deimos 系）依然是硬骨头。置信度：高（结果本身）。

### 分歧二：是否使用动作队列/链式经济

1st 早期避免链；Tigga/Siesta 的链式经济被其承认"更优"；5th 也把"没有 conga 线"列为最大遗憾；10th 直接放弃队列。**裁决**：链式经济是上限阵容（需要实现与维护质量），不用会吃亏。置信度：中高。

### 事件：匹配/计分故障 + 社交工程诈骗

1st 的冰冲突一度把分数推到 36k+ 并"破坏匹配算法"（官方修复）；跨赛（Otto）曝光的"社交工程偷方案"骗局被转到本场警示：**不要仅凭段位信任 team merge 对象**。**裁决**：平台治理与分享安全是 agent 赛的隐形风险。置信度：高（事件）。

## 4. 证据分级

| 断言 | 等级 | 说明 |
| --- | --- | --- |
| 1st 的模拟/角色/冰冲突 | 自述 + 开源代码 | 中高 |
| FLG 的 CPU 优先设计与电力算术 | 自述 + 架构图 | 中高 |
| Deimos 的 JAX 环境/PPO/忽略队列 | 自述 + 代码 | 中高 |
| 石头剪刀布 meta | 多队独立描述 | 高（现象） |
| 匹配故障 | 1st/5th 描述 | 中高 |
| 诈骗警示 | 跨赛转帖 | 中（与本场无直接受害证据） |

## 5. 悬案与缺口（登记）

- 2nd/3rd（ttigga/danmctree）方案未收录——他们代表了"conga 线/慢速轻群"的顶级路线，缺正文是最大缺口。
- "Final notes and parameter tweaking"（43 票）与 "Yet-another-logic-bot"（31 票）未收录。
- 环境/匹配故障的官方说明缺失；Deimos 的 JAX 环境许可/边界未展开。
- 模仿帖的最终成绩与失败细节未读完（后文未细读）。

## 6. 图表证据

![FLG 的 RL 架构](../../intel/lux-ai-season-2/bodies/406702_img/01.png)

**图 1**（topic 406702）：输入 48×48×105 → Conv+ResBlock×4 → DoubleConeBlock（stride 4 → ResBlock×6 → ConvTransp×2 跳连）→ ResBlock×4 → Critic（标量价值）+ Actor Heads（多形状 logits）。**面向 CPU 性能的紧凑 CNN-AC 架构**。

![1st 的"可视化器"](../../intel/lux-ai-season-2/bodies/407982_img/01.jpg)

**图 2**（topic 407982，玩笑）：作者自述"state-of-the-art visualizer"——实为实体棋盘（CATAN/Quoridor）照片。本场社区文化的注脚。

## 7. 出处

- 1st（43 票）：https://www.kaggle.com/competitions/lux-ai-season-2/discussion/407982
- 4th FLG（51 票）：https://www.kaggle.com/competitions/lux-ai-season-2/discussion/406702
- 5th（11 票）：https://www.kaggle.com/competitions/lux-ai-season-2/discussion/409394
- 10th Deimos（15 票）：https://www.kaggle.com/competitions/lux-ai-season-2/discussion/411725
- 模仿笔记（31 票）：https://www.kaggle.com/competitions/lux-ai-season-2/discussion/404842
- 防诈骗警示（8 票）：https://www.kaggle.com/competitions/lux-ai-season-2/discussion/381975
- 往届顶尖方案索引：https://www.kaggle.com/competitions/lux-ai-season-2/discussion/381184
