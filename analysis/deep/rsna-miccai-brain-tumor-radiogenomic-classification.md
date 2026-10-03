# RSNA-MICCAI Brain Tumor Radiogenomic Classification 轻量深读（Tier B）

> 赛事：Featured ｜ 主题 cv（医学 MRI 分类）｜ 1555 队 ｜ 代码赛 ｜ 指标：ROC AUC（MGMT 甲基化预测）
> 材料基础：`digests/rsna-miccai-brain-tumor-radiogenomic-classification.md`（6 篇正文：12th 279832 / 1st 281347 / 论文 252833 / 往届金牌 252838 / DICOM→PNG 253000 / 往届数据集 253056；80 条主题索引）+ 1 张图
> 轻读时间：2026-10（Tier B B02）

## 1. 一句话重述与数字账

从脑 MRI 预测 MGMT 启动子甲基化（AUC）。样本极少、信号极弱，本场真正的考题是**与验证/提交噪声作斗争**：同一模型重跑分数几乎随机，公榜大量高分是运气/作弊。

| 关键数字 | 值 | 来源 |
| --- | --- | --- |
| 1st 的噪声量化 | 同一 EF-b0 完全相同设置重训 100 次：CV 0.53–0.62；5 折平均后仍有 0.52–0.56 区间 | 1st |
| 1st 的两阶段筛选 | 每个想法先训 **100 模型（20 次×5 折）** → 前 5 想法各训 **250 模型（50 次×5 折，换折）** 排名 | 1st |
| 1st 的最终模型 | 3D ResNet10 + BCE；**无集成**；256²、bs 8、15 epochs；1 epoch≈1'20''（3090）；top1 用 4 模态、top2 仅 T1wCE | 1st |
| "最佳中心图"技巧 | 以"脑横截面最大"的切片为中心构建 3D 输入：CV +0.01~0.02（作者唯一 100% 成功的实验） | 1st |
| 12th | Task1 分割模型（SegResNet）→ 特征对分类无帮助，放弃；3D DenseNet121/169 × 每模态 × 5 折；val loss 0.66–0.67 的"幸运跑"才对应 AUC>0.6 | 12th |
| 事件 | DICOM→PNG 资源帖 369 票；Fake Accounts/Cheating 107 票；"The real winner…" 100 票 | 主题索引 |

## 2. 逐方案对照矩阵

| 维度 | 1st | 12th |
| --- | --- | --- |
| 模型 | 3D ResNet10（无集成） | 3D DenseNet121/169（每模态×5 折） |
| 模态 | 4 模态（top2 为 T1wCE-only）；多数模型去掉 T2w | FLAIR/T1w/T1wCE/T2w 分别训练 |
| 输入技巧 | 最佳中心图（最大脑截面为中心） | 去空切片+按最长轴 resize 到 144³ |
| 验证 | 承认没有可靠验证；靠 100/250 模型的均值排序 | 5 折按 MGMT 分层；"重跑直到 lucky" |
| 分割辅助 | 未用 | 尝试 SegResNet → 特征无用，弃 |
| 结果 | **1st**（自述"公榜 0.5–0.6 却拿第一"） | 12th |

## 3. 共识、分歧与裁决

### 共识一：数据小+信号弱 → 验证噪声是第一敌人

1st：同设置重跑 CV 0.53–0.62，任何"验证策略"都不可靠；12th：val loss 0.66–0.67 的幸运跑才相关；公榜上"随机预测也能 0.7+"。**裁决**：在这种赛制里，**单次训练结果无信息量**；必须用大规模重复（几十~几百次）估计均值/方差，并以方差而非单点分数做决策。置信度：高。

### 共识二：简单模型 + 少特征/少模态反而更稳

1st 的冠军模型是其"最早的简单 baseline"：ResNet10、BCE、无集成、无复杂增广；深网/大模型失败。12th 的 DenseNet 也只在"幸运跑"上到 0.6。**裁决**：小数据下大模型只是把噪声拟合得更彻底；选容量匹配的简单 3D CNN。置信度：高。

