# Home Credit - Credit Risk Model Stability

> 主题：tabular ｜ 子类：— ｜ 领域：金融 ｜ 类别：Featured
> 截止：2024-05-27 ｜ 队伍数：3856 ｜ 机制：代码赛 ｜ 指标：Gini Stability（跨时间稳定性加权）
> 数据来源：`intel/home-credit-credit-risk-model-stability/`（120 条主题索引 + 8 篇 write-up 正文）

## 1. 任务与数据

- **预测目标**：预测客户违约概率，但指标是 **Gini × 稳定性**——不仅要求区分度，还要求模型表现**随时间稳定**。
- **数据形态**：多张关系型表（credit_bureau_a1 等），深度关联聚合；日期字段被相对化处理。
- **构造陷阱（本场最大特色）**：
  - 指标本身可被"钻空子"（metric hacking）：通过构造方法让不同时间段的 Gini 更一致，从而在榜上获得虚高分。
  - 比赛实际分成两个阶段：**Phase 1 机器学习，Phase 2 指标黑客**。多支队伍明确这样描述。
  - 公开榜的有效 hack 往往**不能迁移**到私榜（本场已多次验证）。

## 2. 验证方案

| 方案 | 使用者 | 说明 |
| --- | --- | --- |
| StratifiedGroupKFold（分组 + 分层） | 1st、57th | 1st 明确比较了 shuffle / no-shuffle 的差异，并指出 CV 的 0.001–0.005 差异与 LB 相关性弱 |
| 时间外推验证 | 多队 | 与 "stability" 指标直接对应 |
| 公开榜探针 | 逆优化者 | 用于判断 hack 是否生效——**这是本场比赛里最危险的动作** |

## 3. 方案谱系

| 方案 | 名次 | 关键点 |
| --- | --- | --- |
| "下注策略"：ML 模型池 + 有节制地使用指标 hack | 1st | 明确把比赛拆成 ML 与 MH 两阶段；**不用 hack 的模型池上限约 0.53**，最终成绩取决于"押多少注在 hack 上" |
| 恢复日期信息（refreshdate 反推）+ 自研方法 | 公开 8 / 私榜 253 | 自研方法公开榜 0.655，私榜 0.560–0.617；公开流传的方法私榜只有 0.510–0.520 |
| 纯 ML 多模型集成（CatBoost/LGBM/XGB/MLP/1DCNN） | 57th（0.528） | **不用 hack**；比赛前期曾进前十，hack 潮开始后名次下滑 |
| pmts_year_1139T 后处理 | 13th | 针对特定字段的后处理技巧 |
| 不使用任何 hack 的方案 | 53rd | 明确以"干净方案"为目标 |

## 4. 关键技巧

- **模型多样性与分组验证**：CatBoost / LGBM / XGB / MLP / 1DCNN 的集成，配合统一 StratifiedGroupKFold 与多层集成（L3 ensemble）。
- **特征工程**：在聚合前按 `numgroups` 排序（对 first/last 类聚合器有效）；多级分组聚合。
- **指标理解优先**：想拿名次必须理解 Gini Stability 的构造方式——**理解指标既能帮你优化，也能揭示它的漏洞**。
- **对 hack 的克制**：私榜结果反复证明"公开榜有效的 hack 私榜无效"，最终排名基本取决于判断的准确性而非 hack 强度。

## 5. 可迁移性评估

- **可直接迁移**：
  - 遇到**自定义/复合指标**时，第一件事是把指标拆开，理解它奖励什么行为（本场：区分度 + 跨期稳定性）。
  - 分组 + 分层的交叉验证设计（`StratifiedGroupKFold`）。
  - 关系型多表数据的聚合策略：排序后再聚合、多级分组。
- **需要前提**：
  - 指标 hack 依赖指标的具体实现（本题是榜单计算方式），并非普遍存在。
  - 数据恢复（如反推日期）依赖字段间的相关性结构。
- **不建议照搬**：
  - **公开榜探针驱动的 hack**：本场 253 名的案例证明其风险。
  - 把全部精力放在 hack 上而忽视模型池质量（1st 的结论是两者都要，且要控制下注比例）。

## 6. 对新手的关键启示

1. **先彻底理解评估指标**——这是本场最核心的一课，理解指标既决定优化方向，也决定风险。
2. **"能不能 hack 指标"是个策略问题**，不是道德问题；但公开榜有效的 hack 经常不可迁移，需要独立验证。
3. **不用 hack 也能拿到不错的成绩**（0.528 ≈ 57 名 / 3856 队），干净方案是可靠基线。
4. **CV 与 LB 的相关性要量化**，不要假设它们一致（1st 明确指出 CV 的微小差异与 LB 弱相关）。

## 7. 出处

- 讨论区索引：`intel/home-credit-credit-risk-model-stability/topics.md`（120 条）
- 已收录 write-up（8 篇）：
  - 1st（175 票）"My Betting Strategy"：https://www.kaggle.com/competitions/home-credit-credit-risk-model-stability/discussion/508337
  - 公开 8 / 私榜 253（60 票）：https://www.kaggle.com/competitions/home-credit-credit-risk-model-stability/discussion/507946
  - 13th（38 票）：https://www.kaggle.com/competitions/home-credit-credit-risk-model-stability/discussion/508113
  - 53rd 无 hack（29 票）：https://www.kaggle.com/competitions/home-credit-credit-risk-model-stability/discussion/508242
  - 指标 hack 讨论（73 / 39 / 32 票）：497167 ｜ 501172 ｜ 501744
