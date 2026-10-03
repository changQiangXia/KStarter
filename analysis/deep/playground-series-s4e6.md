# Playground Series S4E6 轻量深读（Tier B）

> 赛事：Playground ｜ 主题 tabular（学生升学三分类，教育）｜ 2684 队 ｜ 标准赛 ｜ 指标：Accuracy ｜ 同期含 AutoML Grand Prix
> 材料基础：`digests/playground-series-s4e6.md`（6 篇正文：AGP 1st 509631 / Pt.2 509642 / ravi20076 509665 / 6th 515989 / 集成多样性 512220 / 两个最重要特征 509073；80 条主题索引）+ 5 张图
> 轻读时间：2026-10（Tier B B05）

## 1. 一句话重述与数字账

学生状态三分类（dropout/enrolled/graduate），合成数据 + 原数据。真正的考点是**在"Accuracy + 合成数据"带来的巨大榜面噪声下怎么做决策**：本场同时出现"单模/小集成足够好"与"公榜彩票模型值得 0.86 权重"两种相反证据。

| 关键数字 | 值 | 来源 |
| --- | --- | --- |
| AGP 1st（509631，32 票） | 公开 notebook（gauravduttakiit）在公榜异常强、离线无法解释 → 视为"彩票"；最终**加权集成 0.14（自研）+ 0.86（彩票模型）**；自研部分用 AutoGluon 3 小时：**log-loss 当早停指标、accuracy 仍作选择指标**（ROC AUC 版无提升）；离线结论：序数特征当数值更好、用原始数据更好、样本权重无用 | 509631 |
| Pt.2 写手（509642，36 票，carl） | 离线特征工程"全部徒劳"；删弱特征反而掉分（假设：合成噪声本身携带微弱预测色）；类别列处理方式影响诡异；用众数混合公开输出 + CatBoost/LGBM → 0.83875；**仅把 seed 42→24、CatBoost 树数 1000→1001，公榜从 0.83875 掉到 0.83679** → 断言"运气成分很大" | 509642 |
| ravi20076（509665，32 票） | 24 小时赛的一天分成 4 段实验 + 1 次留底；baseline 0.83758（8 小时，公榜第 2）→ 调参无公榜变化（14 小时）→ 融合公开 kernel 得 0.83924（21 小时，第 8）→ 继续 blending 无提升 | 509665 |
| 6th（515989，55 票） | 方案极简：5 折 StratifiedKFold + 原数据 + XGB/LGBM 集成 + Optuna；核心结论"**多模型集成有害**"：单模型/极小集成表现极好；例证=一位新选手**只提交一次即拿到第 2**；灵感来自 rzatemizel 的 RFECV 选模 notebook | 515989 |
| 集成多样性（512220，70 票，Tilii） | 三分类无单列概率可比 → 把三列压成"置信度"（均匀猜测=0、确定性预测=1），对错误 OOF 取负号，再用相关/KS/散点比较模型多样性；发现 LGB vs CatBoost 比 LGB vs AutoGluon 堆叠更"多样"，并论证 SVC 作为多样性来源（GPU/RAPIDS 下不算慢） | 512220 |
| 特征洞察（509073，61 票） | 浅层决策树直接给出规则：`Curricular units 2nd sem (approved) ≥5 → graduate`；`≤1 → dropout`；中间看 `Tuition fees up to date`（交清→enrolled，否则 dropout） | 509073 |

## 2. 逐方案对照矩阵

| 维度 | AGP 1st | Pt.2（carl） | ravi20076 | 6th |
| --- | --- | --- | --- | --- |
| 形态 | 0.14 自研 + 0.86 公开彩票模型 | 公开输出 + CatBoost/LGBM 众数 | 分段实验 + 融合公开 kernel | XGB+LGBM 小集成 |
| CV 使用 | AutoGluon 离线评估配置 | 离线全失败 → 靠公榜 | 竞赛数据做 CV | 5 折 |
| 关键判断 | 承认离线解释不了 → 直接借力 | 合成噪声携带弱信号、别删弱特征 | 时间盒 + 留底提交 | **集成越多越差** |
| 结果 | AGP 1st | 0.83875→0.83679（换 seed 就掉） | 0.83924（当日第 8） | 6th |

## 3. 共识、分歧与裁决

