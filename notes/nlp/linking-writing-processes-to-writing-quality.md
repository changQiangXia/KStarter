# Learning Agency Lab - Linking Writing Processes to Writing Quality

> 主题：nlp（行为日志）｜ 子类：— ｜ 领域：教育 ｜ 类别：Featured
> 截止：2023-11-21 ｜ 队伍数：2000+ ｜ 机制：代码赛 ｜ 指标：RMSE（作文质量）
> 数据来源：`intel/linking-writing-processes-to-writing-quality/`（80 条主题索引 + 6 篇 write-up 正文）

## 1. 任务与数据

- **预测目标**：由**按键日志（keystroke logs）**预测作文质量分数。
- **数据形态**：事件级行为序列（按键、暂停、删改）+ 少量文章元数据；每条日志对应一名学生的一次写作过程。
- **构造陷阱**：
  - 事件日志需要**聚合成行为特征**（停顿分布、修改率、爆发写作等）。
  - 数据泄漏风险：同一学生的多条日志、文本长度与质量的耦合。
  - 本场出现**队伍被取消资格**的情况（榜单结构因此变化），提示规则合规的重要性。

## 2. 验证方案

| 方案 | 使用者 | 说明 |
| --- | --- | --- |
| "Trust CV is all you need" | 3rd | 明确定调：本地 CV 可信，直接以 CV 决策 |
| 清洗 + 特征 + 外部数据 | 1st | 数据清洗与特征工程是主要收益来源 |

## 3. 方案谱系

| 方案 | 名次 | 关键点 |
| --- | --- | --- |
| 数据清洗 + 特征工程 + 外部数据 + 模型集成 | 1st | 强调清洗与外部数据；代码全开源 |
| 以 CV 为唯一决策依据 | 3rd | "Trust CV is all you need" |
| Blend MLM 预训练 DeBERTa | 3rd（并列方案） | 用掩码语言模型预训练增强表示 |
| 原 1st 方案（队伍被取消资格） | 被 DQ | 8 模型的集成方案，私榜 0.557 / 公开 0.575 |

## 4. 关键技巧

- **行为日志 → 聚合特征**：按键间隔分布、暂停时长、修改频率、写作节奏等。
- **数据清洗优先**（与同系列赛事一致）。
- **外部数据融合**（同系列往届数据）。
- **信任 CV**（当 CV-LB 相关性被验证后）。

## 5. 可迁移性评估

- **可直接迁移**：
  - 行为日志的特征化方法（时间间隔统计 + 事件类型计数 + 节奏指标）。
  - 先验证 CV-LB 相关性，再决定是否以 CV 为唯一依据。
  - 同系列赛事的数据可以合并（注意防泄漏）。
- **需要前提**：
  - 需要理解日志结构；事件量级大。
- **不建议照搬**：无。

## 6. 对新手的关键启示

1. **行为日志类任务的核心是"把事件流变成统计特征"**。
2. **CV 可信时就不必追榜**（3rd 的标题就是结论）。
3. **规则合规与团队管理同样影响结果**（本场有队伍被取消资格）。

## 7. 轻读结论（2026-10 补）

**一句话**：击键日志→重建文本→大规模特征+外部作文数据迁移+异构集成；本场还有一次"冠军 DQ、亚军递补"的治理事件。

- 新 1st（94 票，原 2nd 递补）：数据清洗（ftfy/时间修正/丢输入前 10 分钟）+ 句式重建（模糊匹配/Undo）+ 378 特征 + **8 个外部作文数据集训练的外部分数特征**；单模 CV 0.576–0.609；嵌套 CV 6 bags×5 folds；clip [0.5,6.0]；3 个 GPU 模型中公榜最差（0.578）的私榜胜出——自认幸运。
- 被取消资格的 1st（58 票）：5 人 8 模型（LGBM 0.59759/denselight 0.6135，char tf-idf +0.005、plr embedder +0.01）；**DQ 原因未收录**。
- 3rd（79/117 票）：GBT(165 特征)+DeBERTa(persuade MLM+q→i/X)；**GBM 的 LB/CV 比更好、DeBERTa CV 好 LB 差** → 域移。
- No place（466945）：1356 特征 + 手动权重 65% LGBM/35% NN（Ridge 会高估低 CV 的 NN）。

**裁决**：重建质量是地基；字符 tf-idf 稳；跨家族融合按"信任哪个域"定权，不要只用 OOF。

**悬案**：DQ 原因与官方 recap（468441）未收录；外部数据泄漏边界/效率奖配置未展开。

## 8. 图表证据

![新 1st 的方案流程](../../intel/linking-writing-processes-to-writing-quality/bodies/466873_img/01.jpg)

**图 1**（topic 466873）：比赛数据/外部数据双管线 → 重建文本+tf-idf+外部分数 → 多模型集成 → 后处理。

![3rd 的 CV-LB 关系](../../intel/linking-writing-processes-to-writing-quality/bodies/466906_img/01.png)

**图 2**（topic 466906）：单模型与融合的 CV vs LB（点在拟合线上方，LB>CV），展示域移。

## 9. 出处

- 讨论区索引：`intel/linking-writing-processes-to-writing-quality/topics.md`（80 条）
- 已收录 write-up（6 篇）：
  - 1st（94 票）：https://www.kaggle.com/competitions/linking-writing-processes-to-writing-quality/discussion/466873
  - 原 1st（队伍被 DQ，58 票）：https://www.kaggle.com/competitions/linking-writing-processes-to-writing-quality/discussion/467154
  - 3rd "Trust CV"（117 票）：https://www.kaggle.com/competitions/linking-writing-processes-to-writing-quality/discussion/466775
  - 3rd 并列（79 票）：https://www.kaggle.com/competitions/linking-writing-processes-to-writing-quality/discussion/466906
- 轻读全本：`analysis/deep/linking-writing-processes-to-writing-quality.md`（Tier B 轻读：对照矩阵/裁决/证据分级/悬案 + 2 图证）
