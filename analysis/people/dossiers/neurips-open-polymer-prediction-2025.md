# NeurIPS - Open Polymer Prediction 2025

> `neurips-open-polymer-prediction-2025` ｜ Featured ｜ 指标 open_polymer_2025 ｜ 2240 队 ｜ 截止 2025-09-15

本页汇总该场 **1 条 ≥50 票 GM 主题帖**、**5 条断言**、**0 条高票评论**。

## GM 主题帖

| 票 | 选手 | 日期 | 主题 |
| --- | --- | --- | --- |
| 116 | [@jsday96](https://www.kaggle.com/jsday96) | 2025-09-17 | [1st Place Solution](https://www.kaggle.com/competitions/neurips-open-polymer-prediction-2025/discussion/607947) |

## 断言（条件→动作→机制→结果）

| 选手 | 等级 | 阶段 | 动作（节选） | 出处 |
| --- | --- | --- | --- | --- |
| @jsday96 | A | 后处理 | 用正负 0.1 倍标准差探针发现 Tg 异常；按 V 形曲线拟合最优偏移系数 0.5644，提交时给 Tg 预测整体加上标准差乘 0.5644 | [neurips-open-polymer-prediction-2025#607947-01](https://www.kaggle.com/competitions/neurips-open-polymer-prediction-2025/discussion/607947) |
| @jsday96 | A | 建模与训练 | 用 BERT、Uni-Mol、AutoGluon、D-MPNN 集成给 PI1M 的 5 万个假想聚合物打伪标签；再用性质高低成对比较的排序分类任务预训练（相似对忽略 loss）， | [neurips-open-polymer-prediction-2025#607947-02](https://www.kaggle.com/competitions/neurips-open-polymer-prediction-2025/discussion/607947) |
| @jsday96 | A | 特征与数据工程 | 训练期用随机非 canonical SMILES 每输入生成 10 个变体（数据约 10 倍）；测试期同法生成 50 个预测并取中位数（随机幅度 5 倍） | [neurips-open-polymer-prediction-2025#607947-04](https://www.kaggle.com/competitions/neurips-open-polymer-prediction-2025/discussion/607947) |
| @jsday96 | A | 建模与训练 | 对照：ChemBERTa CV 0.0634、polyBERT 0.592、ModernBERT-base 0.0584、ModernBERT-large 0.0587；CodeB | [neurips-open-polymer-prediction-2025#607947-05](https://www.kaggle.com/competitions/neurips-open-polymer-prediction-2025/discussion/607947) |
| @jsday96 | B | 特征与数据工程 | 五策略：isotonic 重标定、按误差阈值过滤、逐数据集样本权重（Optuna 调）、人工规则（RadonPy 中 Tc 大于 0.402 的行丢弃）、自生成 MD 数据改用 s | [neurips-open-polymer-prediction-2025#607947-03](https://www.kaggle.com/competitions/neurips-open-polymer-prediction-2025/discussion/607947) |

## 高票评论

_无 ≥10 票评论_

## 关联资产

- 深读：`analysis/deep/neurips-open-polymer-prediction-2025.md`
- 结构化摘要：`notes/science/neurips-open-polymer-prediction-2025.md`
- 归档讨论区：`intel/neurips-open-polymer-prediction-2025/`（主题 1 条有 ≥50 票帖，图证 1 个）
