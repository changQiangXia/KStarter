# Smartphone Decimeter Challenge 2022（精简）

> 主题：tabular（GNSS 定位）｜ 子类：— ｜ 领域：导航定位 ｜ 类别：Research ｜ 截止：2022-07-29 ｜ 队伍数：573 ｜ 指标：定位误差（分米级）
> 出处：`intel/smartphone-decimeter-2022/`（80 条主题索引 + 6 篇 write-up 正文）

## 任务

由智能手机的 GNSS 原始观测（伪距、载波相位等）估计高精度位置（分米级），是"**经典方法强于 ML**"的典型领域。

## 关键要点

- 5th 的观察很关键：他"担心比赛吸引不到人，因为**机器学习在上一届 GNSS 数据上效果并不好**"，但最终竞争水平很高——说明**信号处理/几何方法 + 少量 ML 修正**是本题主流。
- 与常规 Kaggle 赛不同：**领域标准方法（RTK/PPP 类算法）本身就是强基线**。
- 手机 GNSS 的挑战在于噪声项复杂（多径、电离层、硬件偏差）。

## 可迁移要点

- **先确认"领域经典方法 vs ML"的力量对比**：某些领域（定位、信号处理、控制）经典算法仍占优。
- ML 的合理位置是**残差修正/噪声建模**，而非端到端替换。
- 与 Ventilator、G2Net、IceCube 对照：**"物理/经典方法打底、ML 做增量"是稳健路线**。

## 出处

- 讨论区索引：`intel/smartphone-decimeter-2022/topics.md`
- 1st（72 票）：https://www.kaggle.com/competitions/smartphone-decimeter-2022/discussion/341111
- 5th（44 票）：https://www.kaggle.com/competitions/smartphone-decimeter-2022/discussion/340692
