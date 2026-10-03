# OpenAI to Z Challenge（精简）

> 主题：other ｜ 子类：hackathon ｜ 类别：Featured ｜ 截止：2025-06-29 ｜ 队伍数：225 ｜ 指标：评审制
> 出处：`intel/openai-to-z-challenge/`（80 条主题索引 + 6 篇 write-up 正文）

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

## 出处

- 讨论区索引：`intel/openai-to-z-challenge/topics.md`
- 入门材料（38 票）：https://www.kaggle.com/competitions/openai-to-z-challenge/discussion/579189
- 关键日期（8 票）：https://www.kaggle.com/competitions/openai-to-z-challenge/discussion/581230
- RAG-LLM 方案（4 票）：https://www.kaggle.com/competitions/openai-to-z-challenge/discussion/580234
