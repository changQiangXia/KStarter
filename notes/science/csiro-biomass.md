# CSIRO - Image2Biomass Prediction

> 主题：science（食品/农业视觉）｜ 子类：— ｜ 领域：农业 ｜ 类别：Research
> 截止：2026-01-28 ｜ 队伍数：3805 ｜ 机制：代码赛 ｜ 指标：生物量回归（多目标）
> 数据来源：`intel/csiro-biomass/`（80 条主题索引 + 6 篇 write-up 正文）

## 1. 任务与数据

- 预测目标：由牧场照片预测**生物量构成**（多组分回归，如绿/枯/总量等）。
- 数据形态：草地图像 + 组分标签；**领域分布差异明显**（不同牧场/季节/拍摄条件）。
- 构造陷阱：
  - 多目标回归（组分之间强相关）；
  - 图像采集条件差异大（光照、高度、密度）；
  - 纯粹的视觉回归任务，缺少结构化先验。

## 2. 方案谱系

| 方案 | 名次 | 关键点 |
| --- | --- | --- |
| 见讨论区 1st 方案 | 1st | 本场最高票方案（137 票） |
| **弱监督语义分割** | 2nd | 把回归任务重构为分割问题，用弱监督降低标注依赖 |
| **ViT-Huge + DINOv3 + 多模态** | 4th | 用大规模自监督视觉骨干（DINOv3）+ 多模态输入 |
| 大量实验驱动的图像回归方案 | 5th（solo 金） | 作者自述做了 **100+ 次训练实验**（v1→v188）；首次参加 CV 类比赛即拿到 solo 金，私人榜 0.76 |

**三种不同思路并存**是本场的看点：2nd 把回归变成分割、4th 上大骨干、5th 用实验量取胜——**同一任务有多条可行路径**。

## 3. 关键技巧

- **大规模实验迭代**：本场 5th 的核心方法不是某个技巧，而是**系统性的实验管理**（编号、记录、对比）。
- **图像回归的多目标处理**：组分之间相关 → 可考虑共享主干 + 多头，或预测总量后按比例分配。
- **数据增强对齐采集条件**（光照/尺度/密度）。

## 4. 可迁移性评估

- **可直接迁移**：
  - **实验编号与追踪的习惯**（v1…v188）——高迭代任务的基础设施；
  - 多目标相关回归的共享表示 + 多头结构；
  - 采集条件差异大时的增强策略。
- 需要前提：足够的 GPU 时间（100+ 实验不是小成本）。
- 不建议照搬：无记录地反复试错。

## 5. 对新手的关键启示

1. **系统性实验 > 单点技巧**：本场 5th 的"方法"就是纪律。
2. 农业/食品视觉是 Kaggle 的重要赛题来源（与 CMI、RSNA 并列的行业方向）。
3. 首次参加新领域也能拿金（前提是实验量与记录到位）。

## 6. 轻读结论（2026-10 补）

**一句话**：小样本 + 分布漂移的农业 CV 赛——**按 Sampling_Date 分组 CV 是生死线**（不分组 CV-LB 差 0.119，分组后 0.027）；DINOv3 底座 + 数据清洗 + 区间分类辅助头 + 在线伪标是涨分四件套。

- 分组验证（132 票）：按 State 分层 CV 0.7189/LB 0.60；按日期分组 CV 0.5837/LB 0.55 → 调优后 0.5968/0.57。
- 1st（670735）：3 折（state+日期）+ 左右视角注意力融合 + DINOv3；**7 区间分类辅助头 +0.03**；两轮伪标 + SWA 在线训练 +0.02；物理关系仅用于后处理；priv 0.68。
- 4th（670677）：**手裁纸板 +0.01**；ViT-Huge + NDVI/Height 表格融合；**从图像预测 NDVI/Height 的辅助任务 +0.01**（最终 0.76/0.66）。
- 5th（670668）：HSV+inpaint 去日期戳；把 Dead=Total−GDM、Clover=GDM−Green 当先验。
- 7th（670654）：DINOv3-Large 冻 80%；日期分组 + WA 细分虚拟日期 + 1000 万种子搜切分；SWA（top-3 loss + top-3 score）。

**裁决**：先做数据审计（伪影/日期戳/背景板）与分组验证，再上大底座；物理约束放推理端推导；测试期自适应（伪标/TTT/SWA）是最后的大杠杆。

**悬案**：2nd/3rd/6th 方案缺失；5th 私榜 0.76 与其余队 0.66–0.68 的口径差未澄清。

## 7. 图表证据

![4th 的多模态融合架构](../../intel/csiro-biomass/bodies/670677_img/01.png)

**图 1**（topic 670677）：RGB → ViT-Huge DINOv3，NDVI/Height → MLP(64→128)，拼接 → 融合 MLP(512→256) → 五个回归头。

## 8. 出处

- 讨论区索引：`intel/csiro-biomass/topics.md`（80 条）
- 已收录 write-up（6 篇）：
  - 1st（137 票）：https://www.kaggle.com/competitions/csiro-biomass/discussion/670735
  - 2nd 弱监督语义分割（61 票）：https://www.kaggle.com/competitions/csiro-biomass/discussion/670895
  - 4th ViT-Huge DINOv3 多模态（46 票）：https://www.kaggle.com/competitions/csiro-biomass/discussion/670677
  - 5th solo 金（81 票）：https://www.kaggle.com/competitions/csiro-biomass/discussion/670668
  - 7th single/dual+TTT（41 票）：https://www.kaggle.com/competitions/csiro-biomass/discussion/670654
  - 按 Sampling_Date 分组（132 票）：https://www.kaggle.com/competitions/csiro-biomass/discussion/615401
- 轻读全本：`analysis/deep/csiro-biomass.md`（Tier B 轻读：对照矩阵/裁决/证据分级/悬案 + 1 图证）
