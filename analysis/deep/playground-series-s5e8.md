# Playground Series S5E8 轻量深读（Tier B）

> 赛事：Playground ｜ 主题 tabular（葡萄牙银行营销二分类，合成数据）｜ 3365 队 ｜ 标准赛 ｜ 指标：ROC AUC
> 材料基础：`digests/playground-series-s5e8.md`（6 篇正文：1st 603210 / 2nd 603297 / 3rd 603198 / 15th 603179 / QuantileDMatrix 600048 / 反盲混帖 596696；80 条主题索引）+ 0 张归档图
> 轻读时间：2026-10（Tier B B05，收官）

## 1. 一句话重述与数字账

银行营销二分类，AUC。真正的考点是**"OOF 收藏馆 + 强集成器"的工程**：本场把"多模型堆叠"推到极限（100+ OOF），并且暴露出 **AutoGluon 不是不可战胜的**（1st 的赛后复盘）。

| 关键数字 | 值 | 来源 |
| --- | --- | --- |
| 1st（JAPE，603210） | 100→136 个 OOF 的大杂烩；**AutoGluon 当集成器**（每次跑满 ~12h）；XGB/LGBM 略优于 CatBoost；flip 技巧 +0.00001~0.00003；100/102 OOF 处遇墙（0.97839），50:50 混合+flip 得 0.97842；**最终 136 OOF 集成 0.97844 pub → 选其 flip 版，私榜 0.97801（第 1）**；赛后复盘：**NN 集成器（5 折）在 143 OOF 上 1.5 小时（GPU）拿到与 AG 相当的成绩，与 LGBM+LR 做爬山后 0.97841/0.97805，优于所有 AG 结果且省 8 倍时间**；CatBoost/LGBM/XGB 支持"以别的模型预测为 baseline"的接力技巧（最后一夜才试）；自评若早上 Optuna+伪标签可达 0.9785+/0.9781+ | 603210 |
| 2nd（603297） | 59 模型集成（用 CatBoost 当集成器）；各家族最好单模：**TabM 0.97765/0.97750（pub/priv）**、XGB 0.97741/0.97707、LGBM 0.97693/0.97660、RealMLP CV 0.97598、CatBoost 0.97590/0.97571、DeepTables/TabR/Gandalf/RF/GRN/FT-Transformer/CNN 依次下降；方法论同 S5E6："先造多样 OOF，再慢慢加" | 603297 |
| 3rd（603198） | **迭代式 OOF 堆叠**：收集公开/自产 OOF 与提交文件（**滤掉泄漏与虚高 CV**）→ 用它们当特征训 AutoGluon → 按特征重要性筛 → 循环；版本表从 AG baseline 私榜 0.96677 提升到 0.97x 档 | 603198 |
| 15th（603179） | 单模最佳：CatBoost Optuna 0.97732 priv、**xLearn FFM 0.97708**、XGB Optuna 0.97701、Keras FM 0.97701、LAMA DenseLight 0.97589；集成器以 **LAMA DenseLight 最好**；**遗传编程特征**：加入原始数据可 +0.0025~0.003，但在已有统计/TE 特征后仅 +0.0001 | 603179 |
| 工程技巧（69 票） | **`xgb.QuantileDMatrix` 代替 `DMatrix`**：分批构建直方图（默认 max_bin=256，32bit→1byte，4×压缩）+ 降 dtype（int64/float64→int32/float32，2×）= 最多可训 8× 数据；进阶用"Notebook A 落盘 → Notebook B 分块读盘"，避免 cuDF 数据框占满显存 | 600048 |
| 事件 | "Say no to blind blending"（34 票）与"Are We Here to Learn or Just to Ensemble Submissions?"（1008 行处）反映本场公开提交互混的生态争议；"Rank-3 Public → Rank-5 Private"（36 票） | 社区 |

## 2. 逐方案对照矩阵

| 维度 | 1st | 2nd | 3rd | 15th |
| --- | --- | --- | --- | --- |
| 形态 | 136 OOF + AG | 59 模型 + CatBoost 集成器 | 迭代 OOF 堆叠 + AG | 多模型 + DenseLight 集成器 |
| 成员 | GBDT/NN/弱模型（RF/KNN）混合 | TabM/XGB/LGBM/RealMLP/CatBoost… | 公开+自产 OOF | CatBoost/xLearn/XGB/Keras FM |
| 特色 | flip、baseline 接力、NN 集成器复盘 | 家族分数表 | 重要性筛选迭代 | 遗传编程特征 |
| 私榜 | 0.97801（#1） | — | — | 0.97732（单模最高） |

