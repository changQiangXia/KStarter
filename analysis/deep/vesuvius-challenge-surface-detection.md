# Vesuvius Challenge - Surface Detection 轻量深读（Tier B）

> 赛事：Research ｜ 主题 cv（3D 表面/拓扑分割）｜ 1391 队 ｜ 代码赛 ｜ 指标：Vesuvius 2025 Metric（Surface Dice + 拓扑/VOI 组合）
> 材料基础：`digests/vesuvius-challenge-surface-detection.md`（6 篇正文：5th 679360 / 1st 679238 / 4th 679222 / Bronze 679221 / placeholder 651532 / 3D Viewer 663144；80 条主题索引）+ 7 张图
> 轻读时间：2026-10（Tier B B02）

## 1. 一句话重述与数字账

古卷 CT 的"表面检测"：指标同时惩罚体素级错误与**拓扑错误（洞/隧道 H1）**。真正考的是**表示（SDF vs 二值）+ 全卷推理 + 拓扑后处理**三件事；公私榜脱钩严重。

| 关键数字 | 值 | 来源 |
| --- | --- | --- |
| 1st（nnU-Net 集成） | 4 模型集成（patch 128/192/256 权重）；Set1 公 0.613/私 **0.620**（阈值 0.20）、Set2 公 0.606/私 **0.627**（阈值 0.26）；单模最好 0.587/0.613 | 1st |
| 1st 的后处理链 | 无 PP 0.572/0.596 → 去小连通 0.586/0.614 → 补小洞 0.598/0.622 → 高度图补大洞 0.601/0.625 → binary closing 0.606/**0.627** → fill_holes 持平 | 1st |
| 5th（SDF 路线） | SEResNeXt152+AttUNet；SDF 回归（加权 L1 + mass Dice）；160³ 训练/**320³ 全卷推理**；H1 隧道填充 0→13 轮 = 拓扑 +0.08（本地）；CV/公榜与私榜都不相关 | 5th |
| 4th/Bronze 等 | 未细读（4th 679222、Bronze 679221、placeholder 651532） | 材料 |

## 2. 逐方案对照矩阵

| 维度 | 1st | 5th |
| --- | --- | --- |
| 表示 | nnU-Net 概率输出 + 阈值 | **SDF 回归**（负内正外，clamp[-100,5]） |
| 损失 | nnU-Net（概率） | 0.5×高斯加权 SDF L1（峰权 9.0@ -5 voxel）+ 0.5×SDF-mass Dice |
| 主干 | nnU-Net（patch 128/160/192/224/256） | 自研 SEResNeXt152+Attention UNet（+ResNet152 谱系） |
| 推理 | 滑窗/patch | **全卷 320³**（避免滑窗拓扑伪影）+ 2/8 flip TTA + 权重 NaN 安全 |
| 后处理 | 去小连通（<20K）/ binary closing r=3 / 高度图线性插值补大洞 / 1-voxel 洞查表修补 / binary_fill_holes | 阈值 0.3 / 去尘 / **迭代 H1 隧道填充**（持久同调 + 自适应半径 3.5–7 + 桥检测 + 组件数保护） |
| 私榜 | 0.627 | 5th |

## 3. 共识、分歧与裁决

### 共识一：拓扑感知的"软表示"优于纯二值（5th 强调；1st 的 nnU-Net 概率亦近之）

SDF 天然编码距离信息，阈值扫描可在 Surface Dice 与拓扑间平滑权衡；BCE 二值模型在拓扑项一致更差；1st 用概率+阈值+后处理同样登顶。**裁决**：不要只学 0/1 mask；用 SDF/距离/概率这类连续表示 + 阈值搜索。置信度：中高。

### 共识二：后处理是本场的最大单点增益（两队均称必需）

1st：私榜 0.596→0.627（+0.031）全靠 5 步后处理；5th：0→13 轮隧道填充 = 拓扑 +0.08，且强调"桥检测/组件数保护"防止误填。**裁决**：在含拓扑项的指标下，后处理不是锦上添花而是主贡献；但每一步都要做"是否引入新洞/是否合并组件"的守卫。置信度：高。

### 共识三：全卷推理避免滑窗伪影（5th）；patch 尺寸是多样性来源（1st）

5th 明确"strided slices 产生的伪影对拓扑极有害"，坚持 320³ 整卷；1st 用不同 patch/训练轮数造集成。**裁决**：推理按整卷（或至少避免跨 sheet 的窗口拼接）；训练端用 patch 尺寸/轮数制造多样性。置信度：中高。

### 共识四：公私榜脱钩 → 提交选择是运气成分最大的一环

5th："本地 CV、公开榜与私榜相关性都差，最终提交选择很糟"；1st 被公榜误导（融合方式与阈值都选反）。**裁决**：融合用 logits、阈值偏大在私榜更好（1st 的教训）；但赛中没有可靠信号，应做多版本对冲。置信度：高（两队独立经历）。

### 分歧一：SDF 回归 vs nnU-Net 概率

5th 的 SDF 路线与 1st 的 nnU-Net 路线都进前 5；5th 自研架构+全卷推理，算力/工程门槛高；1st 依赖成熟 nnU-Net + 后处理。**裁决**：两条路都能赢；SDF 在拓扑项更稳，nnU-Net 在工程与迭代速度上更省。置信度：中高。

### 分歧二：隧道填充 vs 几何补洞

5th 用持久同调找 H1 隧道并球填充；1st 用高度图插值/查表补洞。**裁决**：前者更"拓扑正确"（对 H1 直接优化），后者更简单稳健；最强的组合可能是"几何补洞 + 迭代隧道填充"。置信度：中。

## 4. 证据分级

| 断言 | 等级 | 说明 |
| --- | --- | --- |
| 1st 的后处理逐步分数表 | 自述 + 图 | 中高 |
| 5th 的 SDF 损失/隧道填充 +0.08 | 自述 + 图 + 代码（C++ 模块名） | 中高 |
| 公私榜脱钩 | 两队独立自述 | 高 |
| 单模分数/集成权重 | 自述 | 中 |
| "touching sheets" 未解决 | 1st 明示 | 高（问题存在） |

## 5. 悬案与缺口（登记）

- 2nd/3rd 方案未收录；Vesuvius 2025 Metric 的精确定义（Surface Dice 容差 + VOI + topology 权重）未入库。
- "touching sheets"（相邻 sheet 粘连）无有效解法——本场的开放问题。
- 5th 的本地指标实现（GPU VOI/Betti matching）与 C++ 模块细节未展开。
- 4th/Bronze/placeholder 帖（含 651532 的图）未细读。

## 6. 图表证据

![SDF 目标与高斯权重](../../intel/vesuvius-challenge-surface-detection/bodies/679360_img/01.png)

**图 1**（topic 679360）：左=二值目标（含 ignore=2）；中=SDF 目标（内部负/外部正，黑线为 0 等值面）；右=高斯权重（表面附近权重峰值 9）。**把分割转成距离回归的完整动机图**。

![高度图补大洞](../../intel/vesuvius-challenge-surface-detection/bodies/679238_img/01.jpg)

**图 2**（topic 679238）：before→after 的 sheet 高度图线性插值补洞（大洞被填平）——1st 后处理链中增益最大的一步之一。

## 7. 出处

- 5th（679360）：https://www.kaggle.com/competitions/vesuvius-challenge-surface-detection/discussion/679360
- 1st（679238）：https://www.kaggle.com/competitions/vesuvius-challenge-surface-detection/discussion/679238
- 4th（679222）：https://www.kaggle.com/competitions/vesuvius-challenge-surface-detection/discussion/679222
- Bronze（679221）：https://www.kaggle.com/competitions/vesuvius-challenge-surface-detection/discussion/679221
- placeholder（651532）：https://www.kaggle.com/competitions/vesuvius-challenge-surface-detection/discussion/651532
- 3D Viewer（663144）：https://www.kaggle.com/competitions/vesuvius-challenge-surface-detection/discussion/663144
