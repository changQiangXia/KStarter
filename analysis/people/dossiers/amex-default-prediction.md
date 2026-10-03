# American Express - Default Prediction

> `amex-default-prediction` ｜ Featured ｜ 指标 Amex Custom Gini And X% Percentage Capture ｜ 4874 队 ｜ 截止 2022-08-24

本页汇总该场 **4 条 ≥50 票 GM 主题帖**、**15 条断言**、**11 条高票评论**。

## GM 主题帖

| 票 | 选手 | 日期 | 主题 |
| --- | --- | --- | --- |
| 521 | [@cdeotte](https://www.kaggle.com/cdeotte) | 2022-05-30 | [How To Reduce Data Size](https://www.kaggle.com/competitions/amex-default-prediction/discussion/328054) |
| 271 | [@cdeotte](https://www.kaggle.com/cdeotte) | 2022-08-25 | [14th Place Gold – NN Transformer using LGBM Knowledge Distillation](https://www.kaggle.com/competitions/amex-default-prediction/discussion/347641) |
| 93 | [@jiweiliu](https://www.kaggle.com/jiweiliu) | 2022-08-25 | [10th Place Solution: XGB with Autoregressive RNN features](https://www.kaggle.com/competitions/amex-default-prediction/discussion/347668) |
| 76 | [@titericz](https://www.kaggle.com/titericz) | 2022-08-26 | [13th Place Gold Solution](https://www.kaggle.com/competitions/amex-default-prediction/discussion/348014) |

## 断言（条件→动作→机制→结果）

| 选手 | 等级 | 阶段 | 动作（节选） | 出处 |
| --- | --- | --- | --- | --- |
| @cdeotte | A | 建模与训练 | 先用 LGBM 的 OOF+test 软标签预训练 Transformer，再用硬标签微调；test 数据也参与蒸馏 | [amex-default-prediction#347641-01](https://www.kaggle.com/competitions/amex-default-prediction/discussion/347641) |
| @cdeotte | A | 验证设计 | 10 outer × 10 inner；每个 outer fold 仅用折内标签生成 OOF/test 预测，共 100 个 GBT 模型 | [amex-default-prediction#347641-03](https://www.kaggle.com/competitions/amex-default-prediction/discussion/347641) |
| @jiweiliu | A | 数据理解 | CV 对比：全体 0.7990、长度 13 为 0.8214、其余仅 0.6724；推断短序列是删除了最近月份（保留早期），因此预测缺失月份可帮下游 | [amex-default-prediction#347668-02](https://www.kaggle.com/competitions/amex-default-prediction/discussion/347668) |
| @jiweiliu | A | 特征与数据工程 | 用 1 层 GRU 加 FC 自回归预测下一月特征（log 变换加 fillna(0)）；对 178 个数值特征验证 RMSE 0.019，naive 重复最后月为 0.03；补全 | [amex-default-prediction#347668-03](https://www.kaggle.com/competitions/amex-default-prediction/discussion/347668) |
| @jiweiliu | A | 集成与融合 | 训练 7 个 XGB（不同 RNN/XGB 超参与特征组合）集成 CV 0.7993/public 0.799；与最佳公开方案平均后进金区 | [amex-default-prediction#347668-04](https://www.kaggle.com/competitions/amex-default-prediction/discussion/347668) |
| @titericz | A | 数据工程 | 在 Raddar 数据基础上：按缺失模式为 B、D、P、R、S 特征簇聚类；发现部分连续变量在 (0, 0.01] 加了均匀噪声，用其他特征做滤波去噪（如 B_1 在 0 到 0. | [amex-default-prediction#348014-01](https://www.kaggle.com/competitions/amex-default-prediction/discussion/348014) |
| @titericz | A | 数据工程 | 清洗收益：LGBM 0.7976 到 0.7983、XGB 0.7978 到 0.7986、CatBoost 0.7964 到 0.7968；另 LGBM 5 折到 15 折加 0 | [amex-default-prediction#348014-02](https://www.kaggle.com/competitions/amex-default-prediction/discussion/348014) |
| @titericz | A | 集成与融合 | 两种集成：LGBM stacking 与 CMA 进化策略；最终提交是 3 个集成的平均（LGBM stack 61 模型加两个 CMA 54/55 模型），public 0.80 | [amex-default-prediction#348014-03](https://www.kaggle.com/competitions/amex-default-prediction/discussion/348014) |
| @titericz | A | 复盘与流程 | 有效：知识蒸馏、更长 early stop（3000 到 10000）、大 kfold、全量训练、伪标签；无效：dow 平均后处理、LGBM 样本权重、focal loss、优化  | [amex-default-prediction#348014-04](https://www.kaggle.com/competitions/amex-default-prediction/discussion/348014) |
| @cdeotte | B | 数据工程 | 先逐列最小化 dtype：64 字节 hex ID 取末 16 位转 int64；日期转 datetime 或 3 个 int8；11 个类别列转 int8；177 个 float | [amex-default-prediction#328054-01](https://www.kaggle.com/competitions/amex-default-prediction/discussion/328054) |
| @cdeotte | B | 数据工程 | 用三个属性评估格式：压缩比、行存或列存、是否记住 dtype；Parquet 记住 int8，CSV 不记住需在 read_csv 显式指定 dtype | [amex-default-prediction#328054-02](https://www.kaggle.com/competitions/amex-default-prediction/discussion/328054) |
| @cdeotte | B | 工程/流程 | cuDF 做 GPU 特征工程；GPU XGB 训练；RAPIDS FIL 做 permutation importance（每列 shuffle 10 次 × 10 折） | [amex-default-prediction#347641-04](https://www.kaggle.com/competitions/amex-default-prediction/discussion/347641) |
| @jiweiliu | B | 数据理解 | 把测试集也用于特征生成（只预测特征不预测标签）；短序列因删除了最近的 profile 而信息不足 | [amex-default-prediction#347668-01](https://www.kaggle.com/competitions/amex-default-prediction/discussion/347668) |
| @titericz | B | 复盘与流程 | 赛后发现有 2 个 private 可排 3-4 名的集成，因 CV 较低未被选 | [amex-default-prediction#348014-05](https://www.kaggle.com/competitions/amex-default-prediction/discussion/348014) |
| @cdeotte | C | 建模与训练 | 最终用 4 层无 skip 的 Transformer + 后接 GRU（公共结构为 2 层带 skip） | [amex-default-prediction#347641-02](https://www.kaggle.com/competitions/amex-default-prediction/discussion/347641) |

## 高票评论

| 票 | 选手 | 日期 | 摘录 | 出处 |
| --- | --- | --- | --- | --- |
| 44 | @cdeotte | 2022-06-01 | I published an XGB starter notebook using your data with CV 0.792 and LB 0.794 here. This data is great. It is | [328514](https://www.kaggle.com/competitions/amex-default-prediction/discussion/328514) |
| 41 | @cdeotte | 2022-06-01 | Fantastic job raddar. I was just doing this myself today. When we zoom in on some variables, we see that witho | [328514](https://www.kaggle.com/competitions/amex-default-prediction/discussion/328514) |
| 17 | @cdeotte | 2022-08-25 | Yes, exactly. It's very simple. It's like pseudo labels. Just save your OOF and test predictions. Then train y | [347641](https://www.kaggle.com/competitions/amex-default-prediction/discussion/347641) |
| 16 | @cdeotte | 2022-08-27 | Transformers are hard to train from scratch. The model needs to learn weights for its self attention and weigh | [347641](https://www.kaggle.com/competitions/amex-default-prediction/discussion/347641) |
| 14 | @cdeotte | 2022-08-25 | Congratulations Nischay on your fantastic solo performance. My NN Transformer has a better private LB than LGB | [347641](https://www.kaggle.com/competitions/amex-default-prediction/discussion/347641) |
| 13 | @cdeotte | 2022-08-25 | @kyakovlev Congratulations Konstantin and team. I am so happy for you. You are the best tabular data feature e | [347637](https://www.kaggle.com/competitions/amex-default-prediction/discussion/347637) |
| 11 | @cdeotte | 2022-05-31 | Pandas and cuDF allow you to read a subset of the data rows from the CSV. Therefore i suggest you read the tra | [328054](https://www.kaggle.com/competitions/amex-default-prediction/discussion/328054) |
| 11 | @cdeotte | 2022-06-03 | Great work, i need to update my XGB notebook version. After each update, it would be interesting to take note  | [328514](https://www.kaggle.com/competitions/amex-default-prediction/discussion/328514) |
| 11 | @cdeotte | 2022-08-25 | haha, he groomed me well. I was new to Kaggle then and he invited me to his team when I was like 30th place an | [347637](https://www.kaggle.com/competitions/amex-default-prediction/discussion/347637) |
| 11 | @cdeotte | 2022-08-25 | Hi Joe, congratulations to you and team for achieving 24th out of 5000 teams. That's great. I prepared data ex | [347641](https://www.kaggle.com/competitions/amex-default-prediction/discussion/347641) |
| 10 | @cdeotte | 2022-08-25 | @mrinath Below is my opinion, it might not be fully correct. Pseudo labeling is the process of assigning label | [347641](https://www.kaggle.com/competitions/amex-default-prediction/discussion/347641) |

## 关联资产

- 深读：`analysis/deep/amex-default-prediction.md`
- 结构化摘要：`notes/tabular/amex-default-prediction.md`
- 归档讨论区：`intel/amex-default-prediction/`（主题 4 条有 ≥50 票帖，图证 3 个）
