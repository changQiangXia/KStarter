# MAP - Charting Student Math Misunderstandings

> 主题：nlp ｜ 子类：— ｜ 领域：教育 ｜ 类别：Featured
> 截止：2024-08-XX ｜ 队伍数：1500+ ｜ 机制：代码赛 ｜ 指标：多分类（误解类型）
> 数据来源：`intel/map-charting-student-math-misunderstandings/`（80 条主题索引 + 6 篇 write-up 正文）

## 1. 任务与数据

- 预测目标：给定数学题（含图示描述）、选项、学生所选答案与学生解释，判断其**误解类型**（多分类）。
- 数据形态：文本为主的多字段结构化输入；类别不均衡。
- 构造陷阱：
  - 标签含 **True/False 不一致**（需自动修正）。
  - 存在**近重复样本**，若随机分折会泄漏。
  - 长尾类别导致训练不稳。

## 2. 验证方案

| 方案 | 使用者 | 说明 |
| --- | --- | --- |
| 近重复样本同折 | 10th | 数据卫生的一部分：near-duplicates 必须放在同一折 |
| 自动修正标签不一致 | 10th | 修复 True/False 冲突后再训练 |
| 5 折 × 多骨干 | 10th | 15 个 QLoRA 模型集成 |

## 3. 方案谱系

| 方案 | 名次 | 关键点 |
| --- | --- | --- |
| LLM 提示工程 + 双人方案融合 | 3rd（公开第 1） | 把提示结构从 `{题目/答案/对错/解释}` 改为 `{题目/选项/所选/解释}`——**结构化字段的选择直接影响 LLM 判断质量** |
| 直接多分类 + 15 个 QLoRA 模型集成 | 10th | 3 骨干（Qwen3-Reranker-8B、Qwen3-Embedding-8B、Qwen2.5-32B-Instruct）× 5 折；Focal + CE 混合损失 + 类别权重 warmup（约 33%）；LoRA 合并后 GPTQ-4bit 量化加速推理 |
| 单模型方案 | 22nd | 一个模型也能进前 2% |

## 4. 关键技巧

- **提示结构设计**：把"答案对错"替换为"选项 + 所选"，让模型显式对比——这是 3rd 的核心改动。
- **数据卫生**：标签一致性修正 + 近重复同折。
- **长尾类别处理**：Focal + CE 混合损失与类别权重 warmup。
- **推理成本工程**：LoRA 合并 + GPTQ 4bit 量化，是在时限内跑多模型集成的前提。
- **集成规模**：15 个微调模型的集成为小数据集提供稳定性。

## 5. 可迁移性评估

- **可直接迁移**：
  - **多字段输入的提示结构设计**（用"选项 vs 所选"替代"对错"）是 LLM 分类任务的通用优化点。
  - 近重复样本必须同折。
  - Focal+CE 混合损失处理长尾。
  - 量化 + LoRA 合并控制推理成本。
- 需要前提：QLoRA 微调与量化工具链；多模型推理资源。
- 不建议照搬：直接用默认提示结构（本场证明结构调整即有效）。

## 6. 对新手的关键启示

1. **提示工程在 LLM 分类里是真实收益来源**（改一个字段就提分）。
2. **数据卫生（标签冲突、近重复）先做再训**。
3. **推理成本要提前规划**，否则跑不完集成。

## 7. 出处

- 讨论区索引：`intel/map-charting-student-math-misunderstandings/topics.md`（80 条）
- 已收录 write-up（6 篇）：
  - 1st（191 票）：https://www.kaggle.com/competitions/map-charting-student-math-misunderstandings/discussion/612268
  - 3rd 公开第 1（78 票）：https://www.kaggle.com/competitions/map-charting-student-math-misunderstandings/discussion/612059
  - 18th（81 票）：https://www.kaggle.com/competitions/map-charting-student-math-misunderstandings/discussion/612096
  - 22nd 单模型（68 票）：https://www.kaggle.com/competitions/map-charting-student-math-misunderstandings/discussion/611985
