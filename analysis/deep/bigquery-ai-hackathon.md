# BigQuery AI – Building the Future of Data Hackathon 轻量深读（Tier B）

> 赛事：Featured（评审制 hackathon）｜ 主题 other（BigQuery AI 数据应用）｜ 276 队 / 250+ 份提交 ｜ 截止 2025-09-22
> 材料基础：`digests/bigquery-ai-hackathon.md`（6 篇正文：获奖与评审流程 612730 / 云额度支持 598576 / 官方欢迎 598594 / 结赛致谢 609100 / 评审延期 610964 / Vertex AI notebooks 提示 599317；59 条主题索引）+ 0 张归档图
> 轻读时间：2026-10（Tier B B18）

## 1. 一句话重述与数字账

用 **BigQuery AI**（AI.GENERATE / 向量搜索 / 多模态）做一个真实业务应用，按 **Generative AI / Vector Search / Multimodal** 三类评审。最值得复用的是官方公开的评审流程：**每一份都人工读、必须用三大类之一、必须公开可访问、每个获奖作品都被评委实际复现**；缺 artifact 或无法访问直接过滤。另一条主线是**云成本与账号门槛**：官方给出 $300 试用 + 免费层 + $50 追加额度 + $5 无卡额度，社区仍在担心账单与项目被封；截止前后还出现提交按钮集体失效的事故。

| 关键数字 | 值 | 来源 |
| --- | --- | --- |
| 规模与节奏 | **276 队、250+ 份提交**；计划 9/22–10/6 评审、10/13 公布 → 延期到 **10 月 20 日那周**（人工逐份阅读）→ 最终获奖公告 | 609100 / 610964 / 612730 |
| 评审流程（硬门槛） | 每份**人工阅读**并多次评估；按 rubric 权重，**缺多个 artifact 的直接过滤**；**必须使用三大类之一**（无 BigQuery AI 则过滤）；**公开可访问**是要求；每个获奖提交都被评委**实际复现/验证**（必要时补 DDL 或小修）；每份至少两名评审；违反负责任 AI 政策的过滤 | 612730 |
| 奖项 | 三类各 1 名"Best in X"+前三：GenAI（TriLink / AI Patent Analyst / ESG Reports Agent）、Vector Search（SpeakAura AI / ReDrugAI / Causal RAG）、Multimodal（OncOmix AI / Grid Incident Rag / Auto-Updating Documentation）；另有 2 个 HM（Patent Intelligence、CLARIS）与 2 个 commendable | 612730 |
| 云额度 | 新用户 90 天 **$300** 试用 + BigQuery 免费层 + 填表再给的 **$50** 额度（每周发放、先到先得）+ 无信用卡者可领多个 **$5 instrumentless credits** | 598576 |
| 成本/账号风险 | "没有信用卡怎么办" 8 票；"严重担心账单"；"跟踪成本"；"GCP 项目被标记/暂停"两帖 | 598831 / 604156 / 604152 / 608490 / 607298 |
| 提交事故 | "提交按钮失效"两帖（15 / 10 评论）、"保存锁定"（4 评论）、"按时做完却没提交上"（4 评论）、"技术错误错过截止"、延长截止请求（-6 票） | 608992 / 608986 / 609004 / 608987 / 609159 |
| 规则澄清热帖 | 1 vs 2 个最终提交冲突；公开 notebook 是否被 GitHub 替代；数据集/BigQuery 连接是否必须公开；**不得在提交中包含凭据**；notebook Add-ons 需选 BigQuery 账号 | 599127 / 608073 / 607854 / 608657 / 608853 / 604203 |

## 2. 逐方案对照矩阵

| 维度 | 获奖共性（612730） | 被过滤模式 | 成本/复现风险 |
| --- | --- | --- | --- |
| 技术 | 至少一类 BigQuery AI 能力 + 明确业务闭环 | 没用三大类之一 | 免费层/额度不够 → 跑不完 |
| 交付 | write-up 讲清 impact（时间/成本/ROI） | artifact 缺失、不可公开访问 | GCP 项目被暂停 |
| 验证 | 评委按其说明复现成功 | 无 DDL/说明导致无法复现 | 依赖私有数据/凭据 |
| 合规 | 符合负责任 AI 政策 | 触碰政策红线 | 含凭证泄露 |

## 3. 共识、分歧与裁决

### 共识一：可复现性是第一道生死线（612730；置信度高）

