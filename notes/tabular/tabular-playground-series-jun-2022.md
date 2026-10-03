# Tabular Playground Series - Jun 2022（RMSE，缺失值条件分布与去噪自编码器）

> 主题：tabular ｜ 子类：— ｜ 领域：—（合成数据，缺失值密集） ｜ 类别：Playground
> 截止：2022-06-30 ｜ 队伍数：844 ｜ 机制：标准赛 ｜ 指标：RMSE
> 数据来源：`intel/tabular-playground-series-jun-2022/`（70 条主题索引 + 6 篇 write-up 正文）

## 1. 任务与数据

- 核心难点：**多列缺失**，且"两列以上同时缺失时 F4 的条件分布"是胜负手——不是简单的填充，而是要估计 `P(F4 | 缺失模式)`。
- 行级结构：F1/F3 可均值填充、F2 直接忽略（1st 的取舍）；缺失模式本身携带信息（参见 aug-2022 的缺失显著性）。

## 2. 验证方案

- 常规 K 折；社区帖系统梳理插补方法谱系（删行/删列/统计量填充/半监督视角/最大似然 FIML/多重插补/MICE）。

## 3. 模型家族

| 方案 | 使用者层次 | 关键点 | 出处 |
| --- | --- | --- | --- |
| 去噪自编码器做条件插补 | 1st | 掩码感知的嵌入与输出 | topic 334331 |
| 插补方法综述 | 社区 | FIML/MICE 等 | topic 328568 |
| 冠军技巧汇总 | 社区 | 多种路线对比 | topic 334415 |

## 4. 关键技巧（1st 的 DAE 设计，逐条可复刻）

- **双掩码输入**：把"原始缺失位置"（source null matrix）与"随机掩码"（每行至少掩一个值）合并为输入掩码；用随机掩码构造自监督去噪任务。
- **特征与掩码的嵌入相加**：每个特征与其掩码分别线性投影到嵌入维（16），相加后再展平——比直接 dropout 效果好；点积注意力反而更差。
- **掩码条件输出**：最终输出只在被掩位置取网络预测，未掩位置直接用输入——**未掩位置梯度为零**，网络只学插补贡献（聚焦机制）。
- MLP 细节：LayerNorm + 跳连 + Mish，7 层，宽度到 2048（更大受算力限制）。

## 5. 可迁移性评估

- **可直接迁移**：DAE 条件插补框架（任何"缺失模式敏感"的表格任务）；掩码嵌入与掩码条件损失；"哪些列填、哪些列弃"的显式取舍。
- **需要前提**：缺失比例可观、缺失模式与目标相关；GPU 训练预算。
- **不建议照搬**：把插补当预处理小事（本场是核心建模问题）；均值填充后直接套 GBDT（忽视条件分布）。

## 6. 对新手的关键启示

- 缺失值问题的最高形态是**条件分布估计**：`P(缺失值 | 其它可见值, 缺失掩码)`；DAE 是一种通用实现。
- 掩码要"显式"进入模型：把缺失位置当特征而非噪声。
- 插补方法有成熟谱系（FIML/MICE），先读综述再动手。

## 8. 轻读结论（2026-10 补）

**一句话**：插补赛的难点全部集中在 **F4 的多值缺失条件分布**：1st 用带掩码的**去噪自编码器**（特征/掩码双嵌入 + masked MSE）拿到私榜 0.83343；2nd 用"按缺失数分 6 组 + 逐列回归"卡在 ~0.8358；F1/F3 用均值/描述统计即可，F2 被普遍忽略。

- 1st（334331）：随机二项掩码（每行至少 1 个）+ 源缺失 dummy；16 维特征/掩码嵌入相加；7 层 mish+LayerNorm+skip；输出 `x_pred*m + x_mi*(1-m)`；masked MSE；PyTorch×3 + TF 后条件集成；私榜 0.83351 → 0.83343。
- 2nd（334319）：复用 2022-05 TPS 冠军方案；F4 按 0–5 个缺失分 6 组训练（远超 80 个回归器）。
- 4th（334497）：均值/中位数基线 0.86–0.90；F4 用 Keras 稠密网；"na count of each record" 是关键视角。
- 8th/16th/17th（334415）：MLM 式网络集成 / 重型 NN / 按缺失数建模；判断公榜主要由 F4 构成。
- 资源：插补综述（59 票）、逐列回归 80 模型框架（28 票）、MissForest/missingpy（27 票）。

**裁决**：按缺失模式分解问题；顶部用掩码式自监督条件建模（DAE/MLM），无 GPU 时用缺失模式分组回归；先读赛题"与往届相似"的元信息。

**悬案**：3rd/5th–7th 未收录；特征语义未归档；通用插补器量化表现缺失。

## 9. 图表证据

![DAE 架构](../../intel/tabular-playground-series-jun-2022/bodies/334331_img/01.png)

**图 1**（topic 334331）：0 填充 + 掩码双嵌入 → 7 层 MLP → 条件输出 + masked MSE。

## 10. 出处

- 1st：去噪自编码器方案：https://www.kaggle.com/competitions/tabular-playground-series-jun-2022/discussion/334331
- 插补技术综述：https://www.kaggle.com/competitions/tabular-playground-series-jun-2022/discussion/328568
- 冠军技巧汇总：https://www.kaggle.com/competitions/tabular-playground-series-jun-2022/discussion/334415
- 2nd：缺失模式分组：https://www.kaggle.com/competitions/tabular-playground-series-jun-2022/discussion/334319
- 4th 方案：https://www.kaggle.com/competitions/tabular-playground-series-jun-2022/discussion/334497
- 逐列回归框架：https://www.kaggle.com/competitions/tabular-playground-series-jun-2022/discussion/328369
