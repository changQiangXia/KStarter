# H&M Personalized Fashion Recommendations

> 主题：tabular ｜ 子类：recsys ｜ 领域：电商推荐 ｜ 类别：Featured
> 截止：2022-05-09 ｜ 队伍数：2952 ｜ 机制：标准赛 ｜ 指标：MAP@12
> 数据来源：`intel/h-and-m-personalized-fashion-recommendations/`（120 条主题索引 + 8 节正文：1st/2nd/3rd/4th/6th/52nd + Q&A + 图像数据集；另有 5th/9th/11th 等 20 条 write-up 未收录）

## 1. 任务与数据

- **预测目标**：为每位顾客推荐 12 件商品，按 MAP@12 评分（排序质量）。
- **数据形态**：交易记录（顾客 × 商品 × 时间）、商品元数据、图像；**数据量巨大但信息稀疏**（多数顾客历史极短）。
- **题目特点**：1st place 明确指出 "**训练集与测试集要自己构造**"——候选生成策略是突破精度上限的关键。
- **任务框架（Q&A）**：本质是"预测下一篮（next basket）"；候选=自己造的负样本；customer 当作 ranking query。
- **分布事实**：约 50% 用户在近 3 个月无交易（1st）；2nd 指出比赛部分在预测"商品可得性"（邮编写得显著）。

## 2. 验证方案

| 方案 | 使用者 | 说明 |
| --- | --- | --- |
| 时间切分（用最后一周做验证） | 多队 | 与线上预测窗口对齐 |
| 反馈式验证 | 1st | 强调本场 **CV 与 LB 相关性稳定**，可放心用 CV 迭代 |
| 只保留有历史行为的用户评估 | 多队 | 冷启动用户几乎无法进 top12，需单独说明 |
| 窗口×候选数网格 | 1st | 7w/100→25w/200 五配置；CV-LB 总体同向，25w 窗口 LB 反降 |
| 5 折取 3 折训练 | 4th | 更多训练数据未提升本地 CV/LB |
| 先小样本快速验证、相关性稳定后再放大 | Q&A/52nd | "Fast local validation is key" |

## 3. 方案谱系

| 方案 | 名次 | 关键点 |
| --- | --- | --- |
| 6 路召回 + 5 LGBM/7 CatBoost 排序 | 1st senkin13 | 复购/itemCF/同款/热门/图嵌入/逻辑回归；100–500 候选；单模 LB 0.0367→集成 0.0371 |
| 600 热门 + 两段 LGBM + Rust 特征框架 | 2nd | itemCF 不如热门；Paweł 的属性计数器/共现/图游走做候选多样性；0.0355→0.0368 |
| **召回策略×排名特征** + BPR 相似度 | 3rd sirius | 0.02855→0.03262（召回特征）；0.03363→0.03510（BPR，AUC 0.72）；16 模型平均 |
| 双塔 MMoE + 文本/图像聚类 | 4th | 4 路召回；门控网络服务活跃/非活跃用户；DCN 未调好，LGBM 更强 |
| 召回×模型×目标对照表 | 6th | CatBoost-120 单模 0.0403/0.0341；lambdarank-1000 掉分；类别特征 +0.0005~0.0008 |
| 20 分钟 notebook（~25 候选/人） | 52nd | 时间感知 pair-CF；33M 候选进前 2%；cuML FIL 后 12 分钟 |

## 4. 关键技巧

- **候选生成（召回）决定上限**：排序模型再好，候选里没有正确商品就无法得分。
- **热门商品是强基线**：时间加权热门 > itemCF（2nd）；1st 主召回即近期热门。
- **召回元特征**：是否被某策略召回 + 策略内排名（3rd 的最大杠杆，0.02855→0.03262）；只扩容不加该特征 CV 会崩。
- **BPR user2item 相似度**：AUC 0.720 vs 最佳手工特征 0.680；单特征 LB +0.0015；需按周重训。
- **负采样×候选数**：pos:neg≈1:300 → 30×pos（3rd）；1st 每周 100–200 万；甜区 ~100–500 候选/人，1000 候选+ranker 掉分（6th）。
- **冷启动非对称**：冷用户用人口学/双塔兜底（4th）；冷商品永远排不进 top12（1st），不必强优化。
- **窗口选择也是超参**：更长历史≠更好（25 周配置 CV 第 4、LB 垫底）。

## 5. 深读结论（2026-10 补）

- **召回策略军备竞赛**：1st 的六路召回、2nd 的计数器/共现/图游走、52nd 的时间感知 pair-CF——候选质量是 0.035→0.037 区间所有差距的来源。
- **最高杠杆是特征而非模型**：3rd 的两个单特征（召回策略×排名、BPR）合计值 ~0.0055 LB；模型家族/目标函数差异 ≤0.001。
- **极简也能进前 2%**：52nd 用 25 候选/人 + LGBMRanker 20 分钟（FIL 后 12 分钟）——MAP@12 的宽容度 + 热门先验让"先跑通端到端"本身就有高地板。
- **CV-LB 稳定但非严格同步**：1st 的网格两处反转（12w↔16w、25w 垫底）——窗口类超参必须多配置验证。
- **隐藏结构**：2nd 指出"部分分数=预测商品可得性（postal_code）"；Q&A 建议主办提供商品状态——赛题的"真实难度构成"值得 EDA 阶段主动识别。

