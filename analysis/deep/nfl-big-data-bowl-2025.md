# NFL Big Data Bowl 2025 轻量深读（Tier B）

> 赛事：Community（评审制 analytics）｜ 主题 cv/tracking（NFL pre-snap 分析）｜ 无排行榜 ｜ 截止 2025-01-06
> 材料基础：`digests/nfl-big-data-bowl-2025.md`（6 篇正文：上手资源 539795 / 历届方案 539785 / 官方欢迎与建议 539921 / 直播 539775 / 赛季数据疑问 539822 / 获奖公布 560137；72 条主题索引）+ 0 张归档图
> 轻读时间：2026-10（Tier B B19 收官）

## 1. 一句话重述与数字账

第七届 Big Data Bowl，主题是 **pre-snap（开球前）**：用追踪 + 事件数据研究开球前的阵型、运动/换位（motion/shift）、audible 等如何预示开球后的结果。官方建议非常直接：**别试图一次解决整个橄榄球**——选一个小切口（一个位置/一类战术/一种阵型）做深；足球语境 + 编码能力的组合最容易出成果。本场数据比 2024 版**新增 66 个特征、删除 7 个特征**，讨论区大量问题围绕 `line_set`/`motionSinceLineset`/`inMotionAtBallSnap` 等新事件口径；另有"notebook spam"与提交格式/字数限制等社区摩擦。

| 关键数字 | 值 | 来源 |
| --- | --- | --- |
| 赛制 | 第七届年度赛；pre-snap 主题；无排行榜/评审制；获奖名单以附件公布；截止 2025-01-06 | 539921 / 560137 |
| 官方三建议 | ① 保持简单，选小切口（位置/战术/体系）② 足球语境越多越好 ③ 有足球背景的人 + 会编码的人组队成功率更高 | 539921 |
| 数据变化 | 2025 vs 2024：**新增 66 个特征、删除 7 个**；unique seasons 仍是 2022（数据滞后问题被专帖吐槽） | 539787 / 539822 |
| 新手口径问题 | `line_set` 事件（7 评论）；motionSinceLineset vs inMotionAtBallSnap（多帖）；pre-snap adjustments/audibles；passers other than QB；PFF 数据问题；球员朝向测量；absoluteYardlineNumber >100；WinProbabilityAdded；负 expectedPoints | 541143 / 548627 / 541223 / 543658 / 541889 / 552655 / 548437 / 552417 / 541000 |
| 数据质量 | football tracking inaccuracies；"Where is the football in this play?"；data disagreement between inputs；plays.csv issue；missing birthdays 修正；特勤组识别口径 | 551782 / 551328 / 543709 / 543119 / 546315 / 542111 |
| 社区摩擦 | "Notebook spam is unreal"（8 票 / 9 评论）；"Ideally it's useless"（4 票 / 7 评论）；现场直播/连麦复盘；青少年参赛资格；coaching track 提交格式 8 评论；2000 词附录是否计入 | 540670 / 552318 / 539775 / 541080 / 548189 / 555070 |
| 结果 | 赛后"提交评审中"（6 票 / 8 评论）→ 获奖公布（9 票 / 8 评论）；Feedback on Submissions 3 票 | 555499 / 560137 / 568911 |

## 2. 逐方案对照矩阵

| 维度 | 官方建议路线 | 社区上手动线 | 数据现实 |
| --- | --- | --- | --- |
| 选题 | 一个位置/战术/体系做深 | 复用往届 EDA/动画 notebook | pre-snap 新事件口径不熟 |
| 交付 | 2000 词 + 图表/动画，评审可读 | notebook 直接改写成报告 | 格式/字数规则细节多 |
| 价值 | 足球语境 + 编码结合 | 追踪可视化/派生指标 | 球轨迹与部分事件不可靠 |

## 3. 共识、分歧与裁决

### 共识一：小切口 + 足球语境是评审制 BDB 的长期制胜法（539921；置信度高）

