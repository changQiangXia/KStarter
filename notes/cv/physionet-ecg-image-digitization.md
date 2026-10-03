# PhysioNet - ECG Image Digitization

> 主题：cv ｜ 子类：— ｜ 领域：医疗 ｜ 类别：Research
> 截止：2026-01-22 ｜ 队伍数：1424 ｜ 机制：代码赛 ｜ 指标：波形重建误差
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

## 6. 出处

- 讨论区索引：`intel/physionet-ecg-image-digitization/topics.md`（80 条）
- 已收录 write-up（6 篇）：
  - 1st（73 票）：https://www.kaggle.com/competitions/physionet-ecg-image-digitization/discussion/669584
  - 7th（48 票）：https://www.kaggle.com/competitions/physionet-ecg-image-digitization/discussion/669548
  - 方案设计讨论（40 票）：https://www.kaggle.com/competitions/physionet-ecg-image-digitization/discussion/613540
