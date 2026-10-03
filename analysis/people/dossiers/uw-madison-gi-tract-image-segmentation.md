# UW-Madison GI Tract Image Segmentation 

> `uw-madison-gi-tract-image-segmentation` ｜ Research ｜ 指标 Dice3DHausdorff ｜ 1548 队 ｜ 截止 2022-07-14

本页汇总该场 **1 条 ≥50 票 GM 主题帖**、**3 条断言**、**1 条高票评论**。

## GM 主题帖

| 票 | 选手 | 日期 | 主题 |
| --- | --- | --- | --- |
| 162 | [@yiheng](https://www.kaggle.com/yiheng) | 2022-05-17 | [[LB 0.877] A 3D solution with MONAI](https://www.kaggle.com/competitions/uw-madison-gi-tract-image-segmentation/discussion/325646) |

## 断言（条件→动作→机制→结果）

| 选手 | 等级 | 阶段 | 动作（节选） | 出处 |
| --- | --- | --- | --- | --- |
| @yiheng | B | 建模与训练 | 3D UNet 基线：输入 patch (160,160,80)（RandSpatialCrop）；v1 用 dice+ce loss | [uw-madison-gi-tract-image-segmentation#325646-01](https://www.kaggle.com/competitions/uw-madison-gi-tract-image-segmentation/discussion/325646) |
| @yiheng | B | 建模与训练 | 演进链：224x224x80 微调加推理 0.8970 加 public 0.840；dice+bce 0.9108 / 0.857；多标签大 UNet 0.9024 / 0.86 | [uw-madison-gi-tract-image-segmentation#325646-02](https://www.kaggle.com/competitions/uw-madison-gi-tract-image-segmentation/discussion/325646) |
| @yiheng | B | 验证设计 | 用同一数据划分（awsaf49）对比：2D 与 3D 模型的 local dice 与 LB 分数可比 | [uw-madison-gi-tract-image-segmentation#325646-03](https://www.kaggle.com/competitions/uw-madison-gi-tract-image-segmentation/discussion/325646) |

## 高票评论

| 票 | 选手 | 日期 | 摘录 | 出处 |
| --- | --- | --- | --- | --- |
| 10 | @yiheng | 2022-06-06 | How to reproduce (roughly) the training of 0.868 LB model (mentioned in update 3): Using the training pipeline | [325646](https://www.kaggle.com/competitions/uw-madison-gi-tract-image-segmentation/discussion/325646) |

## 关联资产

- 深读：`analysis/deep/uw-madison-gi-tract-image-segmentation.md`
- 结构化摘要：`notes/cv/uw-madison-gi-tract-image-segmentation.md`
- 归档讨论区：`intel/uw-madison-gi-tract-image-segmentation/`（主题 1 条有 ≥50 票帖，图证 0 个）
