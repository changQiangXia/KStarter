# UM - Game Playing Strength of MCTS Variants

> 主题：tabular ｜ 子类：— ｜ 领域：游戏 AI ｜ 类别：Research
> 截止：2024-12-02 ｜ 队伍数：1608 ｜ 机制：代码赛 ｜ 指标：预测强度（回归/排序）
> 数据来源：`intel/um-game-playing-strength-of-mcts-variants/`（80 条主题索引 + 6 篇 write-up 正文）

## 1. 任务与数据

- 预测目标：预测不同 MCTS（蒙特卡洛树搜索）变体在不同棋类游戏上的**对局强度**。
- 数据形态：表格型特征（算法参数 + 游戏类型 + 对局结果统计）。
- 构造陷阱：
  - 强度是**组合效应**（算法 × 游戏），存在强交互；
  - 特征工程需要理解 MCTS 机制；
  - 评估可能包含"未见组合"的泛化。

## 2. 方案谱系

| 方案 | 名次 | 关键点 |
| --- | --- | --- |
| **对每个游戏的起始局面跑数秒树搜索，生成"平衡度"特征** | 1st | 把**树搜索当作特征生成器**：用搜索得到的局面平衡性描述游戏的内在难度，再喂给表格模型 |

## 3. 关键技巧

- **把"昂贵但可计算"的模拟结果当特征**（搜索/仿真的输出作为表格特征）。
- **特征源自领域机制**（平衡度、分支因子等博弈论量）。
- 表格模型处理"算法 × 游戏"的交互（可显式构造交叉特征或让 GBDT 学习）。

## 4. 可迁移性评估

- **可直接迁移**：
  - **用仿真/搜索生成元特征**（在算力允许时非常有效，也见于 AutoML、系统性能预测）；
  - 领域机制导出的特征（分支因子、平衡度）。
- 需要前提：可运行的目标环境（本场是游戏引擎）；数秒级的搜索预算。
- 不建议照搬：只用手工参数特征（缺少环境内在难度的刻画）。

## 5. 对新手的关键启示

1. **"跑仿真生成特征"是一个被低估的强力手段**（算力换特征）。
2. 组合型任务（A×B）要显式考虑交互。
3. 与 NeuroGolf/Santa 系列对照：**同一场比赛里，搜索既能当解法也能当特征来源**。

## 6. 出处

- 讨论区索引：`intel/um-game-playing-strength-of-mcts-variants/topics.md`（80 条）
- 已收录 write-up（6 篇）：
  - 1st（95 票）：https://www.kaggle.com/competitions/um-game-playing-strength-of-mcts-variants/discussion/549801
  - 3rd 两阶段翻转增强（68 票）：https://www.kaggle.com/competitions/um-game-playing-strength-of-mcts-variants/discussion/549588
  - 5th（56 票）：https://www.kaggle.com/competitions/um-game-playing-strength-of-mcts-variants/discussion/549585
