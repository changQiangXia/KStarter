# Image Matching Challenge 2022 轻量深读（Tier B）

> 赛事：Research ｜ 主题 cv（三维重建的图像匹配）｜ 642 队 ｜ 代码赛 ｜ 指标：pose mAA（相机位姿平均精度）
> 材料基础：`digests/image-matching-challenge-2022.md`（5 篇正文：1st 329131 / 2nd 329317 / 4th 328798 / 9th 328796 / 10th 328903 等；80 条主题索引）+ 15 张图
> 轻读时间：2026-10（Tier B B06）

## 1. 一句话重述与数字账

给定同一场景的多张照片，估计相机位姿（mAA）；每对图像要算基础矩阵 F。真正的考点是**"后处理与集成"而不是训练**：主办方明说目标是发现更好的后处理技术（9th 转述），前列队伍全部使用**预训练模型 + 多分辨率集成 + 关键点筛选/裁剪**，只有少数尝试微调 LoFTR。

| 关键数字 | 值 | 来源 |
| --- | --- | --- |
| 1st（329131） | 两阶段：① 多分辨率匹配（LoFTR@840；SuperPoint+SuperGlue@840/1024/1280）→ 拼接关键点 → **DBSCAN 保留 80~90% 的匹配点簇 → 裁剪共视区（mkpt_crop）**；② 在裁剪图上重匹配（LoFTR@1280、DKM@840、SuperGlue@1024/1280/1536）→ 与阶段①关键点拼接 → RANSAC 求 F；全部预训练、无微调；mkpt_crop 同时**过滤外点 + 复用阶段①关键点**（"lean & efficient"）；Mask2Former 分割裁剪更差（无法判断"两图共视"）；对小块共视区会被裁掉的缺陷，用原始图匹配点补充 | 329131 |
| 2nd（329317） | 自研 transformer 匹配器单模 **0.833/0.838（pub/priv）无 TTA**；与其他强匹配器集成后：+QuadTree 0.854/0.848；对比：LoFTR 单模 0.783/0.772、SuperGlue+8k SuperPoint 0.724/0.728；提出 transformer 匹配器的**归一化位置编码**；明确"不做 TTA/多分辨率/前后处理"也能靠单模强度进前列 | 329317 |
| 4th（328798） | 全员土木背景、零基础起步；纯预训练 + 多尺度集成（LoFTR 长边 1000/1200/1400；SuperGlue 1200/1600/2000/2800；DKM 按面积归一 346800）+ 关键点回缩放到原图 + MAGSAC；**因 SuperGlue 许可证不允许获奖，专门准备"去 SuperGlue"路线**（LoFTR+QuadTree+DKM 私榜 0.843），最终提交 0.852 | 328798 |
| 9th（328796） | "后处理为王"；从公开 notebook 起步；正确回缩关键点 + 简单集成/TTA → 0.833/0.824；**DKM 采样改造**（绝对置信度 >0.8、每窗口随机 200 点、800×600）→ 0.838/0.836；**把 MAGSAC 放到并行线程 + 预取数据**后能加更多 TTA + 置信度阈值（LoFTR 0.3/SG 0.4）+ 迭代 25 万 → 0.845/0.842；**SuperGlue 的正确 TTA 方式**（每张 TTA 只跑一次 SuperPoint，SuperGlue 做 N² 交叉配对，坐标在 SuperGlue 后回缩）→ 0.847/0.848；有一次私榜 0.851（相当于第 5）但未选 | 328796 |
| 事件 | "Sudden 30+ positions leaps on top of the LB"（43 票）质疑榜面跳变；LoFTR 微调帖（70 票）为少数训练路线；官方提供 LoFTR/DISK/DKM 示例 notebook 与学习材料 | 社区 |

## 2. 逐方案对照矩阵

| 维度 | 1st | 2nd | 4th | 9th |
| --- | --- | --- | --- | --- |
| 训练 | 无（全预训练） | 自研模型（未开源） | 无 | 无 |
| 多分辨率 | 是（7 个组合） | 否 | 是（三模型多尺度） | 是（TTA） |
| 关键点筛选 | **DBSCAN+共视区裁剪** | QuadTree | 多尺度拼接 | 置信度阈值 + DKM 采样 |
| 求解器 | RANSAC | — | MAGSAC | **MAGSAC 25 万次迭代** |
| 工程优化 | 复用阶段①关键点 | — | — | MAGSAC 并行线程 + 预取 |
| priv | 1st | 0.838（单模） | 0.852（提交） | 0.848 |

## 3. 共识、分歧与裁决

### 共识一：本赛考"后处理 + 集成"，预训练模型够用（1st/2nd/4th/9th）

