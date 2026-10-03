# H&M Personalized Fashion Recommendations

> 主题：tabular ｜ 子类：recsys ｜ 领域：电商推荐 ｜ 类别：Featured
> 截止：2022-05-09 ｜ 队伍数：2952 ｜ 机制：标准赛 ｜ 指标：MAP@12
> 数据来源：`intel/h-and-m-personalized-fashion-recommendations/`（120 条主题索引 + 8 篇 write-up 正文）

## 1. 任务与数据

- **预测目标**：为每位顾客推荐 12 件商品，按 MAP@12 评分（排序质量）。
- **数据形态**：交易记录（顾客 × 商品 × 时间）、商品元数据、图像；**数据量巨大但信息稀疏**（多数顾客历史极短）。
- **题目特点**：1st place 明确指出 "**训练集与测试集要自己构造**"——候选生成策略是突破精度上限的关键。

## 2. 验证方案

| 方案 | 使用者 | 说明 |
| --- | --- | --- |
| 时间切分（用最后一周做验证） | 多队 | 与线上预测窗口对齐 |
| 反馈式验证 | 1st | 强调本场 **CV 与 LB 相关性稳定**，可放心用 CV 迭代 |
| 只保留有历史行为的用户评估 | 多队 | 冷启动用户几乎无法进 top12，需单独说明 |

## 3. 方案谱系

| 方案 | 名次 | 关键点 |
| --- | --- | --- |
| 多种召回策略 + 特征工程 + GBDT 排序 | 1st | 用"近期热门商品"做主召回（时尚季节性强）；冷启动商品因缺少交互信息永远排不进前 12 |
| 热门召回 + LGBM 排序（两阶段 LGBM） | 2nd | 召回阶段**每用户取约 600 个最热门商品**（itemCF 反而更差）+ 简单历史策略；排序阶段再训一个特征更复杂的 LGBM |
| 召回 + 排序的标准流水线 | 3rd | 强调"有区分度的召回特征"（如该商品是否被该用户历史覆盖） |
| 20 分钟 notebook 方案 | 52nd | 极简基线也能进前 2%（说明基线强度） |

## 4. 关键技巧

- **候选生成（召回）决定上限**：排序模型再好，候选里没有正确商品就无法得分。
- **热门商品是强基线**：2nd 明确记录"itemCF 不如直接选热门"——时尚领域的热门信号非常强。
- **历史购买回填**：把用户历史上买过的商品直接加入候选（2nd、3rd 都做）。
- **时间与季节性特征**：按周/月聚合的交互统计是核心特征。
- **冷启动的诚实处理**：缺交互信息的商品无法排名，不必强行优化。

## 5. 可迁移性评估

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

## 6. 对新手的关键启示

1. **推荐系统的上限由召回决定**，把精力优先放在候选生成，而不是排序模型调参。
2. **简单基线（热门）往往强得惊人**——先量化它，再决定投入。
3. **"训练集要自己构造"是推荐类比赛的常见结构**，理解这一点比模型选择重要。
4. 20 分钟基线能排到 52/2952，说明**先跑通端到端流程**永远是第一步。

## 7. 出处

- 讨论区索引：`intel/h-and-m-personalized-fashion-recommendations/topics.md`（120 条）
- 已收录 write-up（8 篇）：
  - 1st（430 票）：https://www.kaggle.com/competitions/h-and-m-personalized-fashion-recommendations/discussion/324070
  - 2nd（80 票）：https://www.kaggle.com/competitions/h-and-m-personalized-fashion-recommendations/discussion/324197
  - 3rd（96 票）：https://www.kaggle.com/competitions/h-and-m-personalized-fashion-recommendations/discussion/324129
  - 6th（71 票）：https://www.kaggle.com/competitions/h-and-m-personalized-fashion-recommendations/discussion/324075
  - 52nd 极简基线（75 票）：https://www.kaggle.com/competitions/h-and-m-personalized-fashion-recommendations/discussion/324076
