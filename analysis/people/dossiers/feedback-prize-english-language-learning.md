# Feedback Prize - English Language Learning

> `feedback-prize-english-language-learning` ｜ Featured ｜ 指标 Mean Weighted Columnwise Root Mean Squared Error ｜ 2654 队 ｜ 截止 2022-11-29

本页汇总该场 **3 条 ≥50 票 GM 主题帖**、**12 条断言**、**5 条高票评论**。

## GM 主题帖

| 票 | 选手 | 日期 | 主题 |
| --- | --- | --- | --- |
| 197 | [@cdeotte](https://www.kaggle.com/cdeotte) | 2022-09-11 | [RAPIDS SVR starter kit [CV 0.450, LB 0.44x]](https://www.kaggle.com/competitions/feedback-prize-english-language-learning/discussion/351577) |
| 141 | [@cdeotte](https://www.kaggle.com/cdeotte) | 2022-11-30 | [3rd Place Solution - Congratulations New Competition Grandmaster Amed!](https://www.kaggle.com/competitions/feedback-prize-english-language-learning/discussion/369609) |
| 74 | [@philippsinger](https://www.kaggle.com/philippsinger) | 2022-11-30 | [5th place solution](https://www.kaggle.com/competitions/feedback-prize-english-language-learning/discussion/369578) |

## 断言（条件→动作→机制→结果）

| 选手 | 等级 | 阶段 | 动作（节选） | 出处 |
| --- | --- | --- | --- | --- |
| @cdeotte | A | 集成与融合 | 用 hill climbing（从最好单模开始，逐轮尝试所有模型与 -0.5 到 0.5 的权重）选模型并定权；允许负权重 | [feedback-prize-english-language-learning#369609-01](https://www.kaggle.com/competitions/feedback-prize-english-language-learning/discussion/369609) |
| @philippsinger | A | 验证设计 | 每个实验跑 3 个不同 seed，只比较平均；平均提升才升到 5 折，再用 3-seed blends 复核；避免单 seed 噪声误导决策 | [feedback-prize-english-language-learning#369578-01](https://www.kaggle.com/competitions/feedback-prize-english-language-learning/discussion/369578) |
| @philippsinger | A | 建模与训练 | 变体：token 长度 512、1024、2048（全部动态 padding）；pooling 用 CLS 或 GeM；backbone 覆盖 Deberta-v3-base/la | [feedback-prize-english-language-learning#369578-02](https://www.kaggle.com/competitions/feedback-prize-english-language-learning/discussion/369578) |
| @philippsinger | A | 建模与训练 | 只用本赛 train 训集成 → 对上一届数据预测（排除本赛数据）→ 先 pretrain 伪标签、再在本赛 train 上 finetune；重复 3 次；预训练+微调避免调整伪 | [feedback-prize-english-language-learning#369578-03](https://www.kaggle.com/competitions/feedback-prize-english-language-learning/discussion/369578) |
| @philippsinger | A | 集成与融合 | 最佳提交用 Nelder-Mead 按目标列分别优化权重，并把权重限制在 1 到 3；作者有一个无限制（含负权重）的 best CV 提交本可 private 第 2，但选了保守版 | [feedback-prize-english-language-learning#369578-04](https://www.kaggle.com/competitions/feedback-prize-english-language-learning/discussion/369578) |
| @cdeotte | B | 建模与训练 | 从 HuggingFace 预训练模型直接提 embedding，喂 RAPIDS cuML SVR，不做任何微调 | [feedback-prize-english-language-learning#351577-01](https://www.kaggle.com/competitions/feedback-prize-english-language-learning/discussion/351577) |
| @cdeotte | B | 特征与数据工程 | 复刻 PetFinder 1st 做法：数十个未微调模型的 embedding 拼接（上万列）后训练 cuML SVR | [feedback-prize-english-language-learning#351577-02](https://www.kaggle.com/competitions/feedback-prize-english-language-learning/discussion/351577) |
| @cdeotte | B | 集成与融合 | 每天训练多样模型后跑 hill climbing；观察被选顺序：最好 CV 的模型不是第一个入选 | [feedback-prize-english-language-learning#369609-02](https://www.kaggle.com/competitions/feedback-prize-english-language-learning/discussion/369609) |
| @cdeotte | B | 建模与训练 | 高影响技巧：不同目标不同 loss 权重、clip grad norm 设为 10、dropout 设为 0、train max_len 2048 而 infer 640、batc | [feedback-prize-english-language-learning#369609-03](https://www.kaggle.com/competitions/feedback-prize-english-language-learning/discussion/369609) |
| @cdeotte | B | 复盘与流程 | 用 FP1 伪标签后单模 CV 从 0.4470 提升到 0.4370，但 LB 不升；且 FP1 目标分布高于 FP3 | [feedback-prize-english-language-learning#369609-04](https://www.kaggle.com/competitions/feedback-prize-english-language-learning/discussion/369609) |
| @philippsinger | B | 复盘与流程 | 无效：增广（回归尤其）、不同损失、TFIDF、其他 backbone（T5、GPT 等，Deberta 太强）、2 级模型或 stacker | [feedback-prize-english-language-learning#369578-05](https://www.kaggle.com/competitions/feedback-prize-english-language-learning/discussion/369578) |
| @cdeotte | C | 验证设计 | 微调 transformer 时使用与 SVR 完全相同的 folds；也可复用其他赛训练好的模型去头提 embedding；补充元特征与不同层 embedding | [feedback-prize-english-language-learning#351577-03](https://www.kaggle.com/competitions/feedback-prize-english-language-learning/discussion/351577) |

## 高票评论

| 票 | 选手 | 日期 | 摘录 | 出处 |
| --- | --- | --- | --- | --- |
| 29 | @cdeotte | 2022-11-30 | IMO Models want the most train data possible. Training with max_len=2048 allows the model to learn from all th | [369609](https://www.kaggle.com/competitions/feedback-prize-english-language-learning/discussion/369609) |
| 20 | @cdeotte | 2022-11-30 | @datafan07 Also note that Deberta uses "relative embeddings". Therefore if WORD_A in position 1500 relates to  | [369609](https://www.kaggle.com/competitions/feedback-prize-english-language-learning/discussion/369609) |
| 15 | @cdeotte | 2022-09-12 | Great. Note that you can speed up inference by saving the trained SVR during one notebook version, then loadin | [351577](https://www.kaggle.com/competitions/feedback-prize-english-language-learning/discussion/351577) |
| 10 | @cdeotte | 2022-10-10 | The best way to determine which is better for a particular task is try both. I choose SVR here because it has  | [351577](https://www.kaggle.com/competitions/feedback-prize-english-language-learning/discussion/351577) |
| 10 | @cdeotte | 2022-11-30 | @amed can share the details. These are two of his tricks. I think the way "2 x pooling" works is as follows. A | [369609](https://www.kaggle.com/competitions/feedback-prize-english-language-learning/discussion/369609) |

## 关联资产

- 深读：`analysis/deep/feedback-prize-english-language-learning.md`
- 结构化摘要：`notes/nlp/feedback-prize-english-language-learning.md`
- 归档讨论区：`intel/feedback-prize-english-language-learning/`（主题 3 条有 ≥50 票帖，图证 3 个）
