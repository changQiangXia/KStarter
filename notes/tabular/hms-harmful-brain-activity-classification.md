# HMS - Harmful Brain Activity Classification

> 主题：tabular（信号处理）｜ 子类：— ｜ 领域：医疗 ｜ 类别：Featured
> 截止：2024-04-08 ｜ 队伍数：2767 ｜ 机制：代码赛 ｜ 指标：KL 散度（多类别概率）
> 数据来源：`intel/hms-harmful-brain-activity-classification/`（80 条主题索引 + 6 篇 write-up 正文）

## 1. 任务与数据

- 预测目标：由脑电图（EEG）判断**有害脑活动**类型（癫痫发作等），输出 6 类概率分布；KL 散度评估。
- 数据结构：train.csv **106,800 行**，但只有 17,089 个 eeg_id、11,138 个 spectrogram_id、1,950 名患者——**行只是某患者的一个时间窗**：EEG 片段 [T−25:T+25]（50s）、频谱 [T−300:T+300]（600s）、预测目标在中段 [T−5:T+5]（10s）。
- **两处隐藏位移（深读核心）**：
  1) **标注者位移**：训练标签来自 119 名混合标注者（癫痫均值 **18.8%**），测试来自 20 名**专家**（**1.5%**）→ 必须把训练子集对齐专家口径（`vote_count ≥ 10`）；
  2) **增广复制**：主办方用"同标签 + EEG 平移"造出约 10 万冗余行 → 折间泄漏；3rd 逆向还原出 **6,350 行真实数据**后 CV–LB 相关性才变好。

## 2. 方案谱系

| 方案 | 名次 | 关键点 |
| --- | --- | --- |
| 团队集成（统一验证协议） | 1st（Sony） | cdeotte 验证法：按 eeg_id 归一标签、裁 EEG 中段；5 折 GroupKFold；`vote≥10` |
| 16 通道频谱 → **3D-CNN** + EEG 重塑为图像（EffNet-B5） | 2nd | 2D-CNN 无法编码通道位置（通道方向无 padding）；x3d-l priv 0.29；EEG-图 priv **0.2829** |
| 双路线：16 张 MelSpec 拼接（含中段 zoom）+ 1D Conv/Squeezeformer | 3rd | **逆向增广 → 6,350 行**；2D 只用高质量数据；1D 从零训练可用低票数据；伪标签试过无收益 |
| "One Mega Model"：三支路嵌入拼接 + 低票伪标签 | 8th（单模金） | `新标签 = 0.1×旧 + 0.3×模型1..3`；2×专家行 + 1×伪标签行；CV 0.246 / priv **0.290** |
| 数据理解 + EffNetB2 起步 | 社区（603 票） | 把"行=时间窗"讲清楚（图 1） |
| Magic Formula（233 票） | 社区机制 | 逆向官方频谱生成：**先算通道差频谱再平均**（图/公式见 §3） |

## 3. 关键技巧

- **标签来源对齐**：`vote≥10` 近似专家口径；在 KL 指标下，用混合人群标签训练会系统性高估癫痫类。
- **反增广**：同患者/同段信号跨折=泄漏；还原真实数据点（3rd：6,350 行）或用患者分组 + 伪标签回填（8th）。
- **Magic Formula（变换顺序定理）**：官方 4 张频谱是"4 组通道差**各自取谱后平均**"；若先把波形相加再取谱，望远镜求和会退化为 `Fp1−O1`，丢掉中间通道信息。**通则在非线性变换前不要做线性合并。** 实测：官方频谱 0.66 → EEG 频谱 0.63 → 两者同用 **0.59**（KL，越低越好）。
- **表示与架构匹配**：通道位置敏感的频谱用 3D-CNN（2nd）或控制拼接顺序（3rd 的双香蕉 16 对差分）；ViT 用全局注意力弱化位置假设（8th）。
- **损失匹配指标**：CE(0.73/0.57) vs KL(0.66) 差异显著——KL 训练 + `clip(±1024)/32`、**不做逐样本/逐批归一化**（3rd 实测有害）。
- **增广**：zero 掉 1–8/16 个 mel 节点（50%）、随机带宽（20%）、50s 窗平移 ±20s（50%）；1D 加时轴翻转与左右脑交换；2D 加中段 ±5s 平移。
- **伪标签的适用边界**：8th 用它把低票行拉进专家口径（单模金）；3rd 在预训练 2D + 干净子集上实测无收益——**适用性取决于模型家族与数据预算**。

## 4. 可迁移性评估

- **可直接迁移**：标签来源审计（谁标注训练/测试）；按实体（患者/eeg_id）分组；反增广去冗余；"先变换后合并"的非线性顺序原则；损失-指标匹配；on-the-fly GPU 特征（torchaudio MelSpec）。
- **需要前提**：多标注者/多来源标签结构；能读主办方论文或数据生成逻辑。
- **不建议照搬**：不做过滤直接全量训练（KL 下分布错配）；逐样本归一化；把 10 分钟频谱当主力（收益弱）。

## 5. 对新手的关键启示

1. **先读主办方论文/数据说明**：标注者构成（119 vs 20）这类事实决定训练集怎么筛。
2. **行≠样本**：看到"巨大行数 + 少量实体 ID"先怀疑冗余与泄漏。
3. **逆向生成过程**（频谱公式、增广方式）往往比换模型更值钱——本场两篇最高票帖子都是"理解类"。
4. **KL/概率指标**：输出要校准、损失要匹配；CE 用错会白忙。

## 6. 图表证据（深读内嵌）

**图 1：数据结构（行=时间窗）** —— `intel/hms-harmful-brain-activity-classification/bodies/468010_img/01.png`（603 票帖）

![HMS 数据结构](../../intel/hms-harmful-brain-activity-classification/bodies/468010_img/01.png)

**图 2：One Mega Model 三支路结构** —— `intel/hms-harmful-brain-activity-classification/bodies/492482_img/03.png`（8th 单模金）

![One Mega Model](../../intel/hms-harmful-brain-activity-classification/bodies/492482_img/03.png)

## 7. 深读结论（2026-10 补）

- 两个隐藏位移（标注者/增广）是本场真正的"题眼"，先解决它们再谈架构；两条夺冠路线（8th 单模 vs 1st/3rd 集成）都以它们为前提。
- 伪标签结论在本场分裂（8th 受益/3rd 无效）——记录为张力而非定论；适用条件：从零训练 + 专家数据稀缺时更可能受益。
- "先变换后合并"与"损失匹配指标"是本场产出的两条最通用工程原则。

## 8. 出处

- 数据理解 starter（603 票）：https://www.kaggle.com/competitions/hms-harmful-brain-activity-classification/discussion/468010
- Magic Formula（233 票）：https://www.kaggle.com/competitions/hms-harmful-brain-activity-classification/discussion/469760
- 3rd：https://www.kaggle.com/competitions/hms-harmful-brain-activity-classification/discussion/492471
- 2nd：https://www.kaggle.com/competitions/hms-harmful-brain-activity-classification/discussion/492254
- 8th：https://www.kaggle.com/competitions/hms-harmful-brain-activity-classification/discussion/492482
- 1st：https://www.kaggle.com/competitions/hms-harmful-brain-activity-classification/discussion/492560
