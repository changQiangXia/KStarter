# Tabular Playground Series - Apr 2022（AUC，去噪自编码器的跨届血脉）

> 主题：tabular ｜ 子类：— ｜ 领域：—（多传感器序列） ｜ 类别：Playground
> 截止：2022-04-30 ｜ 队伍数：816 ｜ 机制：标准赛 ｜ 指标：ROC AUC
> 数据来源：`intel/tabular-playground-series-apr-2022/`（68 条主题索引 + 6 篇正文）

## 1. 任务与数据

- 二分类 AUC；样本是**多传感器序列**（每样本多步多传感器）。
- 1st 的方案完全建立在**前三个 Playground（Jan/Feb/Mar 2021）的 DAE 血脉**上：沿用"swap 噪声去噪自编码器"思想，仅把模型结构适配为序列。

## 2. 验证方案

- 用 1 折 CV 测试不同 DAE checkpoint 对下游预测的影响，以平衡"更多 epochs 的边际收益 vs 训练时间"；全程受 Kaggle GPU 配额约束。

## 3. 模型家族

| 方案 | 使用者层次 | 关键点 | 出处 |
| --- | --- | --- | --- |
| DAE（LSTM）+ 第二网络 | 1st | 层输出当特征；<30% swap 噪声 | topic 322259 |
| 2nd / 3rd / 5th / 6th | 高位 | 常规加多样线 | topic 322257 |
| 特征工程六大坑 | 社区 | FE 复盘清单 | topic 318527 |

## 4. 关键技巧

- **DAE 的序列版设计**（可复刻细节）：
  - swap 噪声两种：跨样本同位置交换（Seq1-Sensor00-Step02 ↔ Seq2-Sensor00-Step02）、同样本同传感器不同时间步交换；
  - 噪声率低于 30% 最佳（50% 在可承受 epochs 内学不好）；
  - 2 层 LSTM 足够；更大 LSTM 提升但训练成本陡增；
  - 只选部分层的输出当特征（有些层反而伤下游）；
  - 加入 subject count/embedding 无增益；额外 FE 无增益——只用原始缩放传感器数据。
- 用 DAE 表达输入结构、用第二网络预测目标的"两段式表示学习"是表格噪声数据的老配方。

## 5. 可迁移性评估

- **可直接迁移**：swap-noise DAE 的序列适配；噪声率与层选择的经验值；"表示学习 + 下游头"的两段式；checkpoint 影响的下游评估法。
- **需要前提**：输入特征间有可学的结构（传感器序列尤佳）；GPU 预算。
- **不建议照搬**：在此类表示已足够时叠加复杂 FE（本场验证无益）；噪声率拉满。

## 6. 对新手的关键启示

- **跨届复利的活教材**：1st 的方案直接继承 Jan/Feb/Mar 2021 三场社区成果并做序列适配——系列赛的历史帖子就是你的预训练知识。
- DAE 的价值在"理解输入结构"（无论有无标签），层输出是免费特征。
- 特征工程有坑要先读"六大坑"复盘，少走重复路。

## 8. 轻读结论（2026-10 补）

**一句话**：13 路传感器 × 60 步序列 + subject 不相交的二分类：1st 用 **LSTM 去噪自编码器（DAE）自监督 + 预测网络 + 大混合**拿到私榜 0.99249；2nd 的单个 CNN+GRU 私榜 0.989（单独可第 6）；5th 的 tsfresh 9000 特征 + LGBM 也能进前 5。硬约束是 **CV 必须按 subject 分组**。

- 1st（322259）：DAE swap-noise <30%；层输出当特征 + 原始 scaled 序列；spatial dropout >0.35；ElasticNet 混合 4 个 DAE + TPU 模型 + LGBM；单 DAE 私 0.99134，总混合 0.99249。
- 2nd（322257）：40 模型 stacking；单模 4×2D-CNN+GRU+GMP 私 0.989；reshape 后按标签 Stratified（每 index 即完整 subject）；LGBM 元学习器 +0.0013。
- 3rd（322269）：shapelets（tslearn→torch）+ CatBoost stacking；**按 subject 聚合预测 +0.002**；伪标签/HMM/序列拼接失败；powershap 筛特征。
- 5th（322277）：tsfresh ~9000 特征 + 按 subject 归一化 + RFE → LGBM 私 0.97816，再与 LSTM/公开模型加权混合。
- 6th（322622）：每条序列投影 16 维后 13 路独立 4 层 GRU → 私 0.9839。
- 六坑帖（185 票）：kurtosis 是单特征之王；聚合别重复；必须做特征选择；别漏 subject 序列数；**GroupKFold(subject) 不可省**；RF 不如 GBDT。

**裁决**：分组结构决定 CV；序列深度模型为主线，GBDT+统计特征作补充；FE 要针对生成机制并严格筛选；AUC 交概率；组级预测聚合值得一试。

**悬案**：4th/7th–10th 未收录；图证全缺。

## 9. 图表证据

无可用图证（本场归档 0 张可读图，图证缺口已登记）。

## 10. 出处

- 1st：DAE 序列适配全记录：https://www.kaggle.com/competitions/tabular-playground-series-apr-2022/discussion/322259
- 2nd 方案：https://www.kaggle.com/competitions/tabular-playground-series-apr-2022/discussion/322257
- 特征工程六大坑：https://www.kaggle.com/competitions/tabular-playground-series-apr-2022/discussion/318527
- 3rd 方案：https://www.kaggle.com/competitions/tabular-playground-series-apr-2022/discussion/322269
- 5th 方案：https://www.kaggle.com/competitions/tabular-playground-series-apr-2022/discussion/322277
- 6th 方案：https://www.kaggle.com/competitions/tabular-playground-series-apr-2022/discussion/322622
