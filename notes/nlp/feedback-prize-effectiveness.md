# Feedback Prize - Predicting Effective Arguments

> 主题：nlp ｜ 子类：— ｜ 领域：教育 ｜ 类别：Featured
> 截止：2022-07-XX ｜ 队伍数：1500+ ｜ 机制：代码赛 ｜ 指标：对数损失（三档有效性分类）
> 数据来源：`intel/feedback-prize-effectiveness/`（80 条主题索引 + 6 篇 write-up 正文）

## 1. 任务与数据

- 预测目标：在学生议论文中，对已标注的论述要素（论点/证据/结论等）判断其**有效性等级**（无效 / 合格 / 有效）。
- 数据形态：文章 + 跨度标注 + 三档标签；类别不均衡（"合格"居多）。
- 构造陷阱：**跨度级分类**（需要同时利用跨度内容与上下文）；标签主观性带来噪声。

## 2. 验证方案

| 方案 | 使用者 | 说明 |
| --- | --- | --- |
| 分组 K 折（按文章） | 多队 | 避免同文章的跨度跨折 |
| 对数损失导向的概率校准 | 1st | 三档概率预测，校准影响分数 |
| 效率与精度双轨 | 3rd / 1st | 本场设有**效率赛道（Efficiency Track）** |

## 3. 方案谱系

| 方案 | 名次 | 关键点 |
| --- | --- | --- |
| Team Hydrogen 方案 | 1st | 同时拿下正赛与效率赛道第一 |
| 跨度分类 + 集成 | 2nd | 代码与 notebook 公开；含效率优化版推理 |
| **Span MLM + T5 数据增强** | 3rd | 对跨度做掩码语言模型预训练，再用 T5 生成增强样本 |

## 4. 关键技巧

- **跨度级预训练（Span MLM）**：在目标任务的跨度上做 MLM，比通用预训练更贴近任务。
- **生成式数据增强（T5）**：用 T5 改写/生成样本扩充训练集。
- **三档概率的对数损失**：需要输出校准的概率而非硬标签。
- **效率意识**：本场设效率赛道，推理时间本身被计分。

## 5. 可迁移性评估

- **可直接迁移**：
  - **Span MLM**：在任务相关片段上做掩码预训练，是低资源 NER/跨度分类的有效手段。
  - 生成式增强（T5/LLM 改写）。
  - 对数损失任务要校准概率。
- 需要前提：跨度标注数据；生成模型用于增强。
- 不建议照搬：无。

## 6. 对新手的关键启示

1. **跨度级任务可以用"片段预训练"补数据不足**。
2. **生成式增强要控制质量**（改写需与标签语义一致）。
3. **效率也是分数**（本场专设效率赛道，值得注意这类赛制设计）。

## 7. 出处

- 讨论区索引：`intel/feedback-prize-effectiveness/topics.md`（80 条）
- 已收录 write-up（6 篇）：
  - 1st（141 票）：https://www.kaggle.com/competitions/feedback-prize-effectiveness/discussion/347536
  - 1st 效率赛道（75 票）：https://www.kaggle.com/competitions/feedback-prize-effectiveness/discussion/347537
  - 2nd（94 票）：https://www.kaggle.com/competitions/feedback-prize-effectiveness/discussion/347359
  - 3rd（77 票）：https://www.kaggle.com/competitions/feedback-prize-effectiveness/discussion/347433
