# JPX Tokyo Stock Exchange Prediction

> 主题：tabular ｜ 子类：— ｜ 领域：金融 ｜ 类别：Featured
> 截止：2022-09-08 ｜ 队伍数：2000+ ｜ 机制：标准赛 ｜ 指标：Sharpe 型（含收益率与风险）
> 数据来源：`intel/jpx-tokyo-stock-exchange-prediction/`（80 条主题索引 + 6 篇 write-up 正文）

## 1. 任务与数据

- **预测目标**：对东京证券交易所股票做次日的多空组合排序（按收益率排序做多/做空），评分与收益风险比相关。
- **数据形态**：日频量价 + 财务数据 + 期权隐含波动等；目标由股价变化定义。
- **构造陷阱（本场最特殊）**：**股价是公开信息**——只要用历史真实价格，就能构造接近完美的提交。主办方因此专门实施了 **leaderboard 清理（redactions）** 政策，周期性删除"没有历史数据就不可能做到"的提交。

## 2. 验证方案

| 方案 | 使用者 | 说明 |
| --- | --- | --- |
| 时间切分 + 分板块建模 | 8th | 按 33SectorName 分组，每组一个 LGBM |
| 简单的排序规则 + 约束 | 4th | 几乎不做复杂建模 |
| 提交合理性自检 | 主办方政策 | 提交必须"在不使用历史数据的前提下可行" |

## 3. 方案谱系

| 方案 | 名次 | 关键点 |
| --- | --- | --- |
| 极简排序规则（return_1day 升/降序 + 股息规则） | 4th | 作者自述"**这个结果主要是运气**"；同队两个模型一个 -0.196、一个 0.347 |
| 按板块分组的 LGBM（33 个模型） | 8th | 假设不同板块的收益驱动因素不同，分组建模 |
| 社区预测帖 + 往届金融赛方案汇总 | 参考 | 大量横向引用（Optiver、Winton、BattleFin 等） |

## 4. 关键技巧

- **分组建模**：按行业板块分别训练，是金融表格赛的常规做法。
- **规则型提交也可能是最优解**（本题 4th 的方案几乎没有机器学习）。
- **排行榜可信度要主动判断**：本场存在"公开信息即可满分"的结构性问题，主办方只能靠人工清理。
- **运气成分必须被承认**：同一团队的同类模型分数可以从 -0.196 到 0.347。

## 5. 可迁移性评估

- **可直接迁移**：
  - **判断目标是否可由公开信息直接构造**（价格/榜单/可查询数据）——这决定比赛是否"真实可比"。
  - 分组（按行业/区域/类别）建模的思路。
  - 提交前的"合理性自检"：这个分数在不用外部信息时能否达到？
- **需要前提**：
  - 金融域知识（板块、股息、成交约束）。
- **不建议照搬**：
  - 依赖历史真实价格构造提交（规则上可行但在多数比赛属于破坏性行为，且主办方会清理）。

## 6. 对新手的关键启示

1. **先问"目标信息是否公开可得"**：这是判断比赛质量与策略的第一步。
2. **金融赛里简单规则常常打平复杂模型**。
3. **不要把一次高分当作能力证明**（本场 4th 明确说靠运气）。

## 7. 轻读结论（2026-10 补）

**一句话**：金融赛的"运气与泄漏"双重问题——**随机模型得分 ≈ N(0, 0.13785)**，0.3 以内无法区分能力；股价是公开数据，host 需定期清理"用历史数据做出的完美提交"。第 4 名公开承认"主要是运气"：按 `return_1day` 排名（股息调整），升序私榜 -0.196、**降序 +0.347（第 4）**，并指出"**排名翻转使分数取负，而本赛可提交两个模型 → 正反两版保证分数 > 0**"。

- 4th（359151）：无 ML；关键在于 `ExpectedDividend`（除权日前 2 交易日记录）与 target 时间窗（t+2 vs t+1）→ 除权日附近目标大概率负；公开完整 notebook。
- 8th（359227）：按 **33SectorName 分 33 个 LGBM**（板块内相关假设），目标=收益率排名；Optuna 调一组超参后复用到各组。
- 治理（116 票）：host 明确"用历史数据拿满分不违规但无意义"，周期性清理，后期暂停以允许全量训练。
- 社区：幸运冠军（67 票）、股票预测的愚蠢错误（82 票）、无泄漏 CV（74 票）、做空除权日（45 票）。

**裁决**：金融赛先算随机基线再解释名次；寻找会计/日历性结构（除权、停牌、指数调整）；榜单泄漏靠机制治理；引用时区分官方政策与社区猜测。

**悬案**：1st–3rd/5th–7th 方案缺失；清理政策对名次的影响无数据；除权策略的真实交易成本未讨论。

## 8. 图表证据

无可用图证（本场唯一归档图为装饰图，按规则不内嵌）。

## 9. 出处

- 讨论区索引：`intel/jpx-tokyo-stock-exchange-prediction/topics.md`（80 条）
- 已收录 write-up（6 篇）：
  - 排行榜清理政策（116 票）：https://www.kaggle.com/competitions/jpx-tokyo-stock-exchange-prediction/discussion/317413
  - 4th（37 票）：https://www.kaggle.com/competitions/jpx-tokyo-stock-exchange-prediction/discussion/359151
  - 往届金融赛方案汇总与预测帖：见讨论区
  - 首次分数更新公告（31 票）：https://www.kaggle.com/competitions/jpx-tokyo-stock-exchange-prediction/discussion/337385
  - 8th 板块 LGBM：https://www.kaggle.com/competitions/jpx-tokyo-stock-exchange-prediction/discussion/359227
  - 幸运冠军（67 票）：https://www.kaggle.com/competitions/jpx-tokyo-stock-exchange-prediction/discussion/320323
  - 做空除权日（45 票）：https://www.kaggle.com/competitions/jpx-tokyo-stock-exchange-prediction/discussion/320836
  - 无泄漏 CV（74 票）：https://www.kaggle.com/competitions/jpx-tokyo-stock-exchange-prediction/discussion/324217
- 轻读全本：`analysis/deep/jpx-tokyo-stock-exchange-prediction.md`（Tier B 轻读：对照矩阵/裁决/证据分级/悬案；图证缺口已登记）
