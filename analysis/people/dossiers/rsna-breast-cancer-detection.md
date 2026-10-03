# RSNA Screening Mammography Breast Cancer Detection

> `rsna-breast-cancer-detection` ｜ Featured ｜ 指标 Probabilistic F-Score Beta (Micro) ｜ 1687 队 ｜ 截止 2023-02-27

本页汇总该场 **1 条 ≥50 票 GM 主题帖**、**4 条断言**、**0 条高票评论**。

## GM 主题帖

| 票 | 选手 | 日期 | 主题 |
| --- | --- | --- | --- |
| 84 | [@christofhenkel](https://www.kaggle.com/christofhenkel) | 2023-02-28 | [4th place solution](https://www.kaggle.com/competitions/rsna-breast-cancer-detection/discussion/391208) |

## 断言（条件→动作→机制→结果）

| 选手 | 等级 | 阶段 | 动作（节选） | 出处 |
| --- | --- | --- | --- | --- |
| @christofhenkel | A | 数据工程 | 统一预处理与缩放：DICOM windowing、线性 window 加速、min-filter CNN 粗裁乳房区域、PIL lanczos 缩放优于 cv2、统一缩到 1152 | [rsna-breast-cancer-detection#391208-01](https://www.kaggle.com/competitions/rsna-breast-cancer-detection/discussion/391208) |
| @christofhenkel | A | 特征与数据工程 | 增广在缩放前做：vflip、hflip、transpose、shift、scale、rotate、grid distortion、affine；缩放后只做 grid shuffle | [rsna-breast-cancer-detection#391208-02](https://www.kaggle.com/competitions/rsna-breast-cancer-detection/discussion/391208) |
| @christofhenkel | A | 建模与训练 | 类型1：乳房级 1D-CNN + CNN backbone（辅助分割损失加快收敛；stage1 9 epochs + stage2 冻 backbone 2 epochs；线性层  | [rsna-breast-cancer-detection#391208-03](https://www.kaggle.com/competitions/rsna-breast-cancer-detection/discussion/391208) |
| @christofhenkel | A | 集成与融合 | 7 个全量单 seed 模型：EffNet v2s/v2m/b3/b4/b5 + 1D-CNN，SE-ResNext50 + deit-tiny，ConvNext_tiny + d | [rsna-breast-cancer-detection#391208-04](https://www.kaggle.com/competitions/rsna-breast-cancer-detection/discussion/391208) |

## 高票评论

_无 ≥10 票评论_

## 关联资产

- 深读：`analysis/deep/rsna-breast-cancer-detection.md`
- 结构化摘要：`notes/cv/rsna-breast-cancer-detection.md`
- 归档讨论区：`intel/rsna-breast-cancer-detection/`（主题 1 条有 ≥50 票帖，图证 4 个）
