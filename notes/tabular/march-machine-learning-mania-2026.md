# March Machine Learning Mania 2026

> 主题：tabular ｜ 子类：sports ｜ 领域：体育 ｜ 类别：Featured
> 截止：2026-04-07 ｜ 队伍数：3485 ｜ 机制：标准赛 ｜ 指标：Brier / MSE（预测胜率）
> 数据来源：`intel/march-machine-learning-mania-2026/`（120 条主题索引 + 8 篇 write-up 正文）

## 1. 任务与数据

- **预测目标**：预测 NCAA 男女篮锦标赛每场比赛的胜负概率（本质是概率预测，用 Brier/MSE 评分）。
- **数据形态**：历年比赛结果、球队统计、种子（seed）排名等结构化数据。
- **决定性特征：测试集极小**（本届仅 126 场）。意味着**方差极大**——名次很大程度由少数几场比赛决定。

## 2. 验证方案

| 方案 | 使用者 | 说明 |
| --- | --- | --- |
| 分阶段验证（Stage 1 vs Stage 2） | 1st / 3rd | 明确区分"已见比赛"与"未见比赛"，两者最优模型不同 |
| 概率校准评估 | 2nd | 关注极端概率的过度自信问题 |
| 与外部市场概率比对 | 3rd | 用 Vegas/预测市场作为独立参照 |

**关键发现**：3rd place 明确指出——**逻辑回归在 Stage 2（未见比赛）上远好于梯度提升树，尽管在 Stage 1 榜上落后**。这直接说明验证设计要匹配真正的评分阶段。

## 3. 方案谱系

| 方案 | 名次 | 关键点 |
| --- | --- | --- |
| 种子差基线 + 委员会未计入因素的修正 + 后处理锐化 | 1st | 信任选秀委员会的种子排序，再补充"连续性排名、伤病、对位优势"；男女分开建模；明确以"进钱圈"为优化目标 |
| XGBoost(60%) + 逻辑回归(40%) 加权 + 概率裁剪 [0.02, 0.98] | 2nd | LR 提供校准、XGB 捕捉非线性；裁剪抑制极端自信 |
| 逻辑回归（球队差分特征）+ 三方市场概率融合（ESPN BPI / Vegas 赔率 / Kalshi 预测市场） | 3rd | 预测市场提供**正交信息**，在第一轮尤为有效（伤病、旅途、对位因素） |

## 4. 关键技巧

- **概率校准比排序能力更重要**：小样本 + Brier 指标下，过度自信的预测会被重罚；LR 与裁剪都是校准手段。
- **外部市场概率是强特征**：赔率与预测市场聚合了公开信息，且与统计模型正交。
- **男女赛事分开建模**。
- **"为赢而打"（Play the game to win）**：目标是名次而非平均精度，冠军明确表示围绕 Brier 做后处理锐化。
- **简洁模型的稳定性**：LR 在未见比赛上胜过 GBDT。

## 5. 可迁移性评估

- **可直接迁移**：
  - **概率预测任务优先做校准**（裁剪、LR 融合、isotonic 校准）。
  - 小样本评测集上，**稳定性 > 拟合能力**。
  - 引入**外部市场/聚合信息**作为正交特征（任何有公开预测市场的领域都适用）。
  - 验证要区分"已见/未见"阶段，别只看一个总榜。
- **需要前提**：
  - 外部市场数据（赔率、预测市场）的获取与合规使用。
- **不建议照搬**：
  - 直接追求公开榜最优而忽略校准（本场公开/私榜差异明显）。

## 6. 对新手的关键启示

1. **先判断评测集大小**：样本越小，方差越大，"稳"比"准"更重要。
2. **概率预测一定要校准**，并在极端值处裁剪。
3. **简单的线性模型常被低估**，尤其在需要校准的场景。
4. **外部市场数据是被忽视的高质量信号源**。

## 7. 出处

- 讨论区索引：`intel/march-machine-learning-mania-2026/topics.md`（120 条）
- 已收录 write-up（8 篇）：
  - 1st（72 票）：https://www.kaggle.com/competitions/march-machine-learning-mania-2026/discussion/689528
  - 2nd（15 票）：https://www.kaggle.com/competitions/march-machine-learning-mania-2026/discussion/689537
  - 3rd（34 票）：https://www.kaggle.com/competitions/march-machine-learning-mania-2026/discussion/689321
  - 10th（16 票）：https://www.kaggle.com/competitions/march-machine-learning-mania-2026/discussion/689044
  - 银牌方案（13 票）：https://www.kaggle.com/competitions/march-machine-learning-mania-2026/discussion/689174
