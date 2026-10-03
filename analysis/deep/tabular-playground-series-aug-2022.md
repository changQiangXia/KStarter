# Tabular Playground Series Aug 2022（吸水海绵失效预测）轻量深读（Tier B）

> 赛事：Playground ｜ 主题 tabular（合成工业数据二分类，AUC）｜ 1888 队 ｜ 标准赛 ｜ 指标：ROC AUC
> 材料基础：`digests/tabular-playground-series-aug-2022.md`（6 篇正文：背景故事 341462 / 缺失值预测力 342319 / 14th 349810 / 17th 349541 / Less can be more 342126 / 9th 349297；80 条主题索引）+ 1 张归档图
> 轻读时间：2026-10（Tier B B17）

## 1. 一句话重述与数字账

预测"吸水海绵"产品原型在加载一定水量（loading）后是否失效（AUC）。本场的三条主线：①**缺失值本身有预测价值**（137 票的帖，社区统计显著性）；②**验证必须按 `product_code` 分组**——普通 GroupKFold 还不够，要用 AmbrosM 的"3 个产品码训练 / 2 个产品码验证"组合折，因为训练与测试的测量模态分布不同（top10 在私榜平均跳 331 位）；③**少即是多**——17th 只保留 `log(loading)`、WOE 编码的 `attribute_0`、m0/m1/m2/m17 加 4 个派生特征，用 LogisticRegression + XGBoost 线性提升就进前 20。

| 关键数字 | 值 | 来源 |
| --- | --- | --- |
| 缺失值与背景（342319、341462） | 137 票：缺失值有预测价值（缺失指示应与插补并列使用）；63 票的背景解读：product_code=设计编号、attribute=层材料/层数、measurements 多为成对测量、loading=浇水量、失效=饱和溢出 | 342319 / 341462 |
| 14th（349810） | 发现训练/测试测量**模态分布不同** → 验证必须包含测试模态；用 AmbrosM 的 **3-vs-2 产品码组合 CV**（10 折的 5 选 2 组合）防公榜过拟合；最佳单模 **TabNet 私 0.59098**；集成中发现 CatBoost 用 `predict()` 而非 `predict_proba()` 的 bug，修复后集成为 私 **0.59110**（如表所示，本可第 6，但未选中） | 349810 |
| 17th（349541） | 3-vs-2 折 + 预测平均；4 个新特征（m3 缺失指示、m5 缺失指示、`attribute2×attribute3` 面积、m3–m17 均值）；插补用 pourchot 方案（KNN 或按产品码中位数相当）；RobustScaler；**只保留 loading(取 log)、attribute_0(WOE)、m0/m1/m2/m17**；模型 = LogisticRegression + **XGBoost 线性提升（linear booster）**；最佳未提交方案是 XGBoost | 349541 |
| 社区方法论 | "Less can be more"（52 票：特征越少越好）；"GroupKFold isn't enough"（33 票）；"公开榜过拟合陷阱"（41 票 / 24 评论）；"Private vs Public Data"（42 票）；"top10 平均跳 331 位"（7 票）；"最好未选分数 0.59137"（9 票） | 索引 |

## 2. 逐方案对照矩阵

| 维度 | 14th | 17th | 社区共识 |
| --- | --- | --- | --- |
| CV | 3-vs-2 产品码组合（10 折） | 3-vs-2 折 | GroupKFold 不够 |
| 特征 | 测量模态对齐 | 极少列 + 4 派生 | Less is more |
| 模型 | TabNet 单模、多模型集成 | LR + XGB 线性提升 | 线性模型在场 |
| 结果 | 私 0.59090/0.59110（未选） | 前 20 | — |

## 3. 共识、分歧与裁决

### 共识一：缺失值有预测价值，缺失指示要与插补并列（342319、17th；置信度高）

137 票帖给出统计显著性；17th 的 m3/m5 缺失指示直接进特征。**裁决**：先检验缺失模式与目标的关系，保留缺失指示列。置信度：高。

### 共识二：验证必须按产品码分组，且要覆盖测试模态（341070、341896、14th、17th；置信度高）

3-vs-2 组合折成为前列标配；14th 明确因训练/测试模态差异而把测试模态纳入验证。**裁决**：合成产品数据先做"按产品/实体分组 + 模态对齐"的 CV 设计。置信度：高。

### 共识三：特征少而精（17th、342126；置信度中高）

17th 只留 8 个特征族（含派生）就进前 20；52 票帖主张"少即是多"。**裁决**：本场信号集中在 loading/log、attribute_0 WOE 与少数测量列。置信度：中高。

### 事件一：实现 bug 直接吞掉名次（14th；置信度中高）

CatBoost 的 `predict()` vs `predict_proba()` 让集成分数受损，修复后私榜 0.59110（可第 6）却未选中。**裁决**：集成前核对每个模型的输出语义（概率 vs 标签）。置信度：中高。

### 事件二：公榜噪声极大（348767、349307、349312；置信度中高）

top10 平均跳 331 位；"最好未选分数 0.59137"；公榜与私榜/CV 相关性差。**裁决**：以分组 CV 为唯一决策锚，提交保留多条线。置信度：中高。

## 4. 证据分级

| 断言 | 等级 | 说明 |
| --- | --- | --- |
| 缺失值预测力 | 高票帖（137 票）+ 统计 | 高 |
| 3-vs-2 产品码 CV | 多队采用 + 公开代码 | 高 |
| 14th 的 bug 与分数 | 自述 + 提交截图 | 中高 |
| 17th 的极简特征集 | 自述（含代码引用） | 中高 |
| 公榜/私榜大位移 | 多帖 | 中高 |

## 5. 悬案与缺口（登记）

- 1st–13th、15th/16th、18th+ 方案未收录；
- 测试模态差异的具体来源未定论；
- 9th 的方案只有索引（正文未细读）；
- **图证缺口**：无（1 张图，本深读内嵌 1 张）。

## 6. 图表证据

![修复后的集成提交](../../intel/tabular-playground-series-aug-2022/bodies/349810_img/01.PNG)

**图 1**（topic 349810，14th）：修复 CatBoost 输出 bug 后的 `ensemblingALL1.csv`——私榜 0.59110 / 公榜 0.58741，未被选中（本可第 6）。

## 7. 出处

- 缺失值有预测价值（137 票 / 66 评论）：https://www.kaggle.com/competitions/tabular-playground-series-aug-2022/discussion/342319
- 背景故事解读（63 票 / 11 评论）：https://www.kaggle.com/competitions/tabular-playground-series-aug-2022/discussion/341462
- Less can be more（52 票 / 22 评论）：https://www.kaggle.com/competitions/tabular-playground-series-aug-2022/discussion/342126
- 产品码分组 CV（50 票 / 9 评论）：https://www.kaggle.com/competitions/tabular-playground-series-aug-2022/discussion/341070
- GroupKFold 不够（33 票 / 10 评论）：https://www.kaggle.com/competitions/tabular-playground-series-aug-2022/discussion/341896
- 14th（5 票 / 3 评论）：https://www.kaggle.com/competitions/tabular-playground-series-aug-2022/discussion/349810
- 17th（6 票 / 6 评论）：https://www.kaggle.com/competitions/tabular-playground-series-aug-2022/discussion/349541
- 公开榜过拟合陷阱（41 票 / 24 评论）：https://www.kaggle.com/competitions/tabular-playground-series-aug-2022/discussion/348767
- Private vs Public Data（42 票 / 16 评论）：https://www.kaggle.com/competitions/tabular-playground-series-aug-2022/discussion/342403
