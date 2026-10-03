# Linking Writing Processes to Writing Quality

> `linking-writing-processes-to-writing-quality` ｜ Featured ｜ 指标 Mean Squared Error ｜ 1876 队 ｜ 截止 2024-01-09

本页汇总该场 **1 条 ≥50 票 GM 主题帖**、**4 条断言**、**1 条高票评论**。

## GM 主题帖

| 票 | 选手 | 日期 | 主题 |
| --- | --- | --- | --- |
| 79 | [@darraghdog](https://www.kaggle.com/darraghdog) | 2024-01-10 | [[3rd place solution] Blend MLM pretrained DeBERTa & GBM](https://www.kaggle.com/competitions/linking-writing-processes-to-writing-quality/discussion/466906) |

## 断言（条件→动作→机制→结果）

| 选手 | 等级 | 阶段 | 动作（节选） | 出处 |
| --- | --- | --- | --- | --- |
| @darraghdog | A | 集成与融合 | GBM 集成（165 个公开特征：LGB、XGB、CatBoost、LightAutoML、shallow NN）与 Deberta 集成（在 persuade 语料 MLM 预训 | [linking-writing-processes-to-writing-quality#466906-01](https://www.kaggle.com/competitions/linking-writing-processes-to-writing-quality/discussion/466906) |
| @darraghdog | A | 特征与数据工程 | 把遮蔽字符 q 替换为 i 或 X：预训练 DeBERTa 对 i/X 有显式 token，tokenization 更好且序列更短；并训练自定义 tokenizer | [linking-writing-processes-to-writing-quality#466906-03](https://www.kaggle.com/competitions/linking-writing-processes-to-writing-quality/discussion/466906) |
| @darraghdog | B | 验证设计 | 观察 GBM 的 LB/CV 比远好于 Deberta（Deberta CV 强但 LB 差）→ 推测 LB 按主题或学生年份划分存在域偏移 | [linking-writing-processes-to-writing-quality#466906-02](https://www.kaggle.com/competitions/linking-writing-processes-to-writing-quality/discussion/466906) |
| @darraghdog | B | 建模与训练 | deberta-v3-large 微调冻前 12 层；加入的 3 类 keystroke 特征需强 dropout/增广；更多 keystroke 特征无益；deleted tex | [linking-writing-processes-to-writing-quality#466906-04](https://www.kaggle.com/competitions/linking-writing-processes-to-writing-quality/discussion/466906) |

## 高票评论

| 票 | 选手 | 日期 | 摘录 | 出处 |
| --- | --- | --- | --- | --- |
| 10 | @darraghdog | 2024-01-10 | Using the deberta tokenizer on the reconstructed essay with letter ‘q’ results in a very long sequence of toke | [466906](https://www.kaggle.com/competitions/linking-writing-processes-to-writing-quality/discussion/466906) |

## 关联资产

- 深读：`analysis/deep/linking-writing-processes-to-writing-quality.md`
- 结构化摘要：`notes/nlp/linking-writing-processes-to-writing-quality.md`
- 归档讨论区：`intel/linking-writing-processes-to-writing-quality/`（主题 1 条有 ≥50 票帖，图证 2 个）
