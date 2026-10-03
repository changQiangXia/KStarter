# Kaggle - LLM Science Exam

> 主题：nlp ｜ 子类：— ｜ 领域：科学问答 ｜ 类别：Featured
> 截止：2023-10-10 ｜ 队伍数：2664 ｜ 机制：代码赛 ｜ 指标：MAP@3（多选题）
> 数据来源：`intel/kaggle-llm-science-exam/`（120 条主题索引 + 8 篇 write-up 正文）

## 1. 任务与数据

- **任务形式**：科学多选题问答。题目由 LLM 生成、经人工筛选，**闭卷答题**不现实，必须外接知识。
- **资源约束**：Kaggle Notebook 环境（本场为 2×T4 GPU），有推理时限——**检索速度也是竞争力**。
- **数据形态**：题目 + 5 个选项；外部知识来自 Wikipedia 大规模语料。

## 2. 验证方案

| 方案 | 使用者 | 说明 |
| --- | --- | --- |
| 用公开题集做留出验证 | 1st | 与官方 MAP@3 口径一致 |
| 自建 Wikipedia 解析语料的抽样验证 | 5th | 检索质量单独评估 |
| 多 RAG 管线消融 | Top-100 | 对比"增加检索管线"与"增加模型"的收益差异 |

## 3. 方案谱系

| 方案 | 名次 | 关键点 |
| --- | --- | --- |
| 以检索为核心，模型几乎不变 | 1st | 明确记录：**检索部分的改进贡献了绝大部分提升**，建模部分基本没动 |
| Llama 2 70B + BM25 稀疏检索 + 稠密检索 | 5th | 自建 Wikipedia 解析语料；稀疏（pyserini/Lucene）与稠密检索结合 |
| 多 RAG 管线 + DeBERTa 集成 | 3rd | RAG 管线集成 |
| TF-IDF RAG（RAPIDS 加速）+ 集成 | Top 100 | 关键发现：**每增加一条 RAG 管线带来的提升，大于再增加一个 DeBERTa** |
| 60k 自建数据集 | 社区帖 | 蒸馏/训练数据构造同样重要 |

## 4. 关键技巧

- **检索质量决定上限**：冠军的结论是"把时间花在更好的上下文检索上"，而不是换更大的模型。
- **稀疏 + 稠密混合检索**：BM25 与向量检索互补。
- **多 RAG 管线集成**：不同切分/索引/检索器产生的上下文差异，比多模型集成更有效。
- **自建语料**：自己解析 Wikipedia（而非依赖现成索引）是可控且高收益的工程。
- **工程加速**：RAPIDS/TF-IDF 等加速手段直接换来更多集成空间（与 AIMO 的结论一致）。

## 5. 可迁移性评估

- **可直接迁移**：
  - **RAG 任务中，检索侧的投入回报高于模型侧**——这是本场最通用的结论。
  - 稀疏 + 稠密混合检索的常规组合。
  - "多检索管线集成"优于"多模型集成"。
  - 在限时环境中，加速工具直接换算成集成规模。
- **需要前提**：
  - 需要 GPU 与可离线运行的检索库（代码赛无网络）。
  - 大模型的显存/时间预算。
- **不建议照搬**：
  - 只调模型不调检索（本场的性能天花板主要来自检索）。

## 6. 对新手的关键启示

1. **RAG 类比赛先优化检索**：检索不到位，再强的模型也答不对。
2. **集成检索管线比集成模型更划算**（本场有明确对照）。
3. **自己构建语料/索引**是可控且高回报的工程投入。
4. **代码赛的离线约束**（无网络、限时、显存有限）会直接决定技术选型。

## 7. 出处

- 讨论区索引：`intel/kaggle-llm-science-exam/topics.md`（120 条）
- 已收录 write-up（8 篇）：
  - 1st 摘要（239 票）：https://www.kaggle.com/competitions/kaggle-llm-science-exam/discussion/446240
  - 1st 详细版（219 票）：https://www.kaggle.com/competitions/kaggle-llm-science-exam/discussion/446422
  - 3rd（84 票）：https://www.kaggle.com/competitions/kaggle-llm-science-exam/discussion/446358
  - 5th（81 票）：https://www.kaggle.com/competitions/kaggle-llm-science-exam/discussion/446293
  - Top 100 RAG 加速（73 票）：https://www.kaggle.com/competitions/kaggle-llm-science-exam/discussion/446318
