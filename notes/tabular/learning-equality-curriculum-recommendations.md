# Learning Equality - Curriculum Recommendations

> 主题：tabular（召回/匹配）｜ 子类：recsys ｜ 领域：教育 ｜ 类别：Featured
> 截止：2023-03-14 ｜ 队伍数：1057 ｜ 机制：代码赛 ｜ 指标：F-beta（micro）
> 数据来源：`intel/learning-equality-curriculum-recommendations/`（80 条主题索引 + 6 篇 write-up 正文）

## 1. 任务与数据

- 预测目标：为每个"主题（topic）"推荐匹配的课程内容（content/lesson）——本质是**大规模检索/匹配**。
- 数据形态：知识点树（topic tree）+ 多语言文本内容；**"无正确匹配"也是一种可能**（评判标准含"该主题是否真的需要内容"）。
- 构造陷阱：
  - **层级结构（topic tree）** 是核心先验，必须正确遍历（2nd 明确说主办方提供的树遍历代码帮助很大）；
  - 多语言、文本长短差异大；
  - **同时设 Efficiency Prize**：2nd 说"打榜和打效率奖像参加两场不同的比赛"。

## 2. 方案谱系

| 方案 | 名次 | 关键点 |
| --- | --- | --- |
| 多阶段流程（召回 + 排序） | 2nd / 3rd | 借助主办方的树遍历与数据探索 notebook 起步；文本预处理公开帖；多阶段候选生成 + 排序 |
| 社区方法复用 | 3rd | 明确表示"我们用的所有方法都来自 Kaggle 社区" |
| 其他方案 | 1st / 6th | 见讨论区 |

## 3. 关键技巧

- **利用层级结构**：topic tree 的父子关系是强特征（父节点匹配结果可传播给子节点）。
- **多阶段召回 + 排序**（与 Otto、H&M 同构）。
- **主办方资源优先**：官方数据探索 notebook 与"host tips"帖是最可靠的起点。
- **效率赛道要单独优化**（推理时间/内存也是评分项）。

## 4. 可迁移性评估

- **可直接迁移**：
  - **层级/图结构的传播特征**（父 → 子）；
  - 多阶段召回-排序框架；
  - 优先读主办方的数据探索材料；
  - 同一比赛的双赛道（精度 + 效率）需要分别规划。
- 需要前提：多语言文本处理与检索基础设施。
- 不建议照搬：忽略层级结构做平铺匹配。

## 5. 对新手的关键启示

1. **数据的结构（层级/图）往往是最强的免费特征**。
2. **主办方发布的 notebook 与 tips 是最高优先级阅读材料**。
3. 遇到"效率赛道"，要把它当成第二场比赛来规划。

## 6. 轻读结论（2026-10 补）

**一句话**：一对多的多语言检索匹配——**主题树上下文注入 + 训练期负样本/批次设计 + 与候选质量耦合的阈值**是三大支点；重排的价值取决于召回器质量。

- 1st（209 票）：TFIDF+3 模型嵌入召回（ArcFace）+ 23 特征 LightGBM + 相对概率缺口后处理；val 0.764/LB 0.727；效率版 0.740 priv。
- 2nd（79 票）：**单阶段检索、零重排**；对称 InfoNCE + 定制 batch（禁止同批共享内容、难负样本过采样）；语言切换 +0.01~0.02；**动态阈值 +0.02**；单模 priv 0.696；蒸馏+量化打效率榜。
- 3rd（59 票）：无监督 SimCSE 召回 + mdeberta 重排（加载 SimCSE 权重 val 0.7149 vs 从零 0.6378）；FGM+EMA +0.01；12 模型×50 召回 = **priv 0.751**。
- 6th（47 票）：ArcFace+KNN+GBDT 树特征重排；"stage1 单独 <0.6，必须补树结构"。

**裁决**：先投召回器与负样本设计，再考虑二阶段；阈值用"相对/动态"而非全局静态；一对多任务的 CV 必须按共享内容分组。

**悬案**：4th/5th 方案缺失；低资源语言（bn 0.15 / swa 0.09）策略未展开；效率奖完整排名未入库。

## 7. 图表证据

![2nd 的动态阈值计算](../../intel/learning-equality-curriculum-recommendations/bodies/395110_img/05.jpg)

**图 1**（topic 395110）：`dyn_th = max_sim − margin·max_sim`——窗口随行内最高相似度缩放，保证每行至少选一个；这是"阈值必须与候选质量耦合"的直接证据。

## 8. 出处

- 讨论区索引：`intel/learning-equality-curriculum-recommendations/topics.md`（80 条）
- 已收录 write-up（6 篇）：
  - 1st（209 票）：https://www.kaggle.com/competitions/learning-equality-curriculum-recommendations/discussion/394812
  - 2nd（79 票）：https://www.kaggle.com/competitions/learning-equality-curriculum-recommendations/discussion/395110
  - 3rd（59 票，含主办方 tips 与文本预处理链接）：https://www.kaggle.com/competitions/learning-equality-curriculum-recommendations/discussion/394838
  - 6th（47 票）：https://www.kaggle.com/competitions/learning-equality-curriculum-recommendations/discussion/394813
  - 主办方欢迎与说明（52 票）：https://www.kaggle.com/competitions/learning-equality-curriculum-recommendations/discussion/372362
- 轻读全本：`analysis/deep/learning-equality-curriculum-recommendations.md`（Tier B 轻读：对照矩阵/裁决/证据分级/悬案 + 2 图证）
