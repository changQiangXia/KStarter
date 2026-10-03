# Stanford RNA 3D Folding

> `stanford-rna-3d-folding` ｜ Featured ｜ 指标 Ribonanza TM-Score ｜ 1516 队 ｜ 截止 2025-09-24

本页汇总该场 **1 条 ≥50 票 GM 主题帖**、**4 条断言**、**1 条高票评论**。

## GM 主题帖

| 票 | 选手 | 日期 | 主题 |
| --- | --- | --- | --- |
| 97 | [@jaejohn](https://www.kaggle.com/jaejohn) | 2025-09-29 | [1st Place Solution](https://www.kaggle.com/competitions/stanford-rna-3d-folding/discussion/609774) |

## 断言（条件→动作→机制→结果）

| 选手 | 等级 | 阶段 | 动作（节选） | 出处 |
| --- | --- | --- | --- | --- |
| @jaejohn | A | 特征与数据工程 | 五步：搜索→全局对齐→坐标迁移→gap fill（保持 C1'-C1' 约 5.9Å；压缩 gap 用正弦扰动曲率；普通 gap 线性插值；末端沿主干方向延伸）→按置信度自适应精修 | [stanford-rna-3d-folding#609774-04](https://www.kaggle.com/competitions/stanford-rna-3d-folding/discussion/609774) |
| @jaejohn | C | 建模与训练 | 文献与 CASP 结果都显示 template-based modeling 占优 → 从第一天起专注 TBM，90 天只做这一条线 | [stanford-rna-3d-folding#609774-01](https://www.kaggle.com/competitions/stanford-rna-3d-folding/discussion/609774) |
| @jaejohn | C | 验证设计 | 优先保证整体折叠正确，而不是原子级精度 | [stanford-rna-3d-folding#609774-02](https://www.kaggle.com/competitions/stanford-rna-3d-folding/discussion/609774) |
| @jaejohn | C | 工程/流程 | 不改模型本体，集中增强优化与选择：float64 打分、torch.cdist 向量化、预计算三次样条能量函数、PyTorch LBFGS、GPU 加速；另集成 Boltz-1 | [stanford-rna-3d-folding#609774-03](https://www.kaggle.com/competitions/stanford-rna-3d-folding/discussion/609774) |

## 高票评论

| 票 | 选手 | 日期 | 摘录 | 出处 |
| --- | --- | --- | --- | --- |
| 10 | @jaejohn | 2025-09-30 | wow, i just submitted the TBM-only notebook and it scored: 0.59298 my winning score using hybrid approach is:  | [609774](https://www.kaggle.com/competitions/stanford-rna-3d-folding/discussion/609774) |

## 关联资产

- 深读：`analysis/deep/stanford-rna-3d-folding.md`
- 结构化摘要：`notes/science/stanford-rna-3d-folding.md`
- 归档讨论区：`intel/stanford-rna-3d-folding/`（主题 1 条有 ≥50 票帖，图证 0 个）
