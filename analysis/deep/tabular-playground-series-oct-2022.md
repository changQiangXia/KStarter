# Tabular Playground Series Oct 2022（火箭联盟状态预测）轻量深读（Tier B）

> 赛事：Playground ｜ 主题 tabular（游戏状态三分类，流式/在线学习设置）｜ 463 队 ｜ 标准赛 ｜ 指标：Mean Columnwise Log Loss
> 材料基础：`digests/tabular-playground-series-oct-2022.md`（6 篇正文：主办方方案 364908 / "5 分钟冠军" 363288 / 在线学习入门 356584 / dtype 压缩 356540 / LogLoss 往届方案 361308 / 107th 363585；80 条主题索引）+ 2 张归档图
> 轻读时间：2026-10（Tier B B15）

## 1. 一句话重述与数字账

从火箭联盟的比赛状态快照（6 名球员 + 球的位置/速度/加速）预测"未来 Y 秒内 A 队得分 / B 队得分 / 无人得分"（多列 Log Loss），赛制带在线学习色彩（逐帧预测/概念漂移）。本场最完整的技术材料来自**主办方的基线方案**：用"网络中的网络"处理球员对（队友对 + 对手对）的对称结构，并利用 **144 种等价表示**（X/Y 翻转 × 两队各 3! 排列）做训练增强与**测试时置换平均**——后者被作者称为"提升之大令人惊讶"。榜首"Sergey & Sam"（93 次提交、公榜 0.18105）因被平台误判删除，留下了"5 分钟冠军"的治理事件。

| 关键数字 | 值 | 来源 |
| --- | --- | --- |
| 主办方方案（364908） | 私榜 0.17759；思路来自 The Zoo 的 NFL Big Data Bowl 2020"网络中的网络"；输入 = 球 6 维 + 2×3 球员 ×8 维（pos/vel xyz、boost、demoed）；demoed 的 NaN → 加 `p#_demoed` 标志并替换为"球场上空、向上飞、0 boost"的 OOD 状态；结构：球特征 → 与球员/队伍/球-球员差值拼接 → 球员级 conv+pool → **队友对**与**对手对**各做 conv+pool → 再次球员级 conv+pool → dense → 每列一个 softmax（SparseCategoricalCrossentropy）；**144 种对称变换**用于训练增强 + 测试时平均；多时间窗辅助目标（Y=1..10，主目标 Y=10 加权） | 364908 |
| "5 分钟冠军"（363288） | 自称训练 **100+ 模型 + 集成 + 最后一小时选提交**，一度登顶（公榜 0.18105）后被 Kaggle 以作弊为由移除；作者公开申诉，并展示 Neptune.ai 的实验日志（KAG-48…58，loss ~0.035、batch 4096、LR 0.00098、22 epochs）作为"认真参赛"的证据 | 363288 |
| 在线学习入门（356584） | 70 票资源帖：在线学习 = 数据流式到达、逐步预测、应对概念漂移；介绍 creme/river/FTRL、应用场景（天气/金融）与生产风险（漂移导致退化、可扩展性问题） | 356584 |
| 工程优化（356540） | dtype 下采样 + parquet：整体内存 **10,027MB → 3,154MB（-68.55%）**，单步 -73.98%；给出 `reduce_mem_usage` 与预生成 dtype 字典的用法 | 356540 |
| 社区 | "如何避免过拟合的验证"（33 票 / 13 评论）；"数据表示与特征工程"（32 票 / 8 评论）；"一些想法"（29 票 / 13 评论）；"球员位置 NaN"（24 票 / 11 评论）；"球场的一个重要细节"（20 票 / 9 评论）；NN 激活函数对比（20 票 / 3 评论） | 索引 |

## 2. 逐方案对照矩阵

| 维度 | 主办方基线 | 榜首（5 分钟冠军） | 常见社区线 |
| --- | --- | --- | --- |
| 表示 | 2×3 球员 + 球；demoed 标志 + OOD 占位 | 未公开（100+ 模型集成） | 手工 FE / 逐帧特征 |
| 结构 | 球员对网络 + 池化（NIN） | 未公开 | MLP/GBDT |
| 对称性 | **144 变换：训练增强 + 测试平均** | 未公开 | 部分采用 |
| 目标 | 多时间窗辅助 + 主目标 | 未公开 | 单目标为主 |
| 工程 | — | Neptune 日志（93 次提交） | dtype 压缩 69% |

