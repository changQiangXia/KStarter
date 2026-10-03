# The Pokémon Company - PTCG AI Battle Challenge

> 主题：sim-agent（游戏 agent / 自对弈）｜ 子类：— ｜ 领域：游戏 ｜ 类别：Featured
> 截止：2026-08-31 ｜ 队伍数：6807 ｜ 机制：标准赛（提交 agent，平台持续匹配）｜ 指标：cabt_bo1（对局 rating）
> 数据来源：`intel/pokemon-tcg-ai-battle/`（120 条主题索引 + 8 篇正文 + 13 张图；深读升级 2026-10，Tier A #58）

## 1. 任务与数据

- **对局形式**：宝可梦 TCG 1v1，提交 agent 后由平台持续匹配、按 rating 排行；**匹配制**意味着对手分布是环境的一部分，牌组间关系**非传递**（A>B>C>A）。
- **三层决策**：**构筑（牌组）→ 出牌策略 → 环境博弈（metagame）**；同一策略面对不同对手分布表现截然不同。
- **与固定测试集比赛的差异**：rating 是一条随机过程样本路径（最终评估期仍持续匹配，波动 ±50 分）；单局方差大、隐信息多（对手手牌/牌库）。
- **基础设施事件**：社区先就"能否反编译/自建引擎"要求官方裁定（103 票），官方 2026-07-01 **开源引擎源码**（127 票，限定本赛使用/本地测试训练/禁止利用 bug）；此后 C++ 向量化自对弈成为标配。

## 2. 训练与评估方案

| 环节 | 常见做法 |
| --- | --- |
| 冷启动 | 行为克隆（213tubo：rating≥1050 回放）或 GBDT 教师→蒸馏（24th）；15th 纯 RL 无示范 |
| 自对弈 | PPO/GAE + 群体/历史策略池（20–40 对手）；只给终局奖励 |
| 课程/分工 | 多牌组→原型→单牌组（27th）；双牌组专家（15th）；原型专家池+牌组 PPO（213tubo）；基座+6–7 matchup Experts 路由（24th） |
| 仿真吞吐 | C++ 向量化环境：24th 84 局/秒（32 worker）、27th 30 局/秒（3090+16 核）、15th 55 亿决策 ≈5 GPU-days |
| 评估 | 贝叶斯 Bradley–Terry + 自适应配对 + 胜率画像聚类（24th，320 agents/2.2M 局）；同牌组换座位配对赛（15th）；LB rating 曲线（27th） |
| 推理 | 直接 argmax（15th 实测搜索变体更差）；斩杀检查兜底（213tubo）；MC 采样评估随机动作（Magist） |

## 3. 方案谱系

| 方案 | 名次（票数） | 关键点与数字 |
| --- | --- | --- |
| 群体学习生态 | 24th（39） | GBDT 教师(100–1,000 回放→15K–30K 局) → 蒸馏 980,916 参数 Transformer(120 tokens/6 层/4 头) → 群体 PPO(20–40 对手、5,000 局/周期、131,072 决策/更新、KL≈0.004) → 6–7 Experts 按暴露卡路由；C++/OpenBLAS/AVX2 15×（1ms/32 tokens）；贝叶斯 BT 评估 320 agents/2.2M 局 |
| 纯 RL + 群体自对弈 | 15th（44） | 7.5M 循环 actor-critic；Slowking/Dragapult 双专家；无 BC、无推理搜索、只给终局奖励；约 55 亿决策/5 GPU-days；配对换座位离线评估 |
| BC + 原型 PPO + 蒸馏 | 14th（57） | rating≥1050 回放 → 16.7M 小模型(1.35 亿 steps) → 原型 PPO（共享 expert 池）→ 蒸馏 117M(16.8 亿 steps) → 牌组 PPO；斩杀检查 + argmax |
| 三段课程纯 RL | 27th（32） | 12M Entity Transformer；多牌组→原型→单牌组；30 局/秒；Slowking rating 1132（预期 1100–1160） |
| Pattern DB + T96 | Team Magist（37） | 借鉴 Waltheri 围棋检索：Active 主键 + 伤害/板凳/能量副键 → 动作频率与胜率；T96（2 层 4 头，Action/Pass/Value）；牌组 GA（不稳定，回归榜上成熟牌组）；MC 采样 |
| 引擎合规/开源 | c-number 103 / Addison 127 | 逼出官方裁定并开源引擎，把基础设施拉回同一起跑线 |

