# Make Data Count - Finding Data References 轻量深读（Tier B）

> 赛事：Research ｜ 主题 nlp（document-ai，科学文献数据引用抽取）｜ 1282 队 ｜ 代码赛 ｜ 指标：`82370_MDC_Global_F1`
> 材料基础：`digests/make-data-count-finding-data-references.md`（6 篇正文：1st 606853 / 2nd 606786 / 4th 606921 / 5th 606769 / 9th 606743 / 手工标注数据 586075；80 条主题索引）+ 3 张图
> 轻读时间：2026-10（Tier B B06）

## 1. 一句话重述与数字账

从论文 PDF/XML 中找出**数据引用**（两种形态：数据集 DOI 与 accession ID），并判断每个引用是 Primary（本文产生）还是 Secondary（复用）。真正的考点是**"跟着标注产线走"**：标签由 MDC 数据引用语料 + Europe PMC NER 生成，所以直接复用同源上游语料（DCC/DataCite/EUPMC）远胜自训 NER/正则；类型分类才是建模环节。

| 关键数字 | 值 | 来源 |
| --- | --- | --- |
| 1st（606853，61 票） | DOI：DCC v4.1（DataCite 源）候选 + 文本存在性过滤（325 GT → 321 预测 / 302 TP，mention 级 F1 0.935）；类型分类**纯元数据**（Crossref 文章元数据 + DataCite 数据集元数据，标题/作者相似度最重要）CatBoost 6 折按文章分组，OOF F1 0.87、三元组 F1 0.82；accession：**不做自有抽取**，用 DCC(eupmc) + EUPMC 原始映射，按训练+LB probing 挑家族、只留文中出现者；类型用 **Qwen2.5-Coder-32B（AWQ+vLLM）0-shot** + 上下文片段（SAMN 额外给提交者/日期），MultipleChoiceLogitsProcessor 限制 A/B，最后做"同家族多数票"后处理；**预测到 DOI 的文章不再预测 accession（LB 提升）**；最终训练集调整后 F1 0.889 / pub 0.890 / priv 0.797；全流程 29 分钟 | 1st |
| 2nd（606786，29 票） | DOI：DCC v2（最佳）+ DataCite 公共数据文件；**排除训练中被标 Missing 的仓库**（figshare/CCDC/hepdata）；只留 PDF/XML 中出现者；容空白正则；Dryad 去版本号 → 阶段 1 F1 **0.964**（图 1）；accession：EUPMC TextMinedTerms 原始 dump，剔除 hgnc/gca/go/rrid 等家族与含冒号项；**有 DOI 的文章不再出 accession**；**在线表格规则**（XML 里 online-only table 中的 25 个 SAMN）→ +0.003 pub / +0.004 priv（图 2）；仅靠规则+启发式（SAMN/EMDB→Primary 等）即达 0.869 pub / 0.739 priv（**无模型也能金**）；DOI 分类用 MedGemma-4B LoRA（0.880/0.784） | 2nd |
| 4th（606921） | 候选同样来自 DCC v3.0 + PMC TextMinedTerms（过滤白名单外家族、要求文中出现），DCC/PMC 缺失时用正则兜底 + LLM 过滤；类型分类训 LLM：**tool-calling agent 从 Europe PMC 开放获取子集自动合成标签**预热 Qwen2.5，再用竞赛数据微调；伪标签 + EMA；**每篇最多 24 个 mention**（防止长尾文章主导训练）；上下文含首 1400 字符、id 片段、数据可用性段落、其他 DOI 片段、长表头尾；推理时对 cath/alphafold/cellosaurus/chembl 等家族直接假定 Secondary 加速 | 4th |
| 5th（606769） | "站在巨人肩上"：社区一条评论给出 DOI-only 配方（DCC v3 DataCite 引用对 → 只留竞赛文章 → 必须在 PDF/XML 中出现 → 造特征 → 分类器，LB 0.27）；host 回复确认"mention 来自 MDC 语料+Europe PMC，类型由人对 PDF 标注"；据此拼出 accession 全表 → pub 0.82 / priv 0.70 | 5th |
| 9th（606743） | accession 不用概率模型：**"包含 id 的句子里出现 deposit/submit → Primary，否则 Secondary"** 已覆盖 95% 正例，再用 Qwen3-Embedding-0.6B 与 DNA 声明种子句算相似度（阈值 0.667）过滤伪正例；对 ENA/蛋白类限每篇 64 条；**区间写法（KT123456-KT123489）内的 id 全删**；DOI 走 Qwen2.5-7B/32B 四步（抽链接→抽题录→Data vs Literature→Primary vs Secondary，Dryad 全设 Primary） | 9th |
| 数据质量事件 | 训练标签本身噪声极大：host 中途更新标签（589314，28 票）；社区成员手工重标 PDF 后测得"官方训练数据相对其标注的 F1 仅 0.446"（586075）；"Data Quality Mega Thread"（48 票）；另一个社区训练集在（596550，28 票） | 社区 |

