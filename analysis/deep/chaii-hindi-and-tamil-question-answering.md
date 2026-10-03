# CHAII - Hindi and Tamil Question Answering 轻量深读（Tier B）

> 赛事：Research ｜ 主题 nlp（抽取式问答，低资源语言）｜ 943 队 ｜ 代码赛 ｜ 指标：Jaccard（答案 span 的词级重叠）
> 材料基础：`digests/chaii-hindi-and-tamil-question-answering.md`（6 篇正文：1st 287923 / 2nd 287917 / 5th 288049 / 36th 287919 / 往届资源 563 行处 / 讨论 287916；80 条主题索引）+ 0 张归档图
> 轻读时间：2026-10（Tier B B08）

## 1. 一句话重述与数字账

印地语/泰米尔语的抽取式问答。真正的考点是**"训练集小而脏、公开榜大而干净"的反常结构**：1st/2nd 都干脆**完全放弃本地 CV、只用公榜调参**；而 36th 的对照（最佳公榜提交私榜第 728）说明这条路的双刃性。核心涨分手段是**跨语言外部数据（TyDi 孟加拉语/泰卢固语 + MLQA）+ 多分词器模型集成 + 图像式增强**。

| 关键数字 | 值 | 来源 |
| --- | --- | --- |
| 1st（287923） | **完全不跟踪本地 CV，只用公榜**（理由：训练集小且噪声大；公榜更大且有 3 方标注 → 质量更高）；模型 = XLM-R Large、MURIL Large、RemBERT；**词级多数投票**融合 3 个骨干；另一份提交只用多数投票（公榜更差、私榜同为 0.787）；**数据配方（data recipes）**：TyDi 的英/孟加拉/泰卢固子集 + 2/3 chaii 训练集（负采样 0.1）+ 英文 SQUAD + MLQA/XQUAD 印地语部分；发现"**预训练骨干的表现在往优于其微调版**"→ 改为**单阶段训练**（1 epoch、sequential sampler、按配方拼数据）；**图像式增强**：随机裁剪（动态 crop 代替固定 chunk）、**渐进式序列长度 256→384→448**、token cutout（0–10% 替换为 [MASK]）；后处理沿用 HF 官方 QA notebook，仅修标点合并问题（公榜 3→2，但私榜 -0.004） | 287923 |
| 2nd（287917） | 外部数据 = 竞赛 + MLQA + **TyDi（仅孟加拉语/泰卢固语）**："TyDi 把公榜从 0.787 拉到 0.799"，并推测"公榜 >0.81 的队伍大多用了 TyDi"；**2 epoch 全量训练、不区分印地/泰米尔、无本地 CV（全靠公榜）**；集成：XLM-R 7 个（含 deepset squad2、Google 翻译 SQuAD、**俄语微调的 AlexKay 模型**）+ RemBERT 3 + InfoXLM 3 + MURIL 2 → 逐步堆叠 0.799→0.816→0.821→0.827→**0.829**；用 Jaccard-based soft labels 造多样性 | 287917 |
| 5th（288049） | 5 折；训练集 = SQuAD v2 + Google 翻译版 + 全部 TyDi + MLQA/XQUAD 印地语 + **chaii 过采样 5–10×**；1–2 epoch、max_len 384、doc_stride 128；XLM-R 0.800 / MURIL 0.802 / RemBERT 0.803；**不同分词器导致 logits 尺度不同 → 自研 CustomSoftmax 跨 context splits 归一化**再融合 | 288049 |
| 36th（287919） | 最佳公榜提交（0.795，按权重调 public）**私榜 0.718、第 728 名**——公开榜过拟合的活教材；最佳 CV 提交（CV 0.700 / 公榜 0.784）反而私榜 0.744；**后处理改进**：把 `score = start_logit + end_logit` 改成 `expit(1.2*start)*expit(end)`（贝叶斯式乘积、起点略加权）→ CV +0.003、公榜 +0.003、**私榜 +0.004** | 287919 |
| 社区 | "Noisy Labels in the dataset"（65 票）、"Tamil 的 Jaccard 可能有误导性"（51 票）、"what are we learning?"（78 票）、"Sharing Datasets"（46 票）、"我训了印地/泰米尔单语 RoBERTa-large"（45 票） | 社区 |

## 2. 逐方案对照矩阵

