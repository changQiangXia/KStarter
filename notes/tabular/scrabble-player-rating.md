# Scrabble Player Rating（RMSE，玩家级聚合特征与分组之谜）

> 主题：tabular ｜ 子类：— ｜ 领域：棋类游戏 ｜ 类别：Playground
> 截止：2022-12-15 ｜ 队伍数：301 ｜ 机制：标准赛 ｜ 指标：RMSE
> 数据来源：`intel/scrabble-player-rating/`（12 条主题索引 + 6 篇正文）

## 1. 任务与数据

- 预测 Scrabble 对局中的玩家评分变化（RMSE）；数据为对局-回合级。
- **关键结构**：一位玩家的全部对局历史**要么全在训练、要么全在测试**（按昵称完整切分）——这是验证设计的核心谜题。

## 2. 验证方案（本场最大的未解问题）

- 社区帖作者的实践：普通 KFold → 发现"玩家历史整块切分"后改 GroupKFold（按昵称）→ **CV 分数显著变差**；再试 StratifiedGroupKFold（按 time_control/rating_mode/lexicon 分层）也无改善；
- 他的公开提问（"整块切分是否正确？"）未获完整解答——**小赛的验证口径难题常以社区悬案形式存在**。

## 3. 模型家族

| 方案 | 使用者层次 | 关键点 | 出处 |
| --- | --- | --- | --- |
| 玩家历史聚合特征 + LGBM + Optuna | 社区主力 | min/max/mean 的"截至当前局"历史统计 | topic 372554 |
| 高级数据集（含 difficult_word 等新特征） | 社区 | 特征外溢复用 | topic 363143 |

## 4. 关键技巧

- **"截至当前"聚合**：对玩家的历史分数做 min/max/mean（严格使用当前局之前的数据）——防泄漏的时序聚合写法。
- 小赛（12 个讨论帖）的残酷现实：公开资产稀少，验证口径靠自力更生；作者权衡后**保留普通 KFold**（与评分相关性优先），体现"CV 依赖数据切分假设"的两难。

## 5. 可迁移性评估

- **可直接迁移**：按实体"截至当前"的聚合特征规范；GroupKFold 与普通 KFold 冲突时的权衡方法（看哪个 CV 与 LB 相关）；小赛的自力更生策略。
- **需要前提**：能识别实体完整块切分的结构。
- **不建议照搬**：无脑跟随"应该分组"的教条（本场分组 CV 反而更差，需量化决策）。

## 6. 对新手的关键启示

- "分组验证永远更好"不是教条：要量化它对 CV–LB 相关性的影响（本场是反例）。
- 时序类聚合一定写"截至当前"版本。
- 小赛练手价值高（竞争小、问题干净），但公开答案少，适合检验自己的判断力。

## 7. 轻读结论（2026-10 补）

- **301 队、RMSE**；任务是用 woogles.io 人类 vs 3 bot 对局预测玩家评分（第二个 woogles 数据赛，前作预测下一手得分）（362735）。
- **赛后复盘**：玩家历史聚合（此前各局 min/max/mean）+ 回合特征 → LightGBM + Optuna；KFold → GroupKFold(nickname) 后分数显著变差，StratifiedGroupKFold（time_control × rating_mode × lexicon）改善有限；**作者最终选择未在归档中说明**（372554，登记为悬案）。
- **公开基线**：metlover 的 CNN/ANN（Flux.jl）17.24339 RMSE；另有 turn 分析/basicbot/omgwords starter；社区"Advanced Dataset, FE+AGG"（difficult_word 等）（362744 / 363143）。
- **裁决**：按 data 切分逻辑，GroupKFold 是诚实口径、KFold 是乐观上界；玩家级特征必须在分组 CV 下评估（悬案：需对照 LB 才能最终定论）。

## 8. 图表证据

本场 0 张归档图（0/0），**图证缺口已登记**。

## 9. 出处

- 赛后讨论（聚合特征与 CV 之谜）：https://www.kaggle.com/competitions/scrabble-player-rating/discussion/372554
- 高级数据集 FE+AGG：https://www.kaggle.com/competitions/scrabble-player-rating/discussion/363143
- 官方欢迎与任务设定：https://www.kaggle.com/competitions/scrabble-player-rating/discussion/362735
- 公开 kernel 清单：https://www.kaggle.com/competitions/scrabble-player-rating/discussion/362744
- RMSE 资源：https://www.kaggle.com/competitions/scrabble-player-rating/discussion/362749
