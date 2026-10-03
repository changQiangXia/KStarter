# CAFA 6 Protein Function Prediction 轻量深读（Tier B）

> 赛事：Research ｜ 主题 science（蛋白功能预测，极端多标签）｜ 2259 队 ｜ 标准赛 ｜ 指标：`cafa6_metric_final`（IA 加权）
> 材料基础：`digests/cafa-6-protein-function-prediction.md`（6 篇正文：1st 709383 / 2nd 711635 / 3rd 709281 / 加速实验 1283 行处 / 分类学 1337 行处 / 入门 1337 等；80 条主题索引）+ 19 张图
> 轻读时间：2026-10（Tier B B09）

## 1. 一句话重述与数字账

延续 CAFA5 的 GO 功能预测（极端多标签 + IA 加权）。本场的技术脉络高度"世袭"：1st 是 CAFA5 冠军团队的下一代系统 **GOAlpha**（仍是"多源组件 + Learning-to-Rank"），2nd 是 CAFA5 亚军的升级版（新增文献 TF-IDF），3rd 干脆是**复现 CAFA5 亚军开源代码**（并因此拿到第 3）。真正的考点变成**"如何把上一届的公开方案迭代出增量，以及如何处理公共榜/私榜的成分差异"**。

| 关键数字 | 值 | 来源 |
| --- | --- | --- |
| 1st（GOAlpha，709383，私榜 0.52430） | 七个组件：**BLAST-KNN、Net-KNN、FoldSeek-KNN、SVM-ESM2、LR-InterPro（118,677 维二值特征）、GOXML（文献极端多标签）、GORetriever（检索+重排）**，外加 **GO 词频 + 21 维物种编码** → **XGBoost 版 Learning-to-Rank** 融合；验证基准 = 按 CAFA6 测试集物种分布采样 1000 个有实验标注的蛋白（不参与训练）；关键发现：**序列类方法（BLAST-KNN、SVM-ESM2）单点最强**，结构类（FoldSeek）提供互补，**文献类方法在公榜强、私榜掉** → "公榜表现不能保证最终名次"，因此坚持多源融合而非选单点最强；并强调评估要限制"方法用到的证据必须早于测试蛋白的实验标注时间"（时间一致性问题） | 709383 |
| 2nd（711635） | 沿用自家 CAFA5 亚军方案；核心判断：**CAFA6 是 CAFA5 的"最新标注子集"** → 构造 "Old train"（CAFA5 中不在 CAFA6 train 的蛋白 + 从 UniProt 拉最新标注）与 "Train" 两种数据变体；嵌入用 T5、esm2-small（**发现微调无益**）；**本场最大新增量 = 文章 TF-IDF**：从 UniProt 的 `lit_pubmed_id` 取 PMID → 经 NCBI Entrez 批量下载标题/摘要 → 每蛋白 5000 维 TF-IDF 作为嵌入；基模型（py-boost/GCN）+ 更多种子的 stacker 提升稳健性 | 711635 |
| 3rd（709281，0.44640） | 坦白"基本是复现 U900 队 CAFA5-2nd 的开源代码 + 小改动"；用 **ESM2-t33-650M + ProtT5** 末层均值嵌入（ESM-IF 无效）；**把 CAFA5+CAFA6 训练集合并（145,382 蛋白）**；实现细节：`create_helpers.py` 里 **`propagate` 参数（是否沿 GO 层级传播标签）对分数影响巨大**；标签矩阵 = 1/0/**NaN**（词与其父词全 0 时记 NaN）；公开了编码数据集与合并代码 | 709281 |
| 社区侧 | "**从零到 ~0.269 LB：用 GOA UniProt GAF 的 NOT-free 标注**"（22 票 / 31 评论，公开基线）、"生物分类学"（28 票）、"ESM-3/Cambrian 嵌入"（23 票）、"官方 CAFA-evaluator 工具"（21 票）、"构造时间平移验证环境（用 CAFA5）"（16 票）、"T5 嵌入可直接从 UniProt 下载（HDF5）"（16 票） | 社区 |

## 2. 逐方案对照矩阵

| 维度 | 1st（GOAlpha） | 2nd | 3rd |
| --- | --- | --- | --- |
| 组件/特征 | 7 个组件（序列/网络/结构/域/文献）+ 词频 + 物种编码 | 嵌入 + **文章 TF-IDF** + py-boost/GCN | ESM2-t33 + ProtT5 嵌入（复现 CAFA5-2nd） |
| 融合 | **XGBoost Learning-to-Rank** | 堆叠（多数据变体 + 多种子） | 复现原方案 |
| 数据策略 | 证据源全量（含时间一致性约束） | **Train vs Train+Old train 对照** | CAFA5+CAFA6 合并 |
| 验证 | 按测试物种分布采样 1000 蛋白 | 多种子稳健性 | 本地 BP/MF/CC 分项 |
| 关键增量 | 结构/文献组件的互补性分析 | 文献 TF-IDF | propagate 参数与合并数据 |

## 3. 共识、分歧与裁决

### 共识一：多源组件 + 学习排序仍是骨架（1st/2nd/3rd）

与 CAFA5 相同：序列/结构/域/网络/文献各自成组件，再由 LTR/堆叠融合；1st 明确"没有任何单一信息源在所有蛋白上占优"。**裁决**：极端多标签的功能预测是"证据集成"问题；跨届复用组件库 + 融入当年新增数据源（本场=文献 TF-IDF）是最常见的增量路径。置信度：高。

### 共识二：公榜/私榜的"成分差异"会翻转组件排名（1st 的图 3）

1st 观察到序列/结构组件在私榜更高、文献组件在公榜更高；因此不选单点最优而坚持融合。**裁决**：评测集成分（物种/蛋白构成）会改变最优组件；必须建立"按测试分布采样"的验证基准。置信度：高。

### 共识三：上一届的公开代码/数据是本场的公共起点（3rd/2nd + 社区基线帖）

3rd 靠复现 CAFA5-亚军拿到第 3 并公开了编码数据集；社区"从零到 0.269"的 GAF 基线帖（31 评论）成为入门路径。**裁决**：系列赛（CAFA/RSNA 等）的"复用+小幅增量"是理性策略，但要明确标注复现来源与自身增量。置信度：高。

### 分歧一：数据扩充（Old train / 合并 CAFA5）

2nd 构造 "Train vs Train+Old train" 对照（承认"未必提升性能，但值得测试"）；3rd 直接合并 CAFA5+CAFA6（145,382 蛋白）。**裁决**：跨届数据合并要做"版本一致性"审计（标注时间、UniProt 更新），否则会引入时间泄漏或标签漂移。置信度：中高。

### 事件：标签传播与 NaN 掩码（3rd/CAFA5 传统）

3rd 实测 `propagate` 参数（沿 GO 层级传播标签）对分数影响巨大；标签矩阵用 1/0/NaN（父词全 0 时掩码）——这与 CAFA5 亚军首创的"条件概率重构"一脉相承。**裁决**：GO 层级处理（传播、掩码、条件概率）是这类比赛的"隐藏主变量"。置信度：高。

## 4. 证据分级

| 断言 | 等级 | 说明 |
| --- | --- | --- |
| 1st 的七组件 + LTR 与公/私榜组件对比 | 自述 + 三张图 + 团队 CAFA3/4/5 战绩 | 高 |
| 2nd 的文章 TF-IDF 与数据集变体 | 自述 + 管线图 + 开源代码 | 中高 |
| 3rd 的复现来源、propagate 发现与合并数据 | 自述 + 公开数据集/代码 | 中高 |
| 社区 GAF 基线（0.269） | 长讨论帖（31 评论） | 中 |
| 时间平移验证环境 | 讨论帖 | 中 |

## 5. 悬案与缺口（登记）

- 4th–10th 与 11th+ 的方案未细读；"加速实验"帖（1283 行处）与"分类学"（28 票）未细读；
- 1st 的 LTR 特征细节与组件权重未展开；
- 2nd 的 "Old train" 数据变体是否真正提升无明确结论；
- 归档 19 图：1st 的 GOAlpha 总览（图 1）与公/私榜对比（图 3）、2nd 的管线图为关键图证。

## 6. 图表证据

![GOAlpha 总览](../../intel/cafa-6-protein-function-prediction/bodies/709383_img/01.png)

**图 1**（topic 709383）：GOAlpha = 六边形所示的多源组件（Structure / Species / Network / Domain / Description-Literature / Sequence）→ **Learning-to-Rank 融合**；是本场"证据集成"范式的最清晰示意。

## 7. 出处

- 1st（20 票）：https://www.kaggle.com/competitions/cafa-6-protein-function-prediction/discussion/709383
- 2nd（17 票）：https://www.kaggle.com/competitions/cafa-6-protein-function-prediction/discussion/711635
- 3rd（15 票）：https://www.kaggle.com/competitions/cafa-6-protein-function-prediction/discussion/709281
- GAF 基线（22 票）：https://www.kaggle.com/competitions/cafa-6-protein-function-prediction/discussion/613138
- 时间平移验证（16 票）：https://www.kaggle.com/competitions/cafa-6-protein-function-prediction/discussion/614668
- CAFA-evaluator（21 票）：https://www.kaggle.com/competitions/cafa-6-protein-function-prediction/discussion/612097
