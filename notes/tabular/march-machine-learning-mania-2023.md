# March Machine Learning Mania 2023（精简）

> 主题：tabular ｜ 子类：sports ｜ 类别：Featured ｜ 截止：2023-03-XX ｜ 队伍数：3000+ ｜ 指标：Brier
> 出处：`intel/march-machine-learning-mania-2023/`（80 条主题索引 + 6 篇 write-up 正文）

## 任务

预测 2023 年 NCAA 锦标赛胜负概率（Brier 评分），男女赛合并设题。

## 关键要点

- 5th 方案：私榜 0.17619；作者强调**感谢社区公开的 notebook 与讨论**，并把自己的方案完整公开（Notebook 链接）——该系列赛的公开协作文化非常强。
- 与前后的 2022/2025/2026 届对照可见方法论的高度稳定：**外部评分数据 + 树模型/线性模型 + 概率校准 + 稳健提交**。
- 该类比赛的核心难点始终是：数据量小、赛程短、方差大 → 校准与稳健优先于模型创新。

## 可迁移要点

- 成熟的比赛类型（如 NCAA 系列）中，**复用公开方案 + 微调校准**就是理性打法。
- 概率预测任务的评估要围绕 Brier/对数损失做校准，而不是追求分类准确率。

## 轻读结论（2026-10 补）

**一句话**：本届由**公开基线（raddar 旧代码）**统治——冠军只改两处（注掉产生 inf 的 `np.exp()`、种子 1–4 对 13–16 不做 override）就夺冠，未改动版也够第 6；5th 统计"前 100 约 60% 是同一 notebook 的无改动 fork"；**126 个计分样本**让名次噪声极大（前两名都自认有运气成分）。

- 1st（399553）：特征 = 常规赛统计均值（T1/T1 对手/T2/T2 对手 + `PointDiff`）+ 14 天胜率 + Team Quality + Seed_diff + seeds；XGB + 5 折×3 次 CV；注掉 `np.exp()` 后仍有约 25% 训练数据 NaN。
- 2nd（401578，0.17522）：**分区效应 offset**——用 `glmnet` 在非分区常规赛上学"主场分差/主场胜负"，主 +1/客 −1 单列编码，系数差作 offset；加 DataRobot AutoML 与概率平滑；触发案例：South Dakota State 女篮被高估。
- 5th（401382）：只保留**按回合归一化**的效率特征（Moneyball 思路），剔除 `NumOT`、`WLoc`（中立场地）。
- 官方计分（74 票）：成绩从 natstat API 拉取、每天更新；结算只用选中的 2 份提交（"多提交择优选"是赛制一部分）。

**裁决**：公开基线足够强 + 样本极少时，复用是理性策略（但要看"相对基线的增量"）；领域增量要打在基线的具体盲区；两个提交覆盖不同风险偏好。

**悬案**：3rd/4th/6th–10th 方案缺失；2nd 的 AutoML 细节未展开；本场归档图不可读（图证缺口）。

## 图表证据

无可用图证（唯一归档图为 144px 窄条）。

## 出处

- 讨论区索引：`intel/march-machine-learning-mania-2023/topics.md`
- 5th 方案（含 Notebook 链接）：见该比赛讨论区 5th Place Solution
- 1st：https://www.kaggle.com/competitions/march-machine-learning-mania-2023/discussion/399553
- 2nd：https://www.kaggle.com/competitions/march-machine-learning-mania-2023/discussion/401578
- 5th：https://www.kaggle.com/competitions/march-machine-learning-mania-2023/discussion/401382
- 官方计分（74 票）：https://www.kaggle.com/competitions/march-machine-learning-mania-2023/discussion/395257
- 538 外部数据（74 票）：https://www.kaggle.com/competitions/march-machine-learning-mania-2023/discussion/388323
- 轻读全本：`analysis/deep/march-machine-learning-mania-2023.md`（Tier B 轻读：对照矩阵/裁决/证据分级/悬案；图证缺口已登记）
