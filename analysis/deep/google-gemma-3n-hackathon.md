# Google Gemma 3n Hackathon 轻量深读（Tier B）

> 赛事：Featured（评审制 hackathon）｜ 主题 other（端侧多模态应用）｜ 599 队 / ~600 份提交 ｜ 无排行榜 ｜ 交付物：技术 write-up + 可运行 app/演示
> 材料基础：`digests/google-gemma-3n-hackathon.md`（6 篇正文：收尾 597690 / 结果时间线 635977 / 提交故障申诉 597689 / 延期请求 596963 / 观感帖 598062 / 许可更正 589997；80 条主题索引）+ 1 张归档图
> 轻读时间：2026-10（Tier B B11）

## 1. 一句话重述与数字账

以 Gemma 3n（端侧多模态模型）为主题的应用黑客松：参赛者交付"技术 write-up + app/演示"，由评委评审，没有公开排行榜。归档材料的主线不在模型技术，而在**赛事机制**——约 600 份提交、2025-08-06 截止、官方承诺"数周内"公布结果，实际到 11 月底（感恩节后）才选出获奖者；期间讨论区被"提交报错 / 迟到 1 秒 / 时区换算"与"何时出结果"两类帖子占满。

| 关键数字 | 值 | 来源 |
| --- | --- | --- |
| 规模 | **599 队 / ~600 份提交**（官方："nearly 600 submissions"） | 597690 |
| 截止与结果 | 提交窗 2025-08-06 关闭；官方称"coming weeks"，实际 2025-11 底（感恩节后）才公布获奖者；获奖名单帖 13 票 / 30 评论 | 597690 / 635977 / 657756 |
| 讨论区重心 | 收尾帖 51 票 / 99 评论；Welcome 28 票 / 91 评论；延期请求 21 票 / 19 评论；Unsloth 微调帖 20 票 | 主题索引 |
| 提交事故 | "Internal Error" 申诉帖（12 票）附界面截图；另有草稿未提交（597695）、迟到 1 秒 / 1 分钟 / 时区换算（597675 / 597674 / 597682）等 | 597689 等 |
| 规则变动 | 公开 write-up 许可从 CC0 事后更正为 CC BY 4.0（允许撤稿） | 589997 |

## 2. 逐方案/路线对照矩阵

| 维度 | 端侧 app 线（PluvIA 为代表） | 微调线（Unsloth 帖） | 部署工具线（starter/问答） |
| --- | --- | --- | --- |
| 形态 | Flutter 离线优先 app + 本地 Gemma 3n 多模态助手 | Gemma 3n 微调 + 多模态推理 | React Native + MediaPipe / LiteRT / Ollama / iOS |
| 技术栈 | Flutter + n8n + EPA SWMM 5 水文模型，后端预测结果缓存到本地 | Unsloth 微调（官方另有 audio/vision 微调 notebook 593950） | MediaPipe AI 模板（590636）、LiteRT 包选择（588888）、Android 部署问答（589896） |
| 交付证据 | GitHub app/server + APK 演示 + 技术 write-up + 视频 | 帖内流程（正文未收录） | 模板与问答 |
| 状态 | 遭遇 "Internal Error" 错过提交，公开申诉 | 索引可见，正文未归档 | 社区互助 |
| 启示 | 端侧隐私/低延迟叙事 + 现实场景（洪水预警） | 小模型微调是可行路线 | 端侧部署工具链是主要门槛 |

## 3. 共识、分歧与裁决

### 共识一：这是"评审制作品赛"，优化对象是叙事与可运行 demo（官方规则 + 各路线帖）

提交物 = 技术 write-up + app/直播演示，无排行榜。**裁决**：与分数赛不同，hackathon 的"验证"由评委完成——提前打磨故事线、可复现 demo 与影响力度量，比刷任何指标都重要。置信度：高。

### 共识二：Gemma 3n 的差异化卖点是端侧/离线多模态（官方 + PluvIA + starter/微调帖）

Welcome 与 starter 模板围绕"手机/边缘设备上跑 text+audio+vision"；PluvIA 把"离线优先、隐私、低延迟"作为核心卖点；Unsloth 帖与官方 audio/vision notebook 提供微调路径。**裁决**：端侧约束（内存/量化/延迟）既是技术难点也是叙事优势；微调与端侧部署是两条互补路线。置信度：中高（技术细节正文稀薄）。

