# NFL Big Data Bowl 2026 - Analytics Track（精简）

> 主题：other ｜ 子类：analytics ｜ 类别：Featured ｜ 截止：2025-12-17 ｜ 队伍数：277 ｜ 指标：评审制（分析报告）
> 出处：`intel/nfl-big-data-bowl-2026-analytics/`（80 条主题索引 + 6 篇正文）

## 任务

与同届 Prediction 赛道（预测球员轨迹）**平行设立的分析赛道**：围绕"球在空中时球员如何移动"这一主题产出**洞察与可视化报告**，由评审打分。非预测任务，因此从 cv 归入 `other/analytics`。

## 关键要点

- 两条赛道共享同一份数据，但**评分标准完全不同**：预测赛道比误差，分析赛道比洞察质量与表达。
- 讨论区有专门的"首次参赛者提问帖"与官方 Discord——**社区支持完善**。
- 与 Pokemon TCG 的 Strategy 赛道、Kaggle AGI 基准设计赛并列：**"评审制技术赛道"正在成为 Kaggle 的常设形式**。

## 可迁移要点

- **同一数据可以有两种比赛**：预测（可量化）与洞察（需论证）——选择赛道取决于你的强项。
- 分析类赛道的关键是"提出一个好问题 + 用数据讲清楚"。

## 轻读结论（2026-10 补）

- **主题**：第八届 BDB Analytics 赛道（277 队），研究"球在空中"阶段的球员移动，目标是产出新的进攻/防守球员指标；官方再次强调 BDB→体育分析的就业管线（609370）。
- **最强社区资源**：2025 冠军 @VishakhSandwar 的开源补充数据（帧级 coverage scheme + 球员级 coverage 细节）+ man/zone Transformer notebook + SumerSports 博客 + 持续 AMA（614950）。
- **数据口径问题**：ball_land 不一致、player_to_predict、frame_id、朝向、加速度、字段名、dropback、球落点、team coverage type、subset/outside data（610834 / 613454 / 614459 / 613468 / 657011 / 610026 / 639412 / 656536 / 656945）。
- **流程摩擦**：原定 2026-01-20 出结果、1/26 仍在等（670213）；有人遇到"evaluation system not configured"（663170）；writeup 编辑方式不明（663242）。

## 图表证据

本场 0 张归档图（0/0），**图证缺口已登记**。

## 出处

- 讨论区索引：`intel/nfl-big-data-bowl-2026-analytics/topics.md`
- 官方入门与 Discord 帖：见该比赛讨论区 "How to Get Started + Competition's Official Discord"
- 官方欢迎（主题与就业管线）：https://www.kaggle.com/competitions/nfl-big-data-bowl-2026-analytics/discussion/609370
- 2025 冠军 AMA 与开源补充：https://www.kaggle.com/competitions/nfl-big-data-bowl-2026-analytics/discussion/614950
- 结果延期询问：https://www.kaggle.com/competitions/nfl-big-data-bowl-2026-analytics/discussion/670213
- 获奖公布：https://www.kaggle.com/competitions/nfl-big-data-bowl-2026-analytics/discussion/670745
