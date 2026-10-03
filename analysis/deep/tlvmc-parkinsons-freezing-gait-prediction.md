# TLVM C - Parkinson's Freezing of Gait Prediction 轻量深读（Tier B）

> 赛事：Research ｜ 主题 tabular（可穿戴传感器时序，多标签）｜ 1379 队 ｜ 代码赛 ｜ 指标：average precision（三事件：StartHesitation / Turn / Walking）
> 材料基础：`digests/tlvmc-parkinsons-freezing-gait-prediction.md`（6 篇正文：1st 416026 / 2nd 416057 / 4th 416410 / 6th 415992 / 8th 1182 行处 / 往届方案 394004；80 条主题索引）+ 3 张图
> 轻读时间：2026-10（Tier B B07）

## 1. 一句话重述与数字账

从三轴加速度计信号预测帕金森患者的三种冻结步态事件（AP 指标，多标签）。真正的考点是**"数据极噪 + 事件时长尺度差异"**：**训练用短窗口、推理用长窗口**是本场最大的单点杠杆（2nd 明说"最关键因素"），另外还有降低标签分辨率与"频谱图/小波"互补建模。

| 关键数字 | 值 | 来源 |
| --- | --- | --- |
| 1st（416026） | Transformer 编码器 + **2 层 BiLSTM**；**ViT 式分块**：均值-标准差归一化三轴加速度 → 补零到 15552（defog 12096）→ patch=18（defog 14）→ 输入 864×54，输出 **864×3**；**降低标签分辨率**（把标签按 patch 做 max 归约，最后 `tf.tile` 还原）；**带掩码的 BCE**（mask 取自第一个目标通道，处理缺失标注）；只用 tdcsfog/defog 各自建模，不混用；不用 daily/events/subjects/tasks 数据 | 416026 |
| 2nd（416057） | 两个数据集分别训练 **GRU**；**训练短序列、推理长序列**：tdcsfog 训练 1000 步 → 推理 3000/5000 步；defog 训练 5000 → 推理 **30000**（"本赛最关键的因素"）；特征 = 三轴 + 相邻差分 + 累积和 + 逐 ID RobustScaler 标准化；推理时只取序列中段（750/1250→2250/3750）以避免边缘效应；每目标 4 模型集成、StratifiedGroupKFold；**用 Event 列给 DeFog 的 notype 数据造伪标签**（显著提升）；模型选择用公榜（CV 噪声大且与公榜在高分段脱钩），而序列长度由 CV 决定 | 416057 |
| 6th（415992） | 双分支互补：**频谱图分支**（STFT hop 64/50 → 每帧 0.5 秒；用 **UNet 上采样保住时间分辨率** → 频轴池化 → Transformer → 0.5 秒窗预测）擅长 StartHesitation/Turn；**小波分支**（scaleogram 不降时间分辨率 → ResNet18/34）擅长 Walking；两分支 + 1D 卷积集成 0.369/0.462；**嵌套 CV**（外层 4 折 × 内层 4 折）模拟"250 条测试序列取折模型平均"的情形；transformer 加**时间邻近偏置掩码** `bias ∝ exp(-((i-j)/L)^2)` 抑制过拟合；音频式增强（audiomentations） | 415992 |
| 4th（416410） | 多层双向 GRU + 残差连接 | 416410 |
| 8th（1182 行处） | 5 折 1D-ResNet | 1182 |
| 数据侧事件 | "这个数据集是不是严重有问题？"（62 票）、"Data Update and Rescore"（29 票）、"CV and LB Scores"（40 票）、"理解数据"（61 票）、"FOG 你需要知道的一切"（52 票）——标注质量与中途数据更新是全场共同的坑 | 社区 |

## 2. 逐方案对照矩阵

| 维度 | 1st | 2nd | 6th |
| --- | --- | --- | --- |
| 表示 | 原始三轴 patch tokens | 原始三轴 + 差分/累积和 | **频谱图 / 小波 scaleogram** |
| 主干 | Transformer + 2×BiLSTM | GRU | UNet/ResNet + Transformer |
| 标签处理 | **按 patch 降分辨率 + mask BCE** | 长序列中段推理 | 标签 resize 到 0.5 秒帧 |
| 训练/推理长度 | 定长 15552/12096 分块 | **1000→5000 / 5000→30000** | 128 秒块（256 帧） |
| 验证 | — | CV 定长度 + 公榜定模型 | **嵌套 CV** |

## 3. 共识、分歧与裁决

### 共识一：训练短、推理长的"上下文外推"是最大杠杆（2nd 明说）

