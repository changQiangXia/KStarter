# Tabular Playground Series Mar 2022（交通拥堵时空预测）轻量深读（Tier B）

> 赛事：Playground ｜ 主题 tabular（时空预测，MAE）｜ 956 队 ｜ 标准赛 ｜ 指标：Mean Absolute Error
> 材料基础：`digests/tabular-playground-series-mar-2022.md`（6 篇正文：1st 316271 / 中位数基线 310642 / 3rd 317661 / Spark 方案 313882 / 新手汇编 312463 / 可视化提问 311480；80 条主题索引）+ 0 张归档图
> 轻读时间：2026-10（Tier B B16）

## 1. 一句话重述与数字账

预测某周一午后的交通拥堵（时空数据，MAE）。本场最著名的教训来自"**能多简单就多简单**"帖：**不做任何 ML，只按"时间 × 地点"取历史中位数，LB 就有 4.967**——作者试过的 RF/ExtraTrees/Huber 全部打不过它；错误在于把表格的每一行当独立样本，而时间序列必须用"其他行"（比如用早晨流量预测下午）。1st 的单 LGBM 赢在**时空似然编码 + 滞后特征 + Optuna 选特征与训练子集**，且自认有运气成分（私榜大洗牌，前 20 名普遍跳 300+ 位）。

| 关键数字 | 值 | 来源 |
| --- | --- | --- |
| 朴素基线（310642） | 按（时间 × 地点）历史中位数直接提交 → **LB 4.967**；RF/ExtraTrees/Huber 全不如它；改进方向 = 用早晨流量预测下午偏离 | 310642 |
| 1st（316271） | **单 LGBM、无后处理**（时间不够）；特征：似然编码（用 hour-minute × 地点交叉的最小/最大/中位/方差/均值）+ 滞后特征（对每个 x-y 方向组合在 day/weekday 上取均值/方差/中位/最小/最大与 1 区间位移，3/5/10 天滚动 + 扩展窗口）；**Optuna 做特征选择**（每个特征 True/False，300 次 trial）并同时搜"是否只用 day 0 训练、是否只保留与测试同 hour-minute 的训练行"；验证 = 测试前一周、对齐同 day/hour-minute；失败：宽神经网络 | 316271 |
| 3rd（317661） | 明文"这是时间序列问题"：TimeSeriesSplit；时间特征（weekday、isMonday、hour、minute）；**滞后目标 7/14 天**；fastai tabular（8 epoch、lr 0.005677、layers [1066,931]、batch 256）；自述私榜跳 300+ 位，前 20 名都类似 → 运气成分大 | 317661 |
| 其他方案 | Spark/Scala：weekday/hour 拆分 + one-hot + RF + 交叉验证器，MAE 5.320（约 66 分位）；新手汇编（31 票）收录无代码均值基线、GroupTimeSeriesSplit、Temporal Fusion Transformer、SARIMA 等 | 313882 / 312463 |
| 社区 | 公私榜大幅位移（6 票）；"四月一日洗牌？"（4 票）；"为什么中位数有效"（6 票）；"用中位数做 fold 集成"（5 票，来自 cdeotte 思路）；日期特征抽取（34 票）；循环特征文章（20 票）；时空预测资源（36 票） | 索引 |

## 2. 逐方案对照矩阵

| 维度 | 中位数基线 | 1st | 3rd | Spark |
| --- | --- | --- | --- | --- |
| 模型 | 无（历史中位） | 单 LGBM | fastai tabular | Spark RF |
| 时空特征 | 时间×地点中位 | 似然编码 + 多窗口滞后 | 时间特征 + 7/14 天滞后 | weekday/hour one-hot |
| 训练子集 | 全部 | Optuna 搜"day 0 / 同时刻" | 全部 | 全部 |
| 验证 | — | 测试前一周对齐 | TimeSeriesSplit | 10% 留出 |
| 结果 | LB 4.967 | 1st | 3rd（+300 位） | 5.320 |

## 3. 共识、分歧与裁决

### 共识一：本场是时空预测，朴素中位数基线极强（310642、312463；置信度高）

不建模即 4.967；很多 ML 方案打不过它。**裁决**：时空任务先跑"按时间×地点聚合"的基线，再决定建模投入。置信度：高。

### 共识二：有效特征是"空间模式 + 同日/周模式 + 早晚耦合"（1st、3rd；置信度中高）

1st 的似然编码与多窗口滞后、3rd 的 7/14 天滞后都围绕这三类结构。**裁决**：先做时间对齐的滞后与分组统计，再谈模型。置信度：中高。

### 事件：Optuna 同时做特征选择与训练子集选择（1st；置信度中）

300 次 trial 的 True/False 特征开关 + "是否只用 day 0 / 是否只留同时刻"的搜索。**裁决**：把"训练数据切片"也当作超参搜索，是时间序列特征选择的一个实用扩展。置信度：中。

### 事件：私榜大幅洗牌与运气（1st、3rd、316245、316297；置信度中高）

3rd 强调前 20 名普遍跳 300+ 位，1st 自认中彩票；社区有"April Fools' Shakeup"的玩笑帖。**裁决**：时间序列赛的最终名次方差巨大，需以稳健验证与多份提交控制风险。置信度：中高。

### 技巧：用中位数做 fold 集成（313420；置信度中）

引用 cdeotte 的"fold 集成取中位数"在本场比均值更稳。**裁决**：MAE 场景下用中位数聚合折预测。置信度：中。

## 4. 证据分级

| 断言 | 等级 | 说明 |
| --- | --- | --- |
| 中位数基线 4.967 | 自述 + notebook | 高 |
| 1st 的似然编码/滞后/Optuna 细节 | 自述（含代码链接） | 中高 |
| 3rd 的 fastai 配置与 +300 位 | 自述 | 中 |
| Spark 方案 | 自述（含 GitHub） | 中 |
| 洗牌幅度 | 多帖互证 | 中高 |

## 5. 悬案与缺口（登记）

- 2nd、4th–10th 方案未收录；
- 1st 的似然编码未用 K 折防泄漏（作者自承）；
- "早晨预测下午"的量化增益未给出；
- **图证缺口**：本场归档 0 图。

## 6. 图表证据

无可用图证（本场归档 0 图，图证缺口已登记）。

## 7. 出处

- 1st Disbelief（38 票 / 16 评论）：https://www.kaggle.com/competitions/tabular-playground-series-mar-2022/discussion/316271
- 中位数基线（68 票 / 24 评论）：https://www.kaggle.com/competitions/tabular-playground-series-mar-2022/discussion/310642
- 3rd（6 票 / 1 评论）：https://www.kaggle.com/competitions/tabular-playground-series-mar-2022/discussion/317661
- Spark/Scala 方案（4 票）：https://www.kaggle.com/competitions/tabular-playground-series-mar-2022/discussion/313882
- 新手汇编（31 票 / 16 评论）：https://www.kaggle.com/competitions/tabular-playground-series-mar-2022/discussion/312463
- 时间序列资源（36 票 / 10 评论）：https://www.kaggle.com/competitions/tabular-playground-series-mar-2022/discussion/311012
- 日期特征抽取（34 票 / 18 评论）：https://www.kaggle.com/competitions/tabular-playground-series-mar-2022/discussion/310377
- 中位数 fold 集成（5 票 / 0 评论）：https://www.kaggle.com/competitions/tabular-playground-series-mar-2022/discussion/313420
- 公私榜大幅位移（6 票 / 1 评论）：https://www.kaggle.com/competitions/tabular-playground-series-mar-2022/discussion/316245