| 维度 | 1st | 2nd | 5th | 36th |
| --- | --- | --- | --- | --- |
| CV | **不用（只信公榜）** | 不用（只信公榜） | 5 折 CV | 两者对照 |
| 外部数据 | TyDi(英/孟/泰卢固)+SQuAD+MLQA/XQUAD | TyDi(孟/泰卢固)+MLQA | SQuADv2+翻译版+全 TyDi+MLQA/XQUAD+chaii 过采样 | 复用公开 notebook |
| 集成 | 词级多数投票（3 骨干） | 15 模型逐步堆叠 | CustomSoftmax 归一化融合 | 加权 logits |
| 特色 | 渐进式序列长度/随机裁剪/cutout | Jaccard soft labels | chaii 5–10× 过采样 | 后处理乘积式打分 +0.004 |

## 3. 共识、分歧与裁决

### 共识一：本场"训练脏、公榜干净"，信公榜是理性的（1st/2nd）

两队都明确不用本地 CV：1st 说"训练集小且噪声大，公榜更大且有 3 方标注"；2nd 说"这是我第一次完全不跟踪本地分数"。**裁决**：当验证集的信息量/标注质量优于训练集时，可用公榜做选择，但必须（a）限制提交次数、（b）保留一个"纯 CV 选择"的对照（见 36th）。置信度：高。

### 共识二：跨语言同源数据是最大单点增益（1st/2nd/5th）

2nd 量化"TyDi 孟/泰卢固 +0.012 公榜"；1st 的配方里 TyDi 是主料；5th 用全部 TyDi。**裁决**：低资源语言的跨语言迁移应优先找"同源采集流程"的语料（host 提示 chaii 与 TyDi 采集方式相似）。置信度：高。

### 共识三：多分词器集成需要专门的分数归一化（5th/1st/2nd）

5th 的 CustomSoftmax 解决跨 tokenizer 的 logits 尺度差异；1st 直接用**词级多数投票**绕开分数尺度；2nd 靠 15 模型逐步堆叠。**裁决**：不同分词器的模型不能简单平均 logits；要么统一到词级投票，要么做分数归一化。置信度：高。

### 分歧一：要不要信任公榜

1st/2nd 全信公榜并排在 1/2；36th 的最佳公榜提交私榜第 728。**裁决**：两个提交应一"冲公榜"、一"守 CV"（36th 的第二份即最佳 CV，最终私榜明显更好）；把这条写成硬规则。置信度：高。

### 事件：图像式增强迁移到 NLP（1st）

随机裁剪、渐进式序列长度（256→384→448）、token cutout——作者明确说灵感来自 fastai/Jeremy Howard 的 CV→NLP 迁移。**裁决**：NLP 里"长文本切块"与 CV 的裁剪同构，动态/渐进式策略值得作为默认增强。置信度：中高。

## 4. 证据分级

| 断言 | 等级 | 说明 |
| --- | --- | --- |
| 1st 的配方/增强/多数投票与"预训练优于微调"观察 | 自述（细节完整，无图） | 中高 |
| 2nd 的 TyDi +0.012 与 15 模型堆叠分数链 | 自述 + 逐步分数 | 中高 |
| 5th 的过采样与 CustomSoftmax | 自述 + 代码 | 中高 |
| 36th 的"最佳公榜→私榜 728"与 PP +0.004 | 自述 + 三个分数 | 高（对照完整） |
| 训练集标注噪声 | 多条高票讨论 | 中高 |

## 5. 悬案与缺口（登记）

- 3rd/4th 与 6th–35th 的方案未入库；"what are we learning?"（78 票）与"Two weeks to go"（51 票）未细读；
- "TyDi 与 chaii 可能有共享问题"只是 2nd 的猜测，无证据；
- **图证缺口**：本场 0 张归档图。

## 6. 图表证据

无可用图证（本场归档 0 图）。核心证据为分数链与配方细节，已在正文引用。

## 7. 出处

- 1st（287923）：https://www.kaggle.com/competitions/chaii-hindi-and-tamil-question-answering/discussion/287923
- 2nd（59 票）：https://www.kaggle.com/competitions/chaii-hindi-and-tamil-question-answering/discussion/287917
- 5th（47 票）：https://www.kaggle.com/competitions/chaii-hindi-and-tamil-question-answering/discussion/288049
- 36th（40 票）：https://www.kaggle.com/competitions/chaii-hindi-and-tamil-question-answering/discussion/287919
- 噪声标签（65 票）：https://www.kaggle.com/competitions/chaii-hindi-and-tamil-question-answering/discussion/264395
- Tamil Jaccard（51 票）：https://www.kaggle.com/competitions/chaii-hindi-and-tamil-question-answering/discussion/264831