## 4. 关键技巧

- **仿真吞吐第一**：C++/矢量化环境 + 批量推理；小模型 + 大经验（24th 1M 参数换 84 局/秒）；大模型蒸馏（213tubo 117M）在经验充足时上限更高。
- **群体/历史策略池**：多样对手 + 冻结历史，防遗忘、防只剥削最新策略、防自对弈坍塌。
- **专家分工 + 廉价路由**：牌组/原型/对局分层；24th 用"对手暴露的关键卡"整模型切换（未知回退基座）。
- **教师冷启动链**：小回放 → 特征教师（GBDT/LambdaRank）生成 15K–30K 局 → 蒸馏神经策略 → PPO；教师价值是**覆盖率**（低 ~200 分但省 50–80% 冷启动时间）。
- **终局奖励**：只给最终胜负（15th 明确不给伤害/奖赏卡 shaping）。
- **评估数学**：贝叶斯 BT + 不确定性驱动的自适应配对；重复变体做密度校正但不删原始记录；胜率画像聚类揭示 matchup 结构。
- **隐藏信息**：belief（自己的牌库/奖赏卡估计）、MC 采样（Judge 等洗牌动作）、循环记忆；不虚构对手手牌。
- **元游戏节奏**：跟踪榜上牌组趋势（"换牌组总是太晚"），主动开发非主流策略（deck-out）可改变环境。

## 5. 深读结论（2026-10 补）

**一句话**：这是一场"系统战"——引擎速度、对手池、评估数学、专家路由、元游戏判断缺一不可；单模型强度只是其中一环。

- 4/4 队用群体/历史池；4/4 队做专家分工；4/4 队把仿真吞吐当第一约束。
- 评估系统是第二主战场：匹配制 rating 有非传递性/样本偏差/最终期方差；24th 的 2.2M 局评估体系是"把测量变成可优化对象"的范例。
- 冷启动两条路都成功：BC/GBDT 教师（213tubo/24th）vs 纯 RL（15th）；差别在"要不要用回放换时间"。
- 推理期搜索无共识：15th 实测更差 → argmax；Magist 只对随机动作做 MC 采样。
- 基础设施合规要在早期解决：711737 → 717141 是"技术可行 ≠ 规则允许"的标准案例。

**数字账精选**：24th 980,916 参数、84 局/秒、15× 加速、2.2M 评估局；15th 55 亿决策/5 GPU-days；213tubo 16.7M→117M、1.35 亿→16.8 亿 steps；27th 1132/1100–1160。

**失败学**：24th 的小回放直接训 Transformer（先 GBDT 教师才解决）；15th 的推理搜索变体与接口编码错误；Magist 的牌组 GA 不稳定；27th 的"祈祷匹配"；所有队都受最终评估期随机性困扰。

**悬案**：1st–13th 方案缺失；榜单评分不一致（712621）未收录；三万局方法揭示（724362）未收录；最终匹配机制与方差（736361/735123）未收录；策略赛道详细 write-up 未纳入。

## 6. 图表证据

> 路径相对本文件（`notes/sim-agent/`）：`../../intel/pokemon-tcg-ai-battle/bodies/<topic>_img/NN.ext`

![24th 的群体学习生态](../../intel/pokemon-tcg-ai-battle/bodies/740956_img/01.png)

**图 1：24th 的六段式生态**（topic 740956）——专家回放(100–1,000 局) → GBDT 教师(15K–30K 局) → 蒸馏(~1M) → 群体 PPO(20–40 对手、5,000 局/周期) → 评估(320 agents/2.2M 局) → 专家复盘。

![24th 的模型架构](../../intel/pokemon-tcg-ai-battle/bodies/740956_img/02.png)

**图 2：980,916 参数 Transformer**（topic 740956）——120 tokens、6 层/4 头/128d、指针策略头 + 51 bin 价值头；分项参数与总数精确对上。

![24th 的 PPO 周期](../../intel/pokemon-tcg-ai-battle/bodies/740956_img/03.png)

**图 3：PPO 周期与吞吐**（topic 740956）——5,000 局采集（32 vCPU 50–60s / 64 vCPU 30–40s）+ 131,072 决策更新（10–15s GPU）。

