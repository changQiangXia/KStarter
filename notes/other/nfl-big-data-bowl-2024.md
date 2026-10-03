# NFL Big Data Bowl 2024（精简）

> 主题：other ｜ 子类：analytics ｜ 类别：Community ｜ 截止：2024-01-08 ｜ 队伍数：0 ｜ 指标：评审制（分析报告）
> 出处：`intel/nfl-big-data-bowl-2024/`（80 条主题索引 + 6 篇正文）

## 任务

官方称为第六届 Big Data Bowl，主题为**擒抱（tackling）**：用球员追踪数据（NGS）分析"防守方如何放倒持球人"，提交分析报告/notebook 而非预测结果，由 NFL 球队分析师评审。约 300 份提交，分 metric / 本科组 / 教练组三个赛道（比例约 45/30/25）；无公开排行榜，故归入 `other/analytics`。

## 关键要点

- 讨论区主体是**领域知识**而非建模技巧：进攻阵型术语、位置缩写、擒抱技术分类（in-line / open field / engaged / last chance）、missed tackle 与 forced fumble 的口径、assisted tackle 的统计规则——评审制比赛里"把领域问题定义清楚"本身就是得分项。
- 官方给出的文献线索：nflWAR 论文（多项逻辑回归估 EP、GAM 估 WP，再导出 EPA/WPA 与球员 WAR）、Next Gen Stats 的 Expected Rushing Yards 家族（xRY / RYOE / 首攻与达阵概率）。
- 历史冠军被反复引用：The Zoo 的 2020 年方案（直接用全部 22 人的相对位置与速度，不依赖预构造特征），强调**原始状态可迁移到任意 play / 时间戳**。
- 工具生态以 R 为主：nflverse 全家桶（nflfastR、nflseedR、nfl4th、nflreadr、nflplotR）+ cfbfastR 的 EP 建模教程。

## 可迁移要点

- **评审制比赛的写法与打榜赛相反**：先讲清"擒抱是什么、怎么衡量"，再谈模型；领域定义、口径一致性、可视化叙事是第一评分维度。
- EP/WP 的"先建模事件概率再求期望"是通用范式：多分类比分事件 → 概率 → 期望值 → 前后差（EPA/WPA），比直接回归"下一次得分"更稳。
- xRY 类指标的设计思路（用全场相对运动状态估计期望产出）可迁移到任何"多智能体追踪 + 单步产出"的场景。
- 做同类赛前先吃透联盟公开术语与统计口径，避免连"什么算一次成功擒抱"都答错。

## 出处

- 官方欢迎帖（赛道与评分流程）：https://www.kaggle.com/competitions/nfl-big-data-bowl-2024/discussion/446943
- 擒抱技术体系与统计口径：https://www.kaggle.com/competitions/nfl-big-data-bowl-2024/discussion/448833
- 术语表（阵型/位置/传球统计）：https://www.kaggle.com/competitions/nfl-big-data-bowl-2024/discussion/447174
- 指标文献（nflWAR / EP / WP / EPA）：https://www.kaggle.com/competitions/nfl-big-data-bowl-2024/discussion/447660
- 历史冠军与工具生态（xRY / The Zoo / nflverse）：https://www.kaggle.com/competitions/nfl-big-data-bowl-2024/discussion/446946
- 赛后总结（提交量与赛道分布）：https://www.kaggle.com/competitions/nfl-big-data-bowl-2024/discussion/468229
