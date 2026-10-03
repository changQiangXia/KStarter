# Bengali.AI Speech Recognition（精简）

> 主题：audio（语音识别）｜ 子类：— ｜ 领域：低资源语音 ｜ 类别：Research ｜ 截止：2023-10-17 ｜ 队伍数：744 ｜ 指标：WER
> 出处：`intel/bengaliai-speech/`（80 条主题索引 + 6 篇 write-up 正文）

## 任务

孟加拉语语音转文本（低资源语言的 ASR），指标为词错误率（WER）。

## 关键要点

- 5th 的路径很典型：**从公开基线（YellowKing 流程）起步 → 换骨干为 IndicWav2Vec → 重置 CTC 层**，再叠加公开方案的集成——"**集成有效**"（标题即结论）。
- **低资源语言靠领域预训练模型**（IndicWav2Vec 是针对印度语系的语音模型）。
- CTC 解码头重置是换骨干后的标准动作。

## 可迁移要点

- **低资源语音/文本任务优先找领域预训练模型**（比通用模型强得多）。
- 换骨干后要重置任务头并重新训练。
- 集成是低资源任务的稳定增益来源。

## 出处

- 讨论区索引：`intel/bengaliai-speech/topics.md`
- 1st（107 票）：https://www.kaggle.com/competitions/bengaliai-speech/discussion/447961
- 2nd（41 票）：https://www.kaggle.com/competitions/bengaliai-speech/discussion/447976
- 3rd（43 票）：https://www.kaggle.com/competitions/bengaliai-speech/discussion/447957
