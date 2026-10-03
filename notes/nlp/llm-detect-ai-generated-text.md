# LLM - Detect AI Generated Text

> 主题：nlp ｜ 子类：— ｜ 领域：教育 ｜ 类别：Featured
> 截止：2024-01-22 ｜ 队伍数：4358 ｜ 机制：代码赛 ｜ 指标：ROC AUC
> 数据来源：`intel/llm-detect-ai-generated-text/`（120 条主题索引 + 8 节正文：1st×2/2nd/3rd/4th/5th/8th/21st + 社区数据帖；22 条 write-up 标记中其余未收录）

## 1. 任务与数据

- **预测目标**：判断一篇学生作文是否由 LLM 生成（二分类），指标 ROC AUC。
- **数据形态**：文本分类。训练集只有少量作文，比赛允许使用外部数据——这直接决定了打法。
- **构造陷阱（本场的核心矛盾）**：
  - **隐藏测试集的生成模型与公开集不同**，导致公开榜（≈0.98）与私榜（≈0.93）严重脱节，发生大规模洗牌。
  - 多支队伍报告"CV 近乎完美但 LB 不稳定"（2nd place 原话），本地验证失去参考价值。
  - 训练数据的**生成方式、主题、改写程度**与测试集分布差异是主要风险源。
- **比赛允许外部数据** → 自建数据（多生成器覆盖）成为方法本体；1st 明言"建模影响较小，多个单模都 0.970+"。
- **公开榜是陷阱**：1st/2nd 私榜 > 公开榜（0.984 vs 0.966）；21st 公开 0.986 但选中提交私榜仅 0.932（最佳 0.957）。

## 2. 验证方案

| 方案 | 使用者 | 说明 |
| --- | --- | --- |
| 多源交叉验证 + 外部数据 | 1st | 承认 CV 不可全信，转而用**数据多样性**对冲分布差异 |
| 分数据集交叉验证 | 4th | 明确记录"很难建立可靠的 CV" |
| 公开榜观察 | 2nd | 初期 CV 完美但 LB 不稳，随后放弃以 CV 为唯一依据 |
| 特征阶梯置信 | 8th | 同一 CV 失效下用"特征+数据量阶梯"（44k→800k）验证方向 |
| rank 融合 | 1st | 公开榜饱和至 ~0.98，概率尺度不可比，改用排名 |

**结论**：当 CV 与 LB 都不可靠时，唯一有效的策略是**最大化泛化面**（数据多样性 + 模型多样性 + 后处理保守）。

## 3. 模型家族

| 方案 | 名次 | 关键点 |
| --- | --- | --- |
| 160k 多源 datamix + 6 范式模型 + rank 融合 | 1st | Mistral LoRA 0.984 私榜；Ghostbuster 0.974；自定义 tokenizer+MLM 0.943；"建模影响较小" |
| SlimPajama 预训练 + 学生作文域适应 | 2nd | 0.916/0.967 → 0.94/0.98 → 集成 0.967/0.983；放弃"CV 完美但不稳"的初始微调 |
| TF-IDF + 12×DeBERTa + 迭代难样本筛选 + 测试伪标签 | 3rd | 11k 精选模型过拟合（0.845 私榜）；1m 续写模型 0.956/0.967；+1k 伪标签私榜 0.893→0.927 |
| "Combined Arms"（TF-IDF+Mistral logprob+Longformer+700k DeBERTa 兜底） | 4th | 拥抱错字并复制随机错字（30%）；权重不按公开榜给 |
| 1.7M 数据 + **测试期域适应**（teacher→短上下文 student） | 5th | 学生 0.977（无 Mamba）；Mamba 拖累私榜；Tricky Crawl 5% 有效 |
| PPL + GLTR 语言学特征 + VotingClassifier | 8th | 800k 后 GLTR 私榜 0.918、+PPL+GPT-2 Large 0.956；10 分钟出提交 |
| "Secret Sauce"：TF-IDF + 多轮测试伪标签 + distilroberta | 21st | 公开 0.986 / **选中私榜 0.932 / 最佳 0.957**——公开榜套利的代价 |

## 4. 关键技巧

