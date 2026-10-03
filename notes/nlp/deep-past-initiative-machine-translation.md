# Deep Past Initiative - Machine Translation

> 主题：nlp ｜ 子类：— ｜ 领域：人文/历史 ｜ 类别：Featured
> 截止：2026-03-23 ｜ 队伍数：2674 ｜ 机制：代码赛 ｜ 指标：BLEU / chrF++
> 数据来源：`intel/deep-past-initiative-machine-translation/`（120 条主题索引 + 8 篇 write-up 正文）

## 1. 任务与数据

- **任务形式**：把古亚述楔形文字的转写（transliteration）翻译成英文——**极低资源机器翻译**。
- **数据形态**：约 6500 篇有完整英译的文档（**但无句级对齐**）、13456 篇已发表但多未翻译的文本、约 1700 篇的句片段元数据，以及主办方提供的大量学术 PDF。
- **构造陷阱**：
  - **缺少句级对齐**是最大障碍（训练需要句对）。
  - 学术 PDF 质量参差：有纯图像型（需 OCR）、文本型、以及"破碎文本"型（6th 明确分类）。
  - 比赛早期存在数据问题，主办方修复后才稳定（1st 明确致谢）。

## 2. 验证方案

| 方案 | 使用者 | 说明 |
| --- | --- | --- |
| 与官方指标一致的句级验证 | 1st / 2nd | BLEU/chrF++ 在句子层面评估，需与官方口径一致 |
| 数据版本对照 | 多队 | 用"数据清洗前后的模型对比"来量化数据质量收益 |

## 3. 方案谱系

| 方案 | 名次 | 关键点 |
| --- | --- | --- |
| **数据质量决定一切** | 1st | 核心投入全在数据；标题即结论 |
| 纯数据驱动的 Akkadian NMT（**模型是原版 ByT5-large，零结构改动**） | 2nd | 三段式 LLM 流水线做句级对齐；人工搜集并 OCR 约 60 篇未被官方数据覆盖的学术出版物；统一多变的正字法 |
| 合成数据教授 OA 基础 | 3rd | 用合成数据注入领域基础能力 |
| 15 模型集成 + 多源数据 | 6th | 把 PDF 分成图像 / 文本 / 破碎三类分别处理；数据、训练、推理三线并进 |
| 两阶段微调 + 高质量数据抽取 | 8th | 先领域适配再任务微调 |
| Seq2Seq + 继续预训练 + 伪标签 | 10th | 利用未翻译文本做半监督 |

## 4. 关键技巧

- **LLM 辅助句级对齐**：用大模型把"文档级翻译"切成句对，是本题最关键的数据工程。
- **学术 PDF 挖掘 + OCR + 正字法归一**：把分散在文献里的平行语料变成训练数据。
- **半监督**：对未翻译文本做伪标签/继续预训练。
- **模型反而次要**：2nd place 用原版 ByT5-large 拿到第二名。

## 5. 可迁移性评估

- **可直接迁移**：
  - **低资源任务的第一投入是语料工程**：对齐、抽取、清洗、归一化。
  - 用 LLM 做自动对齐/数据合成，再人工抽检。
  - 训练/验证指标必须与官方口径完全一致。
- **需要前提**：
  - 需要领域知识（正字法、文献来源）或能借助 LLM 获取。
  - OCR/PDF 抽取工具链。
- **不建议照搬**：
  - 直接上大模型架构改动——本场冠军与亚军都证明架构不是瓶颈。

## 6. 对新手的关键启示

1. **当数据是瓶颈时，模型的选择几乎不重要**——这句话在本场由 1st 和 2nd 双重验证。
2. **句级对齐是最常见的数据瓶颈**，LLM 是当前最有效的工具。
3. **领域规范化（正字法统一）**看似枯燥，但对低资源任务是决定性的。
4. 代码赛要注意：隐藏重跑环境下，**数据流水线必须可复现且不依赖网络**。

## 7. 出处

- 讨论区索引：`intel/deep-past-initiative-machine-translation/topics.md`（120 条）
- 已收录 write-up（8 篇）：
  - 1st（94 票）"Data Quality Dictates Everything"：https://www.kaggle.com/competitions/deep-past-initiative-machine-translation/discussion/684353
  - 2nd（42 票）：https://www.kaggle.com/competitions/deep-past-initiative-machine-translation/discussion/684345
  - 3rd（51 票）：https://www.kaggle.com/competitions/deep-past-initiative-machine-translation/discussion/684425
  - 6th（54 票）：https://www.kaggle.com/competitions/deep-past-initiative-machine-translation/discussion/684231
  - 7th（33 票）：https://www.kaggle.com/competitions/deep-past-initiative-machine-translation/discussion/684215
  - 8th（25 票）：https://www.kaggle.com/competitions/deep-past-initiative-machine-translation/discussion/684329
