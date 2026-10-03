# March Machine Learning Mania 2025

> 主题：tabular ｜ 子类：sports ｜ 领域：体育 ｜ 类别：Featured
> 截止：2025-04-07 ｜ 队伍数：3000+ ｜ 机制：标准赛 ｜ 指标：Brier 分数（胜负概率）
> 数据来源：`intel/march-machine-learning-mania-2025/`（80 条主题索引 + 6 篇 write-up 正文）

## 1. 任务与数据

- 预测目标：预测 NCAA 男女篮锦标赛每场比赛的胜负概率。
- 数据形态：球队赛季统计、历史对阵、种子排名；**测试集极小（百余场）**，方差高。
- 赛制特点：比赛是**锦标赛制、逐个阶段更新榜单**（主办方在讨论区维护 live update 帖），且赛后跑反作弊算法再定奖。

## 2. 验证方案

| 方案 | 使用者 | 说明 |
| --- | --- | --- |
| 以 Brier 分数为准的滚动验证 | 1st / 4th | 4th 明确写"验证策略基于个人直觉 + Brier 分数" |
| 外部数据交叉验证 | 1st | 使用 Kenpom / Massey / 538 等外部评分体系 |
| 历史方案对照 | 社区 | "Previous Solutions and Takeaways" 帖系统整理了历届做法 |

## 3. 方案谱系

| 方案 | 名次 | 关键点 |
| --- | --- | --- |
| 基于社区特征工程 + 外部评分数据 | 1st | 原计划依赖 538 数据，但 2025 年该数据源停更，被迫改用 raddar 的公开 notebook 特征（球队平均统计 + 球队质量） |
| **逻辑回归作用于 XGBoost 叶节点**（Cauchy 损失拟合分差） | 4th | 特征在 raddar 基础上加入 Laplace 平滑的"上赛季对阵 / 客场胜场 / 近 14 天胜率"，并堆叠 OOF 预测 |
| 历史方案索引（Elo + KNN 等） | 社区 | 往届冠军常用 Elo 评分 + 近邻回归预测分差 |

## 4. 关键技巧

- **外部评分体系**（Kenpom/Massey/538）是强特征，但**数据源可能停更**，要准备替代方案。
- **树模型叶节点 + 线性模型**的两级结构（4th）：用 XGB 拟合分差、LR 输出概率，兼顾拟合与校准。
- **Laplace 平滑**处理小样本类别（对阵组合、客场战绩）。
- **OOF 堆叠**作为特征。
- **横向复用**：社区整理的"历届方案与要点"是最高效的起点。

## 5. 可迁移性评估

- **可直接迁移**：
  - 树模型叶节点作为线性模型输入（经典 stacking 变体）。
  - Laplace 平滑处理稀疏类别统计。
  - 外部评分/榜单数据作为特征，但要评估其可持续性。
- **需要前提**：
  - 体育赛事的领域知识（种子、主客场、赛程密度）。
- **不建议照搬**：
  - 只依赖单一外部数据源（538 停更即断供）。

## 6. 对新手的关键启示

1. **外部数据要评估可持续性**（本场冠军被数据源停更打乱计划）。
2. **小样本 + 锦标赛制**：概率校准与稳健性优先。
3. 与 2026 届对照可见同一赛事的稳定套路（外部评分 + 树模型 + 校准），以及逐年变化（数据源、参赛队伍）。

## 7. 轻读结论（2026-10 补）

**一句话**：raddar 特征 + 简单模型 + LOSO 的系列惯例延续；2025 的焦点是"手动覆写/加注（1st）vs 纯模型（4th）"的路线之争与早期 LB 噪声。

- 1st（32 票）：29 特征 XGB（eta 0.0093/depth 4/704 轮）；后处理 <85% 预测 +10%；**手动覆写 6 场男队早期比赛**（0.582→0.982 等，专家确认高种子）。
- 4th（37 票）：LR on XGB leaves（Cauchy 净胜分）+ Laplace 平滑特征；显式规避时间/目标泄漏（弃公共 CV/spline，LOSO 仅做模型平均）；不赌博不手动。
- 事件：可视化器（图 1）；榜单早期出现"全部猜中"的噪声（"Current first place scares me"）。

**裁决**：小样本强先验下手动注入可正收益但高方差、难归因；纯模型路线更可复用；赛程早期 LB 信息量极低。

**悬案**：2nd/3rd 未收录；1st 的手动覆写贡献不可分离。

## 8. 图表证据

![2025 男队预测括号](../../intel/march-machine-learning-mania-2025/bodies/568862_img/01.png)

**图 1**（topic 568862）：可视化器括号（FL Atlantic 胜 Purdue 等）与 Brier 0.21087/0.20150。

## 9. 出处

- 讨论区索引：`intel/march-machine-learning-mania-2025/topics.md`（80 条）
- 已收录 write-up（6 篇）：
  - 1st（32 票）：https://www.kaggle.com/competitions/march-machine-learning-mania-2025/discussion/572717
  - 4th（37 票）：https://www.kaggle.com/competitions/march-machine-learning-mania-2025/discussion/572466
  - 历届方案与要点（47 票）：https://www.kaggle.com/competitions/march-machine-learning-mania-2025/discussion/562585
  - 榜单更新帖（62 票）：https://www.kaggle.com/competitions/march-machine-learning-mania-2025/discussion/569248
- 轻读全本：`analysis/deep/march-machine-learning-mania-2025.md`（Tier B 轻读：对照矩阵/裁决/证据分级/悬案 + 1 图证）
