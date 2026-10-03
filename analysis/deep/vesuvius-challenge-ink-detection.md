# Vesuvius 墨迹检测深读：深度不变性 × 几何对齐 × 校准

> 赛事：Featured ｜ 主题 cv（文化遗产/3D 成像）｜ 1249 队 ｜ 代码赛 ｜ 指标 F0.5（像素级）（2023-06-14 截止）
> 材料基础：`digests/vesuvius-challenge-ink-detection.md`（6 节：1st/2nd/6th/9th/11th + 自制碳化纸莎草帖）+ 18 张图
> 深读时间：2026-10（Tier A #18）

## 0. 一句话重述：这道题真正在考什么

题面是"在碳化卷轴的 3D CT 中分割墨迹像素"，实际被考的是**三个几何/统计问题**：

1. **深度不变性**：墨迹所在的 CT 层深在不同残篇（fragment）间漂移——"把中间 16 层当通道"的 2.5D 做法让模型学"哪一层有墨"的捷径，换残篇即失效；正确姿态是"3D 特征 → 沿深度 max/pool → 2D 分割"（1st/2nd/11th 三家殊途同归）；
2. **几何对齐**：测试残篇被**旋转**（还有 A/B 可拼接结构）→ 旋转增强/TTA 是最大单步增益（6th：公开 0.58→0.74；1st：90° 旋转增强"至关重要"）；
3. **阈值与校准**：F0.5 对阈值极端敏感，且单模型最优阈值范围宽（1st 的日志里某模型 best_th=0.1）——**多模型平均把最优阈值压回 0.5**（1st），或用百分位阈值固定正例比例（6th/2nd）。

其余两件工程事：**大切块**（128<512<1024，且总像素不变→训练时间几乎不变，是"免费的上下文"）与**输出低分辨率化**（1/32 → 双线性上采样；粗分割比逐像素精确更稳，2nd 独立验证）。

一句话：**这是一场"把几何问题处理干净 + 把校准做对"的比赛**——模型架构（SegFormer/UNet）是公共件，分差全在深度聚合方式、旋转处理与阈值选择上。

## 1. 材料与角色

