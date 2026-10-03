# Biohub - Cell Tracking During Development 轻量深读（Tier B）

> 赛事：Research ｜ 主题 cv（3D 细胞追踪）｜ 3947 队 ｜ 代码赛 ｜ 指标：节点数校正的 edge Jaccard + 0.1×division Jaccard
> 材料基础：`digests/biohub-cell-tracking-during-development.md`（6 篇正文：1st 744801 / 3rd 744484 / 5th 744549 / 14th 744486 / 12→95 名复盘 744912 / 欢迎帖 716062；80 条主题索引）+ 30+ 张图
> 轻读时间：2026-10（Tier B B08）

## 1. 一句话重述与数字账

在斑马鱼胚胎的 3D 时序影像里追踪细胞并识别分裂。真正的考点是**"标注极稀疏（仅约 2.8% 的细胞被标）下，把检测、分裂识别与连线评分都学出来"**：1st 用"检测器 + **Soon Net（分裂状态 + 占用图）** + 学习式 linker + 贪心解码"；3rd/5th 走"检测 + 光流 + 图优化/ILP"；同时全场用规则/图修复兜底，并互相印证"训练数据里存在重复帧与漂移帧"这一数据缺陷。

| 关键数字 | 值 | 来源 |
| --- | --- | --- |
| 1st（744801，76 票，solo gold） | 四段式（图 1）：① **检测**：3D U-Net（~3.1M）+ Cellpose 风格头（前景 + 指向中心的流场），**轻量 MAE 预训练**（50% 掩码但每块仅 2×4×4 体素，"不让模型去幻觉整细胞"）→ 用**手工标注 1800 个细胞 + GT 节点上的 4.305µm 印章**微调 → **伪标签重训**（5 折平均 + 4× flip TTA，用公共 twoPass 追踪器过滤 min length>3）；② **Soon Net**（236K CNN + 508K transformer）：看每个细胞 t−1/t/t+1 的三帧裁剪，预测**分裂状态（interphase / soon-to-divide / just-divided）**与**占用图**（continuation/division 两类，"它在哪里、要到哪里去"）；训练技巧：大 FOV 抖动（z ±3、xy ±16）防"只看中心"、时间步增广（t±2/3）、错误类型图在 top-512 体素上加 BCE 防幽灵斑、硬负例挖掘（2492 个难 interphase）、**把分裂样本从 GT 的 151 个扩到 515 个**；③ **学习式 linker**（transformer，LightGlue 启发）：对 t→t+1 的边打分并判定分裂；④ 贪心解码（division refractory、缺口回填、直线拟合）；5 折严格 OOF；自评"soon-to-divide 单点把公榜从 ~0.925 抬到 ~0.963" | 744801 |
| 3rd（744484） | 六段式：① **检测集成**（2.5D U-Net 热图 + 3D SegResNet，占 55% 运行时间）② **稠密 3D 光流**（帧间位移场）③ 用运动校正后的位置匹配细胞 ④ **分裂识别**（原始图 + 运动对齐图，另有"分裂前/后阶段"辅助模型）⑤ **谱系图优化**（联合选择普通边与分裂事件）⑥ 后处理（补短缺口、删小连通域、精修节点坐标）；CV 0.977801（division Jaccard 0.540107），公榜 0.977（0.52），私榜 0.967（0.47） | 744484 |
| 5th（744549） | 三段式：3D U-Net 检测 + **Transformer linker** + **多阶段 ILP 追踪**（整数规划构轨迹）；5 折 + 8 TTA；**关键发现**：训练数据里有"**重复帧**（与下一帧逐字节相同）"与"**漂移帧**（整幅图跳 14µm）"；在验证中剔除这些帧的边后 CV 大涨但 LB 不变 → **隐藏测试集没有大漂移**（这解释了很多人 CV-LB 不匹配）；训练时去掉重复帧并纠正漂移能让同一折模型私榜 +0.011，但公榜下降，最终未采用 | 744549 |
| 12→95 名复盘（744912） | 稀疏标注的处理：把"模型预测但非 GT"的位置**排除在检测损失之外**（pseudo-unlabeling，而非当作正样本），使负样本权重能从 0.01 提到 0.1，训练更快更准；最终用多 checkpoint 加权混合 + 专家 edge 头 + 整数规划构谱系（每细胞 ≤1 父 ≤2 子）+ 图修复（补缺口/重连/删短轨）+ **XY 网格原点 +2 体素校正**；公榜 0.969 → 私榜 0.929 的对照说明榜面波动 | 744912 |
| 社区侧 | "**规则法意外地强？**"（48 票，7 名、无学习）；"**当心 GT 轨迹里的跳跃**"（42 票）；"**Division Metric 的漏洞与补丁**"（36 票）；"18.5GB 全标注合成 3D 显微数据（含 16.5 万次分裂）"（65 票）；"focus3d：最好的 3D 细胞分割之一"（40 票） | 社区 |

## 2. 逐方案对照矩阵