## 3. 共识、分歧与裁决

### 共识一：本场是"OOF 收藏 + 集成器"的比赛（全员）

1st 收集 136 个 OOF；2nd 59 模型；3rd 直接拿 OOF 当特征再训 AG；15th 也做多模型集成。**裁决**：在 CV-LB 一致的 tabular 赛里，**成员的多样性（跨模型族/是否含原数据/不同折）比单个模型强度更重要**；弱模型（RF/KNN）也贡献多样性。置信度：高。

### 共识二：集成器选择是独立杠杆（1st/2nd/3rd/15th 各不相同）

1st 用 AG（并证明 NN 集成器更划算）；2nd/3rd 用 CatBoost/AG；15th 用 LAMA DenseLight。**裁决**：集成器本身值得当作"一个模型"来调；不同集成器对成员池的利用方式不同，赛后固定跑一遍多集成器对照是低成本高收益动作。置信度：高。

### 共识三：flip 是 playground 二分类的惯例小增益（1st）

1st 明确"flip 技巧照例有效，约 +0.00001（私榜 ~+0.00003）"，并最终把 flip 版作为两个提交之一。**裁决**：二分类 playground 的"反标签翻转"属低成本惯性动作；但收益极小，不能替代集成器/成员质量。置信度：中高。

### 分歧一：AutoGluon 是否最优集成器

1st 前半程依赖 AG（"比 Ridge/爬山/LGBM 都好"），赛后却发现 **NN 集成器 + 爬山把成绩推到 0.97805 私榜、耗时仅为 AG 的 1/8**。**裁决**：AG 的强可能来自"跑得久"（12h 预算）；用同等预算对比轻量 NN 集成器是必要的对照实验。置信度：中高（单队赛后实验）。

### 分歧二：公开 OOF/提交互混的边界

3rd 的做法是"收集公开 OOF/提交，但**先过滤泄漏与虚高 CV**"；社区另有"Say no to blind blending"与"我们在学习还是在混提交"的争论。**裁决**：公开 artifact 可用，但必须过"OOF 可信度"检验（CV 分布、泄漏检查）；盲混是噪声放大器。置信度：中高。

### 事件：弱模型与大池子的关系

1st 自述"墙"出现在 70+ OOF，远超他人报告的阈值——因为他在建"更大但更弱的集合"；2nd 强调"不同模型 > 同模型调参/FE 变体"。**裁决**：扩池时应优先加"机制不同"的模型，而不是同族变体；池子大小的甜点区与成员平均质量有关。置信度：中高。

## 4. 证据分级

| 断言 | 等级 | 说明 |
| --- | --- | --- |
| 1st 的全过程分数链与赛后 NN 集成器对照 | 自述 + 完整数字 | 高 |
| 2nd 的家族分数表（TabM 最佳） | 自述 + 表 | 中高 |
| 3rd 的迭代 OOF 堆叠流程 | 自述 + 版本表 | 中高 |
| 15th 的遗传编程特征增益（0.003→0.0001） | 自述 + 公式 + notebook | 中 |
| QuantileDMatrix 8× 内存优势 | 官方 API 机制 + 示例 + notebook | 高（机制层面） |
| flip 增益 ~0.00001 | 单队惯例自述 | 中 |

## 5. 悬案与缺口（登记）

- "Two Pro Tips - Final Week"（63 票）、"Rank-3 Public Rank-5 Private"（36 票）、"Somebody asked why blending works"（22 票）、"Designing NN-Friendly Features"（20 票）未细读；
- 1st 提到的 "baseline 接力"（CatBoost/LGBM/XGB 以他模型预测为基线）细节与失败原因未量化；
- 反盲混争议帖（596696）与"学习 vs 混提交"帖的结论未细读；
- **图证缺口**：本场 0 张归档图。

## 6. 图表证据

无可用图证（本场归档 0 图）。核心证据为分数链与版本表，已在正文引用。

## 7. 出处

- 1st JAPE（26 票）：https://www.kaggle.com/competitions/playground-series-s5e8/discussion/603210
- 2nd（47 票）：https://www.kaggle.com/competitions/playground-series-s5e8/discussion/603297
- 3rd（24 票）：https://www.kaggle.com/competitions/playground-series-s5e8/discussion/603198
- 15th（21 票）：https://www.kaggle.com/competitions/playground-series-s5e8/discussion/603179
- QuantileDMatrix（69 票）：https://www.kaggle.com/competitions/playground-series-s5e8/discussion/600048
- 反盲混（34 票）：https://www.kaggle.com/competitions/playground-series-s5e8/discussion/596696
