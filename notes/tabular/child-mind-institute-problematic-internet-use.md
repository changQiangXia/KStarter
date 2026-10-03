# Child Mind Institute - Problematic Internet Use

> 主题：tabular（含时序信号）｜ 子类：— ｜ 领域：医疗 ｜ 类别：Featured
> 截止：2024-12-19 ｜ 队伍数：3559 ｜ 机制：代码赛 ｜ 指标：Cohen's Quadratic Weighted Kappa
> 数据来源：`intel/child-mind-institute-problematic-internet-use/`（120 条主题索引 + 8 篇 write-up 正文）

## 1. 任务与数据

- **预测目标**：由儿童的身体活动数据（手表加速度时序）+ 健康问卷，预测"问题性网络使用"的严重程度等级，指标是 QWK。
- **数据形态**：小样本（数千人）+ 高噪声时序信号 + 大量缺失；标签本身由问卷分数离散化得到。
- **构造陷阱**：数据噪声极大、样本量小 → **排行榜方差很高**，名次受随机性影响显著（冠军标题即"我如何中了彩票"）。

## 2. 验证方案

| 方案 | 使用者 | 说明 |
| --- | --- | --- |
| 分层 K 折（按目标等级） | 多数 | QWK 需要等级分布稳定 |
| 稳健性优先 | 1st | 复出后把重点放在"提高稳健性"而非刷分 |
| 多提交选择 | 1st | 承认"选对了提交"是运气的一部分 |

## 3. 方案谱系

| 方案 | 名次 | 关键点 |
| --- | --- | --- |
| 投票式集成（LGBM + 2×XGB + CatBoost + ExtraTrees） | 1st | **改用 `PCIAT-PCIAT_Total` 原始分数做目标再转换为等级**；强调稳健性；自述运气成分大 |
| 时序聚类特征（KMeans 提取活动模式） | 5th | 取 6 个方差最大的 parquet，聚 15 类，按用户在各簇上的均值构造 15 维特征 |
| 多模型集成 | 19th | 作者坦率讨论高方差比赛中的心态与策略 |

## 4. 关键技巧

- **目标工程**：用连续的原始问卷分数替代粗粒度标签，再在评估时离散化——保存了更多信息。
- **时序 → 聚类特征**：用 KMeans 把长时序压缩成可解释的活动模式特征。
- **模型多样但结构简单**：树模型投票集成，不做复杂网络。
- **稳健优先**：在高方差比赛中，选择"不会崩"的提交比追求理论最优更重要。
- **承认方差**：冠军明确说运气（选对提交）占很大比重。

## 5. 可迁移性评估

- **可直接迁移**：
  - **用更细粒度的原始标签做目标再离散化**（序数指标的通用技巧）。
  - 时序聚类特征（把长序列压成可解释模式）。
  - 高方差比赛中以稳健性为第一优先。
- **需要前提**：
  - 需要原始连续标签可得（很多比赛只给离散标签）。
- **不建议照搬**：
  - 把高方差比赛的结果当作能力指标（19th 的自省值得一读）。

## 6. 对新手的关键启示

1. **小样本 + 高噪声 = 高方差**：这类比赛的名次波动大，别把它当能力标尺。
2. **标签工程能做就做**：细粒度目标往往直接带来提升。
3. **时序特征聚类**是成本低、可解释性好的降维手段。
4. **稳健的提交策略**本身就是技术。

## 7. 出处

- 讨论区索引：`intel/child-mind-institute-problematic-internet-use/topics.md`（120 条）
- 已收录 write-up（8 篇）：
  - 1st "Or How I Won the Lottery"（94 票）：https://www.kaggle.com/competitions/child-mind-institute-problematic-internet-use/discussion/552638
  - 5th（14 票）：https://www.kaggle.com/competitions/child-mind-institute-problematic-internet-use/discussion/552656
  - 16th（42 票）：https://www.kaggle.com/competitions/child-mind-institute-problematic-internet-use/discussion/552569
  - 19th（25 票）：https://www.kaggle.com/competitions/child-mind-institute-problematic-internet-use/discussion/552513
  - 私榜 7（31 票）：https://www.kaggle.com/competitions/child-mind-institute-problematic-internet-use/discussion/552625
  - 数据问题与 EDA（63 / 73 票）：https://www.kaggle.com/competitions/child-mind-institute-problematic-internet-use/discussion/535354 ｜ 538235
