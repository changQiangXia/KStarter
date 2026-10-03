# CZI Biohub - Cell Tracking During Development

> 主题：cv ｜ 子类：tracking ｜ 领域：生物成像 ｜ 类别：Research
> 截止：2026-09-29 ｜ 队伍数：3947 ｜ 机制：代码赛 ｜ 指标：细胞追踪（检测 + 关联）
> 数据来源：`intel/biohub-cell-tracking-during-development/`（80 条主题索引 + 6 篇 write-up 正文）

## 1. 任务与数据

- 预测目标：在**发育中的胚胎三维延时成像**里检测细胞并跨帧追踪其谱系（tracking + lineage）。
- 数据形态：3D + 时间的体数据（多帧、体量大）；细胞密集且相互接触。
- 构造陷阱：
  - **接触细胞的分割**是最难点（阈值法无法分开）；
  - 追踪关联在细胞分裂/消失时易错；
  - 体数据规模大，显存与推理时间受限。

## 2. 方案谱系

| 方案 | 名次 | 关键点 |
| --- | --- | --- |
| **双管线并行 + 逐视频对齐（而不是调一条管线）** | 14th | 检测端用 **FlowSeg**（为每个体素预测指向自身细胞中心的向量场，积分后分开接触细胞）+ 另一个不同初始化的 **TemporalUNet3D** 检测器；两条独立追踪管线结果按视频**相互校验/调和** |

## 3. 关键技巧

- **向量场分割（flow-field segmentation）**：不靠阈值，而是学习"指向细胞中心"的向量场再积分——分离接触细胞的通用思路（同源于实例分割的 embedding/flow 类方法）。
- **双管线互补 + 逐样本调和**：与其把一条管线调到极致，不如跑两条独立管线再按样本选择/融合（思路与 Feedback 的多模型融合一致，但发生在**追踪**这一层）。
- **3D + 时间的一致性**：检测与关联分步处理。

## 4. 可迁移性评估

- **可直接迁移**：
  - **用向量场/中心回归分离接触实例**（细胞、颗粒、重叠文本等）；
  - "多管线 + 逐样本调和"的鲁棒策略；
  - 3D 时序任务的分步（检测 → 关联）范式。
- 需要前提：3D 体数据处理能力与显存预算。
- 不建议照搬：只做阈值分割（接触细胞必然粘连）。

## 5. 对新手的关键启示

1. **接触/粘连对象的分割要靠"中心回归"，不是阈值**。
2. **与其调一条管线，不如让两条独立管线互相纠错**（对误差方差异质的任务尤其有效）。
3. 与 CZII cryo-ET、Vesuvius、RSNA 系列对照：**3D 生物医学影像的方法论已相当统一**（分块、中心/向量场、事件级后处理）。

## 6. 轻读结论（2026-10 补）

**一句话**：标注仅约 2.8% 的 3D 细胞追踪赛——**检测是上限、分裂要单独建模、图优化兜全局约束**；1st 的"检测器 + Soon Net（分裂状态+占用图）+ 学习式 linker + 贪心解码"把"细胞将要去哪"直接学出来，分裂单点把公榜从 ~0.925 抬到 ~0.963。

- 1st（744801）：轻量 MAE（小块 2×4×4 掩码 50%）→ 手绘 1800 细胞 + GT 节点印章微调 → 伪标签重训；Soon Net（236K CNN+508K Transformer）预测 interphase/soon/just-divided 与 continuation/division 占用图，FOV 抖动 + 时间增广 + 硬负例挖掘 + 分裂样本 151→515；transformer linker + 贪心解码。
- 3rd（744484）：六段式（2.5D+3D 检测集成占 55% 运行时间 → 稠密光流 → 运动校正匹配 → 分裂前后阶段模型 → **谱系图优化** → 后处理）；CV 0.9778/公榜 0.977/私榜 0.967。
- 5th（744549）：3D U-Net + Transformer linker + **多阶段 ILP**；发现训练集有**重复帧与 14µm 漂移帧**（验证剔除后 CV 涨而 LB 不变 → 隐藏测试无大漂移）。
- 12→95（744912）：**pseudo-unlabeling**（把"模型预测但非 GT"的位置从检测损失中掩掉）→ 负样本权重 0.01→0.1；整数规划 + 图修复 + XY 原点 +2 体素校正。
- 社区：规则法拿第 7（48 票）、GT 轨迹跳跃（42 票）、分裂指标漏洞（36 票）、18.5GB 合成数据（65 票）。

**裁决**：稀疏标注必须"未标注≠负样本"；分裂/事件类子任务要独立建模并用挖掘扩样本；学习打分 + 全局图优化/ILP 是顶配组合；先审计数据缺陷（重复帧/漂移）。

**悬案**：2nd/4th/6th–11th 方案缺失；1st 的 Soon Net 单独分数链路不全；榜面洗牌幅度未系统整理。

## 7. 图表证据

![1st 的四段式追踪管线](../../intel/biohub-cell-tracking-during-development/bodies/744801_img/01.png)

**图 1**（topic 744801）：Detector → Soon Net（分裂状态+占用图）→ Learned linker → Decode 的四段式，含训练侧（MAE/印章微调/伪标签/OOF 硬负例/分裂过采样 8×）。

## 8. 出处

- 讨论区索引：`intel/biohub-cell-tracking-during-development/topics.md`（80 条）
- 已收录 write-up（6 篇）：
  - 1st（76 票）：https://www.kaggle.com/competitions/biohub-cell-tracking-during-development/discussion/744801
  - 3rd（95 票）：https://www.kaggle.com/competitions/biohub-cell-tracking-during-development/discussion/744484
  - 5th 3D U-Net + Transformer 关联器（26 票）：https://www.kaggle.com/competitions/biohub-cell-tracking-during-development/discussion/744549
  - 12→95 名复盘：https://www.kaggle.com/competitions/biohub-cell-tracking-during-development/discussion/744912
  - 规则法第 7（48 票）：https://www.kaggle.com/competitions/biohub-cell-tracking-during-development/discussion/716952
  - 分裂指标漏洞与补丁（36 票）：https://www.kaggle.com/competitions/biohub-cell-tracking-during-development/discussion/727154
- 轻读全本：`analysis/deep/biohub-cell-tracking-during-development.md`（Tier B 轻读：对照矩阵/裁决/证据分级/悬案 + 1 图证）
