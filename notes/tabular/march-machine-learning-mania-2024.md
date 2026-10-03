# March Machine Learning Mania 2024（精简）

> 主题：tabular ｜ 子类：sports ｜ 类别：Featured ｜ 截止：2024-XX-XX ｜ 队伍数：3000+ ｜ 指标：Brier
> 出处：`intel/march-machine-learning-mania-2024/`（80 条主题索引 + 6 篇写-up 正文）

## 任务

预测 NCAA 锦标赛胜负概率（Brier）。

## 关键要点（本场最有价值的案例）

- 17th 的方案基于作者 **20-25 年前为国际象棋选手开发的 Chessmetrics 评分算法**——一种迭代式评分方法（队伍评分 = 对手平均评分 + 胜负关系带来的调整）。
- 这是"**跨领域方法迁移**"的绝佳例证：棋类评分体系 → 体育赛事预测（与 `LEARNING_PATH.md` 附录一的主题一致）。
- 与 2022/2023/2025/2026 对照，NCAA 系列的方法论始终围绕：外部评分体系 + 概率校准 + 稳健提交。

## 可迁移要点

- **老方法在新领域可能焕发第二春**：评分/排序体系（Elo、Chessmetrics、TrueSkill 类）在体育、推荐、教育评估中通用。
- 迭代式相对评分值得作为工具箱常备项。

## 出处

- 讨论区索引：`intel/march-machine-learning-mania-2024/topics.md`
- 1st（33 票）：https://www.kaggle.com/competitions/march-machine-learning-mania-2024/discussion/493793
- 2nd（46 票）：https://www.kaggle.com/competitions/march-machine-learning-mania-2024/discussion/492761
- 17th Chessmetrics（28 票）：https://www.kaggle.com/competitions/march-machine-learning-mania-2024/discussion/492459
