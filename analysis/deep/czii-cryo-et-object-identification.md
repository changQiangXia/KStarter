# CZII CryoET Object Identification 轻量深读（Tier B）

> 赛事：Featured ｜ 主题 cv（3D 冷冻电镜粒子识别）｜ 931 队 ｜ 代码赛 ｜ 指标：F-beta 型（`CZI_CryoET_84969`）｜ 500 个扫描 × 12 小时限时（≈1.5 分钟/扫描）
> 材料基础：`digests/czii-cryo-et-object-identification.md`（6 篇正文：1st OD 561440 + 1st 分割 561510 / 2nd 561568 / 3rd 561417 / 4th 561401 / 9th 561431 等；80 条主题索引）+ 11 张图
> 轻读时间：2026-10（Tier B B08）

## 1. 一句话重述与数字账

在 3D CryoET 体数据里找五类粒子（apo-ferritin/beta-galactosidase/ribosome/thyroglobulin/VLP）。真正的考点是**"分割 vs 点检测的路线选择 + 推理时延工程"**：1st 的冠军是**分割模型 + 点检测模型两条路线合并**（单独各只到 Top-5），而点检测路线的关键收益来自"降低输出分辨率 + TensorRT"这类纯工程手段。

| 关键数字 | 值 | 来源 |
| --- | --- | --- |
| 1st-OD（561440，BloodAxe） | 基线是 SegResNet 热图分割（0.740 LB）→ 主动放弃改做**anchor-free 点检测**（SegResNet/DynUnet + 自定义点检测头）；用 **OKS 式点-点 IoU**（`exp(-mse/(2r²))`）当 IoU 代理；损失仿 PP-YOLO（Top-K 分配 + varifocal 分类 + IoU 距离回归）；**输出 stride=2 的类别图与偏移图**（stride1 仅好 0.002 但慢一半；stride2+4 双头无额外收益；大颗粒自然迁移到 stride4）；4×3090 单折 2 小时、单折首提交 0.752 LB；**TensorRT 200% 加速 + 2×T4 并行**；滑窗 192×128×128、1×9×9 块、边界降权加权平均；后处理：CenterNet 式 NMS → top-16K → 逐类置信度阈值 → 贪心 NMS → 像素转 Å；集成 5×OD-SegResNet + 5×OD-DynUnet；**1st 与队友各是 Top-5，合并后直接第 1** | 561440 |
| 1st-分割（561510，Christof） | 7 折（按 experiment 切）；逐类阈值网格搜索 + 用 OOF 交叉拟合阈值曲线再取最优；标准归一化（630×630×184）；MONAI 增强 + 自研 MixUp；核心发现：**倒数第二层特征图比最后一层更准**（"部分 U-Net"即可）、**框回归几乎无增益**（同类型粒子大小一致）、用低类权 + 单像素目标就无需高斯热图；FlexibleUnet(resnet34/effnet-b3)；**6 个检查点 <2 小时即可拿 LB 第 7**；不用任何外部/模拟数据 | 561510 |
| 2nd（561568） | 轻量分割模型集成（873K–14.2M 参数）：UNet3D/VoxResNet/VoxHRNet/SegResNet/DenseVNet；**大模型易过拟合、更差**；发现 MONAI UNet 的 **InstanceNorm3d + PReLU 比 BatchNorm3d + ReLU 训练更稳定**（5 次对照）；CC3D 求质心 + 按体素数过滤小簇；按公榜选模型 | 561568 |
| 3rd（561417） | 3D UNet + CE（7 类粒子）+ cc3d 后处理；res101 骨干 4 折（7 KF）集成；**公私榜同为 0.783** | 561417 |
| 4th（561401） | 热图法（姿态估计思路）；2.5D-UNet（2D 骨干 + 深度方向池化，**优于 strided 3D 卷积**）；σ=6 或按粒子尺寸；**坐标换算应加 1.0 而不是 0.5**（像素中心 vs 角点）；承认 CV-LB 不相关 → 用 LB 做方法取舍 | 561401 |
| 9th（561431） | 3D ConvNeXt 类分割 + 尽量多模型集成；**按粒子类别调整掩码半径**（如 r/2、r/3）→ 公榜 +0.02~0.04；CC3D + DBSCAN 净化质心 | 561431 |
| 社区 | "卡在 benchmark.csv 以下读这篇"（98 票）、"用合成数据构建 CryoET 基础模型（lb 0.748）"（81 票）、"本地 CV 0.35–0.75 但提交几乎 0 分"（38 票）、"网格原点其实是第一个像素的中心"（37 票） | 社区 |

## 2. 逐方案对照矩阵

| 维度 | 1st-OD | 1st-分割 | 2nd | 4th | 9th |
| --- | --- | --- | --- | --- | --- |
| 路线 | 点检测（OKS 代理 IoU） | 部分 U-Net 分割 | 轻量分割集成 | 2.5D 热图 | 3D ConvNeXt 分割 |
| 关键工程 | **stride2 + TensorRT + 双 T4** | 部分 U-Net + OOF 阈值 | InstanceNorm+PReLU | 深度池化替代 3D 卷积 | 按类调掩码半径 |
| 后处理 | CenterNet NMS/逐类阈值 | 逐类阈值曲线 | CC3D + 小簇过滤 | 坐标 +1.0 | CC3D + DBSCAN |
| 结论 | 与分割合并→1st | 与检测合并→1st | 2nd | 4th | 9th |

