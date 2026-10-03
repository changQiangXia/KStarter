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

## 7. 出处

- 讨论区索引：`intel/linking-writing-processes-to-writing-quality/topics.md`（80 条）
- 已收录 write-up（6 篇）：
  - 1st（94 票）：https://www.kaggle.com/competitions/linking-writing-processes-to-writing-quality/discussion/466873
  - 原 1st（队伍被 DQ，58 票）：https://www.kaggle.com/competitions/linking-writing-processes-to-writing-quality/discussion/467154
  - 3rd "Trust CV"（117 票）：https://www.kaggle.com/competitions/linking-writing-processes-to-writing-quality/discussion/466775
  - 3rd 并列（79 票）：https://www.kaggle.com/competitions/linking-writing-processes-to-writing-quality/discussion/466906
