# Santa 2022（精简）

> 主题：sim-agent ｜ 子类：— ｜ 领域：组合优化 ｜ 类别：Featured ｜ 截止：2023-01-XX ｜ 队伍数：1000+ ｜ 指标：解的质量
> 出处：`intel/santa-2022/`（80 条主题索引 + 6 篇 write-up 正文）

## 任务

年度 Santa 优化赛（2022 版）：在给定约束下求最优构造，难度由主办方刻意校准（2nd 提到"额外的扭转（arm twist）"增加了复杂度）。

## 关键要点

- 2nd 的方案围绕**寻找局部最优**展开，并提到"比冠军晚 48 小时到达局部最优"——**发现最优解的时间点本身就是竞争的一部分**。
- 作者评价该场"校准得很好"（calibrated）：难度既能区分水平，又不至于无从下手。
- 多支队伍先后独立到达同一局部最优（C-number、Kibuna），说明这类问题的解空间有明确的"吸引力盆地"。

## 可迁移要点

- **优化赛的关键是搜索策略 + 时间管理**：谁能更快到达更优盆地。
- 关注主办方对难度的"校准"设计（可作为自己出题的参考）。

## 轻读结论（2026-10 补）

**一句话**：机械臂 + TSP 的组合优化题——全场的标准范式是**"先在像素空间解带路径依赖约束的 TSP，再把路径 lift 成构型"**；顶端三队分数都落在 **74075.7** 附近，与社区 TSP 下界 74073.73 只差约 2 分。

- 1st（379167）：**GA-EAX-restart** 解带 4 条罚分约束的 TSP（x<0 前需 ≥64 步 y 向移动、2x<总 y 位移、四对角点不可直线相连、跨象限需 ≥128 步）；成本用 64/128 位整数、种群可保存/合并/断点续跑；构型恢复 = DP（32/64 臂 3D 表）+ 束宽 500 的 beam search；30 vCPU 一天内出 LB 第一。
- 2nd（379086）：自写 C++ lifting（15 分钟/机）；发现"可 lift 是软约束"（硬约束在原点附近），用递增罚分的自定义 TSP（LKH3 混合）拿到 ~74076；**IPT 合并 + 遗传算法在 30 分钟内把分数推到 74075.706541**。
- 4th（379080）：Concorde + GA（74083）；三类额外约束：太早画左半区、太早向右走、**沿外圈第二圈像素走**（图像 resize 伪影）。
- 9th（379150）：LKH v3 + 自写 LK（PyPy 提速 10×）+ 人工修路径 + 可视化。
- 社区：Web 可视化器（107 票）、76000 配方帖（88 票）、TSP 下界 74073.7278（42 票）。

**裁决**：构型类优化要解耦"路径/构型"两层并把构型约束罚分化；先推原点附近的可行性条件；后期从探索切换到合并历史解。

**悬案**：3rd/5th–8th 方案缺失；1st 的精确分数未给；最优性无官方证明。

## 图表证据

![1st 的最优路线可视化](../../intel/santa-2022/bodies/379167_img/01.png)

**图 1**（topic 379167）：覆盖全部像素的最优路线（颜色=时间），展示蛇形填充与边界处理。

## 出处

- 讨论区索引：`intel/santa-2022/topics.md`
- 已收录 write-up（6 篇）：见该比赛讨论区（2nd 方案等）
- 1st（80 票）：https://www.kaggle.com/competitions/santa-2022/discussion/379167
- 2nd（81 票）：https://www.kaggle.com/competitions/santa-2022/discussion/379086
- 4th（73 票）：https://www.kaggle.com/competitions/santa-2022/discussion/379080
- 9th（30 票）：https://www.kaggle.com/competitions/santa-2022/discussion/379150
- Web Visualizer（107 票）：https://www.kaggle.com/competitions/santa-2022/discussion/369788
- TSP 下界（42 票）：https://www.kaggle.com/competitions/santa-2022/discussion/378537
- 轻读全本：`analysis/deep/santa-2022.md`（Tier B 轻读：对照矩阵/裁决/证据分级/悬案 + 1 图证）
