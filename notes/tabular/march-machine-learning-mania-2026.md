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

## 7. 轻读结论（2026-10 补）

**一句话**：seed diff 是主导先验，增量在"委员会没建模的东西"（连续评分/伤病/市场）；小样本要求重度正则与概率校准。

- 1st 0.10975：harry_Rating + 伤病扣减 + 等渗校准（CV 0.1620→0.1590）+ 边缘锐化（≤3%/≥97%，自认负 EV 赌名次）。
- 2nd 0.11499：XGB 60%+LR 40%、clip [0.02,0.98]；CV 0.1925/0.148 vs 终分 0.115 的 gap 归因"chalky year + 63 场小样本"。
- 3rd 0.11604：**Stage 2 用 LR 胜 XGB**（CV 0.124 vs 0.157）；33→23 / 19→11 激进剪枝（单轮 −0.007）；市场分层（R1 男 80%/女 65%）。
- 银牌 0.12007：净胜分回归 + 5 次样条校准；BartTorvik +3.1%；LOSO 22 季模型全保留做免费集成；80/20 与无 Torvik 模型混合。

**数字账精选**：校准 −0.003（1st）；剪枝 −0.007（3rd）；BartTorvik +3.1%（银牌）；clip 0.98 vs 0.99 的 Brier 差（2nd）；命中率 83.7%（银牌）。

**失败学**：更深树（2nd：depth 6/8 更差）；LR+XGB 在小数据上混合（3rd 实测双降）；把单独有效的特征叠加（多重共线）；递归加权（伤 LR）；等渗校准在与 OOF 分布不一致时（3rd 提到 early isotonic 失败于 Stage2）；锐化是负 EV 赌注。

**悬案**：4th–9th 未细读；市场抓取不可复现；伤病人工录入；CV-终分 gap 需多年回测。

## 8. 图表证据

![1st 的边缘锐化](../../intel/march-machine-learning-mania-2026/bodies/689528_img/01.png)

**图 1**（topic 689528）：Regular vs Sharp 预测密度——锐化把 ≤3%/≥97% 边缘推到极端。

![3rd 的市场分层混合](../../intel/march-machine-learning-mania-2026/bodies/689321_img/01.png)

**图 2**（topic 689321）：Tier 1 R1 市场（男 80%/女 65%）→ BPI BT（25%/15%）→ Kalshi（15%/15%）→ 纯 LR（100%），含 fallback 与覆盖量。

## 9. 出处

- 讨论区索引：`intel/march-machine-learning-mania-2026/topics.md`（120 条）
- 已收录 write-up（8 篇）：
  - 1st（72 票）：https://www.kaggle.com/competitions/march-machine-learning-mania-2026/discussion/689528
  - 2nd（15 票）：https://www.kaggle.com/competitions/march-machine-learning-mania-2026/discussion/689537
  - 3rd（34 票）：https://www.kaggle.com/competitions/march-machine-learning-mania-2026/discussion/689321
  - 10th（16 票）：https://www.kaggle.com/competitions/march-machine-learning-mania-2026/discussion/689044
  - 银牌方案（13 票）：https://www.kaggle.com/competitions/march-machine-learning-mania-2026/discussion/689174
