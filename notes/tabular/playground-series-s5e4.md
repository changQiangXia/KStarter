# Playground Series S5E4 - 播客收听时长预测

> 主题：tabular ｜ 子类：— ｜ 领域：媒体（合成数据） ｜ 类别：Playground
> 截止：2025-04-30 ｜ 队伍数：3310 ｜ 机制：标准赛 ｜ 指标：MSE（RMSE）
> 数据来源：`intel/playground-series-s5e4/`（80 条主题索引 + 6 篇 write-up 正文）

## 1. 任务与数据

- 预测目标：播客单集收听时长（回归 RMSE）。
- 数据主结构：`Listening_Time ≈ 0.72 × Episode_Length`，其余 9 个特征调制这条线性关系；**Episode_Length（ELM）承载 90%+ 信号，但 11.6% 缺失**——这一缺失结构是本场的方法分水岭。

## 2. 验证方案

- 所有模型统一 5 折，TE/伪标签全部折内完成（1st 反复强调"remove all leaks"）。
- 2nd：单 LightGBM + TE，1552 特征、79.5 万行，靠类型转换与避免复制在 **Kaggle CPU** 上 4 小时训完，5 seeds 平均。

## 3. 模型家族

| 方案 | 使用者层次 | 关键点 | 出处 |
| --- | --- | --- | --- |
| RAPIDS cuML 三级栈（75 模型） | 1st | 非线性 Level-2 处理"有/无 ELM"双情景 | topic 575784 |
| 单 LightGBM + TE（1552 特征） | 2nd | CPU 可复现；5 seeds | topic 575840 |
| TE + 三级结构 | 3rd | 同族配方 | topic 575862 |
| 100 OOF 的懒人集成 | 5th | 复盘两处失误 | topic 575839 |

## 4. 关键技巧

- **为什么要非线性栈**（1st 的核心论证）：数据存在"有 ELM / 无 ELM"两个情景，各自最优模型不同；**爬山/Ridge 这类线性 Level-2 只能做加权平均，而非线性栈能按情景选用不同模型的预测**。这是"深栈 vs 浅集成"的教科书案例。
- **多样性 ×5 训练矩阵**：同一批 12 个模型各训练 6 种变体——(1) 不同特征工程/超参；(2) **全行删掉 ELM** 训练（专攻缺失情景）；(3) 预测 `target/ELM` 比值再乘回；(4) 用 train+test 预测 ELM 再回填/替换/相乘；(5) 伪标签；(6) 特征子集差异。
- **用 test.csv 的列**：预测 ELM 时 train+test 联用（两边的列齐全）——无标签数据的合法用法。
- 平台期方法：每天用 3×A100 + cuDF/cuML 造一打新模型，只留能提升栈的少数。
- 2nd 的工程：1552 特征 + 精心 dtype 转换，让单模型在 CPU 上可训——**复现门槛也是竞争力**。

## 5. 可迁移性评估

- **可直接迁移**：缺失主特征的双情景建模（删特征专门训一组模型）；比值目标法；用无标签数据预测协变量再回填；多样性训练矩阵；深栈适配复杂交互。
- **需要前提**：GPU + RAPIDS（cuDF/cuML）用于规模化；大量 OOF 管理。
- **不建议照搬**：无差别堆三级栈（本场因交互深才值得）；忽视 TE 泄漏检查。

## 6. 对新手的关键启示

- **先找主特征与其缺失率**：本场一句"ELM 占 90% 信号且缺 11.6%"就决定了所有高分解法的形态。
- 集成器要匹配数据结构：线性加权 vs 非线性栈不是口味问题，而是"情景差异存在与否"的问题。
- 2nd 证明单模型+海量 TE 也能亚军——特征工程到位时，集成不是必需品。

## 8. 轻读结论（2026-10 补）

