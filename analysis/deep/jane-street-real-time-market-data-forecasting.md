# Jane Street Real-Time Market Data Forecasting 轻量深读（Tier B）

> 赛事：Featured ｜ 主题 tabular（tabular-ts，金融）｜ 3757 队 ｜ **代码赛（提交 notebook，隐藏期在线推理）** ｜ 指标：Zero-Mean R²（分数尺度 ~0.01）
> 材料基础：`digests/jane-street-real-time-market-data-forecasting.md`（6 篇正文：私 8th 556542 / 公 17th 556541 / 私 162nd 589829 / 简单解 550849 / 参考帖 540437 / 往届汇总 541003；120 条主题索引）+ 6 张装饰头图（无分析图）
> 轻读时间：2026-10（Tier B B04）

## 1. 一句话重述与数字账

在**评测期实时**预测匿名化金融标的收益：notebook 每周/每日接收新数据、必须现场训练与推理（约 1 分钟/日 的时限）。真正的考点是**非平稳数据下的在线自适应学习 + 推理时延工程 + 验证窗口对齐**，而不是模型结构本身。

| 关键数字 | 值 | 来源 |
| --- | --- | --- |
| 私榜 8th（295 票） | 2 折时序 CV（每折 200 天，与公开集同规模）+ 200 天 gap 模拟私榜；数据起点 date_id≥700（968 个 time_id 稳定后）；标准化+零填充；16 个高相关特征 + 市场均值 + 1000 time_id 滚动统计 + time_id（**+0.002 CV**）；GRU 双架构 2 模型 × 3 seed 集成 → **LB 0.0112**（最佳单模 0.0105）；**辅助 responder（7/8 + 自造 8/60 日滚动）再 +0.001**；**在线学习（每新一天 lr=3e-4 单次更新、只算 responder_6 loss）→ +0.008 CV**；推理 0.06s/时间步（0.02s 数据处理）、更新 3.6s/日 | 8th |
| 公榜 17th（57 票） | 50/50 = 3 层 Transformer（跨 symbol 注意力）+ 3 层 Transformer（跨 time_id + 可学习位置编码）；GELU 防死神经元（在线学习要能"复活"参数）；全 9 个 responder 联合训练；**在线学习 = 每天对最近 7 天数据训 7 个 epoch（lr=1e-4）**，是主要提分来源；赛后更新：**改为"每 8 天对最近 56 天重训一次"还能再 +0.0012** | 17th |
| 私榜 162nd（11 票） | 70% 在线 TabM MLP（3×512，Polars，每天对最近 3–4 天微调 10 epoch、lr=1e-5，小 lr + 混旧数据防灾难性遗忘）+ 30% 静态 LightGBM 集成（79 特征 + 9 个昨日 responder 滞后）；预测 clip | 162nd |
| 简单解（32 票） | 3 层 MLP、单 symbol、无在线学习/集成 → 0.0064；作者强调"训练细节与泛化" | 550849 |
| 事件 | 公开测试集扩展与榜面更新（54 票）；作弊质疑两帖（30 票 ×2）；responder 逆向工程帖 165 票 | 社区 |

## 2. 逐方案对照矩阵

| 维度 | 8th（私榜） | 17th（公榜） | 162nd（私榜） | 简单解 |
| --- | --- | --- | --- | --- |
| 主干 | GRU（3 层 / 1 层+2 线性） | 双 Transformer（symbol 轴 + time 轴） | TabM MLP + LightGBM | 3 层 MLP |
| 在线学习 | **每日单次前向更新**（lr 3e-4，+0.008） | **每日回放最近 7 天 ×7 epoch**（lr 1e-4） | 每日微调最近 3–4 天（lr 1e-5） | 无 |
| 辅助目标 | responder_7/8 + 自造 8/60 日滚动平均 | 全 9 个 responder | 9 个昨日 responder 作特征（GBDT） | 无 |
| 特征工程 | 市场均值 + 1000 步滚动统计 + time_id | signed log + time_id + weight | 79 特征 + 滞后 | 79 特征 |
| 验证 | 2 折 ×200 天 + 200 天 gap | 训练全量（承认 CV/LB 弱相关） | 最后 100 天（自认找不到好相关） | 强调泛化 |
| 分数 | LB 0.0112（集成） | 公榜 17 | — | 0.0064 |

## 3. 共识、分歧与裁决

### 共识一：在线学习是本赛的第一杠杆（3/3 队）

8th 单次更新 +0.008 CV；17th 的 7 天回放是"主要提分来源"；162nd 把在线 TabM 设为 70% 权重。**裁决**：非平稳 + 允许边训边测的赛制下，把算力预算投向"如何可靠地更新"比换模型族更值钱。置信度：高（三队独立自述 + 8th 有逐项消融表）。