官方明确"别一次解决整个运动"，并强调足球背景与编码能力的组合。**裁决**：选题限定到"某位置在某类阵型下的某一步运动"，用领域假设驱动指标设计；报告按"问题—证据—结论—对球队的建议"组织。置信度：高。

### 事件一：新特征/新事件口径是本届主场（539787 / 541143 / 548627 / 541223；置信度中高）

66 个新特征 + pre-snap 事件（line-set、motion、audible）需要先做数据字典与口径统一，否则派生特征会错。**裁决**：先写"事件时间线"（line_set → ball_snap 等）并可视化验证，再建运动/阵型特征。置信度：中高。

### 事件二：追踪数据质量仍需审计（551782 / 551328 / 543709 / 543119；置信度中高）

球的位置/轨迹不准、输入数据互相矛盾、plays.csv 有问题被逐帖报告。**裁决**：任何涉及球位置/速度的结论先做一致性抽检；必要时以事件数据为准而不是球轨迹。置信度：中高。

### 事件三：提交格式与赛道规则是常见淘汰点（548189 / 555070 / 555197 / 555366；置信度中高）

coaching track 的图表/幻灯片规则、2000 词附录计法、提交失败等被反复询问。**裁决**：把"格式合规"当独立 checklist；提前用草稿提交验证流程，别在截止前两小时试。置信度：中高。

### 分歧：公开 notebook 的价值与噪声（540670 / 554993 / 552318；置信度中）

有人抱怨 notebook spam 与低质公开作品，也有人做"最有竞争力 notebook"盘点与直播复盘。**裁决**：以数据问题与领域假设为筛选标准，不追热度；公开作品用于对照口径而非直接套用。置信度：中。

## 4. 证据分级

| 断言 | 等级 | 说明 |
| --- | --- | --- |
| 官方三建议与赛制 | 官方帖（539921） | 高 |
| 66 新增 / 7 删除特征 | 社区对比帖（539787） | 中高（可核对） |
| 新事件口径问题 | 多帖（541143 / 548627 等） | 中高 |
| 数据质量个案 | 多帖（551782 / 551328 等） | 中 |
| 获奖方案 | 仅公告附件（560137） | 低（正文未归档） |
| 社区摩擦 | 讨论帖（540670 / 552318） | 中 |

## 5. 悬案与缺口（登记）

- 获奖作品正文与最终评审细节未归档（560137 只有附件公告）；
- 66 个新特征的官方文档更新说明未归档；
- 球追踪不准确的官方结论/修复未归档；
- 各赛道（metric/undergrad/coaching）的评审权重未公开；
- **图证缺口**：本场 0 张归档图，已登记。

## 6. 图表证据

本场 0/0 张归档图，**图证缺口已登记**。

## 7. 出处

- 官方欢迎与建议（17 票 / 17 评论）：https://www.kaggle.com/competitions/nfl-big-data-bowl-2025/discussion/539921
- 上手资源汇编（22 票 / 6 评论）：https://www.kaggle.com/competitions/nfl-big-data-bowl-2025/discussion/539795
- 历届方案索引（9 票 / 1 评论）：https://www.kaggle.com/competitions/nfl-big-data-bowl-2025/discussion/539785
- 2025 vs 2024 特征变化（6 票 / 0 评论）：https://www.kaggle.com/competitions/nfl-big-data-bowl-2025/discussion/539787
- 赛季数据疑问（14 票 / 2 评论）：https://www.kaggle.com/competitions/nfl-big-data-bowl-2025/discussion/539822
- notebook spam（8 票 / 9 评论）：https://www.kaggle.com/competitions/nfl-big-data-bowl-2025/discussion/540670
- coaching track 提交格式（0 票 / 8 评论）：https://www.kaggle.com/competitions/nfl-big-data-bowl-2025/discussion/548189
- 获奖公布（9 票 / 8 评论）：https://www.kaggle.com/competitions/nfl-big-data-bowl-2025/discussion/560137
