# Child Mind Institute - Detect Sleep States

> `child-mind-institute-detect-sleep-states` ｜ Featured ｜ 指标 Event Detection AP ｜ 1877 队 ｜ 截止 2023-12-05

本页汇总该场 **2 条 ≥50 票 GM 主题帖**、**9 条断言**、**0 条高票评论**。

## GM 主题帖

| 票 | 选手 | 日期 | 主题 |
| --- | --- | --- | --- |
| 186 | [@cdeotte](https://www.kaggle.com/cdeotte) | 2023-12-06 | [11th Place - GRU, CNN, Transformer - GPU Deep Learning!](https://www.kaggle.com/competitions/child-mind-institute-detect-sleep-states/discussion/459596) |
| 70 | [@aerdem4](https://www.kaggle.com/aerdem4) | 2023-12-06 | [7th Place Solution - Wavenet and Some Tricks](https://www.kaggle.com/competitions/child-mind-institute-detect-sleep-states/discussion/459598) |

## 断言（条件→动作→机制→结果）

| 选手 | 等级 | 阶段 | 动作（节选） | 出处 |
| --- | --- | --- | --- | --- |
| @cdeotte | A | 后处理 | 每晚对每个目标取前 30 个猜测，第 k 名分数除以 2 的 k-1 次方 | [child-mind-institute-detect-sleep-states#459596-03](https://www.kaggle.com/competitions/child-mind-institute-detect-sleep-states/discussion/459596) |
| @cdeotte | A | 后处理 | 用 CatBoost 手工卷积特征、1D/2D Unet、Mel Spectrograms、ResNet34、EfficientNetB5、Audio WaveNet 重新打分，再 | [child-mind-institute-detect-sleep-states#459596-04](https://www.kaggle.com/competitions/child-mind-institute-detect-sleep-states/discussion/459596) |
| @cdeotte | A | 集成与融合 | 先各自 NMS（5 分钟内保留最大概率），再用 WBF 集成（同层 5 分钟内取平均位置） | [child-mind-institute-detect-sleep-states#459596-05](https://www.kaggle.com/competitions/child-mind-institute-detect-sleep-states/discussion/459596) |
| @aerdem4 | A | 特征与数据工程 | WaveNet 变体处理 3 天逐分钟聚合序列；特征：target、idx、anglez 均值/方差、enmo 均值/方差、同日同分钟 anglez 差分、volatility（3 | [child-mind-institute-detect-sleep-states#459598-01](https://www.kaggle.com/competitions/child-mind-institute-detect-sleep-states/discussion/459598) |
| @aerdem4 | A | 建模与训练 | 目标相邻分钟也设 1；目标前后第 2、3 分钟设为 -1 忽略近邻误差；双头（分钟级 CE 加 15 分钟窗 BCE）；OHEM 50%；6 epochs 递减 LR；每 epoc | [child-mind-institute-detect-sleep-states#459598-02](https://www.kaggle.com/competitions/child-mind-institute-detect-sleep-states/discussion/459598) |
| @aerdem4 | A | 后处理 | 从最大预测开始加入位置；分数取概率与 ±4 分钟内次高概率，随后把这些窗口清零；±20 分钟窗口乘 0.5；再对高分预测在 ±18 步范围采样低概率预测 | [child-mind-institute-detect-sleep-states#459598-03](https://www.kaggle.com/competitions/child-mind-institute-detect-sleep-states/discussion/459598) |
| @aerdem4 | A | 集成与融合 | LightGBM 用大量 anglez 中位绝对差特征，加 NN 概率与到 onset/wakeup 的时间特征：AUC 显著提升但指标仅加 0.001；另一个 LSTM+Tran | [child-mind-institute-detect-sleep-states#459598-04](https://www.kaggle.com/competitions/child-mind-institute-detect-sleep-states/discussion/459598) |
| @cdeotte | B | 建模与训练 | 改用 NLP QA 头（BertForQuestionAnswering，类比检测）：dataloader 保证每序列含 1 onset 加 1 wakeup，用 1440 类 s | [child-mind-institute-detect-sleep-states#459596-02](https://www.kaggle.com/competitions/child-mind-institute-detect-sleep-states/discussion/459596) |
| @cdeotte | C | 建模与训练 | 三类 building block：双向 RNN、WaveNet 式膨胀卷积、Transformer self-attention；输入输出形状均为 (batch, seq, fe | [child-mind-institute-detect-sleep-states#459596-01](https://www.kaggle.com/competitions/child-mind-institute-detect-sleep-states/discussion/459596) |

## 高票评论

_无 ≥10 票评论_

## 关联资产

- 深读：`analysis/deep/child-mind-institute-detect-sleep-states.md`
- 结构化摘要：`notes/tabular/child-mind-institute-detect-sleep-states.md`
- 归档讨论区：`intel/child-mind-institute-detect-sleep-states/`（主题 2 条有 ≥50 票帖，图证 5 个）