### 共识二：更新强度需要调参，不是"越勤越好"（17th 赛后修正）

17th 的赛后实验：把"每天 × 最近 7 天"换成"每 8 天 × 最近 56 天"再 +0.0012。162nd 用极小 lr（1e-5）+ 混旧数据防灾难性遗忘。**裁决**：在线学习存在"回放窗口 × 频率 × lr"的三维权衡；单日快更新只是起点。置信度：中高（单队赛后对照 + 另一队的工程选择佐证）。

### 共识三：验证必须模拟"评测时的时间结构"（8th vs 17th）

8th 的 200 天验证窗与公开集同规模、另留 200 天 gap 模拟私榜；17th/162nd 都承认 CV-LB 相关性弱、只能靠全量训练 + 稳健工程。**裁决**：代码赛的 CV 要复刻"信息到达节奏"（gap、窗口长度、更新频率）；只做随机切分会系统性高估。置信度：中高。

### 分歧一：架构选择（RNN / 双 Transformer / MLP+GBDT）

三种结构都能进前列/可接受名次（0.0064–0.0112）。8th 明确说 MLP、时序 Transformer、跨 symbol 注意力"对自己无效"，而 17th 恰恰靠双 Transformer 拿公榜 17。**裁决**：本赛结构差异被在线学习与工程细节淹没——**同分带内结构可互换，胜负在更新策略与推理时延**。置信度：中高。

### 分歧二：responder 逆向工程的用法

社区帖（555562，165 票）逆推出 responder 语义：responder_6 ≈ 20 日滚动平均、7 ≈ 120 日、8 ≈ 4 日（含噪声）→ 可由 N 日平均推算 N×K 日平均。8th 直接用它构造辅助目标（+0.001）；17th 阅读后"没找到用法"，改为 9 个 responder 全预测。**裁决**：领域结构知识是"可选增益"，能转化成辅助目标才有价值。置信度：中高。

### 事件：榜面可信度与作弊质疑

公开测试集扩展（550790）+ 两帖作弊质疑（555273 / 586090）。**裁决**：金融高噪声榜要保留对"榜面异常"的怀疑；合法稳健的自适应管线仍是唯一可复制路径。置信度：中（现象级）。

## 4. 证据分级

| 断言 | 等级 | 说明 |
| --- | --- | --- |
| 8th 的 CV 表/消融/在线学习 +0.008 | 自述 + 完整分数表 + 公开代码 | 高 |
| 17th 的在线学习策略与赛后修正 +0.0012 | 自述（无表格） | 中高 |
| 162nd 的 70/30 混合与微调细节 | 自述 | 中 |
| responder 逆向工程语义 | 社区多轮讨论 + 8th 转述应用 | 中高（结构自洽） |
| 简单 MLP 0.0064 | 自述（提问帖） | 中 |
| 作弊质疑 | 论坛帖（未证实） | 低/现象 |

## 5. 悬案与缺口（登记）

- 顶尖名次（0.013+ 档）的完整方案未入库——17th 明言"想不通 top 队伍如何到 0.01+（相对其方法的差距）"，本档缺 1st–5th 的 write-up；
- 公开集扩展（550790）对分数与作弊格局的实际影响未量化；
- CatBoost 在线（556544，60 票）与 LGBM 推理加速（542697，45 票）两条工程线未细读；
- **图证缺口**：本场归档 6 张图全部是往届汇总帖（541003）的装饰横幅（`[图 N: header]`），无架构图/分数表可作证；原帖内嵌图多为站外/CDN 图，未归档。

## 6. 图表证据

无可用图证（见上"图证缺口"）。归档 6 图均为装饰横幅，按"梗图/无信息图跳过"规则不内嵌。

## 7. 出处

- 私榜 8th（295 票）：https://www.kaggle.com/competitions/jane-street-real-time-market-data-forecasting/discussion/556542
- 公榜 17th（57 票）：https://www.kaggle.com/competitions/jane-street-real-time-market-data-forecasting/discussion/556541
- 私榜 162nd（11 票）：https://www.kaggle.com/competitions/jane-street-real-time-market-data-forecasting/discussion/589829
- 简单解（32 票）：https://www.kaggle.com/competitions/jane-street-real-time-market-data-forecasting/discussion/550849
- responder 逆向工程（165 票）：https://www.kaggle.com/competitions/jane-street-real-time-market-data-forecasting/discussion/555562
- 公开测试集扩展（54 票）：https://www.kaggle.com/competitions/jane-street-real-time-market-data-forecasting/discussion/550790
- CatBoost 在线训练（60 票）：https://www.kaggle.com/competitions/jane-street-real-time-market-data-forecasting/discussion/556544
- 往届金融赛方案汇总（48 票）：https://www.kaggle.com/competitions/jane-street-real-time-market-data-forecasting/discussion/541003
