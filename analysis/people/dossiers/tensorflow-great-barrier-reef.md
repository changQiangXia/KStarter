# TensorFlow - Help Protect the Great Barrier Reef 

> `tensorflow-great-barrier-reef` ｜ Research ｜ 指标 CSIROObjectDetectionFBeta ｜ 2025 队 ｜ 截止 2022-02-14

本页汇总该场 **1 条 ≥50 票 GM 主题帖**、**4 条断言**、**2 条高票评论**。

## GM 主题帖

| 票 | 选手 | 日期 | 主题 |
| --- | --- | --- | --- |
| 130 | [@philippsinger](https://www.kaggle.com/philippsinger) | 2022-02-15 | [3rd place solution - Team Hydrogen](https://www.kaggle.com/competitions/tensorflow-great-barrier-reef/discussion/307707) |

## 断言（条件→动作→机制→结果）

| 选手 | 等级 | 阶段 | 动作（节选） | 出处 |
| --- | --- | --- | --- | --- |
| @philippsinger | A | 数据理解 | 发现训练框平均大 3px；提高推理分辨率会生成更紧的框并在 public 提分；手动缩小框同样提分，但在训练数据上无效，据此推断 public 标注更紧而 private 又不同 | [tensorflow-great-barrier-reef#307707-02](https://www.kaggle.com/competitions/tensorflow-great-barrier-reef/discussion/307707) |
| @philippsinger | A | 后处理 | 用中心点欧氏距离找轨迹并保留低置信框；把低置信框置信度提升到该轨迹最大值（0.15 到 0.9）；比 Kalman 估计新框更好，约提升 0.01 | [tensorflow-great-barrier-reef#307707-03](https://www.kaggle.com/competitions/tensorflow-great-barrier-reef/discussion/307707) |
| @philippsinger | B | 集成与融合 | 融合 5 类检测器（CenterNet 加 HRNet、FasterRCNN 加 NFNet、FCOS、EfficientDet、YOLOv5）加跟踪；平均 WBF 融合 | [tensorflow-great-barrier-reef#307707-01](https://www.kaggle.com/competitions/tensorflow-great-barrier-reef/discussion/307707) |
| @philippsinger | B | 集成与融合 | 平均 WBF（投票机制自动抑制非共识框）；另试 Optical Flow 提升仅 0.001 | [tensorflow-great-barrier-reef#307707-04](https://www.kaggle.com/competitions/tensorflow-great-barrier-reef/discussion/307707) |

## 高票评论

| 票 | 选手 | 日期 | 摘录 | 出处 |
| --- | --- | --- | --- | --- |
| 18 | @philippsinger | 2022-01-13 | I should start with competitions one month before deadline, apparently it is the time people release good solu | [300638](https://www.kaggle.com/competitions/tensorflow-great-barrier-reef/discussion/300638) |
| 11 | @philippsinger | 2022-02-16 | GAN augmentation only seems to work in papers, I also never made it work for models, they are clever enough. O | [308007](https://www.kaggle.com/competitions/tensorflow-great-barrier-reef/discussion/308007) |

## 关联资产

- 深读：`analysis/deep/tensorflow-great-barrier-reef.md`
- 结构化摘要：`notes/cv/tensorflow-great-barrier-reef.md`
- 归档讨论区：`intel/tensorflow-great-barrier-reef/`（主题 1 条有 ≥50 票帖，图证 0 个）
