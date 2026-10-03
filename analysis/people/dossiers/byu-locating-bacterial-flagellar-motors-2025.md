# BYU - Locating Bacterial Flagellar Motors 2025

> `byu-locating-bacterial-flagellar-motors-2025` ｜ Research ｜ 指标 BYU_BioPhysics_91249 ｜ 1136 队 ｜ 截止 2025-06-04

本页汇总该场 **2 条 ≥50 票 GM 主题帖**、**6 条断言**、**0 条高票评论**。

## GM 主题帖

| 票 | 选手 | 日期 | 主题 |
| --- | --- | --- | --- |
| 147 | [@brendanartley](https://www.kaggle.com/brendanartley) | 2025-03-25 | [More Motor Annotations](https://www.kaggle.com/competitions/byu-locating-bacterial-flagellar-motors-2025/discussion/569921) |
| 146 | [@brendanartley](https://www.kaggle.com/brendanartley) | 2025-06-05 | [1st Place - 3D U-Net + Quantile Thresholding](https://www.kaggle.com/competitions/byu-locating-bacterial-flagellar-motors-2025/discussion/583143) |

## 断言（条件→动作→机制→结果）

| 选手 | 等级 | 阶段 | 动作（节选） | 出处 |
| --- | --- | --- | --- | --- |
| @brendanartley | A | 验证设计 | 4 折划分；local CV 与 LB 强相关到约 0.93，之后改用 public LB 做验证；且必须配合分位数阈值才能得到可靠的 LB 反馈 | [byu-locating-bacterial-flagellar-motors-2025#583143-01](https://www.kaggle.com/competitions/byu-locating-bacterial-flagellar-motors-2025/discussion/583143) |
| @brendanartley | A | 工程/流程 | 匹配 patch 高宽、只沿深度滑窗：快 4 倍；用高 overlap 0.875 与更多 TTA；边缘预测用 roi_weight_map 降权（中间 40% 权重 1.0，其余 | [byu-locating-bacterial-flagellar-motors-2025#583143-04](https://www.kaggle.com/competitions/byu-locating-bacterial-flagellar-motors-2025/discussion/583143) |
| @brendanartley | A | 后处理 | 按 tomogram 的 max 预测值排名做分位数阈值：去掉最低分位；在 public LB 上调参 | [byu-locating-bacterial-flagellar-motors-2025#583143-05](https://www.kaggle.com/competitions/byu-locating-bacterial-flagellar-motors-2025/discussion/583143) |
| @brendanartley | B | 数据理解 | 数据集：1617 个 motor 标注、1288 个 tomograms、来自 CZII 的 62 个数据集；作者公开可视化与预处理管线 | [byu-locating-bacterial-flagellar-motors-2025#569921-01](https://www.kaggle.com/competitions/byu-locating-bacterial-flagellar-motors-2025/discussion/569921) |
| @brendanartley | B | 特征与数据工程 | 用高斯热图做标签并把热图分辨率降 8 倍（借鉴 CZII 方案） | [byu-locating-bacterial-flagellar-motors-2025#583143-02](https://www.kaggle.com/competitions/byu-locating-bacterial-flagellar-motors-2025/discussion/583143) |
| @brendanartley | B | 建模与训练 | SmoothBCE 三项：主分割头 + 倒数第二特征图深监督 + 主头上的 max-pool 损失（kernel 与 stride 均为 4） | [byu-locating-bacterial-flagellar-motors-2025#583143-03](https://www.kaggle.com/competitions/byu-locating-bacterial-flagellar-motors-2025/discussion/583143) |

## 高票评论

_无 ≥10 票评论_

## 关联资产

- 深读：`analysis/deep/byu-locating-bacterial-flagellar-motors-2025.md`
- 结构化摘要：`notes/cv/byu-locating-bacterial-flagellar-motors-2025.md`
- 归档讨论区：`intel/byu-locating-bacterial-flagellar-motors-2025/`（主题 2 条有 ≥50 票帖，图证 5 个）
