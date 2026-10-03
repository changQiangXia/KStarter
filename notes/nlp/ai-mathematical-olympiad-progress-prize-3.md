# AI Mathematical Olympiad - Progress Prize 3

> 主题：nlp ｜ 子类：reasoning ｜ 领域：数学推理 ｜ 类别：Featured
> 截止：2026-04-15 ｜ 队伍数：4138 ｜ 机制：代码赛 ｜ 指标：多轮运行准确率（50 题，答案 ∈ [0, 99999]）
> 数据来源：`intel/ai-mathematical-olympiad-progress-prize-3/`（120 条主题索引 + 8 篇 write-up 正文）

## 1. 任务与数据

- **任务形式**：在固定时间预算内解 50 道 IMO 级数学题，答案限定为整数。**不允许训练/微调**（或说训练不是有效路线），比拼的是**推理时的系统效率**。
- **技术底座**：开源权重模型 **GPT-OSS-120B**（MoE，117B 参数、每 token 激活约 12B），在**单张 H100 80G** 上用 vLLM 部署，配 Python 工具做"工具集成推理"。
- **评分特性**：多轮运行取准确率 → **稳定性与单题鲁棒性**都计入分数；题目顺序固定，时间预算可被调度优化。

## 2. 验证方案

- 本场没有传统意义的数据集划分，替代品是：**公开题集难度对照**（社区专门开了 "Public vs Private problem set difficulty comparison" 帖）与本地题库自测。
- 因为无法过拟合隐藏题目，**工程稳健性（不崩、不超时、答案格式正确）本身就是分数**。

## 3. 方案谱系

| 方案 | 名次 | 关键点 |
| --- | --- | --- |
| GPT-OSS-120B 单卡推理系统优化 | 1st | 显存优化、前缀缓存、KV cache 量化、**熵加权自洽投票**、验证辅助推理、自适应运行时调度 |
| 在公开 notebook 基础上的 7 项定点改进 | 2nd | 每题 8 路并行推理 + 基于熵的打分；明确致谢公共基础设施（vLLM 服务、沙箱池、并行循环） |
| 提示词压缩思考长度 | 37th | 针对固定题序与时限：循环验证、整数工具推荐、避免浮点运算、指定 Python 工具调用时机 |

## 4. 关键技巧

- **自洽投票 + 熵加权**：并行多次推理，按不确定性加权聚合，是无需训练就能显著提分的核心手段。
- **验证辅助推理**：让模型在给出答案前先做代入/反证等验证步骤（37th 用提示词强制"错误检测循环"）。
- **系统级优化**：前缀缓存、KV cache 量化、批处理与调度，直接决定在时限内能跑多少轮推理。
- **上下文工程**：明确禁止浮点运算、指定工具使用时机、限制思考长度，都是为时间预算服务。
- **社区协作**：本题公开 notebook 是公认的公共基础设施（Parthenos、Andreas 等），前三名都建立在其之上并注明增量。

## 5. 可迁移性评估

- **可直接迁移**：
  - **推理预算管理**：多轮并行 + 自洽投票 + 熵加权，适用于任何"推理时算力换准确率"的场景。
  - 提示词里显式约束（避免浮点、限定工具、先验证后作答）能稳定提升可校验任务的正确率。
  - 把"系统不崩、不超时"当作一等目标。
- **需要前提**：
  - 需要可部署的大模型与 GPU（单卡 H100 是本题的硬性条件）。
  - 题目答案可自动校验（否则无法做自洽投票与验证）。
- **不建议照搬**：
  - 假设可以靠微调取胜——本场是推理工程的比赛。
  - 忽略时间调度而一味增加并行轮数。

## 6. 对新手的关键启示

1. **同样是"推理"，本场比赛比的是工程效率而不是模型训练**；识别比赛真正比什么永远是第一步。
2. **自洽投票是最通用的免费午餐**：多跑几次、按不确定性加权，几乎总能提分。
3. **上下文与工具使用的约束也是提示词工程的一部分**，不要只写"你要很聪明"。
4. **公开 notebook 是合法起点**：前三名都在公开基础上做增量并明确署名——这在 Kaggle 是常态文化。

## 7. 出处

- 讨论区索引：`intel/ai-mathematical-olympiad-progress-prize-3/topics.md`（120 条）
- 已收录 write-up（8 篇）：
  - 1st（14 票）：https://www.kaggle.com/competitions/ai-mathematical-olympiad-progress-prize-3/discussion/703222
  - 2nd（15 票）：https://www.kaggle.com/competitions/ai-mathematical-olympiad-progress-prize-3/discussion/702423
  - 37th（13 票）：https://www.kaggle.com/competitions/ai-mathematical-olympiad-progress-prize-3/discussion/700274
  - GPT-OSS-120B 技术总结（28 票）：https://www.kaggle.com/competitions/ai-mathematical-olympiad-progress-prize-3/discussion/702057
  - 公开/私榜难度对照（64 票）：https://www.kaggle.com/competitions/ai-mathematical-olympiad-progress-prize-3/discussion/679559
  - 数学语料奖（46 / 41 / 31 票）：https://www.kaggle.com/competitions/ai-mathematical-olympiad-progress-prize-3/discussion/672668 ｜ 672592 ｜ 672528
