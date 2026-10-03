# LLM - Detect AI Generated Text

> 主题：nlp ｜ 子类：— ｜ 领域：教育 ｜ 类别：Featured
> 截止：2024-01-22 ｜ 队伍数：4358 ｜ 机制：代码赛 ｜ 指标：ROC AUC
> 数据来源：`intel/llm-detect-ai-generated-text/`（120 条主题索引 + 8 篇 write-up 正文）

## 1. 任务与数据

- **预测目标**：判断一篇学生作文是否由 LLM 生成（二分类），指标 ROC AUC。
- **数据形态**：文本分类。训练集只有少量作文，比赛允许使用外部数据——这直接决定了打法。
- **构造陷阱（本场的核心矛盾）**：
  - **隐藏测试集的生成模型与公开集不同**，导致公开榜（≈0.98）与私榜（≈0.93）严重脱节，发生大规模洗牌。
  - 多支队伍报告"CV 近乎完美但 LB 不稳定"（2nd place 原话），本地验证失去参考价值。
  - 训练数据的**生成方式、主题、改写程度**与测试集分布差异是主要风险源。

## 2. 验证方案

| 方案 | 使用者 | 说明 |
| --- | --- | --- |
| 多源交叉验证 + 外部数据 | 1st | 承认 CV 不可全信，转而用**数据多样性**对冲分布差异 |
| 分数据集交叉验证 | 4th | 明确记录"很难建立可靠的 CV" |
| 公开榜观察 | 2nd | 初期 CV 完美但 LB 不稳，随后放弃以 CV 为唯一依据 |

**结论**：当 CV 与 LB 都不可靠时，唯一有效的策略是**最大化泛化面**（数据多样性 + 模型多样性 + 后处理保守）。

## 3. 模型家族

| 方案 | 名次 | 关键点 |
| --- | --- | --- |
| DeBERTa + 自建超大数据混合集 | 1st | 自评"**建模方法不是关键**，数据集质量才是"；多个单模型都能到 0.970+ |
| 自建数据 + 集成 | 2nd | 后期转向自建数据；强调初期 CV 完美的模型在 LB 上失效 |
| TF-IDF 管线 + 12 个 DeBERTa 加权平均 | 3rd | 传统特征 + 深度模型混合；用去混淆（deobfuscator）预处理；分层样本选择 |
| 多路组合方案（"combined arms"） | 4th | 承认 CV 不可靠，靠多方案互补 |
| DeBERTa-v3-large + Mamba-790m，1.7M 训练样本 | 5th | 数据混合：PERSUADE / Pile / SlimPajama / Tricky Crawl；最佳模型 62–99% 用 Pile 数据；做领域自适应 |
| 语言学特征（困惑度 PPL + GLTR） | 8th | **非神经网络方案**，泛化性反而好，是洗牌后的赢家之一 |
| 数据选择 + 合并策略（"secret sauce"） | 21st | 用 Mistral-7B、Gemini Pro 自造数据 |

## 4. 关键技巧

- **数据构造即核心方法**：围绕"规模、多样性、复杂度"生成/收集文本；冠军团队把大部分预算投在数据混合上。
- **困惑度与 GLTR 等语言学特征**：无需微调大模型，成本低、泛化好。
- **去混淆预处理**：修复被混淆（同形字替换等）的文本，只对错误较多的样本做修正（3rd）。
- **多源数据混合**：开源语料补全（Pile、SlimPajama）+ 竞赛数据 + 自造 LLM 文本，按比例调优。
- **模型多样性对冲**：TF-IDF + Transformer 加权平均、DeBERTa + Mamba 混合。

## 5. 可迁移性评估

- **可直接迁移**：
  - **当 CV 无法反映 LB 时，把预算从"调模型"转向"扩数据多样性"**——这是本场最重要的一课。
  - 传统特征（TF-IDF、统计/语言学特征）与深度模型混合，是低成本高泛化的常规操作。
  - 用困惑度类指标做特征，在文本真假判别任务上通用。
- **需要前提**：
  - 自造数据依赖可用的开源 LLM 与生成成本；比赛规则必须允许外部数据。
  - Mamba 一类新架构需要相应训练框架与算力。
- **不建议照搬**：
  - 依赖公开榜选择提交：本场公开榜与私榜差距过大。
  - 只在小规模共享数据上微调（2nd place 的初期教训）。

## 6. 对新手的关键启示

1. **先问"这个比赛比的是什么"**：本场比的是数据构造能力，不是模型技巧。识别这一点比调参重要得多。
2. **CV 失效时要换策略**，不是更用力地调参；用多样性和保守选择对冲不确定性。
3. **简单的非神经网络方法在泛化场景下仍有价值**（8th place 的 PPL/GLTR）。
4. **外部数据的质量与配比比数量更重要**（5th place 的 Pile 占比结论）。

## 7. 出处

- 讨论区索引：`intel/llm-detect-ai-generated-text/topics.md`（120 条）
- 已收录 write-up（8 篇）：
  - 1st（203 票）：https://www.kaggle.com/competitions/llm-detect-ai-generated-text/discussion/470121
  - 1st 详细版（99 票）：https://www.kaggle.com/competitions/llm-detect-ai-generated-text/discussion/473295
  - 2nd（115 票）：https://www.kaggle.com/competitions/llm-detect-ai-generated-text/discussion/470395
  - 3rd（67 票）：https://www.kaggle.com/competitions/llm-detect-ai-generated-text/discussion/470333
  - 4th（66 票）：https://www.kaggle.com/competitions/llm-detect-ai-generated-text/discussion/470179
  - 5th（84 票）：https://www.kaggle.com/competitions/llm-detect-ai-generated-text/discussion/470093
  - 8th（68 票）：https://www.kaggle.com/competitions/llm-detect-ai-generated-text/discussion/470224
  - 21st（87 票）：https://www.kaggle.com/competitions/llm-detect-ai-generated-text/discussion/470148
