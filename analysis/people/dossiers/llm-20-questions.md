# LLM 20 Questions

> `llm-20-questions` ｜ Featured ｜ 指标 llm_20_questions ｜ 832 队 ｜ 截止 2024-08-29

本页汇总该场 **2 条 ≥50 票 GM 主题帖**、**6 条断言**、**0 条高票评论**。

## GM 主题帖

| 票 | 选手 | 日期 | 主题 |
| --- | --- | --- | --- |
| 90 | [@cnumber](https://www.kaggle.com/cnumber) | 2024-08-30 | [1st Place Solution](https://www.kaggle.com/competitions/llm-20-questions/discussion/531106) |
| 60 | [@cdeotte](https://www.kaggle.com/cdeotte) | 2024-07-16 | [Starter Notebook - Llama3-8B - [LB 0.750+] - [Rank 59th]](https://www.kaggle.com/competitions/llm-20-questions/discussion/520429) |

## 断言（条件→动作→机制→结果）

| 选手 | 等级 | 阶段 | 动作（节选） | 出处 |
| --- | --- | --- | --- | --- |
| @cnumber | A | 建模与训练 | Guesser 开局直接问 Is it Agent Alpha?（而不是强制 Alpha 模式省一轮），因为非 Alpha 对局收益更大，且与低分 Agent 配对时输掉损失大；A | [llm-20-questions#531106-01](https://www.kaggle.com/competitions/llm-20-questions/discussion/531106) |
| @cnumber | A | 工程/流程 | 三类问题：26 个字母问题、约 3000 个来自公开胜局、约 10000 个 GPT-4o mini 生成；用 Meta-Llama-3-8B、Phi-3-small、gemma- | [llm-20-questions#531106-03](https://www.kaggle.com/competitions/llm-20-questions/discussion/531106) |
| @cnumber | B | 特征与数据工程 | 用词数、英语词频与 GPT-4o mini 的 thing-ness（问 Would the word X generally be considered a thing? 取 Y | [llm-20-questions#531106-02](https://www.kaggle.com/competitions/llm-20-questions/discussion/531106) |
| @cnumber | B | 建模与训练 | 一般问题用 Meta-Llama-3-8B-Instruct，数学与字母计数类用 DeepSeek-Math（可输出 Python 程序求解）；用规则触发（问题含 letter 等 | [llm-20-questions#531106-04](https://www.kaggle.com/competitions/llm-20-questions/discussion/531106) |
| @cdeotte | B | 工程/流程 | 该 notebook 演示：如何提问缩小搜索（背后用 CSV 特征）、如何在提交里安装 pip 库、如何下载与使用 HF LLM、如何对 LLM 答题能力做 EDA、如何生成 ag | [llm-20-questions#520429-01](https://www.kaggle.com/competitions/llm-20-questions/discussion/520429) |
| @cdeotte | B | 复盘与流程 | 缺点：用固定（旧）关键词列表（public 已变、private 可能再变）、只问地点类问题；改进：从 Wikipedia 选成千上万词作候选，为其建特征列与预定问题，再根据回答与 | [llm-20-questions#520429-02](https://www.kaggle.com/competitions/llm-20-questions/discussion/520429) |

## 高票评论

_无 ≥10 票评论_

## 关联资产

- 深读：`analysis/deep/llm-20-questions.md`
- 结构化摘要：`notes/nlp/llm-20-questions.md`
- 归档讨论区：`intel/llm-20-questions/`（主题 2 条有 ≥50 票帖，图证 2 个）
