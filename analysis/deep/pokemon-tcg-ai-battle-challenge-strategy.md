# Pokémon TCG AI Battle Challenge – Strategy Category 轻量深读（Tier B）

> 赛事：Featured（评审制 write-up 赛道）｜ 主题 sim-agent（宝可梦 TCG 对战 agent）｜ 939 队 / **942 份 write-up** ｜ 截止 2026-09-13
> 材料基础：`digests/pokemon-tcg-ai-battle-challenge-strategy.md`（6 篇正文：获奖与评审说明 742692 / 迟交资格求助 735276 / 官方欢迎 708588 / 字数与牌表规则 733067 / 发布位置 738911 / 格式问题 709452；47 条主题索引）+ 0 张归档图
> 轻读时间：2026-10（Tier B B18）

## 1. 一句话重述与数字账

与 Simulation 赛道（**6807 队**打 ELO）配套的 **Strategy 赛道**：提交 agent 的解法 write-up（**942 份**），按 **Model / Deck / Report** 三项评审。这篇官方评审复盘是 Tier B 里少见的"评审标准直白版"：**最强 write-up 要给出"观察 → 改动 → 验证"的完整闭环、可见的消融对比、失败路径、牌组意图与关键卡作用、少而精的图表**；只报最终结果、只堆牌表、分析停在诊断的稿件拿不到高分。另有贯穿赛程的资格摩擦：Simulation 报名截止（2026-08-09）早于 Strategy，多支队伍完成 write-up 却无法进入 Simulation。

| 关键数字 | 值 | 来源 |
| --- | --- | --- |
| 规模 | Simulation **6807 队**；Strategy **942 份 write-up**；Top 20 授奖、**Top 8 晋级第二轮**（YouTube 直播） | 742692 |
| 评审机制 | 按规则公布的 **Model / Deck / Report** 三项；评委先独立打分，再集中讨论最强稿件；考虑**最终 ELO + 稳定性 + 原创性 + 决策理由**；**不公开个人分数与分项明细** | 742692 |
| 高分特征（官方总结） | ① 用自建评测（self-play arena、对冻结对手的联赛、固定对手评测集）驱动迭代，并说清"分析后改了什么"② 展示组件贡献（通用 vs 专用策略、有/无搜索、两副牌对比、rating/胜率随时间）③ 讨论失败的尝试（端到端组牌、联赛训练、value-based MCTS、look-ahead search、critic reranking）④ 讲清牌组整体计划与关键卡角色（不必逐张解释 60 张）⑤ 少而精的图表（rating 曲线、对位胜率、管线图） | 742692 |
| 低分模式 | 分析停在诊断（没说改了什么）；只看到最终结果（看不出组件贡献与演化）；牌表没有战略意图 | 742692 |
| 资格摩擦 | Simulation 报名截止 **2026-08-09 23:59 UTC**；多帖反映 write-up 完成后无法进入 Simulation（735276 / 734869 / 735402 / 735996 / 740873 / 741226），有 Simulation 排名 3471 的队伍全员进不了 Strategy 赛道 | 735276 等 |
| 提交规则争议 | write-up **2000 词上限**（正文/附录/图注如何计数）；"Pokémon Elements"含牌表数据，§3.11(b) 限制公开分享——自晒牌表是否合规被反复追问 | 733067 / 738657 / 735679 |
| 平台摩擦 | 草稿被 "ssssssadasfsd" 覆盖 bug、已提交 write-up 无法删除（forumMessages.update 权限）、组队 bug、两份 EN 卡表 218 张不一致（含未翻译日文）、卡库 bug + 先手 deck-out 偏差（对随机基线 92% 胜率） | 739855 / 740949 / 730277 / 734057 / 736918 |

## 2. 逐方案对照矩阵

官方给出的高分/低分稿件对照：

| 维度 | 高分写法 | 低分写法 |
| --- | --- | --- |
| 迭代闭环 | 观察 → 改动 → 验证（自建 arena/固定评测集） | 只有诊断，没有后续改动 |
| 组件贡献 | 消融/对比（搜索 vs 无搜索、两副牌） | 只报最终模型+最终分 |
| 失败路径 | 简述试过但放弃的方案 | 完全不提 |
| 牌组 | 讲整体计划与关键卡角色 | 只贴 60 张牌表 |
| 图表 | 少量关键图（rating/对位/管线） | 无图或堆图 |

## 3. 共识、分歧与裁决

### 共识一：评审要的是"可验证的改进循环"，不是最终分数（742692；置信度高）

官方逐条点出：强稿件用自建评测环境驱动迭代，弱稿件停在诊断。**裁决**：写作时以"问题 → 假设 → 改动 → 评测 → 是否保留"为主线组织，每个数字对应一次改动。置信度：高。

