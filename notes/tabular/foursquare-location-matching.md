# Foursquare - Location Matching

> 主题：tabular（实体匹配）｜ 子类：— ｜ 领域：地理/POI ｜ 类别：Featured
> 截止：2022-XX-XX ｜ 队伍数：1000+ ｜ 机制：标准赛 ｜ 指标：F1（配对匹配）
> 数据来源：`intel/foursquare-location-matching/`（80 条主题索引 + 6 篇 write-up 正文）

## 1. 任务与数据

- 预测目标：把来自不同来源/语言的 POI（兴趣点）记录匹配为同一实体（实体匹配 / record linkage）。
- 数据形态：名称、地址、坐标、类别等字段；**多语言**（需要按语言分别预处理）。
- 构造陷阱（本场最突出）：
  - **比赛存在大规模数据泄漏**：社区帖指出 **67% 的测试行可通过公开数据泄漏获得**；13th 明确指出"因为泄漏，已经无法区分好方案与过拟合方案"，这是比赛设计层面的重大缺陷；
  - 多语言字段需要分语言规范化；
  - 配对任务的正负样本极度不平衡。

## 2. 方案谱系

| 方案 | 名次 | 关键点 |
| --- | --- | --- |
| 分语言预处理 + 嵌入 + "Word Tour" | 7th | 按语言处理 name/address 后转嵌入；"Word Tour" 被作者强调为可迁移到其他任务的关键部件 |
| 四阶段流水线 | 13th | ①候选生成 → ②LightGBM 过滤 → ③匹配（xlm-roberta-base / mdeberta-v3）→ ④GNN 做节点分类后处理；用 `GroupKFold(group='point_')` |

## 3. 关键技巧

- **候选生成 + 过滤**：配对任务不能直接全量比对，必须先召回再精判（与推荐系统的召回-排序同构）。
- **多语言处理**：按语言分别做规范化与嵌入。
- **图模型做后处理**：把匹配结果当作图上的节点分类问题（一致性约束）。
- **按实体分组验证**：`GroupKFold` 按 `point_` 分组，避免同一地点跨折。
- **对泄漏的应对**：识别到泄漏后，公开讨论的价值下降——这类比赛的结论要谨慎采信。

## 4. 可迁移性评估

- **可直接迁移**：
  - **实体匹配的四阶段骨架**（候选生成 → 过滤 → 匹配模型 → 图后处理）；
  - 多语言字段的分语言规范化；
  - 用 GNN 做匹配结果的一致性后处理；
  - 按实体分组验证。
- 需要前提：多语言模型（XLM-R 等）；图模型工具链。
- 不建议照搬：在存在泄漏的比赛里过分相信榜单驱动的技术结论。

## 5. 对新手的关键启示

1. **配对/匹配类任务先想"召回-精判"**，别一上来就做全量二分类。
2. **泄漏会摧毁比赛的比较价值**——学会识别它，并谨慎对待这类比赛的经验。
3. 多语言场景下，**预处理要分语言做**。

## 6. 出处

- 讨论区索引：`intel/foursquare-location-matching/topics.md`（80 条）
- 已收录 write-up（6 篇）：
  - 1st（92 票）：https://www.kaggle.com/competitions/foursquare-location-matching/discussion/336055
  - 3rd（61 票）：https://www.kaggle.com/competitions/foursquare-location-matching/discussion/338112
  - 7th（66 票，含推理代码）：https://www.kaggle.com/competitions/foursquare-location-matching/discussion/335800
  - 13th GNN（102 票）：https://www.kaggle.com/competitions/foursquare-location-matching/discussion/336124
  - 泄漏说明（59 票，67% 测试行泄漏）：https://www.kaggle.com/competitions/foursquare-location-matching/discussion/335799
