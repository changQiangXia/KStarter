# HuBMAP - Hacking the Human Vasculature

> `hubmap-hacking-the-human-vasculature` ｜ Research ｜ 指标 OpenImagesObjDetectionSegmentationAP ｜ 1021 队 ｜ 截止 2023-07-31

本页汇总该场 **2 条 ≥50 票 GM 主题帖**、**9 条断言**、**0 条高票评论**。

## GM 主题帖

| 票 | 选手 | 日期 | 主题 |
| --- | --- | --- | --- |
| 82 | [@tascj0](https://www.kaggle.com/tascj0) | 2023-08-04 | [1st place solution](https://www.kaggle.com/competitions/hubmap-hacking-the-human-vasculature/discussion/429060) |
| 63 | [@ren4yu](https://www.kaggle.com/ren4yu) | 2023-08-01 | [7th Place Solution](https://www.kaggle.com/competitions/hubmap-hacking-the-human-vasculature/discussion/428295) |

## 断言（条件→动作→机制→结果）

| 选手 | 等级 | 阶段 | 动作（节选） | 出处 |
| --- | --- | --- | --- | --- |
| @tascj0 | A | 建模与训练 | EMA 模型不仅验证集更准，训练集上也更准；多数实验用 EMA 加固定学习率 | [hubmap-hacking-the-human-vasculature#429060-02](https://www.kaggle.com/competitions/hubmap-hacking-the-human-vasculature/discussion/429060) |
| @tascj0 | A | 验证设计 | dataset1 按 i 位置划分（比随机更难）；随机划分约 0.47 bbox mAP 与 0.72 segm_mAP60，i 划分约 0.43 与 0.68 | [hubmap-hacking-the-human-vasculature#429060-03](https://www.kaggle.com/competitions/hubmap-hacking-the-human-vasculature/discussion/429060) |
| @tascj0 | A | 建模与训练 | 掩码标注有两种用法：旋转时重算 bbox、或加 mask head；消融显示两种都提升（0.424 到 0.434 / 0.430 / 0.432） | [hubmap-hacking-the-human-vasculature#429060-04](https://www.kaggle.com/competitions/hubmap-hacking-the-human-vasculature/discussion/429060) |
| @tascj0 | A | 集成与融合 | bbox 用 WBF 融合 3 个 RTMDet、1 个 YOLOX-x（带掩码监督）、1 个 Mask R-CNN（每模型 2/5 折权重）；掩码由 Mask R-CNN mas | [hubmap-hacking-the-human-vasculature#429060-05](https://www.kaggle.com/competitions/hubmap-hacking-the-human-vasculature/discussion/429060) |
| @ren4yu | A | 建模与训练 | dataset1 5 折训 Mask R-CNN（Swin Transformer backbone 加 HTC RoI head）；用其给 dataset2、3 生成伪标签（每折 | [hubmap-hacking-the-human-vasculature#428295-01](https://www.kaggle.com/competitions/hubmap-hacking-the-human-vasculature/discussion/428295) |
| @ren4yu | A | 特征与数据工程 | 增广：随机 resize 768 到 1536、flip、Rot90、亮度对比、HSV；TTA：resize 1024 与 1536 加 hvflip；集成同时作用于 region | [hubmap-hacking-the-human-vasculature#428295-02](https://www.kaggle.com/competitions/hubmap-hacking-the-human-vasculature/discussion/428295) |
| @ren4yu | A | 数据理解 | 怀疑膨胀收益来自带噪 dataset2、是过拟合 LB 的手段；通过给 dataset2 同时用伪标签与膨胀标注，把膨胀与不膨胀差距从 0.1 缩到 0.02；最终带膨胀在 pub | [hubmap-hacking-the-human-vasculature#428295-04](https://www.kaggle.com/competitions/hubmap-hacking-the-human-vasculature/discussion/428295) |
| @tascj0 | B | 建模与训练 | 把优化重点放在 bbox；掩码可交给 Mask R-CNN 的 mask head 或任意语义分割模型；主模型选 RTMDet（强且训练快） | [hubmap-hacking-the-human-vasculature#429060-01](https://www.kaggle.com/competitions/hubmap-hacking-the-human-vasculature/discussion/429060) |
| @ren4yu | B | 后处理 | 后处理：膨胀、移除小 mask、移除包含肾小球区域的 mask；负结果：用测试图伪标签在提交内训练、外部数据集、YOLOv8、提交内 puzzle 都无效 | [hubmap-hacking-the-human-vasculature#428295-03](https://www.kaggle.com/competitions/hubmap-hacking-the-human-vasculature/discussion/428295) |

## 高票评论

_无 ≥10 票评论_

## 关联资产

- 深读：`analysis/deep/hubmap-hacking-the-human-vasculature.md`
- 结构化摘要：`notes/cv/hubmap-hacking-the-human-vasculature.md`
- 归档讨论区：`intel/hubmap-hacking-the-human-vasculature/`（主题 2 条有 ≥50 票帖，图证 1 个）