## 3. 共识、分歧与裁决

### 共识一：这是一场"推理时延"比赛（1st-OD/4th/2nd）

12 小时跑 500 个扫描 ≈ 1.5 分钟/扫描；1st 用 stride2 输出（50% 提速）+ TensorRT（200%）+ 双 GPU 并行才装得下 10 模型集成；4th 用 2.5D 骨干也是为了吞吐。**裁决**：限时推理的 3D 赛要把"模型吞吐"当一等指标；降低输出分辨率是收益最高的工程手段。置信度：高。

### 共识二：分割与点检测是互补路线，冠军是两者的合并（1st 两篇）

1st 自述"我单独是 Top-5、队友单独也是 Top-5，合并后立刻第 1"；1st-OD 也承认分割是最容易实现且强的基线（0.740）。**裁决**：当两条范式的错误模式不同（高斯热图 vs 点回归），跨范式集成是最有效的提升方式。置信度：高。

### 共识三：小模型 + 好损失 > 大模型（1st-分割/2nd）

1st-分割："相对小的模型表现很好，**损失设计最重要**"（6 个检查点 <2h 到第 7）；2nd："大参数量易过拟合，反而更差"，且发现 InstanceNorm+PReLU 更稳。**裁决**：3D 医学小数据赛优先把损失/归一化调对，深度与宽度是次要变量。置信度：高。

### 分歧一：目标表示（高斯热图 vs 单像素 vs 点检测）

1st-分割发现"热图不必要，低类权 + 单像素目标即可"，并把监督放在倒数第二层；1st-OD 直接回归点 + 偏移；4th 仍用 σ=6 的高斯热图；9th 用半径可调的掩码。**裁决**：三种都能进前列；热图的 σ/半径是需要按类调的超参（9th 的 +0.02~0.04 即此项），而"部分 U-Net（倒数第二层）"是低成本等价替代。置信度：中高。

### 分歧二：CV 还能不能用

4th 明确"CV-LB 不相关，只用 CV 选检查点、用 LB 决定方法"；1st-分割用 7 折 f4 均值（与 LB 有良好相关）并做 OOF 阈值重标定；2nd 按公榜选模型。**裁决**：本场 CV 与 LB 的关系依赖切分（按 experiment vs 随机）；切分方式本身要先验证相关性。置信度：中高。

### 事件：坐标系细节（4th/37 票帖）

"粒子坐标 +1.0 还是 +0.5""网格原点是首像素中心"——直接影响定位精度与本地-榜一致性（38 票帖：本地 CV 0.35–0.75 但提交近 0）。**裁决**：3D 数据坐标系约定要写成单元测试并交叉验证。置信度：中高。

## 4. 证据分级

| 断言 | 等级 | 说明 |
| --- | --- | --- |
| 1st 的双路线合并与 TensorRT/stride2 细节 | 自述 + 公开代码/权重 + 图 | 高 |
| 1st-分割的"倒数第二层更准/框回归无增益" | 自述 + 图 | 中高 |
| 2nd 的 InstanceNorm+PReLU 对照 | 自述 + 5 次实验对比图 | 中高 |
| 9th 的按类掩码半径 +0.02~0.04 | 自述 | 中 |
| 坐标 +1.0 的结论 | 自述 + notebook + 社区讨论 | 中高 |

## 5. 悬案与缺口（登记）

- 5th–8th 的方案未入库；"卡在 benchmark 下"（98 票）与"合成数据基础模型"（81 票）未细读；
- 1st 的合并权重与逐模型贡献未量化（只有"合并即第 1"）；
- 12 小时限时的具体推理预算分配（TTA/集成规模）未完整给出；
- 归档 11 图：1st-OD 的逐类阈值曲线（图 1）、1st-分割的部分 U-Net、2nd 的稳定性对照为关键图证。

## 6. 图表证据

![1st-OD 的逐类阈值曲线](../../intel/czii-cryo-et-object-identification/bodies/561440_img/01.png)

**图 1**（topic 561440）：点检测集成的 5 折（+平均）逐类 F-beta–置信度阈值曲线——五类粒子的最优阈值差异极大（ribosome/VLP 高置信度仍稳、beta-galactosidase 早早衰减），且折间形状有差异。这是"逐类阈值 + 阈值需按折/集成重标定"的直接依据（也解释了 1st-分割用 OOF 曲线重标定的做法）。

## 7. 出处

- 1st-OD（561440）：https://www.kaggle.com/competitions/czii-cryo-et-object-identification/discussion/561440
- 1st-分割（103 票）：https://www.kaggle.com/competitions/czii-cryo-et-object-identification/discussion/561510
- 2nd（44 票）：https://www.kaggle.com/competitions/czii-cryo-et-object-identification/discussion/561568
- 3rd（53 票）：https://www.kaggle.com/competitions/czii-cryo-et-object-identification/discussion/561417
- 4th（68 票）：https://www.kaggle.com/competitions/czii-cryo-et-object-identification/discussion/561401
- 9th（51 票）：https://www.kaggle.com/competitions/czii-cryo-et-object-identification/discussion/561431
- "卡在 benchmark 下"（98 票）：https://www.kaggle.com/competitions/czii-cryo-et-object-identification/discussion/547350
