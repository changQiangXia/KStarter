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

## 6. 轻读结论（2026-10 补）

**一句话**：本场的核心挑战是**域偏移（HPA 的 DAB 染色 → HuBMAP 的 H&E 染色）**——4th 的标题就是"染色归一化就是全部"；配合**按器官重采样到统一物理尺度 + 双流/分组建模**（肺自成一派）。

- 3rd（354683）：剔除再伪标回一批肺；**统一重采样到 HuBMAP 分辨率**（原始尺度跨 30 倍）+ 按器官加降/升采样；**CutMix 只在同器官内**；CNN 512 / SegFormer 1024（更大裁剪对 CNN 反而伤 LB）；非空掩码采样 0.5；**直方图匹配**到 H&E 参考；外部 GTEX ~140 + HPA 5.7–6.1 万/器官伪标签（集成 0.59 HuBMAP / 0.81 HPA+HuBMAP）。
- 4th（354851）：**双流**（肺单独）+ 训练时把 HPA 随机用 Reinhard/Vahadane 归一化到唯一那张 HuBMAP 测试图；不用外部数据也拿第 4。
- 2nd（354857）：重编码器 + 大分辨率（768/1024/1472 × 5 折）；coat_lite 单模最好、CNN 集成更强；**辅助预测 organ 与 pixel_size**。
- 社区：HPA/HuBMAP 兼容性质疑（78 票）、切片厚度对染色影响（56 票）、外部数据源（55 票）、Heather Couture 的域偏移鲁棒性（47 票）。

**裁决**：病理赛先做染色/协议审计；像素尺度差异要重采样到统一物理尺度并多分辨率训练；冲突子分布（肺）分组建模；外部数据非必需。

**悬案**：**1st 方案未入库**；3rd 的伪标签收益未精确量化；4th 无"不归一化"对照。

## 7. 图表证据

![各主干在 5 器官上的逐折基准](../../intel/hubmap-organ-segmentation/bodies/332941_img/01.png)

**图 1**（topic 332941）：5 折 × 5 器官 Dice——lung 普遍仅 0.18–0.25（其余 0.75–0.95），量化印证"肺是特殊子分布"。

## 8. 出处

- 讨论区索引：`intel/hubmap-organ-segmentation/topics.md`（80 条）
- 已收录 write-up（6 篇）：
  - 2nd（56 票）：https://www.kaggle.com/competitions/hubmap-organ-segmentation/discussion/354857
  - 3rd（70 票）：https://www.kaggle.com/competitions/hubmap-organ-segmentation/discussion/354683
  - 高票单折方案（259 票）：https://www.kaggle.com/competitions/hubmap-organ-segmentation/discussion/332941
  - 4th 染色归一化与往届方案汇总：见讨论区对应主题
  - 4th（50 票）：https://www.kaggle.com/competitions/hubmap-organ-segmentation/discussion/354851
  - 2nd（56 票）：https://www.kaggle.com/competitions/hubmap-organ-segmentation/discussion/354857
  - HPA/HuBMAP 数据质疑（78 票）：https://www.kaggle.com/competitions/hubmap-organ-segmentation/discussion/332714
  - 外部数据源（55 票）：https://www.kaggle.com/competitions/hubmap-organ-segmentation/discussion/333886
  - 1st（未入库，待补）：https://www.kaggle.com/competitions/hubmap-organ-segmentation/discussion/356201
- 轻读全本：`analysis/deep/hubmap-organ-segmentation.md`（Tier B 轻读：对照矩阵/裁决/证据分级/悬案 + 1 图证）
