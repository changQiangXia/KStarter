# Tabular Playground Series Nov 2021（分块数据与探榜事件）轻量深读（Tier B）

> 赛事：Playground ｜ 主题 tabular（二分类，AUC）｜ 1362 队 ｜ 标准赛 ｜ 指标：ROC AUC
> 材料基础：`digests/tabular-playground-series-nov-2021.md`（6 篇正文：1st 291883 / 3rd 291766 / 社区推测 288221 / 生产力指南 287989 / 三重大师 285092 / 学习>=获胜 285738；80 条主题索引）+ 1 张归档图
> 轻读时间：2026-10（Tier B B15）

## 1. 一句话重述与数字账

本场是 Playground 历史上最有名的**数据分块/探榜事件**：训练与测试位于特征空间的不同区域，且数据被切成 9 个 6 万行的块（每块再按超平面分成两个半块）。结果是**常规 CV 完全失效**——3rd 明确说 GroupKFold/分层 CV 都无用，连"用泄漏数据训练的一对 DummyRegressor"都能击败所有真实模型；3rd 于是放弃 CV，用 18 次提交把 18 个半块的目标概率**从公榜探出来**，再以 92%:8% 融合公开 notebook 拿下季军。1st 则走"NN + 重标注 top 5% 误标 + 5% 伪标签 + rank 融合"路线。

| 关键数字 | 值 | 来源 |
| --- | --- | --- |
| 3rd（291766） | 发现训练/测试区域不同 → 加权训练实验失败；数据分块公开后改用 GroupKFold 仍无效（"九块学不到第十块"）；**完全放弃 CV**，用公榜探出 **18 个半块**的目标概率（每半块一次提交，5 次/天 × 4 天）；最终融合权重 = 半块概率 92% + 公开 notebook 8% | 291766 |
| 1st（291883） | 简单 NN OOF ≈ LB 0.749 → **重标注 top 5% 疑似误标样本** 再训（0.75010）→ 用 **5% 伪标签** 重训（0.75070）→ 与 ambrosm/pourchot 的"chunk 处理 kernel"融合；强调融合前先做 **rank(pct=True)**（AUC 只看排序） | 291883 |
| 社区预测帖（288221） | 34 票：预言获胜方案不会有"核弹技巧"，而是"干净、有组织、数百万小步迭代"的产物；NN 在本数据上开箱更强；给出 XGB/LGBM/CatBoost 的 Optuna 模板 | 288221 |
| 治理事件 | "Mislabeled samples"（47 票 / **121 评论**）；"Is he a thief?"（38 票 / 25 评论，围绕泄漏数据的使用）；"The data is chunked!"（28 票 / 25 评论）；"Overfitting tool"（35 票）；"Trick AUC"（30 票） | 索引 |
| 其他 | 生产力指南（80 票 / 20 评论）；"Feedback Requested"（77 票 / 89 评论，系列赛方向讨论）；三重大师帖（83 票 / 84 评论）；"Learning >= Winning"（16 票） | 索引 |

## 2. 逐方案对照矩阵

| 维度 | 1st | 3rd | 大多数参赛者 |
| --- | --- | --- | --- |
| 数据观 | 误标 + 伪标签 | 分块 + 区域差异（CV 无效） | 常规 CV |
| 验证 | OOF + 公榜 | **放弃 CV，只用公榜** | GroupKFold/分层 KFold（失效） |
| 关键动作 | 重标注 5%、5% 伪标签、rank 融合 | 探榜 18 个半块、92:8 融合 | 正常建模 |
| 结果 | 1st | 3rd | — |

## 3. 共识、分歧与裁决

### 事件一：分块结构使 CV 失效，探榜成为最优策略（3rd、286731、291766；置信度高）

九块之间没有可迁移信息；泄漏数据让 dummy 模型击败真实模型；3rd 用 18 次提交探出半块概率。**裁决**：当"验证不可信 + 公榜可探"时，常规建模纪律被完全颠覆；这是赛制缺陷导致的极端案例（登记为治理教训，不建议复刻）。置信度：高。

### 事件二：泄漏数据的使用引发道德争议（285503、285700；置信度中高）

121 条评论的"误标样本"讨论与"他是小偷吗"的指控，说明社区对"使用泄漏"的边界存在严重分歧。**裁决**：泄漏手段即使合规也带来声誉风险；当代 Kaggle 对泄漏的审查已显著加强。置信度：中高。

### 共识：1st 的干净路线 = 误标修正 + 伪标签 + rank 融合（291883；置信度中）

1st 的增益来自重标注 top 5% 与伪标签，最终靠 rank 融合公开 kernel 收尾。**裁决**：在无法信 CV 的比赛里，模型侧仍可做"数据修正 + 半监督"，但融合务必 rank 化。置信度：中。

### 元观点：获胜方案是"小步迭代"而非核弹（288221；置信度中高）

社区预言帖的两条核心判断（无核弹技巧、NN 开箱更强）事后看都被验证。**裁决**：这类"预写获胜方案画像"的帖子本身是很好的赛前策略检查表。置信度：中高（含事后验证）。

## 4. 证据分级

| 断言 | 等级 | 说明 |
| --- | --- | --- |
| 3rd 的探榜与 92:8 融合 | 自述（含数学引用） | 中高 |
| 1st 的重标注/伪标签/rank | 自述（简短） | 中 |
| 分块与 CV 失效 | 高票社区帖 + 3rd 自述 | 中高 |
| 泄漏争议 | 121 评论的讨论帖 + 指控帖 | 中高（现象） |
| 社区预测帖 | 观点帖（事后验证） | 中 |

## 5. 悬案与缺口（登记）

- 2nd、4th–10th 方案未收录；
- "Is he a thief?" 的最终裁定未收录；
- 探榜方法的完整数学细节（safavieh 的 notebook）未展开；
- **图证缺口**：仅 1 张梗图（"Trust your CV? Always."）。

## 6. 图表证据

![Trust your CV meme](../../intel/tabular-playground-series-nov-2021/bodies/288221_img/01.png)

**图 1**（topic 288221）：社区预测帖配图"Trust your CV? Always."——与本场 CV 完全失效的反差形成黑色幽默（该帖预言的"无核弹技巧"结论事后被验证）。

## 7. 出处

- 1st（21 票）：https://www.kaggle.com/competitions/tabular-playground-series-nov-2021/discussion/291883
- 3rd Don't trust the cv scores（27 票 / 14 评论）：https://www.kaggle.com/competitions/tabular-playground-series-nov-2021/discussion/291766
- 社区预测帖（34 票 / 11 评论）：https://www.kaggle.com/competitions/tabular-playground-series-nov-2021/discussion/288221
- Mislabeled samples（47 票 / 121 评论）：https://www.kaggle.com/competitions/tabular-playground-series-nov-2021/discussion/285503
- Is he a thief?（38 票 / 25 评论）：https://www.kaggle.com/competitions/tabular-playground-series-nov-2021/discussion/285700
- The data is chunked!（28 票 / 25 评论）：https://www.kaggle.com/competitions/tabular-playground-series-nov-2021/discussion/286731
- 生产力指南（80 票 / 20 评论）：https://www.kaggle.com/competitions/tabular-playground-series-nov-2021/discussion/287989
- Feedback Requested（77 票 / 89 评论）：https://www.kaggle.com/competitions/tabular-playground-series-nov-2021/discussion/284445
- 三重大师（83 票 / 84 评论）：https://www.kaggle.com/competitions/tabular-playground-series-nov-2021/discussion/285092
