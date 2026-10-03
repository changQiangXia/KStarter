# NBME - Score Clinical Patient Notes

> `nbme-score-clinical-patient-notes` ｜ Featured ｜ 指标 Medical Board F-Beta ｜ 1471 队 ｜ 截止 2022-05-03

本页汇总该场 **2 条 ≥50 票 GM 主题帖**、**10 条断言**、**2 条高票评论**。

## GM 主题帖

| 票 | 选手 | 日期 | 主题 |
| --- | --- | --- | --- |
| 174 | [@cpmpml](https://www.kaggle.com/cpmpml) | 2022-05-04 | [#2 solution](https://www.kaggle.com/competitions/nbme-score-clinical-patient-notes/discussion/323085) |
| 72 | [@conjuring92](https://www.kaggle.com/conjuring92) | 2022-05-04 | [3rd Place Solution: Meta Pseudo Labels + Knowledge Distillation](https://www.kaggle.com/competitions/nbme-score-clinical-patient-notes/discussion/322832) |

## 断言（条件→动作→机制→结果）

| 选手 | 等级 | 阶段 | 动作（节选） | 出处 |
| --- | --- | --- | --- | --- |
| @conjuring92 | A | 建模与训练 | 用患者笔记继续 MLM 预训练所有 DeBERTa（mask 概率 0.2），后续训练使用 task-adapted backbone | [nbme-score-clinical-patient-notes#322832-01](https://www.kaggle.com/competitions/nbme-score-clinical-patient-notes/discussion/322832) |
| @conjuring92 | A | 建模与训练 | 对比标准伪标签、弱监督对比自训练、Meta Pseudo Labels；MPL 最好（soft 与 hard 伪标签混用增加多样性）；学生随后用真实标注再微调并加 SWA | [nbme-score-clinical-patient-notes#322832-02](https://www.kaggle.com/competitions/nbme-score-clinical-patient-notes/discussion/322832) |
| @conjuring92 | A | 建模与训练 | 蒸馏损失：0.15×有标注 BCE 加 0.15×教师伪标签 BCE 加 0.7×未标注伪标签 BCE；文献与学生超过教师的可能性支持该设计 | [nbme-score-clinical-patient-notes#322832-03](https://www.kaggle.com/competitions/nbme-score-clinical-patient-notes/discussion/322832) |
| @conjuring92 | A | 特征与数据工程 | 给 feature 文本加 case 前缀 token，为每个 case 建 10 个新 token（如 [QA CASE=0]），让模型区分同名特征来自哪个病例 | [nbme-score-clinical-patient-notes#322832-04](https://www.kaggle.com/competitions/nbme-score-clinical-patient-notes/discussion/322832) |
| @conjuring92 | A | 复盘与流程 | 细节：多标签 token 分类（inside/begin/end）、拼接最后 12 层 hidden、重初始化最后 4 到 12 层、cosine warmup、混合精度、8-bi | [nbme-score-clinical-patient-notes#322832-05](https://www.kaggle.com/competitions/nbme-score-clinical-patient-notes/discussion/322832) |
| @cpmpml | B | 建模与训练 | 在 Squad v2 上用 HF run_qa.py 自预训练 backbone（保存前 3 个 epoch 的 checkpoint 供下游挑选），再加载权重训练比赛模型 | [nbme-score-clinical-patient-notes#323085-03](https://www.kaggle.com/competitions/nbme-score-clinical-patient-notes/discussion/323085) |
| @cpmpml | B | 建模与训练 | 用未四舍五入的 token 概率做伪标签；自定义损失忽略 0.5 附近样本；只做一轮 | [nbme-score-clinical-patient-notes#323085-04](https://www.kaggle.com/competitions/nbme-score-clinical-patient-notes/discussion/323085) |
| @cpmpml | C | 数据理解 | 不修正标注（测试标注同样不一致）；假设标注者更易漏标重复出现而非首次出现，据此认为标注存在序列依赖、RNN 有帮助 | [nbme-score-clinical-patient-notes#323085-01](https://www.kaggle.com/competitions/nbme-score-clinical-patient-notes/discussion/323085) |
| @cpmpml | C | 特征与数据工程 | 字符级后处理：空格在词首或词尾时清零；对 yof/yom，按 feature 是性别还是年龄保留 om/of 的对应字符或前一 token 概率 | [nbme-score-clinical-patient-notes#323085-02](https://www.kaggle.com/competitions/nbme-score-clinical-patient-notes/discussion/323085) |
| @cpmpml | C | 复盘与流程 | 实验 fgm、vat、sift、smart 等对抗训练变体 | [nbme-score-clinical-patient-notes#323085-05](https://www.kaggle.com/competitions/nbme-score-clinical-patient-notes/discussion/323085) |

## 高票评论

| 票 | 选手 | 日期 | 摘录 | 出处 |
| --- | --- | --- | --- | --- |
| 12 | @cdeotte | 2022-03-31 | Here is the link for the image (YouTube video) above https://www.youtube.com/watch?v=PXc_SlnT2g0 This shows ma | [315707](https://www.kaggle.com/competitions/nbme-score-clinical-patient-notes/discussion/315707) |
| 12 | @cpmpml | 2022-05-09 | I have a PhD in machine learning but it is from a long long time ago and not much relevant. I then took Andrew | [323085](https://www.kaggle.com/competitions/nbme-score-clinical-patient-notes/discussion/323085) |

## 关联资产

- 深读：`analysis/deep/nbme-score-clinical-patient-notes.md`
- 结构化摘要：`notes/nlp/nbme-score-clinical-patient-notes.md`
- 归档讨论区：`intel/nbme-score-clinical-patient-notes/`（主题 2 条有 ≥50 票帖，图证 0 个）
