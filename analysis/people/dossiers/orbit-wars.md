# Orbit Wars

> `orbit-wars` ｜ Featured ｜ 指标 orbit_wars ｜ 4729 队 ｜ 截止 2026-07-07

本页汇总该场 **2 条 ≥50 票 GM 主题帖**、**6 条断言**、**1 条高票评论**。

## GM 主题帖

| 票 | 选手 | 日期 | 主题 |
| --- | --- | --- | --- |
| 150 | [@pressman1](https://www.kaggle.com/pressman1) | 2026-06-26 | [Scaling Reinforcement Learning to the Stars](https://www.kaggle.com/competitions/orbit-wars/discussion/714324) |
| 90 | [@pressman1](https://www.kaggle.com/pressman1) | 2026-07-10 | [1st Place Solution - Scaling Reinforcement Learning to the Stars](https://www.kaggle.com/competitions/orbit-wars/discussion/724268) |

## 断言（条件→动作→机制→结果）

| 选手 | 等级 | 阶段 | 动作（节选） | 出处 |
| --- | --- | --- | --- | --- |
| @pressman1 | A | 建模与训练 | 200M 参数 transformer，纯 self-play RL 训练 15B 步，无模仿学习初始化；押注 Bitter Lesson：表达力足够的大模型加足够训练胜过精调小模 | [orbit-wars#714324-01](https://www.kaggle.com/competitions/orbit-wars/discussion/714324) |
| @pressman1 | A | 工程/流程 | int8 量化线性层、限制可见 fleet 数并优先最大者；对约 8% 超时的 4p 局，在剩余 1 秒 overage 时切换到 5M 小模型收尾；用 4-bit NormalF | [orbit-wars#714324-04](https://www.kaggle.com/competitions/orbit-wars/discussion/714324) |
| @pressman1 | C | 工程/流程 | 用 Codex 完成开发，人工只审文档；agent 能正确实现规格但建议与创造力不足 | [orbit-wars#714324-02](https://www.kaggle.com/competitions/orbit-wars/discussion/714324) |
| @pressman1 | C | 工程/流程 | 用 Rust 重写模拟环境，用真实 replay 做大量 parity 测试；预分配并复用 pinned memory、多线程并行环境 | [orbit-wars#714324-05](https://www.kaggle.com/competitions/orbit-wars/discussion/714324) |
| @pressman1 | C | 建模与训练 | 训练时加动作掩码，结果模型反而更差；推测掩码让模型少学物理；最终只在微调与测试时恢复掩码 | [orbit-wars#714324-06](https://www.kaggle.com/competitions/orbit-wars/discussion/714324) |
| @pressman1 | C | 复盘与流程 | gamma=1.0 让模型缺少尽早取胜的激励，拿到领先就拖延（浪费时间算力）；训练后半段 90% 用 2p，但提交后顶层对局多为 4p；建议加早期截断/投降与 league pla | [orbit-wars#714324-07](https://www.kaggle.com/competitions/orbit-wars/discussion/714324) |

## 高票评论

| 票 | 选手 | 日期 | 摘录 | 出处 |
| --- | --- | --- | --- | --- |
| 15 | @pressman1 | 2026-06-27 | I agree with your sentiment and find myself similarly torn. Software engineering has been unbelievably accessi | [714324](https://www.kaggle.com/competitions/orbit-wars/discussion/714324) |

## 关联资产

- 深读：`analysis/deep/orbit-wars.md`
- 结构化摘要：`notes/sim-agent/orbit-wars.md`
- 归档讨论区：`intel/orbit-wars/`（主题 2 条有 ≥50 票帖，图证 2 个）
