# Lux AI Season 3

> 主题：sim-agent ｜ 子类：— ｜ 领域：游戏 ｜ 类别：Featured
> 截止：2025-XX-XX ｜ 队伍数：1000+ ｜ 机制：标准赛（提交 agent）｜ 指标：对战胜率
> 数据来源：`intel/lux-ai-season-3/`（80 条主题索引 + 6 篇 write-up 正文）

## 1. 任务与数据

- 对局形式：多单位、多玩家的策略对抗（每方 16 个单位，需要同时管理移动与"吸取/攻击"等动作）。
- 与 S1/S2 的差异：**单位数量多、动作空间大**，对多智能体建模与动作头设计要求更高。
- 构造陷阱：动作空间组合爆炸；奖励稀疏；每回合计算预算受限。

## 2. 方案谱系

| 方案 | 名次 | 关键点 |
| --- | --- | --- |
| 多智能体 RL（IMPALA + 动态奖励缩放 + 自适应熵） | 1st | **动作空间被显式拆成两个头**：头一决定"移动 or 吸取"，头二决定吸取目标；强调动作空间设计是核心贡献 |
| 模仿学习（Imitation Learning） | 3rd | 用模仿学习替代纯 RL 训练（另一条主流路线） |
| Rust + 深度 RL | Frog Parade | 作者明确说明"我无法用 Jax 写出无 bug 且高效的特征工程"，因此**改用 Rust** |
| 模仿学习方案 | 4th | 同上路线 |
| 多智能体 RL | 14th（银牌） | 见讨论区 |

## 3. 关键技巧

- **动作空间的分解（多头设计）**：先决定动作类型，再决定目标——显著降低学习难度（1st 的核心）。
- **训练算法**：IMPALA + 动态奖励缩放 + 自适应熵调节。
- **语言/框架选择服务于个人效率**：Frog Parade 选 Rust 而非 Jax，理由是"能写出无 bug 的高效特征工程"（工具选择要看可控性）。
- **模仿学习与 RL 并列可行**（3rd/4th 均为模仿学习）。

## 4. 可迁移性评估

- **可直接迁移**：
  - **动作空间的多头分解**是 agent 类比赛最通用的设计技巧（Orbit Wars 的语义动作同理）；
  - 动态奖励缩放/自适应熵等训练稳定性技巧；
  - 工具链选择以"我能掌控"为准，而非跟风。
- 需要前提：RL 训练基础设施与大量对局算力。
- 不建议照搬：直接端到端输出联合动作。

## 5. 对新手的关键启示

1. **agent 比赛的核心设计是"动作空间"**（本场三家不约而同地强调它）。
2. **模仿学习与 RL 同样可行**，选熟悉的路线更实际。
3. **工具选择服务于效率与正确性**（Rust vs Jax 的取舍值得体会）。

## 6. 轻读结论（2026-10 补）

**一句话**：部分可观测的多智能体对抗——**RL 自对弈（1st，20B 步）vs 从顶级回放做 IL（3rd/4th/9th）**两条路线；隐藏参数估计与"防模仿"的提交博弈是隐形战场。

- 1st（74 票）：IMPALA+动态奖励缩放+动态熵（0.9/3.9→0，100M 步）+教师 KL+冻结对手池；~1000+/tile 特征、24 resblock+ConvLSTM+4 Transformer、双动作头（6 动作/15×15 sap）；**85/15 双模型 + 日志 + logits 噪声**防 IL 抄策略。
- 3rd（57 票）：规则系被 IL 数小时训练击败 → 全面转 IL（Unit-UNet+SAP-UNet、丢 95% 全 Center 样本、镜像 (0,0)、学习 FP/FN 回放）。
- 9th：两阶段 IL（FP 7,935 局仅胜局 → 1,550 局胜负都用）+ 最小费用流分配动作。
- 4th：Action/SapTarget 双 IL 模型；估计 sap dropoff 后**切换模型**。

**裁决**：可观测参数估计是硬前提；镜像归一化是标准工程；IL 是最快追赶路径，RL 靠规模与防模仿维持上限。

**悬案**：Frog Parade 方案未细读；防模仿收益未受控量化；logits 噪声参数未公开。

## 7. 图表证据

![1st 的网络结构](../../intel/lux-ai-season-3/bodies/569562_img/01.png)

**图 1**（topic 569562）：输入→两级压缩→24×24×128→24 残差块→ConvLSTM→4 Transformer→基线/预测/动作头（6 动作+sap 目标）。

## 8. 出处

- 讨论区索引：`intel/lux-ai-season-3/topics.md`（80 条）
- 已收录 write-up（6 篇）：
  - 1st Flat Neurons（74 票）：https://www.kaggle.com/competitions/lux-ai-season-3/discussion/569562
  - 3rd 模仿学习（57 票）：https://www.kaggle.com/competitions/lux-ai-season-3/discussion/568494
  - Frog Parade（53 票）：https://www.kaggle.com/competitions/lux-ai-season-3/discussion/568621
  - 4th 模仿学习（36 票）：https://www.kaggle.com/competitions/lux-ai-season-3/discussion/569928
  - 14th 多智能体 RL（33 票）：https://www.kaggle.com/competitions/lux-ai-season-3/discussion/567961
- 轻读全本：`analysis/deep/lux-ai-season-3.md`（Tier B 轻读：对照矩阵/裁决/证据分级/悬案 + 1 图证）
