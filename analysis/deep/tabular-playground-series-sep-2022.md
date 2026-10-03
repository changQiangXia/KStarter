# Tabular Playground Series Sep 2022（图书销量预测）轻量深读（Tier B）

> 赛事：Playground ｜ 主题 tabular（时间序列回归，SMAPE）｜ 1381 队 ｜ 标准赛 ｜ 指标：SMAPE
> 材料基础：`digests/tabular-playground-series-sep-2022.md`（6 篇正文：1st 388206 / 2nd 356746 / 3rd 356643 / FE 351098 / 视频教程 349557 / Jan 2022 冠军 notebook 349435；80 条主题索引）+ 0 张归档图
> 轻读时间：2026-10（Tier B B14）

## 1. 一句话重述与数字账

预测 2021 年多国图书销量（SMAPE），训练期覆盖 COVID。本场是"**线性/GAM + 强外生特征**"的胜利：3rd 用**一个 GAM**（无技巧、无集成）拿第 3，并推测 4th–7th 都是 GAM 变体；2nd 把 5 份公开 notebook + 2 份自研做 **Boltzmann 集成**（直接复用 TPS Jan 2022 的 40th 方案）；1st 的方法论是"**逐列影响归因 + 反推去除 + 误差公共点**"，并特别处理 2020 年 3–5 月的 COVID 影响（指数衰减/恢复项）。

| 关键数字 | 值 | 来源 |
| --- | --- | --- |
| 1st（388206） | 工作流：①检查每列分布（如把 date 转 day-of-week）；②估计影响并验证；③若估计大致正确则"反推去除"该影响，继续找更大的影响；④按影响调整列；⑤找出预测误差大的样本的公共点，加入特征再训；用图分析确认 2020 年 3–5 月误差来自 COVID，并用**指数型衰减/恢复项**建模 | 388206 |
| 2nd（356746） | **Boltzmann Ensemble**：5 份最佳公开 notebook + 2 份自研高分 notebook 按 `exp(b(S−x))` 加权（来源 = TPS Jan 2022 的 40th 方案）；公开来源含 Ridge/Lasso/Elastic、线性回归、GAM、遗传规划等 | 356746 |
| 3rd（356643） | 单个 **GAM**（paddykb 风格）；无技巧无集成；CV = "留出 3 个月块"；最终只改了一处：把"圣诞→新年"的过渡也用样条捕捉；自述"最后一周在度假、没动手改，是运气" | 356643 |
| FE 合集（351098） | GDP 2017–2021、教育指数、消费者信心指数、商业信心指数、各国封锁日期、节假日；另见"比率至上"（34 票）、"按产品占用呈周期"（28 票）、分层时序方法（34 票） | 351098 等 |
| 方法与资源 | 时序 CV 完整指南（38 票 / 17 评论）；Rob Mulla 两集视频教程（62 票 / 20 评论）；SMAPE 的承诺与陷阱（30 票）；"同样数据、更多科学"的呼吁（22 票 / 7 评论）；TPS Jan 2022 冠军 notebook 公开（ambrosm 的高级线性模型 + CCI） | 索引 |

## 2. 逐方案对照矩阵

| 维度 | 1st | 2nd | 3rd |
| --- | --- | --- | --- |
| 模型 | 残差归因 + 指数项调整 | Boltzmann 集成（公开+自研） | 单 GAM |
| 外生特征 | 逐列归因后发现/调整 | 跟随公开 notebook | 节假日样条 |
| CV | 误差公共点分析 | 公开 notebook 的 CV | 留 3 个月块 |
| 集成 | — | exp(b(S−x)) 加权 | 无 |
| 启示 | 把误差当线索 | 系列赛资产复用 | 简单模型也能进前三 |

## 3. 共识、分歧与裁决

### 共识一：本场属于"线性/GAM + 外生变量"，复杂 GBDT 无优势（3rd、2nd、FE 帖；置信度中高）

