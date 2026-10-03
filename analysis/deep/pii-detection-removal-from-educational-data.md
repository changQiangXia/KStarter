# PII Detection 深读：合成数据引擎 × 标签语义简化 × 规则后处理

> 赛事：Featured ｜ 主题 nlp（PII 检测/NER）｜ 2048 队 ｜ 代码赛 ｜ 指标：TLAL F-beta（token 级，13 类 PII，偏向召回）
> 材料基础：`digests/pii-detection-removal-from-educational-data.md`（8 篇：外部数据影响 169 票/More data 134/1st 99/H2O LLM 85/9th 68/2nd 57/4th/5th + 效率方案；120 条索引）+ 1 张图
> 深读时间：2026-10（Tier A #50，**Batch 5 收官**）

## 0. 一句话重述：这道题真正在考什么

题面是"在学生写作中检测 13 类 PII（token 分类，F-beta 偏向召回）"，实际被考的是**合成数据引擎 + 对齐细节 + 规则后处理**：

1. **外部合成数据是主引擎**：nbroad / mpware / pjmathematician 三套社区数据集 + 各队自生成数据；"Impact of External Datasets"（169 票）逐套量化增益；Mixtral 生成的 2,355 篇把公榜 **0.854→0.888**；4th 用 **Llama3-70B 生成 ~4,600 样本**，单模型（同数据）**超过其最佳集成**——数据质量 > 模型/集成。
2. **生成管线有固定配方**：persona（姓名/年龄/职业/性格）+ 场景 prompt（工具/挑战 + 批判分析）+ Faker 注入 PII 格式；再对"把导师名/虚构角色误判成 NAME_STUDENT"的假阳性样本做改写（paraphrase）补入。
3. **标签语义可简化**：B-/I- 前缀是标注规则而非语言现象 → 去掉只学 7 类，再用规则重建 BIO（2nd/9th/5th）；空白 token 被 tokenizer 忽略 → 默认 O（2nd）；`\n` 只出现在 STREET_ADDRESS → 强制修复（2nd/1st）。
4. **长文本的"训练短、推理长"**：训练 512–1536、推理 2048–4096 + stride（4th：训练 1280 → 推理 4000/stride 1024，stride 训练反而限制在 0.967；1st 训练 1600–2048；训练 >1280 无益）。
5. **后处理是分数关键**（1st 原话 "key"）：逐标签阈值、NAME_STUDENT 大小写/数字规则与**文档级传播**、PHONE↔ID、URL/EMAIL 正则、导师名剔除、换行修复。
6. **稀有类方向一致**：O 降权（1st o_weight=0.05、5th 非 O×5–10、5th-minfuka class_weight O=0.1）或 focal loss（4th）——全部提高稀有 PII 召回，契合 F-beta。

一句话：**这是一场"数据生成 + 对齐 + 规则"的比赛**——DeBERTa-v3-large 是标配主干，名次由合成数据的覆盖/质量与后处理规则决定。

## 1. 材料与角色

