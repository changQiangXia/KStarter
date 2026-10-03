# NBME - Score Clinical Patient Notes 轻量深读（Tier B）

> 赛事：Featured ｜ 主题 nlp（医疗文本 span 抽取）｜ 1471 队 ｜ 代码赛 ｜ 指标：Medical Board F-Beta
> 材料基础：`digests/nbme-score-clinical-patient-notes.md`（6 篇正文：2nd 323085 / 4th 322799 / 3rd 322832 / 1st 323095 / 20th 323094 / 实验帖 315707；80 条主题索引）+ 3 张图
> 轻读时间：2026-10（Tier B B03）

## 1. 一句话重述与数字账

从病历文本里抽取"病例特征"对应的 span（F-beta）。真正的考点是**token 分类 + 标注噪声处理 + 迭代伪标 + 逐 case 阈值/后处理**；1 万倍无标注数据让半监督成为主战场。

| 关键数字 | 值 | 来源 |
| --- | --- | --- |
| 1st（128 票） | 6 个 DeBERTa 模型（v3-large/deberta-large/v2-xlarge/v2-large）集成；每个都做 MLM + 伪标（**90% 伪标+10% 真标**、**软标签**）+ AWP（adv_lr 1.0/eps 0.01，+0.002）+ 去句增广（p=0.2）+ 辅助 start/end 通道；10 折 **GroupStratifiedKFold**（对比 5 折 GroupKFold 是巨大改进）；最终集成权重 0.206/0.172/0.143/0.164/0.167/0.147 → CV 0.8953/公 0.8946/私 0.8946（图 1） | 1st |
| 4th（126 票） | 4 个 token 分类 DeBERTa（v3-large 4/5 折、v2-xlarge、v2-xxlarge）；MLM 0.10–0.15；SmoothFocalLoss；2–4 轮伪标；**逐 case_num 阈值** + 后处理；公/私 ~0.891/0.892；最好私有提交其实是"3 token + 1 char 分类"集成但未能选择 | 4th |
| 2nd（174 票） | 标注不一致的洞察：标注者会漏标重复出现（序列依赖→RNN 有道理）；全部小写（uncased）；缩写归一；**tokenizer 边界分析 + 空格后处理**（扩展 TheoViel 版） | 2nd |
| 3rd（322832） | 任务 MLM 适应；**多标签 token 分类（I/B/E）**；Meta Pseudo Labels + 集成 KD；标记 token "QA CASE=0"；SWA；**字符级预测混合**；按特征的后处理（如 feature 309 的时长过滤） | 3rd |

## 2. 逐方案对照矩阵

| 维度 | 1st | 4th | 3rd |
| --- | --- | --- | --- |
| 骨干 | deberta-large/v2-xlarge/v3-large/v2-large | deberta-v3-large/v2-xlarge/v2-xxlarge | DeBERTa Large/XLarge/V2-XLarge/V3-Large |
| 任务 MLM | 是 | 是（0.10–0.15） | 是（0.2） |
| 伪标 | 1 轮大比例（90/10）、软标签 | 2–4 轮 | Meta Pseudo Labels + KD |
| 正则/增广 | AWP、去句 p=0.2 | SmoothFocalLoss、mask | SWA、标记 token |
| 输出 | token + start/end 辅助通道 | token | I/B/E 多标签 + 字符级混合 |
| 后处理 | 去首尾空格 | 逐 case 阈值 + PP | 特征专属（时长过滤） |
| CV 设计 | 10 折 GroupStratifiedKFold | 4/5 折 | — |
| 私榜 | 0.8946 | 0.892 | 3rd |

## 3. 共识、分歧与裁决

### 共识一：DeBERTa 系 + 任务 MLM + 伪标 + AWP 是标准配方（4/4）

所有前排都是 DeBERTa 家族 + MLM 域适应 + 伪标 + 对抗训练（AWP/FGM）。**裁决**：小标注数据 + 大无标注池的 NLP 赛，半监督管线是入场券；模型差异主要靠骨干/轮数/标签形式制造。置信度：高。

