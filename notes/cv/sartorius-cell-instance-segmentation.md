# Sartorius - Cell Instance Segmentation

> 主题：cv ｜ 子类：— ｜ 领域：生物图像 ｜ 类别：Featured
> 截止：2022-01-XX ｜ 队伍数：2600+ ｜ 机制：代码赛 ｜ 指标：mAP（实例分割）
> 数据来源：`intel/sartorius-cell-instance-segmentation/`（80 条主题索引 + 6 篇 write-up 正文）

## 1. 任务与数据

- **预测目标**：在显微镜图像中分割出每个细胞实例（实例分割）。
- **数据形态**：显微图像 + 实例掩码；标注质量与尺度差异大。
- **构造陷阱**：
  - **掩码标注质量有限** → 冠军明确表示"掩码性能受标注质量限制，因此把重点放在检测框上"。
  - 细胞尺度差异大，需要合适的分辨率与锚框设计。

## 2. 验证方案

| 方案 | 使用者 | 说明 |
| --- | --- | --- |
| COCO mAP + 阈值调优 | 1st | 认为"高 mAP + 合适阈值"即可对应高榜分 |
| 公开基线对照 | 多队 | LiveCell 预训练 + 微调作为起点 |

## 3. 方案谱系

| 方案 | 名次 | 关键点 |
| --- | --- | --- |
| **基于检测框的实例分割**（重点投入 bbox 检测） | 1st | 掩码部分不过度投入（受标注质量限制）；与 2nd 方案思路相近 |
| 基于 Cellpose 的流程 | 3rd | 从 Detectron/LiveCell 微调起步，后转向 Cellpose |
| Mask R-CNN 系路线 | 多队 | 早期主流；U-Net 方案公开结果普遍偏低 |

## 4. 关键技巧

- **判断"哪一环决定上限"**：本场是检测框质量而非掩码精细度 → 把资源投到 bbox。
- **用成熟的预训练模型起步**（LiveCell 预训练）再微调。
- **验证指标与榜分对齐**：用 COCO mAP + 阈值搜索。
- **不要盲从公开 notebook 的结论**：社区普遍认为 U-Net 差，但 3rd 通过 Cellpose 走出了不同路线。

## 5. 可迁移性评估

- **可直接迁移**：
  - **识别瓶颈环节**（检测 vs 分割 vs 后处理），把资源集中在决定上限的环节。
  - 用领域预训练模型（显微图像 → LiveCell）做起点。
  - 阈值搜索对齐榜分。
- 需要前提：实例分割框架经验（Detectron2/Mask R-CNN/Cellpose）与 GPU。
- 不建议照搬：在标注质量受限的任务上死磕掩码精度。

## 6. 对新手的关键启示

1. **先问"这个任务的上限由什么决定"**（本场是标注质量 + 检测框）。
2. **预训练模型是起点，不是答案**。
3. **社区共识可能过时**（U-Net 之差 vs Cellpose 之路）。

## 7. 出处

- 讨论区索引：`intel/sartorius-cell-instance-segmentation/topics.md`（80 条）
- 已收录 write-up（6 篇）：
  - 1st（101 票）：https://www.kaggle.com/competitions/sartorius-cell-instance-segmentation/discussion/298869
  - 2nd（146 票）：https://www.kaggle.com/competitions/sartorius-cell-instance-segmentation/discussion/297988
  - 3rd（124 票）：https://www.kaggle.com/competitions/sartorius-cell-instance-segmentation/discussion/297984
  - 其它方案：https://www.kaggle.com/competitions/sartorius-cell-instance-segmentation/discussion/285516
