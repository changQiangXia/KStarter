# CZII - CryoET Object Identification

> 主题：cv ｜ 子类：— ｜ 领域：结构生物学/3D 成像 ｜ 类别：Featured
> 截止：2025-XX-XX ｜ 队伍数：1000+ ｜ 机制：代码赛 ｜ 指标：颗粒识别（3D 检测）
> 数据来源：`intel/czii-cryo-et-object-identification/`（80 条主题索引 + 6 篇 write-up 正文）

## 1. 任务与数据

- 预测目标：在**冷冻电子断层扫描（cryo-ET）** 3D 体数据中识别并定位多种亚细胞颗粒/大分子。
- 数据形态：3D 体数据（Tomogram）+ 坐标标注；目标小、类别多、各向异性分辨率。
- 构造陷阱：
  - **3D 各向异性**（XY 与 Z 方向分辨率不同）→ 需要专门的重采样/网络设计；
  - 目标尺度小、数据量有限；
  - 体数据显存开销大。

## 2. 方案谱系

| 方案 | 名次 | 关键点 |
| --- | --- | --- |
| 目标检测路线（含训练代码） | 1st（检测部分） | 作者来自乌克兰敖德萨，write-up 开头记录了战争背景——**Kaggle 社区的人文一面** |
| 其他方案 | 见讨论区 | |

## 3. 关键技巧

- **各向异性处理**：对 Z 轴做插值/重采样，或设计各向异性卷积。
- **3D 检测框架**：把通用检测器（如 3D U-Net 系检测头）适配到体数据。
- **按体数据（tomogram）分组验证**。
- **内存管理**：体数据分块推理。

## 4. 可迁移性评估

- **可直接迁移**：
  - **各向异性数据的处理**（医学/材料/生物成像通用）；
  - 3D 检测的"分块 + 合并"推理范式；
  - 按扫描/患者/样本分组。
- 需要前提：3D 影像工具链与显存预算。
- 不建议照搬：直接按各向同性假设处理。

## 5. 对新手的关键启示

1. **先检查体数据的分辨率是否各向异性**——这决定预处理与网络设计。
2. 与 Vesuvius（3D CT 墨迹）、RSNA 系列（3D CT/MRI）对照：**3D 医学/科学影像的方法论高度共通**。

## 6. 出处

- 讨论区索引：`intel/czii-cryo-et-object-identification/topics.md`（80 条）
- 已收录 write-up（6 篇）：
  - 1st 检测部分（117 票，含训练代码）：https://www.kaggle.com/competitions/czii-cryo-et-object-identification/discussion/561440
  - 1st 分割部分（103 票）：https://www.kaggle.com/competitions/czii-cryo-et-object-identification/discussion/561510
  - 4th（68 票，含源码与提交）：https://www.kaggle.com/competitions/czii-cryo-et-object-identification/discussion/561401
