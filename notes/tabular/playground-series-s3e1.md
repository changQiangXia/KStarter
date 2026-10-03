# Playground Series S3E1（坐标驱动回归，RMSE，验证口径之争）

> 主题：tabular ｜ 子类：— ｜ 领域：房产/地理（合成数据） ｜ 类别：Playground
> 截止：2023-01-09 ｜ 队伍数：689 ｜ 机制：标准赛 ｜ 指标：RMSE
> 数据来源：`intel/playground-series-s3e1/`（59 条主题索引 + 6 篇 write-up 正文）

## 1. 任务与数据

- 回归任务，**经纬度坐标是核心信号**（社区公认"coordinates key to victory"）。
- 坐标特征工程工具箱（历史比赛汇总帖）：距离/密度/邻域统计等——跨届可复用的地理特征清单。

## 2. 验证方案（2nd 的关键洞察）

- 多数人把外部数据混入后计算 CV → 分数与 LB 对齐差；
- 2nd 的做法：**先在原始数据（竞赛数据）上做 CV 划分，再把外部数据追加到训练部分**——强制验证集保持竞赛分布，LB 对齐明显改善；同时保留"混合全量划分"的方案做多样性，两者集成。

## 3. 模型家族

| 方案 | 使用者层次 | 关键点 | 出处 |
| --- | --- | --- | --- |
| AutoGluon（8 折 × 多架构 + bootstrap + 3 层堆叠） | 1st | 借公开坐标 FE | topic 377137 |
| 自研 GBDT + Keras NN + 双验证口径集成 | 2nd | CV 口径设计 | topic 377179 |
| 坐标特征工程清单 | 社区 | 跨届复用 | topic 376210 |

## 4. 关键技巧

- **坐标特征工程**：距离、邻域统计、密度类特征（本场胜负手可在公开 notebook 中直接复用）。
- **外部数据的验证口径**："验证集必须来自竞赛分布"——与 S3E2/S5E3 的原数据用法一脉相承。
- AutoGluon 的 3 层堆叠 + bootstrap 就能夺冠——**框架能力已能覆盖中低级手工作业**（1st 明言"没太多时间"）。
- NN 单模 CV 0.59 仍提供显著多样性（2nd 的混合策略）。

## 5. 可迁移性评估

- **可直接迁移**：坐标特征清单；"先在竞赛数据上划分、后并入外部数据"的 CV 协议；外部数据双口径集成；AutoGluon 作为稳健基线。
- **需要前提**：存在地理坐标；外部数据与竞赛数据分布有差异。
- **不建议照搬**：把外部数据混入后计算 CV（口径失真）；小看 AutoML（本场冠军是 AG）。

## 6. 对新手的关键启示

- 有坐标的任务先做地理特征（距离/邻域/密度），这是被反复验证的高杠杆。
- 外部数据的"划分顺序"决定验证可信度：先划竞赛数据，再扩训练集。
- AutoGluon 一类框架是时间有限时的正确选择——并且它也能拿第一。

## 7. 出处

- 1st：AutoGluon 方案（含坐标 FE 出处）：https://www.kaggle.com/competitions/playground-series-s3e1/discussion/377137
- 2nd：验证口径与双口径集成：https://www.kaggle.com/competitions/playground-series-s3e1/discussion/377179
- 坐标特征工程跨届清单：https://www.kaggle.com/competitions/playground-series-s3e1/discussion/376210
