# 2021 Kaggle Machine Learning & Data Science Survey（精简）

> 主题：other ｜ 子类：meta ｜ 类别：Community ｜ 截止：2021-11-28 ｜ 队伍数：0 ｜ 指标：评审制（最佳分析 notebook）
> 出处：`intel/kaggle-survey-2021/`（72 条主题索引 + 6 篇正文）

## 任务

第五届 Kaggle 年度调查的最佳分析 notebook 赛：用当年的问卷数据"讲述数据科学社区中某个切面的数据故事"，叙事与可视化质量由 Kaggle 评审。

## 关键要点

- 冠军方案《Data Science in 2021: Adaptation or Adoption?》：把调查数据与多个外部数据源连接，构造 **AI adoption index**，讨论行业与地区的 ML 成熟度——"外部数据 + 自建指标体系 + 交互可视化"的范式；二名作品分别用 2017–2021 数据做性别对比（D3.js 主题化视觉）、Analyst vs Scientist 的薪资/职责差异、早期职业路径、云计算趋势。
- 上届得主的**7 条 notebook 建议**（可直接当 checklist）：选一个具体问题（别做逐变量全景 EDA）；角度与众不同；研究并引用来源；先确认数据类型再选方法（调查数据几乎全是定性变量——**不能**用 Pearson/直方图/线性回归）；简单图表优于花哨图表；每个结果都要有文字解释；注意美学与导航。
- **8 大叙事主题模板**：地域、性别、技术兴起、编程语言、教育水平、跨年时序、'有价值的数据科学家'、'如何成为数据科学家'。
- 社区资产：21+ 个分析赛获奖 notebook 巡礼；历届获奖名单（2017–2020）——选题与技法的最佳参照库。
- 设有 $1,000 "早期提交奖"鼓励提前公开 notebook（与 2022 届冠军"提前两周公开换反馈"策略一脉相承）。

## 可迁移要点

- 调查/问卷类数据的**方法纪律**：先判定测量尺度，定性变量禁用连续变量方法。
- 选题公式：一个明确问题 + 独特角度 > 全景式 EDA；冠亚军的差异主要在选择的故事，而非代码。
- 外部数据三种用法：构造指标、对照比较、跨年拼接。
- 提前公开换反馈在评审制比赛中是被官方激励的策略。

## 轻读结论（2026-10 补）

**一句话**：第五届调查的叙事赛：冠军用多源外部数据构造 **AI 采用指数**（$10k），4 名 runner-up 分别做性别 5 年对比、Analyst vs Scientist、早期职业路径、云趋势（各 $5k）——**选题独特性与叙事质量**而非代码复杂度决定名次；上届得主的 7 条建议是可直接执行的 checklist。

- 7 条建议（279327，94 票）：具体问题、差异化角度、研究+引用、**方法匹配测量尺度（定性变量禁用 Pearson/直方图/线性回归）**、简单图表、完整文字解释、美学与导航。
- 8 大主题（278727，63 票）：地域/性别/技术兴起/编程语言/教育/跨年/有价值的数据科学家/如何成为数据科学家。
- 官方资产：往届获奖名单（54 票）、21 个获奖示例（25 票）、外部数据集（24 票）、可视化建议（25 票）；早期提交奖 $1,000（47 票）。

**裁决**：先定叙事主线再选方法；把 notebook 当论文写；外部数据用于差异化；早期公开换反馈。

**悬案**：获奖作品完整细节未收录；6 图中仅 1 张入选图证。

## 图表证据

![冠军的 AI 采用指数](../../intel/kaggle-survey-2021/bodies/295401_img/01.png)

**图 1**（topic 295401）：AI 采用阶段（Seedling→Ripening）。

## 出处

- 上届得主的 7 条建议：https://www.kaggle.com/competitions/kaggle-survey-2021/discussion/279327
- 获奖名单与评语：https://www.kaggle.com/competitions/kaggle-survey-2021/discussion/295401
- 8 大叙事主题模板：https://www.kaggle.com/competitions/kaggle-survey-2021/discussion/278727
- 21+ 分析赛获奖 notebook 巡礼：https://www.kaggle.com/competitions/kaggle-survey-2021/discussion/281091
- 往届获奖名单（2017–2020）：https://www.kaggle.com/competitions/kaggle-survey-2021/discussion/278542
- 早期提交奖公告：https://www.kaggle.com/competitions/kaggle-survey-2021/discussion/288495
