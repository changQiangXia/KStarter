# Google ASL Fingerspelling 轻量深读（Tier B）

> 赛事：Research ｜ 主题 cv（手势序列识别）｜ 1314 队 ｜ 代码赛 ｜ 指标：自定义（字符/短语级，PostProcessorKernelDesc）
> 材料基础：`digests/asl-fingerspelling.md`（6 篇正文：1st 434485 / 2nd 434588 / 5th 434415 / 3rd 434393 / Silver 434353 / 上届冠军 409438；80 条主题索引）+ 13 张图
> 轻读时间：2026-10（Tier B B04）

## 1. 一句话重述与数字账

从 MediaPipe 关键点序列（双手+姿态+面部）解码手语拼写短语。真正的考点是**"语音识别范式迁移"：encoder-decoder/CTC、序列增广、效率与部署约束（tf-lite 40MB）**；1st 的 242 票方案把"每个效率改进都换成更深模型"写成方法论。

| 关键数字 | 值 | 来源 |
| --- | --- | --- |
| 1st（242 票） | 130 关键点（21×2 手 + 6×2 姿态 + 76 面）；改进 Squeezeformer 编码器（**Llama RoPE 替相对位置编码：训练 2×、tf-lite 3×、参数 -20%**；去 time reduction；可学习 scaling 代 Macaron）+ 2 层 Transformer 解码器 + **反转序列辅助损失**；4096→400 epochs、fp16、时间掩码；**置信度头**（归一化 Levenshtein）→ <0.15 或 <15 帧替换为 dummy 短语 "2 a-e -aroe"（+0.006）；增广：CutMix/FingerDropout/FacePoseDropout（各 +0.005）、解码输入掩码 +0.003；4 折按 signer；tf-lite 仅 39988KB、2 seed 集成 | 1st |
| 3rd（434393） | 17 层 Squeezeformer + time reduce + RoPE；输入 769 维（原始+归一化+绝对位置/1000）；不丢无手帧；训练数据+补充数据（权重 0.1）400 epochs + AWP（adv_lr 0.2）；blank index 规则后处理 | 3rd |
| 5th（434415） | Vanilla Transformer + conv stem + RoPE；**Data2vec 2.0 预训练**；3D 关键点正确旋转（去归一化→旋转→再归一化；y 缩放 1.898）；姿态+嘴唇辅助输入防过拟合；CTC 分割 + CutMix；KD | 5th |
| 2nd / Silver / 上届 | 2nd：ASR 算法对比；Silver "两行代码"达 0.770（98 票）；上届冠军方案 | 材料 |

## 2. 逐方案对照矩阵

| 维度 | 1st | 3rd | 5th |
| --- | --- | --- | --- |
| 编码器 | 14× Squeezeformer+RoPE | 17× Squeezeformer+RoPE+time reduce | Vanilla Transformer+conv stem+RoPE |
| 解码 | 2 层 Transformer + 反转辅助 | CTC/blank 规则 | CTC + KD |
| 预训练 | — | — | Data2vec 2.0 |
| 输入 | 130 点 | 769 维特征 | 3D 点+姿态+嘴唇 |
| 增广 | CutMix/FingerDropout/FacePoseDropout | 时间缩放/掩码/affine | 3D 旋转/CutMix/掩码 |
| 部署 | tf-lite fp16（40MB 限制） | — | — |
| 名次 | 1st | 3rd | 5th |

## 3. 共识、分歧与裁决

### 共识一：这是"sign-language ASR"——语音识别的工具箱直接迁移（3/3）

encoder-decoder/CTC、CTC 分割/CutMix、RoPE、Data2vec 预训练、KD、beam search 取舍——全部来自 ASR。**裁决**：跨模态序列任务优先查同构领域的成熟范式。置信度：高。

### 共识二：效率改进 = 更深模型的预算（1st 的方法论）

1st 把 RoPE（2-3×）、fp16、时间掩码、解码缓存逐项换算成"可以加深模型"的增益（每项 +0.003~0.005）；3rd 用 17 层 + time reduce。**裁决**：在部署约束（tf-lite/内存/时间）下，效率优化与架构创新等价。置信度：高。

