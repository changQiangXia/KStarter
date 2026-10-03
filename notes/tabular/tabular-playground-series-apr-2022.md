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

## 7. 出处

- 1st：DAE 序列适配全记录：https://www.kaggle.com/competitions/tabular-playground-series-apr-2022/discussion/322259
- 2nd 方案：https://www.kaggle.com/competitions/tabular-playground-series-apr-2022/discussion/322257
- 特征工程六大坑：https://www.kaggle.com/competitions/tabular-playground-series-apr-2022/discussion/318527