### 共识二：消融与失败路径显著提高可读性与评分（742692；置信度高）

官方明确"不需要大规模消融，去掉一个组件的一次对比就够"，并点名端到端组牌、value-based MCTS 等失败尝试值得写。**裁决**：保留实验日志，至少写 1 个消融 + 1 个失败方案。置信度：高。

### 共识三：牌组评审看"意图"，不看清单完整度（742692；置信度高）

官方原文：不必解释全部 60 张，关键是整体 game plan 与关键卡（如 Dragapult 针对特定对局线）的作用。**裁决**：Deck 部分按"计划 → 关键卡 → 对位调整"写，附牌表即可。置信度：高。

### 事件一：两条赛道的报名截止错位造成系统性资格风险（735276 / 734869 / 735996 / 741226；置信度中高）

多队完成 Strategy 作品却因 Simulation 报名截止（8/9）无法满足"必须参加 Simulation"的要求；官方获奖帖未逐一回应这些边缘案例。**裁决**：双赛道比赛第一天就把两条都报名锁定；把 entry deadline 写进计划表。置信度：中高。

### 事件二：提交平台与素材合规的摩擦不可忽视（739855 / 740949 / 733067 / 734057；置信度中）

草稿覆盖 bug、无法删除已提交稿件、牌表公开的规则模糊、两份官方卡表数据不一致。**裁决**：本地保存终稿备份；提交流程留 48h 缓冲；涉及 IP 的素材（牌表图、卡图）先行确认或改为文字描述。置信度：中。

### 分歧：赛道设计（Strategy 是否必须绑定 Simulation）（738058 / 740873；置信度中）

规则 2.1.c 与 3.5.d 被反复引用质疑；官方复盘未展开资格裁决逻辑。**裁决**：按保守解读准备（两赛道都参加并保留凭证），并把疑问在早期发帖确认。置信度：中。

## 4. 证据分级

| 断言 | 等级 | 说明 |
| --- | --- | --- |
| 评分维度与高分/低分特征 | 官方帖（742692） | 高 |
| Top 20 / Top 8 与 6807 / 942 规模数字 | 官方帖（742692） | 高 |
| 资格截止与无法参赛案例 | 多帖 + 官方元数据引用（735276 等） | 中高 |
| 2000 词与牌表分享争议 | 选手提问（733067 / 738657） | 中（官方答复未归档） |
| 平台 bug 与卡表数据问题 | 单帖（739855 / 734057 / 736918） | 中低 |

## 5. 悬案与缺口（登记）

- 获奖 write-up 正文未归档；官方明确不公开分项评分；
- 迟报名/资格争议的最终处理结果未归档（735276 / 740873 等无后续）；
- 2000 词与"Pokémon Elements"牌表公开规则无官方答复记录；
- 卡表 218 张差异与卡库 bug 的影响范围未定论；
- **图证缺口**：本场 0 张归档图（官方强调的 rating/对位图均在获奖稿件内，未归档），已登记。

## 6. 图表证据

本场 0/0 张归档图，**图证缺口已登记**；社区"Show us your final ELO rollercoaster graphs"（742226）可见图表文化，但图片未随归档保存。

## 7. 出处

- 获奖与评审说明（19 票 / 6 评论）：https://www.kaggle.com/competitions/pokemon-tcg-ai-battle-challenge-strategy/discussion/742692
- 官方欢迎（25 票 / 6 评论）：https://www.kaggle.com/competitions/pokemon-tcg-ai-battle-challenge-strategy/discussion/708588
- 迟报名资格求助（6 票 / 3 评论）：https://www.kaggle.com/competitions/pokemon-tcg-ai-battle-challenge-strategy/discussion/735276
- 字数与牌表规则（3 票 / 0 评论）：https://www.kaggle.com/competitions/pokemon-tcg-ai-battle-challenge-strategy/discussion/733067
- write-up 格式（4 票 / 0 评论）：https://www.kaggle.com/competitions/pokemon-tcg-ai-battle-challenge-strategy/discussion/709452
- 发布位置（2 票 / 1 评论）：https://www.kaggle.com/competitions/pokemon-tcg-ai-battle-challenge-strategy/discussion/738911
- 已完成提交被草稿覆盖（-1 票）：https://www.kaggle.com/competitions/pokemon-tcg-ai-battle-challenge-strategy/discussion/739855
- 两份 EN 卡表 218 张不一致：https://www.kaggle.com/competitions/pokemon-tcg-ai-battle-challenge-strategy/discussion/734057
- 卡库 bug 与先手偏差：https://www.kaggle.com/competitions/pokemon-tcg-ai-battle-challenge-strategy/discussion/736918
- Strategy-only 能否获奖（-2 票 / 8 评论）：https://www.kaggle.com/competitions/pokemon-tcg-ai-battle-challenge-strategy/discussion/738058
