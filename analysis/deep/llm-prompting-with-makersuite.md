# LLM Prompting with MakerSuite 轻量深读（Tier B）

> 赛事：Community（提示词工程设计赛，评审制）｜ 主题 other（LLM prompting）｜ 200+ 份提交 ｜ 无排行榜 ｜ 截止 2023-11-06
> 材料基础：`digests/llm-prompting-with-makersuite.md`（6 篇正文：游戏/模拟赛巡礼 451608 / 获奖公布 457016 / 资源合集 447223 / MakerSuite 地区限制 446465 / BIPOC 机会 446695 / 玩笑 write-up 447146；38 条主题索引）+ 2 张归档图
> 轻读时间：2026-10（Tier B B17）

## 1. 一句话重述与数字账

Google × Kaggle 的**提示词设计赛**：用 MakerSuite（后并入 Google AI Studio）为 LLM 写文本/数据/对话 prompt，按 7 个应用类别评审。归档材料给出的可迁移结论非常集中：**"system prompt 定角色 + 多组 input/output 示例"是让输出稳定的最小范式**；教育类获奖者进一步用 **JSON（题目+答案矩阵+示例答案）**让生成可自动判分。另一个现实教训是：**硬性可及性（地区/年龄）是参赛第一门槛**，社区大量讨论巴西、欧洲无法访问 MakerSuite。

| 关键数字 | 值 | 来源 |
| --- | --- | --- |
| 评审规模 | 官方评估 **200+ 份提交**，选出 **7 个类别各 1 名获奖**（Developer Tools / Data Science Tools / Education & Interactive Tutors / Utilities for Everyday Life / Well Explained Reasoning / Storytelling & Interactive Games / Other Ideas）；获奖 prompt 承诺收入 MakerSuite Prompt Gallery | 457016 |
| 获奖范式 | 开发工具类 @ajaysadhu：**system prompt + 多组"乱格式输入→规范 YAML 输出"示例**，多次测试证明稳定；教育类 @hoangpham51：输出 **JSON + answer matrix + 示例答案**，换输入即可生成新题 | 457016 |
| 可及性约束 | MakerSuite 有**地区限制**（巴西、欧洲等不可用）与 **18+ 年龄要求**；巴西选手帖子获 17 票 / 12 评论，欧洲帖 7 票 | 446465 / 446473 |
| 讨论区规模 | 38 条主题；置顶 Q&A 23 评论（446450）；资源合集 18 票（447223）；"prompt marketplace"建议 7 票（447012） | 索引 |
| 无排行榜 | 队伍数 0、无公开分数；选手问"能拿到我的评分吗"（447125）、"什么时候出结果"（455618）——评审制社区赛的透明度和长周期 | 索引 |
| 社区副产物 | MPWolke 的"Kaggle 游戏/模拟赛巡礼"长帖（ConnectX / Halite / Kore / Lux AI / AI Village CTF 等，14 票）成为错位选题的示范：MakerSuite 不可用时改讲"agent vs agent" | 451608 |

## 2. 逐方案对照矩阵

按 7 个类别冠军归纳的 prompt 模式：

| 类别 | 获奖者 | 提示词模式 | 复现要点 |
| --- | --- | --- | --- |
| Developer Tools | @ajaysadhu | system prompt + 多组 YAML 修复示例 | 少样本对 + 多次稳定性测试 |
| Data Science Tools | @elanderos | 概念解释 + 代码示例 | 面向学习者的答疑结构 |
| Education & Interactive Tutors | @hoangpham51 | JSON（题目 + answer matrix + 示例答案） | 输出可机读、可换输入复用 |
| Utilities for Everyday Life | @ankushmandal | 销售/客服通话摘要 | 指定"为什么感兴趣/不感兴趣"的结构化解释 |
| Well Explained Reasoning | @abprime5 | 评估想法强度 + 优缺点 + 替代方案 | 把模型当头脑风暴伙伴 |
| Storytelling & Interactive Games | @mvoulo | 给世界名 → 生成 D&D 战役 | 输入槽位固定、输出多分支 |
| Other Ideas | @dineshctech | 逆境自助手册（描述困境+人群 → 行动清单+资源） | 双输入 + 行动导向输出 |

## 3. 共识、分歧与裁决

### 共识一：system prompt + few-shot 示例是可控输出的最小可靠范式（457016 全 7 例 + 447223 资源；置信度高）

