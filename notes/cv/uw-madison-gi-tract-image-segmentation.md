# UW-Madison - GI Tract Image Segmentation

> 主题：cv ｜ 子类：— ｜ 领域：医疗影像 ｜ 类别：Research
> 截止：2022-07-14 ｜ 队伍数：1548 ｜ 机制：代码赛 ｜ 指标：Dice（多类别分割）
> 数据来源：`intel/uw-madison-gi-tract-image-segmentation/`（80 条主题索引 + 6 篇 write-up 正文）

## 1. 任务与数据

- 预测目标：在 MRI 序列中分割胃肠道器官（胃、小肠、大肠，多类别分割）。
- 数据形态：2D MRI 切片序列 + 分割掩码；**切片间相关性强**（同一患者同一扫描）。
- 构造陷阱：
  - 同一患者/扫描的切片不能跨折（否则泄漏）；
  - 部分切片无标注（部分标注问题）；
  - 类别间粘连（相邻器官边界模糊）。

## 2. 方案特征

| 类型 | 说明 |
| --- | --- |
| 社区资源汇总帖（高票） | 把 EDA、基线、实验记录集中整理——本场高价值的公共材料 |
| 分割方案 | 主流为 2D/2.5D 分割网络 + 后处理（器官尺寸约束、连通域） |

## 3. 关键技巧

- **按患者/扫描分组验证**（医学影像通用纪律）。
- **部分标注的处理**：只对已标注区域计损失（masked loss）。
- **后处理约束**（最小体积、连通域、类间优先级）。
- **社区整理的资源帖**极大降低入门成本。

## 4. 可迁移性评估

- **可直接迁移**：
  - 部分标注下的 masked loss；
  - 分组验证 + 后处理约束；
  - 社区资源汇总的做法。
- 需要前提：分割框架（nnU-Net/UNet 系）。
- 不建议照搬：随机切片划分。

## 5. 对新手的关键启示

1. **分割任务的分数常在"后处理"环节拉开**（尺寸/连通性约束）。
2. 部分标注是医学数据常态，要显式处理。
3. 与 RSNA 系列、HuBMAP、CMI 对照：**医学影像分割的方法论已标准化**。

## 6. 出处

- 讨论区索引：`intel/uw-madison-gi-tract-image-segmentation/topics.md`（80 条）
- 已收录 write-up（6 篇）：
  - 1st（127 票）：https://www.kaggle.com/competitions/uw-madison-gi-tract-image-segmentation/discussion/337197
  - 1st 2.5D 部分（56 票）：https://www.kaggle.com/competitions/uw-madison-gi-tract-image-segmentation/discussion/337217
  - 社区资源汇总（140 票）：https://www.kaggle.com/competitions/uw-madison-gi-tract-image-segmentation/discussion/320060
