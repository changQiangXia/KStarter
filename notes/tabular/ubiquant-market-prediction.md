# Ubiquant Market Prediction

> 主题：tabular ｜ 子类：— ｜ 领域：金融 ｜ 类别：Featured
> 截止：2022-07-19 ｜ 队伍数：2893 ｜ 机制：标准赛 ｜ 指标：Mean Pearson 相关系数
> 数据来源：`intel/ubiquant-market-prediction/`（120 条主题索引 + 8 节正文：1st/2nd/3rd/5th/7th/17th + Parquet 数据帖 + 匿名竞赛汇总；8th（338236）与两个汇总帖未收录）

## 1. 任务与数据

- **预测目标**：用 300 个匿名特征（f_0 … f_299）预测投资标的的未来收益，按时间序列评估。
- **数据形态**：典型"匿名特征"金融赛——特征含义不明，只能靠统计手段处理。
- **构造陷阱**：
  - **停牌/缺失**：中国股市存在停牌，样本缺失本身携带信息（17th 专门构造 `missing` 特征）。
  - 非平稳：市场环境变化会直接影响模型表现。
  - 时间序列权重：越近的时间步信息越重要。
- **赛制**：多轮更新（update1…final）——每轮在新增未来时段上重估；名次/分数跨轮不可比（2nd：34→12→4→2→2；5th：1344→16→24→11→13→5；3rd：900+→失败→7→7→4→3）。
- **评估期 regime**：2022-04—07 深证成指先急跌后反弹（1st 配图），"市场条件让模型笑了"是冠军的自我限定。

## 2. 验证方案

| 方案 | 使用者 | 说明 |
| --- | --- | --- |
| 时间序列划分（后期区间） | 17th | 只用第 850 个时间区间之后的数据，并对新样本加权 |
| **Purged K-Fold + embargo** | 2nd | 剔除与验证窗口重叠的样本，防前瞻泄漏 |
| PurgedGroupTimeSeries / TimeSeriesSplit | 1st | FE/调参用；训练用 KFold（限制轮数 + 早停） |
| 20 折 + purge 10 | 5th | 自定义训练 CV |
| last-k 验证（k=100/200/300） | 3rd | 滚动末段验证 |
| 与市场条件结合分析 | 1st | 明确承认"市场环境让模型笑了"（运气成分），并说明如何提高胜率 |

## 3. 方案谱系

| 方案 | 名次 | 关键点 |
| --- | --- | --- |
| LGBM×5 + TabNet×5；300+100 特征；最近 2.4M 行 | 1st | +100 time_id 均值特征：CV 0.141→0.154 / LB 0.141→0.149；第二提交（无 supplemental）仅 0.115796 |
| Purged K-Fold + 5 LGBM（CV 相关性早停）；405 特征 | 2nd | 100 列 time_id 均值（近 1000 个 time_id、>31 观测）+ 5 行级宏聚合 |
| 6 层 Transformer（3500 序列）+ PCC 损失 + 5 seeds | 3rd | 仅 300 特征；time_id 均值等系列尝试全失败 |
| 单 NN（4 层）+ QuantileTransformer；20 折 + purge 10 | 5th | 无 FE；目标 log + 去 127 离群行；名次 1344→5 |
| 单 LGB（extra_trees）+ 900+ 特征；不用 supplemental | 7th | 300 特征对照仅 0.112（掉出奖牌）；"多数人在公开榜过拟合" |
| 全特征 + 排列重要性删 24 个 + 停牌 missing + 时间加权 | 17th | missing：0.115486→0.117721；无它掉到 84 名；两段式 l2→l1 训练 |

## 4. 关键技巧

- **缺失即信息**：`missing`（上一时间步是否存在=停牌）单项 +0.0022 分 ≈ 67 个名次（17th）。
- **横截面归一化**：time_id 均值特征（1st +100 列：CV +0.013；2nd 的 100 列 + >31 观测门槛）+ 5 行级宏聚合（mean/std/q10/q50/q90）；17th 按 time_id 独立标准化目标。
- **Purged/Embargo 时间 CV**：5/6 家显式采用；金融序列赛第一工程。
- **时间衰减加权**（17th）与新时间步优先采样。
- **排列重要性**删 24 个特征（17th）；特征池 900+ vs 300 对照差 0.112→第 7（7th）。
- **内存-特征-数据三角**：1st 的 400 特征逼到 13GB RAM，只能取 2.4M 行；parquet 低内存版（3.5GB）是公共底座。
- **低信噪比实验纪律**：少调参（17th 借 G-Research 教训）、接受运气、提高期望（1st）。

