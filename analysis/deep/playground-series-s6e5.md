# Playground Series S6E5（F1 进站预测）轻量深读（Tier B）

> 赛事：Playground ｜ 主题 tabular（F1 策略二分类）｜ 3022 队 ｜ 标准赛 ｜ 指标：ROC AUC
> 材料基础：`digests/playground-series-s6e5.md`（6 篇正文：1st 703562 / 2nd 703615 / 5th 703572 / 8th 703539 / 4th 703528 / 赛道 EDA 698434；42 条主题索引）+ 2 张归档图
> 轻读时间：2026-10（Tier B B13）

## 1. 一句话重述与数字账

预测 F1 车手下一圈是否进站（PitNextLap，AUC）。本场有两个标志性事实：①**"agent 自主实验"成为现实**——2nd 让 Codex（GPT-5.5）在 4×A100 上自主跑实验/写特征/调参/记录本地排行榜，最终 218 个模型的 logistic 融合以 0.00001 之差屈居第 2；②**名次由"融合与提交选择"决定**——1st 靠最后一分钟提交的"AutoGluon+LR-logits 50-50"混合以 0.00001 取胜，4th 也是靠并入他人集成从第 6 升到第 4。

| 关键数字 | 值 | 来源 |
| --- | --- | --- |
| 1st（703562） | 最后一分钟提交、**以 0.00001 取胜**；186 个 OOF（182 个 L1 + 4 个 L2）；200–400 特征的重型 FE + 大量模型族（XGB/LGBM/CatBoost/RealMLP/TabM/HGB/RF/YDF/FT-Transformer/MLP-PLR…）；突破点 = 对抗 AUC 最高的 `Driver` 变量引发质疑 → **去掉 Driver 的模型 + 部分不用原数据的模型提分**；原数据样本权重 0.25 会掉分（0.5–1 影响不大）；集成器 AutoGluon 最好、LR-logits 紧随；50-50 混合 → 公 0.95488 / **私 0.95503** | 703562 |
| 2nd（703615） | "Autonomous Codex Yolo"：让 Codex 自主循环（生成 FE 想法 → 跑模型 → 记 local_leaderboard.md → 分析 → 下一轮）连续数小时、4×A100 并行；重点提升"六大件"（XGB/CatBoost/LGBM/RealMLP/TabM/TabICLv2）单模 CV，再扩多样性；最终 **218 个模型（37 个类别）** 的 logits → NVIDIA cuML Logistic Regression 融合；无 stacking、无伪标签；最佳单模 RealMLP CV 0.954426（XGB 0.953553 / CatBoost 0.953404 / TabM 0.953371 / LGBM 0.953023）；上午选了私榜 0.95506 的版本、下午换成 0.95502 的保守版 → 输 0.00001 | 703615 |
| 5th（703572） | **99 模型 logit 栈**：每个基模型 OOF 概率转 logit（clip ±30）→ sklearn LR（`class_weight=None`、C=1.0）折内拟合出诚实 OOF，再全量重拟合 ×5 seeds；OOF AUC 0.95536 / log-loss 0.2119 / Brier 0.0660 / 折间 std 0.00081；校准斜率 0.082（过度自信，但 AUC 不受影响）；**多样性量化**：4851 个模型对的平均 Spearman 0.950（Pearson 0.957），LGBM 家族互相 0.965–0.968（部分 >0.998），而 Deep FFM（AUC 0.918，Spearman 0.852）、BART、Nyström、GNN、GRU 最正交、贡献最大；"原数据当额外行"是唯一稳健的 FE 增益 | 703572 |
| 8th（703539） | L5 集成：5/7/10 折三种切分各建 L4 集成 → 简单平均；L1 OOF → L2 meta（logit/rank/统计/两两差/AUC 加权）→ L3 低自由度 LR → L4 自蒸馏学生 → L5 三种切分平均；公 0.95462 / 私 0.95487；明确记录用 GPT-5.5 写码、Gemini 3.1 Pro 讨论思路；承认 CV 偏乐观（未做嵌套 CV） | 703539 |
| 4th（703528） | 只剩 5 天时从 0.95406 重启：小特征集（计数编码 + yekenot 的算术交互 + 少量 pair TE）；XGB CV 0.95378 / 私 0.95346；爬山集成 CV 0.95529；最后并入 mikhailnaumov 的集成 → 公 0.95471 / 私 0.95490（否则第 6） | 703528 |
| EDA（698434） | 用 `RaceProgress` 把 PitNextLap 目标率画到各赛道的"赛道头像"上——不同赛道/位置的进站率差异显著（Monaco 0.3574 vs Canada 0.1539） | 698434 |
| 社区 | 轮胎配方变化（43 票）；原始数据不一致（31 票）；"数据说不通"（12 票）；逐年 PitNextLap 分布不一致（8 票）；"stacking stacked predictions"（11 票） | 索引 |

## 2. 逐方案对照矩阵

| 维度 | 1st | 2nd | 5th | 8th | 4th |
| --- | --- | --- | --- | --- | --- |
| 基模型规模 | 186 OOF | **218 模型 / 37 类** | 99 模型 | 3×L4（123/11/13 OOF） | 少量自训 + 公开 OOF |
| 融合器 | AutoGluon + LR-logits 50-50 | cuML Logistic（logits） | sklearn LR（logits, C=1） | L2→L3 LR→L4 蒸馏→L5 平均 | Hill Climbing |
| 原数据用法 | 部分模型不用；权重 0.5–1 最佳 | 作为多样性来源之一 | 额外行（唯一稳健增益） | 行/列两种策略 × 三种切分 | 计数/TE 派生 |
| 关键洞察 | Driver 对抗性 → 去掉提分 | Agent 自主迭代 | 正交弱模型 > 重复强模型 | 多切分多样性 | 5 天冲刺可进前 4 |
| 私榜 | **0.95503**（1st） | 0.95502（2nd） | — | 0.95487 | 0.95490 |

