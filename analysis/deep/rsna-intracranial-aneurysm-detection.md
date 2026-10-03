# RSNA Intracranial Aneurysm Detection 轻量深读（Tier B）

> 赛事：Featured ｜ 主题 cv（3D 医学影像，14 标签多标签分类）｜ 1147 队 ｜ 代码赛 ｜ 指标：Mean Weighted Columnwise AUCROC
> 材料基础：`digests/rsna-intracranial-aneurysm-detection.md`（3+ 篇正文：1st 611846 / 9th 611908 / 5th 611849 / 3rd 611856 / 4th 611893 / 临床背景 591648；80 条主题索引）+ 30+ 张图
> 轻读时间：2026-10（Tier B B06 收官）

## 1. 一句话重述与数字账

从头部 CTA/MRA/MRI 体数据中判断"是否存在颅内动脉瘤"并给出 **13 个解剖位置**的概率（14 个独立二分类，指标是按列加权的 AUC）。真正的考点是**"用血管结构当先验，把巨大体数据压成一个位置感知的小 ROI 分类问题"**——血管分割/检测决定下限，ROI 分类器的位置建模决定上限。

| 关键数字 | 值 | 来源 |
| --- | --- | --- |
| 1st（611846） | 三段式 coarse-to-fine：① **nnU-Net 粗定位**（1mm 间距、3 组血管区、Dice+CE）扫全图 → DBSCAN 去散点 → 以最大簇中心裁 140³ mm ROI；② 两个 nnU-Net 细分割（0.80×0.45×0.44mm，**Dice+CE+SkeletonRecall / Tversky+CE+SkeletonRecall(权重 3)**），仅在前景做**左-右镜像增强**（保留解剖不对称）；③ **ROI 分类器**（128×256×256）——backbone 直接用**预训练于血管分割的 nnU-Net**（比 timm 2.5D/3D 更准更快），简化解码器末块；**辅助任务：用解码器特征重建每个动脉瘤位置半径 5 像素的球**；**Vessel Region-Masked Pooling** 按 13 个血管掩码各取特征 + 全局 GAP → **Location-Aware Transformer** 建模位置间关系 → MLP；另有"整体存在性"头（全血管掩码并集池化）。**损失权重 1.0（球分割）/0.1（13 位置）/0.05（存在性）**——分类权重过大会过拟合；EMA + 4 折集成 + 左右翻转 TTA；失败兜底回退到 OOF 均值；处理时间：分割 10.65s/序列、训练 nnU-Net 14h（4090） | 611846 |
| 3rd（611856） | 两段：**YOLOv8n/m 检测血管区**（用矢状/冠状 MIP 生成的 2D axis-aligned 框，验证 mAP@0.5 >0.95；理由：动脉瘤在轴位 XY 上位置相对固定）→ 固定 3D 裁剪（90³ 或 120³ mm）→ 3D ResNet-18（timm-3d）+ **在特征图上做 14 类分类**（而非整卷池化）；默认 128³ 只得到 4×4×4 特征图、效果差 → **把部分卷积 stride 从 2 改 1** 以获得更大特征图 | 611856 |
| 4th（611893） | 14 天冲刺；分割模型学不动（Dice 卡 0.6）→ 改为 **DINOv3 ViT 回归 ROI 框坐标**（输入每患者 48 张等距切片 48×1×128×128，输出 x1/x2/y1/y2），保留 95%+ 动脉瘤位置；分类数据 54.5 万样本、正例仅 2.2k（1:250），14 标签 → 正例率约 1/1700 | 611893 |
| 9th（611908） | 三路互补：**YOLO 2.5D**（把切片 i−1/i/i+1 当 RGB；YOLOv11m 与 timm 底座自定义 YOLO）+ **3D CenterNet（2D EffNetV2-s 提取器）** + 三个元分类器（LGBM/XGB/CatBoost），最终平均；**13 个位置当作 13 个检测类**；**不做 Z 轴重采样**的 2.5D 反而 +0.02 CV（与直觉相反） | 611908 |
| 5th（611849） | 2.5D [t−1,t,t+1]；基于 host 的动脉瘤质心 ±10 切片**手工标注检测框**；YOLOv11x@1280 训练 5 折；公开全套代码 | 611849 |
| 数据侧 | 多帧 DICOM 问题（40 票）、血管分割与 NIfTI 方向相反（39 票）、两次数据更新（30/27 票）、提交变慢（33 票）——数据质量与运行时是本次额外战场 | 社区 |

## 2. 逐方案对照矩阵

| 维度 | 1st | 3rd | 4th | 9th | 5th |
| --- | --- | --- | --- | --- | --- |
| 定位方式 | **nnU-Net 分割 + DBSCAN ROI** | YOLOv8 检测（MIP 框） | **ViT 回归 ROI 坐标** | YOLO 2.5D + 3D CenterNet | 手工框 + YOLOv11x |
| 分类器 | nnU-Net backbone + 掩码池化 + Transformer | 3D ResNet-18（逐特征图分类） | ViT/DINOv3 | 元分类器集成 | YOLO 检测即分类 |
| 关键设计 | 辅助球重建（权重 1.0）+ 位置感知 | 检测框 → 大特征图 | 大 ROI 保召回 | 2.5D 不做 Z 重采样 | 质心 ±10 切片人工标注 |
| 定位精度 | 高（分割级） | mAP@0.5 >0.95 | 保留 95%+ | — | — |

