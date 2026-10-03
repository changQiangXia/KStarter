# Bengali.AI Speech Recognition 轻量深读（Tier B）

> 赛事：Research ｜ 主题 audio（低资源语言 ASR）｜ 744 队 ｜ 代码赛 ｜ 指标：Word Error Rate（WER）
> 材料基础：`digests/bengaliai-speech.md`（6 篇正文：1st 447961 / 2nd 447976 / 3rd 447957 / 5th 448006 / 44th 450635 / 实验帖 425496；80 条主题索引）+ 6 张图
> 轻读时间：2026-10（Tier B B07）

## 1. 一句话重述与数字账

孟加拉语语音识别（低资源 + **未验证的噪声标注**）。真正的考点是**"标注噪声治理"**：Whisper/Wav2Vec 系模型对错误转写极其敏感，会去学"错误音频-文本对"——因此数据清洗（MOS/WER 过滤）、外部数据、伪标签与"用 LM/标点模型补上下文"是主线；模型结构本身几乎不创新。

| 关键数字 | 值 | 来源 |
| --- | --- | --- |
| 1st（447961） | **Whisper-medium**（HF trainer，8×A6000，bs=8、lr=1e-5、50k 步）；增强：频谱抖动、时间/频率遮蔽、**16k→8k→16k 重采样**、libsonic 变速变调；推理 `max_length=260, num_beams=4, chunk_length_s=20.1`；数据：OpenSLR-37/53、MadASR、Shrutilipi、Macro、Kathbath、**GoogleTTS 合成 42 万条**、YouTube 伪标；**三轮过滤式自训练**（对 MadASR/Shrutilipi/Macro/Kathbath 推理、只留 WER<15% 的音频再训）→ Macro 验证 8% WER、公榜 ≈0.380；拼接短音频成长音频（~7 万条）→ 0.370；**自训 12k 词表孟加拉 tokenizer**（beam 8 + 20.1s chunk 的 7 小时内推理）→ 0.360；**4 模型标点集成** → 0.325；更多 YouTube 伪标 → **0.312 pub / 0.372 priv**；作者本职是低资源中亚语言 ASR，明说"**修标注噪声是本场最关键的事**" | 447961 |
| 2nd（447976） | ASR = **indicwav2vec_v1_bengali**；数据：竞赛 + Shrutilipi + MADASR + ULCA（部分链接失效）+ 噪声（MUSAN、DNS Challenge 2020）；**朗读语音重增强、自发语音轻增强**；**concat 增强**让训练长度分布贴近 OOD 测试；SpecAugment；先全量训练、再剔除 WER 最高 10% 重训；不冻结特征编码器；cosine + warmup restarts（5/3/3 epoch，峰值 lr 4e-5/3e-5/2e-5）；推理用 transformers pipeline 分块 + stride；外加 **6-gram KenLM**（IndicCorp v1+v2）与标点模型 | 447976 |
| 5th（448006） | 从 YellowKing 管线起步改 IndicWav2Vec + 重初始化 CTC；发现"**训练太久后本地 WER 与公榜脱钩**"——推测在学错误的音频/标注对；**剔除 MOS>2.0 的样本 → 0.472**；再用模型重新标注并去掉两侧 WER>0.5 的样本，本地-公榜相关性恢复；210k 步（bs16、lr8e-5）→ **0.452（无 LM）**；**集成法：把多个微调模型的最后一层隐状态拼接 → 加 Transformer 编码器 + CTC（冻结原模型，只训新头）**，全管线 0.355→**0.344**（仅 7k 步、bs8） | 448006 |
| 3rd（447957） | 见 digest（第 368 行起），以 Wav2Vec 系 + 语言模型为主 | 447957 |
| 44th（450635） | 低名次方案：说明"资源受限 + 基线微调"也能拿分 | 450635 |
| 社区侧 | "[LB 0.481] 我的实验结果"（52 票）；"**微调是关键**（LB 0.445）"（47 票）；"资源高效训练的数据集与检查点"（36 票）；"WER 的 S/I/D 分解 + 加数据太慢"（28 票）；"Wav2Vec2 + LM 基线（0.471）"（27 票） | 社区 |

## 2. 逐方案对照矩阵

| 维度 | 1st | 2nd | 5th |
| --- | --- | --- | --- |
| 底座 | Whisper-medium | indicwav2vec_v1_bengali | IndicWav2Vec（重初始化 CTC） |
| 外部数据 | OpenSLR/MadASR/Shrutilipi/Macro/Kathbath + GoogleTTS + YouTube 伪标 | 竞赛+Shrutilipi+MADASR+ULCA | 竞赛 + YellowKing 管线 |
| 噪声处理 | **三轮自训练（WER<15% 过滤）** + 拼长音频 | **剔除 WER 最高 10%** | **MOS>2.0 过滤 + 双向 WER>0.5 清洗** |
| 增强 | 频谱抖动/遮蔽、重采样链、libsonic | audiomentations（分场景强度）+ concat + SpecAugment | — |
| 解码/后处理 | 自训 12k tokenizer + beam4 + 标点 4 模型集成 | 6-gram KenLM + 标点 | 外部 LM + 标点 |
| 集成 | 单模型为主 | 单模型 + LM | **隐状态拼接 + 新 Transformer/CTC 头** |

