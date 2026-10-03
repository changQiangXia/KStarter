# Pokemon TCG AI Battle Challenge - Strategy Category（精简）

> 主题：sim-agent ｜ 子类：— ｜ 领域：游戏 ｜ 类别：Featured ｜ 截止：2026-09-13 ｜ 队伍数：939 ｜ 指标：评审制（write-up）
> 出处：`intel/pokemon-tcg-ai-battle-challenge-strategy/`（80 条主题索引 + 6 篇 write-up 正文）

## 任务

这是同一届 Pokémon TCG 挑战赛的 **Strategy 赛道**：模拟赛（6807 队）比 agent 强度，Strategy 赛道则**提交解法 write-up 由评审**（942 份），两条赛道的排名独立。

## 关键要点

- 主办方评价：**许多 write-up 的深度达到研究论文水平**，且不只是分享成功经验，也分享了失败路径。
- 对新手而言，这类"策略赛道"是理解 agent 比赛设计（环境、动作空间、对手池、评测体系）的最佳读物——因为作者被迫把思路讲清楚。
- 与模拟赛道对照：同一比赛的两条赛道分别奖励"打得赢"和"讲得清"。

## 可迁移要点

- **写清楚方案本身就是一种能力**（也是 Kaggle 社群文化的核心）。
- 评审制赛道适合系统学习思路：优先读 Strategy 类 write-up，而不是只看分数。

## 轻读结论（2026-10 补）

- **规模**：Simulation 6807 队 vs Strategy 942 份 write-up；Top 20 授奖、Top 8 晋级第二轮（742692）。
- **高分标准（官方复盘原文级）**：① 自建评测（self-play arena/冻结对手联赛/固定评测集）驱动"观察→改动→验证"闭环；② 组件消融对比（通用 vs 专用策略、搜索有无、两副牌）；③ 写失败路径（端到端组牌、value-based MCTS、look-ahead search 等）；④ 牌组讲意图与关键卡（不必逐张）；⑤ 少而精的图表（rating 曲线/对位胜率/管线图）。只报最终结果、只贴牌表、分析停在诊断 = 低分（742692）。
- **资格摩擦**：Simulation 报名 2026-08-09 截止早于 Strategy，多队写完无法满足"必须参加 Simulation"；有 Simulation 排名 3471 的队伍全员进不了 Strategy（735276 等）。**双赛道比赛第一天就要两条都报名。**
- **规则/平台坑**：2000 词计数范围、牌表公开与 §3.11(b) "Pokémon Elements" 冲突、草稿被乱码覆盖、已提交稿件无法删除、两份 EN 卡表 218 张不一致（733067 / 739855 / 734057）。

## 图表证据

本场 0 张归档图（0/0），**图证缺口已登记**（官方强调的 rating/对位图都在获奖稿件内，未归档）。

## 出处

- 讨论区索引：`intel/pokemon-tcg-ai-battle-challenge-strategy/topics.md`
- 获奖公布与评审说明：https://www.kaggle.com/competitions/pokemon-tcg-ai-battle-challenge-strategy/discussion/742692
- 官方欢迎：https://www.kaggle.com/competitions/pokemon-tcg-ai-battle-challenge-strategy/discussion/708588
- 字数与牌表规则：https://www.kaggle.com/competitions/pokemon-tcg-ai-battle-challenge-strategy/discussion/733067
- 迟报名资格求助：https://www.kaggle.com/competitions/pokemon-tcg-ai-battle-challenge-strategy/discussion/735276
- 草稿覆盖 bug：https://www.kaggle.com/competitions/pokemon-tcg-ai-battle-challenge-strategy/discussion/739855
