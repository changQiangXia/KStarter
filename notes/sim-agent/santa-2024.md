# Santa 2024（LLM 困惑度优化）

> 主题：sim-agent（纯优化）｜ 子类：— ｜ 领域：优化 / LLM 评测 ｜ 类别：Featured
> 截止：2025-01-XX ｜ 队伍数：2000+ ｜ 机制：标准赛 ｜ 指标：由语言模型计算的困惑度（Kaggle 提供 metric.py）
> 数据来源：`intel/santa-2024/`（80 条主题索引 + 6 篇 write-up 正文）

## 1. 任务与数据

- **任务形式**：年度"Santa"系列赛的 2024 版，本质是**组合优化**问题，但目标函数由**语言模型的困惑度**给出（官方提供 `metric.py`）。
- **数据形态**：多个子问题（sample），每个都可独立优化；社区按 sample 比较分数。
- **构造陷阱**：
  - 目标函数是"黑箱式"的模型打分，**必须本地精确复现**才能迭代。
  - 官方 metric 的实现细节（分批推理与 padding 方向）会直接改变分数（见第 4 节）。

## 2. 验证与优化方案

| 方案 | 使用者 | 说明 |
| --- | --- | --- |
| 本地精确复现 metric | 社区共识 | 迭代速度取决于评测回路的速度与正确性 |
| 分 sample 独立优化 | 多队 | 每个子问题单独搜索，最后合并 |
| 团队互补 | 2nd / 5th | 5th 明确记录"队友在某个 sample 上的最佳解是我单独找不到的" |

## 3. 方案谱系

| 方案 | 名次 | 关键点 |
| --- | --- | --- |
| 迭代局部搜索（Iterated Local Search）+ 受限 k-opt + 自定义 kick | 2nd | 把 TSP 的 k-opt/踢动技术迁移到本题；"受限"以控制指数级搜索成本 |
| 模拟退火变体 + 词分组 | 5th | 从随机打乱出发，多数 sample 能在一半以上次数里找到最优；作者同时列出**无效尝试** |
| 顶层方案 | 1st / 3rd | 见讨论区 |
| "255.9" 通用解法帖 | 社区 | 面向通用分数的解法讨论 |

## 4. 关键技巧

- **跨问题迁移经典算法**：TSP 的 k-opt / ILS 直接改造即可用（与 Santa 2025 的"全局搜索 + 局部精修"骨架一致）。
- **受限邻域**：k-opt 的搜索空间随 k 指数增长，必须限制候选边/移动集合。
- **本地精确评测**：metric 的工程细节至关重要——社区专门发帖说明"**batch_size>1 时要把 tokenizer 的 padding_side 设为 right**"，否则困惑度算错。
- **分 sample 独立优化 + 团队互补**：不同 sample 的最优搜索路径不同，合作能补足。

## 5. 可迁移性评估

- **可直接迁移**：
  - **"本地精确复现打分函数"是黑箱优化任务的第一前提**（与 LLM Prompt Recovery、AI Agent Security 的结论一致）。
  - 经典组合优化技术（k-opt、ILS、SA）可跨领域迁移。
  - 分样本独立优化再合并。
- 需要前提：可本地推理的语言模型（否则评测太慢）；

  实现细节要与官方 metric 完全一致。
- 不建议照搬：任何"看起来对但没对齐官方 metric"的本地评测。

## 6. 对新手的关键启示

1. **先对齐评测函数，再谈优化**——padding 方向这种细节就能让分数失真。
2. **优化类比赛拼的是搜索效率与实现细节**，不是模型规模。
3. **公开讨论里"哪些做法无效"往往比成功经验更省时间**（5th 专门列了无效尝试）。

## 7. 出处

- 讨论区索引：`intel/santa-2024/topics.md`（80 条）
- 已收录 write-up（6 篇）：
  - 1st（85 票）：https://www.kaggle.com/competitions/santa-2024/discussion/560560
  - 2nd（43 票）：https://www.kaggle.com/competitions/santa-2024/discussion/560533
  - 3rd（30 票）：https://www.kaggle.com/competitions/santa-2024/discussion/560620
  - 5th（43 票）：https://www.kaggle.com/competitions/santa-2024/discussion/560597
  - 正确困惑度计算（92 票）：https://www.kaggle.com/competitions/santa-2024/discussion/548249
