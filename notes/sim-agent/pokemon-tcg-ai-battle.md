# The Pokémon Company - PTCG AI Battle Challenge

> 主题：sim-agent ｜ 子类：— ｜ 领域：游戏 ｜ 类别：Featured
> 截止：2026-08-31 ｜ 队伍数：6807 ｜ 机制：标准赛（提交 agent）｜ 指标：cabt_bo1（对战评分）
> 数据来源：`intel/pokemon-tcg-ai-battle/`（120 条主题索引 + 8 篇 write-up 正文）

## 1. 任务与数据

- **对局形式**：宝可梦集换式卡牌 1v1 对战，提交 agent 后由平台持续匹配、按评分排行。
- **三层决策**：**构筑（牌组）→ 出牌策略 → 环境博弈（metagame）**。同一策略面对不同对手分布表现截然不同。
- **与典型 agent 比赛的差异**：卡牌游戏有隐信息（对手手牌/牌库）、随机性大、单局方差高，且**牌组构筑本身就是一个搜索问题**。

## 2. 训练与评估方案

| 环节 | 常见做法 |
| --- | --- |
| 对手池 | 分布式群体自对弈（15th）、population-based PPO（24th） |
| 评估 | 用统一环境测量 agent 之间的对阵矩阵，而不是单一分数 |
| 人类反馈 | 24th 引入专家审查 agent 决策，形成闭环 |
| 冷启动 | 15th 明确**不用行为克隆/人类示范**，从随机初始化开始 |

## 3. 方案谱系

| 方案 | 名次 | 关键点 |
| --- | --- | --- |
| PPO + 3 阶段课程学习 | 27th | 纯 RL，分阶段逐步加难 |
| 7.5M 参数循环 actor-critic + 牌组专家（Slowking / Dragapult） | 15th | 分布式群体自对弈；不同牌组分别训练专家 |
| "宝可梦模式数据库"（受围棋 Waltheri 棋谱检索启发） | 前列 | 从真实对局回放中检索相似局面，用历史统计估计后续动作与结果 |
| 群体式 RL 生态：回放 → GBDT → Transformer 蒸馏 → 群体 PPO → 评估 → 专家反馈 | 24th | 把"持续训练多样 agent + 度量对阵强度"当作系统工程 |

## 4. 关键技巧

- **回放数据是核心资产**：检索相似局面做统计决策（Pattern DB），或用于蒸馏与评估。
- **群体 / 种群训练**：单一自对弈会退化，需要维持多样对手池（与 Orbit Wars 结论一致）。
- **牌组与策略分层**：先固定牌组训策略，再做牌组搜索/专门化。
- **评测体系**：建立 agent 之间的对阵矩阵并持续测量，是选提交的依据。
- **社区工程**：反编译/重建游戏引擎源码是社区级协作（"Game Engine Source Code" 是最高票主题），但**是否合规需要主办方裁定**——这是重要的合规风险提示。

## 5. 可迁移性评估

- **可直接迁移**：
  - "检索相似历史局面 + 统计决策"（Pattern DB 思路）在棋牌类 agent 中通用。
  - 群体自对弈 + 对阵矩阵评估的标准范式。
  - 分层处理"构筑 + 策略"这类组合决策问题。
- **需要前提**：
  - 高质量回放数据（本场由平台提供）。
  - 分布式训练资源；15th 的方案规模（7.5M 参数）相对亲民。
- **不建议照搬**：
  - 依赖反编译引擎的做法有合规风险，需先确认规则授权。
  - 单一牌组专家在 metagame 变化时会失效，需要与环境博弈耦合。

## 6. 对新手的关键启示

1. **agent 比赛的评测体系比模型更重要**：先建立可靠的对阵评估，再谈优化。
2. **随机性大的游戏里，单局结果不可用于决策**，必须看统计。
3. **组合决策问题（如构筑 + 打法）要分层解决**，一次性端到端学习更难。
4. **注意合规边界**：本场关于"反编译引擎"的争论值得记住——技术上可行不等于规则允许。

## 7. 出处

- 讨论区索引：`intel/pokemon-tcg-ai-battle/topics.md`（120 条）
- 已收录 write-up（8 篇）：
  - 24th（39 票）：https://www.kaggle.com/competitions/pokemon-tcg-ai-battle/discussion/740956
  - 15th（44 票）：https://www.kaggle.com/competitions/pokemon-tcg-ai-battle/discussion/739241
  - 27th（32 票）：https://www.kaggle.com/competitions/pokemon-tcg-ai-battle/discussion/738158
  - Team Magist（37 票）：https://www.kaggle.com/competitions/pokemon-tcg-ai-battle/discussion/735593
  - 213tubo（57 票）：https://www.kaggle.com/competitions/pokemon-tcg-ai-battle/discussion/735867
  - 引擎源码与合规讨论（127 / 103 / 29 票）：https://www.kaggle.com/competitions/pokemon-tcg-ai-battle/discussion/717141
