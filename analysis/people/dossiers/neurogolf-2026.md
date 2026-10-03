# The 2026 NeuroGolf Championship

> `neurogolf-2026` ｜ Research ｜ 指标 NeuroGolf Metric ｜ 2963 队 ｜ 截止 2026-07-15

本页汇总该场 **2 条 ≥50 票 GM 主题帖**、**7 条断言**、**1 条高票评论**。

## GM 主题帖

| 票 | 选手 | 日期 | 主题 |
| --- | --- | --- | --- |
| 115 | [@cdeotte](https://www.kaggle.com/cdeotte) | 2026-07-16 | [1st Place - Kaggle Agent - Introduction](https://www.kaggle.com/competitions/neurogolf-2026/discussion/726654) |
| 66 | [@yiheng](https://www.kaggle.com/yiheng) | 2026-07-16 | [9th place solution](https://www.kaggle.com/competitions/neurogolf-2026/discussion/726653) |

## 断言（条件→动作→机制→结果）

| 选手 | 等级 | 阶段 | 动作（节选） | 出处 |
| --- | --- | --- | --- | --- |
| @cdeotte | A | 工程/流程 | 观察历史分数：重写架构平均每任务加 0.5，优化现有图只有 0.05，因此鼓励 agent 探索新架构 | [neurogolf-2026#726654-02](https://www.kaggle.com/competitions/neurogolf-2026/discussion/726654) |
| @yiheng | A | 工程/流程 | 先构建优化系统而非逐任务优化：受 2025 Code Golf 第四名方案启发（并行采样、规则化 prompt 生成、候选验证、选最优、结构化 prompt 驱动下一轮、迭代精修与 | [neurogolf-2026#726653-01](https://www.kaggle.com/competitions/neurogolf-2026/discussion/726653) |
| @yiheng | A | 建模与训练 | 新口径 cost = memory + parameters，score = max(1, 25 - ln(max(1, cost)))，MACs 仅诊断 → 计算免费、参数与中间 | [neurogolf-2026#726653-02](https://www.kaggle.com/competitions/neurogolf-2026/discussion/726653) |
| @yiheng | A | 工程/流程 | 每任务固定三文件：ONNX（提交物）、attack 脚本（可读可复现构建器）、task 文档（语义、成本历史、验证证据、风险）；成功则三文件同时晋级、失败同时回滚 | [neurogolf-2026#726653-03](https://www.kaggle.com/competitions/neurogolf-2026/discussion/726653) |
| @yiheng | A | 工程/流程 | worker 读取：任务样本（dataset/taskNNN.json）、当前实现（onnx、attack 脚本、任务文档）、共享优化知识（tricks.md 与 scorer 政 | [neurogolf-2026#726653-04](https://www.kaggle.com/competitions/neurogolf-2026/discussion/726653) |
| @yiheng | A | 工程/流程 | 两条互补流水线：Codex 调度器做高吞吐实现与验证；ChatGPT 网页工作流做长上下文语义分析与架构发现 | [neurogolf-2026#726653-05](https://www.kaggle.com/competitions/neurogolf-2026/discussion/726653) |
| @cdeotte | C | 工程/流程 | 用 dashboard 追踪各任务进度并共享 onnx | [neurogolf-2026#726654-01](https://www.kaggle.com/competitions/neurogolf-2026/discussion/726654) |

## 高票评论

| 票 | 选手 | 日期 | 摘录 | 出处 |
| --- | --- | --- | --- | --- |
| 18 | @jiweiliu | 2026-07-15 | a special medal should be awarded to you 🫡 | [726541](https://www.kaggle.com/competitions/neurogolf-2026/discussion/726541) |

## 关联资产

- 深读：`analysis/deep/neurogolf-2026.md`
- 结构化摘要：`notes/sim-agent/neurogolf-2026.md`
- 归档讨论区：`intel/neurogolf-2026/`（主题 2 条有 ≥50 票帖，图证 7 个）
