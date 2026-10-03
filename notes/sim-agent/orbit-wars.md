# Orbit Wars

> 主题：sim-agent ｜ 子类：— ｜ 领域：游戏 ｜ 类别：Featured
> 截止：2026-07-07 ｜ 队伍数：4729 ｜ 机制：标准赛（提交 agent）｜ 指标：orbit_wars（对战评分）
> 数据来源：`intel/orbit-wars/`（120 条主题索引 + 10 篇 write-up 正文 = **8 篇独立**，含 2 对同作者重发；另有 5th–11th 等约 20 条 write-up 未收录）

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
| 环境 | 重写为 JAX / C++ / Rust（全员；2nd 从 Rust→C 移植配合 PufferLib，8×H100 达 40K SPS） |
| 自我对弈 | PPO 自对弈为基底；4p 必须联赛/PFSP 防退化（13th：准入 70%/池≤30；Jake：低胜率组合平方加权） |
| 联盟（league） | 与历史版本/多样对手对战，防止过拟合当前自身策略 |
| 冷启动 | IL 只作脚手架：13th 随机初始化在 10–20k update 反超 warm start；2nd 赛前 5 天从零反超 IL |
| 推理期搜索 | 2–3 步 rollout；13th 双 ckpt merge（2p 100 局 0.71 vs 0.29）；FLG 2p +30~40 分；**4p 搜索存疑** |

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

## 5. 深读结论（2026-10 补）

- **效率前沿**：1st 用 2400 B200h（200M 参数/15B 步）夺冠，13th 用 ~$630、约 200 B200h（1.2M 参数/22.8B samples）拿 rank 13——参数差 167×、算力差约 12×，最终只差 12 名；归纳偏置与算力可互换，但换算比非线性。
- **折叠表示是主流最优**：多数方案把在飞舰队折叠进行星未来态（被动 rollout / 到达桶 / 时间序列 / combat preview）；13th 给出无损性论证与 horizon 边界（最坏 140 回合、常见 20–30 回合到达）。
- **语义动作 > 数值动作**：3rd 换语义动作后学习明显加速；simjeg 砍到 all-in-only 得第 2；FLG 实测多比例档零增益——让引擎算"多少船/什么角度"，策略只答"打哪、为什么"。
- **熵是第一训练旋钮**：3rd 的 4p 首跑 ent 0.05 导致"行星完全停止发射"，0.02 修复；其调度 0.05→~0.0005。lightmk 附件给出前兆信号：clip_frac 0.10→0.30+ 先于熵崩溃。
- **已决局是训练算力黑洞**：Jake 投降机制砍 60–70% 回合、FLG 早停省 ~18% 回合；1st 因 γ=1.0 学会拖局（浪费训练算力）；13th resign 试验致稳赢局崩溃而弃用——早停收益大但有策略崩溃风险。
- **评测非平稳（本场最大不确定性）**：评测期 rank 6–28 摆动（top 10 时间占比 24.2%）；2p/4p 能力完全脱钩（Jake 2p 71% vs 4p 19%；Isaiah 2p 89% vs 4p 28%）；merge 本地强，但评测期 2p/4p 结论相反。

## 6. 图表证据

**图 1：13th OrbitNet 全图**（topic 723731）——`../../intel/orbit-wars/bodies/723731_img/05.jpg`

![OrbitNet](../../intel/orbit-wars/bodies/723731_img/05.jpg)

*读图*：CNN 7→16→32→64 过 50 回合 + [mean‖max‖attn] 池化；FiLM 公式 `feat=(1+γ)·feat+β`；边特征 P×P×6 → MLP 6→32→4 作逐头注意力偏置、6→16→1 作指针偏置；fraction 头 [src‖tgt‖global]=384→256→2。右栏为 2p→4p 全部维度变化。

**图 2：参数/FLOPs 分解**（topic 723731）——`../../intel/orbit-wars/bodies/723731_img/06.png`

![model profile](../../intel/orbit-wars/bodies/723731_img/06.png)

