# Stable Diffusion - Image to Prompts 轻量深读（Tier B）

> 赛事：Featured ｜ 主题 cv（图像→提示词，跨模态检索）｜ 1231 队 ｜ 代码赛 ｜ 指标：Mean Cosine Similarity（对 all-MiniLM-L6-v2 句向量的平均余弦）
> 材料基础：`digests/stable-diffusion-image-to-prompts.md`（6 篇正文：1st 411237 / 2nd 410606 / 3rd 410686 / 11th 765 行处 / 起步指南 831 行处 / 数据集帖；80 条主题索引）+ 1 张图
> 轻读时间：2026-10（Tier B B10）

## 1. 一句话重述与数字账

给一张 Stable Diffusion 生成的图，预测它对应的提示词——但由于指标只比较**句子嵌入的余弦相似度**，任务实际退化成"**预测句向量**"（预测文本的语法/顺序几乎不重要）。真正的考点是**自造大规模"提示词-图像"对 + 加速生成 + 用多 backbone 回归句向量**。

| 关键数字 | 值 | 来源 |
| --- | --- | --- |
| 1st（411237，121 票） | **约 860 万提示词生成约 1060 万张图**；加速链路：xFormers（15s→10s）→ FP16（→5s）→ 分辨率 768→512、采样步数 50→25（→**2s/图**）；数据：DiffusionDB-2M + 图像描述数据集（COCO Captions、VizWiz、Open Images、ADE20K、Flickr30K、TextCaps，去重相似度 >0.8）+ ChatGPT 生成提示词 → **PROMPTS_HQ（约 200 万高质量提示词，每条生成 2 张不同 seed 的图）**；COYO-700M 筛出约 660 万对做 **PROMPTS_LQ** 用于**预训练（+0.008~0.01）**；模型 = **ViT-Large、ConvNeXt-XXLarge、BLIP-2**（**去掉 BLIP-2 的 LLM 部分**——"语法与顺序不重要甚至有害"）；LoRA 微调底层；**在输出层前加一个大全连接层（Linear→BN→ReLU→Linear）对 CLIP 有显著提升**；两阶段训练（先 LQ 预训练、再 HQ 微调）；同提示词的多张图每 epoch 随机选一张；更大输入尺寸更好（用到 336）；CLIP 不用增强、BLIP-2 用默认增强；最终 = 三类模型嵌入的**加权集成** | 411237 |
| 2nd（410606，96 票） | 与公开 ViT 基线同源；**生成提速 4×**：调度器 DDIM→**DPMSolver++**（50→16 步）+ FP16 + xFormers；关键教训：**固定随机种子是错误**——每条提示词用不同 seed（`zlib.adler32(name, index)` 生成）后分数大幅提升；guidance 7.5 与 9.0 差异不大、3.0 明显更差；数据：DiffusionDB（约 180 万去重提示词）+ COCO（约 60 万 caption→50 万图）+ **Open Images 前 500 万自然图经 BLIP-2-flan-t5-xxl 生成 caption（用"链式生成"制造多句复杂提示）再喂 SD**；训练（图 1）：Dataset A 训 4 个视觉模型（ConvNeXt-xlarge/256、BLIP-2 vision/224、EVA02-L/336、EVA02-e/224）→ 在 A+B 上以更大分辨率（384/336/448/336）继续训练并冻结权重 → 每个模型接 Q-former 头 → 视觉模型与 Q-former 分别加权平均 → 最终平均 | 410606 |
| 3rd（410686） | CLIP 直接回归 384 维句向量；约 40 万数据；**关键数据集 = VizWiz caption（约 7 万，每条最多 5 个 caption 抽 3 个）**——"比 COCO 更描述性、更多样、更长"：加入后本地验证 0.5415 / LB 0.5309，不加则 0.5528 / **0.48765**（本地更高但 LB 大跌，说明泛化更好）；DiffusionDB 30 万（自生成 SD2 图，含 21 万提示词筛选 + 8 万用已训模型做**难例采样**）；COCO 2.5 万 | 410686 |
| 社区侧 | "**我上传了 DiffusionDB-2M**"（138 票）、"3 万对图像-提示词"（102 票）、"我分享 SD2 生成的图像"（81 票）、"Vlomme 的实验"（59 票）、"基于检索的工程方案"（53 票）、"ChatGPT 生成的图像-提示词对"（52 票）、"如何到 0.58+"（831 行处） | 社区 |

## 2. 逐方案对照矩阵

| 维度 | 1st | 2nd | 3rd |
| --- | --- | --- | --- |
| 自造数据规模 | **~1060 万图 / 860 万提示词** | ~180 万提示词（+COCO+OID→BLIP-2 链式 caption） | ~40 万（VizWiz 为关键） |
| 生成加速 | xFormers→FP16→512/25 步（2s/图） | DPMSolver++ 16 步 + xFormers（4×） | — |
| 模型 | ViT-L / ConvNeXt-XXL / BLIP-2（去 LLM）+ 额外 FC 层 | 4 个视觉模型（两阶段放大分辨率）+ Q-former 头 | CLIP → 384 维 |
| 关键技巧 | 两阶段预训练（LQ→HQ）、LoRA、去 LLM | **每提示词不同 seed**、链式 caption | **VizWiz 提升泛化**、难例采样 |
| 集成 | 三类嵌入加权 | 双路加权平均 + 最终平均 | 单模 |

