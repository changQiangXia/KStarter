# Playground Series S4E10（贷款获批预测）轻量深读（Tier B）

> 赛事：Playground ｜ 主题 tabular（金融贷款二分类，合成数据）｜ 3858 队 ｜ 标准赛 ｜ 指标：ROC AUC
> 材料基础：`digests/playground-series-s4e10.md`（6 篇正文：1st 543725 / 2nd 543766 / 8th 543772 / 10th 543735 / LLM 方案 543734 / 新手提示 539612；80 条主题索引）+ 5 张归档图
> 轻读时间：2026-10（Tier B B14）

## 1. 一句话重述与数字账

预测贷款是否获批（AUC）。本场是"**CatBoost 一枝独秀 + 数值列当类别**"的教科书：1st 把每个数值特征都再存一份类别副本（全类别化），用 Optuna 给 XGB/LGBM/CatBoost 各找 10 组超参并平均，再加一个 NN；真正的"秘密武器"是把每个模型的预测当 baseline 再训一个 **CatBoost 残差提升器**（连 CatBoost 自己的预测也能再被它提升）；最后用 NN 堆叠 4 路预测：CV 0.97059 / 公 0.97344 / 私 **0.96938**。

| 关键数字 | 值 | 来源 |
| --- | --- | --- |
| 1st（543725） | 数值特征保留"数值 + 类别副本"；不做其他 FE；加入原始数据；XGB/LGBM/CatBoost 各 10 组 Optuna 超参平均（参考大 max_bin 技巧）+ 一个 paddykb 风格的 NN；**用 CatBoost 以各模型预测为 baseline（init_score）再训练**：LGBM .96811→.96856、XGB .96767→.96815、CatBoost .96972→.96997、NN .96678→.96732；最终 NN 堆叠 → CV 0.97059 / 公 0.97344 / 私 0.96938；自述"CatBoost 提升版单独就够第 3" | 543725 |
| 2nd（543766） | 方案简单：用原始数据 + 少量 FE 做多样性；**没有选 LB 最高的版本**（0.97350 / CV 0.96954），最终两份提交为 21 模型（CV 0.97107 / LB 0.97217）与 24 模型（CV 0.97026 / LB 0.97335）；致谢 siukeitin 与 paddykb 的"全类别"notebook | 543766 |
| 8th（543772） | 5 条预处理流水线（其中 3 条用原始数据但只进训练）；CatBoost 全特征当类别；模型池 = CatBoost/XGB/LGBM(GBDT/DART/GOSS)/HGB/GB/AutoGluon/NN；AutoGluon 融合 **52 个 OOF**（24 小时，CV 0.970887 / 私 0.96900）；另一份多层 Ridge+LR 融合——**减少 OOF 数量反而更好**（暴力法选 19 个，RFECV 更差） | 543772 |
| 10th（543735） | "No blind blend"：4 个元学习器（每个是 GBM 栈）→ LogisticRegression 融合；为稳健性每个配置跑 4 个随机种子并画箱线图；训练 30+ GBM 探索三个库的分类超参；person_income 等列同时保留类别与数值；不插补、不 FE；原始数据只进训练 | 543735 |
| LLM 方案（543734） | 用 LLM 写"通用好方案"：最终 **789 名（top 21%）**；自述 GPT-4o1-preview 长上下文对调试帮助大，能写复杂 NN 架构；BlueCast（AutoML）约 1000 名；FE 无明显收益；无监督模型（Isolation Forest）经有监督式调参从 ~0.78 提到 0.84+ | 543734 |
| 社区与提示 | 新手贴（55 票 / 63 评论）：读 Rules/Overview/Data、认准指标、预期噪声、取原始数据、读讨论与公开 notebook、先自己查、**避免盲混**；XGBoost 大 `max_bin` 提分（34 票）；"数据有明显分组"（34 票）；线性 booster 当集成器（33 票）；原数据提升 CV+LB（25 票 / 50 评论）；RF 也能 0.96（25 票） | 索引 |

## 2. 逐方案对照矩阵

| 维度 | 1st | 2nd | 8th | 10th |
| --- | --- | --- | --- | --- |
| 核心 | 全类别化 + CatBoost 残差提升 + NN 堆叠 | 简单多模型 + 谨慎提交 | 5 流水线 + AutoGluon/多层融合 | 4 个 GBM 栈 → LR |
| 类别处理 | 数值 + 类别双份 | 全类别（paddykb 风） | CatBoost 全类别 | 数值 + 类别双份 |
| 原数据 | 加入 | 加入 | 3 条流水线 | 仅训练 |
| 特殊技巧 | CatBoost 以预测为 baseline | 不选最高 LB | 减少 OOF 数量 | 多随机种子箱线图 |
| 私榜 | **0.96938** | 0.97217/0.97335（公榜） | 0.96900 | — |