## 3. 共识、分歧与裁决

### 共识一：对称/置换结构是本场最大的方法学要点（364908、社区；置信度中高）

144 种等价表示（翻转 × 队内排列）既做训练增强，也做测试时平均；作者明确说测试时置换平均带来"惊讶的提升"。**裁决**：输入存在对称群时，先把它显式建模/平均掉，比调参更划算。置信度：中高。

### 共识二：球员对（队友/对手）建模 + 池化是处理小队状态的合适结构（364908；置信度中）

主办方直接沿用橄榄球（NFL Big Data Bowl）的"pair + pooling"网络。**裁决**：多智能体状态预测可把"对关系"作为一等结构。置信度：中（单方案，但来源有先例）。

### 事件一：NaN/demoed 与"球场细节"是数据侧的主要坑（364908、356545、356789；置信度中）

被击毁玩家的 NaN 需要用标志 + 占位状态处理；球员位置缺失与球场坐标细节都有专门讨论。**裁决**：状态被移除的实体要显式编码，否则模型会把缺失当真实位置。置信度：中。

### 事件二：平台误判与治理风险（363288、356530；置信度中）

榜首团队被以作弊为由移除（作者申诉并公开实验日志）；赛事欢迎帖与验证讨论也强调"别过拟合"与该赛的特殊性。**裁决**：高提交数 + 强集成的团队要留好实验日志/复现材料以应对审查。置信度：中。

### 共识三：流式赛要先解决内存/速度工程（356540；置信度中高）

10GB 级数据通过 dtype 下采样 + parquet 压到 3.15GB。**裁决**：在线学习/逐帧预测场景中，工程效率是可行性的前提。置信度：中高。

## 4. 证据分级

| 断言 | 等级 | 说明 |
| --- | --- | --- |
| 主办方的网络结构与 144 变换 | 自述 + notebook 链接（代码完整） | 高 |
| "5 分钟冠军"的事件与实验日志 | 自述 + 截图 | 中 |
| 在线学习资源 | 汇总帖 | 中 |
| dtype 压缩数字 | 可复现代码 + 输出 | 中高 |
| 社区坑位讨论 | 多帖 | 中 |

## 5. 悬案与缺口（登记）

- 榜首团队的完整方案未公开（其被移除后也未发布技术细节）；
- 官方对"作弊"判定的说明未收录；
- 多时间窗辅助目标的量化增益未给出；
- **图证缺口**：无（2 张图，本深读内嵌 2 张）。

## 6. 图表证据

![榜首榜单一度第一](../../intel/tabular-playground-series-oct-2022/bodies/363288_img/01.jpg)

**图 1**（topic 363288）：公榜截图——Sergey & Sam 以 0.18105 列第 1（93 次提交），随后遭移除。

![Neptune 实验日志](../../intel/tabular-playground-series-oct-2022/bodies/363288_img/02.png)

**图 2**（topic 363288）：作者的 Neptune.ai 实验日志（KAG-48…58，loss ~0.035、batch 4096、LR 0.00098、22 epochs）——被指控作弊时的自证材料。

## 7. 出处

- 主办方方案（19 票 / 10 评论）：https://www.kaggle.com/competitions/tabular-playground-series-oct-2022/discussion/364908
- "5 分钟冠军"事件（19 票 / 12 评论）：https://www.kaggle.com/competitions/tabular-playground-series-oct-2022/discussion/363288
- 在线学习入门（70 票 / 33 评论）：https://www.kaggle.com/competitions/tabular-playground-series-oct-2022/discussion/356584
- dtype 压缩（40 票 / 20 评论）：https://www.kaggle.com/competitions/tabular-playground-series-oct-2022/discussion/356540
- 欢迎帖（33 票 / 15 评论）：https://www.kaggle.com/competitions/tabular-playground-series-oct-2022/discussion/356530
- 如何避免过拟合的验证（33 票 / 13 评论）：https://www.kaggle.com/competitions/tabular-playground-series-oct-2022/discussion/359714
- 数据表示与特征工程（32 票 / 8 评论）：https://www.kaggle.com/competitions/tabular-playground-series-oct-2022/discussion/356718
- 球员位置 NaN（24 票 / 11 评论）：https://www.kaggle.com/competitions/tabular-playground-series-oct-2022/discussion/356545
- 往届 LogLoss 方案（7 票）：https://www.kaggle.com/competitions/tabular-playground-series-oct-2022/discussion/361308