## 3. 共识、分歧与裁决

### 共识一：标注噪声是本赛的头号敌人（1st/2nd/5th）

1st 明说"竞赛数据未验证、修标注噪声最关键"；5th 观察到"训练过久本地与公榜脱钩，疑似在学习错误的音频/标注对"；2nd 也剔除最高 WER 的 10%。**裁决**：低资源 ASR 的数据清洗（MOS/WER 过滤、重标注、伪标签筛选）是**先于建模**的工作；不做清洗，训练越久越糟。置信度：高（多队独立 + 机制自洽）。

### 共识二：外部数据 + 合成语音 + 伪标签是主要扩容手段（1st/2nd/5th，社区帖子标题亦如此）

1st 用 42 万条 GoogleTTS 合成语音、YouTube 伪标；2nd 用 Shrutilipi/MADASR/ULCA；社区教程强调"微调是关键"（Whisper-large-v3 微调帖 47 票）。**裁决**：低资源语音的容量扩展顺序 = 公开语料 → TTS 合成 → 伪标真实录音。置信度：高。

### 共识三：LM/标点后处理是"最后一公里"（1st/2nd）

1st 加 4 模型标点集成后公榜 0.360→0.325；2nd 配 6-gram KenLM + 标点模型。**裁决**：ASR 的 WER 里有一块来自格式（标点/大小写/数字），专门的后处理模型是独立增益点。置信度：高。

### 分歧一：Whisper 还是 Wav2Vec2 系

1st 选 Whisper-medium（"对 OOD 音频很鲁棒，甚至能转写歌词；但对标注噪声极敏感"）；2nd/5th 用 IndicWav2Vec + CTC。**裁决**：Whisper 的鲁棒性适合脏/OOD 数据，但需要更重的噪声治理；自监督 CTC 系在本地数据充分时更稳、更省算力。置信度：中高。

### 分歧二：如何集成 ASR 模型

5th 发现"直接平均 logits 不行（预测不对齐）"，改用**隐状态拼接 + 新 Transformer/CTC 头**（冻结原模型只训新头）→ 全管线 0.355→0.344；1st/2nd 主要靠单模型 + LM。**裁决**：异构 ASR 的融合要在"表示层"而不是"输出层"做。置信度：中高（有对照）。

### 事件：本地与公榜脱钩（5th 的诊断）

5th 给出可操作症状：本地 WER 继续降而公榜变差 = 在拟合错误标注；清洗后两者恢复相关（210k 步仍可训）。**裁决**：长训练前先做"本地-公榜一致性"体检；把这条作为噪声数据的标准诊断。置信度：中高。

## 4. 证据分级

| 断言 | 等级 | 说明 |
| --- | --- | --- |
| 1st 的三轮自训练分数链（0.380→0.312） | 自述 + 完整分数 + 公开权重/数据 | 高 |
| 5th 的 MOS/WER 清洗与本地-公榜脱钩诊断 | 自述 + 架构图 | 中高 |
| 2nd 的分场景增强与 KenLM | 自述 + 代码片段 | 中高 |
| 隐状态拼接集成的收益（0.355→0.344） | 自述（单次实验，全管线口径） | 中 |
| 社区教程"微调是关键" | 多帖共识 | 中高 |

## 5. 悬案与缺口（登记）

- 3rd 的方案未细读（digest 有正文）；44th 的具体做法未展开；
- 1st 未给"三轮自训练"的逐轮数据量与 WER 分布；
- 5th 的隐状态集成只在一个配置上验证，缺少多模型/异构（Whisper+HuBERT）证据；
- 归档 6 图：5th 的集成架构（图 1）、3rd 的 2 张图、实验帖的 1 张；1st/2nd 无图归档。

## 6. 图表证据

![5th 的隐状态拼接集成](../../intel/bengaliai-speech/bodies/448006_img/01.png)

**图 1**（topic 448006）：左为方法出处（自监督模型特征拼接 → Transformer 编码 → CTC 线性层）；右为其实际应用——两个微调模型（IndicWav2Vec、XLS-R 1b）各抽嵌入 → 拼接 → 2 层 6 头 Transformer → CLS/CTC 层；原模型冻结，只训新头（7k 步即见效）。

## 7. 出处

- 1st（447961）：https://www.kaggle.com/competitions/bengaliai-speech/discussion/447961
- 2nd（41 票）：https://www.kaggle.com/competitions/bengaliai-speech/discussion/447976
- 3rd（43 票）：https://www.kaggle.com/competitions/bengaliai-speech/discussion/447957
- 5th（34 票，ensembling works）：https://www.kaggle.com/competitions/bengaliai-speech/discussion/448006
- 44th（31 票）：https://www.kaggle.com/competitions/bengaliai-speech/discussion/450635
- "微调是关键"（47 票）：https://www.kaggle.com/competitions/bengaliai-speech/discussion/433722
