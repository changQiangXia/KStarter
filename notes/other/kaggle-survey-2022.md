# 2022 Kaggle Machine Learning & Data Science Survey（精简）

> 主题：other ｜ 子类：meta ｜ 类别：Community ｜ 截止：2022-11-27 ｜ 队伍数：0 ｜ 指标：评审制（最佳分析 notebook）
> 出处：`intel/kaggle-survey-2022/`（63 条主题索引 + 6 篇正文）

## 任务

第六届 Kaggle 年度调查的**最佳分析 notebook 赛**：用当年 2.3 万+ 份问卷数据（大量定性/哑变量字段）写出一篇有叙事的分析报告，由 Kaggle 评审，比的是选题、叙事与可视化质量，而非预测精度。

## 关键要点

- **冠军的"因子化"变换思路**（1st place 幕后连载）：调查数据几乎全是定性/哑变量，指标维度受限；他按分组变量（如国家）计算各群体特征占比（如 30 岁以下比例 ∈ [0,1]），把定性列**转成连续"因子"**，之后就能用分布、相关、回归、散点图等全套定量工具——共构造 15 个跨人口/教育/技术/职业领域的因子做国家间对比。
- **先设计后编码**：冠军自述总开发约 70–80 小时；开工前先画图表草图、把选题放几天再用"冷脑袋"取舍，并强调"边加载数据边试"的即兴做法会让叙事散架。
- **把比赛当迭代**：作者 2019 年无奖、2020 年拿 notebook 奖、当年夺冠——说明这类赛的复利来自选题直觉的逐年打磨。
- **运营细节**：提前 2 周多公开 notebook 收集评论/点赞反馈再做调整；赛程期清空杂事、请 2 天假；逐条研读评审规则并按规则优化。
- 社区资产：历届获奖 notebook 清单（2017–2021）与外部数据源建议（历年调查、Stack Overflow 调查、World Bank 指标、Meta Kaggle、薪资数据）——**往年获奖作是最好的选题库与技法参照**。

## 可迁移要点

- **"定性 → 连续"的因子化**是调查/表格类分析的通用放大招：任何"类别 × 分组"数据都能转成组内占比的连续特征，把可做的分析维度放大一个量级。
- 叙事类比赛的正序是"选题 → 草图 → 数据 → 成品"；先想清楚讲什么故事，再决定用什么图，最后才写代码。
- 提前公开作品换反馈的"半开源"策略，在评审制比赛里优于憋到最后。
- 对新手：这类比赛零算力、门槛低、竞争靠洞见而非资源，适合作为叙事能力的练兵场。

## 出处

- 冠军幕后连载（一）：开发前如何构思：https://www.kaggle.com/competitions/kaggle-survey-2022/discussion/374157
- 冠军幕后连载（二）：因子化思路与选题动机：https://www.kaggle.com/competitions/kaggle-survey-2022/discussion/374969
- 冠军幕后连载（五）：时间投入与复盘：https://www.kaggle.com/competitions/kaggle-survey-2022/discussion/377522
- 历届获奖 notebook 清单：https://www.kaggle.com/competitions/kaggle-survey-2022/discussion/359064
- 上一届冠军作品集：https://www.kaggle.com/competitions/kaggle-survey-2022/discussion/359075
- 外部数据源建议：https://www.kaggle.com/competitions/kaggle-survey-2022/discussion/359047