*读图*：1.17M 参数 / 144.9M FLOPs（P=32）；主干占参数 67.8% 但 FLOPs 仅 38.3%，**50 回合预测序列吃掉约 48% FLOPs**（forecast CNN 29.6%+池化 18.7%）——13th 自己承认"CNN 可能不值"。

**图 3：merge vs greedy 本地评测**（topic 723731）——`../../intel/orbit-wars/bodies/723731_img/10.png`

![final eval](../../intel/orbit-wars/bodies/723731_img/10.png)

*读图*：2p 100 局 merge 0.71 vs greedy 0.29；4p 各 80 局 0.31 vs 0.12（公平份额 0.25）。

**图 4：评测期全场 2p/4p 分化**（topic 723731）——`../../intel/orbit-wars/bodies/723731_img/12.png`

![eval field](../../intel/orbit-wars/bodies/723731_img/12.png)

*读图*：Isaiah 2p 89%/87%、4p 28%；Jake Will 2p 71%/68%、4p 19%/22%；TonyK 2p 41%、4p 44%——同一 agent 的两种强度。

**图 5：2nd 的 all-in 极简管线**（topic 723728）——`../../intel/orbit-wars/bodies/723728_img/02.png`

![simjeg architecture](../../intel/orbit-wars/bodies/723728_img/02.png)

*读图*：每体 20×10 时间序列 → 4×残差块（Conv1D k=5 d=128）→ GAP → 128→256；ModernBERT XXS（7 层/4 头/d256/全局注意力）→ launch 头 + target 头；两种掩码（非己方不可发；20 回合内不可达不可选）。

**图 6：3rd 熵调度曲线**（topic 723820）——`../../intel/orbit-wars/bodies/723820_img/03.png`

![entropy schedule](../../intel/orbit-wars/bodies/723820_img/03.png)

*读图*：0.05 保持到 500M 步，随后指数衰减（1.5B≈0.011、2B≈0.006、3B≈0.002），3.5B 后进入 ~0.0005 平台。

## 7. 可迁移性评估

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

## 8. 对新手的关键启示

1. **agent 类比赛的胜负手是"训练环境 + 动作空间设计"**，不是网络层数。
2. **算力和归纳偏置可以互换**：没有大算力就用领域知识补。
3. **先做启发式系统再决定是否上 RL**——13th 正是从启发式里发现了推理速度瓶颈，才转向 RL。
4. **自我对弈必须有对手多样性机制**，否则策略会退化并被针对。

## 9. 出处

- 讨论区索引：`intel/orbit-wars/topics.md`（120 条）
- 已收录 write-up（10 篇 = 8 篇独立）：
  - 1st（150 票 / 90 票两个版本）：https://www.kaggle.com/competitions/orbit-wars/discussion/714324 ｜ https://www.kaggle.com/competitions/orbit-wars/discussion/724268
  - 2nd（98 票 / 90 票两个版本）：https://www.kaggle.com/competitions/orbit-wars/discussion/713276 ｜ https://www.kaggle.com/competitions/orbit-wars/discussion/723728
  - 3rd（31 票，"Ab in den Orbit"）：https://www.kaggle.com/competitions/orbit-wars/discussion/723820
  - Jake Will（38 票）：https://www.kaggle.com/competitions/orbit-wars/discussion/723325
  - FLG 方案（38 票）：https://www.kaggle.com/competitions/orbit-wars/discussion/713519
  - 13th（38 票，Luca）：https://www.kaggle.com/competitions/orbit-wars/discussion/723731
  - Evoformer 思路（40 票）：https://www.kaggle.com/competitions/orbit-wars/discussion/713126
  - RL 经验分享（126 票）：https://www.kaggle.com/competitions/orbit-wars/discussion/697725
- 未收录缺口（登记备查）：8th `723739`、7th `728348`、5th `727619`、9th `727595`、10th `727854`、11th `727715`、`714276`、`714226` 等
- 深读全文：`analysis/deep/orbit-wars.md`
