# MAP - Charting Student Math Misunderstandings

> 主题：nlp ｜ 子类：— ｜ 领域：教育 ｜ 类别：Featured
> 截止：2024-08-XX ｜ 队伍数：1500+ ｜ 机制：代码赛 ｜ 指标：多分类（误解类型）
> 数据来源：`intel/map-charting-student-math-misunderstandings/`（80 条主题索引 + 6 节正文：1st/3rd/6th/10th/18th + 题目结构帖；2nd/4th/5th/8th 等 16 条未收录）

## 1. 任务与数据

- 预测目标：给定数学题（含图示描述）、选项、学生所选答案与学生解释，判断其**误解类型**（多分类）。
- 数据形态：文本为主的多字段结构化输入；类别不均衡。
- 构造陷阱：
  - 标签含 **True/False 不一致**（需自动修正）。
  - 存在**近重复样本**，若随机分折会泄漏。
  - 长尾类别导致训练不稳。
- **标签结构**：65 类 = True/False × {Correct/Neither/Misconception} × 37 种误解；**仅 15 道题，每题只可能有 2–5 种误解**（可降解为"每题 k 选 1"）。
- **数据质量**：Q31778 有 12 行错误标签（MC_Answer=9 而正确为 6）；主噪声来自 "Neither"。

## 2. 验证方案

| 方案 | 使用者 | 说明 |
| --- | --- | --- |
| 近重复样本同折 | 10th | 数据卫生的一部分：near-duplicates 必须放在同一折 |
| 自动修正标签不一致 | 10th | 修复 True/False 冲突后再训练 |
| 5 折 × 多骨干 | 10th | 15 个 QLoRA 模型集成 |
| **多种子合成验证** | 1st | 5 折×5 种子；单种子不可信；3 种子稳定；"信 loss 不信 MAP@3" |
| is_correct 规则字段 | Chris（98 票帖） | 15 题固定 → 正确答案可规则计算，不许模型猜 |

## 3. 方案谱系

| 方案 | 名次 | 关键点 |
| --- | --- | --- |
| **后缀分类**（每题 8–12 候选选 1）+ FlexAttention 前缀共享 | 1st | offload_adam 单卡 32B 全参；5 折×5 种子；W8A8 INT8 + 逐层 offload（65min/16k） |
| 提示结构（Choices/Selected +0.001）+ R-Drop + 多阶段推理 | 3rd monsaraida | Qwen3-14B；多任务（65+2+3+36 类）；fp16+no-padding 4× 提速 |
| CausalLM 每题候选 + 置信级联（72B 190→60min） | 3rd Masaya | 标签限制 +0.002~0.003 且快 3×；其他选项 +0.003~0.004 |
| 直接 65 类 + 15 个 QLoRA 模型（3 骨干×5 折） | 10th | Focal+CE + 权重 warmup 0.33；GPTQ-4bit + FP16 头 + vLLM；logit 加权融合 0.951/0.948 |
| 37 类 + 去重/伪标签重复/合成稀类 + Qwen-semble | 6th | 7 模型 0.951/0.947；个体差的增强模型贡献显著 |
| 金字塔集成（按不确定度四级重推，权重 1/2/4/8） | 18th Chris | 3 个月 1000+ 模型；分类/生成/多选/多头四范式全试；0.952/0.947 |

## 4. 关键技巧

- **标签空间工程**：利用"每题候选集"把 65 类降解为 k 选 1（+0.002~0.003、快 3×）；1st 的后缀分类把输出空间与标签空间完全对齐。
- **提示对比结构**：{Choices+Selected}（+0.001~0.004）、候选误解 hint（+0.0003）、规则字段 is_correct 不学。
- **数据卫生**：去重、near-dup 同折、自动修正 True/False、伪标签重复样本、补稀类合成。
- **多种子验证纪律**：噪声标签下单种子不可信；3 种子起步；loss 比 MAP@3 稳。
- **推理预算编排**：置信级联/金字塔（大模型只跑最不确定的 6–50%）、W8A8/GPTQ 量化、逐层 offload、fp16+no-padding。
- **跨范式集成**：序列分类/CausalLM/多选/多头互补；选成员看互补性而非单体分。

