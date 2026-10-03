# ISIC 2024 - Skin Cancer Detection with 3D-TBP

> 主题：cv（医学影像 + 表格）｜ 子类：— ｜ 领域：医疗 ｜ 类别：Research
> 截止：2024-09-06 ｜ 队伍数：2739 ｜ 机制：代码赛 ｜ 指标：pAUC（部分 AUC，关注高敏感度区间）
> 数据来源：`intel/isic-2024-challenge/`（80 条主题索引 + 6 篇 write-up 正文）

## 1. 任务与数据

- 预测目标：由皮肤病变的**3D 全身摄影（3D-TBP）裁剪图** + 患者元数据判断恶性（黑色素瘤）。
- 数据形态：**图像 + 表格元数据**混合；正样本极稀少（典型医学筛查场景）。
- 构造陷阱：
  - 指标是 **pAUC（部分 AUC）**——只在高敏感度区间计分，与常规 AUC 的优化目标不同；
  - 类别极度不平衡，**过采样/重加权必须配套**；
  - 图像质量与拍摄设备差异大。

## 2. 方案谱系

| 方案 | 名次 | 关键点 |
| --- | --- | --- |
| **GBDT 多实现集成 + 图像模型集成** | 1st | 与多数参赛者同构：树模型（多实现）+ 图像模型双线；起点是社区公开的"仅表格数据"notebook |
| 多模型融合 | 2nd | 强调社区讨论带来的启发 |
| 其他方案 | 9th | 见讨论区 |
| 图像数据处理 | 社区 | "More Training Data (Processed JPEGs) - Upsampling Malignant Images"——**对恶性样本上采样**是公共数据资产 |

## 3. 关键技巧

- **表格 + 图像双线并进**：元数据（年龄/部位等）与图像信息互补。
- **面向 pAUC 的优化**：指标只在高敏感度区间计分 → 需要专门的阈值/重加权策略。
- **恶性样本上采样**是公开的有效手段（社区数据集）。
- **社区起点复用**：冠军明确说用了公开的"仅表格数据"notebook 作为实验起点。

## 4. 可迁移性评估

- **可直接迁移**：
  - **pAUC/部分 AUC 类指标的优化思路**（只关注特定决策区间）；
  - 类别极不平衡时的上采样 + 重加权组合；
  - 图像 + 元数据双线融合（与 Petfinder 的"元数据作辅助"形成对照——本场元数据是有价值的）。
- 需要前提：医学影像 + 表格数据的处理能力。
- 不建议照搬：用常规 AUC 的思路优化 pAUC。

## 5. 对新手的关键启示

1. **指标是"部分 AUC"时，优化目标要相应改变**（先读懂 pAUC 的定义）。
2. **极端不平衡要同时做数据侧（上采样）与损失侧（重加权）**。
3. 与 RSNA 系列、HMS、CSIRO 对照：**医学影像是 Kaggle 最稳定的赛题来源之一**。

## 6. 出处

- 讨论区索引：`intel/isic-2024-challenge/topics.md`（80 条）
- 已收录 write-up（6 篇）：
  - 恶性样本上采样数据集（**296 票**，本场最高票）：https://www.kaggle.com/competitions/isic-2024-challenge/discussion/515356
  - 1st（149 票）：https://www.kaggle.com/competitions/isic-2024-challenge/discussion/533196
  - 9th（81 票）：https://www.kaggle.com/competitions/isic-2024-challenge/discussion/532577
  - 公开 1 / 私榜 24（81 票）：https://www.kaggle.com/competitions/isic-2024-challenge/discussion/532564
