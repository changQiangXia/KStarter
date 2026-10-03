# HMS - Harmful Brain Activity Classification 

> `hms-harmful-brain-activity-classification` ｜ Research ｜ 指标 Kullback Leibler Divergence ｜ 2767 队 ｜ 截止 2024-04-08

本页汇总该场 **4 条 ≥50 票 GM 主题帖**、**13 条断言**、**7 条高票评论**。

## GM 主题帖

| 票 | 选手 | 日期 | 主题 |
| --- | --- | --- | --- |
| 603 | [@cdeotte](https://www.kaggle.com/cdeotte) | 2024-01-15 | [Understanding Competition Data and EfficientNetB2 Starter - LB 0.43 🎉](https://www.kaggle.com/competitions/hms-harmful-brain-activity-classification/discussion/468010) |
| 233 | [@cdeotte](https://www.kaggle.com/cdeotte) | 2024-01-21 | [Magic Formula to Convert EEG to Spectrograms!](https://www.kaggle.com/competitions/hms-harmful-brain-activity-classification/discussion/469760) |
| 159 | [@cdeotte](https://www.kaggle.com/cdeotte) | 2024-04-09 | [8th Place Gold - One Mega Model](https://www.kaggle.com/competitions/hms-harmful-brain-activity-classification/discussion/492482) |
| 133 | [@christofhenkel](https://www.kaggle.com/christofhenkel) | 2024-04-09 | [3rd place solution](https://www.kaggle.com/competitions/hms-harmful-brain-activity-classification/discussion/492471) |

## 断言（条件→动作→机制→结果）

| 选手 | 等级 | 阶段 | 动作（节选） | 出处 |
| --- | --- | --- | --- | --- |
| @cdeotte | A | 数据理解 | 读 host 论文发现差异后，用 vote_count>=10 过滤出专家标注训练；模型预测的是专家观点 | [hms-harmful-brain-activity-classification#492482-01](https://www.kaggle.com/competitions/hms-harmful-brain-activity-classification/discussion/492482) |
| @cdeotte | A | 建模与训练 | 三个单模（spectrogram tiny_vit_512、wave-plot tiny_vit_224、EegNet-1D）先各训 6 类；再用 new_label = 0.1  | [hms-harmful-brain-activity-classification#492482-03](https://www.kaggle.com/competitions/hms-harmful-brain-activity-classification/discussion/492482) |
| @cdeotte | A | 报告结果 | 公开单模推理 notebook：CV 0.246 / public 0.243 / private 0.290 | [hms-harmful-brain-activity-classification#492482-04](https://www.kaggle.com/competitions/hms-harmful-brain-activity-classification/discussion/492482) |
| @christofhenkel | A | 数据工程 | 追溯原始数据点，过滤到 6350 行，既用于 4 折验证也用于主要训练，丢弃其余约 10 万行；验证只保留超过 9 票的行 | [hms-harmful-brain-activity-classification#492471-01](https://www.kaggle.com/competitions/hms-harmful-brain-activity-classification/discussion/492471) |
| @christofhenkel | A | 特征与数据工程 | 通用：16 个 mel 节点随机清零 1 到 8 个（50%）、随机换更窄 butter 带（20%）、50s 窗口随机平移（50%）；1D 加时间翻转与换脑侧；2D 加中心 10 | [hms-harmful-brain-activity-classification#492471-04](https://www.kaggle.com/competitions/hms-harmful-brain-activity-classification/discussion/492471) |
| @christofhenkel | A | 集成与融合 | 18 个 2D Mixnet 加 5 个 1D CNN（每折 23 模型）；用简单 NN 学融合权重，再加每类 bias 到 logits；public 从第 9 升到第 4 | [hms-harmful-brain-activity-classification#492471-05](https://www.kaggle.com/competitions/hms-harmful-brain-activity-classification/discussion/492471) |
| @cdeotte | B | 数据理解 | 用公榜探针比较 4 种样本加权口径，最终选按 eeg_id 加权 | [hms-harmful-brain-activity-classification#468010-01](https://www.kaggle.com/competitions/hms-harmful-brain-activity-classification/discussion/468010) |
| @cdeotte | B | 特征与数据工程 | 对每条链先对相邻电极差分做 spectrogram、再对 4 个 spectrogram 求平均（LL/LP/RL/RP），而不是先合并波形再算 spectrogram | [hms-harmful-brain-activity-classification#469760-01](https://www.kaggle.com/competitions/hms-harmful-brain-activity-classification/discussion/469760) |
| @cdeotte | B | 工程/流程 | 把 17089 个 EEG spectrogram 打成 7.5GB 的 .npy 字典、11138 个 Kaggle spectrogram 打成 2.5GB 字典并发布为 Ka | [hms-harmful-brain-activity-classification#469760-02](https://www.kaggle.com/competitions/hms-harmful-brain-activity-classification/discussion/469760) |
| @christofhenkel | B | 建模与训练 | 低票集单独损失并随时间衰减：3 到 8 票权重 0.8 衰减到 0.2；1 到 2 票权重 0.5 衰减到 0 | [hms-harmful-brain-activity-classification#492471-02](https://www.kaggle.com/competitions/hms-harmful-brain-activity-classification/discussion/492471) |
| @christofhenkel | B | 特征与数据工程 | torchaudio GPU 在线 Mel；double banana 16 导联左右成对排序；butter order 2（低通 0 到 1.5Hz、高通 20 到 30Hz）不 | [hms-harmful-brain-activity-classification#492471-03](https://www.kaggle.com/competitions/hms-harmful-brain-activity-classification/discussion/492471) |
| @cdeotte | C | 建模与训练 | 单模型同时输入两套 spectrogram | [hms-harmful-brain-activity-classification#469760-03](https://www.kaggle.com/competitions/hms-harmful-brain-activity-classification/discussion/469760) |
| @cdeotte | C | 特征与数据工程 | 把 2D spectrogram 与 matplotlib 画的 2D 波形图都作为模型输入（1D 原始波形也有帮助） | [hms-harmful-brain-activity-classification#492482-02](https://www.kaggle.com/competitions/hms-harmful-brain-activity-classification/discussion/492482) |

## 高票评论

| 票 | 选手 | 日期 | 摘录 | 出处 |
| --- | --- | --- | --- | --- |
| 17 | @cdeotte | 2024-01-22 | Neural networks like input data to have a Gaussian distribution (i.e. normal bell shaped histogram with mean=0 | [469760](https://www.kaggle.com/competitions/hms-harmful-brain-activity-classification/discussion/469760) |
| 14 | @cdeotte | 2024-01-15 | The larger window provides context. Imagine if i asked you to predict what i will eat for lunch today. I can g | [468010](https://www.kaggle.com/competitions/hms-harmful-brain-activity-classification/discussion/468010) |
| 13 | @cdeotte | 2024-01-22 | Another trick is using Gauss Rank Transform (shown here). Or using a Quantile Transform here. Both can transfo | [469760](https://www.kaggle.com/competitions/hms-harmful-brain-activity-classification/discussion/469760) |
| 12 | @cdeotte | 2024-01-15 | Hi. The variable eeg_label_offset_seconds is the beginning, not the middle. (We are not given the middle). The | [468010](https://www.kaggle.com/competitions/hms-harmful-brain-activity-classification/discussion/468010) |
| 11 | @cdeotte | 2024-01-24 | When doctors evaluate patients, they use the spectrograms to see the "big picture" of how the patient were fee | [468010](https://www.kaggle.com/competitions/hms-harmful-brain-activity-classification/discussion/468010) |
| 11 | @cdeotte | 2024-01-17 | Yes, I do 2 and Tawara does 3. My 256 is because I take the middle 512 seconds (instead of full 600 seconds).  | [468010](https://www.kaggle.com/competitions/hms-harmful-brain-activity-classification/discussion/468010) |
| 11 | @cpmpml | 2024-04-09 | Using plots is an intriguing idea. I never saw it before. Glad you ended in top 10 despite sharing so much. Co | [492482](https://www.kaggle.com/competitions/hms-harmful-brain-activity-classification/discussion/492482) |

## 关联资产

- 深读：`analysis/deep/hms-harmful-brain-activity-classification.md`
- 结构化摘要：`notes/tabular/hms-harmful-brain-activity-classification.md`
- 归档讨论区：`intel/hms-harmful-brain-activity-classification/`（主题 4 条有 ≥50 票帖，图证 11 个）