## 5. 深读结论（2026-10 补）

- **这是"标签空间工程 + 推理预算编排"的比赛**：模型是公共品；结构读数（每题候选集、对错可规则计算）与算力分配（级联/金字塔/量化）决定名次。
- **最大单步是输出空间降维**：65 类 → 每题 2–6 候选 → 后缀分类；三家独立验证（3rd、1st、18th 的多选范式）。
- **提示的对比结构值 0.001~0.004**：Choices/Selected 让"误解类型"成为可比较的相对判断；is_correct 直接规则化。
- **噪声标签 → 验证工程**：单种子 CV 抖动大于模型差异；1st 用 5 折×5 种子 + "信 loss"，18th 用 3 个月 1000+ 模型，10th/6th 用多骨干集成。
- **推理工程直接换集成规模**：fp16/padding 4×、W8A8 2×、级联把 72B 从 190min 压到 60min；1st 因 /tmp 存储事故只交 4/6 模型——工程事故即失分。

## 6. 图表证据

**图 1：18th 金字塔集成（标签空间×范式×算力分配）**（Chris Deotte，topic 612096）——`../../intel/map-charting-student-math-misunderstandings/bodies/612096_img/01.png`

![pyramid](../../intel/map-charting-student-math-misunderstandings/bodies/612096_img/01.png)

*读图*：100%（权重 1.0，4B–14B）→ 50%（权重 2.0，27B–32B）→ 10%（权重 4.0）→ 6%（权重 8.0，72B）→ 提交；红=序列分类、绿=文本生成、蓝=多选。

**图 2/3：3rd 两方案总览（SVG）**（topic 612059）——`../../intel/map-charting-student-math-misunderstandings/bodies/612059_img/01.svg`、`.../02.svg`

![3rd overview](../../intel/map-charting-student-math-misunderstandings/bodies/612059_img/01.svg)
![Masaya overview](../../intel/map-charting-student-math-misunderstandings/bodies/612059_img/02.svg)

*说明*：SVG 为纯矢量路径；细节以正文为准（monsaraida：Qwen3-14B LoRA 多任务 + R-Drop + 多阶段推理；Masaya：CausalLM 每题候选 + 14B/32B→72B 级联）。

## 7. 可迁移性评估

- **可直接迁移**：
  - **多字段输入的提示结构设计**（用"选项 vs 所选"替代"对错"）是 LLM 分类任务的通用优化点。
  - 近重复样本必须同折。
  - Focal+CE 混合损失处理长尾。
  - 量化 + LoRA 合并控制推理成本。
- 需要前提：QLoRA 微调与量化工具链；多模型推理资源。
- 不建议照搬：直接用默认提示结构（本场证明结构调整即有效）。

## 8. 对新手的关键启示

1. **提示工程在 LLM 分类里是真实收益来源**（改一个字段就提分）。
2. **数据卫生（标签冲突、近重复）先做再训**。
3. **推理成本要提前规划**，否则跑不完集成。

## 9. 出处

- 讨论区索引：`intel/map-charting-student-math-misunderstandings/topics.md`（80 条）
- 已收录正文（6 节）：
  - 1st（tascj，191 票）：https://www.kaggle.com/competitions/map-charting-student-math-misunderstandings/discussion/612268
  - 题目结构/is_correct（Chris Deotte，98 票）：https://www.kaggle.com/competitions/map-charting-student-math-misunderstandings/discussion/589400
  - 18th 金字塔（Chris Deotte，81 票）：https://www.kaggle.com/competitions/map-charting-student-math-misunderstandings/discussion/612096
  - 3rd/公开第 1（monsaraida & Masaya，78 票）：https://www.kaggle.com/competitions/map-charting-student-math-misunderstandings/discussion/612059
  - 10th（64 票）：https://www.kaggle.com/competitions/map-charting-student-math-misunderstandings/discussion/612038
  - 6th Qwen-semble（Manan Jhaveri，44 票）：https://www.kaggle.com/competitions/map-charting-student-math-misunderstandings/discussion/612099
- 未收录缺口（登记备查）：2nd/4th/5th/8th 等 16 条 write-up
- 深读全文：`analysis/deep/map-charting-student-math-misunderstandings.md`
