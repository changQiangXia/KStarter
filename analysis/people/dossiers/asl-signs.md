# Google - Isolated Sign Language Recognition

> `asl-signs` ｜ Research ｜ 指标 PostProcessorKernelDesc ｜ 1165 队 ｜ 截止 2023-05-01

本页汇总该场 **1 条 ≥50 票 GM 主题帖**、**3 条断言**、**0 条高票评论**。

## GM 主题帖

| 票 | 选手 | 日期 | 主题 |
| --- | --- | --- | --- |
| 73 | [@cdeotte](https://www.kaggle.com/cdeotte) | 2023-05-02 | [44th Place Silver - How To Improve Best Public Notebook](https://www.kaggle.com/competitions/asl-signs/discussion/406302) |

## 断言（条件→动作→机制→结果）

| 选手 | 等级 | 阶段 | 动作（节选） | 出处 |
| --- | --- | --- | --- | --- |
| @cdeotte | A | 工程/流程 | 先缩小 LANDMARK_UNITS、UNITS、MLP_RATIO 到不影响 CV 的最小；小于 5M 参数时可用 FP16 塞 4 份模型（40MB 上限对应 20M 参数）； | [asl-signs#406302-01](https://www.kaggle.com/competitions/asl-signs/discussion/406302) |
| @cdeotte | A | 建模与训练 | blocks 2 到 3（约加 0.01 到 0.02）；MLP_RATIO 4 到 3 省参数；INPUT_SIZE 64 到 12（提速且意外加 0.01 到 0.02）；N_ | [asl-signs#406302-02](https://www.kaggle.com/competitions/asl-signs/discussion/406302) |
| @cdeotte | A | 复盘与流程 | 11 处改动把 public LB 0.73 提到 0.77（CV/LB 加约 0.03），最终 44th Silver；外部数据无益；只有 frame dropout 与 tim | [asl-signs#406302-03](https://www.kaggle.com/competitions/asl-signs/discussion/406302) |

## 高票评论

_无 ≥10 票评论_

## 关联资产

- 深读：`analysis/deep/asl-signs.md`
- 结构化摘要：`notes/tabular/asl-signs.md`
- 归档讨论区：`intel/asl-signs/`（主题 1 条有 ≥50 票帖，图证 0 个）
