# 5-Day AI Agents Intensive (Vibe Coding with Google) 轻量深读（Tier B）

> 赛事/活动：Featured ｜ 主题 other（课程/meta）｜ "0 队"（非竞赛，Kaggle 课程）｜ 无排行榜 ｜ 11 条主题
> 材料基础：`digests/5-day-ai-agents-intensive-vibecoding-course-with-google.md`（6 篇正文：Codelabs FAQ 1654+ / Welcome+Setup 2592 / Final(Unit5) 1254 / Day2 2147 / Day3 1564 / Day1 4217 票；80 条主题索引）+ 0 张归档图
> 轻读时间：2026-10（Tier B B01）

## 1. 概要：这不是竞赛，而是"Agent 工程"课程

Google × Kaggle 的 5 日 Vibe Coding 课程：每天 1 个 Unit（播客 + 白皮书 + codelab），作业不提交、无排名。它的"深读"价值在于**任务框架与工具链**（与本仓库的 skill/agent 工作流同源）。

| Unit | 主题 | 工具/协议 | 核心概念 |
| --- | --- | --- | --- |
| 1 | Introduction to Agents & Vibe Coding | Antigravity 2.0/IDE/CLI、AI Studio、Cloud Run | 从手写语法 → 意图驱动"vibe coding" → "agentic engineering"；开发者=系统编排者（评估/约束/上下文 harness）；factory model |
| 2 | Agent Tools & Interoperability | Antigravity CLI、Developer Knowledge MCP | MCP（模型↔数据源）、A2A（agent 协作）、A2UI（生成式 UI）、AP2/UCP（机器间支付/商务） |
| 3 | Agent Skills | Agents CLI、ADK、SKILL.md | 便携"技能目录"；**渐进式披露**保持系统提示轻量、按需加载工具与细节；对抗"context rot" |
| 4 | （Day4 未收录正文） | — | —（缺口） |
| 5 | Spec-Driven Production Grade Development | Cloud Run、Antigravity、Policy Server | SDD：代码可弃、**Gherkin 行为规格即真源**；零信任流水线 + 自动代码评审 agent + 混合策略服务器 |

## 2. 要点与"裁决"

### 要点一：Vibe coding 的定位是"原型速度"，生产化靠规格与护栏

Unit1：vibe coding 是意图驱动；Unit5：从"脆弱原型"到企业级要靠 **Spec-Driven Development（行为规格为真源、代码可弃）**、自动评审 agent 与策略服务器。**裁决**：把生成代码当"可替换产物"，把规格/测试/评审当资产——与 agent 编程的最佳实践一致。置信度：高（官方材料）。

### 要点二：工具互操作协议栈 = MCP / A2A / A2UI / AP2 / UCP

MCP 接数据源与工具；A2A 做 agent 间协作；A2UI 生成式界面；AP2/UCP 处理机器间支付与商务。**裁决**：agent 生态正从"自定义集成"转向"开放协议插拔"，工程上应优先选协议化接口。置信度：高（官方）。

### 要点三：Agent Skills 的机制 = SKILL.md + 渐进式披露

技能是围绕 `SKILL.md` 的目录；系统提示只放轻量索引，执行细节/工具**按需加载**，从而让单 agent 以低上下文成本扮演大量专家角色。**裁决**：这解释了本仓库 `skills/` 体系的设计动机；"context rot"是长会话 agent 的中心问题。置信度：高（官方）。

### 要点四：成本/配额是课程实操的第一约束（FAQ）

FAQ 覆盖：课程是否收费、Cloud Run 部署的计费与 $300 试用额度、如何避免意外扣费、Gemini API key 获取、Antigravity 安装/系统要求/配额耗尽后的处理、本地 vs 云端 lab（Kaggle Notebooks/Colab 可行性）、提问渠道（Discord）。**裁决**：动手前先处理账号/配额/计费护栏。置信度：高。

## 3. 证据分级

| 断言 | 等级 | 说明 |
| --- | --- | --- |
| 课程结构（5 Unit/工具/概念） | 官方课程帖（Day1–5+FAQ） | 高 |
| 成本/配额/部署说明 | 官方 FAQ | 高 |
| 课程"成效"（学员收获/落地数据） | 无 | —（缺口） |

## 4. 悬案与缺口（登记）

- **Unit 4（Day 4）与 Capstone 正文未收录**（主题索引有 Day4 709165、Capstone 709721、Wrap-up 609?）；本轻读缺 1/5 课程内容。
- 课程无数值化成效/评测；"0 队"表明它不是可竞技的赛道。
- 无归档图（本场无图证）。

## 5. 图表证据

**本场无归档图片**，无法内嵌图证。

## 6. 出处

- Day 1（4217 票）：https://www.kaggle.com/competitions/5-day-ai-agents-intensive-vibecoding-course-with-google/discussion/708280
- Welcome + Setup（2592 票）：https://www.kaggle.com/competitions/5-day-ai-agents-intensive-vibecoding-course-with-google/discussion/708114
- Day 2（2147 票）：https://www.kaggle.com/competitions/5-day-ai-agents-intensive-vibecoding-course-with-google/discussion/708469
- Codelabs FAQ（1654 票）：https://www.kaggle.com/competitions/5-day-ai-agents-intensive-vibecoding-course-with-google/discussion/708107
- Day 3（1564 票）：https://www.kaggle.com/competitions/5-day-ai-agents-intensive-vibecoding-course-with-google/discussion/708744
- Final Assignment（1254 票）：https://www.kaggle.com/competitions/5-day-ai-agents-intensive-vibecoding-course-with-google/discussion/709464
- 缺口登记：Day 4（709165）、Capstone（709721）、Wrap-up（709712）、Learn Guide（716539）
