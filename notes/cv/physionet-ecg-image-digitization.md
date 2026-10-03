# PhysioNet - ECG Image Digitization

> 主题：cv ｜ 子类：— ｜ 领域：医疗 ｜ 类别：Research
> 截止：2026-01-22 ｜ 队伍数：1424 ｜ 机制：代码赛 ｜ 指标：逐图 SNR（线性域平均后转 dB）
> 数据来源：`intel/physionet-ecg-image-digitization/`（80 条主题索引 + 6 篇 write-up 正文）

## 1. 任务与数据

- 预测目标：从**心电图的扫描图像**重建出可用的波形数值（图像 → 时序信号的逆向任务）。
- 数据形态：ECG 纸图/扫描图 + 对应的真实波形；多导联、网格背景、印刷伪影。
- 构造陷阱：
  - **图像到信号的坐标变换**（网格标定、非线性畸变）；
  - 多导联布局识别；
  - 评估是波形误差（不是像素误差）。

## 2. 方案谱系

| 方案 | 名次 | 关键点 |
| --- | --- | --- |
| **三段式流水线**（stage0/1 沿用公开实现 + stage2 分割与后处理为重点） | 2nd | 作者明确说前两阶段直接用了社区公开实现（hengck23 的基线），自己的贡献集中在**分割与后处理** |

## 3. 关键技巧

- **分阶段流水线**：版面/导联检测 → 波形分割 → 坐标到数值的转换与后处理。
- **复用公开基线**（hengck23 的实现被广泛采用），把精力放在自己的增量上。
- **后处理决定最终精度**（网格标定、断点连接、去伪影）。
- 评估是"重建信号误差"，因此**几何精度比分类精度更关键**。

## 4. 可迁移性评估

- **可直接迁移**：
  - **图像 → 数值信号的数字化流水线**（仪表读数、曲线提取、历史文档数字化通用）；
  - 分阶段设计 + 公开基线的复用策略；
  - 后处理中的几何标定。
- 需要前提：分割与几何变换能力。
- 不建议照搬：端到端回归（忽略几何约束）。

## 5. 对新手的关键启示

1. **"图像 → 数值"任务的瓶颈常在几何标定与后处理**。
2. 社区公开基线（如 hengck23 的实现）可以放心复用，把时间留给你自己的增量。
3. 与 Benetech（图表转数据）、AI4Code 对照：**结构化抽取类任务的通用套路 = 分阶段 + 后处理**。

## 6. 轻读结论（2026-10 补）

**一句话**：图像→信号的数字化任务——**几何校正 + 子像素采样密度 + 后处理（导联定律/FFT 重采样）**决定分数，模型只负责提供"轨道"。

- 1st（669584）：hengck23 校正管线 + Fourier 重采样 + 三解码策略；后处理导联定律软混合（+0.06）、TTA +0.07；10 模型集成。
- 2nd（669871）：把竞赛信号换回 PTB-XL 原始 500Hz（单折 21.67→22.49 dB）；**稀疏掩码（每列≤2 px + 小数分配）可精确往返**；whole+series 双模型；按指标结构优先中高分图。
- 3rd（669668）：低分辨算几何、原图执行；1px 掩码故意过拟合细线；宽度 2200→4400 使 SNR 24.22→31.23。
- 6th（669562）：直接回归信号绕过分割后处理；重采样基准验证 FFT 最优、密度越高越好。
- 7th（669548）：旋转分类→导联检测/分割→数字化→OOD 集成筛选；ECG-image-kit+DTD 合成数据。

**裁决**：先标准化版面再数字化；横向采样密度与亚像素编码是"白送"的 SNR；重采样用 FFT 而非图像插值；读指标要做分数贡献分解再分配算力。

**悬案**：4th/5th/13th 方案缺失；"0.16→0.20"帖未细读；合成数据增益未量化。

## 7. 图表证据

![2nd 的稀疏掩码往返](../../intel/physionet-ecg-image-digitization/bodies/669871_img/02.png)

**图 1**（topic 669871）：小数部分拆到相邻两格、重建时加权平均 → 原值精确复原（11.71/10.43/9.81/10.98），子像素精度可直接编码进标签。

## 8. 出处

- 讨论区索引：`intel/physionet-ecg-image-digitization/topics.md`（80 条）
- 已收录 write-up（6 篇）：
  - 1st（73 票）：https://www.kaggle.com/competitions/physionet-ecg-image-digitization/discussion/669584
  - 7th（48 票）：https://www.kaggle.com/competitions/physionet-ecg-image-digitization/discussion/669548
  - 方案设计讨论（40 票）：https://www.kaggle.com/competitions/physionet-ecg-image-digitization/discussion/613540
  - 2nd（36 票）：https://www.kaggle.com/competitions/physionet-ecg-image-digitization/discussion/669871
  - 3rd（31 票）：https://www.kaggle.com/competitions/physionet-ecg-image-digitization/discussion/669668
  - 6th（30 票）：https://www.kaggle.com/competitions/physionet-ecg-image-digitization/discussion/669562
- 轻读全本：`analysis/deep/physionet-ecg-image-digitization.md`（Tier B 轻读：对照矩阵/裁决/证据分级/悬案 + 3 图证）
