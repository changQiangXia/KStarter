# RSNA 2022 Cervical Spine Fracture Detection

> `rsna-2022-cervical-spine-fracture-detection` ｜ Featured ｜ 指标 Weighted Mean Columnwise Log Loss ｜ 883 队 ｜ 截止 2022-10-27

本页汇总该场 **2 条 ≥50 票 GM 主题帖**、**7 条断言**、**0 条高票评论**。

## GM 主题帖

| 票 | 选手 | 日期 | 主题 |
| --- | --- | --- | --- |
| 179 | [@harshitsheoran](https://www.kaggle.com/harshitsheoran) | 2022-07-30 | [Explaining Data and Submission in detail](https://www.kaggle.com/competitions/rsna-2022-cervical-spine-fracture-detection/discussion/340612) |
| 59 | [@darraghdog](https://www.kaggle.com/darraghdog) | 2022-10-28 | [3rd place solution](https://www.kaggle.com/competitions/rsna-2022-cervical-spine-fracture-detection/discussion/362643) |

## 断言（条件→动作→机制→结果）

| 选手 | 等级 | 阶段 | 动作（节选） | 出处 |
| --- | --- | --- | --- | --- |
| @darraghdog | A | 特征与数据工程 | 不用骨折框，只用分割图两级信息：C1-C7 的 study 级 bbox（切片 bbox 的 rollmean max）与每切片椎骨体积比；体积比加 train 骨折标签得到切片级 | [rsna-2022-cervical-spine-fracture-detection#362643-01](https://www.kaggle.com/competitions/rsna-2022-cervical-spine-fracture-detection/discussion/362643) |
| @darraghdog | A | 特征与数据工程 | effnet-v2 预测 5 个标签（x0、y0、x1、y1、has_bbox）；用 has_bbox 概率的 z 向 rollmean 排除椎骨前后切片；整个 study 用单个 | [rsna-2022-cervical-spine-fracture-detection#362643-02](https://www.kaggle.com/competitions/rsna-2022-cervical-spine-fracture-detection/discussion/362643) |
| @darraghdog | A | 建模与训练 | Model1：用 87 个 study 分割图训椎骨比例（RMSE），乘 study 骨折标签得切片骨折标签；Model2：随机 32×3 切片窗口训三个目标（椎骨比例、切片骨折、 | [rsna-2022-cervical-spine-fracture-detection#362643-03](https://www.kaggle.com/competitions/rsna-2022-cervical-spine-fracture-detection/discussion/362643) |
| @darraghdog | A | 集成与融合 | Model3：从 Model2 载入 CNN 并冻结，仅训新 1D RNN 与注意力，用比赛指标作损失；长 study 用 torch 插值把超过 192×3 的序列压到 192； | [rsna-2022-cervical-spine-fracture-detection#362643-04](https://www.kaggle.com/competitions/rsna-2022-cervical-spine-fracture-detection/discussion/362643) |
| @harshitsheoran | B | 数据理解 | 理解 DICOM 的 ImagePositionPatient：z 轴不是时间戳而是矢状面位置，用于确定当前轴位切片在脊柱中的位置 | [rsna-2022-cervical-spine-fracture-detection#340612-01](https://www.kaggle.com/competitions/rsna-2022-cervical-spine-fracture-detection/discussion/340612) |
| @harshitsheoran | B | 特征与数据工程 | 按 NIfTI header 重排：[:, ::-1, ::-1].transpose(2, 1, 0)，得到 (num_images, height, width) 与 DICO | [rsna-2022-cervical-spine-fracture-detection#340612-02](https://www.kaggle.com/competitions/rsna-2022-cervical-spine-fracture-detection/discussion/340612) |
| @harshitsheoran | C | 数据理解 | 用分割 mask 的 unique 值判定：0 为背景、6 表示 C6、超出 7 的值对应 Th1 等；提交格式为每患者 8 行（C1-C7 + overall） | [rsna-2022-cervical-spine-fracture-detection#340612-03](https://www.kaggle.com/competitions/rsna-2022-cervical-spine-fracture-detection/discussion/340612) |

## 高票评论

_无 ≥10 票评论_

## 关联资产

- 深读：`analysis/deep/rsna-2022-cervical-spine-fracture-detection.md`
- 结构化摘要：`notes/cv/rsna-2022-cervical-spine-fracture-detection.md`
- 归档讨论区：`intel/rsna-2022-cervical-spine-fracture-detection/`（主题 2 条有 ≥50 票帖，图证 6 个）