### 共识三：时空增广是防过拟合核心（3/3）

1st：CutMix/FingerDropout/FacePoseDropout/时间掩码；3rd：时间缩放+重掩码+affine；5th：3D 旋转+掩码。**裁决**：关键点序列的增广要覆盖"丢手指、丢模态、时间伸缩、空间仿射"四个维度；丢模态增广还能提升泛化。置信度：高。

### 共识四：辅助输入（姿态/嘴唇）有效（1st/3rd/5th）

5th 明确"只用手几周 0.757，加入姿态+嘴唇后更好且防过拟合"；1st/3rd 用全 130 点/769 维。**裁决**：手语拼写并非只看手；面部/姿态提供韵律与上下文。置信度：高。

### 分歧一：解码器路线（Transformer decoder vs CTC）

1st：**Transformer decoder 优于 CTC**（即使效率重要）；3rd 用 CTC+blank 规则；5th 用 CTC+分割。**裁决**：自回归解码上限更高，CTC 更省算力；在时间/内存受限时取舍不同。置信度：中高。

### 分歧二：补充数据价值

1st：补充数据仅 +0.001（50k 样本但只有 500 短语→模型学会分类而非解码；按短语分组每 epoch 加 1 个样本）；3rd：补充数据权重 0.1 用于训练。**裁决**：补充数据的短语多样性不足时收益有限；采样策略比数据量重要。置信度：中高。

### 失败学（1st）

编辑距离作损失、CTC 辅助、label smoothing、AWP（fp16 NaN）、TTA（翻转/拉伸）、hidden mixup、beam search（太贵）均无效。**裁决**：ASR 里的部分正则/搜索技巧在此任务不迁移；fp16 下要避开 AWP。置信度：中高。

## 4. 证据分级

| 断言 | 等级 | 说明 |
| --- | --- | --- |
| 1st 的架构/增广消融/效率换算 | 自述 + 图 + 代码 + 公开权重 | 高 |
| 3rd 的 17 层/特征/训练细节 | 自述 + 代码 | 中高 |
| 5th 的 Data2vec/3D 旋转/CTC | 自述 + 代码 | 中高 |
| Silver 两行代码 0.770 | 自述（趣味帖） | 中 |
| 补充数据有限收益 | 1st 分析 | 中 |

## 5. 悬案与缺口（登记）

- 2nd 的 ASR 对比细节未细读；上届冠军方案（409438）未细读。
- 指标 PostProcessorKernelDesc 的精确计算未入库；tf-lite 40MB 规则的官方说明缺失。
- 1st 的置信度头目标（OOF Levenshtein）训练细节只简述。

## 6. 图表证据

![1st 的模型架构](../../intel/asl-fingerspelling/bodies/434485_img/01.png)

**图 1**（topic 434485）：130 点时间热力图 → 5 个特征提取分支（All/Face/LHand/RHand/Pose：Conv2d+BN+SiLU+FC）→ All 分支 Add、四分支 Concat → 14× Squeezeformer 编码器 → FC(1) 置信度 + 2 层 Transformer 解码器 → 短语预测。**"多模态关键点 + 高效编码器 + 自回归解码 + 置信度后处理"的完整骨架**。

## 7. 出处

- 1st（242 票）：https://www.kaggle.com/competitions/asl-fingerspelling/discussion/434485
- 2nd（434588）：https://www.kaggle.com/competitions/asl-fingerspelling/discussion/434588
- 5th（434415）：https://www.kaggle.com/competitions/asl-fingerspelling/discussion/434415
- 3rd（434393）：https://www.kaggle.com/competitions/asl-fingerspelling/discussion/434393
- Silver（98 票）：https://www.kaggle.com/competitions/asl-fingerspelling/discussion/434353
- 上届冠军（91 票）：https://www.kaggle.com/competitions/asl-fingerspelling/discussion/409438
