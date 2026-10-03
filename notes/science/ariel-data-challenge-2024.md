# ARIEL Data Challenge 2024

> 主题：science ｜ 子类：— ｜ 领域：天文 ｜ 类别：Featured
> 截止：2024-XX-XX ｜ 队伍数：1000+ ｜ 机制：代码赛 ｜ 指标：光谱反演误差
> 数据来源：`intel/ariel-data-challenge-2024/`（80 条主题索引 + 6 篇 write-up 正文）

## 1. 任务与数据

- 预测目标：由模拟的**系外行星凌星光变/光谱信号**反演大气参数。
- 数据形态：仿真光谱与光变曲线（凌星 ingress/egress 形状）；物理模型明确、噪声可控。
- 构造陷阱：
  - 信号微弱、依赖对凌星几何的理解；
  - 仿真数据的生成机制（噪声、系统误差）决定了有效特征。

## 2. 方案谱系

| 方案 | 名次 | 关键点 |
| --- | --- | --- |
| **纯贝叶斯推断（完全不用深度学习）** | 2nd | 作者主张贝叶斯方法在深度学习时代被严重低估，并强调其可迁移到现实问题 |
| 多项式拟合凌星边界 | 4th | 用两段二次多项式 + 连线拟合 ingress/egress 的起止点（在信号前后半段分别处理） |
| 1st / 5th / 6th | 其他 | 见讨论区 |

## 3. 关键技巧

- **物理驱动的参数化拟合**：把凌星形状参数化（分段多项式）后拟合，比端到端网络更稳。
- **贝叶斯推断**：给出后验分布而非点估计，天然处理不确定性。
- **信号处理优先**：先理解信号的物理结构，再决定用不用神经网络。

## 4. 可迁移性评估

- **可直接迁移**：
  - **先做物理/信号层面的参数化建模**，把神经网络留给"参数化做不到的部分"。
  - 贝叶斯方法在小数据、强结构场景下优于深度模型（本场亚军即证据）。
- 需要前提：对问题物理机制的理解（凌星几何、光谱形成）。
- 不建议照搬：默认"end-to-end 深度学习一定更好"。

## 5. 对新手的关键启示

1. **有物理模型时，先做参数化拟合**——它常比深度模型更强且可解释。
2. **贝叶斯方法被低估**（本场亚军专门为此发声）。
3. 与 Hull Tactical、Otto 等场次共同说明：**"不用 ML"也能拿奖牌**。

## 6. 出处

- 讨论区索引：`intel/ariel-data-challenge-2024/topics.md`（80 条）
- 已收录 write-up（6 篇）：
  - 2nd 纯贝叶斯（125 票）：https://www.kaggle.com/competitions/ariel-data-challenge-2024/discussion/543853
  - 1st（51 票）：https://www.kaggle.com/competitions/ariel-data-challenge-2024/discussion/544317
  - 5th（36 票）：https://www.kaggle.com/competitions/ariel-data-challenge-2024/discussion/543760
  - 6th（57 票）：https://www.kaggle.com/competitions/ariel-data-challenge-2024/discussion/543666
