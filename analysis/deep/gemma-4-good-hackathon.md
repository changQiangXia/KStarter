# Gemma 4 Good Hackathon 轻量深读（Tier B）

> 赛事：Featured（评审制 hackathon）｜ 主题 other（Gemma 4 公益应用）｜ 1606 队 / 1500+ 份提交 ｜ 无排行榜 ｜ 交付物：项目 + 技术 write-up（≤1500 词）+ 3 分钟视频
> 材料基础：`digests/gemma-4-good-hackathon.md`（6 篇正文：Welcome 687467 / 评审进展 707673 / 评审完成 732628 / 获奖公布 736681 / ETA 讨论 701910 / 提交问题 695781+701671+701672；80 条主题索引）+ 0 张归档图
> 轻读时间：2026-10（Tier B B13）

## 1. 一句话重述与数字账

用 Gemma 4 系列做"对社会有益"的应用，由主办方人工评审：**技术深度 + 社会影响 + 表达**，其中**视频 Pitch & Storytelling 占 30% 评分**（官方明示）。本场延续 Gemma 3n 的模式，但规模更大（1506+ 份提交、1606 队）：讨论区主线仍是**平台/规则风险**——提交 "Internal Error"、状态不同步、迟到数秒、字数超限，以及"评审完成后还能不能更新 GitHub/HF/线上部署"的反复澄清；评审周期从 5/18 截止拖到数月后才公布获奖名单。

| 关键数字 | 值 | 来源 |
| --- | --- | --- |
| 规模 | 1606 队；官方"well over 1,500 submissions"（远超上一届） | 707673 |
| 评分口径 | 视频 Pitch & Storytelling = **30%**；官方建议：采访真实用户、讲人的故事、3 分钟视频"show, don't tell" | 687467 |
| 时间线 | 截止 2026-05-18；"Reviewing..." 时无明确时间表（58 票 / 35 评论）；"Judging is complete! Final technical checks underway"（36 票 / 42 评论）；随后"Congratulations to our winners!"（24 票 / 32 评论）；另有 ETA 讨论帖（23 票 / 10 评论，反复追问 1600+ 提交何时有结果） | 707673 / 732628 / 736681 / 701910 |
| 提交事故 | "Internal Error"（695781）；提交成功但状态未更新（701671）；迟到数秒（701672 / 701688）；write-up 6,036 词 vs 1,500 词上限（701693） | 索引 |
| 规则澄清 | Health & Sciences 赛道 vs Gemma 禁用政策（687315）；Live Demo 要求（691415）；.apk/.exe 本地执行（693484）；能否用其他模型（687363）；AI Studio API（688843）；**评审完成/技术检查期间能否更新 GitHub / HuggingFace / 线上部署**（701946 / 705045 / 735636） | 索引 |
| 技术与项目 | "31B 可在 Kaggle notebook 推理/微调"（690070，13 票）；Gemma 4 当嵌入模型（691356）；端侧部署被称"最被低估的路线"（687353）；E4B 在医学视觉上与 MedGemma 1.5 4B 接近（704936）；项目谱系集中于健康（DueCare 移工、SafeVoice 家暴）、教育（RealLearn、OpenRead）、农业/环境（FarmWise、GemmaTaiga）、无障碍（VoxLex）与离线物理实验台 | 索引 |

## 2. 逐方案/路线对照矩阵

| 维度 | 视频叙事线（官方强调） | 工程落地线 | 规则合规线 |
| --- | --- | --- | --- |
| 核心 | 3 分钟视频、真实用户访谈、故事化 | 端侧/离线部署（Android/iOS/笔记本）、小模型（2B/4B/E2B）微调、嵌入 | 禁用政策、Live Demo、外部数据、模型组合、提交物格式 |
| 代表帖 | 687467（官方三条样板） | 690070（31B 上 Kaggle）、687353（edge 被低估）、691356（embedding） | 687315 / 691415 / 693484 / 701946 |
| 风险 | 只讲代码不讲人 | 只做 demo 不可复现 | 提交/更新规则踩线导致失格 |

## 3. 共识、分歧与裁决

### 共识一：评审制 hackathon 的胜负在"影响叙事 + 现场演示"，不在模型参数（官方 + 项目帖；置信度高）

