# Tabular Playground Series - Oct 2022（在线学习赛与"5 分钟的冠军"）

> 主题：tabular ｜ 子类：— ｜ 领域：—（在线学习机制） ｜ 类别：Playground
> 截止：2022-10-31 ｜ 队伍数：463 ｜ 机制：标准赛（在线学习） ｜ 指标：Mean Columnwise Log Loss
> 数据来源：`intel/tabular-playground-series-oct-2022/`（80 条主题索引 + 6 篇 write-up 正文）

## 1. 任务与数据

- 官方 overview 明确指向 **online learning**（并提供 FTLR notebook 参考）：数据按时间流入，需要逐步生成预测——与批量训练范式不同。
- 社区资源帖给出在线学习入门清单（Qwak 对比文、awesome-online-ml 仓库、creme 库视频等）。

## 2. 验证方案

- 在线学习场景的验证接近"前向滚动"：每个时间步只能使用此前数据；离线 K 折与线上机制错位，需按时间结构设计。

## 3. 模型家族

| 方案 | 使用者层次 | 关键点 | 出处 |
| --- | --- | --- | --- |
| 主机方基线方案 | Host | 官方视角 | topic 364908 |
| "100+ 模型集成 + 最后一小时选提交" | 被下架团队 | 冠军 5 分钟后被判作弊 | topic 363288 |
| 在线学习入门资源 | 社区 | FTLR/creme | topic 356584 |

## 4. 关键技巧与警示

- **在线学习的工程要点**：逐样本/逐批更新、概念漂移适应、计算与内存约束；官方指定的 FTLR（Follow-The-Regularized-Leader）是轻量首选。
- **"5 分钟冠军"事件**：一支团队自称训练 100+ 模型做集成、并在最后一小时选提交，随后被平台判定违规下架并申诉——**在线学习赛里"多次查询/联动提交"的规则边界很敏感**，工程炫耀帖也可能是违规案例。
- 内存优化（dtype 转换省 75% 内存）在本场是实用工程帖。

## 5. 可迁移性评估

- **可直接迁移**：FTLR/在线学习工具链认知；逐时间步评估设计；内存压缩工程。
- **需要前提**：赛制确为在线/流式；规则对交互查询的要求要先读清。
- **不建议照搬**：把该队的操作方式当模板（结果是被判违规）；忽视规则边界的"极限优化"。

## 6. 对新手的关键启示

- 遇到"online learning"机制的比赛，先搭 FTLR 基线，再谈模型；它与批量赛是两种游戏。
- 读规则比读方案更优先：本场有团队在"冠军 5 分钟"后被下架，代价巨大。
- 工程优化（内存/速度）在流式场景直接决定可行性。

## 7. 出处

- "5 分钟冠军"事件帖：https://www.kaggle.com/competitions/tabular-playground-series-oct-2022/discussion/363288
- 在线学习入门资源：https://www.kaggle.com/competitions/tabular-playground-series-oct-2022/discussion/356584
- 主机方基线方案：https://www.kaggle.com/competitions/tabular-playground-series-oct-2022/discussion/364908