开发工具冠军明确以"系统提示 + 多组输入/输出对"稳定 YAML 修复；其余类别也都把角色/格式写进指令层。**裁决**：任何 LLM 结构化改写任务，先固定角色与输出格式，再用 2–5 组示例锚定行为；示例质量优先于措辞技巧。置信度：高。

### 共识二：让输出可机读/可判分是评审友好设计（457016 教育类 + 447223 资源；置信度中高）

教育类要求 JSON 中含答案矩阵与示例答案，换输入即可批量出新题。**裁决**：评审制比赛里把"评审成本"设计进产物（JSON、rubric、示例），既方便打分也方便他人复用。置信度：中高。

### 事件一：可及性是第一门槛，不是技能（446465 / 446473；置信度中高）

MakerSuite 地区限制与 18+ 要求直接劝退巴西/欧洲选手，讨论热度高于多数技术帖。**裁决**：参加平台工具类比赛前先验证账号、地区、年龄合规；把"访问截图 + 替代路径"写进计划（如用可用工具完成同题演示）。置信度：中高。

### 事件二：类别化评审 = 选题策略的一等变量（457016 七类；置信度中）

同一套"角色+示例"写法套进答疑导师、通话摘要、头脑风暴、跑团生成等 7 个壳体，各自都能出奖。**裁决**：评审制 prompt 赛优先挑"有真实小痛点 + 评审能看懂价值"的类别，而不是堆技巧。置信度：中。

### 分歧：评审透明度（447125 / 455618 vs 官方承诺赛后公开 Gallery；置信度中）

选手询问个人评分与结果时间未获公开答复；官方只承诺赛后把获奖 prompt 收入 Gallery。**裁决**：社区评审赛把"公开可复用产物"当交付标准，参赛时按"作品会被公开引用"来写文档与命名。置信度：中。

## 4. 证据分级

| 断言 | 等级 | 说明 |
| --- | --- | --- |
| 200+ 提交、7 类别获奖与评语 | 官方帖（457016） | 高 |
| 获奖 prompt 的具体结构 | 官方评语（457016，无 prompt 原文） | 中高 |
| 地区/年龄限制 | 截图 + 选手反馈（446465；官方页面文案） | 高 |
| 资源与课程清单 | 社区合集（447223） | 中 |
| 游戏/模拟赛巡礼 | MPWolke 长帖（451608） | 低—中（社区史料，非本赛结论） |
| 评审透明度问题 | 选手提问（447125 / 455618） | 低—中 |

## 5. 悬案与缺口（登记）

- 获奖 prompt 原文未随归档保存（官方称将补进 Prompt Gallery，归档时链接未更新）；
- 个人评分与排名永不公开，无法复核评审一致性；
- 447146 "Kaggle solution write-up" 是复制 sample_submission 的玩笑帖，不构成方案证据；
- 2 张归档图中 1 张为梗图（451608_img/01.jpg），无分析价值，未内嵌；
- **图证缺口**：无（2 张图，本深读内嵌 1 张）。

## 6. 图表证据

![MakerSuite Access restricted](../../intel/llm-prompting-with-makersuite/bodies/446465_img/01.png)

**图 1**（topic 446465）：Brazil 选手访问 MakerSuite 得到 "Access restricted / You do not have permission to view this page"——地区限制是本届最热的非技术讨论，也是参赛硬门槛的直接证据。

（451608_img/01.jpg 为 Spy vs Spy 梗图，与赛题分析无关，未内嵌。）

## 7. 出处

- 获奖名单与评语（10 票 / 7 评论）：https://www.kaggle.com/competitions/llm-prompting-with-makersuite/discussion/457016
- 资源合集（18 票 / 10 评论）：https://www.kaggle.com/competitions/llm-prompting-with-makersuite/discussion/447223
- MakerSuite 地区限制（17 票 / 12 评论）：https://www.kaggle.com/competitions/llm-prompting-with-makersuite/discussion/446465
- 欧洲不可用（7 票 / 1 评论）：https://www.kaggle.com/competitions/llm-prompting-with-makersuite/discussion/446473
- 游戏/模拟赛巡礼（14 票 / 0 评论）：https://www.kaggle.com/competitions/llm-prompting-with-makersuite/discussion/451608
- BIPOC 机会（13 票 / 0 评论）：https://www.kaggle.com/competitions/llm-prompting-with-makersuite/discussion/446695
- 置顶 Q&A（9 票 / 23 评论）：https://www.kaggle.com/competitions/llm-prompting-with-makersuite/discussion/446450