官方把视频叙事直接计为 30%，并给出三条高分样板（辅助视障设备、皮肤健康跟踪、语音控制计算）；项目帖也普遍强调真实用户与可用性。**裁决**：先读评审 rubric 再决定投入；演示视频与 write-up 是产品的一部分，不是收尾工作。置信度：高。

### 事件一：平台与规则风险是主要失败源（695781、701671、701672、701693、701946；置信度高）

与 Gemma 3n 如出一辙：Internal Error、状态不同步、迟到数秒、字数超限、赛后能否更新仓库/部署的反复提问。**裁决**：提前数小时提交、留截图证据、按最严格解释执行规则；赛后更新要等官方明确。置信度：高。

### 事件二：评审周期长且时间表多次变化（707673、701910、732628、736681；置信度中高）

5/18 截止后官方先称"没有确切时间表"，之后才进入"评审完成 + 技术检查"，再到获奖公布；期间涌现大量追问帖。**裁决**：评审制比赛的回报周期不可控，参赛规划要按"数月"计。置信度：中高。

### 共识二：技术栈集中在"端侧/离线 + 小模型 + 多模态"（690070、687353、704936；置信度中）

社区热帖围绕 31B 在 Kaggle 上跑、2B/4B/E2B 微调、Gemma 4 嵌入、Android/iOS 离线部署与医学视觉对比。**裁决**：Gemma 4 一届的"可落地性"叙事要求端侧/离线能力，微调与量化是常见技术投入点。置信度：中。

## 4. 证据分级

| 断言 | 等级 | 说明 |
| --- | --- | --- |
| 视频 30% 与三条样板 | 官方帖 | 高 |
| 1506+ 提交/无时间表 | 官方帖 + 高票讨论 | 高 |
| 评审完成与获奖公布时间线 | 官方帖（按帖序） | 中高 |
| 提交事故案例 | 参赛者自述（多帖） | 中高 |
| 规则澄清的具体结论 | 讨论帖（部分未闭合） | 中 |
| 技术路线（31B/端侧/嵌入） | 社区帖 + 票数 | 中 |

## 5. 悬案与缺口（登记）

- 获奖作品名单与技术细节未收录（736681 只有公布帖）；
- "赛后能否更新 GitHub/HF/部署"的最终口径未确认；
- 各赛道评审权重（除视频 30% 外）未整理；
- **图证缺口**：本场归档 0 图。

## 6. 图表证据

无可用图证（本场归档 0 图，图证缺口已登记）。

## 7. 出处

- 官方 Welcome 与评审建议（39 票 / 55 评论）：https://www.kaggle.com/competitions/gemma-4-good-hackathon/discussion/687467
- 评审进展（58 票 / 35 评论）：https://www.kaggle.com/competitions/gemma-4-good-hackathon/discussion/707673
- 评审完成 / 技术检查（36 票 / 42 评论）：https://www.kaggle.com/competitions/gemma-4-good-hackathon/discussion/732628
- 获奖公布（24 票 / 32 评论）：https://www.kaggle.com/competitions/gemma-4-good-hackathon/discussion/736681
- 获奖时间 ETA 讨论（23 票 / 10 评论）：https://www.kaggle.com/competitions/gemma-4-good-hackathon/discussion/701910
- 31B 推理/微调 notebook（13 票）：https://www.kaggle.com/competitions/gemma-4-good-hackathon/discussion/690070
- 端侧部署被低估（3 票）：https://www.kaggle.com/competitions/gemma-4-good-hackathon/discussion/687353
- 提交 Internal Error（1 票）：https://www.kaggle.com/competitions/gemma-4-good-hackathon/discussion/695781
- 状态未更新（1 票）：https://www.kaggle.com/competitions/gemma-4-good-hackathon/discussion/701671
- 迟到数秒（1 票）：https://www.kaggle.com/competitions/gemma-4-good-hackathon/discussion/701672
- Live Demo 澄清（3 票）：https://www.kaggle.com/competitions/gemma-4-good-hackathon/discussion/691415
- 更新规则澄清（2 票）：https://www.kaggle.com/competitions/gemma-4-good-hackathon/discussion/701946