| 帖子 | 作者 | 票数 | 角色与独有信息 |
| --- | --- | --- | --- |
| [473139](https://www.kaggle.com/competitions/pii-detection-removal-from-educational-data/discussion/473139) 外部数据影响 | — | 169 | 三套社区数据集（PJ/Moth/Nicholas）逐套实验，均有强提升；"外部数据将主导头部"的判断被验证 |
| [472221](https://www.kaggle.com/competitions/pii-detection-removal-from-educational-data/discussion/472221) Mixtral 2355 | nbroad | 134 | persona + 场景 prompt + Faker；混入后公榜 **0.854→0.888**；格式与官方一致 |
| [497374](https://www.kaggle.com/competitions/pii-detection-removal-from-educational-data/discussion/497374) 1st | — | 99 | 多源数据 + 多 Deberta 架构（multi-sample dropout / BiLSTM / KD +0.005–0.01）；**Optuna 权重投票（7 组 10 模型）**；多步后处理（逐标签阈值/大小写/文档传播/PHONE→ID/换行修复）；私榜 **0.96988** |
| [497367](https://www.kaggle.com/competitions/pii-detection-removal-from-educational-data/discussion/497367) 4th | — | — | **Llama3-70B 生成数据**（~4,600 样本；单模型 > 最佳集成）；10 个 Deberta（focal loss + BiLSTM/GRU）；推理 4000/stride 1024；训练 1280；[SPACE] token + unidecode 预处理 |
| [497352](https://www.kaggle.com/competitions/pii-detection-removal-from-educational-data/discussion/497352) 2nd | — | 57 | **预切分子串 tokenization**（is_split_into_words，空白忽略→O）；去 B-/I-（7 类）；nbroad 权重 0.5；后处理：名称文档级传播、`\n`→STREET、O 概率缩放 0.02–0.03 |
| [497306](https://www.kaggle.com/competitions/pii-detection-removal-from-educational-data/discussion/497306) 5th | — | — | 12 模型集成，成员 maxlen 多样（128/512/1536）；**简单投票最优**；私榜更偏好长 maxlen；stride train/overlap、位置特征、EMA、冻结首 epoch、O:非O=1:10 |
| [497177](https://www.kaggle.com/competitions/pii-detection-removal-from-educational-data/discussion/497177) 9th | — | 68 | deberta v2 xlarge LoRA + v3 large；**字符级映射**解决不同 tokenizer；手动修正 train.json（~30 处）；每 epoch 回调轮换姓名；规则后处理清单 |
| [497185](https://www.kaggle.com/competitions/pii-detection-removal-from-educational-data/discussion/497185) 效率方案 | — | — | 三阶段级联（RNN 过滤 → mini-attn-RNN → v3-xsmall）+ 蒸馏：**0.955 in 8 分钟**；生产部署友好 |

**材料缺口（受"不扩采"约束，登记备查）**：Truncation of Input Sequence(473011,108)、+4400 外部文本(469493,107)、2000 AI PII 数据集(470921,104)、**H2O LLM NER 路线(481135,85)**、简单公榜提升(470978,79)、LongFormer baseline(479971,61)、原始 prompt 文本(478911,58) 等未收录——**LLM 微调路线与长文本截断细节**是主要缺口。

## 2. 逐方案对照矩阵

| 维度 | 1st | 2nd | 4th | 5th | 9th |
| --- | --- | --- | --- | --- | --- |
| 外部数据 | comp + nbroad + mpware + Tonya + 自产 2k | nbroad（权重 0.5） | **Llama3-70B 自产 ~4.6k**（最佳） | nbroad/mpware/pj 多库 | Mixtral + 假阳性改写 |
| 主干/损失 | Deberta 多架构（multi-dropout/BiLSTM/KD）；o_weight 0.05 | deberta-v3-large ×6；类别权重 | Deberta + focal loss + BiLSTM/GRU 头 | deberta-v3-large ×12；O:非O=1:10 | v2-xlarge LoRA + v3-large |
| 长度/推理 | 训练 1600–2048、3–4 epoch | 训练 512/1024/2048、stride 32 | 训练 1280 → 推理 4000/stride 1024 | 128/512/1536（成员多样）| 512/stride 128 |
| 标签处理 | 13 类 | **去 B-/I- → 7 类**；预切分子串 | 13 类；[SPACE]+unidecode | B-/I- 不用 | 去前缀；字符级对齐 |
| 后处理 | 逐标签阈值/大小写/文档传播/PHONE→ID/换行/URL-regex | 名称传播/换行/O 缩放 | 数字名剔除/导师名剔除 | 空白/前缀一致性/正则 | 大小写/称谓词/文档传播/B 修复/URL 黑名单 |
| 集成 | Optuna 权重投票（7 组 10 模型） | 6 模型 bag | 单数据模型 > 集成 | **简单投票最优** | 多模型 |
| 成绩 | 私 **0.96988** | — | — | 私 0.960–0.967（成员） | 私榜大涨（未给） |
| 失败清单 | MLM 预训练、冻结层、stride、CausalLM、Longformer、单标签模型、罕见名增强、测试伪标 | augmentations 未进最终 | Longformer/Gemma、预训练、BERT/XGB 后处理 | 二阶段 FP 模型、AWP、标签平滑、GRU | 对齐调试耗时 |

## 3. 共识、分歧与裁决

### 共识一：外部合成数据是主杠杆（全员 + 社区量化）

Impact 帖（169 票）：逐套外部数据均有强提升；
More data（134 票）：Mixtral 2,355 篇 **0.854→0.888**；
4th：Llama3-70B 自产数据让单模型超越最佳集成；
1st/2nd/5th/9th：全部使用社区或自产数据。

**裁决**：13 类 PII 的长尾分布使"定向合成"成为最高性价比动作；生成质量（persona/场景丰富度 + Faker 格式合法性 + 假阳性改写）决定上限。置信度：高。

### 共识二：标签语义简化——去掉 B-/I-，只学 7 类，规则重建 BIO（2nd/9th/5th）

2nd：B-/I- 是规则性前缀、非数据驱动 → 7 类 + 精确重建；
5th：B-/I- 不用（"should not be learned in a data-driven manner"）；
9th：去前缀 + 相邻同类合并。

**裁决**：边界前缀交给规则，模型只学类型判别；减少容量浪费与边界错误。置信度：高。

### 共识三：训练长度与推理长度分离，stride 训练无益（1st/2nd/4th/5th）

4th：训练 1280、推理 4000/stride 1024；stride 训练限制在 0.967；训练 >1280 无益；
1st：训练 1600–2048；尝试 stride 失败；
2nd：推理 stride 32（推理端重叠）；
5th：成员 maxlen 多样，私榜偏好长 maxlen。

**裁决**：**训练长度决定表示能力，推理长度/重叠决定长文本覆盖**；在推理端加长/加 stride 是低风险涨分，训练端盲目拉长/加 stride 有害。置信度：高。

### 共识四：规则后处理是分数关键（1st 明确 + 2nd/4th/5th/9th 清单）

1st："This was the key towards improving our CV and LB"；逐标签阈值、NAME_STUDENT 标题化/数字、文档级同名传播、PHONE(≥9 位)→ID、`\n` 修复、URL/EMAIL 格式；
2nd：名称传播 + `\n`→STREET + O 概率缩放；
9th：称谓词剔除/文档传播/B 修复/URL 黑名单。

**裁决**：token 分类的错误模式高度规则化（大小写、格式、重复提及），规则后处理风险低、收益高；**先做错误分析（OOF 模式）再写规则**。置信度：高。

### 共识五：稀有类加权方向一致（1st/4th/5th）

1st：o_weight=0.05；5th：非 O×5–10 或 class_weight O=0.1；4th：focal loss。

**裁决**：与 F-beta 的召回倾向一致；降 O 权重等价于提高稀有类梯度份额。置信度：高。

### 分歧一：集成策略——简单投票 vs 权重搜索 vs 单模型

5th：简单投票在 CV/公榜最优；
1st：Optuna 权重投票（7 组 10 模型）贡献显著；
4th：单数据模型 > 最佳集成；
2nd：6 模型 bag + 后处理。

**裁决**：**当合成数据质量跃迁时，单模型可以反超集成**（4th）；常态下多架构/多长度的简单投票最稳（5th）；权重搜索收益有限且有过拟合风险（1st 用 Optuna 但强调后处理是关键）。置信度：中高。

### 分歧二：数据对齐/分词策略（隐形大坑）

4th：[SPACE] token 替代 `.isspace()` 字符串 + unidecode 归一；
2nd：预切分子串 + is_split_into_words + 空白忽略→O；
9th：token→字符→spacy token 的最大值映射；
1st：跨 tokenizer 蒸馏时也需对齐。

**裁决**：没有普适最优，关键是**选定一种可验证的对齐并写回归测试**（对齐错误会静默吞噬分数）。置信度：高。

### 分歧三：外部数据是否越多越好

4th：只保留 Llama3 数据（"This was the only dataset that worked for us"）；
1st/5th：多库拼用；
9th：Mixtral + 假阳性改写。

**裁决**：数据要"覆盖稀有类且格式合法"；不同生成器的多样性有用，但低质库可以拖后腿 → 用验证集逐个评估。置信度：中高。

## 4. 增量数字账

| 动作 | 数字 | 来源 |
| --- | --- | --- |
| 外部数据增益 | Mixtral 2,355 篇：公榜 **0.854→0.888**；Impact 帖三库各自强提升 | 472221/473139 |
| 4th 自产数据 | Llama3-70B + Mixtral 共 ~4,600 样本；**Llama3 单模型 > 最佳集成** | 4th |
| 4th 长度实验 | 训练 1280；推理 4000/stride 1024；stride 训练限制 0.967；训练 >1280 无益 | 4th |
| 1st 模型群 CV | multi-dropout 0.96659、蒸馏 0.95881、exp073 0.95992、BiLSTM 0.95382、basic 0.96521、model2 0.96273；KD +0.005–0.01 | 1st（图） |
| 1st 配置 | 13 类；maxlen 1600–2048；3–4 epoch；lr 1e-5；o_weight 0.05；Optuna 投票（7 组 10 模型）；私榜 **0.96988** | 1st |
| 5th 成员 | 128/128：CV .979/公 .973/私 .960；512/512：.977/.975/.965；1536/4096：公 .972/私 .967；12 模型简单投票 | 5th |
| 2nd 配置 | 6×deberta-v3-large；512/1024/2048、stride 32；nbroad 权重 0.5；O 概率缩放 0.02–0.03 | 2nd |
| 9th | v2-xlarge LoRA + v3-large；字符级映射；手动修正 ~30 处标签；每 epoch 轮换姓名 | 9th |
| 效率方案 | 三阶段级联 + 蒸馏：**0.955 / 8 分钟**；Base ensemble 3 折 CV 0.964–0.972 | 497185 |
| 赛事 | 2048 队；13 类 PII；TLAL F-beta；120 帖 | 元数据 |

**结构校验（2 处吻合）**

1. 4th 的"Llama3 数据单模型 > 集成"与 More data 帖的"外部数据大幅增益"方向一致 ✓；
2. 1st/2nd/9th 的后处理清单高度重合（名称传播、大小写、格式约束）→ 错误模式系统性 ✓。

## 5. 机制推演

**M1｜为什么合成数据主导 PII**：13 类 PII 是长尾标签空间（STREET_ADDRESS、PHONE_NUM、ID_NUM、URL_PERSONAL、NAME_STUDENT、USERNAME、EMAIL…），真实教学文本中部分类别极稀少。合成数据可以**按类别配额生成**（Faker 保证格式合法），等价于对稀有类的定向增强；4th 的"单模型>集成"说明数据覆盖比模型多样性更重要。

**M2｜生成质量的关键因子**：① persona 多样性（避免姓名分布单一）；② 场景 prompt 多样性（工具/挑战/反思结构）；③ **假阳性模式覆盖**（导师名、虚构角色、`The` 等冠词引导的非人名）——4th/9th 专门改写这类样本；④ 与官方格式一致性（token 级标注可直接训练）。

**M3｜B-/I- 为什么应该交给规则**：BIO 前缀对应"实体边界"这一由标注约定定义的信息；模型只需回答"这个 token 属于哪类 PII"。去除前缀将标签空间从 13 类降到 7 类，减少类别不平衡（O 之外的 B-/I- 细分），也避免"B 后面跟 I 但类别不同"这类无意义的边界损失。

**M4｜长文本的注意力与覆盖**：DeBERTa 的位置编码支持长序列，但训练显存/噪声限制实际长度（1280–2048）；推理端用更长窗口 + stride 重叠，让跨窗口实体在多个窗口内被完整观察 → 提升召回。stride 训练引入重叠标注/对齐复杂度，收益为负（1st/4th 的对照）。

**M5｜规则后处理的收益来源**：模型错误集中在可枚举的模式上（名称大小写、文档内同名、格式约束、标题词）；规则修正几乎无方差，且在 F-beta 惩罚漏检的指标下"宁可多触发"。逐标签阈值则解决各类 logit 尺度不同的问题（O 概率缩放 0.02–0.03 是它的简化版）。

**M6｜效率路线的蒸馏级联**：先用极快模型（RNN/小 DeBERTa）过滤全量 token（~3% 候选），再用强模型精判，配合教师蒸馏 → 保持 0.955 的同时把推理压到 8 分钟。**在 PII 生产中（隐私删除流水线）延迟/成本与精度同等重要**，这条路线有直接落地价值。

## 6. 证据分级

| 断言 | 等级 | 说明 |
| --- | --- | --- |
| Mixtral 数据 0.854→0.888 | 社区帖（nbroad）+ 多队复现使用 | 高 |
| 4th Llama3 单模型 > 集成 | 自述（含公开数据集/模型） | 中高 |
| 1st 后处理关键 + 私 0.96988 | 自述 + 图 + 完整代码 | 高 |
| 5th 12 模型/长度多样性 | 自述 + 成员表 | 中高 |
| 2nd 7 类/B-/I- 简化 | 自述 + notebook | 中高 |
| 9th 字符级对齐/标签修正 | 自述 + 代码 | 中 |
| 效率方案 0.955/8min | 自述（未给完整验证） | 中 |

## 7. 边界条件与反事实

- **反事实 1**：不用外部数据 → 公榜停在 0.85 级（More data 帖的起点），与头部 0.96+ 差距巨大。
- **反事实 2**：不去 B-/I- → 边界约定占用容量、标签更不平衡（2nd/9th 的正向对照）。
- **反事实 3**：不做规则后处理 → 1st 称后处理是"关键"；缺少精确消融，但多队清单一致指认其价值。
- **反事实 4**：训练端拉长到 4000/加 stride → 4th 实测无益/受限（0.967）。
- **反事实 5**：把候选过滤成单标签模型（1st 的失败清单）→ 丢失跨类别上下文。
- **边界**：结论依赖"PII 格式可被 Faker 模拟 + 标注 token 级对齐可得"；自由文本/未知格式的实体检测收益会降低。

## 8. 悬案与失败学

**悬案**

1. 473011 "Truncation of Input Sequence"（108 票）未收录——长文本截断/窗口的系统分析缺失。
2. H2O Danube 1.8B 的 LLM NER 路线（481135，85 票）未收录——与 DeBERTa 路线的对照不完整。
3. 1st 后处理的独立消融（各规则各值多少）未给出；保守后处理提交的实际差异未公开。
4. 4th 的 Llama3 数据规模（~4,600）与"单模型>集成"的完整对照缺失。

**失败学（跨队合集）**

- 1st：MLM 预训练、冻结层、I-URL 修复、CausalLM 推理、stride 训练、Longformer/LLM、单标签模型、罕见名增强、测试伪标。
- 5th：NAME_STUDENT 二阶段 FP 模型（仅 +0.0005）、AWP、标签平滑、GRU 头、层重初始化。
- 4th：Longformer/Gemma、预训练、BERT 分类器过滤 FP（漏检罚重导致失败）、XGBoost 验证器。
- 2nd：多种增强（未进最终）。
- 通用：不同 tokenizer 的对齐调试极其耗时（9th 的自述）。

## 9. 图表证据

> 路径相对本文件（`analysis/deep/`）：`../../intel/pii-detection-removal-from-educational-data/bodies/<topic>_img/NN.png`

**图 1：1st 的方案总览（数据 → 模型 → 集成 → 后处理）**（topic 497374）——`../../intel/pii-detection-removal-from-educational-data/bodies/497374_img/01.png`

*读图结论*：数据侧 5 个来源（Comp/MPWARE/Nicholas Broad/TonyaRobertson/自产 2k）；模型侧 6 类 Deberta（multi-dropout 0.96659、KD 蒸馏 0.95881、BiLSTM 0.95382 等）；**Optuna 权重投票 → 多方法后处理 → 私榜 0.96988**。一张图概括"外部数据 + 架构多样性 + 后处理"的三段式。

*（本场归档图片仅此 1 张可用；Impact 帖的外部数据对比截图未入库。）*

## 10. 对既有笔记/playbook 的修订点

1. `notes/nlp/pii-detection-removal-from-educational-data.md` 升级：补 8 篇作者/票数、五方案 × 8 维对照、数字账（0.854→0.888、0.96988、0.955/8min）与 1 张图证；新增"合成数据管线"与"对齐陷阱"节。
2. `playbook/nlp.md`（NER/PII 节）增补：
   - **合成数据管线配方**：persona + 场景 + Faker + 假阳性改写 + 格式一致性；
   - **标签语义简化**：去 B-/I-，只学类型，规则重建 BIO；
   - **长度策略**：训练长度定表示、推理长度+stride 定覆盖；不要 stride 训练；
   - **后处理清单**：逐标签阈值、大小写/数字、文档级传播、格式正则、换行修复；
   - **稀有类加权**（O 降权/focal）与 F-beta 召回方向；
   - **对齐测试**：token↔spacy 映射写回归测试；unidecode/[SPACE] 等归一化。
3. `playbook/00-通用方法论.md` 增补：**"合成数据是长尾标签空间的第一杠杆"**（与 eedi/nemotron 的合成数据同族）；**"规则后处理是模型输出的免费先验"**。
4. `analysis/THEORY.md`（Batch 5 末汇总 v0.5）候选：
   - **L87｜长尾标签：定向合成 > 模型/集成**（本场 + eedi 的合成分组）；
   - **L88｜token 分类：简化标签 + 规则重建**（去前缀；后处理清单）；
   - **L89｜训练长度≠推理长度**（推理端加长/stride 提召回）。

## 11. 出处

- 外部数据影响（169 票）：https://www.kaggle.com/competitions/pii-detection-removal-from-educational-data/discussion/473139
- Mixtral 数据（134 票）：https://www.kaggle.com/competitions/pii-detection-removal-from-educational-data/discussion/472221
- 1st（99 票）：https://www.kaggle.com/competitions/pii-detection-removal-from-educational-data/discussion/497374
- 4th：https://www.kaggle.com/competitions/pii-detection-removal-from-educational-data/discussion/497367
- 2nd（57 票）：https://www.kaggle.com/competitions/pii-detection-removal-from-educational-data/discussion/497352
- 5th：https://www.kaggle.com/competitions/pii-detection-removal-from-educational-data/discussion/497306
- 9th（68 票）：https://www.kaggle.com/competitions/pii-detection-removal-from-educational-data/discussion/497177
- 效率方案：https://www.kaggle.com/competitions/pii-detection-removal-from-educational-data/discussion/497185
- 缺口登记：473011、469493、470921、481135、470978、479971、478911 未收录正文