四队都不用微调；9th 转述主办方"目标是更好的后处理"；1st/4th 的全部增益来自匹配器组合、分辨率与筛选。**裁决**：特征匹配赛的 ROI 排序 = 集成 > 关键点筛选/裁剪 > 求解器调参 > 模型训练。置信度：高。

### 共识二：多分辨率是"免费多样性"（1st/4th/9th）

1st 用 7 个（模型×分辨率）组合并显式指出"不同分辨率得到不同匹配点 → 多样性"；4th 每模型 3–4 档尺度；9th 的 TTA 也以分辨率/翻转/旋转为主。**裁决**：同一预训练模型在不同输入尺度下的输出近似"不同模型"，是零成本的集成来源。置信度：高。

### 共识三：关键点必须回缩放到原图坐标（9th 明确指为公共 bug）

9th 指出"所有公开 notebook 都没把匹配点正确回缩放"，修好后集成/TTA 才能正确拼接。**裁决**：多尺度管线里坐标变换是最容易错的环节，值得写单元测试。置信度：高。

### 分歧一：要不要裁剪/筛选关键点

1st 用 mkpt_crop（DBSCAN 簇 + 共视区裁剪）拿第 1，并说"裁剪后重匹配"显著增益；2nd 的基线**不做任何前后处理**仍拿 0.838（其 QuadTree 版 0.854）；9th 只做置信度阈值与 DKM 采样。**裁决**：裁剪的收益取决于匹配器质量与场景类型——它同时是筛选器与"再匹配的聚焦器"，但对小共视区有风险（1st 自己也补了原始图匹配点）。置信度：中高。

### 分歧二：单模强度 vs 大规模集成

2nd 用单模 0.838（无 TTA）证明模型本身的强度；1st/4th/9th 靠集成与后处理。**裁决**：两条路都能到前列；若无法训新模型（本赛多数队伍），集成与工程是唯一路径。置信度：中高。

### 事件：许可证影响选型（4th）

SuperGlue 的许可证不允许获奖 → 4th 专门准备"去 SuperGlue"的提交路线。**裁决**：代码赛选型前先核对许可证（与"是否可获奖"绑定），并准备合规备选提交。置信度：中高（单队自述，但有官方规则背景）。

## 4. 证据分级

| 断言 | 等级 | 说明 |
| --- | --- | --- |
| 1st 的 mkpt_crop 框架与多分辨率组合 | 自述 + 框架图 | 高 |
| 9th 的分数链（0.833→0.848）与工程细节 | 自述 + 逐项数字 | 高 |
| 2nd 的单模 0.838 与各匹配器对照 | 自述 + 表 | 中高（自研模型未开源） |
| 4th 的许可证路线与 0.843/0.852 | 自述 + 公开 notebook | 中高 |
| 榜面跳变质疑 | 论坛帖 | 低/现象 |

## 5. 悬案与缺口（登记）

- 3rd/5th–8th/10th 的方案未细读；LoFTR 微调帖（70 票）与"Experiments with pretrained models"（51 票）未细读；
- 2nd 的自研匹配器细节因论文双盲未公开，无法复核；
- 1st 未给出逐项消融（mkpt_crop 单独贡献多少未量化）；
- 归档 15 图中 2 张（1st 的框架图与 mkpt_crop 示意）为关键证据，另有 9th/10th 的流程与可视化图。

## 6. 图表证据

![1st 的两阶段匹配框架](../../intel/image-matching-challenge-2022/bodies/329131_img/01.png)

**图 1**（topic 329131）：1st 的框架——LoFTR@840 与 SuperPoint+SuperGlue@840/1024/1280 的关键点拼接 → DBSCAN 聚类 → 裁剪共视区 → 在裁剪图上再用 LoFTR/DKM/SuperGlue 多分辨率重匹配 → 与阶段①拼接 → USAC_MAGSAC 求基础矩阵。阶段①的关键点同时服务于"裁剪"和"最终集成"。

## 7. 出处

- 1st（329131）：https://www.kaggle.com/competitions/image-matching-challenge-2022/discussion/329131
- 2nd（45 票）：https://www.kaggle.com/competitions/image-matching-challenge-2022/discussion/329317
- 4th（43 票）：https://www.kaggle.com/competitions/image-matching-challenge-2022/discussion/328798
- 9th（51 票）：https://www.kaggle.com/competitions/image-matching-challenge-2022/discussion/328796
- 基础矩阵科普（94 票）：https://www.kaggle.com/competitions/image-matching-challenge-2022/discussion/316975
- LoFTR 微调（70 票）：https://www.kaggle.com/competitions/image-matching-challenge-2022/discussion/320219
