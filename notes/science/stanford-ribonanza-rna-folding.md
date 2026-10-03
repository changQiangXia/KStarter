# Stanford Ribonanza - RNA Folding

> 主题：science ｜ 子类：— ｜ 领域：结构生物学 ｜ 类别：Research
> 截止：2023-12-07 ｜ 队伍数：755 ｜ 机制：标准赛 ｜ 指标：化学位移预测（多目标回归）
> 数据来源：`intel/stanford-ribonanza-rna-folding/`（80 条主题索引 + 6 篇 write-up 正文）

## 1. 任务与数据

- 预测目标：预测 RNA 序列中每个碱基的**化学位移**（多目标、逐碱基回归），是 RNA 结构预测的代用任务。
- 数据形态：序列 + 逐位点实验测量；含**公开的补充数据**（可加入训练）。
- 构造陷阱：
  - 逐位点回归 + 大量目标（多输出）；
  - 实验噪声；
  - 序列长度差异大。

## 2. 方案谱系

| 方案 | 名次 | 关键点 |
| --- | --- | --- |
| **Transformer + 动态位置编码** | 1st | 用动态位置编码处理不同长度序列；多目标回归 |
| 其他方案 | 见讨论区 | |

## 3. 关键技巧

- **动态/相对位置编码**（处理长度差异大的序列，与 IceCube 的相对时空偏置同源）。
- **多目标回归**（每个碱基多个化学位移通道）。
- **外部补充数据**的使用。

## 4. 可迁移性评估

- **可直接迁移**：
  - 变长序列用相对/动态位置编码；
  - 多输出回归的共享主干；
  - 生物序列任务的代用目标设计（化学位移 → 结构）。
- 需要前提：序列建模与生物信息基础。
- 不建议照搬：绝对位置编码处理极端变长序列。

## 5. 对新手的关键启示

1. **代用目标（proxy task）是科学比赛的常见设计**（化学位移 → 结构；指纹 → 结合）。
2. 变长序列优先用相对/动态位置编码。
3. 与 Stanford RNA 3D Folding（同校系列）、CAFA、Leash-BELKA 对照：**生物分子类比赛的主线是"表示 + 领域先验"**。

## 6. 出处

- 讨论区索引：`intel/stanford-ribonanza-rna-folding/topics.md`（80 条）
- 已收录 write-up（6 篇）：
  - 1st Transformer + 动态位置编码（147 票）：https://www.kaggle.com/competitions/stanford-ribonanza-rna-folding/discussion/460121
  - 2nd Squeezeformer + BPP（42 票）：https://www.kaggle.com/competitions/stanford-ribonanza-rna-folding/discussion/460316
  - 7th（44 票）：https://www.kaggle.com/competitions/stanford-ribonanza-rna-folding/discussion/460190