### 共识一：本场榜面噪声极高，"Accuracy + 合成数据"是放大器（1st/carl/6th）

1st 找不到任何离线证据解释公开 notebook 的强（"彩票"）；carl 换 seed 掉 0.002；6th 观察到"新选手一次提交得第 2"；另有帖子"公榜 333 → 私榜 61"。**裁决**：该指标下公榜差异多为噪声；要么像 1st 那样承认不可解释并借力，要么像 6th 那样守 CV 做小集成——关键是**知道自己选的是哪条路线**。置信度：高（多条独立证据）。

### 共识二：特征工程在本场基本无效（carl/1st/509073）

carl 的交叉项全部无效、删弱特征掉分；1st 的有效离线动作只有"序数当数值、加原数据"；509073 的浅树显示信号集中在 2–3 个列。**裁决**：合成数据 + 小信号场景里，FE 的边际远低于"数据来源选择（原数据）+ 类别/序数编码"。置信度：中高。

### 分歧一：集成越大越好还是越小越好

AGP 1st 用加权融合（含 0.86 权重的单一模型）；6th 明确"多模型集成有害"，主张单模/小集成；ravi20076 的 blending 也未提升。**裁决**：在噪声主导的榜面上，集成放大的往往是噪声；**只有当成员多样性有明确依据（如 512220 的置信度散点）时才值得融合**。置信度：中高。

### 分歧二：要不要用原始数据

1st 离线验证"用原始数据更好（尽管有分布漂移）"；ravi20076 早期也发现加原数据有帮助；carl 未强调。**裁决**：合成赛优先做"加/不加原数据"的单变量对照。置信度：中高。

### 事件：集成多样性的度量（512220）

Tilii 把三分类概率压成带符号置信度后用相关/KS/散点判断成员互补性，并指出"LGB 与 SVC 的互补性 > LGB 与 AutoGluon 堆叠"。**裁决**：多分类集成的成员筛选需要自定义多样性度量，不能只看单列概率相关。置信度：中（方法自洽，收益未量化）。

## 4. 证据分级

| 断言 | 等级 | 说明 |
| --- | --- | --- |
| AGP 1st 的 0.14/0.86 权重与 AutoGluon 配置 | 自述 + GitHub 汇总 | 中高 |
| carl 的 seed 敏感实验（0.83875→0.83679） | 自述（单次对照） | 中 |
| 6th 的"单模/小集成更好" | 自述 + 社区案例（新选手第 2） | 中高 |
| 512220 的置信度多样性方法 | 自述 + 4 张散点图 | 中 |
| 509073 的两特征规则 | 决策树图 + 众队共识 | 高 |

## 5. 悬案与缺口（登记）

- "3rd place solution: a single xgb model"（515983，30 票）与"Outlier detection to boost the score"（511076，34 票）未入库/未细读；
- 公开彩票 notebook 为何在公榜强始终未解释（1st 明说不可复现）；
- "公榜 333 → 私榜 61"（515976）的成因未细读；
- 归档 5 图：1 张决策树（509073）+ 4 张置信度散点（512220）。

## 6. 图表证据

![浅层决策树给出的主规则](../../intel/playground-series-s4e6/bodies/509073_img/01.png)

**图 1**（topic 509073）：深度 3 的决策树——`Curricular units 2nd sem (approved)` 一列就把样本切成 graduate（≥5.5）与 dropout（≤1.5）两翼，中间仅由 `Tuition fees up to date` 区分 enrolled/dropout。这是"本场信号集中在极少列"的直接证据。

## 7. 出处

- AGP 1st（32 票）：https://www.kaggle.com/competitions/playground-series-s4e6/discussion/509631
- Pt.2 写手（36 票）：https://www.kaggle.com/competitions/playground-series-s4e6/discussion/509642
- ravi20076（32 票）：https://www.kaggle.com/competitions/playground-series-s4e6/discussion/509665
- 6th（55 票）：https://www.kaggle.com/competitions/playground-series-s4e6/discussion/515989
- 集成多样性（70 票）：https://www.kaggle.com/competitions/playground-series-s4e6/discussion/512220
- 两个最重要特征（61 票）：https://www.kaggle.com/competitions/playground-series-s4e6/discussion/509073
- 3rd 单 XGB（30 票）：https://www.kaggle.com/competitions/playground-series-s4e6/discussion/515983
