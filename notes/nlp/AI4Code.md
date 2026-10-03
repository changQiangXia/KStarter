# Google AI4Code（代码与注释顺序预测）

> 主题：nlp ｜ 子类：— ｜ 领域：代码理解 ｜ 类别：Featured
> 截止：2022-XX-XX ｜ 队伍数：1000+ ｜ 机制：代码赛 ｜ 指标：Kendall tau（排序相关性）
> 数据来源：`intel/AI4Code/`（80 条主题索引 + 6 篇 write-up 正文）

## 1. 任务与数据

- 预测目标：给定 Jupyter Notebook 的代码单元格与文档单元格（markdown），**恢复它们的原始排列顺序**（本质是排序/关系预测）。
- 数据形态：代码片段 + 自然语言文档，混合模态但主体是文本。
- 构造陷阱：
  - **排序任务**：输出是排列而非标签，Kendall tau 对局部顺序敏感；
  - 大量"看似无关"的对应关系（注释与代码的语义关联弱）；
  - notebook 的结构噪声（执行顺序 ≠ 展示顺序）。

## 2. 方案特征

| 方案类型 | 说明 |
| --- | --- |
| 关系预测 + 排序重建 | 先预测"某代码是否在某文档之前"这类成对关系，再把关系还原成全局顺序 |
| 领域理解帖（高票） | 作者自述"看不懂高手的方案，于是退一步理解领域"，系统整理了任务本质与常用做法 |

## 3. 关键技巧

- **把排序问题分解为成对关系预测**，再用排序算法（如拓扑排序）重建顺序。
- **用上下文特征**：相邻单元的类型序列、代码/文档的语言学线索。
- **领域理解优先**：本场最高价值的公开材料是一篇"退一步理解领域"的说明帖，而非某个具体模型。

## 4. 可迁移性评估

- **可直接迁移**：
  - **排序任务 → 成对关系 + 重建** 的范式（检索、推荐排序通用）；
  - 指标是排序相关性时，评估要注意局部顺序误差；
  - "先理解领域再建模"的准备工作本身可以产出高价值文档。
- 需要前提：代码与自然语言的混合处理能力。
- 不建议照搬：把排序当分类处理。

## 5. 对新手的关键启示

1. **排序类任务的通用分解**：成对关系 → 全局顺序。
2. **看不懂高分方案时，先退一步理解领域**（本场高票帖的示范）。
3. 与检索/推荐类比赛对照（Otto、H&M）：排序问题的解法可以互相借鉴。

## 6. 轻读结论（2026-10 补）

**一句话**：code 顺序已知的 markdown 排序赛——**LTR 重构 + 长上下文 + 槽位后处理**三件套；指标由长 notebook 主导。

- 1st（62 票）：单 listwise deberta-v3-large；MLM 1024（3 天）→微调 2048（7 天）→推理 5120（6h）；MAE+LSTM head；先预测 code/md，再把 code 按 GT 排；xlm-r/mdeberta 明显更差。
- 2nd（82 票）：逐 cell CodeBERT + 双 decoder 互注意；1D conv → N+1 槽位；3 输出 + BCE；后处理最小化错位概率和（期望交换数代理）；共享 CodeBERT 全 0.9113/非英 0.8652，CodeBERT+mpnet 非英 0.8825 但总分略降。
- 4th：recall（tau 897）→ pairwise rank（905）→ context rank（+0.004）；最终 9170；8×V100×30h。
- 11th：Nested Transformers（cell 级 + notebook 级注意）。

**裁决**：后处理不是 argmax 而是"最小化期望错位"；长序列与长 notebook 采样权重直接决定 Kendall tau。

**悬案**：3rd–10th 方案未收录；Kendall tau 口径与 oracle 上界未量化。

## 7. 图表证据

![2nd 的双塔+双 decoder](../../intel/AI4Code/bodies/343659_img/01.png)

**图 1**（topic 343659）：code/md 两塔 → 1D conv 槽位 → 双 TransformerDecoder 互注意 → code×md / md×md 矩阵。

![11th 的 Nested Transformers](../../intel/AI4Code/bodies/343680_img/01.png)

**图 2**（topic 343680）：cell transformer + notebook transformer 两级结构。

## 8. 出处

- 讨论区索引：`intel/AI4Code/topics.md`（80 条）
- 已收录 write-up（6 篇）：
  - 领域理解帖（100 票）：https://www.kaggle.com/competitions/AI4Code/discussion/328905
  - 1st（62 票）：https://www.kaggle.com/competitions/AI4Code/discussion/360501
  - 2nd（82 票）：https://www.kaggle.com/competitions/AI4Code/discussion/343659
- 轻读全本：`analysis/deep/AI4Code.md`（Tier B 轻读：对照矩阵/裁决/证据分级/悬案 + 2 图证）
