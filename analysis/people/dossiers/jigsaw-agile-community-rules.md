# Jigsaw - Agile Community Rules Classification

> `jigsaw-agile-community-rules` ｜ Featured ｜ 指标 94635_Jigsaw_Rules_AUC ｜ 2445 队 ｜ 截止 2025-10-23

本页汇总该场 **2 条 ≥50 票 GM 主题帖**、**7 条断言**、**0 条高票评论**。

## GM 主题帖

| 票 | 选手 | 日期 | 主题 |
| --- | --- | --- | --- |
| 127 | [@cnumber](https://www.kaggle.com/cnumber) | 2025-09-17 | [The rules are revealed](https://www.kaggle.com/competitions/jigsaw-agile-community-rules/discussion/607941) |
| 118 | [@wowfattie](https://www.kaggle.com/wowfattie) | 2025-10-25 | [1st place solution](https://www.kaggle.com/competitions/jigsaw-agile-community-rules/discussion/613305) |

## 断言（条件→动作→机制→结果）

| 选手 | 等级 | 阶段 | 动作（节选） | 出处 |
| --- | --- | --- | --- | --- |
| @wowfattie | A | 验证设计 | 用 public LB 验证：host 说明公私有随机划分（public 约 30%、方差低），所有模型在线微调并用 public LB 选型 | [jigsaw-agile-community-rules#613305-01](https://www.kaggle.com/competitions/jigsaw-agile-community-rules/discussion/613305) |
| @wowfattie | A | 集成与融合 | 对每个模型输出先按 rule 排名，再归一化到 [0,1] 后集成；最终 6 模型加权平均 | [jigsaw-agile-community-rules#613305-05](https://www.kaggle.com/competitions/jigsaw-agile-community-rules/discussion/613305) |
| @wowfattie | B | 特征与数据工程 | 去重时排除 subreddit 列；使用 LLM 内置 chat template；把 test.csv 例子上采样一次（等效 train 1 epoch 加 test 2 epo | [jigsaw-agile-community-rules#613305-02](https://www.kaggle.com/competitions/jigsaw-agile-community-rules/discussion/613305) |
| @wowfattie | B | 建模与训练 | 手动把 Yes/No 之外的 token 从 loss 中排除 | [jigsaw-agile-community-rules#613305-03](https://www.kaggle.com/competitions/jigsaw-agile-community-rules/discussion/613305) |
| @wowfattie | B | 工程/流程 | 只 forward 取最后一个 token 的 logits；构造 Yes/No 变体集（大小写、首字母、True/False 与空格前缀）；分数等于 sigmoid(Yes 与  | [jigsaw-agile-community-rules#613305-04](https://www.kaggle.com/competitions/jigsaw-agile-community-rules/discussion/613305) |
| @cnumber | C | 数据理解 | 公共规则可见（no advertising、no legal advice）；私有规则隐藏（no financial advice、no medical advice、no ill | [jigsaw-agile-community-rules#607941-01](https://www.kaggle.com/competitions/jigsaw-agile-community-rules/discussion/607941) |
| @cnumber | C | 复盘与流程 | 提出核心问题：合成数据是否 work（帖子未给结论） | [jigsaw-agile-community-rules#607941-02](https://www.kaggle.com/competitions/jigsaw-agile-community-rules/discussion/607941) |

## 高票评论

_无 ≥10 票评论_

## 关联资产

- 深读：`analysis/deep/jigsaw-agile-community-rules.md`
- 结构化摘要：`notes/nlp/jigsaw-agile-community-rules.md`
- 归档讨论区：`intel/jigsaw-agile-community-rules/`（主题 2 条有 ≥50 票帖，图证 0 个）
