# NFL Big Data Bowl 2023 轻量深读（Tier B）

> 赛事：Community（评审制 analytics）｜ 主题 cv/tracking（NFL 锋线球员评估）｜ 超 400 名参与者 / 近 300 份提交 ｜ 截止 2023-01-09
> 材料基础：`digests/nfl-big-data-bowl-2023.md`（6 篇正文：历届获奖 361175 / finalists 公告 382941 / 官方 demo 360659 / 选题清单 365497 / 官方欢迎 359079 / film review 362714；47 条主题索引）+ 0 张归档图
> 轻读时间：2026-10（Tier B B20）

## 1. 一句话重述与数字账

第五届 BDB，主题是**锋线球员（OL/DL）评估**：用 2021 赛季**第 1–8 周的 dropback pass plays** 追踪数据（snap 到出手）+ PFF 球探数据，讲清楚传球保护/冲传表现。赛道从两条扩到**三条**：Metric、Undergrad、以及新增的 **Coaching**；近 300 份提交、400+ 参与者创纪录，8 名 finalist 在印第安纳 Combine 现场决赛（额外 $20,000 奖金）。本场的高价值材料是**官方 demo（edge rusher get-off）+ 21 票选题清单 + 前两届获奖全名单**，基本把"怎么选题、怎么做图、评委爱看什么"都摊开了。

| 关键数字 | 值 | 来源 |
| --- | --- | --- |
| 规模 | **近 300 份提交 / 400+ 参与者**（analytics 赛记录）；**8 名 finalist**（Coaching 2 / Undergrad 2 / Metric 4）+ 9 个 HM；Combine 现场决赛、额外 **$20,000** 奖金 | 382941 |
| 数据 | 2021 赛季 Weeks 1–8、dropback pass plays；从 snap 到出手的球员追踪（位置/速度/加速度/方向）+ PFF scouting 字段 | 359079 |
| 官方 demo | Tom Bliss 的 edge rusher get-off 分析 notebook：数据探索、play 动画、基础图表——官方强调"这不是提交模板" | 360659 |
| 选题清单（21 票） | 进攻：锋线策略分类（Man Duel/Slide/Empty）、强弱侧判断、跑卫路线 vs 保护、姿势与内外侧、出手后站位、pre-snap→post-snap 保护指派变化、false start/开球时机、主客场 snap count；防守：识别 stunt/twist、pre-snap 冲传概率、吸引包夹的球员、blitz 策略、offside 率、主客场倾向 | 365497 |
| 领域活动 | 与两届超级碗冠军 Kevin Boothe 的 film review；新兵/OL-DL 技术视频与论文清单（14 票）；"linemen and the Matthews family" 故事帖 | 362714 / 359945 / 361504 |
| 争议/口径 | `pff_positionLinedUp` 含义（8 评论）、`pff_passCoverage*` 字段（5 评论）、screen pass 是否排除、frame 长度、周数据缺失、timestamp 修正；"bias concerns" 18 评论与"unfair competition" 公开信 12 评论 | 369849 / 373948 / 364365 / 359781 |
| 提交/规则 | 附录是否计分、GUI applet 是否可行、图像失效、外部/比赛影片可用性；有人遇到"evaluation system not configured" | 375499 / 370682 / 377798 / 376730 |

## 2. 逐方案对照矩阵

| 维度 | Metric 赛道 | Undergrad 赛道 | Coaching 赛道 |
| --- | --- | --- | --- |
| finalist 主题 | STRAIN（sacks/tackles/rushing aggression index）、IDPI 情境化冲传指标、球员影响分布、Completions Added through Pressure Suppression | 压力如何测量（Toronto）、空间生存概率（UChicago） | blitz 策略（使用数据决定）、xPassRush（pre-snap 识别冲传者） |
| 产出 | 新指标 + 验证 | 学术化分析 | 教练可用的战术洞察 |
| 评审口味 | 可解释、可复现的指标 | 方法严谨 | 战术落地性 |

## 3. 共识、分歧与裁决

### 共识一：选题先用"官方素材三件套"（360659 / 365497 / 382941；置信度高）

