# Optiver - Trading at the Close 轻量深读（Tier B）

> 赛事：Featured ｜ 主题 tabular（tabular-ts，高频金融）｜ 4436 队 ｜ 代码赛 ｜ 指标：Mean Columnwise MAE（MCMAE）
> 材料基础：`digests/optiver-trading-at-the-close.md`（8 篇正文：1st 338 / 9th 66 / 特征加速 54 / 6th 49 / 前作回顾 47 / 7th 43 / 14th 31 / 30th 25；120 条主题索引）+ 0 张归档图
> 轻读时间：2026-10（Tier B B01；Tier A 既有 notes 已较完整，本篇补对照/裁决/证据分级/缺口）

## 1. 一句话重述与数字账

预测收盘集合竞价最后 10 分钟（55 秒桶 × 200 只股票 × date_id）的价格变动，指标 MCMAE；**target 的跨股票加权和恒为 0**（合成指数约束），因此后处理（减加权均值/零和约束）是几乎免费的正收益。真正考的是三件套：**稳定 CV 环境下的特征工程 × 在线学习 × 内存/时限约束下的重训预算**。

| 动作 | 数字 | 来源 |
| --- | --- | --- |
| 1st 总成绩 | CV 5.8117 / 私有 **5.4030**（三模型 0.5/0.3/0.2；300 特征；在线 12 天×5，因超时实际 4 次） | 1st |
| 1st 在线消融（集成） | 不更新 5.4438 → 1 次 5.4157 → 5 次 5.4030；CatBoost 5.4523→5.4165；GRU 5.4690→5.4259；Transformer 5.4678→5.4296 | 1st 表 |
| 1st 后处理 | 验证集 CatBoost 5.8287→5.8240；三模型 5.8142→5.8117（≈0.005） | 1st 表 |
| 9th | XGB×3 seed、157 特征；最近 45 天样本权 1.5；只重训 2 次；后处理减加权和 | 9th |
| 6th | 35–36 特征；3 Transformer + 1 GRU（stock-wise attention、零和约束）；**逐日增量更新**；私有 5.4285 | 6th |
| 30th | LGBM 202 / CatBoost 141 特征（**分模型筛选**）；在线每 15 天；**interim update 期在线学习崩溃**；名次 18→37→41→39→40→30 | 30th |
| 7th | LGBM+NN；组中位数偏差特征 + 在线学习"大幅降误差" | 7th |
| 特征工程效率 | numba+multiprocessing 相对 pandas **~20×**；单次推断 23.5s→**1.04s**；IR 做因子筛选；流式缓存 | 特征帖 |

## 2. 逐方案对照矩阵

| 维度 | 1st | 7th | 9th | 6th | 30th | 14th |
| --- | --- | --- | --- | --- | --- | --- |
| 模型 | CatBoost+GRU+Transformer | LGBM+LSTM/ConvNet | XGB×3 seed | Seq2seq Transformer×3+GRU | LGBM+CatBoost | XGB+LGB |
| 特征 | 300（CatBoost 重要性 top300） | 少而精 + 组中位数偏差 | 157（分组增量筛选） | 35–36 | 202/141（分模型筛选） | 170 |
| 在线学习 | 12 天×5（实际 4） | 有 | 2 次 | 逐日增量 | 15 天（中期崩溃） | 尽量多 refit |
| 后处理 | 减加权均值 | — | 减加权和 | 零和约束 | — | — |
| 验证 | 400/81 单折 | 时间切分 | 单折 | 359/121 + EMA 平滑 | 单折 holdout | — |
| 私有 | **5.4030** | 7th | 9th | 5.4285 | 30th | 14th |

## 3. 共识、分歧与裁决

### 共识一：CV-LB 高度一致是"赛制属性"，先测再决定预算

1st/9th/30th 都报告本地 CV 与榜分稳定一致 → 简化验证（单折 holdout 即可）。**裁决**：开赛后第一件事是量化 CV-LB 关系；稳定则把预算全投特征/在线/融合，不稳定则先修验证。置信度：高。

### 共识二：在线学习是最大机制红利（4/4 使用）