评委明确"每个获奖提交都被复现验证"，且公开可访问是硬要求。**裁决**：提交前做一次"评委视角冷启动"（新账号、无私有依赖、按说明逐步执行），把 DDL/数据准备/配额要求写进 notebook。置信度：高。

### 共识二：三大类必须选其一，组合可以自由（598594 / 612730；置信度高）

官方欢迎帖鼓励组合，但结赛复盘明确"没有 BigQuery AI 就过滤"。**裁决**：至少给一个明确的 AI.GENERATE / 向量搜索 / 多模态调用点，并说明它解决业务问题的哪一步。置信度：高。

### 事件一：云成本与账号是隐性门槛（598576 / 598831 / 608490 / 604156；置信度中高）

官方用试用+免费层+$50+$5 无卡额度覆盖长尾，但社区仍出现 GCP 项目暂停与账单担忧。**裁决**：开赛第一周跑通计费监控与配额告警；避免长时间循环调用；保留额度申领凭证。置信度：中高。

### 事件二：截止前的提交系统不可靠（608992 / 608986 / 609004 / 608987；置信度中高）

多人报告按钮失效/保存锁定，官方未在归档中回应补救。**裁决**：至少提前 48h 完成提交，保留截图与 notebook 版本号作为申诉证据。置信度：中高。

### 事件三：评审周期长且会延期（610964；置信度中高）

从 10/13 推到 10/20 那周，理由是逐份人工阅读。**裁决**：不要把结果时间写进对外承诺；延期期间保持 notebook 可访问。置信度：中高。

### 分歧：评审 rubric 与个人反馈（612790；置信度低—中）

有选手请求评分与 rubric 反馈，获奖帖只公开 rubric 概览与自己承诺的流程，不给个人分。**裁决**：按公开的硬门槛自检，不指望事后反馈。置信度：中。

## 4. 证据分级

| 断言 | 等级 | 说明 |
| --- | --- | --- |
| 评审流程与硬门槛 | 官方帖（612730） | 高 |
| 获奖名单与评语 | 官方帖（612730） | 高 |
| 250+ 提交与评审时间线 | 官方帖（609100 / 610964） | 高 |
| 额度方案 | 官方帖（598576） | 高 |
| 成本/账号与提交事故 | 多帖（社区） | 中高（现象密集，官方回应缺失） |
| rubric 反馈问题 | 单帖（612790） | 低 |

## 5. 悬案与缺口（登记）

- 官方 rubric 的完整权重未在归档中给出（只说明硬门槛与验证方式）；
- 提交事故是否有补救/延期处理未归档；
- 获奖作品的 notebook 均在站外，未随归档复制；
- 幻灯片/视频是否为必需项（"video 似乎可选"帖无官方答复）；
- **图证缺口**：本场 0 张归档图，已登记。

## 6. 图表证据

本场 0/0 张归档图，**图证缺口已登记**。

## 7. 出处

- 获奖与评审流程（8 票 / 12 评论）：https://www.kaggle.com/competitions/bigquery-ai-hackathon/discussion/612730
- 云额度支持（13 票 / 37 评论）：https://www.kaggle.com/competitions/bigquery-ai-hackathon/discussion/598576
- 官方欢迎（24 票 / 49 评论）：https://www.kaggle.com/competitions/bigquery-ai-hackathon/discussion/598594
- 结赛致谢与 250+ 提交（8 票 / 2 评论）：https://www.kaggle.com/competitions/bigquery-ai-hackathon/discussion/609100
- 评审延期（13 票 / 10 评论）：https://www.kaggle.com/competitions/bigquery-ai-hackathon/discussion/610964
- 提交按钮失效（1 票 / 15 评论）：https://www.kaggle.com/competitions/bigquery-ai-hackathon/discussion/608992
- 无信用卡与额度（8 票 / 4 评论）：https://www.kaggle.com/competitions/bigquery-ai-hackathon/discussion/598831
- GCP 项目暂停（2 票 / 1 评论）：https://www.kaggle.com/competitions/bigquery-ai-hackathon/discussion/607298
- 不得包含凭证（5 票 / 0 评论）：https://www.kaggle.com/competitions/bigquery-ai-hackathon/discussion/608853
- 评审 rubric 反馈请求（1 票 / 1 评论）：https://www.kaggle.com/competitions/bigquery-ai-hackathon/discussion/612790
