# OTTO – Multi-Objective Recommender System

> `otto-recommender-system` ｜ Featured ｜ 指标 WeightedRecall@{K} ｜ 2574 队 ｜ 截止 2023-01-31

本页汇总该场 **2 条 ≥50 票 GM 主题帖**、**7 条断言**、**0 条高票评论**。

## GM 主题帖

| 票 | 选手 | 日期 | 主题 |
| --- | --- | --- | --- |
| 335 | [@cdeotte](https://www.kaggle.com/cdeotte) | 2022-12-03 | [How To Build a GBT Ranker Model](https://www.kaggle.com/competitions/otto-recommender-system/discussion/370210) |
| 151 | [@cdeotte](https://www.kaggle.com/cdeotte) | 2023-02-01 | [3rd Place - Using Only Rules Achieves LB 0.590!](https://www.kaggle.com/competitions/otto-recommender-system/discussion/383013) |

## 断言（条件→动作→机制→结果）

| 选手 | 等级 | 阶段 | 动作（节选） | 出处 |
| --- | --- | --- | --- | --- |
| @cdeotte | A | 集成与融合 | 按每个 target type 的用户内 rank 相加做融合 | [otto-recommender-system#383013-01](https://www.kaggle.com/competitions/otto-recommender-system/discussion/383013) |
| @cdeotte | A | 集成与融合 | 三件套：(1) 候选从 20 扩到 50；(2) 用 covisit 计数做 user-item 交互特征；(3) 扩展到 20 个 covisit 矩阵（时间衰减、前进/双向、仅 | [otto-recommender-system#383013-02](https://www.kaggle.com/competitions/otto-recommender-system/discussion/383013) |
| @cdeotte | B | 建模与训练 | 先用共访矩阵等方法生成 50-200 个候选，再用 GBT ranker 排序取最终 20；训练表每行一个 session-aid 对，含 user/item/交互特征与 clic | [otto-recommender-system#370210-01](https://www.kaggle.com/competitions/otto-recommender-system/discussion/370210) |
| @cdeotte | B | 验证设计 | 前 3 周训练、最后 1 周验证；再把验证周拆成 A/B，A 当测试输入、B 当标签 | [otto-recommender-system#370210-02](https://www.kaggle.com/competitions/otto-recommender-system/discussion/370210) |
| @cdeotte | B | 数据工程 | 持续把每列 dtype 降到最小（int32/float32）；cuDF 22.08+ 可设默认 32 位；仍不够就分块落盘或用 DASK | [otto-recommender-system#370210-03](https://www.kaggle.com/competitions/otto-recommender-system/discussion/370210) |
| @cdeotte | B | 验证设计 | GroupKFold 按 user 分 5 折；DMatrix 用 group 标记每 50 个候选一组；user/item 列不作为特征 | [otto-recommender-system#370210-04](https://www.kaggle.com/competitions/otto-recommender-system/discussion/370210) |
| @cdeotte | B | 工程/流程 | 用 RAPIDS cuDF 在 4×V100 上生成矩阵，每个 covisit 矩阵 <1 分钟；共试了几百个矩阵并逐个算 local CV | [otto-recommender-system#383013-03](https://www.kaggle.com/competitions/otto-recommender-system/discussion/383013) |

## 高票评论

_无 ≥10 票评论_

## 关联资产

- 深读：`analysis/deep/otto-recommender-system.md`
- 结构化摘要：`notes/tabular/otto-recommender-system.md`
- 归档讨论区：`intel/otto-recommender-system/`（主题 2 条有 ≥50 票帖，图证 0 个）
