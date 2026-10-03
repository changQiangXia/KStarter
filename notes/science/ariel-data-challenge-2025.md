# ARIEL Data Challenge 2025

> 主题：science ｜ 子类：— ｜ 领域：天文 ｜ 类别：Featured
> 截止：2025-XX-XX ｜ 队伍数：800+ ｜ 机制：代码赛 ｜ 指标：光谱反演误差
> 数据来源：`intel/ariel-data-challenge-2025/`（80 条主题索引 + 6 篇 write-up 正文）

## 1. 任务与数据

- 预测目标：由模拟的系外行星凌星光谱反演大气参数（与 2024 届同类）。
- 数据形态：仿真光谱 + 物理模型；噪声与系统误差可控。
- 构造陷阱：信号微弱、参数间存在退化（不同参数组合可产生相似光谱）。

## 2. 方案谱系

| 方案 | 名次 | 关键点 |
| --- | --- | --- |
| **纯贝叶斯推断**（"Bayesian Inference, of course"） | 1st | 与 2024 届亚军同一作者：他在 2024 用贝叶斯拿第 2，2025 终于用同一路线夺冠；**公开了完整开发历史仓库** |
| 其他方案 | 见讨论区 | |

## 3. 关键技巧

- **贝叶斯推断给出后验分布**，天然处理参数退化与不确定性（比点估计更适合反演问题）。
- **公开完整开发历史**（含失败尝试）——对社区价值极高，也是 1st 明确致谢社区后的回馈。
- 物理模型驱动的参数化。

## 4. 可迁移性评估

- **可直接迁移**：
  - **反演类问题优先考虑贝叶斯方法**（后验 > 点估计）；
  - 把完整开发历史开源（自己未来复盘与社区复用双赢）。
- 需要前提：概率编程工具与对物理模型的掌握。
- 不建议照搬：默认"端到端深度学习更好"。

## 5. 对新手的关键启示

1. **同一作者两年连续用贝叶斯路线**（第 2 → 第 1），说明这条路线在科学反演里的稳定性。
2. 与 ARIEL 2024、Hull Tactical、Otto 合并观察：**"不用深度学习的方案"在 Kaggle 上常被低估**。

## 6. 轻读结论（2026-10 补）

**一句话**：系外行星光谱反演——**预处理/校准（+0.01~0.05）是主战场，D(λ) 与 σ(λ) 必须分别建模/校准**；贝叶斯反演与物理特征+ML 两条路线都能登顶。

- 1st（56 票）：预处理（jitter PCA、进阶波长合并 +0.01）→ 贝叶斯（高斯先验：噪声/星谱/漂移/凌星 batman/深度均值+FGS 高斯+AIRS GP+PCA；迭代线性化 + 超参梯度下降；网格→BFGS 初始化）→ Fudging（对 D/σ 经验修正）；完整开发史开源（图 1）。
- 3rd（32 票）：8σ 时间剔除 **+0.05**、AIRS 按频率 32 块 **+0.025**、梯度极值相位检测、CNN + Rational Quadratic NN 集成。
- 7th：Phase detector → 物理特征 → NN 差分修正 → **GBM 调 σ 尺度** → 伪标（CV ~0.42）。

**裁决**：预处理决定上限；σ 是第二引擎；梯度极值相位检测是轻量方案；贝叶斯与 ML 各有优势。

**悬案**：6th/9th 未细读；ExoSim2 生成器与官方指标实现未入库。

## 7. 图表证据

![1st 的先验分解](../../intel/ariel-data-challenge-2025/bodies/609888_img/04.png)

**图 1**（topic 609888）：Raw signal = (Star spectrum × Drift × Transit) + Noise 的时×波长分解。

## 8. 出处

- 1st（56 票）：https://www.kaggle.com/competitions/ariel-data-challenge-2025/discussion/609888
- 3rd（32 票）：https://www.kaggle.com/competitions/ariel-data-challenge-2025/discussion/609252
- 7th（609210）：https://www.kaggle.com/competitions/ariel-data-challenge-2025/discussion/609210

- 讨论区索引：`intel/ariel-data-challenge-2025/topics.md`
- 已收录 write-up（6 篇）：见该比赛讨论区（1st 含训练/提交代码与完整开发历史仓库）
- 轻读全本：`analysis/deep/ariel-data-challenge-2025.md`（Tier B 轻读：对照矩阵/裁决/证据分级/悬案 + 1 图证）
