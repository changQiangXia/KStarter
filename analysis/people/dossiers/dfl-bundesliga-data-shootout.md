# DFL - Bundesliga Data Shootout

> `dfl-bundesliga-data-shootout` ｜ Featured ｜ 指标 DFLEventDetectionAP ｜ 530 队 ｜ 截止 2022-12-20

本页汇总该场 **1 条 ≥50 票 GM 主题帖**、**4 条断言**、**0 条高票评论**。

## GM 主题帖

| 票 | 选手 | 日期 | 主题 |
| --- | --- | --- | --- |
| 139 | [@philippsinger](https://www.kaggle.com/philippsinger) | 2022-10-14 | [Team Hydrogen: 1st place solution](https://www.kaggle.com/competitions/dfl-bundesliga-data-shootout/discussion/359932) |

## 断言（条件→动作→机制→结果）

| 选手 | 等级 | 阶段 | 动作（节选） | 出处 |
| --- | --- | --- | --- | --- |
| @philippsinger | A | 建模与训练 | 输入 1024x1024 灰度、3 帧堆叠为通道；5 个时间步各过 backbone，最后一层 3D 卷积加池化聚合，总感受野 15 帧；灰度优于彩色 | [dfl-bundesliga-data-shootout#359932-01](https://www.kaggle.com/competitions/dfl-bundesliga-data-shootout/discussion/359932) |
| @philippsinger | A | 验证设计 | 固定 4 个验证视频；local 0.857 与 public LB 强相关；最终用全量数据重训最佳模型 | [dfl-bundesliga-data-shootout#359932-03](https://www.kaggle.com/competitions/dfl-bundesliga-data-shootout/discussion/359932) |
| @philippsinger | B | 工程/流程 | 推理分辨率加 128 提升分数；单模型隔帧预测，两模型交替逐帧覆盖；后处理降假阳性 | [dfl-bundesliga-data-shootout#359932-04](https://www.kaggle.com/competitions/dfl-bundesliga-data-shootout/discussion/359932) |
| @philippsinger | C | 建模与训练 | 只选 efficientnetv2_b0 或 b1；更大 backbone 快速过拟合 | [dfl-bundesliga-data-shootout#359932-02](https://www.kaggle.com/competitions/dfl-bundesliga-data-shootout/discussion/359932) |

## 高票评论

_无 ≥10 票评论_

## 关联资产

- 深读：`analysis/deep/dfl-bundesliga-data-shootout.md`
- 结构化摘要：`notes/cv/dfl-bundesliga-data-shootout.md`
- 归档讨论区：`intel/dfl-bundesliga-data-shootout/`（主题 1 条有 ≥50 票帖，图证 0 个）
