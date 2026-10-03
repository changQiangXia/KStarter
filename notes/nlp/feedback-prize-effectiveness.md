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

## 7. 轻读结论（2026-10 补）

**一句话**：整篇输入 + 逐 span 池化是正确表示；**前届同题数据的无泄漏伪标**是最大外部杠杆；两级模型与均值校准稳定加分；Efficiency Track 考"大集成蒸馏成单模 + 推理工程"。

- 3 队共识：DeBERTa-large/v3-large 是唯一可靠骨干；essay group model 优于孤立 discourse 分类。
- Span MLM（mask 40–50%、span 3–15、chunk 720）+0.02~0.03；AWP +0.005~0.01；prompts +0.002~0.005。
- 伪标分歧：1st（3 轮）/2nd（最多 5 轮）为核心；3rd 尝试无效——实现差异而非方法问题；"更多教训"作者后悔没亲自充分测试。
- 1st 的 CV-LB 图近线性（图 1）；2nd 指出 StratifiedGroupKFold > GroupKFold。
- Efficiency：单 deberta-v3-large 私 0.557/5m40s（前三水平），预分词+按长度排序再省 40s。

**数字账精选**：1st 二级模型 +0.003~0.005；2nd stacking +0.004；3rd 单模公私 0.563/0.566；2nd 单模私 0.558–0.571。

**悬案**：4th–10th 方案未收录；Token Classification/单模日志/DeBERTa 综述（88/90/91 票）未收录；T5 合成质量与 prompt 泄漏风险未讨论。

## 8. 图表证据

![1st 的 CV vs LB](../../intel/feedback-prize-effectiveness/bodies/347536_img/01.png)

**图 1**（topic 347536）：CV vs LB 近乎严格线性——本场"CV 可信"的直接证据。

![3rd 的 span 架构](../../intel/feedback-prize-effectiveness/bodies/347433_img/01.png)

**图 2**（topic 347433）：特殊 token → Transformer → Bi-LSTM → span Mean Pooling → Multihead Attention → 分类头。

![2nd 的 span 标记示例](../../intel/feedback-prize-effectiveness/bodies/347359_img/01.png)

**图 3**（topic 347359）：正文中 `(Lead start)…(Lead end)` 标记 discourse 的实例。

## 9. 出处

- 讨论区索引：`intel/feedback-prize-effectiveness/topics.md`（80 条）
- 已收录 write-up（6 篇）：
  - 1st（141 票）：https://www.kaggle.com/competitions/feedback-prize-effectiveness/discussion/347536
  - 1st 效率赛道（75 票）：https://www.kaggle.com/competitions/feedback-prize-effectiveness/discussion/347537
  - 2nd（94 票）：https://www.kaggle.com/competitions/feedback-prize-effectiveness/discussion/347359
  - 3rd（77 票）：https://www.kaggle.com/competitions/feedback-prize-effectiveness/discussion/347433
- 轻读全本：`analysis/deep/feedback-prize-effectiveness.md`（Tier B 轻读：对照矩阵/裁决/证据分级/悬案 + 3 图证）
