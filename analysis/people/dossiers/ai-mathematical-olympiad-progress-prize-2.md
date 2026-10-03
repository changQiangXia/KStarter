# AI Mathematical Olympiad - Progress Prize 2

> `ai-mathematical-olympiad-progress-prize-2` ｜ Featured ｜ 指标 Accuracy Score ｜ 2212 队 ｜ 截止 2025-04-01

本页汇总该场 **1 条 ≥50 票 GM 主题帖**、**6 条断言**、**0 条高票评论**。

## GM 主题帖

| 票 | 选手 | 日期 | 主题 |
| --- | --- | --- | --- |
| 147 | [@darraghdog](https://www.kaggle.com/darraghdog) | 2025-04-23 | [1st place solution - NemoSkills](https://www.kaggle.com/competitions/ai-mathematical-olympiad-progress-prize-2/discussion/574765) |

## 断言（条件→动作→机制→结果）

| 选手 | 等级 | 阶段 | 动作（节选） | 出处 |
| --- | --- | --- | --- | --- |
| @darraghdog | A | 集成与融合 | 用 mergekit 试多种合并，最简单线性组合最优：CoT 0.3 加 TIR 0.7；maj@16 从 62.9/66.8 提升到 69.1，pass@16 从 76.2/80 | [ai-mathematical-olympiad-progress-prize-2#574765-03](https://www.kaggle.com/competitions/ai-mathematical-olympiad-progress-prize-2/discussion/574765) |
| @darraghdog | A | 工程/流程 | 12 个异步生成；前 5 个里 4 个答案一致就取消其余；完成 10/12 也提前停；每题基础 350 秒，剩余时间进共享池，下一题最多借 210 秒（共 560 秒） | [ai-mathematical-olympiad-progress-prize-2#574765-05](https://www.kaggle.com/competitions/ai-mathematical-olympiad-progress-prize-2/discussion/574765) |
| @darraghdog | A | 验证设计 | 自建 Comp-Math-24-25 基准（256 题：AIME/HMMT）作主信号；同一模型不同设置 public 在 23 到 29 波动，最终 private 与 CV 更一 | [ai-mathematical-olympiad-progress-prize-2#574765-06](https://www.kaggle.com/competitions/ai-mathematical-olympiad-progress-prize-2/discussion/574765) |
| @darraghdog | B | 特征与数据工程 | 从 AoPS 收集并清洗 540K 唯一数学题；每题最多 32 个候选解（温度 0.7、top-p 0.95，难题给更多候选）；用 Qwen2.5-32B-Instruct 验证答 | [ai-mathematical-olympiad-progress-prize-2#574765-01](https://www.kaggle.com/competitions/ai-mathematical-olympiad-progress-prize-2/discussion/574765) |
| @darraghdog | B | 特征与数据工程 | 先用 LIMO 做小规模推理微调，再生成带工具调用的长推理并激进过滤；多轮训练、生成、过滤迭代得到 1.7M TIR 解，最终过滤到 15K 用于末段训练 | [ai-mathematical-olympiad-progress-prize-2#574765-02](https://www.kaggle.com/competitions/ai-mathematical-olympiad-progress-prize-2/discussion/574765) |
| @darraghdog | B | 工程/流程 | TensorRT-LLM 加 FP8 或 W8A16 量化（约 1.5x）；训练 ReDrafter 头（10 万解），3 tokens 每步、65% 接受率，再提升约 1.8x； | [ai-mathematical-olympiad-progress-prize-2#574765-04](https://www.kaggle.com/competitions/ai-mathematical-olympiad-progress-prize-2/discussion/574765) |

## 高票评论

_无 ≥10 票评论_

## 关联资产

- 深读：`analysis/deep/ai-mathematical-olympiad-progress-prize-2.md`
- 结构化摘要：`notes/nlp/ai-mathematical-olympiad-progress-prize-2.md`
- 归档讨论区：`intel/ai-mathematical-olympiad-progress-prize-2/`（主题 1 条有 ≥50 票帖，图证 4 个）