1st 的消融把收益钉死：集成 **5.4438→5.4030**（5 次更新，−0.041），且 1 次更新已拿到大部分；6th 逐日增量；9th 两次；30th 15 天。**裁决**：测试期标签分批揭示 = 增量训练红利；节奏由内存/时限决定。置信度：高。

### 共识三：后处理零和约束几乎免费

1st（−0.005 级）、9th（跨股票加权和=0）、6th（训练时加零和约束）。**裁决**：从指标定义推导出的结构性约束，成本低、方向确定，应默认做。置信度：高。

### 共识四：内存/推断时限是硬约束，特征选择是必需项

1st 指出"GBDT + 在线学习最多用 ~200 特征（历史与在线数据拼接双倍内存）"；6th 只用 35 特征；9th/30th 都做激进筛选。**裁决**：本赛的特征数上限由重训预算倒推，不是模型容量。置信度：高。

### 分歧一：大特征量 vs 端到端少特征

1st 300 特征（灰盒）vs 6th 35 特征（纯 NN）——两者都在前 6；7th 刻意最小化 NN 特征以降低融合方差。**裁决**：两条路线都能赢，决定性的是**跨家族融合**（树+序列模型）而非特征多寡。置信度：中高。

### 分歧二：在线学习的节奏与稳健性

12 天×5（1st）vs 逐日（6th）vs 2 次（9th）vs 15 天（30th）；30th 在 interim update 期因数据形状不齐（缺股票/55 桶不完整）持续崩溃。**裁决**：节奏无最优常数，受时限与数据形状稳定性约束；工程上要为"新数据形状变化"写防护（按 date_id/stock 逐日加载 + 校验）。置信度：中高（30th 的失败是直接证据）。

### 分歧三：特征筛选方法

top-300 重要性（1st）、分组增量（9th）、分模型筛选（30th：CatBoost 好而 LGBM 坏的特征并存）。**裁决**：分模型筛选值得做；筛选目标函数是"在线重训后的 CV"。置信度：中。

## 4. 证据分级

| 断言 | 等级 | 说明 |
| --- | --- | --- |
| 1st 的在线消融表与后处理分差 | 自述 + 完整表格 | 中高 |
| CV-LB 稳定 | 三队独立自述 | 中高 |
| 9th/6th/30th 的私有分数与做法 | 自述 | 中 |
| 特征加速 20×/1.04s | 自述（可复现思路） | 中 |
| 30th 的 interim 崩溃 | 自述 + 时间线 | 中高 |
| 合成指数权重/Reverse Engineering 等机制帖 | 未收录 | —（缺口） |

## 5. 悬案与缺口（登记）

- 2nd/3rd/4th/5th/8th/10th+ 方案未收录；1st 的"magic features"（seconds_in_bucket_group 聚合、rank 特征）工程细节只有代码片段。
- `442851` Weights of the Synthetic Index（141 票）与 `457721` Reverse Engineering（50 票）未收录——后处理的机制来源缺失。
- `462639` NN with no FE（63 票，"5.34X"）与最终 5.40 的关系（是否公开榜虚高）未厘清。
- 30th 的中期更新崩溃原因无官方说明；赛制数据形状规则未收录。

## 6. 图表证据

**本场无归档图片**（`intel/optiver-trading-at-the-close/bodies/` 无 `*_img`），无法内嵌图证。数字与结构证据均来自正文表格。

## 7. 出处

- 1st（338 票）：https://www.kaggle.com/competitions/optiver-trading-at-the-close/discussion/487446
- 9th（66 票）：https://www.kaggle.com/competitions/optiver-trading-at-the-close/discussion/486868
- 特征加速（54 票）：https://www.kaggle.com/competitions/optiver-trading-at-the-close/discussion/451735
- 6th（49 票）：https://www.kaggle.com/competitions/optiver-trading-at-the-close/discussion/486040
- 前作回顾（47 票）：https://www.kaggle.com/competitions/optiver-trading-at-the-close/discussion/442167
- 7th（43 票）：https://www.kaggle.com/competitions/optiver-trading-at-the-close/discussion/486169
- 14th（31 票）：https://www.kaggle.com/competitions/optiver-trading-at-the-close/discussion/485985
- 30th（25 票）：https://www.kaggle.com/competitions/optiver-trading-at-the-close/discussion/462650
- 缺口登记：442851、457721、462639、450626、444516、441590