![24th 的评估系统](../../intel/pokemon-tcg-ai-battle/bodies/740956_img/05.png)

**图 4：自适应群体评估**（topic 740956）——贝叶斯 Bradley–Terry + 不确定性 + 胜率画像聚类 + GitHub CI/CD（~20 分钟）。

![213tubo 的训练管线](../../intel/pokemon-tcg-ai-battle/bodies/735867_img/01.png)

**图 5：213tubo 四段训练管线**（topic 735867）——数据筛选(≥1050) → BC 16M → 原型 PPO（共享 expert 池）→ 蒸馏 117M → 牌组 PPO；斩杀检查 + argmax。

![27th 的 LB 曲线](../../intel/pokemon-tcg-ai-battle/bodies/738158_img/02.png)

**图 6：最终评估期的 rating 波动**（topic 738158）——提交截止后持续评分；Slowking 1132、Ogerpon+Meganium 1036，波动 ±50 分。

![宝可梦 Pattern DB 示例](../../intel/pokemon-tcg-ai-battle/bodies/735593_img/02.png)

**图 7：Pattern DB 动作统计**（topic 735593）——相似局面中 Ogerpon 攻击 58%（胜 61%）、Dipplin 17%（55%）、其他 13%（49%）、不攻击 12%（38%）。

## 7. 可迁移性评估

- **可直接迁移**：
  - 仿真吞吐优先（C++/矢量化 + 批量推理）与"小模型 + 大经验"的取舍；
  - 群体/历史策略池 + 对手分布设计；
  - 分层专业化（牌组/原型/对局）+ 廉价路由；
  - 评估系统（BT/不确定性/自适应配对/重复变体校正/胜率聚类）；
  - 教师冷启动链（特征教师 → 生成数据 → 蒸馏 → RL）；
  - 终局奖励、belief 表征、MC 采样处理随机性。
- **需要前提**：可本地运行/可批量仿真的环境；大量对局预算；可用的回放数据（无则纯 RL）。
- **不建议照搬**：单模型通吃所有牌组；只对最新策略自对弈；依赖反编译/灰色基础设施（先拿官方裁定）；把最终评估期 rating 当精确强度。

## 8. 对新手的关键启示

1. **agent 比赛的评测体系比模型更重要**：先建可靠的对阵评估（统计量+不确定性），再谈优化。
2. **随机性大的游戏里，单局结果不可用于决策**；最终名次本身含随机成分（匹配方差）。
3. **组合决策要分层**（构筑→策略→元游戏），一次性端到端最难。
4. **基础设施是竞争力**：仿真吞吐、C++ 推理、自动化评估流水线都是分数。
5. **合规边界要前置**：引擎/逆向/公开协作这类问题，早期逼出官方裁定；技术上可行不等于规则允许。

## 9. 出处

- 讨论区索引：`intel/pokemon-tcg-ai-battle/topics.md`（120 条）
- 已收录正文（8 篇）：
  - 引擎裁定请求（103 票）：https://www.kaggle.com/competitions/pokemon-tcg-ai-battle/discussion/711737
  - 引擎源码发布（127 票）：https://www.kaggle.com/competitions/pokemon-tcg-ai-battle/discussion/717141
  - 分享时机（16 票）：https://www.kaggle.com/competitions/pokemon-tcg-ai-battle/discussion/733137
  - 213tubo（57 票）：https://www.kaggle.com/competitions/pokemon-tcg-ai-battle/discussion/735867
  - 15th（44 票）：https://www.kaggle.com/competitions/pokemon-tcg-ai-battle/discussion/739241
  - 24th（39 票）：https://www.kaggle.com/competitions/pokemon-tcg-ai-battle/discussion/740956
  - Team Magist（37 票）：https://www.kaggle.com/competitions/pokemon-tcg-ai-battle/discussion/735593
  - 27th（32 票）：https://www.kaggle.com/competitions/pokemon-tcg-ai-battle/discussion/738158
- 深读全本：`analysis/deep/pokemon-tcg-ai-battle.md`（11 组件 + 机制推演 M1–M8 + 13 图证）
- 缺口登记（未收录正文）：712621、724362、709160、729926、735822、736361、735123、717697、716045、708586