## 3. 共识、分歧与裁决

### 共识一：数据规模与多样性就是主赛道（1st/2nd/3rd + 社区数据帖）

1st 生成 1060 万图；2nd 用 DiffusionDB+COCO+OID 转 caption；3rd 发现"更描述性的 caption 数据（VizWiz）"虽降低本地验证却大幅提升 LB。**裁决**：本场的模型架构是次要变量（ViT/ConvNeXt/CLIP 都能用），**数据来源与提示词分布**才是主变量；高描述性、长句、多样的 caption 数据能提升泛化。置信度：高。

### 共识二：指标只比句向量 → 不需要生成文本（1st/2nd/3rd）

三队都直接回归句向量（all-MiniLM-L6-v2 的输出）；1st 还专门去掉 BLIP-2 的 LLM 部分（"语法与顺序不重要甚至有害"）。**裁决**：先读指标——"图像描述生成"类任务若只比嵌入余弦，应把它当作"跨模态回归/检索"而非文本生成。置信度：高。

### 共识三：生成数据的随机性细节会显著影响质量（2nd + 1st）

2nd 明确"固定 seed 是大错"（每条提示词换 seed 后分数大涨）；1st 也每条提示词生成 2 张不同 seed 的图。**裁决**：自造数据时，多样性（seed/guidance/步数）既是数据增强也是分布覆盖，必须显式设计。置信度：高。

### 分歧一：更大的模型 vs 更大的数据

1st 用 3 类大 backbone + 10M 数据；3rd 用单 CLIP + 40 万数据拿到第 3。**裁决**：数据管线（尤其 caption 质量）能补偿模型规模；算力有限时应先投数据质量。置信度：中高。

### 事件：公共数据集生态（138/102/81/52 票）

DiffusionDB-2M 上传、3 万对数据、SD2 生成图、ChatGPT 生成对等帖子构成全场公共基础设施。**裁决**：无数据赛的"数据共享帖"等价于半条赛道；引用时要注意各数据集的生成模型/参数差异（SD1.x vs SD2）。置信度：中高。

## 4. 证据分级

| 断言 | 等级 | 说明 |
| --- | --- | --- |
| 1st 的数据规模、加速链路与模型细节 | 自述 + 消融表（文中称 table 1）+ 公开代码 | 高 |
| 2nd 的"seed 不同"教训与两阶段训练 | 自述 + 管线图 | 高 |
| 3rd 的 VizWiz 对照（0.5415/0.5309 vs 0.5528/0.48765） | 自述 + 数字对照 | 高 |
| 社区数据集的质量与规模 | 高票帖子 | 中高 |
| "去 LLM 的 BLIP-2 更好" | 1st 自述（机制解释合理） | 中 |

## 5. 悬案与缺口（登记）

- 4th–10th 的方案未细读；"Vlomme 的实验"（59 票）、"基于检索的工程方案"（53 票）、"如何到 0.58+"（831 行处）未细读；
- 1st 的消融表（table 1）细节未在 digest 展开；
- 各数据集使用的 SD 版本差异（1.x/2.x）对结果的影响未系统整理；
- 归档 1 图：2nd 的两阶段训练管线（图 1）为关键图证。

## 6. 图表证据

![2nd 的两阶段训练与集成管线](../../intel/stable-diffusion-image-to-prompts/bodies/410606_img/01.png)

**图 1**（topic 410606）：数据分 A/B 两组（A：DiffusionDB 1M + COCO 500k + OID1/2 2M + ChatGPT 1M；B：DiffusionDB 800k + OID3/4/5 3M）；先用 A 训 4 个视觉模型（ConvNeXt-xlarge/256、BLIP-2/224、EVA02-L/336、EVA02-e/224），再在 A+B 上放大分辨率（384/336/448/336）继续训练并**冻结权重**，各接 Q-former 头；最后"Q-former 集成 + 视觉模型集成"两路加权平均再取平均。展示了"先适配提示词分布、再提分辨率、最后多头集成"的完整流程。

## 7. 出处

- 1st（121 票）：https://www.kaggle.com/competitions/stable-diffusion-image-to-prompts/discussion/411237
- 2nd（96 票）：https://www.kaggle.com/competitions/stable-diffusion-image-to-prompts/discussion/410606
- 3rd：https://www.kaggle.com/competitions/stable-diffusion-image-to-prompts/discussion/410686
- DiffusionDB-2M（138 票）：https://www.kaggle.com/competitions/stable-diffusion-image-to-prompts/discussion/388080
- 30K 图像-提示词对（102 票）：https://www.kaggle.com/competitions/stable-diffusion-image-to-prompts/discussion/391500
- 如何到 0.58+：https://www.kaggle.com/competitions/stable-diffusion-image-to-prompts/discussion/398529
