# Orbit Wars

> 主题：sim-agent ｜ 子类：— ｜ 领域：游戏 ｜ 类别：Featured
> 截止：2026-07-07 ｜ 队伍数：4729 ｜ 机制：标准赛（提交 agent）｜ 指标：orbit_wars（对战评分）
> 数据来源：`intel/orbit-wars/`（120 条主题索引 + 8 篇 write-up 正文）

## 1. 任务与数据

- **对局形式**：2 人或 4 人实时策略对战。玩家从起始行星发射飞船占领新星球，星球持续产船，终局按飞船总数（或消灭对手）判定胜负。
- **提交物**：一个 agent（代码），平台持续与其他 agent 对战更新技能分。
- **与常规比赛的根本差异**：
  - 没有静态测试集，**评分来自持续对局**，提交后分数仍会漂移。
  - 对手是其他参赛者的 agent，策略存在"石头剪刀布"式的相互克制。
  - 推理时间是硬约束：单位回合内的计算预算决定了可用方法。

## 2. 训练与评估方案

| 环节 | 常见做法 |
| --- | --- |
| 环境 | 重写为 JAX / C++ 以加速（3rd、FLG 都做了） |
| 自我对弈 | PPO + PFSP（优先虚构自对弈）避免策略退化 |
| 联盟（league） | 与历史版本/多样对手对战，防止过拟合当前自身策略 |
| 冷启动 | 模仿学习（2nd：行为克隆进前十）或纯自对弈（1st、3rd） |
| 推理期搜索 | 2–3 步 rollout 搜索，FLG 报告 2 人局 +30~40 分 |

## 3. 方案谱系

| 方案 | 名次 | 关键点 |
| --- | --- | --- |
| 200M 参数 transformer + 150 亿步纯自对弈 RL | 1st | 刻意**最小化领域工程**，赌"Bitter Lesson"；全程由 AI 编码代理写代码 |
| ModernBERT + 1D-CNN 嵌入 | 2nd | 路径：启发式（前 50）→ 模仿学习（前 10）→ RL 微调（前 5）→ 从零 RL |
| 纯自对弈 RL（PPO + PFSP）+ JAX 环境，6.2M 参数 transformer | 3rd | "可达性张量"（任意两星球间不同规模舰队的到达时间）几乎和模型本身一样费工 |
| Evoformer 风格的节点/边消息传递 | 上榜 | 生物学背景作者把蛋白质折叠的归纳偏置迁移过来；**不把飞行中的舰队当作一等对象**，而视为"未来事件" |
| RL + 联赛 + 短程 rollout 搜索 + 自定义边注意力 | 上榜 | C++ 环境 + pybind 特征工程；先训小模型（稠密辅助奖励）再迁移到大 transformer |
| 单星球 token 的 1.2M 参数 transformer | 13th（solo 金） | 先做启发式，因**推理速度**（每回合需数秒物理计算）转向 RL |

## 4. 关键技巧

- **动作表示**：用语义动作（hold / sortie / kill-at-arrival）替代连续的兵力比例（3rd）；舰队规模档位（100% / 50%）等设计影响巨大。
- **架构**：以"行星 = 节点、行星对 = 边"的关系型注意力为主流；绝对坐标与玩家 id 通常去掉（相对化）。
- **熵调度（entropy schedule）**：3rd 明确称其为"最重要的训练旋钮"。
- **推理速度决定路线**：多个团队因为启发式方案的物理计算太慢而转向神经网络策略。
- **算力量级差异巨大**：冠军用 200M 参数 × 150 亿步，季军用 6.2M 参数 + JAX 重写环境——**两者都上领奖台**，说明归纳偏置与算力可以互相替代。
- **联赛/多样性**：单靠自我对弈会退化，需要历史版本或多样对手池。

## 5. 可迁移性评估

- **可直接迁移**：
  - "**推理预算决定方法选择**"这一判断在 agent 类比赛中普遍成立。
  - 关系型建模（节点 + 边）适用于任何实体交互场景。
  - 先小模型 + 稠密奖励，再迁移到大模型（FLG 的课程式训练）。
  - 联盟训练 / 对手池是自对弈防退化的标准手段。
- **需要前提**：
  - 环境重写（JAX/C++）需要工程能力与时间，是上榜的常见门槛。
  - 冠军路线依赖大规模算力（150 亿步自对弈）。
  - 短程 rollout 搜索的收益（+30~40 分）依赖游戏可精确前向模拟。
- **不建议照搬**：
  - 直接复刻 200M 参数方案：没有相应算力时，小而精的架构 + 强归纳偏置更实际。
  - 把绝对坐标/身份特征带进模型（会造成泛化问题）。

## 6. 对新手的关键启示

1. **agent 类比赛的胜负手是"训练环境 + 动作空间设计"**，不是网络层数。
2. **算力和归纳偏置可以互换**：没有大算力就用领域知识补。
3. **先做启发式系统再决定是否上 RL**——13th 正是从启发式里发现了推理速度瓶颈，才转向 RL。
4. **自我对弈必须有对手多样性机制**，否则策略会退化并被针对。

## 7. 出处

- 讨论区索引：`intel/orbit-wars/topics.md`（120 条）
- 已收录 write-up（8 篇）：
  - 1st（150 票 / 90 票两个版本）：https://www.kaggle.com/competitions/orbit-wars/discussion/714324 ｜ https://www.kaggle.com/competitions/orbit-wars/discussion/724268
  - 2nd（90 票）：https://www.kaggle.com/competitions/orbit-wars/discussion/723728
  - 3rd（31 票，"Ab in den Orbit"）：https://www.kaggle.com/competitions/orbit-wars/discussion/723820
  - FLG 方案（38 票）：https://www.kaggle.com/competitions/orbit-wars/discussion/713519
  - 13th（38 票）：https://www.kaggle.com/competitions/orbit-wars/discussion/723731
  - Evoformer 思路（40 票）：https://www.kaggle.com/competitions/orbit-wars/discussion/713126
  - RL 经验分享（126 票）：https://www.kaggle.com/competitions/orbit-wars/discussion/697725
