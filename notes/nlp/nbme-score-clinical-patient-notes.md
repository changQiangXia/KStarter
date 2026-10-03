# NBME - Score Clinical Patient Notes

> 主题：nlp ｜ 子类：— ｜ 领域：医疗文本 ｜ 类别：Featured
> 截止：2022-XX-XX ｜ 队伍数：1500+ ｜ 机制：代码赛 ｜ 指标：微平均 F1（跨度抽取）
> 数据来源：`intel/nbme-score-clinical-patient-notes/`（80 条主题索引 + 6 篇 write-up 正文）

## 1. 任务与数据

- 预测目标：在临床病历文本中**抽取出对应"病例特征"的关键短语**（token 分类 / 跨度抽取）。
- 数据形态：**无标注数据是有标注数据的 10 倍**——2nd 明确说"这是本场最有意思的地方"，为半监督方法提供了空间。
- 构造陷阱：
  - **标注不一致**（2nd 与 4th 都指出注释质量参差）；
  - 不同病例（case_num）的跨度分布差异大 → 需要**分病例阈值**。

## 2. 方案谱系

| 方案 | 名次 | 关键点 |
| --- | --- | --- |
| 1st 方案 | 1st | 见讨论区 |
| 半监督 + 无标注数据利用 | 2nd | 强调 10 倍无标注数据是核心资源；指出标注不一致问题 |
| Meta Pseudo Labels + 知识蒸馏 | 3rd | 用元伪标签与蒸馏提升小样本表现 |
| 4 个 token 分类模型集成 + 分病例阈值 + 后处理 | 4th | DeBERTa-v3-large 4 折、MLM(0.15) 中间预训练、SmoothFocalLoss、两轮伪标签 |

## 3. 关键技巧

- **无标注数据是主要杠杆**：MLM 中间预训练 + 多轮伪标签（4th 用了两轮）。
- **分病例（case_num）设定阈值**：不同病例的最优阈值不同，统一阈值会损失分数。
- **后处理**：跨度合并、边界修正。
- **损失函数**：SmoothFocalLoss 处理类别不平衡。
- **面对噪声标注**：用伪标签与集成降低单点标注错误的影响。

## 4. 可迁移性评估

- **可直接迁移**：
  - **无标注数据 ≫ 有标注数据时，半监督是首要方向**（MLM + 伪标签）。
  - **按子群分别设阈值**（分病例/分机构/分设备）。
  - 跨度任务的后处理（合并、边界）。
- 需要前提：MLM 中间训练与伪标签需要额外算力；

  需要按子群统计样本量。
- 不建议照搬：全局统一阈值。

## 5. 对新手的关键启示

1. **先看有/无标注数据的比例**：比例悬殊时，半监督的收益通常大于换模型。
2. **阈值要分群设**（本场按病例，其他场景可按机构/品类）。
3. 与 PII Detection、Feedback 系列对照：**长文本/跨度任务的后处理是必备环节**。

## 6. 出处

- 讨论区索引：`intel/nbme-score-clinical-patient-notes/topics.md`（80 条）
- 已收录 write-up（6 篇）：
  - 1st（128 票）：https://www.kaggle.com/competitions/nbme-score-clinical-patient-notes/discussion/323095
  - 2nd（174 票）：https://www.kaggle.com/competitions/nbme-score-clinical-patient-notes/discussion/323085
  - 3rd（72 票）：https://www.kaggle.com/competitions/nbme-score-clinical-patient-notes/discussion/322832
  - 4th（126 票）：https://www.kaggle.com/competitions/nbme-score-clinical-patient-notes/discussion/322799
  - 20th（73 票）：https://www.kaggle.com/competitions/nbme-score-clinical-patient-notes/discussion/323094