## 3. 共识、分歧与裁决

### 共识一：大规模 OOF 池 + 线性 logit 融合是本场主流（1st/2nd/5th/8th；置信度高）

四支队伍分别用 186/218/99/多种规模 OOF，融合器全部选择 LR/Ridge/linear logit 或 AutoGluon+线性；5th 明确 AUC 下 `class_weight=None`、不做校准/后处理。**裁决**：高相关模型池用低自由度线性融合最稳，非线性 meta 只会放大过拟合。置信度：高。

### 共识二：多样性来自"正交的弱者"（5th 的量化分析、8th 的多切分；置信度高）

5th 测得平均 Spearman 0.950，LGBM 家族互相 0.965–0.968（部分 >0.998）；而 0.918 AUC 的 Deep FFM、BART、Nyström、GNN、GRU 才是真正贡献增量方向；8th 用不同折数制造多样性。**裁决**：当模型池高度相关时，边际价值来自尾部正交模型与不同验证切分，而不是再堆一个强 GBDT。置信度：高。

### 事件一：Agent 自主实验成为可复现工作流（2nd、1st、8th；置信度中高）

2nd 完整描述了 Codex 自主循环（含 local_leaderboard.md、4×A100 并行、数小时无人值守）；1st 用 Claude、8th 用 GPT-5.5/Gemini。同时 1st 也记录了必须人工纠正的失败模式：过早放弃、整本 notebook 重写导致配额被锁。**裁决**：2026 年的高效工作流是"agent 跑实验、人管方向与选择"；需要给 agent 设定可检查的中间产物与预算约束。置信度：中高（自述）。

### 事件二：提交选择与数据伪影（1st、2nd、4th、696380；置信度中高）

冠亚军差距 0.00001，胜负手都是"选哪份提交"；4th 靠并入他人集成从第 6 变第 4；1st 通过逐变量对抗 AUC 发现 Driver 是原数据伪影并剔除。**裁决**：当分数饱和时，提交选择 + 原数据逐列审计与建模同等重要。置信度：中高。

### 分歧：原数据到底怎么用（1st vs 5th vs 8th；置信度中）

1st 发现去掉 Driver、控制原数据权重更优；5th 说"原数据当额外行"是唯一稳健增益；8th 用行/列两种策略 × 多种切分。**裁决**：原数据不是二元选择，需按变量做对抗验证、按"行/列/权重"做消融；本场 Driver 是特殊异常点。置信度：中。

## 4. 证据分级

| 断言 | 等级 | 说明 |
| --- | --- | --- |
| 2nd 的 218 模型表与 agent 工作流 | 自述 + 完整模型表 + 流程图 | 中高 |
| 5th 的 99 模型栈与相关性统计 | 自述（含 OOF 诊断与系数分析） | 高 |
| 1st 的最终融合与 Driver 发现 | 自述 | 中高 |
| 8th 的 L5 结构与分数 | 自述 | 中 |
| 4th 的 5 天冲刺与借力 | 自述 | 中 |
| 赛道 EDA | 图 + 交互式 notebook | 中高 |

## 5. 悬案与缺口（登记）

- 3rd/6th/7th/9th 等方案未细读（7th 有 write-up 未收录全文）；
- 原始数据不一致（696380）与逐年 PitNextLap 分布（696769）的成因未细读；
- agent 工作流的 token/算力成本未量化；
- **图证缺口**：无（2 张图已内嵌）。

## 6. 图表证据

![各赛道 PitNextLap 目标率](../../intel/playground-series-s6e5/bodies/698434_img/01.png)

**图 1**（topic 698434，54 票）：把 PitNextLap 目标率画到 RaceProgress 赛道头像上——Monaco（0.3574）与加拿大（0.1539）等赛道差异显著，是"赛道×位置"特征的 EDA 依据。

![Agent 迭代循环](../../intel/playground-series-s6e5/bodies/703615_img/01.png)

**图 2**（topic 703615，2nd）：LLM Agent 循环——生成新特征工程想法 → 跑模型 → 根据结果生成新想法；2nd 用 Codex 在 4×A100 上无人值守连续迭代。

## 7. 出处

- 1st（54 票 / 33 评论）：https://www.kaggle.com/competitions/playground-series-s6e5/discussion/703562
- 2nd Autonomous Codex（36 票 / 26 评论）：https://www.kaggle.com/competitions/playground-series-s6e5/discussion/703615
- 5th 99 模型 logit 栈（15 票）：https://www.kaggle.com/competitions/playground-series-s6e5/discussion/703572
- 8th L5 集成（10 票）：https://www.kaggle.com/competitions/playground-series-s6e5/discussion/703539
- 4th 5 天冲刺（22 票）：https://www.kaggle.com/competitions/playground-series-s6e5/discussion/703528
- 赛道 EDA（54 票）：https://www.kaggle.com/competitions/playground-series-s6e5/discussion/698434
- 轮胎配方（43 票）：https://www.kaggle.com/competitions/playground-series-s6e5/discussion/696012
- 原数据不一致（31 票）：https://www.kaggle.com/competitions/playground-series-s6e5/discussion/696380
- Rank17（18 票）：https://www.kaggle.com/competitions/playground-series-s6e5/discussion/703529
- Stacking stacked predictions（11 票）：https://www.kaggle.com/competitions/playground-series-s6e5/discussion/703542
