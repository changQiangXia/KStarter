# Santa 2022 - The Christmas Card Conundrum

> `santa-2022` ｜ Featured ｜ 指标 Santa's Print Shop 2022 ｜ 874 队 ｜ 截止 2023-01-17

本页汇总该场 **1 条 ≥50 票 GM 主题帖**、**4 条断言**、**0 条高票评论**。

## GM 主题帖

| 票 | 选手 | 日期 | 主题 |
| --- | --- | --- | --- |
| 80 | [@cnumber](https://www.kaggle.com/cnumber) | 2023-01-18 | [1st place solution with visualized route](https://www.kaggle.com/competitions/santa-2022/discussion/379167) |

## 断言（条件→动作→机制→结果）

| 选手 | 等级 | 阶段 | 动作（节选） | 出处 |
| --- | --- | --- | --- | --- |
| @cnumber | A | 建模与训练 | 阶段一：GA-EAX 解带路径依赖约束的 TSP；阶段二：beam search 构造臂配置；约束以惩罚成本加入而非硬排除，随 GA 进化逐渐减少违规路径 | [santa-2022#379167-01](https://www.kaggle.com/competitions/santa-2022/discussion/379167) |
| @cnumber | A | 工程/流程 | 选 GA-EAX：cost 计算次数少、易加约束、可保存与恢复种群；LKH 加约束难且差（约 74077），一天 LKH 无改进；Concorde 5000 顶点要数小时到数天，G | [santa-2022#379167-02](https://www.kaggle.com/competitions/santa-2022/discussion/379167) |
| @cnumber | A | 工程/流程 | 64 臂约束为 L∞ 距离不超过 64；DP 表 [step][32-arm][64-arm]（约 9 乘以 10 的 9 次方规模，C++ 几秒）判定可行性；beam searc | [santa-2022#379167-03](https://www.kaggle.com/competitions/santa-2022/discussion/379167) |
| @cnumber | B | 复盘与流程 | 非最优臂移动收益低于重构成本（移动 3 臂使重构成本从 1 升到 sqrt(3)，增加 0.7）；去掉约束 3 只省 0.19 但重构成本更高；LKH、Concorde、GPX2  | [santa-2022#379167-04](https://www.kaggle.com/competitions/santa-2022/discussion/379167) |

## 高票评论

_无 ≥10 票评论_

## 关联资产

- 深读：`analysis/deep/santa-2022.md`
- 结构化摘要：`notes/sim-agent/santa-2022.md`
- 归档讨论区：`intel/santa-2022/`（主题 1 条有 ≥50 票帖，图证 2 个）
