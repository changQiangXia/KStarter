# Tabular Playground Series - Sep 2022（销量预测，SMAPE，残差驱动工作流）

> 主题：tabular ｜ 子类：— ｜ 领域：零售（合成数据） ｜ 类别：Playground
> 截止：2022-09-30 ｜ 队伍数：1381 ｜ 机制：标准赛 ｜ 指标：SMAPE
> 数据来源：`intel/tabular-playground-series-sep-2022/`（80 条主题索引 + 6 篇 write-up 正文）

## 1. 任务与数据

- 预测目标：多国/多店/多商品销量（SMAPE），与 Jan 2022 同族的乘性销售数据结构。
- 社区资源链：**Jan 2022 的冠军 notebook 被公开为起点**（ambrosm 的高级线性模型）——季度系列之间可以直接继承。

## 2. 验证方案

- 1st 的迭代循环本质上是"分布检查驱动的 CV 实验"：
  （1）检查某列（或时间派生列）的分布；（2）推断它对误差的作用并验证；
  （3）若推断成立就把该效应反向扣除、再找下一个影响更大的因素；
  （4）按影响调整列以利学习；（5）找大误差样本的公共点；（6）把公共点加成特征看误差是否下降。
- 明确的异常事件处理：2020 年 3–5 月的误差被识别为 COVID 影响，用指数型衰减/回升函数建模。

## 3. 模型家族

| 方案 | 使用者层次 | 关键点 | 出处 |
| --- | --- | --- | --- |
| 残差驱动 + 事件校正的线性/混合方案 | 1st | 逆向扣除效应 | topic 388206 |
| Boltzmann 集成 | 2nd | 统计物理视角的集成 | topic 356746 |
| 继承 Jan 2022 冠军 notebook | 社区 | 跨届复用 | topic 349435 |

## 4. 关键技巧

- **"反向扣除"特征工程**：把已确认的效应（周内模式、事件）从目标中先扣掉，让模型专注剩余影响——与 JAN-2022 的残差分析一脉相承。
- 大误差样本的公共点分析 → 转化为特征（类似"错误聚类"思路）。
- 跨届资产：同族比赛的获奖 notebook 直接作为起点（省去从零建模）。

## 5. 可迁移性评估

- **可直接迁移**：残差/大误差聚集分析驱动特征；事件效应显式建模（指数衰减等）；同族赛事继承。
- **需要前提**：结构可分解（乘性/事件）；有同族历史比赛可参考。
- **不建议照搬**：不做验证直接套用往届模型结构（本场有 COVID 等新事件）。

## 6. 对新手的关键启示

- 预测误差不是终点：画"大误差样本"，找它们的公共点，这往往是下一个特征的来源。
- 系列赛是复利资产：先读同族上一届的冠军 notebook，再开始写代码。

## 8. 轻读结论（2026-10 补）

**一句话**："线性/GAM + 强外生特征"的胜利：3rd 用**单个 GAM**（留 3 月块 CV，无集成）拿第 3，并猜测 4–7 名都是 GAM 变体；2nd 复用 TPS Jan 2022 的 **Boltzmann 集成**（5 公开 + 2 自研 notebook）；1st 用"逐列影响归因 + 反推去除 + 误差公共点"的迭代流程，并对 2020 年 3–5 月 COVID 影响用指数项建模。

- 1st（388206）：分布检查 → 影响估计与验证 → 反推去除 → 调整列 → 找大误差样本公共点 → 加特征。
- 2nd（356746）：`exp(b(S−x))` 加权集成，成分含 Ridge/Lasso/Elastic、线性回归、GAM、遗传规划。
- 3rd（356643）：单 GAM；最终只把"圣诞→新年"过渡改成样条。
- FE 合集（43 票）：GDP、教育指数、消费者/商业信心指数、封锁日期、节假日；比率特征（34 票）、周期性占用（28 票）、分层时序（34 票）。
- 方法资源：时序 CV 指南（38 票）、Rob Mulla 教程（62 票）、SMAPE 陷阱（30 票）、Jan 2022 冠军 notebook。

**裁决**：先补外生/事件特征，用线性/GAM 类可解释模型；CV 用留块而非随机折；把残差当线索迭代；复用系列赛历史方案。

**悬案**：1st 细节少；4th–7th 是否 GAM 未核实；本场 0 图。

## 9. 图表证据

无可用图证（本场归档 0 图，图证缺口已登记）。

## 10. 出处

- 1st：残差驱动的工作流：https://www.kaggle.com/competitions/tabular-playground-series-sep-2022/discussion/388206
- 2nd：Boltzmann 集成：https://www.kaggle.com/competitions/tabular-playground-series-sep-2022/discussion/356746
- Jan 2022 冠军 notebook 公开：https://www.kaggle.com/competitions/tabular-playground-series-sep-2022/discussion/349435
- 3rd：单 GAM：https://www.kaggle.com/competitions/tabular-playground-series-sep-2022/discussion/356643
- FE 合集（43 票）：https://www.kaggle.com/competitions/tabular-playground-series-sep-2022/discussion/351098
- SMAPE 的陷阱（30 票）：https://www.kaggle.com/competitions/tabular-playground-series-sep-2022/discussion/349553
