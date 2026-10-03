# Google Brain - Ventilator Pressure Prediction

> 主题：science（控制/时序）｜ 子类：— ｜ 领域：医疗 ｜ 类别：Research
> 截止：2021-11-03 ｜ 队伍数：2605 ｜ 机制：标准赛 ｜ 指标：MAE（逐时间步气压）
> 数据来源：`intel/ventilator-pressure-prediction/`（80 条主题索引 + 6 篇 write-up 正文）

## 1. 任务与数据

- 预测目标：给定呼吸机的**控制输入序列**（吸气/呼气、流量等），预测气道压力随时间的曲线（模拟环境）。
- 数据形态：多组时间序列（每次呼吸为一个样本）；**部分数据由确定性控制器生成**。
- 构造陷阱（本场最特殊）：**数据中有 2/3 可由物理/控制规则精确还原**——冠军明确说"一个匹配算法能完美预测 66% 的数据"，剩下 34% 才需要深度学习。

## 2. 方案谱系

| 方案 | 名次 | 关键点 |
| --- | --- | --- |
| **深度学习（LSTM/Transformer 混合）+ 匹配算法** | 1st | 两大块：① 多架构融合覆盖 34% 的困难数据；② **匹配算法完美预测 66%** 的数据（利用控制逻辑的确定性） |
| Conv1d + 堆叠 LSTM（单模型 0.0975，未用 PID 控制器） | 3rd | 分层验证（按 `type_rc` 分层）；结构简洁 |
| 拉普拉斯分布损失 | 9th | 用分布假设改进损失函数 |

## 3. 关键技巧

- **先识别数据的确定性成分**：本场是"控制逻辑可复现"的典型案例——**规则引擎 + 模型**的混合结构。
- **分层验证**（按呼吸类型分层）。
- **简单结构 + 恰当损失**（Conv1d+LSTM、拉普拉斯损失）。

## 4. 可迁移性评估

- **可直接迁移**：
  - **"确定性部分用规则、随机部分用模型"的分工**（与 ICR 的物理模型+NN、ARIEL 的贝叶斯+参数化同源）；
  - 分层验证；
  - 分布型损失（拉普拉斯/分位数）处理非正态误差。
- 需要前提：对数据生成机制的逆向理解。
- 不建议照搬：直接端到端学习全部数据（浪费了可解析的 2/3）。

## 5. 对新手的关键启示

1. **先问"数据里有多少是可解析的"**——本场 66% 的分数来自规则匹配。
2. 与前后的科学赛对照：**"物理/规则 + 模型"混合是科学类比赛的稳定范式**。

## 6. 出处

- 讨论区索引：`intel/ventilator-pressure-prediction/topics.md`（80 条）
- 已收录 write-up（6 篇）：
  - 1st Winner's Writeup（326 票）：https://www.kaggle.com/competitions/ventilator-pressure-prediction/discussion/285256
  - 3rd Conv1d+LSTM（221 票）：https://www.kaggle.com/competitions/ventilator-pressure-prediction/discussion/285330
  - 9th 拉普拉斯损失（123 票）：https://www.kaggle.com/competitions/ventilator-pressure-prediction/discussion/285353
