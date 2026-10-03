# Feedback Prize - Predicting Effective Arguments

> `feedback-prize-effectiveness` ｜ Featured ｜ 指标 Multiclass Loss ｜ 1557 队 ｜ 截止 2022-08-23

本页汇总该场 **3 条 ≥50 票 GM 主题帖**、**10 条断言**、**2 条高票评论**。

## GM 主题帖

| 票 | 选手 | 日期 | 主题 |
| --- | --- | --- | --- |
| 107 | [@cpmpml](https://www.kaggle.com/cpmpml) | 2022-08-24 | [Some more lessons](https://www.kaggle.com/competitions/feedback-prize-effectiveness/discussion/347425) |
| 77 | [@conjuring92](https://www.kaggle.com/conjuring92) | 2022-08-24 | [3rd Place Solution - Span MLM + T5 Augmentations](https://www.kaggle.com/competitions/feedback-prize-effectiveness/discussion/347433) |
| 75 | [@philippsinger](https://www.kaggle.com/philippsinger) | 2022-08-24 | [Team Hydrogen: Efficiency Prize 1st Place](https://www.kaggle.com/competitions/feedback-prize-effectiveness/discussion/347537) |

## 断言（条件→动作→机制→结果）

| 选手 | 等级 | 阶段 | 动作（节选） | 出处 |
| --- | --- | --- | --- | --- |
| @conjuring92 | A | 特征与数据工程 | 继续 MLM 预训练 backbone：mask 概率改为 40-50%（非 15%）、掩码连续 3 到 15 个 token、chunk/max length 720 对齐平均作 | [feedback-prize-effectiveness#347433-02](https://www.kaggle.com/competitions/feedback-prize-effectiveness/discussion/347433) |
| @conjuring92 | A | 特征与数据工程 | 训练 seq2seq T5-large：输入为效果标签加 discourse 类型加 prompt 加左右上下文，输出为 discourse 文本；生成样本按 0-50% 比例混入 | [feedback-prize-effectiveness#347433-03](https://www.kaggle.com/competitions/feedback-prize-effectiveness/discussion/347433) |
| @conjuring92 | A | 复盘与流程 | 按影响排序：Span MLM 0.02 到 0.03、AWP 0.005 到 0.01、prompts 0.002 到 0.005、T5 增广 -0.002 到 0.005、mas | [feedback-prize-effectiveness#347433-04](https://www.kaggle.com/competitions/feedback-prize-effectiveness/discussion/347433) |
| @conjuring92 | A | 复盘与流程 | 稳定训练要素：参数选择、cosine、MLM 任务适应、AWP、mask 增广加 multi-sample dropout、逐层 LR 衰减、全精度；负结果：伪标签（作者称是大漏） | [feedback-prize-effectiveness#347433-05](https://www.kaggle.com/competitions/feedback-prize-effectiveness/discussion/347433) |
| @philippsinger | A | 建模与训练 | 用大集成（含 2 级模型）给上一届 Feedback 生成伪标签（4 轮）+ 给本赛 train 生成 OOF 伪标签，两份软标签合并训练单个新模型且完全不用原始硬标签；priva | [feedback-prize-effectiveness#347537-01](https://www.kaggle.com/competitions/feedback-prize-effectiveness/discussion/347537) |
| @philippsinger | A | 工程/流程 | 预 tokenize 后按序列长度排序 + dynamic padding，比按字符长度排序快 40 秒；deberta-small/base 也可行，base 单模不到 2 分钟 | [feedback-prize-effectiveness#347537-02](https://www.kaggle.com/competitions/feedback-prize-effectiveness/discussion/347537) |
| @conjuring92 | B | 特征与数据工程 | 预处理：为每种 discourse 类型插入 span 起止特殊 token；essay 前加 [TOPIC] 段；加 [SOE]/[EOE] 标记首尾；再按 span 分类架构建 | [feedback-prize-effectiveness#347433-01](https://www.kaggle.com/competitions/feedback-prize-effectiveness/discussion/347433) |
| @cpmpml | C | 复盘与流程 | 整场基于错误假设复用 AI4Code 复杂管线；最后一天才发现 Deberta 能直接吃 2048 tokens | [feedback-prize-effectiveness#347425-01](https://www.kaggle.com/competitions/feedback-prize-effectiveness/discussion/347425) |
| @cpmpml | C | 复盘与流程 | 教训：先简单基线再逐步加料；读 top 方案与论文；亲自测试他人结论（作者只试一次伪标签就相信报告）；不要把鸡蛋放一个篮子 | [feedback-prize-effectiveness#347425-02](https://www.kaggle.com/competitions/feedback-prize-effectiveness/discussion/347425) |
| @cpmpml | C | 复盘与流程 | 作者总结：每场重置，过去拿过奖不代表现在更懂；应尽早入场、组队、保持谦逊 | [feedback-prize-effectiveness#347425-03](https://www.kaggle.com/competitions/feedback-prize-effectiveness/discussion/347425) |

## 高票评论

| 票 | 选手 | 日期 | 摘录 | 出处 |
| --- | --- | --- | --- | --- |
| 13 | @philippsinger | 2022-08-24 | I personally think it is a just a tuning thing, we tried it a few times and it did not bring anything. As with | [347425](https://www.kaggle.com/competitions/feedback-prize-effectiveness/discussion/347425) |
| 11 | @cdeotte | 2022-08-26 | Congratulations Psi and Yauhen! Great solution! Pre-train models on the pseudo labels and finetune it only on  | [347536](https://www.kaggle.com/competitions/feedback-prize-effectiveness/discussion/347536) |

## 关联资产

- 深读：`analysis/deep/feedback-prize-effectiveness.md`
- 结构化摘要：`notes/nlp/feedback-prize-effectiveness.md`
- 归档讨论区：`intel/feedback-prize-effectiveness/`（主题 3 条有 ≥50 票帖，图证 1 个）
