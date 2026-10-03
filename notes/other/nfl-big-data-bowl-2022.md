# NFL Big Data Bowl 2022（精简）

> 主题：other ｜ 子类：analytics ｜ 类别：Community ｜ 截止：2022-01-06 ｜ 队伍数：0 ｜ 指标：评审制（分析报告）
> 出处：`intel/nfl-big-data-bowl-2022/`（80 条主题索引 + 6 篇正文）

## 任务

第四届 Big Data Bowl，主题为**特勤组（special teams）**：用 2018–2020 赛季的 NGS 追踪数据（全体球员位置/速度/加速度/朝向）+ PFF 球探数据，分析弃踢、开球、任意球/附加分三类战术；评审制、无目标指标，提交须在截止时公开；另设高校学生组别。

## 关键要点

- 官方给三类特勤组战术定了不同策略语境，并首次引入 **"Coaches Corner" 教练连线与 film study**（与超级碗冠军 Usama Young 等复盘比赛录像）。
- 官方 demo 以**踢球手相对中线的偏移量**为例（R/Python 双教程：读数、清洗、动画、绘图）——"先标准化位置信息"是追踪数据分析的第一步。
- 讨论区先导内容：NFL 规则/位置/计分入门指南（面向无橄榄球背景的 Kagglers）、历届获奖作品陈列（2021 BDB、1st & Future、Punt Analytics）——沿用了 BDB 系列"先补领域知识，再谈分析"的传统。
- 与 2021 届一样没有排行榜：评审看的是问题定义、方法、叙事与 notebook 质量。

## 可迁移要点

- 评审制分析赛的入口动作：**读官方 demo + 往届获奖作 + 领域入门材料**，再选切口。
- 追踪数据通用预处理：坐标标准化/朝向归一 → 可视化动画 → 派生指标（如偏移量）→ 叙事。
- 系列赛的"组别"（高校/开放）影响投稿定位；同一数据可产多种故事（策略、球员评估、战术演化）。

## 轻读结论（2026-10 补）

- **赛制**：第四届 BDB、特勤组主题；NGS 2018–2020 追踪 + PFF 球探数据；无目标指标、评审制；提交须公开；高校组别（274053 / 274066）。
- **上手链**：NFL 规则入门（18 票）→ 特勤组 10 分钟（17 票）→ 官方 demo"踢球手偏移量"R/Python 双教程（读数/清洗/动画/绘图）→ 位置标准化（Tom Bliss）→ 往届获奖作品模板（274258 / 274376 / 275296 / 274056）。
- **数据质量坑**：身高不一致、tracking 精度、飞行球运动学异常、无效值、PFF/tracking 不匹配、PFF hangTime NaN——派生指标前先审计（276122 / 295359 / 284774 / 284166 / 298160）。
- **领域活动**：首次 Coaches Corner + film study（Usama Young 复盘弃踢）；评审看问题定义/叙事/notebook 质量（300722）。

## 图表证据

本场 0 张归档图（目录为空），**图证缺口已登记**。

## 出处

- 官方欢迎帖（组别与规则）：https://www.kaggle.com/competitions/nfl-big-data-bowl-2022/discussion/274053
- 任务说明（数据范围与 Coaches Corner）：https://www.kaggle.com/competitions/nfl-big-data-bowl-2022/discussion/274066
- 历届获奖作品：https://www.kaggle.com/competitions/nfl-big-data-bowl-2022/discussion/274056
- NFL 入门指南：https://www.kaggle.com/competitions/nfl-big-data-bowl-2022/discussion/274258
- 官方 demo（踢球手偏移量）：https://www.kaggle.com/competitions/nfl-big-data-bowl-2022/discussion/275296
- film study 说明：https://www.kaggle.com/competitions/nfl-big-data-bowl-2022/discussion/283822
- judging 与 next steps：https://www.kaggle.com/competitions/nfl-big-data-bowl-2022/discussion/300722
- 2022 Winners：https://www.kaggle.com/competitions/nfl-big-data-bowl-2022/discussion/307969
