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

## 轻读结论（2026-10 补）

**一句话**：本场的名次杠杆不在模型复杂度，而在**评分来源 + 敢不敢重注超级球队**——1st 以 Nate Silver 评分为底、把南卡女篮与 UConn 男篮设为"模拟全胜"的超级球队（私榜 0.05313）；2nd 自建岭回归/混合效应球队评分 + 两级 XGBoost + 10 万次模拟，真正的跳升来自手动 override：把 UConn 男篮胜率置 100% 后从第 16 升到第 2。

- 1st（493793）：起点 = Nate Silver 的男女队评分；简单公式把评分差转成胜率；主动放弃旧年 ELO/混合效应模型，自述这个"赌博"可能下得比冲前 8 该有的更重。
- 2nd（492761）：R 语言全流程——岭回归/混合效应求球队评分（分差、攻防效率、节奏，含"对位调整"混合模型）→ XGBoost 两级（队级效率/节奏 → 比赛分差）→ GLM 转胜率 → 每届锦标赛 10 万次模拟；赛期每天赛后重训；改版提交（UConn 全胜）从第 16 升到第 2。
- 17th（492459，28 票）：方法学复盘，主线是"简单、可复现、稳健"；45th 走 BERT 文本分类另类路线。
- 社区：起步参考（52 票）、比赛设计（35 票 / 51 评论）、提交/选择问题（27 票 / 18 评论）、与专家提交对比（24 票 / 80 评论）。

**裁决**：锦标赛预测的首位投入是稳健的球队强弱评分（外部评分或自建混合效应/岭回归）；赛程中有统治级球队时，加大其胜率的 override 收益远大于模型微调；蒙特卡洛模拟是把单场概率转成最终名次期望的标准手段，样本要跑足。

**悬案**：3rd–16th/18th–44th 未细读；1st 的公式细节只在 notebook；本届评分口径与往届差异未整理；本场 0 张归档图（图证缺口已登记）。

## 图表证据

无可用图证（本场归档 0 图，图证缺口已登记）。

## 出处

- 讨论区索引：`intel/march-machine-learning-mania-2024/topics.md`
- 1st（33 票）：https://www.kaggle.com/competitions/march-machine-learning-mania-2024/discussion/493793
- 2nd（46 票）：https://www.kaggle.com/competitions/march-machine-learning-mania-2024/discussion/492761
- 17th Chessmetrics（28 票）：https://www.kaggle.com/competitions/march-machine-learning-mania-2024/discussion/492459
