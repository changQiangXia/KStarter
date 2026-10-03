# Santa 2025 - Christmas Tree Packing Challenge

> `santa-2025` ｜ Featured ｜ 指标 Santa 2025 Metric ｜ 3357 队 ｜ 截止 2026-01-30

本页汇总该场 **3 条 ≥50 票 GM 主题帖**、**6 条断言**、**1 条高票评论**。

## GM 主题帖

| 票 | 选手 | 日期 | 主题 |
| --- | --- | --- | --- |
| 111 | [@jeroencottaar](https://www.kaggle.com/jeroencottaar) | 2026-02-08 | [1st place: genetic algorithm and GPU relaxation](https://www.kaggle.com/competitions/santa-2025/discussion/672465) |
| 84 | [@jeroencottaar](https://www.kaggle.com/jeroencottaar) | 2026-01-31 | [1st place solution preview](https://www.kaggle.com/competitions/santa-2025/discussion/671058) |
| 65 | [@cnumber](https://www.kaggle.com/cnumber) | 2025-11-18 | [Visualization of my 10 trees solution. This year's santa is going to b](https://www.kaggle.com/competitions/santa-2025/discussion/629896) |

## 断言（条件→动作→机制→结果）

| 选手 | 等级 | 阶段 | 动作（节选） | 出处 |
| --- | --- | --- | --- | --- |
| @jeroencottaar | A | 建模与训练 | 偶数棵树强制 180° 对称（genotype 只存一半，phenotype 展开）；再用 tessellated 种子（预定晶体加边缘随机），GA 只动边缘树 | [santa-2025#672465-02](https://www.kaggle.com/competitions/santa-2025/discussion/672465) |
| @jeroencottaar | A | 工程/流程 | cost 为重叠平方和加越界平方和；exact separation distance 用 Minkowski 几何预计算 3D 查找表加三线性插值；LBFGS 批量 CUDA 实 | [santa-2025#672465-03](https://www.kaggle.com/competitions/santa-2025/discussion/672465) |
| @jeroencottaar | A | 建模与训练 | 每岛 1500 个个体缩到 111：前 27 按 overlap；其余 84 用 overlap 加遗传多样性阈值筛选（Hungarian 近似计算最小变换集） | [santa-2025#672465-04](https://www.kaggle.com/competitions/santa-2025/discussion/672465) |
| @jeroencottaar | B | 建模与训练 | 多岛遗传算法：层级交互、防止单一解支配；所有解用 GPU 松弛到局部极小（LBFGS 批量 CUDA） | [santa-2025#672465-01](https://www.kaggle.com/competitions/santa-2025/discussion/672465) |
| @jeroencottaar | B | 工程/流程 | 岛停滞约 100 代或冠军与他岛重复则重置；岛达到零重叠就缩小方形边界；全群长期不进步才停止；最后 legalize；算力为 250 美元租 1000 小时 RTX 5090 | [santa-2025#672465-05](https://www.kaggle.com/competitions/santa-2025/discussion/672465) |
| @jeroencottaar | C | 复盘与流程 | 作者建议读者等 writeup 与代码整理后再看实现 | [santa-2025#671058-01](https://www.kaggle.com/competitions/santa-2025/discussion/671058) |

## 高票评论

| 票 | 选手 | 日期 | 摘录 | 出处 |
| --- | --- | --- | --- | --- |
| 11 | @cnumber | 2025-11-26 | Thank you for sharing! The main question is, are you using simulated annealing to solve this problem? | [640894](https://www.kaggle.com/competitions/santa-2025/discussion/640894) |

## 关联资产

- 深读：`analysis/deep/santa-2025.md`
- 结构化摘要：`notes/sim-agent/santa-2025.md`
- 归档讨论区：`intel/santa-2025/`（主题 3 条有 ≥50 票帖，图证 8 个）
