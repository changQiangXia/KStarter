# BYU - Locating Bacterial Flagellar Motors 2025

> 主题：cv ｜ 子类：— ｜ 领域：结构生物学 ｜ 类别：Research
> 截止：2025-06-04 ｜ 队伍数：1136 ｜ 机制：代码赛 ｜ 指标：3D 定位（F1/距离阈值）
> 数据来源：`intel/byu-locating-bacterial-flagellar-motors-2025/`（80 条主题索引 + 6 篇 write-up 正文）

## 1. 任务与数据

- 预测目标：在**冷冻电子断层扫描（cryo-ET）3D 体数据**中定位细菌鞭毛马达（点状目标定位）。
- 数据形态：3D 体数据 + 坐标标注（稀疏点目标）。
- 构造陷阱：目标极小且稀疏；3D 显存受限；坐标系（体素/物理单位）转换需仔细。

## 2. 方案谱系

| 方案 | 名次 | 关键点 |
| --- | --- | --- |
| **3D/2D UNet + 高斯热图（Gaussian Heatmap）** | 3rd | 把点定位转为**热图回归**再取峰值——与中心回归/SDF 同属"改为连续表示"的思路；使用社区共享的外部数据集 |
| 其他方案 | 见讨论区 | |

## 3. 关键技巧

- **点目标 → 高斯热图回归**（避免稀疏点带来的梯度问题）。
- **3D/2D 混合架构**（在计算成本与精度间折中）。
- **社区外部数据集**（本场有选手共享标注，3rd 明确致谢）。
- **坐标转换与峰值提取后处理**。

## 4. 可迁移性评估

- **可直接迁移**：
  - 点目标定位用**热图回归**（关键点检测、细胞/颗粒定位通用）；
  - 3D/2D 混合处理体数据；
  - 峰值提取与坐标变换后处理。
- 需要前提：cryo-ET 数据读取与 3D 处理能力。
- 不建议照搬：直接回归坐标（稀疏目标训练不稳）。

## 5. 对新手的关键启示

1. **点定位用热图，而不是坐标回归**（本场与 Biohub、CZII 的做法一致）。
2. **社区共享的标注数据可以改变比赛格局**（3rd 专门致谢）。
3. 与 CZII cryo-ET、Biohub、Vesuvius、RSNA 并列：**3D 生物影像的方法论已高度统一**（分块 + 连续表示回归 + 后处理）。

## 6. 出处

- 讨论区索引：`intel/byu-locating-bacterial-flagellar-motors-2025/topics.md`（80 条）
- 已收录 write-up（6 篇）：
  - 1st 3D U-Net + 分位数阈值（146 票）：https://www.kaggle.com/competitions/byu-locating-bacterial-flagellar-motors-2025/discussion/583143
  - 3rd 3D/2D UNet + 高斯热图（42 票）：https://www.kaggle.com/competitions/byu-locating-bacterial-flagellar-motors-2025/discussion/583380
  - 4th ResNet18 分类方案（42 票）：https://www.kaggle.com/competitions/byu-locating-bacterial-flagellar-motors-2025/discussion/583411
