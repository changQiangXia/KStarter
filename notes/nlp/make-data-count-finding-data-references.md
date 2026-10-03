# Make Data Count - Finding Data References

> 主题：nlp ｜ 子类：document-ai ｜ 领域：科研元数据 ｜ 类别：Research
> 截止：2025-09-09 ｜ 队伍数：1282 ｜ 机制：代码赛 ｜ 指标：数据集引用检测 + 类型分类
> 数据来源：`intel/make-data-count-finding-data-references/`（80 条主题索引 + 6 篇 write-up 正文）

## 1. 任务与数据

- 预测目标：在科研论文中**检测数据集的提及**（两种形式：DOI 链接与 accession ID），并判断其类型（Primary / Secondary）。
- 数据形态：学术全文 + 实体标注（数据集引用）。
- 构造陷阱：
  - **两种引用形式差异大**（DOI 是 URL 模式，accession ID 是各数据库的编号规则）；
  - 长文档 + 实体稀疏；
  - 类型分类需要上下文语义（该数据集是本文产生还是复用）。

## 2. 方案特征

| 类型 | 说明 |
| --- | --- |
| 两阶段方案 | 先做**引用检测**（是否提及数据集），再做**类型分类**（Primary/Secondary） |
| 规则 + 模型结合 | DOI/accession 的模式规整，可用正则先召回，再由模型判定与消歧 |

## 3. 关键技巧

- **任务分解**：检测与分类分开（各自的特征与阈值不同）。
- **规则召回 + 模型判定**（结构化模式用规则，语义判断用模型）。
- **长文档切分与实体边界**处理。

## 4. 可迁移性评估

- **可直接迁移**：
  - 实体抽取任务的"检测 → 分类"两阶段；
  - 规则（模式匹配）与模型的分工；
  - 长文档中的稀疏实体处理。
- 需要前提：文档解析与 NER 技术栈。
- 不建议照搬：端到端一把抓（两类引用的特征差异太大）。

## 5. 对新手的关键启示

1. **同一"实体"的多种形式要分别处理**（DOI vs accession ID）。
2. **规则与模型不是对立的**：结构化部分交规则，语义部分交模型。
3. 与 PII Detection、AI4Code 对照：**文档实体类任务的标准套路 = 分解 + 规则兜底**。

## 6. 出处

- 讨论区索引：`intel/make-data-count-finding-data-references/topics.md`（80 条）
- 已收录 write-up（6 篇）：
  - 1st（61 票）：https://www.kaggle.com/competitions/make-data-count-finding-data-references/discussion/606853
  - 2nd（29 票）：https://www.kaggle.com/competitions/make-data-count-finding-data-references/discussion/606786
  - 5th（46 票）：https://www.kaggle.com/competitions/make-data-count-finding-data-references/discussion/606769
