# Playground Series S4E1（银行客户流失）轻量深读（Tier B）

> 赛事：Playground ｜ 主题 tabular（二分类，合成数据）｜ 3632 队（当时 Playground 参与纪录）｜ 标准赛 ｜ 指标：ROC AUC
> 材料基础：`digests/playground-series-s4e1.md`（6 篇正文：1st 472502 / 2nd 472496 / 3rd 472413 / 5th 472497 / 17th 472636 / SMOTE 讨论 467034；80 条主题索引）+ 1 张归档图
> 轻读时间：2026-10（Tier B B12）

## 1. 一句话重述与数字账

银行客户流失二分类（AUC）。本场是"**合成数据泄漏**"的教科书案例：2nd 自动枚举 10 个基础特征的 1–10 元子集、检查每个子集是否原样出现在原始数据里（~1000 个 0/1 特征），靠"合成痕迹"把私榜推到 0.90462；1st 则是"单 CatBoost + 20 折平均 + CustomerId/Surname 高基数编码"；3rd 把"几乎所有特征都做 CatBoost 编码"（连 Age、EstimatedSalary 都转整数再编码）拿到 99 票的第三名。反例是 5th——明确不用泄漏、单 XGB + 大量 LAG/LEAD 真实业务特征，也拿到 0.902。

| 关键数字 | 值 | 来源 |
| --- | --- | --- |
| 1st（472502） | 单个 CatBoost 模型 **20 折平均**；关键 = `CustomerId` 与 `Surname` 高基数类别的正确编码；自述"CatBoost 调好参就能前 3" | 472502 |
| 2nd（472496） | 合成痕迹特征：对 10 个基础特征自动生成 **1–10 元全部子集**，检查是否原样出现在原始数据集（0/1），加 `CustomerId+Surname` 子集；LGBM（50 特征）私榜 0.90203；AutoGluon `best_quality` 4 小时 0.90378；**（LGBM+AG）/2 = 0.90462（最终第 2）**；paddykb "feeling lucky" 技巧 +0.01 | 472496 |
| 3rd（472413） | "CatBoost Encoding Galore"：TF-IDF + TruncatedSVD（Surname 4 维）；**除 Balance/HasCrCard 外全部编码**（Age×10、EstimatedSalary×100 转整数以便编码）；`has_time=True` 保持顺序、原数据排在竞赛数据之前；7 模型（LR/NN/XGB/LGBM/3×CatBoost 不同 bootstrap）用 Ridge 定权重；5 折实验 → **30 折提交（约 12 小时）**；原数据拼接两次私榜最佳；使用 paddykb 泄漏后处理 | 472413 |
| 5th（472497） | 单 XGBoost + 大量窗口特征（按 CustomerId/Surname/Age 分组的 LAG/LEAD、比值、聚合）；CV 0.9030 / 私榜 0.902；**明确不使用泄漏**，并称"反转泄漏数据对自己的模型无帮助" | 472497 |
| 17th（472636） | AutoGluon "Frankenstein II" 三层堆叠 + 历史模型平均；OpenFE 470 特征 → BorutaSHAP+RFECV 保留 103；CleanLab 重标注；两版提交：WeightedEnsemble_L3 私 0.89637 vs 最终平均版 私 0.90106；失败清单：PCA/ICA、单模型 boosting、TabPFN、Surname 特征、原始数据 | 472636 |
| 社区 | "Feeling lucky? Add ~0.002 to your LB"（32 票 / 24 评论）；榜单洗牌可视化（34 票）；SMOTE/SMOTEENN/ADASYN 自述无正收益且过拟合（12 票）；参与数创 Playground 纪录（22 票） | 索引 |

## 2. 逐方案对照矩阵

| 维度 | 1st | 2nd | 3rd | 5th | 17th |
| --- | --- | --- | --- | --- | --- |
| 主模型 | 单 CatBoost ×20 折 | LGBM + AutoGluon 平均 | 7 模型 Ridge 加权 | 单 XGB | AutoGluon 三层栈 + 平均 |
| 核心特征 | CustomerId/Surname 编码 | ~1000 个"子集是否在原数据"特征 | TF-IDF+SVD + 全量 CatBoost 编码 | LAG/LEAD 窗口 + 比值 | OpenFE 470 → 103（Boruta/RFECV） |
| 用泄漏？ | 否（但用高基数编码） | **是（合成痕迹）** | 是（paddykb 后处理） | **否** | 部分（公开思路） |
| 折数 | 20 | — | 5 → 30 | CV 0.9030 | — |
| 私榜 | 1st | 0.90462（2nd） | 3rd | 0.902（5th） | 0.90106（17th） |

## 3. 共识、分歧与裁决

