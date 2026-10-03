# Novozymes Enzyme Stability Prediction

> `novozymes-enzyme-stability-prediction` ｜ Featured ｜ 指标 SpearmanR ｜ 2482 队 ｜ 截止 2023-01-03

本页汇总该场 **2 条 ≥50 票 GM 主题帖**、**9 条断言**、**1 条高票评论**。

## GM 主题帖

| 票 | 选手 | 日期 | 主题 |
| --- | --- | --- | --- |
| 218 | [@cdeotte](https://www.kaggle.com/cdeotte) | 2022-10-07 | [How To Use Kaggle's Train Data](https://www.kaggle.com/competitions/novozymes-enzyme-stability-prediction/discussion/358320) |
| 169 | [@cdeotte](https://www.kaggle.com/cdeotte) | 2023-01-04 | [1st Place Public - Shakedown to 967th Place Private - Hahaha](https://www.kaggle.com/competitions/novozymes-enzyme-stability-prediction/discussion/376116) |

## 断言（条件→动作→机制→结果）

| 选手 | 等级 | 阶段 | 动作（节选） | 出处 |
| --- | --- | --- | --- | --- |
| @cdeotte | A | 特征与数据工程 | 先按 ≤2 个突变把训练蛋白分组，用组内多数氨基酸推断野生型，再构造野生型-单突变对（与测试同构） | [novozymes-enzyme-stability-prediction#358320-02](https://www.kaggle.com/competitions/novozymes-enzyme-stability-prediction/discussion/358320) |
| @cdeotte | A | 特征与数据工程 | 对每组 Tm 排名后除以组大小得到 1/N 到 N/N 作为目标；组规模小于 25 的小组剔除（否则 0/1 目标偏置） | [novozymes-enzyme-stability-prediction#358320-04](https://www.kaggle.com/competitions/novozymes-enzyme-stability-prediction/discussion/358320) |
| @cdeotte | A | 工程/流程 | 利用规则：全 0 提交报错且不扣次数；2 次提交定位切分：public 为 df.iloc[:541] 加 df.iloc[1757:] 加 df.iloc[1169]；publi | [novozymes-enzyme-stability-prediction#376116-02](https://www.kaggle.com/competitions/novozymes-enzyme-stability-prediction/discussion/376116) |
| @cdeotte | A | 特征与数据工程 | 用 RSASA（相对溶剂可及表面积）单特征；简单融合 50% Rosetta energy 加 50% RSASA（25% wildtype 加 25% mutation） | [novozymes-enzyme-stability-prediction#376116-03](https://www.kaggle.com/competitions/novozymes-enzyme-stability-prediction/discussion/376116) |
| @cdeotte | A | 复盘与流程 | 被怀疑过拟合的 RF（public 0.829）最终 private 546 第一；赛后把 RF 调 depth=4 得 public 655 / private 558；hill | [novozymes-enzyme-stability-prediction#376116-04](https://www.kaggle.com/competitions/novozymes-enzyme-stability-prediction/discussion/376116) |
| @cdeotte | B | 数据理解 | 把任务理解为同一野生型上 2413 个单点突变的 dTm 排序；提交 dTm 而非 Tm（排名等价） | [novozymes-enzyme-stability-prediction#358320-01](https://www.kaggle.com/competitions/novozymes-enzyme-stability-prediction/discussion/358320) |
| @cdeotte | B | 验证设计 | 用 public test 当验证：先生成大量单模型与特征，再 probe LB 取回 public 标签，用它们训 level-2 模型 | [novozymes-enzyme-stability-prediction#376116-01](https://www.kaggle.com/competitions/novozymes-enzyme-stability-prediction/discussion/376116) |
| @cdeotte | C | 数据工程 | 统计组内 (data_source, pH) 组合出现次数，只保留最高频组合并丢弃其余 | [novozymes-enzyme-stability-prediction#358320-03](https://www.kaggle.com/competitions/novozymes-enzyme-stability-prediction/discussion/358320) |
| @cdeotte | C | 特征与数据工程 | 把该位置的最差稳定性赋给 delete mutation 行（按 position 取 min） | [novozymes-enzyme-stability-prediction#376116-05](https://www.kaggle.com/competitions/novozymes-enzyme-stability-prediction/discussion/376116) |

## 高票评论

| 票 | 选手 | 日期 | 摘录 | 出处 |
| --- | --- | --- | --- | --- |
| 11 | @cdeotte | 2023-01-04 | Most of my ideas originated from something someone shared in discussion or notebook. When i start reading how  | [376116](https://www.kaggle.com/competitions/novozymes-enzyme-stability-prediction/discussion/376116) |

## 关联资产

- 深读：`analysis/deep/novozymes-enzyme-stability-prediction.md`
- 结构化摘要：`notes/science/novozymes-enzyme-stability-prediction.md`
- 归档讨论区：`intel/novozymes-enzyme-stability-prediction/`（主题 2 条有 ≥50 票帖，图证 7 个）