## 2. 逐方案对照矩阵

| 维度 | 1st | 2nd | 4th | 9th |
| --- | --- | --- | --- | --- |
| DOI 候选 | DCC v4.1(DataCite) | DCC v2 + DataCite dump | DCC v3 | DCC v3 + Qwen 抽链接 |
| accession 候选 | DCC(eupmc)+EUPMC 映射（挑家族） | EUPMC TextMinedTerms（剔除家族） | PMC TextMinedTerms + 正则兜底 | DCC v4(eupmc) |
| 类型分类 | CatBoost（DOI，元数据）/ Qwen-32B 0-shot（ACC） | MedGemma-4B LoRA / 规则 | LLM 微调（合成数据预热 + 伪标签） | 规则 + 嵌入相似度 / Qwen 四步 |
| 关键规则 | 有 DOI 则不出 ACC | 在线表格规则、Missing 仓库剔除 | mention 上限 24、家族直判 | 区间删除、每篇上限 |
| priv | 0.797 | 0.739（纯规则）/0.784（+模型） | — | 0.745 |

## 3. 共识、分歧与裁决

### 共识一：先逆推标注产线，再决定"要不要自研抽取器"（全员）

1st/2nd/4th/5th 都发现标签来自 MDC 语料 + EUPMC NER + DataCite 映射，转而直接复用上游语料获得近 100% 召回；5th 引用的 host 回复也确认这一点；2nd 明说"我花太多时间在 NER，结果发现不需要"（4th 也是先做正则后放弃）。**裁决**：遇到"标签由自动管线生成"的赛题，第一步是**复现该管线**而不是超越它；自研 NER 是典型的时间陷阱。置信度：高（多队 + host 确认）。

### 共识二：mention 级"存在性过滤"是主要精度杠杆（1st/2nd/4th）

所有队都把候选限制在"确实出现在 PDF/XML 文本中"；1st 还做空白/Unicode 归一化以提升召回；2nd 的容空白正则把 DOI 阶段 1 做到 F1 0.964。**裁决**：候选从上游来、精度靠"文中出现 + 源过滤"保障，无需模型。置信度：高（有分数表/图证）。

### 共识三：类型分类必须按文章分组验证 + 防长尾文章（1st/4th）

1st 用按文章分组的 6 折（"测试集也是新文章"）；4th 限制每篇最多 24 个 mention 防长尾主导、用 EMA；9th 给每篇设上限。**裁决**：本任务的样本单位是文章，验证与采样都必须按文章聚合。置信度：高。

### 分歧一：类型分类用 GBDT+元数据 vs LLM 上下文

1st 的 DOI 分类是**纯元数据 CatBoost**（标题/作者相似度）且效果很好（OOF 0.87）；accession 才用 LLM 0-shot。2nd 用 MedGemma-4B LoRA；4th 用合成数据预热的 LLM；9th 用规则+嵌入。**裁决**：DOI 类型可仅凭元数据判断（是否同一团队/题目/年份）；accession 的语义要靠上下文（deposit/submit 动词）——**两类引用应走不同管线**。置信度：高。