**一句话**：`Listening_Time ≈ 0.72 × ELM` 且 ELM 缺失 11.6% → 数据分成两个情景：1st 用 **75 模型 3 级 RAPIDS 栈**（CV 11.54 / 私榜 11.44）击败线性爬山（私榜 11.503）；2nd 反其道而行，**单 LightGBM + 1552 个 TE 特征**在 CPU 上 4 小时训练拿到亚军。

- 1st（575784）：L1 12 类模型 ×5+ 变体；多样性来源 = 不同特征工程/超参、**全行删 ELM**、预测 `target/ELM` 比值、用 train+test 预测 ELM 再回填/替换/相乘、伪标签；L2 = XGB+MLP（73 个 L1 预测，11.56）；L3 = 加权平均（11.54）。
- 2nd（575840）：1552 特征 / 794,868 行；LGBM `n_iter=12000, depth=15, lr=0.008, leaves=480, colsample=0.25`；TE = 12 列 × pair_size 1–6 + 统计量；5 seeds。
- 3rd（575862）：TE 2–7 元组合、top 模型约 270 个 TE 特征；首次 stacking 11.66→11.62；最终 80% stack + 20% 爬山；最好单模 LGBM CV 11.79。
- 6th（575783）：三处"泄漏"修正——ELM 小数位 >2（1017 行，系数 0.9554）、`Number_of_Ads>3`（7 行，×1.0588）、相同特征组合用组均值覆盖；1000+ 实验用 WandB + 自动 commit 管理。
- 5th（575839）：100 OOF + Ridge；未裁剪提交私榜 **177.25**（灾难），最强单模 30 折 XGB 私榜 11.67（≈34 名）。
- 社区：强相关（149 票）、强交互（142 票）、重复行（49 票）、小数位（27 票）、建议 cap 离群（11 票）。

**裁决**：主特征结构性缺失 → 用非线性 L2 + 专攻缺失情景的模型；TE 组合仍是表格赛主干；合成数据的生成痕迹先挖；提交必须 clipping 并保留保守版本。

**悬案**：4th（575782，53 票）与 19th/18th 等正文未收录；WarpGBM 等 GPU 工具帖未细读；原始数据重复行结构未核对。

## 9. 图表证据

![数值特征与目标的关系](../../intel/playground-series-s5e4/bodies/571549_img/01.png)

**图 1**（topic 571549）：ELM 与目标近似线性、Ads 负相关、Host Popularity 非线性。

![小数位泄漏](../../intel/playground-series-s5e4/bodies/575783_img/01.png)

**图 2**（topic 575783）：小数位 >2 的 1017 行几乎由 ELM 线性决定（系数 0.9554、RMSE 6.17）。

![特征组合的 RMSE–覆盖率搜索](../../intel/playground-series-s5e4/bodies/575783_img/04.png)

**图 3**（topic 575783）：5006 个特征组合的 RMSE–覆盖率散点，用于筛选 TE 组合。

![1st 的三级栈结构](../../intel/playground-series-s5e4/bodies/575784_img/02.png)

**图 4**（topic 575784）：12 类 L1 模型 ×5+ 变体 → 非线性 L2（XGB+MLP）→ L3 加权平均。

## 10. 出处

- 1st：RAPIDS cuML 三级栈与多样性 ×5：https://www.kaggle.com/competitions/playground-series-s5e4/discussion/575784
- 2nd：单 LightGBM + 目标编码：https://www.kaggle.com/competitions/playground-series-s5e4/discussion/575840
- 3rd：TE 与三级结构：https://www.kaggle.com/competitions/playground-series-s5e4/discussion/575862
- 5th：100 OOF 与复盘：https://www.kaggle.com/competitions/playground-series-s5e4/discussion/575839
- 6th：特征组合选择与数据泄漏：https://www.kaggle.com/competitions/playground-series-s5e4/discussion/575783
- 强相关 EDA（149 票）：https://www.kaggle.com/competitions/playground-series-s5e4/discussion/571549