官方 demo（get-off）给出数据操作与可视化范例；选题清单直接列了 20+ 个可做方向；历届获奖名单给出"什么样的故事能赢"。**裁决**：开局顺序 = 读数据字典 → 复现 demo → 从清单挑一个窄题（某位置 × 某战术）→ 对照往届获奖结构写报告。置信度：高。

### 共识二：三赛道共享数据但评审口味不同（382941；置信度中高）

Metric 要新指标，Coaching 要战术洞察，Undergrad 看学术规范；finalist 题目已验证这一点。**裁决**：先定赛道再定方法——同一份分析，Metric 版强调指标定义与稳健性，Coaching 版强调战术结论与可执行建议。置信度：中高。

### 事件一：PFF 字段口径必须锁死（369849 / 373948 / 364365；置信度中高）

`pff_positionLinedUp`、`pff_passCoverage*`、screen pass 是否排除等被反复提问。**裁决**：所有派生指标先写出"字段 → 官方定义 → 例外"的口径表；不确定的字段不要用于核心结论。置信度：中高。

### 事件二：数据/参与公平性有争议（359200 / 366229 / 460361；置信度中）

"bias concerns"（18 评论）与"不公平竞赛"公开信（12 评论）以及"追踪数据有限"帖说明数据范围（仅 Weeks 1–8）引发部分参与者不满。**裁决**：在报告里显式声明数据范围与局限；这是评审制比赛的加分项而非减分项。置信度：中。

### 事件三：交付细节（附录/交互/图片）需要提前验证（375499 / 370682 / 377798；置信度中）

附录是否计分、能否放 GUI、notebook 图片失效等都被问到。**裁决**：把正文控制在主指标上，交互/动画作为附件并提前渲染验证；提交前在 Kaggle 环境重跑一次。置信度：中。

## 4. 证据分级

| 断言 | 等级 | 说明 |
| --- | --- | --- |
| 规模、赛道、finalist 与奖金 | 官方帖（382941） | 高 |
| 数据范围与主题 | 官方帖（359079） | 高 |
| 官方 demo 与选题清单 | 官方帖（360659 / 365497） | 高 |
| 历届获奖名单 | 社区整理（361175） | 中高（链接可查） |
| PFF 字段问题 | 多帖（369849 等） | 中（答复未归档） |
| 公平性争议 | 讨论帖（359200 / 366229） | 中 |

## 5. 悬案与缺口（登记）

- 2023 获奖作品正文未随归档保存（仅链接与公告）；
- PFF 字段官方答复与 screen pass 口径未归档；
- "bias concerns"/公平性公开信的官方回应未归档；
- 最终 8 名 finalist 的现场排名未归档；
- **图证缺口**：本场 0 张归档图（官方 demo 的 ExamplePlay.gif 未归档），已登记。

## 6. 图表证据

本场 0/0 张归档图，**图证缺口已登记**（官方 demo 的 play 动画为站外/未归档 GIF）。

## 7. 出处

- 官方欢迎（72 票 / 70 评论）：https://www.kaggle.com/competitions/nfl-big-data-bowl-2023/discussion/359079
- finalists 公告（18 票 / 6 评论）：https://www.kaggle.com/competitions/nfl-big-data-bowl-2023/discussion/382941
- 官方 demo notebook（18 票 / 0 评论）：https://www.kaggle.com/competitions/nfl-big-data-bowl-2023/discussion/360659
- 选题清单（21 票 / 0 评论）：https://www.kaggle.com/competitions/nfl-big-data-bowl-2023/discussion/365497
- 历届获奖方案（23 票 / 2 评论）：https://www.kaggle.com/competitions/nfl-big-data-bowl-2023/discussion/361175
- film review（25 票 / 0 评论）：https://www.kaggle.com/competitions/nfl-big-data-bowl-2023/discussion/362714
- NFL/ML 论文清单（14 票 / 6 评论）：https://www.kaggle.com/competitions/nfl-big-data-bowl-2023/discussion/359945
- bias concerns（-1 票 / 18 评论）：https://www.kaggle.com/competitions/nfl-big-data-bowl-2023/discussion/359200