### 事件一：提交基础设施与截止认定是最大风险（多帖，置信度高）

迟到 1 秒（597675）、迟到 1 分钟（597674）、时区换算错误（597682）、"Internal Error"（597689）、草稿未提交（597695）等案例密集出现，另有两条延期请求帖（591519 / 596963）。**裁决**：此类比赛应提前数小时完成提交并回读确认状态，保留截图/时间戳作申诉证据；平台侧则暴露了提交系统的可靠性问题。置信度：高（案例多、含截图）。

### 事件二：评审周期远超官方承诺（635977 / 610632 / 657756）

官方 8/6 称"coming weeks"，11 月底才宣布获奖者，期间出现"是不是忘了公布"的帖子。**裁决**：评审制 hackathon 的结果时间不可控，参赛成本应按"无确定回报"计。置信度：高（时间线自明）。

### 事件三：规则/许可的事后修正（589997 / 590361）

许可从 CC0 更正为 CC BY 4.0 并允许撤稿；另有"write-up 类别矛盾"等规则歧义帖。**裁决**：参赛前应确认许可与公开范围；事后改规则会实质影响参赛者的公开意愿。置信度：中（单帖官方，未核对全部规则版本）。

## 4. 证据分级

| 断言 | 等级 | 说明 |
| --- | --- | --- |
| 规模 ~600 提交、8/6 截止、评审启动 | 官方帖 | 高 |
| 获奖者 11 月底公布 | 官方帖（635977）+ 名单帖（657756） | 高 |
| 提交故障/迟到案例 | 参赛者自述 + 截图 | 中高 |
| PluvIA 的技术栈（Flutter + n8n + SWMM 5） | 参赛者自述 + GitHub 链接 | 中 |
| Unsloth 微调 / 官方 audio-vision notebook 的实际效果 | 索引标题 + 官方帖（正文未细读） | 中 |

## 5. 悬案与缺口（登记）

- 获奖作品名单与评审标准（657756）未细读；获胜项目技术细节未归档；
- 20 票的 Unsloth 微调帖（587725）与官方 audio/vision 微调 notebook（593950）正文未收录，微调路线效果无法评估；
- 无排行榜与分数，无法定量对比；所有性能叙述均为自述；
- **图证**：仅 1 张（提交报错截图），无项目架构/演示图。

## 6. 图表证据

![提交 "Internal Error" 截图](../../intel/google-gemma-3n-hackathon/bodies/597689_img/01.png)

**图 1**（topic 597689）：参赛者提交 PluvIA 时遭遇 "Internal Error" 的界面截图——提交系统故障被公开申诉，是本届讨论区的代表性事件。

## 7. 出处

- 收尾公告（51 票 / 99 评论）：https://www.kaggle.com/competitions/google-gemma-3n-hackathon/discussion/597690
- 获奖者选定与公布时间线（36 票）：https://www.kaggle.com/competitions/google-gemma-3n-hackathon/discussion/635977
- 获奖名单（13 票 / 30 评论）：https://www.kaggle.com/competitions/google-gemma-3n-hackathon/discussion/657756
- Welcome（28 票 / 91 评论）：https://www.kaggle.com/competitions/google-gemma-3n-hackathon/discussion/586454
- 提交 "Internal Error" 申诉（12 票）：https://www.kaggle.com/competitions/google-gemma-3n-hackathon/discussion/597689
- 延期请求（21 票）：https://www.kaggle.com/competitions/google-gemma-3n-hackathon/discussion/591519
- Unsloth 微调 + 多模态推理（20 票）：https://www.kaggle.com/competitions/google-gemma-3n-hackathon/discussion/587725
- 公开 write-up 许可更正（5 票）：https://www.kaggle.com/competitions/google-gemma-3n-hackathon/discussion/589997
- 官方 audio/vision 微调 notebook（6 票）：https://www.kaggle.com/competitions/google-gemma-3n-hackathon/discussion/593950
- 移动端 starter 模板（9 票）：https://www.kaggle.com/competitions/google-gemma-3n-hackathon/discussion/590636