- **数据构造即核心方法**：规模/多样性/复杂度；1st 的 4 类来源+7 种增强、5th 的 14 模型生成、3rd 的 35 模型续写。
- **测试期域适应光谱**：teacher→student 蒸馏（5th）> 学生作文 LM 微调（2nd）> 置信伪标签（3rd/1st）> 多轮 top/bottom 伪标签（21st，风险最高）。
- **生成器无关特征**：PPL + GLTR（Top-k rank 桶）抗洗牌；参考 LM 越大越好（8th 阶梯）。
- **错字/混淆的双向使用**：去混淆只修高错误率文本（3rd）；主动注入随机错字（4th 30%）压制伪相关。
- **rank 融合与条件融合**：公开榜饱和时按排名融合（1st）；中间区间交给 TF-IDF（3rd）。
- **Mamba 教训**：公开兼容≠私榜兼容；不确定成员低权重/剔除。

## 5. 深读结论（2026-10 补）

- **当隐藏生成器未知时，"数据多样性 = 唯一正则"**：模型在单一生成器数据上学指纹，在多生成器数据上学边界；1st 的私榜>公开榜、8th 的 CV 0.98→私榜 0.674 是正反两面证据。
- **域适应要用、要被验证**：5th 的测试片蒸馏稳定有效；21st 的多轮伪标签公开暴涨而私榜塌方——**使用测试分布的强度必须与验证能力匹配**。
- **PPL/GLTR 是洗牌中的"正交路线"**：生成器无关的统计特征让 8th 以非微调路线进前 8；其上限随参考 LM 增大而上升。
- **公开榜在可被测试数据放大时会失去参考性**：21st 的 0.986/0.932/0.957 三数字是本场最重要的风险教材；1st/2nd 的"私榜>公开"则说明泛化路线在公开榜上被低估。
- **选择即分数**：5th 未提交最佳（5th vs 可到第 3）；21st 选错提交——本场两次名次级损失都来自"提交选择"而非模型。

## 6. 图表证据

**图 1：PPL 分布——AI 低而集中、人写高而分散**（8th，topic 470224）——`../../intel/llm-detect-ai-generated-text/bodies/470224_img/01.png`

![ppl](../../intel/llm-detect-ai-generated-text/bodies/470224_img/01.png)

*读图*：text_ppl 左图 AI（橙）峰值 ~10、人写（蓝）~25–30 且长尾；句级 PPL 同样分离——生成器无关统计信号的第一手证据。

## 7. 可迁移性评估

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

## 8. 对新手的关键启示

1. **先问"这个比赛比的是什么"**：本场比的是数据构造能力，不是模型技巧。识别这一点比调参重要得多。
2. **CV 失效时要换策略**，不是更用力地调参；用多样性和保守选择对冲不确定性。
3. **简单的非神经网络方法在泛化场景下仍有价值**（8th place 的 PPL/GLTR）。
4. **外部数据的质量与配比比数量更重要**（5th place 的 Pile 占比结论）。

## 9. 出处

- 讨论区索引：`intel/llm-detect-ai-generated-text/topics.md`（120 条）
- 已收录正文（8 节）：
  - 1st 短版（Raja Biswas，203 票）：https://www.kaggle.com/competitions/llm-detect-ai-generated-text/discussion/470121
  - 2nd（Guanshuo Xu，115 票）：https://www.kaggle.com/competitions/llm-detect-ai-generated-text/discussion/470395
  - 1st 完整版（Nicholas Broad 等，99 票）：https://www.kaggle.com/competitions/llm-detect-ai-generated-text/discussion/473295
  - 21st（Ali，87 票）：https://www.kaggle.com/competitions/llm-detect-ai-generated-text/discussion/470148
  - 5th（James Day，84 票）：https://www.kaggle.com/competitions/llm-detect-ai-generated-text/discussion/470093
  - 8th（Abdullah Meda，68 票）：https://www.kaggle.com/competitions/llm-detect-ai-generated-text/discussion/470224
  - 3rd（Yevhenii Maslov，67 票）：https://www.kaggle.com/competitions/llm-detect-ai-generated-text/discussion/470333
  - 4th（Ertuğrul Demir，66 票）：https://www.kaggle.com/competitions/llm-detect-ai-generated-text/discussion/470179
- 社区数据帖：https://www.kaggle.com/competitions/llm-detect-ai-generated-text/discussion/452155（Radek 的 500 篇生成作文）
- 未收录缺口（登记备查）：22 条 write-up 标记中的其余条目
- 深读全文：`analysis/deep/llm-detect-ai-generated-text.md`