| 帖子 | 作者 | 票数 | 角色与独有信息 |
| --- | --- | --- | --- |
| [417496](https://www.kaggle.com/competitions/vesuvius-challenge-ink-detection/discussion/417496)（1st，112 票） | ryches | 112 | **四大归因**：大切块（128<512<1024 的曲线）、深度不变架构（3D→max→2D，最佳 UNETR→b5 0.82 公开/0.67 私榜）、多模型平均改善校准、验证后全量训练（+0.04）；9 模型清单与后处理 |
| [417274](https://www.kaggle.com/competitions/vesuvius-challenge-ink-detection/discussion/417274)（6th，84 票） | chumajin | 84 | **测试旋转的实证修复**（0.58→0.74）；A/B 拼接推理；百分位阈值；IR 图像 +0.01；7→10 折；EfficientNet+SegFormer 对照表 |
| [417255](https://www.kaggle.com/competitions/vesuvius-challenge-ink-detection/discussion/417255)（2nd，76 票） | tattaka & mipypf & yukke42 & ron | 76 | **1/32 分辨率足够**；2.5D/3D 混合架构；percentile 阈值（0.9 vs 0.93 的反转）；MViTv2 3D Transformer；stride 实验 |
| [417361](https://www.kaggle.com/competitions/vesuvius-challenge-ink-detection/discussion/417361)（9th，43 票） | hengck23 | 43 | 2 折 × 2 模型（resnet34d-unet 256/32 层 + pvtv2-b3-daformer 384/16 层）；验证 fragment-1/2aa |
| [417281](https://www.kaggle.com/competitions/vesuvius-challenge-ink-detection/discussion/417281)（11th，33 票） | tk | 33 | 2.5D + 1D pool encoder；6 UNet 集成；RandomRotate90 因推理旋转而加；阈值 0.5 直接可用 |
| [407545](https://www.kaggle.com/competitions/vesuvius-challenge-ink-detection/discussion/407545)（自制纸莎草，136 票） | 社区 | 136 | 买纸莎草自己碳化（没有 CT 机，无法扩充数据）——本场社区参与度的最佳注脚 |

**材料缺口（未扩采，登记备查）**：索引里另有 14 条 write-up 未收录，含 [7th（417430）](https://www.kaggle.com/competitions/vesuvius-challenge-ink-detection/discussion/417430)、[3rd（417536）](https://www.kaggle.com/competitions/vesuvius-challenge-ink-detection/discussion/417536)、[4th（417779）](https://www.kaggle.com/competitions/vesuvius-challenge-ink-detection/discussion/417779)、[5th（417642）](https://www.kaggle.com/competitions/vesuvius-challenge-ink-detection/discussion/417642)、[top solutions live discussion（417448）](https://www.kaggle.com/competitions/vesuvius-challenge-ink-detection/discussion/417448) 等。

## 2. 逐方案对照矩阵

| 维度 | 1st ryches | 2nd tattaka 队 | 6th chumajin | 11th tk | 9th hengck23 |
| --- | --- | --- | --- | --- | --- |
| 深度处理 | 中 16 层 → 3D（CNN/UNet/UNETR）→ **沿 z 取 max** 成多通道 → 2D SegFormer | 2.5D 分组（5×7/3×9 层，取 65 层中段 35/27）+ 3D ResBlock → avg+max 池化 z | 三组层段（25-30/27-32/29-34）+ IR 图；CNN+Unet 与 SegFormer 双线 | 按 3 分组（z_len=img_num/3）→ 2D 编码 → avg pool z | 固定深度：32 层/16 层 |
| 切块/分辨率 | 1024 为主（对比 128/512） | 输入 256（2.5D）/192（3D）；**标签与输出都降采样到 1/32** | 480–1024（按 backbone） | 224；训练 stride 112、推理 56 | 256 / 384 |
| 测试几何 | 4× 旋转 TTA + 1/4 stride 窗口；旋转增强至关重要 | h/v flip TTA；按 stride 切换 | **A/B 拼接 + 顺时针旋转推理 + 逆时针还原**；百分位阈值 | 加入 RandomRotate90（推理旋转有效） | 常规 |
| 损失/正则 | dice+bce；SWA（应对 checkpoint 不稳） | bce + **global fbeta**；label smoothing 0.1；cutmix/mixup/manifold mixup；drop_path 0.2；EMA | SoftBCEWithLogitsLoss；20 epoch/早停 4 | bce+dice | — |
| 集成/阈值 | 9 模型；逐模型像素平均→sigmoid→再平均；**平均后阈值≈0.5** | 多成员各自模型；percentile 阈值 0.9/0.93 | 两提交：th 0.96 / 0.95（百分位） | 简单平均，th 0.5 | 2 折 × 2 模型 |
| 后处理 | 连通域清理（<10k 像素剔除；本地最优 25k） | 忽略输出边缘（红色有效区） | mask=0 区域跳过 | mask=0 跳过 | — |
| 成绩 | 最佳单模 UNETR→b5：公开 0.82 / 私榜 0.67 | 1/32 分辨率路线（未给总分） | 公开 0.8116 / 私榜 0.6613（sub1） | — | 第 9 |

## 3. 共识、分歧与裁决

### 共识一：深度不变性是本题的核心架构问题（三家独立收敛）

1st 的诊断最清晰：2.5D 把层当通道 → 模型学"哪层有墨"，而**层深在残篇间漂移**；解法是 3D 特征 + **沿深度 max**。2nd 的 2.5D→3D 混合（avg+max 池化 z）与 11th 的 1D pool 是同一思想的不同实现。

**裁决**：3D 医学/成像任务中，"沿第三维做特征聚合"（max/pool）比"固定层切片"泛化好得多。置信度高（三家 + 1st 的机制论证）。

### 共识二：旋转处理是最大单步（6th 量化，1st/11th 呼应）

6th：把测试残篇拼接后顺时针旋转再推理（预测后逆时针还原）→ EfficientNet B4 **0.58→0.74**；11th：加入 RandomRotate90 因为"推理时旋转图像提升了公开榜"；1st：不确定测试是否旋转，但 90° 旋转增强"至关重要"，并用 4× 旋转 TTA。

**裁决**：当测试几何与训练不一致时，先做几何对齐（增强/TTA），收益可能数倍于架构调整。置信度高。

### 共识三：阈值必须显式校准（三条不同路线都有成功案例）

1. **平均即校准**（1st）：单模型最优阈值范围宽（日志中某模型 best_th=0.1），多模型平均后"几乎普遍居中 0.5"；
2. **百分位阈值**（6th/2nd）：按整图排名固定正例比例——与模型无关、与 GT 正例率有关；6th 公开最优 0.96，2nd 用 0.9/0.93；
3. **直接 0.5**（11th）：其 2.5D+1D 集成在 0.5 上工作良好。

**裁决**：校准路线取决于集成规模与分布假设；小公开榜下 1st 认为百分位"风险太大"（若测试墨迹占比不同就错），2nd/6th 接受该假设。置信度中高。

### 分歧一：输出分辨率——高精度小图 vs 低分辨率粗图

1st：SegFormer 输入 1024 输出 256，粗分类更容易（"第二名的 1/32 验证了低分辨率有帮助"）；2nd 实证：**标签降采样到 1/32**、decoder 无上采样、资源全给编码器；6th/11th 用较高分辨率输出。

**裁决**：F0.5 对像素级边界不敏感（粗分割上采样即可），低分辨率输出=更少的无效精度与更强的正则；这是本任务特有的"降维打击"。置信度高（1st 与 2nd 互证）。

### 分歧二：外部/IR 数据（+0.01 vs 伤害）

6th：**训练集加入 IR 图像** → CV/LB 各 +0.01；但 **IR 预训练** → LB 下降；EMNIST 外数据 → 也降。1st：试了多种数据准备只保留"中 16 层"。

**裁决**：同源配准的 IR 图像作为输入通道有效；跨域数据（EMNIST）或错误阶段（预训练）注入无效甚至有害。置信度中（单家消融）。

## 4. 增量数字账

| 动作 | 数字 | 来源 |
| --- | --- | --- |
| 切块尺寸缩放（dice 曲线） | 128 < 512 < 1024；1024 收敛到 ~0.58、512 ~0.55、弱增强版 ~0.52 | 1st |
| 大切块的时间中性性 | 1024² 覆盖面积是 128² 的 64 倍 → 每 epoch 切块数 ~1/64；epoch/收敛时间几乎不变 | 1st（机制） |
| 最佳单模 | UNETR（32 通道）→ SegFormer b5：公开 0.82 / 私榜 0.67 | 1st |
| 9 模型集成分值带 | 公开 0.77–0.82（3d unet/cnn/unetr × b3/b5 × 512/1024） | 1st |
| 全量数据训练收益 | 验证通过后对全部残篇训练同 checkpoint：**+0.04** | 1st |
| stride 减半 | 1/4 → 1/8 stride：+0.01（但不如"多塞模型"） | 1st |
| 旋转修复（6th） | EfficientNet B4：公开 **0.58→0.74** | 6th |
| IR 图像（6th） | CV +0.01 / LB +0.01 | 6th |
| k 折增加（6th） | 5→7 折：公开 +~0.1（原文口径；存疑，登记待核） | 6th |
| 6th 最终两提交 | sub1 th 0.96：公开 0.8116 / 私榜 0.6613；sub2 th 0.95：公开 0.7996 / 私榜 0.6548 | 6th |
| 2nd 的百分位阈值 | 0.9 vs 0.93：预期 0.90 私榜更好，实际 **0.93 更好** | 2nd |
| 2nd 输出分辨率 | 标签 1/32 双线性降采样；输出 1/32 → 双线性上采样 | 2nd |
| 11th 推理 stride | 训练 112 → 推理 56（更细） | 11th |
| 后处理清理 | 连通域 <10k 像素剔除（本地最优阈值下调 + 清理至 25k） | 1st |

**可复算/结构校验（2 处吻合）**

1. 1st 的"大切块免费"机制：1024²/128² = **64** 倍面积 → 相同覆盖率下切块数成比例减少 ✓；
2. 11th 的分组：z_len = img_num/3 → 30 层 → 10 组、21 层 → 7 组 ✓（与其 backbone 表一致）。

## 5. 机制推演

**M1｜为什么大切块"免费"**：分割训练按滑窗采样，总像素预算≈覆盖率×图像面积；切块越大 → 单个样本覆盖越多像素 → 样本数越少，总计算量近似不变，但**感受野内可包含整字母/多字母的上下文**（小切块的输出"斑驳"，1st 语）。这是分割任务相对分类任务独有的"上下文免费午餐"。

**M2｜为什么"沿 z 取 max"能获得深度不变性**：3D 卷积先在局部深度上检测"任意深度的墨迹模式"，max-pool 把"某处有墨"变成"这个 (x,y) 位置有墨"的聚合（类 MIL）；无论墨迹出现在第几层，输出通道都会被激活 → 深度成为不变维度。相反，2.5D 的通道索引被当成特征维度，模型学到"第 7 层有事"这样的片段特异捷径。

**M3｜为什么低分辨率输出反而好**：F0.5 的像素指标对边界不敏感；墨迹检测的不确定性本来就是"哪个区域有字"而非"哪一像素"；1/32 输出把任务从逐像素分类变成区域分类（更少的假阳性碎片），再上采样恢复。2nd 的"1/32 够了"是对此的独立验证。

**M4｜百分位阈值的假设与风险**：`threshold = 使正例数=固定比例的 rank 分位`，依赖"测试墨迹占比≈已知先验"。优点是消除模型尺度差异（与校准解耦）；风险是分布漂移时系统性错（1st 明确拒绝："若墨迹分布不是预期的那样，太危险"）。2nd 的 0.9/0.93 反转说明连"预期更优"的方向都不可靠。

**M5｜平均为何校准**：每个模型的预测分布形状不同（有的 best_th=0.1、有的 0.9）；对同一像素平均多个模型的概率 → 中心极限式地收缩方差、概率向 0.5 附近集中 → 阈值敏感性下降。**这是"多模型平均改善校准"的统计本质**（1st 的第一手观察）。

**M6｜几何对齐优先于模型容量的证据链**：6th 的 0.58→0.74 只是加了"旋转推理"；1st 用 4× 旋转 TTA；11th 的 RandomRotate90 直接提公开分。当数据/测试存在已知几何差异时，**不变性处理（增强/TTA）是乘法项**，而模型升级是加法项。

## 6. 证据分级

| 断言 | 等级 | 说明 |
| --- | --- | --- |
| 切块尺寸曲线（128/512/1024） | **可读取（图）** | 1st 训练日志（dice vs step） |
| 旋转推理 0.58→0.74 | **自述（强）** | 单变量改动；社区多人复现旋转重要 |
| 深度不变架构（3D→max→2D） | **自述 + 三家同构** | 机制论证清晰 |
| 平均后阈值居中 0.5 | **自述（含日志截图）** | 有阈值扫描原始日志（best_th=0.1 可见） |
| 6th 模型对照表 | **可读取（表）** | CV/公开/私榜三列 |
| 2nd 的 1/32 分辨率 | **自述 + 1st 互证** | 无单独消融数字 |
| 全量训练 +0.04 | **自述** | 未给方差 |
| k 折 5→7 公开 +0.1 | **自述（口径存疑）** | 疑似 0.01 或不同口径；登记待核 |
| 自制纸莎草 | **社区证据（无法评估）** | 无 CT，未用于建模 |

## 7. 边界条件与反事实

- **小公开榜 → 防守型策略**：1st"全程打得很保守"；最终 30 分钟前试 0.55 阈值（公开更差、私榜略好，未选）——**选择风险双向存在**；2nd 的 0.9/0.93 反转同理。
- **反事实（6th）**：若不做旋转推理，0.58 的公开分大概率无缘金区；几何对齐的杠杆 >> 继续调架构。
- **反事实（1st）**：他自己说"在集成与最优阈值上其实有很多没吃掉"——若阈值/集成再优化，0.67→更高未必不可能；但防守策略牺牲了探索。
- **假设边界**：百分位阈值依赖"测试墨迹占比先验"；若主办方换残篇/换扫描仪，正例率变化会让该方法系统性偏移。
- **数据边界**：碳化卷轴的"墨"是 CT 中的微弱密度差；IR/可见光图像不是所有残篇都有——6th 的 IR 增益不可无条件复制。

## 8. 悬案与失败学

**悬案**

1. **测试旋转的确切规范**：1st 未证实（只做了不变性），6th 从榜分推断；官方是否旋转、旋转多少度（90° 倍数？）未定论；
2. **低分辨率输出的极限**：1/32 是否还够、1/64 会怎样——1st 猜测"更低或许也行"，未验证；
3. **多类输出（nothing/mask/ink）**：1st 说输出更干净但未充分评估——一个被时间截断的方向。

**失败学**

| 失败 | 来源 | 教训 |
| --- | --- | --- |
| 2.5D 当通道（学"哪层有墨"） | 1st | 深度漂移任务不能用固定层切片 |
| 花哨增强（噪声/模糊/粗丢/网格畸变等） | 1st | "旋转与翻转至关重要，其余都是非因素" |
| TTA 加翻转 | 1st | 对已旋转不变的任务无增量 |
| 百分位阈值（1st 未采用） | 1st | 分布假设太强，风险 > 收益（但他也承认自己保守） |
| ConvNext/Mask2Former/Swin+PSPNet/BeiT | 6th | CV/LB 都不稳定；EfficientNet/SegFormer 家族更稳 |
| SegFormer b5 等大模型 | 6th | 更大模型 CV 好但 LB 差（数据量不足过拟合） |
| IR 预训练 / EMNIST 外数据 | 6th | 同源输入有效 ≠ 同源预训练有效；跨域数据有害 |
| 训练 stride 75/56（yukke42） | 2nd | 训练窗口步长过小无效；推理才用更细 stride |
| 3D 编码器 / SegFormer / mixup / 更多层（11th 视角） | 11th | 与其 2.5D+1D pool+UNet 配方相比均无增益 |

## 9. 图表证据

> 路径相对本文件（`analysis/deep/`）：`../../intel/vesuvius-challenge-ink-detection/bodies/<topic>_img/NN.ext`

**图 1：切块尺寸的训练曲线（128<512<1024 的直接证据）**（1st，topic 417496）——`../../intel/vesuvius-challenge-ink-detection/bodies/417496_img/01.png`

![crop size](../../intel/vesuvius-challenge-ink-detection/bodies/417496_img/01.png)

*读图结论*：dice vs step——1024（灰）收敛到 ~0.58，512（橙）~0.55，1024+弱增强（蓝）~0.52；**大 crop 的最终精度与曲线形状都更优**，且作者旁注"1024 的训练时间几乎不变（切块数少了 64 倍）"。

**图 2：单模型阈值扫描日志（校准问题的物证）**（1st）——`../../intel/vesuvius-challenge-ink-detection/bodies/417496_img/05.png`

![threshold sweep](../../intel/vesuvius-challenge-ink-detection/bodies/417496_img/05.png)

*读图结论*：该模型的最佳阈值是 **0.1**（fbeta 0.6447），阈值升到 0.5 时 fbeta 掉到 0.6032——**"好模型 + 错阈值 = 榜上灾难"**的具体数字。这正是"平均后阈值居中 0.5"的价值所在。

**图 3/4：后处理前后（连通域清理）**（1st）——`../../intel/vesuvius-challenge-ink-detection/bodies/417496_img/06.png`、`.../07.png`

![before](../../intel/vesuvius-challenge-ink-detection/bodies/417496_img/06.png)
![after](../../intel/vesuvius-challenge-ink-detection/bodies/417496_img/07.png)

*读图结论*：两图像素级差异（MD5 不同）但视觉近似——清理剔除的是 <10k 像素的细小斑粒（放大后可见），主体字形不变。**后处理的作用是"去噪点"而非改形状**；作者本地最优是"阈值调低 + 清理到 25k"，提交版保守用 10k。

**图 5：6th 对测试数据的结构理解（旋转 + A/B 拼接）**（topic 417274）——`../../intel/vesuvius-challenge-ink-detection/bodies/417274_img/01.jpg`

*读图结论*：Frag a + Frag b 可横向拼接；文字沿纵向排布（图像被旋转）。据此推理流程 = 拼接 → 顺时针旋转 → 推理（+hflip TTA）→ 逆时针还原 → 分别切回 A/B；EfficientNet B4 公开 0.58→0.74。

**图 6：6th 的 CNN+Unet 训练管线**（topic 417274）——`../../intel/vesuvius-challenge-ink-detection/bodies/417274_img/02.jpg`

*读图结论*：三组层段（25-30/27-32/29-34，各 6 层）+ 同一张 IR 图像；训练集 = 三组之和，valid 1/2/3 分别验证；输出 → Average → **Percentile**（百分位阈值）。

**图 7：6th 的 SegFormer 管线（3 通道限制）**（topic 417274）——`../../intel/vesuvius-challenge-ink-detection/bodies/417274_img/03.jpg`

*读图结论*：层段收窄为 3 层/组（25-27/28-30/31-33）+ IR，凑成 3 通道喂 SegFormer；其余同上。

**图 8：2nd 的"红色有效区"（忽略输出边缘）**（topic 417255）——`../../intel/vesuvius-challenge-ink-detection/bodies/417255_img/01.png`

*读图结论*：滑窗推理的边缘（padding/感受野不足）不可靠；只取每个窗口内部的红色区域拼接输出。**滑窗分割的通用后处理动作**，与 1st 的 connected-components 清理互补。

## 10. 对既有笔记/playbook 的修订点

1. `notes/cv/vesuvius-challenge-ink-detection.md` 升级：补齐 6 节作者/票数；方案谱系扩为 5 方案对照矩阵；新增深度不变性、旋转对齐、阈值三路线、大切块机制、低分辨率输出与图证/失败学。
2. `playbook/cv.md`（3D/分割节）增补：
   - **深度不变聚合**（3D→沿 z max/pool→2D，替代固定层切片）；
   - **大切块免费午餐**（总像素不变、上下文翻倍；切块尺寸是首要消融项）；
   - **测试几何对齐优先**（旋转增强/TTA 常是乘法项）；
   - **分割后处理三件套**（连通域清理、忽略窗口边缘、mask=0 跳过）；
   - **阈值三路线**（平均即校准 / 百分位 / 固定 0.5）与各自假设。
3. `playbook/00-通用方法论.md` 增补："**校准是集成的一部分**"——多模型平均的收益不只在均值精度，还在把阈值敏感性压回中心。

## 11. 出处

- 1st（ryches，112 票）：https://www.kaggle.com/competitions/vesuvius-challenge-ink-detection/discussion/417496
- 6th（chumajin，84 票）：https://www.kaggle.com/competitions/vesuvius-challenge-ink-detection/discussion/417274
- 2nd（tattaka 队，76 票）：https://www.kaggle.com/competitions/vesuvius-challenge-ink-detection/discussion/417255
- 9th（hengck23，43 票）：https://www.kaggle.com/competitions/vesuvius-challenge-ink-detection/discussion/417361
- 11th（tk，33 票）：https://www.kaggle.com/competitions/vesuvius-challenge-ink-detection/discussion/417281
- 自制碳化纸莎草（136 票）：https://www.kaggle.com/competitions/vesuvius-challenge-ink-detection/discussion/407545
- 未收录缺口（登记备查）：417430（7th）｜417536（3rd）｜417779（4th）｜417642（5th）｜417448（top solutions 讨论）
