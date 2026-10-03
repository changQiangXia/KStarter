# Playground Series S3E26（肝硬化结局三分类）轻量深读（Tier B）

> 赛事：Playground ｜ 主题 tabular（肝硬化结局三分类，医学合成数据）｜ 1661 队 ｜ 标准赛 ｜ 指标：Multi-class Log Loss
> 材料基础：`digests/playground-series-s3e26.md`（6 篇正文：1st 464865 / 2nd 464887 / 4th 464863 / 7th 465167 / 医学风险因子 459392 / 资源合集 459389；80 条主题索引）+ 3 张归档图
> 轻读时间：2026-10（Tier B B14）

## 1. 一句话重述与数字账

预测肝硬化患者的三种结局（C/CL/D，Log Loss）。本场的经验是**"堆叠 + 医学先验 + 现代表格 NN"**：4th 用 XGB 元模型吃下多个公开 OOF（AutoGluon/LightAutoML/AutoXGB）拿第 4；2nd 用 **PLE（piecewise linear encoding）** 神经网络（单模私榜 ~0.401，进前 10%）并把 NN 堆叠器的权重改成"每个类别概率独立权重、且权重由全部输入预测共同决定"，比简单平均提升 0.004；1st 的帖子只有一句话——**把两年前的冠军方案改成伪标签版**就赢了。

| 关键数字 | 值 | 来源 |
| --- | --- | --- |
| 1st（464865） | "两年前冠军方案的修改版，唯一区别是**伪标签**"（帖极短，指向 2021 TPS 的冠军帖） | 464865 |
| 2nd（464887） | XGB/LGBM 各为 10 组 Optuna 超参的平均；初始 NN = 每个连续特征做 **PLE** + edema/stage 嵌入 + 其余二元特征原样（0/1）→ 单模私榜约 **0.401**（top 10%）；堆叠 NN：**每个类别概率各自有权重**且由全部输入预测共同计算 → 比简单平均 **+0.004**；NN 加进 GBDT 堆叠只 +0.001 | 464887 |
| 4th（464863） | XGB 元模型堆叠多来源 OOF + 原始特征；自造 Age 特征（`Age_Group` 分箱 9000–30000、`Log_Age`、MinMax `Scaled_Age`）；多框架产出 OOF：AutoGluon 1.0.1b（WeightedEnsemble_L2 最优）、LightAutoML（CatBoost 权重 0.279+0.485）、AutoXGB 5 折、公开 notebook（LGBM+XGB）；最终 **20 折 XGB 元模型**；建议"别把每个基模型调得太好，把预测当特征更稳" | 464863 |
| 7th（465167） | LightGBM + XGBoost 的 **VotingClassifier 软投票**；Optuna + 自定义负 logloss 目标；LabelEncoding + `date_of_diagnosis`/`diseases` 等特征 | 465167 |
| 医学先验（459392、459860、460069） | 化验指标临床阈值（胆红素/胆固醇/白蛋白/铜/碱性磷酸酶/SGOT 等）；新类别特征；Cox PH 生存分析视角 | 459392 等 |
| 社区 | "给 boosted trees 一个快速小提升"（33 票）；"7 条分类经验"（25 票）；排行榜洗牌可视化（27 票）；"不用原数据能否 <0.4"（2 票）等讨论 | 索引 |

## 2. 逐方案对照矩阵

| 维度 | 1st | 2nd | 4th | 7th |
| --- | --- | --- | --- | --- |
| 核心 | 2021 冠军方案 + 伪标签 | PLE 表格 NN + NN 堆叠器 | XGB 元模型堆叠多来源 OOF | LGBM+XGB 软投票 |
| 特征 | 沿用往届 | PLE + 嵌入 + 二元原样 | Age 分箱/对数/缩放 | LabelEncoding + 派生类别 |
| 元模型 | — | 自定义权重 NN | 20 折 XGB | 投票 |
| 结果 | 1st | 2nd（NN 单模 ~0.401） | 4th | 7th |

## 3. 共识、分歧与裁决

### 共识一：堆叠（XGB/NN 元模型）吃下多来源 OOF 是本场主线（2nd、4th；置信度高）

4th 的 20 折 XGB 元模型融合四个框架的 OOF；2nd 的自定义 NN 堆叠比简单平均 +0.004。**裁决**：多分类 log loss 下，元模型能同时做"加权 + 校准"，优于投票/平均。置信度：高。

