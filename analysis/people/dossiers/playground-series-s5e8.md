# Binary Classification with a Bank Dataset

> `playground-series-s5e8` ｜ Playground ｜ 指标 Roc Auc Score ｜ 3365 队 ｜ 截止 2025-08-31

本页汇总该场 **1 条 ≥50 票 GM 主题帖**、**3 条断言**、**0 条高票评论**。

## GM 主题帖

| 票 | 选手 | 日期 | 主题 |
| --- | --- | --- | --- |
| 69 | [@cdeotte](https://www.kaggle.com/cdeotte) | 2025-08-20 | [XGBoost - QuantileDMatrix Trick](https://www.kaggle.com/competitions/playground-series-s5e8/discussion/600048) |

## 断言（条件→动作→机制→结果）

| 选手 | 等级 | 阶段 | 动作（节选） | 出处 |
| --- | --- | --- | --- | --- |
| @cdeotte | A | 工程/流程 | hist 把每列分成 256 bin，每个数变成 1 字节（32bit 压 4 倍、64bit 压 8 倍），因此能训比想象更大的数据 | [playground-series-s5e8#600048-01](https://www.kaggle.com/competitions/playground-series-s5e8/discussion/600048) |
| @cdeotte | A | 工程/流程 | QuantileDMatrix 分批加载并即时压缩（4GB 数据分 4 批各 1GB 压到 250MB），显存需求大幅下降；再配合 int64→int32、float64→floa | [playground-series-s5e8#600048-02](https://www.kaggle.com/competitions/playground-series-s5e8/discussion/600048) |
| @cdeotte | A | 工程/流程 | notebook A 做 GPU 特征工程并存盘；notebook B 从磁盘按 16k 行读取、转 GPU 并压缩成 QuantileDMatrix；原 15GB 数据只在磁盘， | [playground-series-s5e8#600048-03](https://www.kaggle.com/competitions/playground-series-s5e8/discussion/600048) |

## 高票评论

_无 ≥10 票评论_

## 关联资产

- 深读：`analysis/deep/playground-series-s5e8.md`
- 结构化摘要：`notes/tabular/playground-series-s5e8.md`
- 归档讨论区：`intel/playground-series-s5e8/`（主题 1 条有 ≥50 票帖，图证 0 个）
