# CHAIi - Hindi and Tamil Question Answering

> 主题：nlp ｜ 子类：— ｜ 领域：多语言问答 ｜ 类别：Research
> 截止：2022-XX-XX ｜ 队伍数：1000+ ｜ 机制：代码赛 ｜ 指标：Jaccard / 字符 F1（抽取式问答）
> 数据来源：`intel/chaii-hindi-and-tamil-question-answering/`（80 条主题索引 + 6 篇 write-up 正文）

## 1. 任务与数据

- 预测目标：在印地语与泰米尔语文章中抽取答案片段（抽取式问答）。
- 数据形态：问题 + 上下文 + 答案跨度；**训练数据小且确认有噪声**。
- 构造陷阱：低资源语言的预训练模型有限；标注噪声大；长上下文。

## 2. 方案谱系

| 方案 | 名次 | 关键点 |
| --- | --- | --- |
| **"完全信任公开榜、不追踪本地 CV"** | 1st | 作者明确记录：训练集小且确认噪声大，因此**放弃本地 CV 作为决策依据**，直接用公开榜迭代（他还自嘲这段总结"可能事后变苦涩"） |

## 3. 关键技巧

- **何时可以信公开榜**：当训练数据小且噪声大、本地 CV 无法反映真实泛化时，公开榜可能是更可靠的信号（**前提是评估集足够大**）。
- 多语言模型的选择（XLM-R 类）与长上下文切分。
- 噪声标签的处理（软标签/过滤）。

## 4. 可迁移性评估

- **可直接迁移**：
  - **"信 CV 还是信 LB"是一个需要论证的决策**，不是教条（本场是少见的"信 LB"案例）；
  - 长上下文问答的切分与答案聚合；
  - 噪声标签的处理手段。
- 需要前提：对评估集规模与数据噪声的判断力。
- 不建议照搬：不加论证地盲信任何一侧。

## 5. 对新手的关键启示

1. **"Trust CV"不是教条**——当训练数据小且噪声大时，公开榜可能更可靠（与 ICR/Jigsaw 的两种相反案例对照）。
2. 判断依据是：**评估集大小 + 训练集噪声**。
3. 与 AI4Code、PII Detection 对照：低资源语言任务的通用手段是"多语言预训练模型 + 噪声处理"。

## 6. 轻读结论（2026-10 补）

**一句话**：训练集小而脏、公榜大且有 3 方标注 → 1st/2nd 都**完全放弃本地 CV、只信公榜**；最大涨分来自**跨语言同源数据（TyDi 孟加拉语/泰卢固语 + MLQA）**，其次是多分词器集成与图像式增强。36th 的对照（最佳公榜提交私榜第 728）提醒这条路是双刃剑。

- 1st（287923）：XLM-R/MURIL/RemBERT + **词级多数投票**；数据配方（TyDi 英/孟/泰卢固 + 2/3 chaii + SQUAD + MLQA/XQUAD、负采样 0.1、1 epoch）；发现"预训练骨干常优于其微调版"→ 单阶段；**渐进式序列长度 256→384→448 + 随机裁剪 + token cutout**；标点后处理公榜 3→2 但私榜 -0.004。
- 2nd（287917）：**TyDi 孟/泰卢固把公榜 0.787→0.799**；15 模型逐步堆叠到 0.829（XLM-R×7 含俄语微调版、RemBERT×3、InfoXLM×3、MURIL×2）；Jaccard soft labels 造多样性。
- 5th（288049）：chaii 过采样 5–10×；max_len 384/doc_stride 128；**CustomSoftmax 解决跨 tokenizer 的 logits 尺度差异**。
- 36th（287919）：最佳公榜 0.795 → 私榜 0.718（728 名）；最佳 CV 提交私榜 0.744；**后处理 `expit(1.2*start)*expit(end)` 私榜 +0.004**。

**裁决**：验证集质量优于训练集时可信公榜，但必须"一冲榜、一守 CV"双提交；低资源语言优先找同源采集语料；跨分词器融合要么词级投票要么分数归一化。

**悬案**：3rd–35th 方案缺失；TyDi 与 chaii 是否共享内容无证据；本场 0 归档图。

## 7. 图表证据

无可用图证（本场归档 0 图）。

## 8. 出处

- 讨论区索引：`intel/chaii-hindi-and-tamil-question-answering/topics.md`（80 条）
- 已收录 write-up（6 篇）：
  - 1st 只信公开榜（173 票）：https://www.kaggle.com/competitions/chaii-hindi-and-tamil-question-answering/discussion/287923
  - 2nd（59 票）：https://www.kaggle.com/competitions/chaii-hindi-and-tamil-question-answering/discussion/287917
  - 5th（47 票）：https://www.kaggle.com/competitions/chaii-hindi-and-tamil-question-answering/discussion/288049
  - 36th（CV vs LB 对照 + PP）：https://www.kaggle.com/competitions/chaii-hindi-and-tamil-question-answering/discussion/287919
  - 噪声标签（65 票）：https://www.kaggle.com/competitions/chaii-hindi-and-tamil-question-answering/discussion/264395
  - Tamil Jaccard 讨论（51 票）：https://www.kaggle.com/competitions/chaii-hindi-and-tamil-question-answering/discussion/264831
- 轻读全本：`analysis/deep/chaii-hindi-and-tamil-question-answering.md`（Tier B 轻读：对照矩阵/裁决/证据分级/悬案；图证缺口已登记）