## 6. 图表证据

**图 1：1st 的召回菜单与排序层**（topic 324070）——`../../intel/h-and-m-personalized-fashion-recommendations/bodies/324070_img/01.png`

![1st pipeline](../../intel/h-and-m-personalized-fashion-recommendations/bodies/324070_img/01.png)

*读图*：六路召回（复购/itemCF/同 product_code/热门/图嵌入/逻辑回归+类别信息）→ Top 100–500 → 排序（5 LGBM + 7 CatBoost）→ Top 12。

**图 2：1st 的窗口×候选 CV/LB 网格**（topic 324070）——`../../intel/h-and-m-personalized-fashion-recommendations/bodies/324070_img/02.png`

![cv grid](../../intel/h-and-m-personalized-fashion-recommendations/bodies/324070_img/02.png)

*读图*：20w/500 最佳（CV 0.0441 / LB 0.0367）；25w/200 CV 第 4 但 LB 垫底（0.0360）。

**图 3：4th 的四路召回架构**（topic 324094）——`../../intel/h-and-m-personalized-fashion-recommendations/bodies/324094_img/01.png`

![4th arch](../../intel/h-and-m-personalized-fashion-recommendations/bodies/324094_img/01.png)

*读图*：Two Tower MMoE / Item2Item CF / 复购 / 热门 → 候选 → LightGBM + DCN → top12。

**图 4：4th 用户塔（MMoE 门控）**（topic 324094）——`../../intel/h-and-m-personalized-fashion-recommendations/bodies/324094_img/02.png`

*读图*：embedding（age/postal_code/article_id/product_code + 时间）→ gating → 多 expert → user embedding；面向冷启动用户。

**图 5：4th 商品塔**（topic 324094）——`../../intel/h-and-m-personalized-fashion-recommendations/bodies/324094_img/03.png`

*读图*：item embedding（article_id/product_code/.../image_cluster_id）→ deep → item embedding；图像簇 id 以离散特征注入。

**图 6：4th 的 Sampled Softmax**（topic 324094）——`../../intel/h-and-m-personalized-fashion-recommendations/bodies/324094_img/04.png`

*读图*：user×item 内积经 sampled softmax 训练——双塔嵌入兼作召回与排序特征。

## 7. 可迁移性评估

- **可直接迁移**：
  - "**召回 + 排序**"两阶段推荐框架（几乎所有推荐比赛通用）。
  - 热门度作为强基线，先量它，再决定是否上复杂召回。
  - 用户自身历史回填候选。
  - 先用时间切分验证，再确认 CV-LB 相关性后放心迭代。
- **需要前提**：
  - 大规模数据的处理能力（数百万级交互）。
  - 时尚/电商领域的季节性假设。
- **不建议照搬**：
  - 冷启动商品的复杂处理（本场证明收益接近零）。
  - 直接套用 itemCF（本场表现不如热门）。

## 8. 对新手的关键启示

1. **推荐系统的上限由召回决定**，把精力优先放在候选生成，而不是排序模型调参。
2. **简单基线（热门）往往强得惊人**——先量化它，再决定投入。
3. **"训练集要自己构造"是推荐类比赛的常见结构**，理解这一点比模型选择重要。
4. 20 分钟基线能排到 52/2952，说明**先跑通端到端流程**永远是第一步。

## 9. 出处

- 讨论区索引：`intel/h-and-m-personalized-fashion-recommendations/topics.md`（120 条）
- 已收录正文（8 节）：
  - Q&A（Paweł Jankiewicz，431 票）：https://www.kaggle.com/competitions/h-and-m-personalized-fashion-recommendations/discussion/307288
  - 1st（senkin13 & h4211819，430 票）：https://www.kaggle.com/competitions/h-and-m-personalized-fashion-recommendations/discussion/324070
  - 图像数据集（Sanskar Hasija，100 票）：https://www.kaggle.com/competitions/h-and-m-personalized-fashion-recommendations/discussion/306152
  - 3rd（sirius，96 票）：https://www.kaggle.com/competitions/h-and-m-personalized-fashion-recommendations/discussion/324129
  - 2nd（wht1996 & Paweł，80 票）：https://www.kaggle.com/competitions/h-and-m-personalized-fashion-recommendations/discussion/324197
  - 52nd 20 分钟方案（75 票）：https://www.kaggle.com/competitions/h-and-m-personalized-fashion-recommendations/discussion/324076
  - 6th（Ethan 队，71 票）：https://www.kaggle.com/competitions/h-and-m-personalized-fashion-recommendations/discussion/324075
  - 4th（Hongwei Zhang，65 票）：https://www.kaggle.com/competitions/h-and-m-personalized-fashion-recommendations/discussion/324094
- 未收录缺口（登记备查）：324098（5th）、324127（9th）、324084（11th）、324278（Giba）、324152（22nd 单 LGBM）、324486（top-10 汇总）等
- 深读全文：`analysis/deep/h-and-m-personalized-fashion-recommendations.md`