## 3. 共识、分歧与裁决

### 共识一：先定位/分割，再分类（全员）

动脉瘤只占极小体素比例且位置固定于血管；1st 的三级分割、3rd 的 YOLO 检测、4th 的 ROI 回归、9th/5th 的检测框架都是同一思路。**裁决**：3D 医学影像的多标签分类应当拆成"定位 → 局部判别"两段；端到端整卷分类在样本量/显存约束下不可行。置信度：高。

### 共识二：位置信息要显式建模（1st/3rd/9th）

1st 用 13 个血管掩码分别池化 + Location-Aware Transformer；3rd 把 14 类头挂在特征图上（保留空间对应）；9th 把 13 个位置当作 13 个检测类。**裁决**：当标签是"解剖位置"时，模型结构必须保留空间/位置对应关系，不能只做全局池化。置信度：高。

### 共识三：极不平衡 + 弱信号 → 用辅助任务/检测式标签（1st/4th/5th）

正例率低至 1/250（4th）到 1/1700（14 标签）；1st 用"重建动脉瘤球"辅助任务（权重 1.0 高于分类）避免过拟合；5th 手工补标注检测框；9th 用元分类器。**裁决**：正例稀少时，"辅助定位任务 + 检测式监督"比直接加权 BCE 更有效；分类损失权重要压低。置信度：高（1st 有明确权重实验）。

### 分歧一：分割 vs 检测

1st/3rd 走分割/检测 ROI；4th 直接回归 ROI 坐标；9th 用 YOLO+CenterNet。**裁决**：若分割模型能在时限内训好（1st 用 1000 epoch/14h），分割提供的掩码是分类器最强的结构性先验；否则 ROI 回归（4th）是更省时的替代。置信度：中高。

### 分歧二：Z 轴要不要重采样

9th 明确"不做 Z 轴重采样的 2.5D 反而 +0.02 CV"（他们花 1–2 周做 Z resize 结果更差）；1st 则把"模拟厚层"作为增强、并按间距统一处理。**裁决**：各向异性数据的"对齐 vs 忽略"需要实验裁决，直觉不可靠；把间距差异当增强是更稳的做法。置信度：中。

### 事件：数据质量与运行时是隐形战场（社区）

多帧 DICOM、方向反了的血管分割、两次数据更新、提交变慢——都被大量讨论；1st 直接剔除约 60 个问题序列并实现"异常兜底回退 OOF 均值"。**裁决**：医学影像赛要预留"数据清洗 + 失败兜底 + 推理时延"的工程量（1st 的分割单序列 10.65s，需在 2×T4 上跑完全部测试）。置信度：高。

## 4. 证据分级

| 断言 | 等级 | 说明 |
| --- | --- | --- |
| 1st 的完整管线、损失权重与耗时 | 自述 + 6 张架构图 | 高 |
| 3rd 的 YOLO mAP>0.95 与 stride 修改 | 自述 + 图 | 中高 |
| 4th 的 ROI 回归与 1:250 正例率 | 自述（细节完整） | 中高 |
| 9th 的 2.5D 无 Z 重采样 +0.02 | 自述（单队反直觉结论） | 中 |
| 数据质量/运行时问题 | 多条高票讨论 | 高（现象） |

## 5. 悬案与缺口（登记）

- 2nd/6th–8th 的方案未入库；临床背景帖（90 票）与数据更新帖未细读；
- 1st 的 13 位置 Transformer 具体超参与 4 折集成的逐项消融未给；
- 3rd 的 3D ResNet 多分辨率/多尺度集成细节未读完；
- 归档 30+ 张图：1st 的 6 张（分割流程、损失、模型总览、掩码池化、Transformer、朝向校正）为核心图证。

## 6. 图表证据

![1st 的 ROI 分类器结构](../../intel/rsna-intracranial-aneurysm-detection/bodies/611846_img/03.png)

**图 1**（topic 611846）：ROI 体数据（1×128×256×256）过 **nnU-Net 分割预训练骨干**；13 个血管掩码（13×1×128×256×256）与解码器特征做 **Vessel Region-Masked Pooling**（13×64）→ **Location-Aware Transformer**（13×96）→ 位置分类头（13 输出）；另一路用掩码并集 + GAP 特征做"存在性"头；辅助分支输出半径 5 像素的动脉瘤球（图中紫色体）。

## 7. 出处

- 1st（611846）：https://www.kaggle.com/competitions/rsna-intracranial-aneurysm-detection/discussion/611846
- 9th（47 票）：https://www.kaggle.com/competitions/rsna-intracranial-aneurysm-detection/discussion/611908
- 5th（54 票，含代码）：https://www.kaggle.com/competitions/rsna-intracranial-aneurysm-detection/discussion/611849
- 3rd（46 票）：https://www.kaggle.com/competitions/rsna-intracranial-aneurysm-detection/discussion/611856
- 4th（44 票）：https://www.kaggle.com/competitions/rsna-intracranial-aneurysm-detection/discussion/611893
- 临床背景（90 票）：https://www.kaggle.com/competitions/rsna-intracranial-aneurysm-detection/discussion/591648
