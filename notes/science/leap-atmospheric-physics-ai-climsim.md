# LEAP - Atmospheric Physics / ClimSim

> 主题：science ｜ 子类：— ｜ 领域：气候科学 ｜ 类别：Research
> 截止：2024-07-15 ｜ 队伍数：693 ｜ 机制：标准赛 ｜ 指标：物理量回归误差
> 数据来源：`intel/leap-atmospheric-physics-ai-climsim/`（80 条主题索引 + 6 篇 write-up 正文）

## 1. 任务与数据

- 预测目标：由大气状态特征预测**次网格物理量**（云量、辐射等），用于加速气候模拟（替代昂贵的物理参数化）。
- 数据形态：大规模仿真数据（数百个输入特征 + 多个输出目标）。
- 构造陷阱：
  - 输出是物理量，**误差需要符合物理约束**（如守恒、界值）；
  - 数据规模大；
  - 训练成本高（4th 记录了单模型 60-120 小时的训练时间）。

## 2. 方案谱系

| 方案 | 名次 | 关键点 |
| --- | --- | --- |
| ConvNeXt 系列 + 规模缩放 | 4th | 明确记录了三档模型（64→128→256→512 通道）的 CV/公开/私榜与**训练耗时（1×RTX4090 60h / 120h）**——**算力-收益的量化表格**很有参考价值 |

## 3. 关键技巧

- **模型规模与收益的量化**（4th 的表格：通道数翻倍 → 收益递减、时间翻倍）。
- **物理约束的输出处理**（界值裁剪、守恒修正）。
- **大数据的训练效率**（混合精度、分块）。

## 4. 可迁移性评估

- **可直接迁移**：
  - **算力-收益的消融表**（决定是否值得加大模型）；
  - 物理量的界值/守恒后处理；
  - 大模型训练的成本管理。
- 需要前提：较大算力（或 Kaggle 云端 GPU）。
- 不建议照搬：无评估地堆模型规模。

## 5. 对新手的关键启示

1. **训练成本要显式记录与权衡**（4th 的表格是范例）。
2. 物理量输出需要物理感知的后处理。
3. 与 Waveform、IceCube、G2Net 对照：**科学计算赛的共识是"物理 + 数据 + 工程成本"三者平衡**。

## 6. 出处

- 讨论区索引：`intel/leap-atmospheric-physics-ai-climsim/topics.md`（80 条）
- 已收录 write-up（6 篇）：
  - 1st（82 票）：https://www.kaggle.com/competitions/leap-atmospheric-physics-ai-climsim/discussion/523063
  - 2nd（47 票）：https://www.kaggle.com/competitions/leap-atmospheric-physics-ai-climsim/discussion/523055
  - 4th 规模对照表（34 票）：https://www.kaggle.com/competitions/leap-atmospheric-physics-ai-climsim/discussion/523042