### 共识一：合成痕迹/泄漏主导本场公榜（2nd、3rd、社区；置信度高）

2nd 的 ~1000 个"子集出现"特征把"这段数据是否来自原始数据集"变成特征，官方目标均值 21% 在不同子集上显著偏移；paddykb 的"feeling lucky"后处理被 3rd 采用、被 2nd 计为 +0.01。**裁决**：合成 Playground 上，先做"与原始数据比对"的痕迹分析是首要动作；这是合法但强依赖赛制的技巧。置信度：高。

### 分歧一：要不要用泄漏（2nd/3rd vs 5th；置信度中高）

5th 用纯业务特征（窗口 LAG/LEAD 等）拿到 0.902，明确拒绝泄漏；2nd/3rd 靠痕迹特征与后处理站上领奖台。**裁决**：不用泄漏也能进前 5，但在本场它是前 3 的"增长引擎"；是否采用取决于赛事规则与个人取向，且必须在 CV 中验证其稳定性。置信度：中高。

### 共识二：CatBoost 及其类别编码是核心工具（1st、3rd；置信度中高）

1st 单 CatBoost 20 折夺冠；3rd 把 CatBoost 编码扩展到几乎所有列（含整数化的 Age/EstimatedSalary），并强调 `has_time=True` 与"原数据在前"的顺序效应。**裁决**：高基数类别（CustomerId/Surname）的编码方式是本场的分水岭；CatBoost 在此类合成表格数据上优势明显。置信度：中高。

### 共识三：折数与多折平均的稳定增益（1st、3rd、2nd；置信度中高）

1st 用 20 折平均单模型；3rd 从 5 折提到 30 折；2nd 用两模型平均。**裁决**：该数据噪声小、信号强，多折平均提升稳定（3rd 的 30 折耗时约 12 小时）。置信度：中高。

### 共识四：不平衡重采样（SMOTE/ADASYN）没有正收益（467034、各前排方案；置信度中）

社区帖报告 SMOTE/SMOTEENN/ADASYN 导致过拟合；前排方案无一依赖重采样。**裁决**：AUC 指标下优先用类别权重/阈值不动，不做重采样。置信度：中。

## 4. 证据分级

| 断言 | 等级 | 说明 |
| --- | --- | --- |
| 2nd 的合成痕迹特征与 0.90462 | 自述（伪代码 + 分数） | 中高 |
| 3rd 的编码体系与 30 折 | 自述 + 99 票社区认可 | 中高 |
| 1st 的单 CatBoost 20 折 | 自述（简短） | 中 |
| 5th 的无泄漏 0.902 | 自述（特征清单完整） | 中高 |
| 17th 的特征选择与 AutoGluon 栈 | 自述 + 结构图 | 中 |
| SMOTE 无效 | 单帖 + 前排方案旁证 | 中 |

## 5. 悬案与缺口（登记）

- 1st 的 CatBoost 参数与编码细节未展开（帖极短）；
- paddykb 泄漏后处理的原理未在归档正文说明（只有标题与 +0.002/+0.01 效果）；
- "反转泄漏数据"的具体实验（5th）未展开；
- 归档 1 图（AutoGluon 栈示意图，超宽）可读性一般；
- **图证缺口**：无分数/分布类图。

## 6. 图表证据

![AutoGluon 三层栈示意](../../intel/playground-series-s4e1/bodies/472636_img/01.png)

**图 1**（topic 472636，17th）：AutoGluon "Frankenstein II" 的三层堆叠结构（L1 大量基模型 → L2 加权集成 → L3 最终集成）——本场唯一归档图，超宽示意。

## 7. 出处

- 1st（43 票 / 35 评论）：https://www.kaggle.com/competitions/playground-series-s4e1/discussion/472502
- 2nd（82 票 / 42 评论）：https://www.kaggle.com/competitions/playground-series-s4e1/discussion/472496
- 3rd CatBoost Encoding Galore（99 票 / 53 评论）：https://www.kaggle.com/competitions/playground-series-s4e1/discussion/472413
- 5th 无泄漏单 XGB（9 票）：https://www.kaggle.com/competitions/playground-series-s4e1/discussion/472497
- 17th AutoGluon（11 票）：https://www.kaggle.com/competitions/playground-series-s4e1/discussion/472636
- Feeling lucky（32 票 / 24 评论）：https://www.kaggle.com/competitions/playground-series-s4e1/discussion/469859
- SMOTE 等重采样讨论（12 票）：https://www.kaggle.com/competitions/playground-series-s4e1/discussion/467034
- 榜单洗牌可视化（34 票）：https://www.kaggle.com/competitions/playground-series-s4e1/discussion/472397
- 参与数纪录（22 票）：https://www.kaggle.com/competitions/playground-series-s4e1/discussion/470362
