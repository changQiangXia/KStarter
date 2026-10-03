# Learning Agency Lab - Automated Essay Scoring 2.0

> `learning-agency-lab-automated-essay-scoring-2` ｜ Featured ｜ 指标 Cohen Kappa Score ｜ 2706 队 ｜ 截止 2024-07-02

本页汇总该场 **4 条 ≥50 票 GM 主题帖**、**16 条断言**、**1 条高票评论**。

## GM 主题帖

| 票 | 选手 | 日期 | 主题 |
| --- | --- | --- | --- |
| 218 | [@cdeotte](https://www.kaggle.com/cdeotte) | 2024-04-25 | [DeBERTa Starter Suggestions and Tips - LB 0.800+](https://www.kaggle.com/competitions/learning-agency-lab-automated-essay-scoring-2/discussion/497832) |
| 176 | [@cdeotte](https://www.kaggle.com/cdeotte) | 2024-04-22 | [More Train Data Available!](https://www.kaggle.com/competitions/learning-agency-lab-automated-essay-scoring-2/discussion/496906) |
| 95 | [@tascj0](https://www.kaggle.com/tascj0) | 2024-07-03 | [4th place solution](https://www.kaggle.com/competitions/learning-agency-lab-automated-essay-scoring-2/discussion/516639) |
| 86 | [@ferdinandlimburg](https://www.kaggle.com/ferdinandlimburg) | 2024-07-03 | [1st Place Solution - Trust CV (and LB a bit)](https://www.kaggle.com/competitions/learning-agency-lab-automated-essay-scoring-2/discussion/516791) |

## 断言（条件→动作→机制→结果）

| 选手 | 等级 | 阶段 | 动作（节选） | 出处 |
| --- | --- | --- | --- | --- |
| @cdeotte | A | 建模与训练 | 按回归 + 长序列 + batch/LR 调优发布的 starter 达到 CV 0.822 / LB 0.800，作者称超过当时所有公开 DeBERTa 单模 | [learning-agency-lab-automated-essay-scoring-2#497832-04](https://www.kaggle.com/competitions/learning-agency-lab-automated-essay-scoring-2/discussion/497832) |
| @tascj0 | A | 数据理解 | 加数据源 tag（如 [A]/[B] 前缀）、加数据源分类头、部分模型按数据源分别用分类头、按 non-persuade 分数早停；作者假设两源分数采集方式不同，混合训练损害拟合 | [learning-agency-lab-automated-essay-scoring-2#516639-01](https://www.kaggle.com/competitions/learning-agency-lab-automated-essay-scoring-2/discussion/516639) |
| @tascj0 | A | 验证设计 | 对抗验证 train vs test AUC 0.65 到 0.675；本地用 51% persuade 加 18% non-persuade 训练、31% non-persuad | [learning-agency-lab-automated-essay-scoring-2#516639-02](https://www.kaggle.com/competitions/learning-agency-lab-automated-essay-scoring-2/discussion/516639) |
| @tascj0 | A | 集成与融合 | 3 个模型（deberta-large、deberta-v3-large、Qwen2-1.5B-Instruct）× 5 折 × 3 seeds 共 45 个预测取平均；阈值在 O | [learning-agency-lab-automated-essay-scoring-2#516639-03](https://www.kaggle.com/competitions/learning-agency-lab-automated-essay-scoring-2/discussion/516639) |
| @ferdinandlimburg | A | 验证设计 | 先 pretrain old 再 finetune new，阶段内用 prompt_id 加 score 分层 5 折；public LB 至少加 0.015，CV-LB 相关性显 | [learning-agency-lab-automated-essay-scoring-2#516791-01](https://www.kaggle.com/competitions/learning-agency-lab-automated-essay-scoring-2/discussion/516791) |
| @ferdinandlimburg | A | 建模与训练 | 所有环节 3-seed 平均；只重做 fine-tune 阶段换 seed（不重跑预训练）省时间；模型目录约 2TB | [learning-agency-lab-automated-essay-scoring-2#516791-02](https://www.kaggle.com/competitions/learning-agency-lab-automated-essay-scoring-2/discussion/516791) |
| @ferdinandlimburg | A | 后处理 | 自定义阈值（如 1/2 用 1.7、5/6 用 4.9）同时：过拟合标签、纠正不平衡误差、优化 QWK；阈值随 seed 波动大，必须用 3 seeds 算，用 scipy Pow | [learning-agency-lab-automated-essay-scoring-2#516791-04](https://www.kaggle.com/competitions/learning-agency-lab-automated-essay-scoring-2/discussion/516791) |
| @ferdinandlimburg | A | 集成与融合 | 预计算每模型自己的阈值（3 seeds），并把集成权重同时用于阈值；多数提交用简单平均；最大集成 7 模型 × 3 seeds 等于 21 个 Deberta large | [learning-agency-lab-automated-essay-scoring-2#516791-05](https://www.kaggle.com/competitions/learning-agency-lab-automated-essay-scoring-2/discussion/516791) |
| @cdeotte | B | 建模与训练 | 改用 AutoModelForSequenceClassification(num_labels=1) 做回归（target 转 float32），并在回归时移除 dropout | [learning-agency-lab-automated-essay-scoring-2#497832-01](https://www.kaggle.com/competitions/learning-agency-lab-automated-essay-scoring-2/discussion/497832) |
| @cdeotte | B | 建模与训练 | DeBERTa 用 max_length 1024/1536；RoBERTa 类改用 LongFormer；tokenizer 加 trim_offsets=False 保留空白信 | [learning-agency-lab-automated-essay-scoring-2#497832-02](https://www.kaggle.com/competitions/learning-agency-lab-automated-essay-scoring-2/discussion/497832) |
| @cdeotte | B | 工程/流程 | 实验阶段用 deberta-v3-small/xsmall 快速试参，定参后训练 large；作者最佳为 bs=8、起始 LR 1e-5 | [learning-agency-lab-automated-essay-scoring-2#497832-03](https://www.kaggle.com/competitions/learning-agency-lab-automated-essay-scoring-2/discussion/497832) |
| @cdeotte | B | 数据工程 | 直接用 Persuade corpus 的 25996 条训练，比比赛 train 多出 8689 条样本 | [learning-agency-lab-automated-essay-scoring-2#496906-01](https://www.kaggle.com/competitions/learning-agency-lab-automated-essay-scoring-2/discussion/496906) |
| @cdeotte | B | 验证设计 | 用探针 notebook 把测试集与语料匹配，命中则用语料标签预测 | [learning-agency-lab-automated-essay-scoring-2#496906-03](https://www.kaggle.com/competitions/learning-agency-lab-automated-essay-scoring-2/discussion/496906) |
| @tascj0 | B | 工程/流程 | 按总 token 数把 batch 切成 micro batch，loss 按 micro batch token 占比缩放后再累积；并改 DeBERTa 实现（训练提速 15%+ | [learning-agency-lab-automated-essay-scoring-2#516639-04](https://www.kaggle.com/competitions/learning-agency-lab-automated-essay-scoring-2/discussion/516639) |
| @ferdinandlimburg | B | 建模与训练 | 第一轮用 mean(score, ensemble_pred)，第二轮用纯预测（重训后的集成）；始终用未取整 float；第一轮 CV 大幅提升/LB 略升，第二轮 CV 再升但  | [learning-agency-lab-automated-essay-scoring-2#516791-03](https://www.kaggle.com/competitions/learning-agency-lab-automated-essay-scoring-2/discussion/516791) |
| @cdeotte | C | 建模与训练 | 训练时把这些列作为辅助目标一起预测，提交时忽略 | [learning-agency-lab-automated-essay-scoring-2#496906-02](https://www.kaggle.com/competitions/learning-agency-lab-automated-essay-scoring-2/discussion/496906) |

## 高票评论

| 票 | 选手 | 日期 | 摘录 | 出处 |
| --- | --- | --- | --- | --- |
| 10 | @cdeotte | 2024-05-01 | We should try both. However note that OOF is 6 more features whereas the embeddings are 1024 new features whic | [497832](https://www.kaggle.com/competitions/learning-agency-lab-automated-essay-scoring-2/discussion/497832) |

## 关联资产

- 深读：`analysis/deep/learning-agency-lab-automated-essay-scoring-2.md`
- 结构化摘要：`notes/nlp/learning-agency-lab-automated-essay-scoring-2.md`
- 归档讨论区：`intel/learning-agency-lab-automated-essay-scoring-2/`（主题 4 条有 ≥50 票帖，图证 1 个）