3rd 的单 GAM 拿第 3 并猜测 4–7 名同为 GAM 变体；2nd 的 Boltzmann 集成的成分也以线性/GAM 为主。**裁决**：强季节 + 外生驱动的小数据时序，"可解释的加性/线性结构"优于树模型。置信度：中高。

### 共识二：外生指标与日历/事件特征决定上限（FE 帖、1st；置信度中高）

GDP、教育指数、消费者/商业信心、封锁日期、节假日被反复验证；1st 用 COVID 指数项。**裁决**：先补外部宏观/事件数据，再做模型。置信度：中高。

### 事件一：误差归因式迭代（1st；置信度中）

1st 的方法论是"反推去除已知影响 → 找新影响 → 误差公共点 → 加特征"，与前面 S3E20 的残差驱动思路同源。**裁决**：把残差当作待解释结构，是时序特征工程的有效框架。置信度：中。

### 事件二：系列赛资产复用（2nd、349435；置信度中高）

2nd 直接复用 TPS Jan 2022 的 Boltzmann 方案；社区公开 Jan 2022 冠军 notebook 作为起点。**裁决**：TPS 系列的历史方案是首选起手式（与 S3E26 的"两年前冠军 + 伪标签"一致）。置信度：中高。

### 事件：SMAPE 的陷阱（349553、349941；置信度中）

"SMAPE 的承诺与陷阱"（30 票）与"比率至上"（34 票）说明该指标对低值/比率敏感，需注意预测下限与比率特征。**裁决**：SMAPE 赛优先用比率/相对量特征，并对低销量做稳健处理。置信度：中。

## 4. 证据分级

| 断言 | 等级 | 说明 |
| --- | --- | --- |
| 3rd 的单 GAM + 留 3 月块 CV | 自述（简短） | 中 |
| 2nd 的 Boltzmann 来源与成分 | 自述 + 来源清单 | 中高 |
| 1st 的误差归因流程 | 自述（延迟发布、较简略） | 中 |
| 外生特征增益 | 高票 FE 帖 + 多个来源 | 中高 |
| SMAPE/比率讨论 | 高票帖 | 中 |

## 5. 悬案与缺口（登记）

- 1st 的完整代码与量化细节未收录（帖发布于赛后很久、篇幅短）；
- 4th–7th 是否确为 GAM 变体未核实；
- GDP/信心指数等外部数据的量化增益未给出；
- **图证缺口**：本场归档 0 图。

## 6. 图表证据

无可用图证（本场归档 0 图，图证缺口已登记）。

## 7. 出处

- 1st（13 票）：https://www.kaggle.com/competitions/tabular-playground-series-sep-2022/discussion/388206
- 2nd Boltzmann 集成（11 票）：https://www.kaggle.com/competitions/tabular-playground-series-sep-2022/discussion/356746
- 3rd 单 GAM（13 票）：https://www.kaggle.com/competitions/tabular-playground-series-sep-2022/discussion/356643
- FE 合集（43 票 / 10 评论）：https://www.kaggle.com/competitions/tabular-playground-series-sep-2022/discussion/351098
- 时序 CV 指南（38 票 / 17 评论）：https://www.kaggle.com/competitions/tabular-playground-series-sep-2022/discussion/350505
- 比率至上（34 票 / 7 评论）：https://www.kaggle.com/competitions/tabular-playground-series-sep-2022/discussion/349941
- 分层时序方法（34 票 / 4 评论）：https://www.kaggle.com/competitions/tabular-playground-series-sep-2022/discussion/350190
- GDP 外生数据（32 票 / 7 评论）：https://www.kaggle.com/competitions/tabular-playground-series-sep-2022/discussion/349371
- SMAPE 的陷阱（30 票 / 4 评论）：https://www.kaggle.com/competitions/tabular-playground-series-sep-2022/discussion/349553
- Jan 2022 冠军 notebook 公开（6 票）：https://www.kaggle.com/competitions/tabular-playground-series-sep-2022/discussion/349435
