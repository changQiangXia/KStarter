# CZII - CryoET Object Identification

> `czii-cryo-et-object-identification` ｜ Featured ｜ 指标 CZI_CryoET_ 84969 ｜ 931 队 ｜ 截止 2025-02-05

本页汇总该场 **2 条 ≥50 票 GM 主题帖**、**10 条断言**、**2 条高票评论**。

## GM 主题帖

| 票 | 选手 | 日期 | 主题 |
| --- | --- | --- | --- |
| 103 | [@christofhenkel](https://www.kaggle.com/christofhenkel) | 2025-02-06 | [1st place solution [segmentation with partly U-NET and ensembling part](https://www.kaggle.com/competitions/czii-cryo-et-object-identification/discussion/561510) |
| 68 | [@ren4yu](https://www.kaggle.com/ren4yu) | 2025-02-06 | [4th Place Solution [Source Codes & Submission Notebook Released!]](https://www.kaggle.com/competitions/czii-cryo-et-object-identification/discussion/561401) |

## 断言（条件→动作→机制→结果）

| 选手 | 等级 | 阶段 | 动作（节选） | 出处 |
| --- | --- | --- | --- | --- |
| @christofhenkel | A | 验证设计 | 7 折按 experiment 划分；每 epoch 在验证 experiment 上网格搜索类阈值；7 折后取 OOF，用其他 6 折拟合每折阈值，再平均 f4 曲线取最优阈值 | [czii-cryo-et-object-identification#561510-01](https://www.kaggle.com/competitions/czii-cryo-et-object-identification/discussion/561510) |
| @christofhenkel | A | 建模与训练 | 发现倒数第二层特征图比最后一层更准；box 回归收益可忽略；改用部分 UNet 加单像素目标加低背景权重（不用高斯热图）；深监督无大增益 | [czii-cryo-et-object-identification#561510-02](https://www.kaggle.com/competitions/czii-cryo-et-object-identification/discussion/561510) |
| @christofhenkel | A | 建模与训练 | 7 类加权 CE（β-amylase 保留为类以帮助区分 β-galactosidase）；正像素权重 256、背景 1；cosine 峰值 LR 0.001、混合精度、有效 ba | [czii-cryo-et-object-identification#561510-03](https://www.kaggle.com/competitions/czii-cryo-et-object-identification/discussion/561510) |
| @ren4yu | A | 特征与数据工程 | 作者主张加 1.0（而非讨论里的 0.5），因为圆心平均落在像素中心 (0.5,0.5)；高斯 mask 中心为 1.0，yu4u 模型 sigma 取 6 像素，tattaka  | [czii-cryo-et-object-identification#561401-01](https://www.kaggle.com/competitions/czii-cryo-et-object-identification/discussion/561401) |
| @ren4yu | A | 建模与训练 | 2D backbone 各阶段输出沿深度池化以分层聚合深度特征；换成 strided 3D 卷积会掉分；编解码之间加 3D 卷积（借鉴 contrails 3rd 方案）；高分辨率 | [czii-cryo-et-object-identification#561401-02](https://www.kaggle.com/competitions/czii-cryo-et-object-identification/discussion/561401) |
| @ren4yu | A | 建模与训练 | 输入 32×128×128，ResNetRS-50 backbone；前两阶段用平均池化把深度减半，之后用 kernel=3、stride=1、padding=1 保持深度；解码器 | [czii-cryo-et-object-identification#561401-03](https://www.kaggle.com/competitions/czii-cryo-et-object-identification/discussion/561401) |
| @ren4yu | A | 后处理 | TensorRT 转换加双 T4 多进程并行；热图用 maxpool k=7 做 NMS 找局部极大，再按粒子类型分别阈值过滤；坐标换算：像素加 0.5 到中心、减 1.0 修正偏 | [czii-cryo-et-object-identification#561401-05](https://www.kaggle.com/competitions/czii-cryo-et-object-identification/discussion/561401) |
| @christofhenkel | B | 集成与融合 | 对每个类把所有像素值排序，把 B 的值替换为 A 的同秩值（rank matching），使两者分布一致后再混合特征图并跑检测后处理 | [czii-cryo-et-object-identification#561510-04](https://www.kaggle.com/competitions/czii-cryo-et-object-identification/discussion/561510) |
| @ren4yu | B | 建模与训练 | 最终用简单 MSE 的正/负区域分别归一化后相加（balanced loss），比调整热图生成参数更有效并加速收敛 | [czii-cryo-et-object-identification#561401-04](https://www.kaggle.com/competitions/czii-cryo-et-object-identification/discussion/561401) |
| @ren4yu | B | 验证设计 | CV 只用于确认指标合理与选 checkpoint；有潜力的方法直接提交靠 LB 决策取舍；两阶段 refinement 方案 CV 好但 LB 不升 | [czii-cryo-et-object-identification#561401-06](https://www.kaggle.com/competitions/czii-cryo-et-object-identification/discussion/561401) |

## 高票评论

| 票 | 选手 | 日期 | 摘录 | 出处 |
| --- | --- | --- | --- | --- |
| 13 | @christofhenkel | 2025-02-09 | If you have specific points where I should be clearer, I am happy to edit the post and elaborate more. My aim  | [561510](https://www.kaggle.com/competitions/czii-cryo-et-object-identification/discussion/561510) |
| 12 | @christofhenkel | 2025-02-06 | for segmentation: resnet34 backbone: 0.766 resnet34 backbone + deep supervision: 0.767 effnet-b3 backbone: 0.7 | [561510](https://www.kaggle.com/competitions/czii-cryo-et-object-identification/discussion/561510) |

## 关联资产

- 深读：`analysis/deep/czii-cryo-et-object-identification.md`
- 结构化摘要：`notes/cv/czii-cryo-et-object-identification.md`
- 归档讨论区：`intel/czii-cryo-et-object-identification/`（主题 2 条有 ≥50 票帖，图证 7 个）
