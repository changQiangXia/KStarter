# Benetech - Making Graphs Accessible

> 主题：cv ｜ 子类：— ｜ 领域：无障碍/文档理解 ｜ 类别：Featured
> 截止：2023-XX-XX ｜ 队伍数：1000+ ｜ 机制：代码赛 ｜ 指标：图表数据抽取（多子任务）
> 数据来源：`intel/benetech-making-graphs-accessible/`（80 条主题索引 + 6 篇 write-up 正文）

## 1. 任务与数据

- 预测目标：把图片里的**图表还原成可访问的数据表**（识别图表类型、抽取数据点与坐标轴标签）。
- 数据形态：图表图像（折线/柱状/散点等）+ 结构化标注。
- 构造陷阱：
  - 图表类型多样 → **先分类再抽取**的两步结构；
  - 坐标轴刻度与数据点需要几何推理；
  - 多语言/多字体标签。

## 2. 方案谱系

| 方案 | 名次 | 关键点 |
| --- | --- | --- |
| **两步流水线：先分类图表类型，再按类型抽取数据** | 1st | 针对不同图表类型使用不同的抽取策略——"先判断是什么，再决定怎么读" |
| 其他方案 | 见讨论区 | |

## 3. 关键技巧

- **类型条件化的抽取**：不同图表类型（折线/柱状/散点）需要不同的几何解码策略。
- **几何 + 文本联合推理**：坐标轴刻度识别 + 数据点定位。
- **任务分层**：把"无障碍化"拆成识别 → 抽取两个可独立评估的子问题。

## 4. 可迁移性评估

- **可直接迁移**：
  - **"先分类再处理"的流水线**（文档理解、OCR 后处理、版面分析通用）；
  - 类型条件化（type-conditioned）的解码策略。
- 需要前提：图表检测/关键点定位的视觉模型能力。
- 不建议照搬：用单一模型端到端处理所有图表类型。

## 5. 对新手的关键启示

1. **当任务包含多种异质对象时，先分类再分治**。
2. 无障碍/文档类任务的社会价值明确，且评估维度通常可分解。
3. 与 AI4Code、Feedback 2021 对照：**结构化抽取类任务的通用套路是分阶段 + 后处理**。

## 6. 出处

- 讨论区索引：`intel/benetech-making-graphs-accessible/topics.md`（80 条）
- 已收录 write-up（6 篇）：
  - 1st（60 票）：https://www.kaggle.com/competitions/benetech-making-graphs-accessible/discussion/418786
  - 2nd（64 票，含代码）：https://www.kaggle.com/competitions/benetech-making-graphs-accessible/discussion/418430
  - 3rd（54 票，Matcha + 目标检测）：https://www.kaggle.com/competitions/benetech-making-graphs-accessible/discussion/418420
  - 7th（51 票，不用外部数据）：https://www.kaggle.com/competitions/benetech-making-graphs-accessible/discussion/418510
