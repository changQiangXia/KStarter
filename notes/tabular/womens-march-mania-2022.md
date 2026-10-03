# Women's March Mania 2022（精简）

> 主题：tabular ｜ 子类：sports ｜ 类别：Community ｜ 截止：2022-03-15 ｜ 队伍数：200+ ｜ 指标：Brier
> 出处：`intel/womens-march-mania-2022/`（80 条主题索引 + 6 篇 write-up 正文）

## 任务

与男子赛分开设题，预测女子 NCAA 锦标赛胜负概率。

## 关键要点

- 2nd 明确记录："**我今年的提交与 2021 年的代码完全相同**"（2021 年他拿到男子第 10、女子第 12）——同一代码跨年、跨性别赛事直接复用。
- 他还专门感谢社区成员提供并维护了**提交评分 UI 工具**——公共工具也是社区基础设施的一部分。
- 女子赛事可用数据更少（历史数据质量低于男子赛），因此简单稳健的方案更常见。

## 可迁移要点

- **同一赛事系列跨年份复用代码是完全合理的策略**（前提是假设未被规则/数据结构变化推翻）。
- 数据更稀缺的子赛事（女子赛）应优先保证稳健性。

## 轻读结论（2026-10 补）

**一句话**：女篮强弱差距大 → **概率极端化（override/赌博）比建模更有效**；冠亚军都不是"更准的模型"，而是"把预测推向极端 + 用两个提交互补覆盖结果分支"。

- 1st（317817）：passive 提交 = 纯 LightGBM 无后处理 **0.43574（铜牌）**；aggressive 提交 = override Stanford/UConn/South Carolina → **0.35438（第 1）**；自述"运气成分大，明年多半不适用"。
- 2nd（316966）：Five38 概率近似基底 0.42217（≈31 名）；**Madtown：13 场近 0.5 的比赛在两个提交里分别设 0.36/0.64**（T=0.16、P=0.36）→ 0.38864（第 2）；全组合模拟：最差第 8、58% 前三；同一做法在男篮 542 名。
- 6th（317105）：XGBoost 回归分差 + 历史分差→胜率映射；三条 override（≥92.5%→99%、首轮 1/2 号种子 99.9%、第二轮 1 号 99%）。
- 40th（316863）：3 模型集成；一份提交用"加权移动靶"，另一份基本不动；经验=下次连中间段概率也抬。

**裁决**：log-loss 型指标 + 竞争不平衡的赛程里，把高置信预测推极端可降期望损失；最终两个提交应"互补覆盖"；这套策略与赛事的竞争平衡度强绑定，不可跨赛事照搬。

**悬案**：3rd/5th 方案缺失；1st 未给 override 概率值；归档仅 2 图。

## 图表证据

![13 场赌博的全组合模拟](../../intel/womens-march-mania-2022/bodies/316966_img/02.png)

**图 1**（topic 316966）：13 场近 0.5 比赛的命中数 → 分数/名次/概率表；最差也只有第 8，实际 k=9 得第 2。

## 出处

- 讨论区索引：`intel/womens-march-mania-2022/topics.md`
- 2nd（33 票）：https://www.kaggle.com/competitions/womens-march-mania-2022/discussion/316966
- 6th（18 票）：https://www.kaggle.com/competitions/womens-march-mania-2022/discussion/317105
- 40th（17 票）：https://www.kaggle.com/competitions/womens-march-mania-2022/discussion/316863
- 1st（317817）：https://www.kaggle.com/competitions/womens-march-mania-2022/discussion/317817
- 4th（17 票）：https://www.kaggle.com/competitions/womens-march-mania-2022/discussion/317183
- 轻读全本：`analysis/deep/womens-march-mania-2022.md`（Tier B 轻读：对照矩阵/裁决/证据分级/悬案 + 1 图证）