| 维度 | 1st | 3rd | 5th | 12→95 |
| --- | --- | --- | --- | --- |
| 检测 | 3D U-Net（Cellpose 头）+ 轻量 MAE + 伪标签 | 2.5D U-Net + 3D SegResNet 集成 | 3D U-Net（5 折 + 8 TTA） | 复用公共管线 + 微调 |
| 分裂建模 | **Soon Net（状态 + 占用图）** | 独立的"分裂前/后阶段"辅助模型 | — | 分裂分类器否决 |
| 连线 | 学习式 transformer linker | 图优化（联合选边与分裂） | **ILP** | 整数规划 + 图修复 |
| 数据缺陷 | 伪标签+人工复核 | — | **重复帧/漂移帧诊断** | pseudo-unlabeling |
| 指标 | edge Jaccard + 0.1×div Jaccard | 同 | 同 | 同（+2 体素原点校正） |

## 3. 共识、分歧与裁决

### 共识一：检测是上限，但稀疏标注要求"宽容的损失/伪标签"（1st/3rd/12→95）

3rd 说"检测占 55% 运行时间、下游全靠它"；1st 花一个半月攻检测；12→95 用 pseudo-unlabeling 防止把未标注细胞当背景。**裁决**：稀疏标注赛里，检测目标必须显式处理"未标注≠负样本"（掩掉预测点或用印章式弱监督），否则负样本权重永远上不去。置信度：高。

### 共识二：分裂是独立子问题，要单独建模（1st/3rd/12→95）

1st 的 Soon Net 把分裂识别做成"状态 + 占用图"（并说它单独就把公榜从 0.925 抬到 0.963）；3rd 有专职的分裂前后辅助模型；12→95 用分裂分类器否决可疑分裂。**裁决**：分裂事件的样本量极小（GT 仅 151 次）→ 必须用挖掘/增广扩充，并放在独立的模型/判别器里。置信度：高。

### 共识三：训练数据本身有系统性缺陷（5th/42 票帖/36 票帖）

5th 定位了重复帧与 14µm 漂移帧；社区帖提醒"GT 轨迹有跳跃"、并讨论"分裂指标的漏洞与补丁"。**裁决**：3D 追踪赛先做数据审计（逐帧一致性、漂移、GT 连续性）；训练/验证要一致地剔除这些污染帧，否则 CV-LB 会脱钩。置信度：高（多队独立发现）。

### 分歧一：端到端学习 vs 图优化/ILP

1st 的学习式 linker + 贪心解码；3rd 的图优化联合选边；5th 的 ILP；12→95 的整数规划 + 图修复。**裁决**：两者互补——学习式打分负责"边/分裂的局部概率"，图优化负责"全局约束（每细胞 ≤1 父 ≤2 子）"；顶配方案是"学习打分 + 全局求解"。置信度：高。

### 事件：规则法能到第 7（48 票帖）

有队伍用**无学习的规则法**拿到第 7（gold zone）。**裁决**：说明本场的"几何/强度/速度手作特征"依然强（1st 也说细胞追踪领域不用大模型、靠 handmade 特征），学习方法的价值在于补上"分裂识别"与"难例"。置信度：中高。

## 4. 证据分级

| 断言 | 等级 | 说明 |
| --- | --- | --- |
| 1st 的四段管线、Soon Net 细节与 +0.038 公榜 | 自述 + 总览图 + 多图/GIF | 高 |
| 3rd 的六段式与 CV/公榜/私榜三档分数 | 自述 + 管线图 | 高 |
| 5th 的重复帧/漂移帧诊断（CV 涨 LB 不变） | 自述 + 漂移图 | 中高 |
| 12→95 的 pseudo-unlabeling 与图修复细节 | 自述 | 中高 |
| 规则法第 7 | 社区帖（48 票） | 中 |

## 5. 悬案与缺口（登记）

- 2nd/4th/6th–11th/14th 的方案未细读；"Division Metric exploit"（36 票）与"18.5GB 合成数据"（65 票）未细读；
- 1st 的 Soon Net 独立评分（0.9270/0.9288）与最终集成分数的完整链路未给全；
- 私榜与公榜的洗牌幅度（12→95 等）未系统整理；
- 归档 30+ 图（1st 的 10 张、3rd/5th 的管线与漂移图等）为图证来源。

## 6. 图表证据

![1st 的四段式追踪管线](../../intel/biohub-cell-tracking-during-development/bodies/744801_img/01.png)

**图 1**（topic 744801）：① Detector（3D U-Net 前景+流场 → 实例掩码）；② Soon Net（三帧裁剪 → 分裂状态 + 占用图）；③ Learned linker（t↔t+1 交叉注意力 → 边分与分裂分叉头）；④ Decode（贪心配置、分裂不应期、缺口回填、直线拟合）→ 谱系（节点+边）。下方标注训练侧：MAE 预训练 → R1 GT 印章+手绘掩码 / R2 教师伪标签 → Soon Net 的 OOF 硬负例 → linker 只在已标注边上算 NLL、分裂过采样 8×；5 折严格 OOF。

## 7. 出处

- 1st（76 票）：https://www.kaggle.com/competitions/biohub-cell-tracking-during-development/discussion/744801
- 3rd：https://www.kaggle.com/competitions/biohub-cell-tracking-during-development/discussion/744484
- 5th：https://www.kaggle.com/competitions/biohub-cell-tracking-during-development/discussion/744549
- 12→95 名复盘：https://www.kaggle.com/competitions/biohub-cell-tracking-during-development/discussion/744912
- 规则法第 7（48 票）：https://www.kaggle.com/competitions/biohub-cell-tracking-during-development/discussion/716952
- 分裂指标漏洞（36 票）：https://www.kaggle.com/competitions/biohub-cell-tracking-during-development/discussion/727154