### 分歧二：把 accession 做成分类器值得吗

9th 明确"数据极噪、没有可学的模式"，用规则即达 95% 正例覆盖；2nd 的 accession 分类器 OOF 0.91 但 LB 显著更低（疑似过拟合）；1st 用 0-shot LLM 而非训练。**裁决**：噪声标签下，简单规则 + 嵌入过滤优于训练分类器。置信度：中高。

### 事件：数据质量与"稀疏标注"陷阱

1st/2nd 都指出被标 `Missing` 的稀疏标注文章**不该计入本地 F1**（否则产生假 FP）；host 中途更新标签；社区手工重标发现官方训练数据质量极差（F1 0.446）。**裁决**：标签质量存疑的比赛要（a）自建验证口径排除污染样本，（b）用 LB 探测家族级分布，（c）关注 host 更新。置信度：高。

## 4. 证据分级

| 断言 | 等级 | 说明 |
| --- | --- | --- |
| 1st 的双管线、分数表（0.890/0.797）与 29 分钟运行 | 自述 + 完整表 + 公开代码 | 高 |
| 2nd 的在线表格规则 +0.003/+0.004 | 自述 + XML 截图（图 2） | 中高 |
| 4th 的合成数据 agent 与训练策略 | 自述 + 公开数据集/notebook | 中高 |
| 5th 引用的 host 回复 | 社区评论转述（可回溯） | 中高 |
| 9th 的规则覆盖 95% | 自述（人工分析） | 中 |
| 官方训练标签质量差（F1 0.446 对照） | 社区手工标注（单人，口径主观） | 中 |

## 5. 悬案与缺口（登记）

- 3rd/6th–8th 方案未入库；"Tricks (10char)"（47 票）、"Data Quality Mega Thread"（48 票）、"Extra Data (PDB)"（41 票）未细读；
- host 最终是否再次更新训练标签、评测口径如何处理 `Missing` 文章，材料未给结论；
- 1st 的 LB probing 家族清单选择过程未量化（只有最终名单）；
- 归档 3 图均来自 2nd（阶段 1 分数表、在线表格 XML、accession F1）。

## 6. 图表证据

![2nd 的阶段 1 验证分数](../../intel/make-data-count-finding-data-references/bodies/606786_img/01.png)

**图 1**（topic 606786）：DOI 阶段 1 的验证表——Precision 0.972 / Recall 0.957 / F1 **0.964**（TP 311、FP 9、FN 14）；此时 accession 尚未接入（全 0）。即"复用上游语料 + 文中存在性过滤"即可把候选抽取做到接近上限。

![online-only table 中的 SAMN](../../intel/make-data-count-finding-data-references/bodies/606786_img/02.png)

**图 2**（topic 606786）：文章 XML 中 "Online-only Table" 的表格（含 `SAMN10880015` 等）——训练标签里对应 25 个 SAMN 假阳性；据此加规则后 +0.003 pub / +0.004 priv。

## 7. 出处

- 1st（61 票）：https://www.kaggle.com/competitions/make-data-count-finding-data-references/discussion/606853
- 2nd（29 票）：https://www.kaggle.com/competitions/make-data-count-finding-data-references/discussion/606786
- 4th（606921）：https://www.kaggle.com/competitions/make-data-count-finding-data-references/discussion/606921
- 5th（46 票）：https://www.kaggle.com/competitions/make-data-count-finding-data-references/discussion/606769
- 9th（606743）：https://www.kaggle.com/competitions/make-data-count-finding-data-references/discussion/606743
- 手工重标数据（586075）：https://www.kaggle.com/competitions/make-data-count-finding-data-references/discussion/586075
- 标签更新公告（28 票）：https://www.kaggle.com/competitions/make-data-count-finding-data-references/discussion/589314
