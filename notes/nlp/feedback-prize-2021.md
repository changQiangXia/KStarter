# Feedback Prize - Evaluating Student Writing

> 主题：nlp ｜ 子类：— ｜ 领域：教育 ｜ 类别：Featured
> 截止：2022-03-15 ｜ 队伍数：2058 ｜ 机制：代码赛 ｜ 指标：TextOverlapF-beta（跨度重叠）
> 数据来源：`intel/feedback-prize-2021/`（120 条主题索引 + 8 篇 write-up 正文）

## 1. 任务与数据

- **预测目标**：在学生作文中**切分出 7 类论述要素**（论点、证据、结论等）的文本跨度（span），本质是**序列标注 / 跨度抽取**。
- **数据形态**：长文本 + 字符级标注；指标是跨度重叠的 F-beta。
- **构造陷阱**：长文本需要滑动窗口切分；跨度边界对指标影响大（后处理收益高）。

## 2. 验证方案

| 方案 | 使用者 | 说明 |
| --- | --- | --- |
| 分组 K 折（按文章） | 多队 | 避免同一文章跨折 |
| CV-LB 对齐确认 | 1st / 3rd | 1st 的 CV 0.748 ≈ LB 0.742，一致性良好 |
| 后处理单独验证 | 2nd | 后处理带来的提升单独量化 |

## 3. 方案谱系

| 方案 | 名次 | 关键点 |
| --- | --- | --- |
| 长文本模型组合 + 后处理 + **加权框融合** | 2nd | 把目标检测里的 **Weighted Box Fusion** 迁移到文本跨度抽取；后处理带来显著 CV/LB 提升；模型多样性强（多种长序列模型） |
| Transformer 序列标注 + 堆叠框架 | 3rd | 7 类论述要素分别建模，再用堆叠整合 |
| 多种长文本模型 + 集成 | 1st / 4th | 见讨论区 |

## 4. 关键技巧

- **跨领域技术迁移**：Weighted Box Fusion（目标检测）→ 跨度融合（NLP），是本场最有启发性的做法。
- **后处理是主要收益点**：跨度边界修正、重叠消解、最小长度约束。
- **长文本处理**：滑动窗口 + 重叠 + 结果合并。
- **多模型多样性**：不同长序列模型（DeBERTa/Longformer 等）带来的互补。
- **分类别建模**：7 类论述要素分别处理再整合。

## 5. 可迁移性评估

- **可直接迁移**：
  - **跨领域借用集成技术**（检测 → NLP 的框/跨度融合）——值得作为通用思路记住。
  - 跨度类任务的后处理（边界、最小长度、重叠消解）。
  - 长文本的滑窗 + 重叠合并范式。
- **需要前提**：
  - 长文本模型需要较长上下文与显存预算。
- **不建议照搬**：
  - 直接套用通用分类模型（跨度任务需要专门的头与后处理）。

## 6. 对新手的关键启示

1. **后处理在跨度任务里经常比换模型更值钱**。
2. **跨领域技术迁移**是 Kaggle 的隐藏红利（检测的融合方法用到 NLP）。
3. 长文本任务先解决"切分与合并"，再谈模型。

## 7. 出处

- 讨论区索引：`intel/feedback-prize-2021/topics.md`（120 条）
- 已收录 write-up（8 篇）：
  - 1st（282 票）：https://www.kaggle.com/competitions/feedback-prize-2021/discussion/313177
  - 2nd（203 票）：https://www.kaggle.com/competitions/feedback-prize-2021/discussion/313389
  - 3rd（72 票）：https://www.kaggle.com/competitions/feedback-prize-2021/discussion/313235
  - 4th（149 票）：https://www.kaggle.com/competitions/feedback-prize-2021/discussion/313330
  - 相关赛事方案汇总（69 票）：https://www.kaggle.com/competitions/feedback-prize-2021/discussion/295193