### 共识二：标注噪声不可"修"，要顺着它建模（2nd 最深刻）

2nd：标注者漏标重复出现 → 标注有序列依赖；不应修正训练标注（测试同样不一致），可在模型里用序列结构利用它。4th/3rd 也都做逐 case 阈值与特征专属后处理。**裁决**：噪声标注赛里，"模仿标注者行为"比"追求真值"更接近评测分布。置信度：高。

### 共识三：后处理/阈值是独立增益（4th/3rd/2nd）

4th 逐 case_num 阈值；2nd 的空格边界后处理（tokenizer 无法表达边界时规则补齐）；3rd 的特征时长过滤。**裁决**：token 化边界 + 标注习惯造成的系统性误差，必须用规则 PP 修正。置信度：高。

### 共识四：CV 要按患者/病例分组（1st 明证）

1st 从 5 折 GroupKFold → 10 折 **GroupStratifiedKFold** 是"巨大改进"；2nd 的分析也基于分组一致性。**裁决**：同患者的笔记/特征跨折会泄漏；分组+分层是必须。置信度：高。

### 分歧一：伪标策略（1 轮大比例 vs 多轮）

1st：1 轮、90% 伪标 + 10% 真标、软标签；4th：2–4 轮且"更多轮私榜更好"；3rd：Meta Pseudo Labels。**裁决**：轮数与比例是超参，关键是软标签与验证；1st 的单轮大比例在分组 CV 下获胜。置信度：中。

### 分歧二：token 级 vs 字符级

1st/4th 以 token 分类为主（4th 的最佳私榜含 char 模型）；3rd 混合字符级预测。**裁决**：字符级可绕过 tokenization 边界误差，作为集成成员有价值。置信度：中。

### 失败学

1st：句子 shuffle 增广、label smoothing loss、clip_grad_norm（调得不好）均变差；除空格外的 PP 无效。**裁决**：增广/正则要按任务语义筛选。置信度：中。

## 4. 证据分级

| 断言 | 等级 | 说明 |
| --- | --- | --- |
| 1st 的管线/权重/分数 | 自述 + 图 + 公开代码 | 高（图内权重与分数） |
| 4th 的阈值/PP 与分数 | 自述 | 中高 |
| 2nd 的标注不一致/边界分析 | 自述（可复现分析逻辑） | 中高 |
| 3rd 的 MPL/KD/SWA | 自述 + 代码 | 中 |
| 各增益（AWP/MLM +0.002） | 自述 | 中 |

## 5. 悬案与缺口（登记）

- 5th–19th 方案未收录；"Tokenization Analysis"（127 票）与 Deberta-base 基线（106 票）未入库。
- 4th 的"最好私榜集成未选中"的决策复盘缺失；20th 未细读。
- 标注一致性的官方说明缺失（2nd 的假设无官方确认）。

## 6. 图表证据

![1st 的模型管线](../../intel/nbme-score-clinical-patient-notes/bodies/323095_img/01.jpeg)

**图 1**（topic 323095）：3 骨干 × 4 阶段（normal → pseudo → auxiliary target → auxiliary+pseudo）→ pseudo label blend；集成权重 0.206/0.172/0.143/0.164/0.167/0.147；最终 CV 0.8953/公 0.8946/私 0.8946。**半监督 span 抽取的完整流水线**。

## 7. 出处

- 2nd（174 票）：https://www.kaggle.com/competitions/nbme-score-clinical-patient-notes/discussion/323085
- 4th（126 票）：https://www.kaggle.com/competitions/nbme-score-clinical-patient-notes/discussion/322799
- 3rd（322832）：https://www.kaggle.com/competitions/nbme-score-clinical-patient-notes/discussion/322832
- 1st（128 票）：https://www.kaggle.com/competitions/nbme-score-clinical-patient-notes/discussion/323095
- 20th（323094）：https://www.kaggle.com/competitions/nbme-score-clinical-patient-notes/discussion/323094
- 实验帖（315707）：https://www.kaggle.com/competitions/nbme-score-clinical-patient-notes/discussion/315707
