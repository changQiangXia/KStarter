# Deep Past 阿卡德语翻译深读：数据质量决定一切

> 赛事：Featured ｜ 主题 nlp（低资源机器翻译）｜ 2674 队 ｜ 代码赛 ｜ 指标：DPI BLEU / chrF++（越高越好）
> 材料基础：`digests/deep-past-initiative-machine-translation.md`（8 篇：1st 94 票/编译讨论 93/6th 54/2nd 42/7th 33/8th 25/10th 21/15th 16；120 条讨论索引）+ 23 张图
> 深读时间：2026-10（Tier A #44）

## 0. 一句话重述：这道题真正在考什么

题面是"把古亚述楔形文字的阿卡德语转写翻译成英文"，实际被考的是**语料工程**——模型几乎原封不动：

1. **官方数据是"文档级、无句对齐"的**：train.csv ~6,500 份文档只有整篇译文；published_texts ~13k 多数未翻译；S_meta 片段又常有错位。**句级对齐是第一个瓶颈**——1st/2nd/15th 都用 LLM 流水线重建句对（Breaker/Fixer/Generator 三段式）。
2. **学术 PDF 是最大增量**：2nd 从约 60 本 Old Assyrian 出版物 OCR 出 **60,654 句对/149 个来源**（TR 27k/EN 21.7k/FR 6.4k/DE 5.4k，非英语统一译为英语）；1st 用 GLM-OCR 布局 + Gemini-3.0-pro 分三版迭代重建 data1/2/3（并对 CV 硬样本、长度失配样本重抽 740/131 份文档）。
3. **正字法归一化 + 去重**：sz→š、下标 2/3→重音、ḫ→h/H、限定符 `(d)→{d}`；prefer-EN 去重避免同一泥板多语言译文冲突；多版本提取作为自然增强。
4. **模型是原版 ByT5**：byte-level 对罕见字符/变音符号最鲁棒（8th：NLLB/mT5 差 1–1.5 GM；7th：byt5 完胜 LLM 微调）；base→large→xl 单调涨分（数据足够干净时）。
5. **训练/推理工程**：两阶段 SFT（大量噪声数据→小量高质量数据 1 epoch）、CPT→SFT、伪标签（Gemma 教师/KD）、MBR 解码（beam+采样候选 + 多指标一致性选择）、ct2 int8 量化压进 9 小时；**用 eval_loss 而非 eval_bleu/chrf 选 checkpoint**（后者持续上涨是过拟合）。
6. **公私榜差异大**：1st 最佳提交 41.5/43.2 却被"更稳"的 41.6/42.8 取代；2nd 的公榜峰值 42.4 对应私榜 40.4。**提交选择本身是一个决策问题**。

一句话：**这是一场"数据质量决定一切"的比赛**——2nd 说"模型的每一个改进点都来自更大、更干净的语料"；15th 说"这从来不是关于巧妙的模型，而是关于数据"。

## 1. 材料与角色

