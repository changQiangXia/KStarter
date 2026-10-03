# Playground Series S5E6 - 最优肥料推荐（MAP@K）

> 主题：tabular ｜ 子类：— ｜ 领域：农业（合成数据） ｜ 类别：Playground
> 截止：2025-06-30 ｜ 队伍数：2648 ｜ 机制：标准赛 ｜ 指标：MAP@K（多分类排序）
> 数据来源：`intel/playground-series-s5e6/`（80 条主题索引 + 6 篇 write-up 正文）

## 1. 任务与数据

- 预测目标：为 (土壤, 作物) 组合推荐 7 种肥料中最优的若干种（MAP@K 排序指标）。
- 数据特性（EDA 帖）：目标平衡（各类 12–16%）；(Soil, Crop) 联合分布信号强；数值列近似均匀、**两两 Spearman 相关 < 0.01**，但各肥料会整体平移 N/P/K 的中位数——**信号在比值/交互里，不在原始值里**。

## 2. 验证方案

- 主流 5–10 折 OOF；本场是"低相关数据"的排序任务，CV 与 LB 较稳。
- 2nd 的 L3 集成超 100 个 OOF；3rd 用 Ridge + CV；5th 53 OOF——集成规模再度成为主轴。

## 3. 模型家族

| 方案 | 使用者层次 | 关键点 | 出处 |
| --- | --- | --- | --- |
| RAPIDS cuDF/cuML 快速实验流（72 模型量级） | 1st | 复用其半年来的六大招式 | topic 587393 |
| L3 集成（100+ OOF） | 2nd | 三层结构 | topic 587398 |
| Ridge + CV | 3rd | 简单集成器 | topic 587464 |
| 53 OOF 集成 | 5th | 中等规模 | topic 587392 |

## 4. 关键技巧

- **比值/交互特征优先**（EDA 帖的核心结论）：低相关 ≠ 无信号——堆叠直方图显示各肥料 Nutrient 密度在不同区间出现峰值 → 构造 N/P/K 比值与 (温度, 湿度, 水分) 交互。
- **1st 的"半年招式表"**（社区名人堂式总结）：2024-12 RAPIDS cuDF FE（1st）→ 2025-01 boosting over residuals（2nd）→ 2025-02 原数据使用（1st）→ 2025-03 RAPIDS cuML（2nd）→ 2025-04 cuML 堆叠（1st）→ 2025-05 GPU Hill Climbing（1st）→ 本场组合。**Playground 高手的方法是逐月迭代累积的**。
- MAP@K 类指标要按 k 截断评估、注意每行候选排序（与 EEDI 的 MAP@25 同源）。

## 5. 可迁移性评估

- **可直接迁移**：低相关信息下的比值/交互构造思路；月度方法迭代的档案化习惯；MAP@K 的评估细节。
- **需要前提**：GPU 加速工具链（RAPIDS）用于大规模实验；大量 OOF 存档。
- **不建议照搬**：只看相关性筛选特征（本场相关≈0 但中位数平移有信号）。

## 6. 对新手的关键启示

- "相关性接近 0"不代表特征没用：看分布/中位数/比值，再看两两相关。
- 建立自己的"招式-赛事"对照表（像 1st 那样），比记零散技巧更有复利。

## 7. 出处

- 1st：RAPIDS 快速实验与半年招式表：https://www.kaggle.com/competitions/playground-series-s5e6/discussion/587393
- N/P/K 比值：低相关数据里的隐藏信号：https://www.kaggle.com/competitions/playground-series-s5e6/discussion/583189
- 2nd：100+ OOF 的 L3 集成：https://www.kaggle.com/competitions/playground-series-s5e6/discussion/587398
- 3rd：Ridge 与 CV 就够了：https://www.kaggle.com/competitions/playground-series-s5e6/discussion/587464
- 5th：53 OOF 集成：https://www.kaggle.com/competitions/playground-series-s5e6/discussion/587392
