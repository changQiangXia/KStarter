# Google Tunix Hackathon 轻量深读（Tier B）

> 赛事：Featured（评审制 hackathon）｜ 主题 other（LLM 后训练，JAX/TPU）｜ 319 队 / 322 份提交 ｜ 无排行榜 ｜ 交付物：notebook + 视频
> 材料基础：`digests/google-tunix-hackathon.md`（6 篇正文：提交模板与 FAQ 651560 / 延期请求 667200 / 起步与 Discord 617697 / 官方欢迎 617813 / 评审进展 670878 / write-up 数量 664187；80 条主题索引）+ 0 张归档图
> 轻读时间：2026-10（Tier B B17）

## 1. 一句话重述与数字账

用 Google 开源的 JAX 原生后训练库 **Tunix** 对 **Gemma2 2B / Gemma3 1B** 做后训练（SFT/RL/GRPO/蒸馏均可），目标是"通用推理能力"，由人工评委 + AI 评测。本场最鲜明的特征不是算法而是**硬件与复现约束**：Kaggle 只给 v5e-8 TPU（每核 16GB HBM，9h/会话、20h/周），社区被 6+ 小时排队卡死，出现大量延期/提额请求；评测则明确分成"**单会话 45 分**（官方 API、单次 9h 内完成、可复现）"与"**自由模式 15 分**（任意手段，但必须给出可被 Tunix 加载的 Kaggle 模型 ID）"。

| 关键数字 | 值 | 来源 |
| --- | --- | --- |
| 评测规则（651560） | 单会话 **45 分**：只能加载官方 Gemma2 2B/Gemma3 1B、用官方 Tunix API、**9 小时单会话内完成**、禁止加载其他 checkpoint（重罚）；评委会先重跑复现模型再评测，使用私有数据/工具导致无法复现得 0 分。自由/多会话模式 **+15 分**：任意方法，但必须显式给出 Kaggle 模型 ID 且可被 Tunix 加载，否则 0 分 | 651560 |
| 算力与限制 | TPU v5e-8（16GB HBM/核）、**9h/会话、20h/周**；社区帖：排队 **6+ 小时**（666198）、"3 小时排队怎么办"（665744）、"这是 TPU 抢夺战吗"（663707）、"提高 Kaggle TPU 配额"（666506）、正式请求延期一周（667200）；官方拒绝换更大模型（270M 太弱、3n 未实现） | 651560 / 667200 |
| 数据与评审 | 不提供任何数据，自备（Kaggle/HF/其他）；训练数据必须在评测开始前**公开可复现**（单会话模式）；评测集从零私有构建、不公开；**数学/编码等可验证任务权重更低**（starter 已覆盖 + 1B/2B 数学弱 + Gemma 编程不强）；人工评委评 notebook+视频 | 651560 |
| 结果时间线 | 截止 2026-01-12 收到 **322 份提交**，官方称远超预期、需逐份人工审阅 + 复现模型，预计 3 月公布（670878）；随后"终于获奖者揭晓"（691572） | 670878 / 691572 |
| 技术讨论 | GRPO 奖励函数设计（618578）、GRPO 数学（665679）、"SFT 够不够还是必须 RL"（666752）、"完成 15 分多会话加成的澄清"（665714）、TPU 环境错误（`abstracted_axes`、cache size 1536>1024、session 无错误停止）、"leak 很贵"（665032） | 索引 |

## 2. 逐方案/路线对照矩阵

| 维度 | 单会话模式（45 分） | 自由模式（+15 分） |
| --- | --- | --- |
| 模型 | 官方 Gemma2 2B / Gemma3 1B | 任意（最终以 Tunix 加载 Gemma 代码） |
| 训练 | 9h 单会话内完成、官方 API | 多会话、恢复 checkpoint、私有数据均可 |
| 复现 | 评委会重跑 notebook | 只需可加载的 Kaggle 模型 ID |
| 风险 | 无法复现 = 0 分 | 模型不可加载 = 0 分 |

## 3. 共识、分歧与裁决

### 事件一：TPU 配额与排队是本场第一约束（667200、666198、663707、666506、665744；置信度高）

9h/会话、20h/周 + 6 小时以上排队，直接压缩了实验次数；社区集体请求延期与提额。**裁决**：这类"新硬件栈 hackathon"的实际门槛是算力调度；应把排队时间纳入计划并优先跑通端到端最小链路。置信度：高。

### 共识一：可复现性是评分的第一道生死线（651560；置信度高）

单会话模式评委会先重跑 notebook，私有数据/工具不可达即 0 分；自由模式必须有可加载的 Kaggle 模型 ID。**裁决**：提交前必须做"从零复现"演练（公开数据、锁定版本、单会话 9h 内完成）。置信度：高。

### 共识二：官方鼓励 SFT/RL 之外的任意后训练组合，但可验证任务权重低（651560；置信度中高）

官方明确支持 SFT/偏好/RL/蒸馏，并说明数学/编码任务权重下调，希望模型"在现实中有用"。**裁决**：选题要朝通用能力与领域任务倾斜，数据处理与评测设计也是评分内容。置信度：中高。

### 事件二：评审周期长且不透明（670878、691572；置信度中高）

322 份提交需人工逐份审阅 + 复现，官方把公布时间从原计划推迟到 3 月。**裁决**：评审制 hackathon 按"数月"计回报周期。置信度：中高。

## 4. 证据分级

| 断言 | 等级 | 说明 |
| --- | --- | --- |
| 45+15 分评测规则与复现要求 | 官方 FAQ 帖 | 高 |
| TPU 配额/排队 6h+ | 多帖（含官方约束） | 高 |
| 322 份提交与 3 月公布 | 官方帖 | 高 |
| 获奖名单 | 官方帖（简短） | 中高 |
| 技术讨论（GRPO 等） | 社区帖 | 中 |

## 5. 悬案与缺口（登记）

- 获奖方案的技术细节未收录（691572 为名单帖）；
- 自由模式的实际提交数/得分分布未知；
- "leak 很贵"帖指代的数据泄漏事件未细读；
- **图证缺口**：本场归档 0 图。

## 6. 图表证据

无可用图证（本场归档 0 图，图证缺口已登记）。

## 7. 出处

- 提交模板与 FAQ（13 票 / 77 评论）：https://www.kaggle.com/competitions/google-tunix-hackathon/discussion/651560
- 延期请求（23 票 / 5 评论）：https://www.kaggle.com/competitions/google-tunix-hackathon/discussion/667200
- 起步与 Discord（22 票 / 10 评论）：https://www.kaggle.com/competitions/google-tunix-hackathon/discussion/617697
- 官方欢迎（29 票 / 59 评论）：https://www.kaggle.com/competitions/google-tunix-hackathon/discussion/617813
- 评审进展（19 票 / 29 评论）：https://www.kaggle.com/competitions/google-tunix-hackathon/discussion/670878
- 获奖名单（10 票 / 9 评论）：https://www.kaggle.com/competitions/google-tunix-hackathon/discussion/691572
- TPU 排队 6+ 小时（11 票 / 13 评论）：https://www.kaggle.com/competitions/google-tunix-hackathon/discussion/666198
- TPU 抢夺战（9 票 / 12 评论）：https://www.kaggle.com/competitions/google-tunix-hackathon/discussion/663707
- 提高配额请求（5 票 / 14 评论）：https://www.kaggle.com/competitions/google-tunix-hackathon/discussion/666506
