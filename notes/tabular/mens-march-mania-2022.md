# March Machine Learning Mania 2022 - Men's

> 主题：tabular ｜ 子类：sports ｜ 领域：体育 ｜ 类别：Community ｜ 截止：2022-03-15 ｜ 队伍数：500+ ｜ 指标：Brier
> 出处：`intel/mens-march-mania-2022/`（120 条主题索引 + 8 篇正文，含赛后修复补采）

## 1. 任务与数据

- 预测 2022 年 NCAA 男篮锦标赛每场胜负概率（Brier 评分）；同年女子赛单独设赛。
- 外部数据生态：538 团队评分（raddar 汇编，历届通用）、往届赛果、球队特征聚合。

## 2. 验证方案

- 社区惯例：按赛季时间切分 + Brier/对数损失校准评估（体育概率赛的通用纪律，与 Mania 2023–2026 一致）。
- 本场揭示的"复现陷阱"：照搬旧代码时，**代码中的赛季常量也是逻辑的一部分**（详见下）。

## 3. 模型家族

| 方案 | 使用者层次 | 关键点 | 出处 |
| --- | --- | --- | --- |
| "复用 raddar 2018 女子赛方案" | 1st | 一句话方案："没有新东西" | topic 317145 |
| 球队 embedding（torch Embedding 学 team_id 表示） | 6th | 与 FE 路线正交 | topic 317114 |
| 538 外部评分数据 | 社区 | 历届通用资产 | topic 309917 |

## 4. 关键技巧（含本场最著名的"魔法解释"）

- **1st 的实质**：直接复用 raddar 的 2018 女子赛冠军代码——"跨届/跨性别复用"最直白的例证。
- **"1st Place Magic Explained"（必读的复现学案例）**：一位选手按帖复现但分数差很远（0.663 vs 0.516）。排查发现：代码末尾有一行"合并赛季统计"的常量——原作者写死 `sub$Season = 2018`（拿到 2018 赛季统计），复现者改成 `2022` 就完全变了结果。**照搬方案时，连常量与"看起来是笔误的地方"都要原样理解**；共享解法的高分往往依赖这类未言明的细节。
- **球队 embedding 路线**（6th）：用 `nn.Embedding` 学 team_id 表示、两支球队 embedding 预测胜负——同一方法在同年女子赛只排 472/659，说明**跨赛事迁移并非无脑成立**（男/女赛数据结构不同）。

## 5. 可迁移性评估

- **可直接迁移**：体育概率赛的"复用成熟方案 + 校准"路线；embedding 表示球队的思路；外部评分资产（538）。
- **需要前提**：理解被复用代码的全部常量与隐含约定（本场最大教训）；跨赛事迁移前先验证结构可比性。
- **不建议照搬**：不读细节地复现公开方案；把单赛表现当成通用能力证据。

## 6. 对新手的关键启示

- **复现公开方案时逐行读懂常量与怪写法**：本场的胜负差异就藏在一个 `Season = 2018` 里。
- 成熟赛型的理性策略是复用 + 微调 + 校准，但"复用"包含"理解"。
- 同一方法在不同子赛事（男子/女子）可能差几百名——迁移要用验证说话。

## 7. 出处

- #1 方案自述（复用 2018 女子赛方案）：https://www.kaggle.com/competitions/mens-march-mania-2022/discussion/317145
- 1st Place Magic Explained（常量复现案例）：https://www.kaggle.com/competitions/mens-march-mania-2022/discussion/317316
- 6th：球队 embedding：https://www.kaggle.com/competitions/mens-march-mania-2022/discussion/317114
- 外部数据：538 评分：https://www.kaggle.com/competitions/mens-march-mania-2022/discussion/309917
