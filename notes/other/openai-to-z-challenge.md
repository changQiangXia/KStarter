# OpenAI to Z Challenge（精简）

> 主题：other ｜ 子类：hackathon ｜ 类别：Featured ｜ 截止：2025-06-29 ｜ 队伍数：225 ｜ 指标：评审制
> 出处：`intel/openai-to-z-challenge/`（80 条主题索引 + 2 篇 write-up 正文）

## 任务

用 OpenAI 的 o3/o4-mini、GPT-4.1 等模型**协助发现亚马逊雨林中可能被植被掩藏的考古遗址**（结合卫星/遥感影像与地理空间分析）。Kaggle 首届 hackathon 形式，**人工评审**而非榜单评分。

## 关键要点

- 数据/领域入口是公开文献（PNAS、ScienceDirect 等关于亚马逊雨林与毁林的论文），社区在讨论区汇总了入门材料。
- 讨论区还出现了**成本相关话题**（"API 费用由谁承担"）——这类以商业 API 为核心的比赛需要提前评估调用成本。
- 有队伍采用 **RAG-LLM 方案**（检索增强 + 大模型推理）。

## 可迁移要点

- **以商业模型 API 为核心的比赛，先算成本再定方案**（否则可能被预算限制卡住）。
- 领域文献先行：遥感/考古类任务的入门门槛主要在领域知识。
- 评审制比赛仍需提交可复现的技术方案（而非只看结果）。

## 轻读结论（2026-10 补）

- **赛事定位**：Kaggle 首届 hackathon（225 队）；用 OpenAI 模型 + 公开遥感数据找亚马逊被植被掩藏的考古遗址；评审制无排行榜（579189 / 579068）。
- **第一约束是 API 成本**：最高热帖 "Who is paying for API?"（48 票/23 评论）；低门槛讨论 35 票；官方用 checkpoint $100 credits + 6-14 前早提交 5×$1000 API credits 对冲，社区仍担忧预算（579187 / 579173 / 579196 / 579362）。
- **方法共识**：别想一口吃成胖子——先选小区域/单一特征类型（579267）+ 文献综述先行（579226）；技术栈为 LiDAR→DTM、DEM、NDVI、高光谱、embedding 检索；LLM 用于假设生成/RAG 综合而非直接检测（581299 / 587383 / 585543 / 580234）。
- **风险**：OpenAI 源文件幻觉（584626）→ 引用逐条核验；write-up 私有 notebook 链接与漏交/迟到争议（589010 / 587369）→ 截止前留缓冲并公开复现产物。

## 图表证据

本场 0 张归档图（0/0），**图证缺口已登记**；候选点地形/NDVI 图均在站外或私有 notebook 中。

## 出处

- 讨论区索引：`intel/openai-to-z-challenge/topics.md`
- 入门材料（38 票）：https://www.kaggle.com/competitions/openai-to-z-challenge/discussion/579189
- 关键日期（8 票）：https://www.kaggle.com/competitions/openai-to-z-challenge/discussion/581230
- RAG-LLM 方案（4 票）：https://www.kaggle.com/competitions/openai-to-z-challenge/discussion/580234
- API 成本（48 票）：https://www.kaggle.com/competitions/openai-to-z-challenge/discussion/579187
- 别想一口吃成胖子（14 票）：https://www.kaggle.com/competitions/openai-to-z-challenge/discussion/579267
- LiDAR→DTM（18 票）：https://www.kaggle.com/competitions/openai-to-z-challenge/discussion/581299
- OpenAI 源文件幻觉（2 票）：https://www.kaggle.com/competitions/openai-to-z-challenge/discussion/584626
- Winners Announced（13 票 / 60 评论）：https://www.kaggle.com/competitions/openai-to-z-challenge/discussion/602618
