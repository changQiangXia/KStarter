# HuBMAP + HPA - Organ Segmentation

> 主题：cv ｜ 子类：— ｜ 领域：医疗影像（病理）｜ 类别：Research
> 截止：2022-XX-XX ｜ 队伍数：1000+ ｜ 机制：代码赛 ｜ 指标：Dice（多器官分割）
> 数据来源：`intel/hubmap-organ-segmentation/`（80 条主题索引 + 6 篇 write-up 正文）

## 1. 任务与数据

- 预测目标：在病理切片中**分割多个器官/组织结构**（多类别语义分割）。
- 数据形态：超大病理图像（WSI）+ 掩码；多中心、多器官（不同染色与形态差异极大）。
- 构造陷阱：
  - **染色差异（stain variation）** 是跨中心泛化的主要障碍；
  - WSI 需切块 + 拼接；
  - 不同器官的结构差异要求模型足够通用。

## 2. 方案谱系

| 方案 | 名次 | 关键点 |
| --- | --- | --- |
| 单折 0.81 的方案（高票） | 社区 | 单折即可达到较高水平（与 4th 的结论一致：**数据标准化比模型更重要**） |
| **染色归一化（Stain Normalization）** | 4th | 标题即结论："**Stain Normalization is all you need**" |
| 多团队方案 | 2nd / 3rd | 3rd 团队同样记录了对乌克兰战事的致谢 |
| 往届 HuBMAP 方案汇总 | 社区 | 系列赛经验复用 |

## 3. 关键技巧

- **染色归一化**是病理图像跨中心任务的第一优先级（4th 的标题结论）。
- **切块 + 拼接**处理 WSI。
- **往届系列方案复用**（社区汇总帖）。
- 单折验证也可行（当数据规模足够、标准化到位时）。

## 4. 可迁移性评估

- **可直接迁移**：
  - **病理图像的染色归一化**（跨中心任务必备）；
  - WSI 的切块流程；
  - 系列赛经验复用。
- 需要前提：病理图像工具链。
- 不建议照搬：不做标准化直接训练（跨中心泛化会崩）。

## 5. 对新手的关键启示

1. **数据标准化（如染色归一化）常比模型选择更重要**（本场 4th 的标题就是结论）。
2. 与 UBC-OCEAN、RSNA 系列对照：**病理/医学影像的第一优先级是"消除采集差异"**。
3. 系列赛的往届方案汇总帖是高效起点。

## 6. 出处

- 讨论区索引：`intel/hubmap-organ-segmentation/topics.md`（80 条）
- 已收录 write-up（6 篇）：
  - 2nd（56 票）：https://www.kaggle.com/competitions/hubmap-organ-segmentation/discussion/354857
  - 3rd（70 票）：https://www.kaggle.com/competitions/hubmap-organ-segmentation/discussion/354683
  - 高票单折方案（259 票）：https://www.kaggle.com/competitions/hubmap-organ-segmentation/discussion/332941
  - 4th 染色归一化与往届方案汇总：见讨论区对应主题
