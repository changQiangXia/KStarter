# Measuring Progress Toward AGI – Cognitive Abilities 轻量深读（Tier B）

> 赛事：Featured（评审制 benchmark 设计赛）｜ 主题 other（AGI 认知评测）｜ 1063 队 / 5 条认知赛道 ｜ 截止 2026-04-16
> 材料基础：`digests/kaggle-measuring-agi.md`（6 篇正文：获奖公布 724918 / 收官 692562 / 投票权重争议 683674 / 提交失败 692560 / 校准 benchmark 683724 / 结果延期 716405；80 条主题索引）+ 1 张归档图
> 轻读时间：2026-10（Tier B B19）

## 1. 一句话重述与数字账

不是做题，而是**设计评测基准**：围绕 5 条认知赛道（Executive Functions / Learning / Metacognition / Social Cognition / Attention）构建 benchmark，由人类评审团选出最能"超越记忆、衡量推理/行动/判断"的作品。奖池 **$200k**（4 个 $25k 大奖 + 10 个 $10k 赛道奖）。本场最大的争议是 rubric 里 **Community upvotes 占 15%**——在一个以"客观评测"为名的比赛里引入社区投票，被 28 票帖直接质疑为 upvote farming；另一条主线是**数据集必须公开**（66 评论的 action-needed 帖）与提交系统故障。

| 关键数字 | 值 | 来源 |
| --- | --- | --- |
| 规模 | **1063 队**、5 条认知赛道、**>1000 份提交**；截止 2026-04-16；人类评审团 | 692562 / 724918 |
| 奖池 | **Grand Prizes $25k × 4**（MEDLEY-BENCH / LearningBench / GAUGE / Metaproteus）+ **Track Prizes $10k × 10**（每赛道 2 个）= **$200k** | 724918 |
| rubric 争议 | Community upvotes **占 15%**（"只算 benchmark 投票、不算 write-up 票"）；质疑帖 28 票 / 5 评论；另有 22 票"Evaluation rubric change"更新 | 683674 / 684184 |
| 评审时长 | 4 月收官（692562，25 票 / 41 评论）→ 组委会再要 1–2 周（716405，23 票 / 12 评论）→ 最终获奖公布（724918，22 票 / 43 评论）；投票争议帖形容"3 小时就有人在刷帖" | 692562 / 716405 / 724918 |
| 提交硬门槛 | "Action needed if your dataset is private" **66 评论**；"Important submission info" 37 评论；"Unable to submit my writeup"、"I missed the submission window"、"没有被评分"等 | 702378 / 689547 / 692560 / 692776 / 741884 |
| 平台生态 | Kaggle Benchmarks SDK + FAQ（682714）；产品反馈 63 评论（681731）；**Task versions** 功能（684183）；Gemma 4 上线 Benchmarks（687230）；本地运行 SDK 讨论（684823） | 索引 |
| 冠军发现样例 | GAUGE：某前沿模型 270 题里**一次都不弃权**（monitoring 有、control 无）；EphLangBench：10 模型 × 200 题的临时语言通过率 **7%–89%**；ABC：15 模型 × 2160 例显示选择性注意非单一能力；Metaproteus：模型对自身输出分布的认知系统性偏差 | 724918 |

## 2. 逐方案对照矩阵

从 14 个获奖 benchmark 归纳的四类设计范式：

| 范式 | 代表 | 设计要点 |
| --- | --- | --- |
| 不确定性与弃权 | GAUGE（监测 vs 控制）、Metacognitive Calibration | 三回合"元认知阶梯"：预测难度 → 作答+置信度 → 弃权/提交（带博弈收益） |
| 全新系统上的学习 | LearningBench、GrammarGym、EphLangBench | 会话内学新规则/程序生成语言，杜绝训练集记忆 |
| 社会压力与社交推理 | MEDLEY-BENCH、HedgeDecode、AdvisorBench | 社会压力下信念更新、含蓄意图、按用户表达水平测建议质量 |
| 注意/执行控制的干扰 | RIAC、ABC、Turn Bench、SecureExec-Bench | 重复干扰 token、结构 vs 特征注意、回合制游戏变体 |

## 3. 共识、分歧与裁决

### 共识一：好 benchmark 要"超越记忆"且能判别（724918；置信度高）

获奖作品全部指向具体失败模式：置信度校准、弃权、会话内学习、注意塌缩、社会压力下的信念更新。**裁决**：设计基准时先写"要暴露的失败模式"，再设计任务与计分；能区分强弱模型（判别力）比题目数量重要。置信度：高。

### 分歧一：社区投票占 15% 是否合理（683674 vs rubric 设计；置信度中高）