## 5. 深读结论（2026-10 补）

- **本场是"验证与归一化"比赛**：模型（LGBM/NN/Transformer）差异 ≤ 名次带；purge 泄漏、time_id 归一化、停牌指示才是分差来源。
- **多轮 update 改变了证据结构**：单轮名次（1344/900+）几无参考价值；只有跨轮坚持稳健 CV 的模型能被"翻盘"（5th、3rd 的轨迹）。
- **time_id 均值特征存在模型家族张力**：GBDT 上明确有效（1st/2nd），Transformer 上 3rd 报告完全失败——跨模型照搬特征工程有风险。
- **"缺失即信息"给出最干净的单特征账**：+0.0022 分 = 17 名 vs 84 名。
- **补充数据 + 有限训练是隐形配方**：1st 的第一提交（用 supplemental、限制轮数）夺冠；第二提交（不用 + 无限训练）掉到银牌。

## 6. 图表证据

**图 1：评估期市场 regime（SZSE 深证成指）**（1st，topic 338220）——`../../intel/ubiquant-market-prediction/bodies/338220_img/01.png`

![szse](../../intel/ubiquant-market-prediction/bodies/338220_img/01.png)

*读图*：2022-04—07 先急跌（~11,700→~10,500）后反弹至 ~12,500；冠军用这张图说明"市场条件让模型笑了"——多轮评估下的 regime 暴露本身就是名次变量。

> `02.jpg` 为"300 勇士"梗图（对 300 特征的玩笑），按规范不内嵌。

## 7. 可迁移性评估

- **可直接迁移**：
  - **把缺失本身当作特征**（尤其在金融、医疗等有"缺席即事件"语义的领域）。
  - 时间衰减加权与按时间步标准化。
  - 排列重要性做特征筛选。
  - "承认运气、提高期望"的心态：在非平稳环境中控制风险敞口。
- **需要前提**：
  - 需要理解数据的领域语义（停牌、交易日历等）。
- **不建议照搬**：
  - 假设模型在样本外持续有效（本场冠军明确说市场环境变了模型就失效）。

## 8. 对新手的关键启示

1. **匿名特征比赛比的是数据工程**（缺失、时间、标准化），不是模型花活。
2. **一个小特征可能价值几十名**（本例的停牌指示）——领域理解 > 模型复杂度。
3. **金融赛要接受运气成分**，策略应是"提高期望"而不是"追求确定"。
4. **横向参考历届同类比赛**是最快的进阶路径。

## 9. 出处

- 讨论区索引：`intel/ubiquant-market-prediction/topics.md`（120 条）
- 已收录正文（8 节）：
  - Parquet 数据集（Rob Mulla，276 票）：https://www.kaggle.com/competitions/ubiquant-market-prediction/discussion/301724
  - 1st（yuuniee，198 票）：https://www.kaggle.com/competitions/ubiquant-market-prediction/discussion/338220
  - 3rd（hyd，69 票）：https://www.kaggle.com/competitions/ubiquant-market-prediction/discussion/338561
  - 匿名特征竞赛汇总（34 票）：https://www.kaggle.com/competitions/ubiquant-market-prediction/discussion/311546
  - 5th（Ricardo Colomer，33 票）：https://www.kaggle.com/competitions/ubiquant-market-prediction/discussion/338400
  - 2nd（Davide Stenner，28 票）：https://www.kaggle.com/competitions/ubiquant-market-prediction/discussion/338615
  - 7th（Wenrui Kong，24 票）：https://www.kaggle.com/competitions/ubiquant-market-prediction/discussion/338293
  - 17th（Kyle Peters，23 票）：https://www.kaggle.com/competitions/ubiquant-market-prediction/discussion/338239
- 未收录缺口（登记备查）：338236（8th）、301804（匿名竞赛汇总 81 票）、301699（往届冠军方案索引）
- 深读全文：`analysis/deep/ubiquant-market-prediction.md`
