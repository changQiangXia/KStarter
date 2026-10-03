# AI Agent Security - Multi-Step Tool Attacks

> 主题：nlp ｜ 子类：agent-safety ｜ 领域：AI 安全 ｜ 类别：Featured
> 截止：2026-09-01 ｜ 队伍数：4186 ｜ 机制：代码赛 ｜ 指标：Agents Security Metric
> 数据来源：`intel/ai-agent-security-multi-step-tool-attacks/`（120 条主题索引 + 8 篇 write-up 正文）

## 1. 任务与数据

- **任务形式**：在确定性离线沙箱中对带工具的 AI agent 做红队攻击。提交物是 `attack.py`，实现 `AttackAlgorithm`：向被攻击 agent 发提示、观察其工具调用，返回可重放候选。
- **评分结构（本场核心）**：
  - 两个目标模型依次被攻击：GPT-OSS 20B 与 Gemma（llama.cpp + T4）；
  - 每个攻击同时跑两套护栏：**公开的 OptimalGuardrail**（源码在 SDK 里）与**从未公开的私有护栏**；
  - 排行榜因此有四行（两个模型 × 公开/私有），**一半分数建立在看不见的评分器上**。
- **与常规比赛的差异**：攻击要经过重放验证，不可重放的"侥幸成功"会被判 0 分。

## 2. 验证方案

| 方案 | 使用者 | 说明 |
| --- | --- | --- |
| 本地重放沙箱 | 社区共识 | 官方提供的 `Validate Your Attack Locally` 工具，提交前先本地重放 |
| 公开护栏精确测量 + 私有护栏买保险 | 11th | "能测的测准，测不到的用对冲"：提交两个 notebook，一个冲吞吐、一个保守求稳 |
| 排行榜探针（probe） | 1st | 通过探针推断私有护栏的判定行为 |

**本场的血泪教训**：7th place 的公开分 123.73 → **私榜 0.000**，原因是攻击无法迁移；最终靠一个"公开看起来弱"的方案（34.63 / 34.51）拿到奖牌。

## 3. 方案谱系

| 方案 | 名次 | 关键点 |
| --- | --- | --- |
| 改造 GCG，去掉每次成功工具调用后的"第二跳"开销 | 1st | 先探针确认 Confused Deputy 是唯一可靠路径，再用吞吐量优势取胜 |
| 优化单一 `email.send` 攻击路径 | 4th | 把最简攻击做到极致 |
| 拥抱"迁移性"而非公开分 | 7th | 结论：**公开分高不等于能迁移**，情绪上很难否定一条已经"跑通"的路线 |
| 双 notebook 对冲（吞吐型 + 保守型） | 11th | 私榜取两者较优 |
| 系统梳理沙箱与四行评分结构 | 10th | 把"不可见评分器"的不确定性显式建模 |

## 4. 关键技巧

- **攻击路径的可靠性 > 单次成功率**：私榜重放决定成败，不能迁移的攻击等于 0。
- **吞吐量也是竞争力**：1st 只是去掉了每次成功调用后的额外一跳，就拿到冠军——因为评分对可重放的攻击次数敏感。
- **探针（LB probing）在"隐藏评分器"场景里是正规手段**：本题它不是作弊，而是理解评分机制的合理途径（与 ICR 那类比赛的探针风险不同）。
- **对冲式提交**：当一半分数不可见时，用"一个冲分 + 一个求稳"的组合代替"押注单点最优"。
- **编码 agent 的双刃剑**：7th 反思——agent 会以极高速度沿着一条已跑通的路线做局部优化，让人更难意识到"这条路线本身是错的"。

## 5. 可迁移性评估

- **可直接迁移**：
  - "**能测的测准，测不到的买保险**"——任何存在隐藏评测集的比赛都适用。
  - 提交前做本地重放验证；对不可重放的结果不抱幻想。
  - 当评分对调用次数/吞吐敏感时，减少无效开销就是提分手段。
  - 对 AI 编码 agent 的使用要保持"路线怀疑"：它的局部优化速度会掩盖全局错误。
- **需要前提**：
  - 攻击类比赛需要理解目标模型与护栏的交互机制，门槛较高。
  - 探针策略依赖排行榜可探测（部分比赛禁止或惩罚）。
- **不建议照搬**：
  - 只追求公开分而忽略迁移性（本场已给出 0 分的极端案例）。

## 6. 对新手的关键启示

1. **先弄清评分机制**，再决定优化方向；本题"一半分数不可见"直接决定了策略。
2. **高分不等于有效**：无法迁移/重放的结果是零收益。
3. **用组合对冲不确定性**，而不是押注单一最优解。
4. 这是目前少见的"安全 × agent"交叉赛道，值得作为了解 agent 评测与护栏机制的入口。

## 7. 出处

- 讨论区索引：`intel/ai-agent-security-multi-step-tool-attacks/topics.md`（120 条）
- 已收录 write-up（8 篇）：
  - 1st（82 票）：https://www.kaggle.com/competitions/ai-agent-security-multi-step-tool-attacks/discussion/739181
  - 4th（27 票）：https://www.kaggle.com/competitions/ai-agent-security-multi-step-tool-attacks/discussion/739040
  - 7th（22 票）：https://www.kaggle.com/competitions/ai-agent-security-multi-step-tool-attacks/discussion/738981
  - 10th（12 票）：https://www.kaggle.com/competitions/ai-agent-security-multi-step-tool-attacks/discussion/738946
  - 11th（15 票）：https://www.kaggle.com/competitions/ai-agent-security-multi-step-tool-attacks/discussion/739322
  - 59th / 工作笔记：https://www.kaggle.com/competitions/ai-agent-security-multi-step-tool-attacks/discussion/738890