质疑者指出 Kaggle 的 upvote farming/互赞圈风险，且本赛讨论区已出现自我推广式回复；rubric 另有"判别力 15%"的社区转述（见截图评论）。**裁决**：若规则含社区分，尽早发布并持续维护 benchmark 页面（曝光=分数），同时用判别力与构造效度自证质量；对"完全客观"不做期待。置信度：中高。

### 事件一：rubric 会中途变更（684184；置信度中）

官方发布"Important Update: Evaluation rubric change"（22 票）。**裁决**：开赛与提交前各读一次规则与 rubric；把评分维度映射到交付清单。置信度：中。

### 事件二：数据集公开+提交物流是硬门槛（702378 / 689547 / 692560 / 692776；置信度中高）

数据集私有需 action，提交说明 37 评论，仍有人无法提交/错过窗口/未评分。**裁决**：提前一周把 dataset 设为 public 并做"陌生账号可见性"检查；提交后截图确认；关注 private→public 的联动要求。置信度：中高。

### 事件三：人工评审周期以月计（692562 / 716405 / 724918；置信度中高）

千人提交逐份评审，结果两度延期。**裁决**：作品保持公开可访问；把结果等待纳入个人计划，不在期间改动 benchmark 版本（避免版本错位）。置信度：中高。

### 事件四：benchmark 生态本身在快速扩张（681731 / 684183 / 687230 / 682518；置信度中）

产品反馈 63 评论、Task versions 功能、Gemma 4 上线、社区自建 MetaTruth/AttentionLens/MIRROR 等并寻求 arXiv endorsement。**裁决**：把参赛 benchmark 当研究资产运营（版本化、公开、可引用），比一次性打榜更符合本赛定位。置信度：中。

## 4. 证据分级

| 断言 | 等级 | 说明 |
| --- | --- | --- |
| 获奖名单、奖池与各作品设计 | 官方帖（724918） | 高 |
| 1063 队、5 赛道、>1000 提交 | 官方帖（692562 / 724918） | 高 |
| 15% 社区投票与 rubric 变更 | 争议帖引述 rubric（683674）+ 官方更新帖标题（684184） | 中高（原文未归档） |
| 数据集公开/提交问题 | 官方与社区帖（702378 / 689547 等） | 中高 |
| 平台功能与生态 | 官方产品帖 + 社区帖 | 中 |
| 截图中的社区建议（跑 8–27 个模型、$50/天预算、判别力 15%） | 帖内截图（683674_img/01） | 中低（社区评论） |

## 5. 悬案与缺口（登记）

- rubric 全文与变更细节未归档（684184 正文缺失）；
- 个人评分与未评分申诉结果未归档（741884）；
- 15% 社区投票是否最终保留/调整无归档结论；
- 获奖 write-up 正文与 benchmark 页面未随归档保存；
- **图证缺口**：无（1 张图，已内嵌）。

## 6. 图表证据

![争议帖引用的社区回复截图](../../intel/kaggle-measuring-agi/bodies/683674_img/01.png)

**图**（topic 683674）：质疑帖附的讨论区截图——两条自称"跑了 14 / 27 个模型"的经验回复，含"更多模型 = 更强判别力（评分 15%）""$50/天预算内可跑""建议跑 8–10 个以上模型"等建议。它同时展示了社区互助与自我推广的边界，是 15% 社区投票争议的直接证据。

## 7. 出处

- 获奖公布（22 票 / 43 评论）：https://www.kaggle.com/competitions/kaggle-measuring-agi/discussion/724918
- 收官说明（25 票 / 41 评论）：https://www.kaggle.com/competitions/kaggle-measuring-agi/discussion/692562
- 社区投票权重质疑（28 票 / 5 评论）：https://www.kaggle.com/competitions/kaggle-measuring-agi/discussion/683674
- rubric 变更（22 票 / 2 评论）：https://www.kaggle.com/competitions/kaggle-measuring-agi/discussion/684184
- 结果延期（23 票 / 12 评论）：https://www.kaggle.com/competitions/kaggle-measuring-agi/discussion/716405
- 数据集私有需处理（10 票 / 66 评论）：https://www.kaggle.com/competitions/kaggle-measuring-agi/discussion/702378
- 提交说明（12 票 / 37 评论）：https://www.kaggle.com/competitions/kaggle-measuring-agi/discussion/689547
- 无法提交 write-up（1 票 / 0 评论）：https://www.kaggle.com/competitions/kaggle-measuring-agi/discussion/692560
- Benchmarks FAQ（8 票 / 7 评论）：https://www.kaggle.com/competitions/kaggle-measuring-agi/discussion/682714
- 产品反馈（7 票 / 63 评论）：https://www.kaggle.com/competitions/kaggle-measuring-agi/discussion/681731
