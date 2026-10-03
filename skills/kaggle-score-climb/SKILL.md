---
name: kaggle-score-climb
description: Score-first Kaggle leaderboard climbing — decide which experiments actually add rank, exploit metric structure with legal postprocessing, reconcile CV with public/private LB, hedge shakeups, and protect the final submission. Use when the objective is improving a Kaggle score or rank; pair with an execution/plumbing skill for Kaggle CLI, GPU offload, and notebook pipelines.
---

# Kaggle Score Climb（上分决策层）

## 目标与边界

- 唯一目标：在比赛规则允许的范围内，最大化**最终（private）排行榜名次**；public LB 只是测量工具，不是目标。
- 本 skill 负责**决策层**：指标结构、验证可信度、实验排序、合法后处理、提交组合、收官保护、分差管理。
- 执行层（Kaggle CLI、GPU/TPU offload、producer/consumer notebook、提交重跑与日志）交给执行型 skill（如 `agentic-kaggle-skill`）；两者配合使用，本 skill 决定"打什么、先打什么、何时停"。
- **规则优先**：任何泄漏、探榜、外部数据或提交套利动作前先确认比赛规则；不合规的分数不算分数。

## 0. 先建"分数模型"（每场必做，30 分钟内）

1. **指标数学结构**：中位数型 / 排序型 / 阈值型 / 容差型 / 回归型 / 对局型（见 `references/metric-arbitrage.md`）。
2. **榜单结构**：public/private 切分比例、每日提交次数、medal/prize cutoff、历史 shakeup 幅度。
3. **得分分解**：分数由哪些样本/行为决定——中位数那一个样本、头部少数类、阈值附近、长尾、还是全程排序。
4. **分差管理**：离下一个名次/奖牌还差多少；这个差距是真实信号还是榜单噪声。
5. **输出**：一页 score model，写进 experiments ledger（`assets/experiment_ledger_template.csv`）。

## 1. 上分阶梯（按 expected gain / hour 排序）

1. **修验证**：CV 与 LB 同向、无实体/时间泄漏、指标实现口径正确 —— 最大且最便宜的一步。
2. **指标结构后处理**：clip / 校准 / 档位 / 分布形态 / 阈值 / 秩变换 —— 常常是 0.001–0.1 量级。
3. **数据红利**：重复/结构/生成痕迹/OOD/原始数据 —— 合法前提下收益大，先做规则确认。
4. **强单模与多样性**：跨家族模型、embedding+GBDT、域内预训练权重。
5. **集成/栈**：只在 OOF 证明有增量时；低信号目标上集成会过拟合。
6. **调参与长尾**：先过种子稳定性检验；低信号场次设"够了就停"预算。
7. **提交策略与收官**：组合对冲、冻结协议、格式保护（见 `references/submission-portfolio.md`）。

## 2. 五条硬规则

1. **验证不可信时，一切模型结论作废**：先修验证，再谈模型。
2. **public LB 是带噪测量**：用样本量判断它的信息量；不做"LB 微差选模"。
3. **任何技巧必须过同折对照**：没有对照的增益按 0 计。
4. **每次实验只改一个东西**：记录 CV/LB/成本/决策，形成可复用的分数账本。
5. **最后 48 小时不引入新方法**：只做选择、对冲与格式保护。

## 3. 快速决策

| 信号 | 动作 |
| --- | --- |
| CV 与 LB 方向不一致 | 先查实体/时间泄漏与指标口径；读 `references/validation-to-lb.md` |
| 排行榜分数扎堆（如 0.25 聚集、26.38–26.41） | 停止 LB 调参；回到指标结构与 OOF 选择 |
| 公榜高、私榜崩（shakeup） | 改提交组合对冲；读 `references/submission-portfolio.md` |
| 指标是 MedAE/分位/容差型 | 先做样本权重与分布整形，再谈模型 |
| 指标是 top-K/AUC/NDCG | 优先排序与校准不变融合，追加预测可能白赚 |
| 大家的分差不多、公开方案饱和 | 找差分：数据、后处理、验证口径（`references/public-intel-differential.md`） |
| 时间不够 | 按上分阶梯从 1→7 只做前两步能做的 |

## 4. 资源路由

- 指标结构、套利与合法后处理 → `references/metric-arbitrage.md`
- 验证设计、CV↔LB 关系、探榜纪律 → `references/validation-to-lb.md`
- 实验排序、期望收益、台账与 kill 标准 → `references/score-gain-ladder.md`
- 提交预算、shakeup 对冲、收官冻结 → `references/submission-portfolio.md`
- 公开 notebook/讨论区差分挖掘 → `references/public-intel-differential.md`
- 跨场顶层规律速查（60 条） → `references/top-rules.md`
- 赛前 40 项故障预检 → `references/failure-preflight.md`
- 按赛型打法（表格/CV/NLP/时序/Agent/评审/研究） → `references/archetypes.md`
- 提交 CSV 体检 → `scripts/submission_guard.py`
- 实验台账模板 → `assets/experiment_ledger_template.csv`
- 收官清单（可复制） → `assets/endgame_checklist.md`

## 5. Definition of Done

- 每个得分动作都有台账行：假设 / 改动 / ΔCV / ΔLB / 成本 / 决策。
- 最终提交通过 `submission_guard.py` 与 `assets/endgame_checklist.md`。
- 记录：最终 public/private、选择依据、未选提交与原因、剩余风险、赛后复盘。
- 如果无法继续上分：明确写出"下一步最高期望实验"与阻塞条件，而不是停在"模型已训练"。

## 6. 汇报节奏

- 每个实验一行：`改动 → ΔCV / ΔLB → 决策（保留/回退/再加一轮）`。
- 每轮：更新分数模型 + 列出下一轮 3 个最高期望实验。
- 收官：候选提交表（分数 / CV / 风险 / 是否选）与最终选择理由。
