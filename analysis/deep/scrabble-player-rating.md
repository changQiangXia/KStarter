# Scrabble Player Rating 轻量深读（Tier B）

> 赛事：Playground ｜ 主题 tabular（玩家评分回归，RMSE）｜ 301 队 ｜ 标准赛 ｜ 截止 2022-12-15
> 材料基础：`digests/scrabble-player-rating.md`（6 篇正文：赛后复盘 372554 / 公开 kernel 清单 362744 / 官方欢迎 362735 / RMSE 资源 362749 / 评分系统提问 363404 / FE+AGG 数据集 363143；12 条主题索引）+ 0 张归档图
> 轻读时间：2026-10（Tier B B21 收官）

## 1. 一句话重述与数字账

用 woogles.io 上的对局数据预测**人类玩家评分**（RMSE）：场景是"你在熟悉联赛里认识这些玩家与他们的评分，现在去另一个联赛观察同一批 bot 对局，能猜出人类玩家评分吗"。数据的关键结构是**同一玩家的全部历史只出现在 train 或 test 之一**——这直接决定了验证方案：赛后复盘者发现普通 KFold 偏乐观，改用按昵称的 GroupKFold 后分数显著变差，而 StratifiedGroupKFold（按 time_control/rating_mode/lexicon 分层）改善有限。主 FE 是**玩家历史聚合**（此前各局分数的 min/max/mean）+ 回合特征，模型是 LightGBM + Optuna。

| 关键数字 | 值 | 来源 |
| --- | --- | --- |
| 规模与任务 | **301 队**；RMSE；woogles.io 人类 vs 3 bot 对局；这是作者第二个 woogles 数据赛（前作预测"下一手得分"） | 362735 |
| 主 FE（赛后复盘） | 玩家历史聚合：此前各局得分的 **min/max/mean** + 回合特征；**LightGBM + Optuna** 调参；notebook 公开 | 372554 |
| CV 核心问题 | 数据中同一玩家的历史**整体落在 train 或 test**；作者从 KFold 改 **GroupKFold（nickname 分组）** 后分数"substantially worse"；**StratifiedGroupKFold**（time_control_name × rating_mode × lexicon）改善不大 | 372554 |
| 公开基线 | 社区 kernel：mpwolke 的 turn 分析、mrisdal 的 basicbot 数据分析、**metlover 的 CNN/ANN（Flux.jl）17.24339 RMSE**、mathurinache starter、toadofsky omgwords starter | 362744 |
| 现成特征数据 | 社区发布"Advanced Dataset, FE+AGG"（含 `difficult_word` 等新特征，加速建模） | 363143 |
| 讨论区体量 | 仅 **12 条主题**：赛后复盘、kernel 清单、RMSE 资源、游戏介绍、提交错误、词表获取（0 票 / 2 评论）等 | 索引 |

## 2. 逐方案对照矩阵

| 维度 | 赛后复盘者（372554） | 公开 starter 线 |
| --- | --- | --- |
| 特征 | 玩家历史 min/max/mean + 回合特征 | turn 分析、basicbot 数据、word 特征 |
| 模型 | LightGBM + Optuna | CNN/ANN（Flux.jl）等 |
| 验证 | KFold → GroupKFold(nickname) | 多为 KFold |
| 分数参考 | 未给最终分 | 17.24339 RMSE（单 notebook） |

## 3. 共识、分歧与裁决

### 共识一：按 nickname 分组才是诚实 CV（372554 + 数据切分设定；置信度中高）

同一玩家的历史整体落在 train 或 test，普通 KFold 会让"同一玩家"跨折出现，特征（历史统计）与目标的关联被高估；GroupKFold 分数更低但更接近真实泛化。**裁决**：默认用 GroupKFold(nickname)；把 KFold 分数视为乐观上界；任何"玩家级"特征都要在分组 CV 下评估。置信度：中高（逻辑与作者实验一致，但作者本人仍在求确认）。

### 事件一：玩家历史聚合是最主要的信息来源（372554 / 363143；置信度中高）

min/max/mean 历史分数等聚合特征与 `difficult_word` 类新特征都指向"把玩家行为压缩成稳定画像"。**裁决**：围绕"玩家是谁、稳定水平、波动"设计特征（分位数、趋势、对手强度），而不是只堆单局特征。置信度：中高。

### 事件二：本场公开复盘极少，学习价值有限（12 条主题；置信度中）

只有一位选手详细复盘 CV 问题，没有 top-10 write-up。**裁决**：把本场当"分组 CV 案例"学习；要复现前列方案需要自行读公开 notebook。置信度：中。

### 分歧：Rating 系统能否直接预测胜负（363404 vs 本题设定；置信度低）

有选手问用 rating 预测胜负（Shogi 场景），但本赛的目标是**没有 rating 的新玩家**，rating 恰是需要预测的量。**裁决**：不要用目标泄漏变量（rating）作特征；用行为特征重建评分。置信度：中（逻辑明确）。

### 事件三：外部资源与词表边界需确认（363660 / 362749；置信度低）

有帖问能否拿到词表（Scrabble 词典）以及 RMSE 解释资源。**裁决**：lexicon 相关外部资源先确认规则允许范围；RMSE 类基础资源只用于汇报口径。置信度：低—中。

## 4. 证据分级

| 断言 | 等级 | 说明 |
| --- | --- | --- |
| 任务设定与数据来源 | 官方欢迎帖（362735） | 高 |
| 玩家历史聚合 + LightGBM/Optuna | 赛后复盘（372554） | 中高 |
| GroupKFold 与分数差异 | 自述（372554） | 中（个人实验，未给数字） |
| starter 17.24339 RMSE | 社区 kernel 清单（362744） | 中低（单一 notebook） |
| FE+AGG 数据集 | 社区帖（363143） | 中 |
| 词表/外部资源 | 提问帖（363660） | 低 |

## 5. 悬案与缺口（登记）

- 最终高分方案未归档，GroupKFold 下各队分数不可比；
- 作者对"整玩家切分是否正确"的疑问没有归档结论；
- 词表能否使用、外部数据的边界未归档；
- 本场没有 top-10 write-up；
- **图证缺口**：本场 0 张归档图，已登记。

## 6. 图表证据

本场 0/0 张归档图，**图证缺口已登记**。

## 7. 出处

- 赛后复盘与 CV 问题（3 票 / 2 评论）：https://www.kaggle.com/competitions/scrabble-player-rating/discussion/372554
- 公开 kernel 清单（9 票 / 1 评论）：https://www.kaggle.com/competitions/scrabble-player-rating/discussion/362744
- 官方欢迎（16 票 / 3 评论）：https://www.kaggle.com/competitions/scrabble-player-rating/discussion/362735
- RMSE 资源（6 票 / 2 评论）：https://www.kaggle.com/competitions/scrabble-player-rating/discussion/362749
- FE+AGG 数据集（10 票 / 3 评论）：https://www.kaggle.com/competitions/scrabble-player-rating/discussion/363143
- 词表问题（0 票 / 2 评论）：https://www.kaggle.com/competitions/scrabble-player-rating/discussion/363660
