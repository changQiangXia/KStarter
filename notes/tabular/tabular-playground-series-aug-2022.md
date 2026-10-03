# Tabular Playground Series - Aug 2022（海绵失效预测，缺失即信号）

> 主题：tabular ｜ 子类：— ｜ 领域：制造（合成数据） ｜ 类别：Playground
> 截止：2022-08-31 ｜ 队伍数：1888 ｜ 机制：标准赛 ｜ 指标：ROC AUC
> 数据来源：`intel/tabular-playground-series-aug-2022/`（80 条主题索引 + 6 篇 write-up 正文）

## 1. 任务与数据

- 预测目标：合成"吸水海绵"产品在实验室测试中的失效（AUC）。
- 背景故事（本场最有名的 EDA 帖）：从官方设定出发解读每个字段（两层材料、层数/strata、测量值里混有"实验参数"）——**读背景故事是理解合成字段语义的低成本入口**（Ambrose 式 EDA）。

## 2. 验证方案

- 常规 5–10 折；缺失模式的显著性检验：对"某测量缺失"的条件失效率做 z 检验（对照 p=0.2126 的二项零假设）。

## 3. 模型家族

| 方案 | 使用者层次 | 关键点 | 出处 |
| --- | --- | --- | --- |
| 缺失指示特征 + 常规 GBDT | 社区 | 两行代码的显著增益 | topic 342319 |
| 14th（本可第 6） | 社区 | 选择/运气复盘 | topic 349810 |
| 特征工程"少即是多" | 社区 | 精简特征清单 | topic 342126 |

## 4. 关键技巧

- **缺失即信号（带统计检验）**：`measurement_3` 缺失时失效率 0.160（z=-2.50, p=0.012）、`measurement_5` 缺失时 0.254（z=2.66, p=0.008）——两行 `isna()` 指示特征进入模型；其余测量缺失不显著。**别把缺失一律插补掉**。
- 机制假设先行：作者推断"测量设备失效可能是产品失效的并发结果"，再用条件失效率验证——先写假设、再检验。
- "Less can be more"：本场有效特征集中在少数测量与缺失指示，精简特征优于堆砌。

## 5. 可迁移性评估

- **可直接迁移**：缺失指示 + z 检验的显著性流程（任何有缺失的诊断类数据）；从背景故事提取字段语义；条件失效率分析法。
- **需要前提**：缺失比例适中、样本量支持检验。
- **不建议照搬**：所有缺失都做指示（本场只有 2 个显著）；不检验就相信"缺失有信号"的直觉。

## 6. 对新手的关键启示

- **缺失值不是脏数据**，是可能的事件：先算"缺失条件下的目标率"，再决定插补还是保留指示。
- 遇到合成字段，先读官方背景故事和社区解读帖——语义线索就在这里。
- 一个两行代码的假设检验，可能胜过数小时的调参。

## 7. 出处

- 背景故事解读：https://www.kaggle.com/competitions/tabular-playground-series-aug-2022/discussion/341462
- 缺失值有预测价值（含显著性表）：https://www.kaggle.com/competitions/tabular-playground-series-aug-2022/discussion/342319
- Less can be more：https://www.kaggle.com/competitions/tabular-playground-series-aug-2022/discussion/342126
- 14th 复盘：https://www.kaggle.com/competitions/tabular-playground-series-aug-2022/discussion/349810
