# Feedback Prize - Evaluating Student Writing

> `feedback-prize-2021` ｜ Featured ｜ 指标 TextOverlapFBeta ｜ 2058 队 ｜ 截止 2022-03-15

本页汇总该场 **3 条 ≥50 票 GM 主题帖**、**12 条断言**、**1 条高票评论**。

## GM 主题帖

| 票 | 选手 | 日期 | 主题 |
| --- | --- | --- | --- |
| 296 | [@cdeotte](https://www.kaggle.com/cdeotte) | 2021-12-17 | [TensorFlow/PyTorch NER Starter - What is NER? -  LB 0.630](https://www.kaggle.com/competitions/feedback-prize-2021/discussion/295794) |
| 203 | [@cdeotte](https://www.kaggle.com/cdeotte) | 2022-03-16 | [2nd Place - Weighted Box Fusion and Post Process](https://www.kaggle.com/competitions/feedback-prize-2021/discussion/313389) |
| 165 | [@tascj0](https://www.kaggle.com/tascj0) | 2022-03-17 | [6th place solution. A YOLO-like text span detector.](https://www.kaggle.com/competitions/feedback-prize-2021/discussion/313424) |

## 断言（条件→动作→机制→结果）

| 选手 | 等级 | 阶段 | 动作（节选） | 出处 |
| --- | --- | --- | --- | --- |
| @cdeotte | A | 集成与融合 | 用 WBF 对 span 起点与终点分别平均：8-11 与 10-13 合成 9-12；token 概率平均会取并集或交集，BIO 平均会产生两个 B | [feedback-prize-2021#313389-01](https://www.kaggle.com/competitions/feedback-prize-2021/discussion/313389) |
| @cdeotte | A | 集成与融合 | 去掉 3 个 fold 后共推理 27 个模型；同模型 folds 先平均再进 WBF | [feedback-prize-2021#313389-02](https://www.kaggle.com/competitions/feedback-prize-2021/discussion/313389) |
| @cdeotte | A | 后处理 | 规则后处理：修复断裂 span、discourse 上限（Lead/Position/Concluding 各最多一个）、按预测长度调整边界（小于 45 词的 Evidence 起 | [feedback-prize-2021#313389-03](https://www.kaggle.com/competitions/feedback-prize-2021/discussion/313389) |
| @cdeotte | A | 建模与训练 | 多 backbone 支持长序列：DeBERTa 任意长度、Funnel 改 config 到 1536、BigBird 用 original_full、YOSO 关 lsh_ba | [feedback-prize-2021#313389-04](https://www.kaggle.com/competitions/feedback-prize-2021/discussion/313389) |
| @tascj0 | A | 建模与训练 | TokenClassification 头输出 1 个 objectness 加 2 个回归（到 span 首尾距离）加 num_classes 分类；用 RoIAlign 把 t | [feedback-prize-2021#313424-01](https://www.kaggle.com/competitions/feedback-prize-2021/discussion/313424) |
| @tascj0 | A | 集成与融合 | 只集成 deberta-large 加 deberta-xlarge（各 2/5 folds）；后处理只用 NMS；尝试 WBF 但本地验证不 work | [feedback-prize-2021#313424-03](https://www.kaggle.com/competitions/feedback-prize-2021/discussion/313424) |
| @cdeotte | B | 建模与训练 | LongFormer-base（支持 4096 tokens）实际输入 1024；单折 5 epochs；使用官方 metric 实现 | [feedback-prize-2021#295794-02](https://www.kaggle.com/competitions/feedback-prize-2021/discussion/295794) |
| @cdeotte | B | 建模与训练 | BigBird backbone 单折训练；演示 predictionstring→标签转换与 dataloader | [feedback-prize-2021#295794-03](https://www.kaggle.com/competitions/feedback-prize-2021/discussion/295794) |
| @cdeotte | B | 工程/流程 | FP16 + gradient_accumulation + gradient_checkpointing，配合每 500 步按 Kaggle metric 评估并存最优权重 | [feedback-prize-2021#313389-05](https://www.kaggle.com/competitions/feedback-prize-2021/discussion/313389) |
| @cdeotte | C | 数据理解 | 把 NER 视为 token 级分割；把 Question Answering 视为检测（框住 span，可保留中间空洞） | [feedback-prize-2021#295794-01](https://www.kaggle.com/competitions/feedback-prize-2021/discussion/295794) |
| @cdeotte | C | 工程/提交 | 提前把 HuggingFace backbone 下载成 Kaggle dataset 并挂载 | [feedback-prize-2021#295794-04](https://www.kaggle.com/competitions/feedback-prize-2021/discussion/295794) |
| @tascj0 | C | 建模与训练 | objectness 正样本取 span 第一个词；另把每个 span 内最低 cost 词也设为阳性（YOLOX 启发） | [feedback-prize-2021#313424-02](https://www.kaggle.com/competitions/feedback-prize-2021/discussion/313424) |

## 高票评论

| 票 | 选手 | 日期 | 摘录 | 出处 |
| --- | --- | --- | --- | --- |
| 13 | @cdeotte | 2021-12-18 | I trained this model offline using the exact code posted in starter notebook. The code uses batch_size = 32, m | [295794](https://www.kaggle.com/competitions/feedback-prize-2021/discussion/295794) |

## 关联资产

- 深读：`analysis/deep/feedback-prize-2021.md`
- 结构化摘要：`notes/nlp/feedback-prize-2021.md`
- 归档讨论区：`intel/feedback-prize-2021/`（主题 3 条有 ≥50 票帖，图证 1 个）
