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

## 6. 轻读结论（2026-10 补）

**一句话**：图表→数据表的异质性极强——**"类型分类 + 分类型路由"是标配**（line/bar 交给 DePlot/Matcha 端到端、scatter/dot 交给目标检测/分割）；瓶颈在数据管线（标注口径、噪声、坐标定义）与合成数据，而不是模型选择。

- 1st（418786）：分类 + 分类型 DePlot + scatter 检测；数据 = 竞赛（剔约 100 张噪声）+ **ICDAR 逐张复核/伪标再复核** + **自造 6.5 万合成图**；多阶段训练（全类型 12 万图 8 epoch → 类型专属二次训练；h-bar/dot 因数据不足不二次训练）；处理了"竞赛 x/y 定义与 DePlot 相反"→ 按原定义训练、推理交换；public 0.86 → private 0.72（dot 仅 0.00/0.01）。
- 2nd（418430）：全 Matcha-base 两阶段——**adaptation（大量合成图）→ specialization（scatter / 非 scatter 两个专用模型）**；输出模板含类型/点数/x/y 序列；公开代码。
- 3rd（418420）：团队两条路线互补（端到端 vs 检测+OCR）；scatter/dot 检测、line/bar Matcha。
- 7th（418510）：**无外部数据**的多模型流水线（分类/文本检测/文本识别/目标检测/分割 + DePlot 兜底仅 1/559）；CV/LB 0.871/0.86、私榜 0.67。
- 社区：**"为什么 Pix2Struct/MatCha/DePlot 训不起来"**（42 票 / 133 评论）是全场共同坑。

**裁决**：按图表类型路由；散点类必须检测/分割；先修数据与坐标口径；高公榜低私榜下看分项与稳定性选提交。

**悬案**：4th/5th/8th–12th 方案缺失；dot 类近乎全灭的原因未系统整理；1st 的检测细节未展开。

## 7. 图表证据

![2nd 的两阶段训练管线](../../intel/benetech-making-graphs-accessible/bodies/418430_img/01.png)

**图 1**（topic 418430）：matcha-base → adaptation（合成图适配，兼作分类检查点）→ specialization（scatter / 非 scatter 两条专精）。

## 8. 出处

- 讨论区索引：`intel/benetech-making-graphs-accessible/topics.md`（80 条）
- 已收录 write-up（6 篇）：
  - 1st（60 票）：https://www.kaggle.com/competitions/benetech-making-graphs-accessible/discussion/418786
  - 2nd（64 票，含代码）：https://www.kaggle.com/competitions/benetech-making-graphs-accessible/discussion/418430
  - 3rd（54 票，Matcha + 目标检测）：https://www.kaggle.com/competitions/benetech-making-graphs-accessible/discussion/418420
  - 7th（51 票，不用外部数据）：https://www.kaggle.com/competitions/benetech-making-graphs-accessible/discussion/418510
  - 1st（60 票）：https://www.kaggle.com/competitions/benetech-making-graphs-accessible/discussion/418786
  - 6th（40 票）：https://www.kaggle.com/competitions/benetech-making-graphs-accessible/discussion/418466
  - Pix2Struct 训不起来（42 票 / 133 评论）：https://www.kaggle.com/competitions/benetech-making-graphs-accessible/discussion/406250
- 轻读全本：`analysis/deep/benetech-making-graphs-accessible.md`（Tier B 轻读：对照矩阵/裁决/证据分级/悬案 + 1 图证）