2nd 发现训练更长序列并不能提升、但推理时用 5–6 倍长窗口能显著改善（tdcsfog 1000→5000、defog 5000→30000）；1st 也用整段（15552）推理、6th 用 128 秒长块。**裁决**：事件型时序任务里，**感受野/推理上下文长度**是可以独立于模型容量调优的超参；训练受显存限制时，可以在推理阶段放大上下文。置信度：高（2nd 自评最关键因素，多队间接印证）。

### 共识二：标签分辨率可以粗于采样率（1st/6th）

1st 把标签按 patch 做 max 归约（864 步）后 tile 还原；6th 干脆预测 0.5 秒窗再 resize 回全分辨率。**裁决**：当指标（AP）对事件边界的容忍度较高时，降低标签/输出分辨率能显著降算力并稳定训练。置信度：中高。

### 共识三：数据噪声/标注问题必须正面处理（全员 + 高票帖）

62 票帖质疑数据严重有问题；29 票的"数据更新与重算"；1st 用掩码 BCE 处理缺失标注，2nd 用 Event 列给 notype 造伪标签。**裁决**：噪声标签赛要先审计标注（缺失/更新/分布），再设计掩码与伪标签策略。置信度：高。

### 分歧一：原始信号 vs 频谱/小波

1st/2nd/4th/8th 用原始信号（Transformer/GRU/1D-ResNet）；6th 用频谱图与小波。**裁决**：两者可互补——6th 明确指出频谱图擅长 StartHesitation/Turn、小波擅长 Walking；如果单路模型已到瓶颈，换"表示"比加深网络更值。置信度：中高。

### 分歧二：模型选择用 CV 还是公榜

2nd 明说"公榜分数升高后 CV 与公榜脱钩、CV 波动大"，因此**用公榜选模型、用 CV 选序列长度**；6th 则投入大量精力做嵌套 CV 以模拟测试聚合。**裁决**：当 CV 与榜脱钩时，应把"超参搜索"与"模型选择"放到不同信号源上，并明确各自的可信边界。置信度：中高。

### 事件：数据更新与重算（29 票）

比赛中期 host 更新数据并重算榜单。**裁决**：数据更新后必须重跑验证基线；归档时登记版本。置信度：中（现象）。

## 4. 证据分级

| 断言 | 等级 | 说明 |
| --- | --- | --- |
| 2nd 的"训练短/推理长"与伪标签增益 | 自述 + 逐项细节 | 高 |
| 1st 的 patch 降分辨率 + mask BCE | 自述 + 代码片段 | 中高 |
| 6th 的嵌套 CV、双分支互补与偏置掩码 | 自述 + 架构图 | 中高 |
| 数据严重有问题 | 高票讨论（未定论） | 中 |
| 数据更新与重算 | 官方/社区帖 | 中高 |

## 5. 悬案与缺口（登记）

- 3rd/5th/7th 的方案未入库；"Is the dataset SERIOUSLY WRONG?"（62 票）与"Data Update and Rescore"（29 票）未细读；
- 1st 未公布验证方案与集成细节；
- "训练短/推理长"的机制解释（是显存优化还是事件尺度匹配）未在材料中澄清；
- 归档 3 图：6th 的双分支架构图（图 1）与注意力偏置掩码为关键图证。

## 6. 图表证据

![6th 的频谱图/小波双分支](../../intel/tlvmc-parkinsons-freezing-gait-prediction/bodies/415992_img/01.png)

**图 1**（topic 415992）：左：三轴信号 → STFT 频谱图 → UNet（保时间分辨率）→ Transformer → 0.5 秒窗预测；右：小波 scaleogram → ResNet → Transformer → 同样的 0.5 秒窗输出。两条表示的频率/时间分辨率互补，是其"频谱擅长 StartHesitation/Turn、小波擅长 Walking"结论的结构基础。

## 7. 出处

- 1st（416026）：https://www.kaggle.com/competitions/tlvmc-parkinsons-freezing-gait-prediction/discussion/416026
- 2nd（62 票）：https://www.kaggle.com/competitions/tlvmc-parkinsons-freezing-gait-prediction/discussion/416057
- 4th（37 票）：https://www.kaggle.com/competitions/tlvmc-parkinsons-freezing-gait-prediction/discussion/416410
- 6th（66 票）：https://www.kaggle.com/competitions/tlvmc-parkinsons-freezing-gait-prediction/discussion/415992
- 数据质疑（62 票）：https://www.kaggle.com/competitions/tlvmc-parkinsons-freezing-gait-prediction/discussion/403470
- 数据更新与重算（29 票）：https://www.kaggle.com/competitions/tlvmc-parkinsons-freezing-gait-prediction/discussion/406700