## 3. 共识、分歧与裁决

### 共识一：数值列"同时保留数值 + 类别副本"、CatBoost 全类别化是本场最大共性增益（1st、2nd、8th、10th；置信度高）

四人都在做这件事；2nd 明确称 paddykb 的"all features as categories"是 game-changer。**裁决**：在合成金融表格上，"离散化 + 类别处理"比连续建模更贴合生成机制；CatBoost 的类别处理能力被最大化利用。置信度：高。

### 共识二：CatBoost 是本场最强模型族，且可作"残差提升器"（1st；置信度中高）

1st 的 CatBoost 单族 CV 0.96972 已高于 XGB/LGBM；把任意模型预测当 baseline 再训 CatBoost 可再涨（含 CatBoost 自己）。**裁决**：模型同族化时，用强模型做"二次提升（init_score）"是低成本的稳定增益。置信度：中高。

### 共识三：原始数据只入训练、CV 只算合成数据（1st、8th、10th、社区 25 票帖；置信度中高）

与 S3E3/S4E1/S3E11/S3E15 完全同型；社区实测原数据同时提升 CV 与公榜。**裁决**：标准协议。置信度：中高。

### 事件一："盲混"被反复警告（539612、543735；置信度中高）

新手贴把"blind blending"列为最大陷阱（短期快乐、私榜疼痛）；10th 的方案标题就是 "no blind blend"。**裁决**：权重必须由 OOF/结构决定；公开 notebook 的盲混是负期望策略。置信度：中高。

### 事件二：LLM 全自动方案只到 top 21%（543734；置信度中）

LLM 写出的"通用好方案"789 名；人主导的类别化/CatBoost 残差提升等比赛特有技巧仍是差距来源。**裁决**：LLM 可代写代码与探索架构，但"读数据 + 选方向"仍决定上限。置信度：中。

## 4. 证据分级

| 断言 | 等级 | 说明 |
| --- | --- | --- |
| 1st 的 CatBoost baseline 提升与全部 CV/公私榜 | 自述（含完整表格） | 高 |
| 8th 的 52 OOF AutoGluon 与 19 模型多层融合 | 自述 + CV 图 | 中高 |
| 10th 的 4 元学习器与种重复 | 自述 + 箱线图 | 中高 |
| 2nd 的提交选择 | 自述 | 中 |
| 社区（max_bin/分组/原数据） | 高票帖 | 中高 |
| LLM 方案 789 名 | 自述 | 中 |

## 5. 悬案与缺口（登记）

- 3rd–7th、9th 方案未收录；
- "There are clear groups in data"（34 票）未细读；
- 线性 booster 当集成器（33 票）未展开；
- **图证缺口**：无（5 张图，本深读内嵌 2 张）。

## 6. 图表证据

![10th 的 OOF AUC 箱线图](../../intel/playground-series-s4e10/bodies/543735_img/01.png)

**图 1**（topic 543735，10th）：各基模型与集成的 OOF AUC 箱线图（4 个种子重复）——集成（0.97041）稳居民模型之上。

![8th 的模型 CV 对比](../../intel/playground-series-s4e10/bodies/543772_img/01.png)

**图 2**（topic 543772，8th）：5 条流水线下所有基模型的 fold/average AUC——CatBoost 系（cb-*）与 LGBM-GOSS 领先，RF/ET 垫底。

## 7. 出处

- 1st CatBoost All The Way Down（174 票 / 105 评论）：https://www.kaggle.com/competitions/playground-series-s4e10/discussion/543725
- 2nd（31 票 / 22 评论）：https://www.kaggle.com/competitions/playground-series-s4e10/discussion/543766
- 8th（21 票 / 7 评论）：https://www.kaggle.com/competitions/playground-series-s4e10/discussion/543772
- 10th no blind blend（19 票）：https://www.kaggle.com/competitions/playground-series-s4e10/discussion/543735
- LLM 方案落点（12 票）：https://www.kaggle.com/competitions/playground-series-s4e10/discussion/543734
- 新手提示（55 票 / 63 评论）：https://www.kaggle.com/competitions/playground-series-s4e10/discussion/539612
- XGBoost max_bin（34 票 / 28 评论）：https://www.kaggle.com/competitions/playground-series-s4e10/discussion/539963
- 数据有明显分组（34 票 / 31 评论）：https://www.kaggle.com/competitions/playground-series-s4e10/discussion/538099
- 线性 booster 当集成器（33 票 / 28 评论）：https://www.kaggle.com/competitions/playground-series-s4e10/discussion/540769
- 原数据提升 CV+LB（25 票 / 50 评论）：https://www.kaggle.com/competitions/playground-series-s4e10/discussion/537494
- Rank 4 方案（45 票 / 41 评论）：https://www.kaggle.com/competitions/playground-series-s4e10/discussion/543672