| 帖子 | 作者 | 票数 | 角色与独有信息 |
| --- | --- | --- | --- |
| [684353](https://www.kaggle.com/competitions/deep-past-initiative-machine-translation/discussion/684353) 1st | Datatech Club | 94 | 弃用 train.csv；GLM-OCR 布局 + Gemini-3.0-pro 提取句对；data1 29,908 → data2 30,931（CV 硬样本重抽 740 文档）→ data3 34,146（长度失配重抽 131 文档）；llmlabel 21,759；synth1 9,685/synth2 4,972；byt5-xl×11 + ct2 int8 + MBR；最佳 41.5/43.2（未选）、选中 41.6/42.8、保守 41.2/42.4 |
| [684345](https://www.kaggle.com/competitions/deep-past-initiative-machine-translation/discussion/684345) 2nd | wukeneth | 42 | vanilla byt5-large；三段 LLM 流水线（Breaker 9,378 / Fixer 11,302 / Generator 失败）；外部 ~60 本出版物 → **60,654 句对/149 源**；正字法归一化表；768 字节文档增强；Adafactor + group_by_length + **β1=0.9 稳梯度**；run1 ~90.5k 41.8/41.0 被选 |
| [684231](https://www.kaggle.com/competitions/deep-past-initiative-machine-translation/discussion/684231) 6th | — | 54 | 15 模型集成；PDF 三分类（image/text/**broken_text**）；PyMuPDF+正则+LLM / GLM-OCR 带坐标；MBR beam=4 无采样；final **40.7**、208m50s、2×T4；失败：上下文提示、名称/词典增强、权重融合、文档级 maxlen、LLM、双向训练 |
| [684329](https://www.kaggle.com/competitions/deep-past-initiative-machine-translation/discussion/684329) 8th | — | 25 | byt5-xl；**2 阶段 SFT**（~350k 噪声 3 epoch → 65k 高质量 1 epoch fp32；再多就崩）；普通版式用滑窗（prev/cur/next 页）、列式用 VLM；CV 与 LB 无相关（用前 500 对）；失败：词典/RAG 伪标、名称增强、自动对齐、RL（DPO/PPO/GRPO） |
| [684211](https://www.kaggle.com/competitions/deep-past-initiative-machine-translation/discussion/684211) 10th | — | 21 | ByT5-large/XL + MADLAD-400-3B；**CPT→SFT→伪标签**三阶段；集成 38.5/39.9 |
| [684819](https://www.kaggle.com/competitions/deep-past-initiative-machine-translation/discussion/684819) 15th | — | 16 | ByT5/Qwen3 混合；GLM-OCR（整页 + Tesseract 裁剪双路）；Gemma3-27B 伪标 + **KD 软标签**；MBR(chrF++ word_order=2)；失败：ByT5 large/XL 未调好、model soup、Qwen3.5 PL |
| [684215](https://www.kaggle.com/competitions/deep-past-initiative-machine-translation/discussion/684215) 7th | — | 33 | 数据扩 4×（~36k）：TR→EN 6k、16 本 PDF 6k、published_texts 去重后 30 词切片伪标 18k；byt5-small≪base≪large≈xl；byt5 > LLM 微调 |
| [668402](https://www.kaggle.com/competitions/deep-past-initiative-machine-translation/discussion/668402) 编译讨论 | — | 93 | 必读讨论清单（"Avoid Bad Advice"）——低资源赛的社区知识导航 |

**材料缺口（受"不扩采"约束，登记备查）**：Two practical stumbling blocks(665209,75 票)、3rd 合成数据(684425,51)、translation column 映射(664948,55)、open-source issue(680686,45)、社区知识综合(672511,45)、Data Update(664177,44)、Probing 公榜模型(668619,42)、24th Qwen2.5-32B/72B + Gemini OCR(684189,36)、A Stitch in Time(678899,36)、Cuneify/Fairseq(663233,35)、Other Public Data(663357,31) 等未收录——**3rd 的合成数据路线与实用避坑帖是主要缺口**。

## 2. 逐方案对照矩阵

| 维度 | 1st（94） | 2nd（42） | 6th（54） | 8th（25） | 10th/15th/7th |
| --- | --- | --- | --- | --- | --- |
| 官方数据用法 | **完全弃用 train.csv**，重建句对 | 三段流水线重建句对 | 文档对→句切分 | 重建高质量句对 | 10th 伪标 published；7th 切片伪标 |
| 外部数据 | PDF 书籍（自有+官方）+ OARE | ~60 本出版物 60,654 句对/149 源 | PDF 三分类提取 | 官方 PDF 两种版式 | 10th/15th/7th 各家 PDF/词典 |
| 句对齐 | GLM-OCR + Gemini 结构化提取；CV 硬样本/长度失配重抽 | Breaker/Fixer（Generator 失败） | 正则+LLM/坐标 | 滑窗（跨页）+ VLM（列式） | — |
| 归一化/去重 | 预处理尽量，后处理尽量少 | 正字法表 + prefer-EN + 多版本增强 | 字符修复（AKT5 规则等） | 字符/上下标/苏美尔语展开 | 15th 名称词典；7th 去重 |
| 模型 | byt5-xl ×11 | byt5-large（原版） | byt5 base/large ×15 | byt5-xl | 10th ByT5+MADLAD；15th ByT5+Qwen3；7th byt5-xl |
| 训练 | 3 epoch 固定；1 个质量加权损失模型 | Adafactor；group_by_length+β1=0.9 | 5 折 CV 最佳模型 | **2 阶段 SFT**（噪声→干净 1 epoch） | 10th CPT→SFT→PL；15th KD |
| 推理/集成 | ct2 int8 + MBR（beam 4 + 采样 3 温度） | 单模型最优配置 | MBR beam=4 无采样 | 单模型 | 15th MBR(chrF++)；10th MBR |
| 成绩 | 最佳 41.5/43.2（未选）；选中 41.6/42.8；保守 41.2/42.4 | run1 41.8/41.0（选中）；run3 42.4/40.4 | 40.7 | 金区（未给总分） | 10th 38.5/39.9；7th 金区 |
| 失败清单 | decoder-only、CPT、多语、上下文、TTA | 形态元数据生成、逐词词典、PN 后处理 | 上下文提示、名称/词典增强、权重融合、长 maxlen、LLM、双向 | 词典/RAG 伪标、名称增强、自动对齐、RL | 15th：model soup、Qwen3.5；7th：手动对齐收益低 |

## 3. 共识、分歧与裁决

### 共识一：数据质量与规模决定一切（全员，1st 直接用作标题）

1st："Data Quality Dictates Everything"；
2nd："这是一个数据瓶颈问题……模型的每个改进点都来自更大、更干净的语料"；
15th："这从来不是关于巧妙的模型，而是关于数据"；
8th："两阶段 SFT 是最大单项贡献"；
7th：数据扩 4× 后单模型进金区。

**裁决**：官方 6.5k 文档对 NMT 来说极小；**分数主要来自"从 PDF/在线资源重建句级平行语料"的工程能力**，模型结构改动无收益。置信度：高（多队独立）。

### 共识二：ByT5（byte-level）是最合适的主干（多队对照）

8th：NLLB/mT5 比 ByT5 差 1–1.5 GM；
7th：byt5-small≪base≪large≈xl；其他 T5 变体差很多；LLM 微调不如 byt5；
2nd/1st/10th/15th：ByT5 为集成核心（15th 混 Qwen3 做多样性）。

**裁决**：阿卡德语转写的罕见字符/变音符号对 subword 分词不友好；byte-level 无 OOV 且对正字法变体鲁棒。置信度：高。

### 共识三：更大模型更好——前提是数据干净（1st/8th/7th）

7th：模型规模单调提升；
8th："larger the model, better the score"（ByT5-XL）；
1st：从 byt5-base→large→xl 公榜显著提升，但强调"前提是有足够干净的数据，否则大模型过拟合"。

**裁决**：在数据工程到位后，容量收益可以兑现；这与"小数据只能用简单模型"（T12）并不矛盾——本场用 LLM 把数据从小扩到大。置信度：高。

### 共识四：MBR 解码是标准增益（1st/6th/10th/15th）

1st：beam 4 + 3 温度采样 2 候选 + chrF++/BLEU/Jaccard/长度奖励加权 MBR；
6th：MBR beam=4 无采样（采样会降分）；
15th：MBR(chrF++ word_order=2)；
10th：MBR。

**裁决**：低资源翻译里，多候选一致性选择（MBR）比单次 beam 更稳；候选生成方式（采样温度/beam）需按模型调。置信度：中高。

### 分歧一：伪标签/合成数据——来源与筛选决定成败

有效：10th（自模型伪标 published_texts）、15th（Gemma3-27B 教师 + KD 软标签）、7th（切片伪标 18k）、1st（synth1/2 进多个集成模型）；
失败：2nd 的 Generator（仅形态元数据生成翻译，噪声大）、8th 的词典/RAG 重建、6th 的词典/名称增强、15th 的 Qwen3.5 PL。

**裁决**：伪标的收益取决于**教师质量与筛选**：强教师（Gemma/自集成+MBR）有效；从形态/词典规则"重建"不可行。置信度：中高。

### 分歧二：训练阶段设计（2 阶段 vs CPT vs 单阶段）

8th：噪声大数据 3 epoch → 干净小数据 **1 epoch**（再多崩）；
10th：CPT（3 epoch 文档级）→ SFT → 伪标，一致优于直接微调；
1st：固定 3 epoch + eval_loss 选 ckpt；
2nd：单阶段但配 group_by_length + β1=0.9 稳梯度。

**裁决**：数据分布差异大时，"先宽后窄"的两阶段/CPT 有效；高质量阶段极易过拟合（1 epoch 即上限），选 ckpt 要盯 eval_loss。置信度：中高。

### 分歧三：后处理与提交选择

1st：原则上"预处理尽力、后处理尽量少"；最终仍选了带 n-gram 清理的公榜更高提交 → **私榜反而更差**（41.6/42.8 vs 未选 41.5/43.2），自认判断被证明正确；
2nd：公榜峰值 42.4 对应私榜 40.4，选稳健 41.8/41.0；
8th/15th：LLM 后处理无收益；名称后处理无收益。

**裁决**：低资源翻译的榜单随机性/来源差异大；**后处理与提交选择要按"稳健"而非"公榜峰值"**——本场两队的自述构成直接证据（对照 T3/T10）。置信度：中高。

## 4. 增量数字账

| 动作 | 数字 | 来源 |
| --- | --- | --- |
| 1st 数据链 | data1 29,908 句对/4,472 泥板 → data2 30,931（硬样本重抽 740 文档）→ data3 34,146（长度失配重抽 131 文档）；llmlabel 21,759；synth1 9,685；synth2 4,972 | 1st |
| 1st 单模型成绩 | 多个 byt5-xl+M​​BR 单模型提交 41.0–42.0/39.5–40.5（如 data2_llmlabel_synth2 42.0/40.4）——**单模型即可金区** | 1st（图） |
| 1st 提交选择 | 最佳 41.5/43.2（未选）；选中 41.6/42.8（+n-gram 清理）；保守 41.2/42.4 | 1st |
| 1st 训练 | 3 epoch、bs 64；1 个模型质量加权损失 bs 48 4 epoch；ct2 int8_float32；预编译省 30 min；9h 限制几乎用尽 | 1st |
| 1st ckpt 选择 | eval/loss 最低 ~2.5–3k step；eval/chrf、eval/bleu 持续上涨至 4k+（不可信） | 1st（图） |
| 2nd 数据 | Breaker 1,558 文档/9,378 句对；Fixer 1,416 文档/11,302 句对；外部 60,654 句对/149 源（TR 27,089/EN 21,683/FR 6,436/DE 5,413）；总量 ~90.5k–100k | 2nd |
| 2nd 训练 | byt5-large；768 bytes；Adafactor；group_by_length；β1=0.9 稳梯度；run1 41.8/41.0（选中）、run2 42.1/40.9、run3 42.4/40.4 | 2nd |
| 6th | 15 模型（ByT5 base/large，数据子集 v1–v6 迭代清洗）；MBR beam=4；40.7；208m50s/2×T4 | 6th |
| 8th | Stage1 ~350k 噪声对 3 epoch；Stage2 ~65k 高质量 **1 epoch fp32**（>1 崩）；CV 无相关（用前 500 对） | 8th |
| 10th/15th/7th | 10th 集成 38.5/39.9（CPT→SFT→PL）；15th 5×ByT5+Qwen3 MBR、~9h；7th 数据 4×≈36k（含 18k 伪标） | 各帖 |
| 赛事 | 2674 队；DPI BLEU/chrF++；120 帖 | 元数据 |

**结构校验（2 处吻合）**

1. 1st 的 data2 增量逻辑（740 份硬样本重抽 → +1,023 句对）与"CV 反查错误样本"的方法自洽 ✓；
2. 2nd 的 149 源语言分布加总 ≈60.6k ✓（27,089+21,683+6,436+5,413=60,621）。

## 5. 机制推演

**M1｜为什么"数据瓶颈"压过模型设计**：官方语料 6.5k 文档、句级对齐缺失；对 NMT 来说这是"十万句对以下"的低资源区间，模型容量的边际收益远小于语料规模/质量。LLM（GLM-OCR/Gemini/Claude）把"学术出版物的排版结构"转化为句对，相当于**用通用能力换取领域平行语料**——这是本场唯一可放大的杠杆。

**M2｜为什么 byte-level 赢**：阿卡德语转写含 ā/š/ṭ/ḫ/下标/通配符等，subword 分词器（多为现代语言/多语训练）覆盖差、把同一个词切成不同碎片；ByT5 直接在 UTF-8 字节上操作，变体在字节层共享前缀，模型能学到正字法不变性。7th/8th 的对照（byt5 vs 其他 T5/NLLB/mT5/LLM）方向一致。

**M3｜归一化与去重的统计意义**：同一符号几十种写法 → 若不归一，训练分布被"表面变体"稀释；归一把它们合并为同一 token 序列，等价于**给低频形式做数据增强**。prefer-EN 去重避免同一泥板的英/德/土译文在训练集中互相冲突（标签噪声）；多版本提取（不同 LLM 运行的翻译差异）则起到自然增强作用。

**M4｜两阶段 SFT / CPT 的机制**：Stage1 用大量噪声/宽分布数据学"任务先验"（Akka→En 的粗映射），Stage2 用干净数据在 1 个 epoch 内把决策边界收紧；直接大量训练干净数据会很快过拟合（8th 的"再训崩"、1st 的 loss 拐点）。CPT 则先适配阿卡德语分布，再学翻译。

**M5｜eval_loss 与 eval_bleu/chrf 的背离**：验证集与隐藏测试的来源/风格不同；模型会先学会验证集的"对齐全貌"，指标持续上涨；而 loss 反映概率拟合质量，更早暴露过拟合（1st 图：loss 在 ~2.5–3k step 反弹）。**验证指标的选择取决于它是否代表测试分布**（对照 L52）。

**M6｜公私榜差异与"提交选择"**：低资源翻译测试集由不同出版物片段构成，来源风格差异大；公榜子集的偶然性使 42.4 公榜对应 40.4 私榜（2nd run3）。1st 的"最佳提交未选中"与此同源。**在噪声榜单下，最优策略是选择多来源稳健的模型/配置，而不是公榜峰值**（对照 T3/T10）。

## 6. 证据分级

| 断言 | 等级 | 说明 |
| --- | --- | --- |
| 1st 数据链/提交表/训练曲线 | 自述 + 18 张图（含平台截图） | 中高 |
| 2nd 外部数据 60k 句对/149 源 | 自述 + 数据集附件 | 中高 |
| 6th 15 模型+MBR 40.7 | 自述 + 图 | 中 |
| 8th 两阶段 SFT/失败清单 | 自述（开源栈，无 API） | 中 |
| 10th/15th/7th 路线 | 自述 | 中 |
| ByT5 > 其他主干 | 8th/7th 对照 + 多队选择 | 中高 |
| 伪标"教师质量决定成败" | 有效/失败案例对照 | 中 |
| 公私榜差异（1st/2nd） | 自述具体数字 | 中高 |

## 7. 边界条件与反事实

- **反事实 1**：不做句级重建（只训文档对）→ 2nd 明确"会浪费大量价值"；1st 干脆弃用官方 train.csv。
- **反事实 2**：用 subword 模型 → 8th 差 1–1.5 GM；7th "other T5 variants much worse"。
- **反事实 3**：无限加"多"但不加"干净" → 2nd run3 公榜最高、私榜最低；**数据质量 > 数量**。
- **反事实 4**：Stage2 多训几个 epoch → 8th 的模型崩塌；1st 的 eval_loss 拐点同证。
- **反事实 5**：按公榜峰值选提交 → 1st/2nd 都证明会损失私榜名次。
- **边界**：结论依赖"存在可 OCR 的学术出版物体量"与 LLM API 能力；无外部文献的小语种任务只能靠官方数据，收益结构不同。

## 8. 悬案与失败学

**悬案**

1. **3rd "Synthetic Data to Teach OA Fundamentals"（684425，51 票）未收录**——与 1st synth1/2 的对照缺失。
2. **"Two practical stumbling blocks"（665209，75 票）**：社区公认的实用避坑帖未收录。
3. 24th 的 Qwen2.5-32B/72B + Gemini OCR 路线（684189）未收录——decoder-only 路线的完整数据缺失（1st 把 decoder-only 列为放弃方向，但 25th 证明可行）。
4. 数据更新帖（664177）与 open-source 争议（680686）未收录——官方数据修订对成绩的影响无法量化。
5. 8th 的"CV 与 LB 无相关"只给了结论，无图证。

**失败学（跨队合集）**

- 伪标类：形态元数据生成翻译（2nd）、词典/RAG 重建（8th）、Qwen3.5 PL（15th）。
- 后处理类：名称/PN-GN 修正（2nd/8th/15th）、LLM 后处理（8th）、n-gram 清理（1st，公榜涨私榜跌）。
- 训练类：Stage2 >1 epoch（8th）、文档级长 maxlen（6th）、RL（DPO/PPO/GRPO，8th）、focal loss/架构技巧（15th 早期）。
- 模型类：LLM 微调不如 byt5（7th/6th）、model soup/权重融合（15th/6th）、NLLB/mT5（8th）；1st 尝试的 CPT/多语/TTA 也放弃。

## 9. 图表证据

> 路径相对本文件（`analysis/deep/`）：`../../intel/deep-past-initiative-machine-translation/bodies/<topic>_img/NN.png`

**图 1：1st 的单模型提交列表（单模型即金区）**（topic 684353）——`../../intel/deep-past-initiative-machine-translation/bodies/684353_img/02.png`

*读图结论*：多条 byt5-xl + MBR 提交在 40–42/39–40.5（如 data2_llmlabel_synth2 42.0/40.4、data2_llmlabel/split 41.4/40.5、v1 41.8/40.8）。**数据到位后单模型即可进金区**，集成只是最后的稳定增益。

**图 2：eval_loss vs eval_chrf/bleu（过拟合拐点）**（topic 684353）——`../../intel/deep-past-initiative-machine-translation/bodies/684353_img/18.png`

*读图结论*：eval/loss 在 ~2.5–3k step 触底后回升；eval/chrf 与 eval/bleu 却持续上涨到 4k+ step。**指标持续上涨是验证集过拟合的假象**——选 checkpoint 要看 loss（1st 的显式策略）。

**图 3：1st 的 LLM 提取工具（人机协同）**（topic 684353）——`../../intel/deep-past-initiative-machine-translation/bodies/684353_img/05.png`

*读图结论*：Query Builder 界面（中文提示词 + 书籍页面预览 + 批量 API），把"阿卡德语转写 + 译文"从书页抽成句对。**数据流水线的工程界面**——本场真正的"模型"。

**图 4：普通版式的跨页问题（8th）**（topic 684329）——`../../intel/deep-past-initiative-machine-translation/bodies/684329_img/01.png`

*读图结论*：这一页是转写 + 德语摘要，译文常落在下一页（8th：至少 40% 文档如此）→ 用 (prev, cur, next) 三页滑窗才能对齐。解释了"自动句对齐难"的根源。

**图 5：列式版式（8th）**（topic 684329）——`../../intel/deep-past-initiative-machine-translation/bodies/684329_img/03.png`

*读图结论*：左列阿卡德语转写、右列英语译文同行并列；OCR 易把两列句子合并 → 需要 VLM 处理。**版式分类是 PDF 流水线的前置步骤**。

**图 6：text 层的系统性 OCR 错误（6th）**（topic 684231）——`../../intel/deep-past-initiative-machine-translation/bodies/684231_img/01.png`

*读图结论*：AKT 8 (2015) 的文本层把 š 系统性渲染成 `§`（高亮处）——"broken_text" 类型无法直接 PyMuPDF 抽取，只能走图像 OCR + 自定义规则。**OCR 质量审计决定数据可用性**。

## 10. 对既有笔记/playbook 的修订点

1. `notes/nlp/deep-past-initiative-machine-translation.md` 升级（现为浅版）：补 8 篇作者/票数、六方案 × 10 维对照、数字账（60,654 句对/149 源、90.5k→100k、41.5/43.2 vs 41.6/42.8）与 6 张图证；新增"数据流水线"与"提交选择"节。
2. `playbook/nlp.md`（低资源翻译节）增补：
   - **数据构建优先**：LLM 句对齐（Breaker/Fixer；Generator=形态元数据不可行）、迭代纠错（CV 硬样本/长度失配重抽）、多版本提取增强、prefer-EN 去重；
   - **正字法归一化**（变体合并 = 免费增强）；
   - **byte-level 主干**（ByT5）对罕见字符/低资源转写最稳；
   - **训练协议**：两阶段 SFT/CPT、高质量阶段 1 epoch、用 eval_loss 而非指标选 ckpt；
   - **解码/集成**：MBR（候选生成方式按模型调）、ct2 量化让大集成可行；
   - **榜单纪律**：公榜峰值≠私榜最优；提交选择取稳健。
3. `playbook/00-通用方法论.md` 增补：**"数据瓶颈型比赛：模型是常量"**（本场 + ARIEL/LEAP 的变体）；**"教师伪标的筛选决定成败"**；**"指标持续涨而 loss 回头 = 验证集过拟合"**。
4. `analysis/THEORY.md`（Batch 5 末汇总 v0.5）候选：
   - **L69｜低资源任务的数据构建优先**（LLM 对齐/迭代纠错/归一化；分数来自语料而非模型）；
   - **L70｜byte-level 主干适配罕见字符集**（证据 = 本场多队对照）；
   - **L71｜提交选择：公榜峰值 vs 多来源稳健**（1st/2nd 的自述反向证据）。

## 11. 出处

- 1st（94 票）：https://www.kaggle.com/competitions/deep-past-initiative-machine-translation/discussion/684353
- 编译讨论（93 票）：https://www.kaggle.com/competitions/deep-past-initiative-machine-translation/discussion/668402
- 6th（54 票）：https://www.kaggle.com/competitions/deep-past-initiative-machine-translation/discussion/684231
- 2nd（42 票）：https://www.kaggle.com/competitions/deep-past-initiative-machine-translation/discussion/684345
- 7th（33 票）：https://www.kaggle.com/competitions/deep-past-initiative-machine-translation/discussion/684215
- 8th（25 票）：https://www.kaggle.com/competitions/deep-past-initiative-machine-translation/discussion/684329
- 10th（21 票）：https://www.kaggle.com/competitions/deep-past-initiative-machine-translation/discussion/684211
- 15th（16 票）：https://www.kaggle.com/competitions/deep-past-initiative-machine-translation/discussion/684819
- 缺口登记：665209、684425、664948、680686、672511、664177、668619、684189、678899、663233、663357 未收录正文
