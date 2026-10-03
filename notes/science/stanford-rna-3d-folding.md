# Stanford RNA 3D Folding（Part 1）

> 主题：science ｜ 子类：— ｜ 领域：结构生物学 ｜ 类别：Featured
> 截止：2024-XX-XX ｜ 队伍数：1800+ ｜ 机制：代码赛 ｜ 指标：结构相似度（TM-score 类）
> 数据来源：`intel/stanford-rna-3d-folding/`（80 条主题索引 + 6 篇 write-up 正文）

## 1. 任务与数据

- 预测目标：由 RNA 序列预测三级结构（3D 坐标）。
- 数据形态：序列 + 实验解析结构（PDB 体系）；样本量小、结构标注昂贵。
- 与 Part 2 的区别：本场（Part 1）受**算力限制更明显**，多队采用模板/检索式方法。

## 2. 方案谱系

| 方案 | 名次 | 关键点 |
| --- | --- | --- |
| **"没有 GPU"的路线选择** | 1st | 作者明确说明"没有 GPU，从头训练模型不现实"，因此选择检索/模板类方法并做精细实现 |
| **模板建模（TBM）** | 2nd | 作者有 CASP 参赛经验：从已知结构中找相似模板并迁移原子坐标 |
| 临时登顶方案 | 高票帖 | 见讨论区 |
| 3rd 方案 | 3rd | 见讨论区 |

## 3. 关键技巧

- **算力约束决定方法路线**：小算力下"检索 + 模板"往往优于从头训练（与 Part 2 的结论一致）。
- **领域数据处理能力**（PDB 解析、结构对齐）是核心壁垒。
- **模板检索 + 坐标迁移**：在结构预测里是最古老也最有效的方法之一。
- 关注评测细节：结构相似度指标需要本地精确复现。

## 4. 可迁移性评估

- **可直接迁移**：
  - **"先看算力预算，再选方法路线"**——小算力走检索/模板，大算力才考虑端到端训练。
  - 检索式方法（找相似样本迁移结果）在各领域的低算力场景通用。
- 需要前提：结构生物学工具链（PDB/CASP 体系）与对齐算法。
- 不建议照搬：无视算力约束强行端到端训练。

## 5. 对新手的关键启示

1. **算力也是约束条件**：冠军的胜利部分来自"认清自己没有 GPU"。
2. **检索/模板方法被低估**，在结构类任务里常是最优解。
3. 与 Part 2 对照可见同一问题的两条路线：**模板/物理方法** vs **预训练大模型 + 领域特征**。

## 6. 出处

- 讨论区索引：`intel/stanford-rna-3d-folding/topics.md`（80 条）
- 已收录 write-up（6 篇）：
  - 1st（97 票）：https://www.kaggle.com/competitions/stanford-rna-3d-folding/discussion/609774
  - 3rd（16 票）：https://www.kaggle.com/competitions/stanford-rna-3d-folding/discussion/609701
  - 方案说明（121 票）：https://www.kaggle.com/competitions/stanford-rna-3d-folding/discussion/566906
  - 临时登顶说明（20 票）：https://www.kaggle.com/competitions/stanford-rna-3d-folding/discussion/582295