### 共识三：公榜不可信，私榜 shakeup 是结构性的

1st 事前判断"大多数公榜高分是随机，私榜必崩"并据此把预算压到 2 周；"random predictions 0.7+"帖；作弊/假账号帖（107 票）。**1st 最终靠"忘记选提交、自动选公榜最好的两个"夺冠**（运气成分的极端例证）。**裁决**：此类比赛应把目标定为"不被 shakeup 甩掉"，而不是追公榜。置信度：高。

### 分歧一：集成 vs 单模

1st：集成无增益、换折分数完全变；12th：大量单模态模型（预测相关性低）用于稳健性。**裁决**：由于噪声主导，集成的期望增益被方差吞掉；1st 的"简单单模 + 重复平均"与 12th 的"多模型平均"本质都是**在重复维度上平均噪声**，不是传统集成收益。置信度：中高。

### 分歧二：分割（Task1）是否帮助分类（Task2）

12th 认真做了 SegResNet 分割，但特征/掩码通道对分类无帮助，遗憾放弃；1st 未做。**裁决**：本场分割与分类信号不共享（肿瘤位置 ≠ 甲基化状态），分割辅助未证实。置信度：中。

### 事实：模态选择有信息（T1wCE/FLAIR/四模态；T2w 常被弃）

1st 的 top1=4 模态、top2=T1wCE-only，且 >50% 最终模型不含 T2w；12th 的单模态分数 T2w 反而偶有亮点。**裁决**：模态的价值需要按"重复实验均值"评估，单次分数不可作依据。置信度：中。

## 4. 证据分级

| 断言 | 等级 | 说明 |
| --- | --- | --- |
| 1st 的噪声量化与两阶段 250 模型筛选 | 自述（细节具体） | 中高 |
| 1st 的最佳中心图 +0.01~0.02 | 自述（唯一成功实验） | 中 |
| 12th 的逐折 AUC 与损失相关性 | 自述表格 | 中高 |
| 公榜随机性/作弊 | 多帖 + 1st 的经历 | 高（事实层面） |
| 分割对分类无帮助 | 12th 的失败记录 | 中 |

## 5. 悬案与缺口（登记）

- 2nd–11th 方案未收录；**Fake Accounts In Competition（269396，107 票）**的处置与 "The real winner…"（100 票）未入库——本场治理问题严重；MRI 拍摄方法差异（252843，99 票）也未细读。
- 数据集规模/官方基线未在材料中给全；AUC 的最终分数与 shakeup 幅度未量化。
- 1st 的 8 个初始想法清单只给了一半；"最佳中心图"为何有效的机制解释缺失。

## 6. 图表证据

![12th 的预测相关性矩阵](../../intel/rsna-miccai-brain-tumor-radiogenomic-classification/bodies/279832_img/01.png)

**图 1**（topic 279832）：各模态/骨干的预测相关性矩阵（多为 0.0–0.48），与 MGMT 的相关最高约 0.33。**信号弱 + 模型间低相关**的可视化证据。

## 7. 出处

- 12th（279832）：https://www.kaggle.com/competitions/rsna-miccai-brain-tumor-radiogenomic-classification/discussion/279832
- 1st（281347）：https://www.kaggle.com/competitions/rsna-miccai-brain-tumor-radiogenomic-classification/discussion/281347
- 论文帖（252833）：https://www.kaggle.com/competitions/rsna-miccai-brain-tumor-radiogenomic-classification/discussion/252833
- 往届金牌（252838）：https://www.kaggle.com/competitions/rsna-miccai-brain-tumor-radiogenomic-classification/discussion/252838
- DICOM→PNG（253000）：https://www.kaggle.com/competitions/rsna-miccai-brain-tumor-radiogenomic-classification/discussion/253000
- 往届数据集（253056）：https://www.kaggle.com/competitions/rsna-miccai-brain-tumor-radiogenomic-classification/discussion/253056
- 未收录正文：269396（作弊账号）、252843（MRI 拍摄差异）、252838（往届金牌索引）