### 共识二：表格 NN 的现代组件（PLE/嵌入）值得投入（2nd、459392 之外的社区讨论；置信度中高）

2nd 的 PLE 单模进前 10%；其"每类概率独立权重"的堆叠结构也被证明有效。**裁决**：表格 NN 的增益来自特征编码（PLE）与堆叠结构，而非更深的全连接。置信度：中高。

### 事件：跨届复用 + 伪标签足以夺冠（1st；置信度中）

1st 是两年前冠军方案的修改版，唯一区别是伪标签；社区还有"不用原数据能否 <0.4"等问题。**裁决**：Playground 系列的高度同质性让"旧冠军方案 + 一个现代技巧"成为可行打法；但需要留意规则与泄漏。置信度：中。

### 共识三：医学先验（阈值/风险因子）是可解释的增益来源（459392、459860、7th；置信度中）

社区整理了化验指标的正常/异常阈值；7th 派生了 diagnosis/diseases 特征。**裁决**：医学表格数据上，把连续指标按临床阈值离散化或做风险计数，往往比纯统计变换更有信号。置信度：中。

### 事件：榜单洗牌与 CV 可靠性（464869、社区；置信度中）

社区做了榜单洗牌可视化；多位选手强调"信 CV"。**裁决**：本场数据量小、类别不平衡，CV 仍是主决策信号；公榜只作 sanity check。置信度：中。

## 4. 证据分级

| 断言 | 等级 | 说明 |
| --- | --- | --- |
| 2nd 的 PLE NN 与堆叠结构（含 3 张图） | 自述 + 网络结构图 | 高 |
| 4th 的 XGB 元堆叠与框架权重 | 自述（含 AutoGluon/LightAutoML 输出） | 中高 |
| 1st 的"旧冠军 + 伪标签" | 自述（指向 2021 帖） | 中 |
| 7th 的软投票方案 | 自述 | 中 |
| 医学阈值/风险因子 | 高票帖 | 中高 |

## 5. 悬案与缺口（登记）

- 3rd、5th–6th、8th+ 方案未收录；
- 1st 的具体改动与伪标签细节未展开；
- "quick and dirty trick"（33 票）未细读；
- **图证缺口**：无（3 张网络结构图已内嵌 2 张）。

## 6. 图表证据

![2nd 的 level-0 PLE 网络](../../intel/playground-series-s3e26/bodies/464887_img/01.png)

**图 1**（topic 464887，2nd）：初始网络结构——各连续特征的 PLE 分支 + edema/stage 嵌入 → 拼接（1634 维）→ Dense → BN → Softmax(3)。

![2nd 的堆叠网络](../../intel/playground-series-s3e26/bodies/464887_img/03.png)

**图 2**（topic 464887，2nd）：堆叠网络——3 个预测输入各自 BN 后拼接（9 维）→ 三个 Dense(3) 分支 → BN/激活 → 与原始预测相乘（每类独立权重）→ Add。

## 7. 出处

- 1st 跨届复用 + 伪标签（19 票）：https://www.kaggle.com/competitions/playground-series-s3e26/discussion/464865
- 2nd PLE 神经网络（71 票 / 39 评论）：https://www.kaggle.com/competitions/playground-series-s3e26/discussion/464887
- 4th XGB 元模型堆叠（26 票 / 9 评论）：https://www.kaggle.com/competitions/playground-series-s3e26/discussion/464863
- 7th 软投票（6 票）：https://www.kaggle.com/competitions/playground-series-s3e26/discussion/465167
- 医学检验风险因子（44 票 / 13 评论）：https://www.kaggle.com/competitions/playground-series-s3e26/discussion/459392
- 资源合集（47 票）：https://www.kaggle.com/competitions/playground-series-s3e26/discussion/459389
- 快速小提升技巧（33 票）：https://www.kaggle.com/competitions/playground-series-s3e26/discussion/461307
- 7 条分类经验（25 票）：https://www.kaggle.com/competitions/playground-series-s3e26/discussion/461062
- 新类别特征（22 票）：https://www.kaggle.com/competitions/playground-series-s3e26/discussion/459860
- Cox PH 生存分析（21 票）：https://www.kaggle.com/competitions/playground-series-s3e26/discussion/460069
