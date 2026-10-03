# GoDaddy Microbusiness Density 深读：倍率建模 × 数据质量 × 榜单探针

> 赛事：Featured ｜ 主题 tabular（面板时序）｜ 3547 队 ｜ 标准赛 ｜ 指标 SMAPE（3135 县 × 未来 3 个月）（2023-06-16 截止）
> 材料基础：`digests/godaddy-microbusiness-density-forecasting.md`（8 节：1st/2nd/3rd/6th + Hugo 复盘 + 基线帖 + 基线修正帖 + Giba SVR）+ 6 张图
> 深读时间：2026-10（Tier A #30，**Batch 3 收官**）

## 0. 一句话重述：这道题真正在考什么

题面是"预测 3135 个县未来 3 个月的微型企业密度"，实际被考的是**三件与模型无关的事**：

1. **倍率（multiplier）建模**：序列非平稳（只有全局线性增长系数稳定）→ 预测"相对变化"再乘回基期（3rd 的 GRU 倍率、Hugo 的相对目标、Giba 的全局线性乘子；M5 经验："平均 notebook × 0.95 就能夺金"）；
2. **数据质量与口径陷阱**：2021-01 方法学变更造成跳变、异常县（Sheridan Co 2.36 家/劳动年龄人口）、**分母换口径**（2023 用新 census，Last-Value 基线不修正私榜 3.28、修正后 1.46）、Dec22/Jan23 约 60% 数据错误（1st 实测）——**先修数据口径，再谈模型**；
3. **榜单探针（probing）**：SMAPE 对单县变化极敏感（公式给出每县贡献），公开榜可反推出"某个县 active 的精确变化"；20 天可探约 100 个县；但数据错误期探针失效（1st 的领先从 0.2 缩到 0.08）——**探针要与数据质量审计联动**。

一句话：**这是一场"相对指标 + 脏数据"的比赛**——冠军用线性回归（4–5 个特征）夺冠；分差来自倍率化、数据修正、探针与后处理的组合，而不是模型复杂度。

## 1. 材料与角色

| 帖子 | 作者 | 票数 | 角色与独有信息 |
| --- | --- | --- | --- |
| [373099](https://www.kaggle.com/competitions/godaddy-microbusiness-density-forecasting/discussion/373099)（基线帖，196 票） | Chris Deotte | 196 | **三基线对照**：Last Value（1.093/1.101）、Linear（1.092/1.098）、Seasonal 融合（1.095）；人口小县用 last value、线性模型只用于人口 >25k |
| [389215](https://www.kaggle.com/competitions/godaddy-microbusiness-density-forecasting/discussion/389215)（基线修正，141 票） | Chris Deotte | 141 | **census 换口径陷阱**：2023 用新分母 → 未修正 3.2776、修正后 **1.4631**；给出 census 数据与 starter notebook |
| [418287](https://www.kaggle.com/competitions/godaddy-microbusiness-density-forecasting/discussion/418287)（3rd，84 票） | — | 84 | **倍率 + GRU**：41 个月 → 每县 18 条序列（56k）；只训 Top 90% 大县；3×8 GRU；探针 1.0045 后处理 → 12th→3rd |
| [395131](https://www.kaggle.com/competitions/godaddy-microbusiness-density-forecasting/discussion/395131)（1st，48 票） | @kaggleqrdl | 48 | **线性回归 + 泛化**：4–5 特征、最后窗口 CV、早期停止贪心选择；LB 探针；全量数据不折腾清洗；诚实复盘 snafu 对探针的冲击 |
| [395011](https://www.kaggle.com/competitions/godaddy-microbusiness-density-forecasting/discussion/395011)（SVR，36 票） | Giba | 36 | 全局线性乘子 + RAPIDS SVR；逐预测跨度相对 Last Value 的增益表（0.0171→0.4750）；RAPIDS 34× 加速 |
| [417821](https://www.kaggle.com/competitions/godaddy-microbusiness-density-forecasting/discussion/417821)（6th，24 票） | 此般浅薄 | 24 | **目标展平（target flatten）+ n_cross 增强框架**；12 月验证用"改善月数"而非均值；黑名单 10 县；后处理 ×1.001 |
| [394822](https://www.kaggle.com/competitions/godaddy-microbusiness-density-forecasting/discussion/394822)（复盘，24 票） | Hugo | 24 | XGB 三 GAP 模型（12 折 TS=29..40；CV 2.34/2.79/3.18，总 2.76±0.06）；GRU 2.84；"模型只发现全局线性趋势，last×1.01x 也差不多" |
| [395264](https://www.kaggle.com/competitions/godaddy-microbusiness-density-forecasting/discussion/395264)（2nd，19 票） | Daniel Phalen | 19 | **数据清洗挑战**：SMAPE 贡献公式、跳变回撤、continuous contract 平滑、无前视特征、探针 100 县/20 天；质疑探针边界 |

**材料缺口（未扩采，登记备查）**：17 条 write-up 标记中收录 8 节。

## 2. 逐方案对照矩阵

| 维度 | 1st @kaggleqrdl | 2nd Daniel | 3rd（倍率 GRU） | 6th 此般浅薄 | Hugo（复盘） | Giba SVR |
| --- | --- | --- | --- | --- | --- | --- |
| 目标形式 | 月 lookahead 的 lag 变化（百分比）| 1 月前向变化→回滚迭代 | **逐月倍率（ratio）** | 年化率 `(mbd[t+n]/mbd[t])^(1/n)-1` + 目标展平 | 相对目标（GAP2/3/4 分别预测 mbd_43/44/45 比 mbd_40） | active 目标 + 全局线性乘子 |
| 模型 | **线性回归**（试遍一切后） | XGBoost | 3 层 GRU（8 单元） | XGBoost | XGB 三 GAP + GRU | RAPIDS SVR |
| 数据清洗 | 只剔 3 个问题县；不折腾 | **continuous contract 平滑**（大跳变置零）；异常回撤假设 | 统一到 2021 census；小县用 last value | 2022-06→08 平滑；10 县黑名单；按 active 展平目标 | 2021 census 统一；300 个跳变（多在 2021-01）平滑；blacklist | 统一口径 |
| 验证 | **最后窗口 CV + 早期停止贪心（4–5 特征）** | 无前视特征；roll-forward | GroupKFold（按县） | 12 月验证 + **改善月数** | 12 折（TS=29..40）逐折 SMAPE | 最后 12 月，增益对 Last Value |
| 探针/后处理 | LB 探针 + 波动县聚焦；四舍五入到整数 active | **逐县探针（约 100 县）+ 回撤** | **探针乘子 1.0045**（Top 90%） | n_cross 框架 + ×1.001 | 无（复盘） | 全局乘子优化 SMAPE |
| 成绩 | 冠军 | 第 2 | 12th→**3rd**（PP） | 6th | 复盘 | 增益表 |

## 3. 共识、分歧与裁决

### 共识一：预测倍率/相对变化，而不是绝对值（全员）

3rd：把 41 个月序列转成倍率再训 GRU；Hugo：相对目标（mbd_43/mbd_40 等）；Giba：全局线性乘子；1st：lag 百分比变化特征；6th：年化率目标。**共同原因：水平非平稳（趋势+口径跳变），而"相邻月比值"更平稳**。

**裁决**：非平稳面板数据的第一动作是目标变换（diff/ratio/年化率）；配合"预测比值→连乘还原"。置信度最高。

### 共识二：数据质量与口径是主要矛盾（有硬证据）

Chris 的修正帖给出最硬数字：**Last-Value 基线从 3.2776 修正到 1.4631**（新 census 分母）；2nd：2021-01 方法学变更 + Sheridan Co 异常 + PPP 时代欺诈嫌疑 + "大跳变常回撤"（CFIPS 48155 图）；1st：Dec22/Jan23 约 60% 数据错误（以 SMAPE 衡量）；6th：2022-06→08 的"急涨急跌"需平滑。

**裁决**：先做 census 口径对齐（训练统一到 2021；预测调整到 2023 新分母），再处理跳变（平滑/回撤/黑名单）；否则任何模型都在拟合错误数据。置信度最高。

### 共识三：小县用 Last Value，模型只服务大县（Chris/3rd/Giba/Hugo）

Chris：线性模型只用于人口 >25k；3rd：只训 Top 90% 大县，小县直接用最后值；2nd：人口切点 ~5000；1st：四舍五入到整数 active（小县 active 少，取整即正则）。**根因：SMAPE 相对误差 + 小县 active 基数小 → 一两家的变化就主导分数**。

**裁决**：按县规模分流建模是"指标与数据"共同决定的结构；小县上任何复杂模型的期望收益都低于风险。置信度最高。

### 分歧一：LB 探针的合法性与可靠性

2nd 明确质疑边界（"最大不确定性是探针被允许到什么程度"）；1st/3rd/2nd 都实际用了探针（1st 聚焦 ~10 个波动县；2nd 20 天探 ~100 县，且"做差更容易反推"；3rd 探出全局乘子 1.0045）；但 1st 的 snafu 复盘显示**数据错误期探针会反噬**（LB 领先 0.2→0.08）。

**裁决**：探针是"数据信息通道"，其价值与数据质量审计绑定；在口径/数据未对齐前，探针结论不可信。置信度中高。

### 分歧二：要不要复杂模型

1st："试遍 sklearn 回归/ARIMA/层次模型/XGB/Cat/LGB/PyTorch，线性回归的 CV 最可靠"；Hugo："模型只是发现全局线性趋势，last×1.010/1.015/1.020 差不多"；6th/Giba 用 XGB/SVR 也只有小幅增益；GRU 单独 12th。

**裁决**：本场模型差异 ≤ 数据修正与探针的量级；简单模型 + 稳健特征 + 数据工程是主答案。置信度最高。

## 4. 增量数字账

| 动作 | 数字 | 来源 |
| --- | --- | --- |
| 基线水平 | Last Value 1.093/1.101；Linear 1.092/1.098；Seasonal 融合 1.095 | Chris 基线帖 |
| **census 修正** | Last Value：3.2776 → **1.4631**（2023 新分母） | Chris 修正帖 |
| 探针灵敏度 | 单县归零→非零每月差 ~0.0638；单县变化 <1% 可在 4 位小数榜单上分辨 | 2nd |
| 探针规模 | 20 天约 100 县 | 2nd |
| 1st 的探针反噬 | LB 领先从 ~0.2 缩到 ~0.08（Dec/Jan 60% 数据错误） | 1st |
| 1st 的特征数 | 4–5 个（早期停止贪心；L10/11 employment、bb census 是关键） | 1st |
| 1st 的冗余检验 | 去 3 个问题县；不裁剪；四舍五入到整数 active | 1st |
| 3rd 的规模 | 41 个月；每县 18 条序列 ≈ **56k** 序列；Top 90% 县；GRU 3×8 | 3rd |
| 3rd 的后处理 | 探针乘子 1.0045 → 12th 跳到 **3rd** | 3rd |
| Hugo 的 CV | GAP2/GAP3/GAP4：2.34/2.79/3.18；总 2.76±0.06；GRU 2.84 | Hugo |
| Hugo 的观察 | last value × 1.010/1.015/1.020 与 XGB 的 CV 相近 | Hugo |
| 6th 的技巧 | 目标展平 `coef=1/(0.007*(active/10+105))+1`；10 县黑名单；×1.001 后处理 | 6th |
| Giba 的增益表 | 1–6 月跨度相对 Last Value 增益 0.0171/0.0611/0.1555/0.2621/0.3524/0.4750；3 月 Last Value 2.717 | Giba |
| Giba 的加速 | sklearn SVR 4607s → RAPIDS SVR 136s（**34×**） | Giba |
| 人口阈值 | 线性模型仅人口 >25k（Chris）；2nd 切点 ~5000 | Chris/2nd |

**可复算/结构校验（3 处吻合）**

1. 预测总量：3135 县 × 8 月 = **25080** ✓（Chris）；
2. 3rd 的序列数：3135 × 18 ≈ **56,430 ≈ 56k** ✓；
3. census 公式：adult_population = 100×active/density ✓（Green County 80/1→8000；Fairfield 120,000/16→750,000）。

## 5. 机制推演

**M1｜为什么倍率化有效**：微型企业密度的绝对水平被三件事驱动——全局增长趋势、人口分母口径、县级局部事件；其中只有"全局趋势"跨期稳定。**相邻月比值消除了县级水平（固定效应）与大部分趋势**，让模型只学"相对变化的可预测部分"，再用连乘还原。M5 的经验是同一机制。

**M2｜为什么换 census 会一次性改变全榜**：density = 100×active/adult_population；2023 年所有县的分母切换到新 census 文件 → 全榜整体平移/缩放。**修正不是"改进模型"，而是修正评测口径**——未修正的模型在私榜系统性偏移（3.28 vs 1.46）。这类"分母换口径"是面板经济数据的典型陷阱。

**M3｜SMAPE 的县规模偏好**：ΔSMAPE,i = 200/n × |F−A|/(F+A)——绝对贡献与县数量无关，但**相对误差对基数小的县放大**；25% 的县"最小变化"都大于模型 0.5%/月的典型预测幅度 → 小县预测被量化噪声主导。分流（小县 last value + 取整）是唯一稳健解。

**M4｜跳变为什么常常回撤**：2021-01 方法学变更、欺诈/PPP 冲刺、误分类堆积（Sheridan Co）造成的跳变并非真实需求变化，随后 3–12 个月回归（CFIPS 48155 图）。**"识别大跳变 → 视作暂时冲击 → 平滑/回归"** 是 continuous contract 的思想；而 Dec 与 Mar 之间的 2 个月 gap 给了回撤时间（2nd 的论点）。

**M5｜探针如何把 SMAPE 变成"逐县读数"**：给定 SMAPE 公式与榜单 4 位小数分辨率，改动单个县的预测值可反解其真实 active 变化；更优策略是"先故意做差"（把预测拉远），用绝对差反推（2nd）。**探针本质是用提交次数购买隐藏标签信息**——其可靠性完全依赖榜单数据本身正确。

**M6｜为什么简单模型赢**：数据只有 41 个月 × 3135 县、含口径突变与大量跳变；CV 窗口短（最后几个月）→ 复杂模型的高方差让"CV 改进"多半是过拟合。1st 的"4–5 特征 + 最后窗口 CV + 早期停止"把模型容量压到与数据信息量匹配的水平。

## 6. 证据分级

| 断言 | 等级 | 说明 |
| --- | --- | --- |
| census 修正 3.2776→1.4631 | **可复现（notebook + census 数据公开）** | 直接实验证据 |
| SMAPE 归零→非零贡献 ~0.0638 | **可复算（公式）** | 2nd 给出的解析式 |
| 基线三件套（1.093/1.092/1.095） | **可读取（帖内数字）** | 有公开 notebook |
| 3rd 的 12th→3rd（PP 乘子） | **自述（强）** | 前后分数与机制明确 |
| 1st 的探针/Snafu 复盘 | **自述** | 无从复核但细节丰富 |
| 6th 的目标展平公式 | **自述 + 图** | 分布图支撑（active 基数 vs 目标均值） |
| Giba 的增益表 | **可读取（表）** | 12 个月平均 |
| "60% 数据错误" | **1st 自述（以 SMAPE 度量）** | 估算口径未完全公开 |

## 7. 边界条件与反事实

- **前提**：允许用公开榜探针（规则未禁止但边界模糊）；外部 census/就业数据可用；预测目标有 2 个月 gap（回撤窗口）。
- **反事实（Chris/全员）**：若不做 census 分母修正，所有模型在 2023 私榜系统性错位（Last Value 3.28 而非 1.46）——**这是本场最大的一次性收益/损失项**。
- **反事实（1st）**：若 Dec/Jan 数据未被污染，其探针策略的 LB 领先可能保持 ~0.2；数据错误期把探针优势打回 0.08。若加入花哨清洗（裁剪等），其自述 CV 反而退化。
- **反事实（3rd）**：GRU 单独仅 12th；后处理乘子（探针 1.0045）把它推到 3rd——**倍率预测 + 探针修正的组合增益大于模型升级**。
- **边界（小县）**：Loving County（90 成人）一人的行为即可改变其 density；任何模型在这种基数上都没有信息优势。
- **伦理边界**：探针的允许范围是社区争议点（2nd 的疑问）；与明显的数据泄漏（如 psp 的 OpenGameData）不同层级。

## 8. 悬案与失败学

**悬案**

1. **探针的合理边界**：20 天 100 县是否为"规则允许的极限"，官方未表态；
2. **Dec22/Jan23 数据错误的成因与官方处理**（60% 错误率的度量口径未公开）；
3. **县级相关性结构**（1st 的未来方向）：相邻县是否以不同滞后期联动，能否全局建模。

**失败学**

| 失败 | 来源 | 教训 |
| --- | --- | --- |
| 花哨数据清洗（裁剪/复杂修正） | 1st | 退化；"不折腾"反而更好 |
| 逐县独立模型 | 1st | 数据不足，白做 |
| ARIMA/层次模型/深度网络 | 1st | 全都输给线性回归的 CV 可靠性 |
| 只看平均 CV | 6th | 异常月份主导均值；改用"改善月数" |
| 直接预测 3 月后变化 | 2nd | 偏置大；改为 1 月前向 + 回滚迭代 |
| 未换 census 的 2023 预测 | Chris | 3.28 vs 1.46 的系统性错误 |
| 在数据错误期做探针决策 | 1st | 探针失效，领先缩水 |
| 公开 notebook 的前视特征（2019 训练用 2021 census） | 2nd | 隐式未来信息；CV 虚高 |
| 复杂模型 + 大量特征 | Hugo/1st | 只是发现了全局线性趋势；last×1.01x 等效 |

## 9. 图表证据

> 路径相对本文件（`analysis/deep/`）：`../../intel/godaddy-microbusiness-density-forecasting/bodies/<topic>_img/NN.ext`

**图 1：目标展平（6th）——目标的绝对值随 active 基数变化**（topic 417821）——`../../intel/godaddy-microbusiness-density-forecasting/bodies/417821_img/02.jpeg`

*读图结论*：按 `active_round` 分箱后，正目标组（蓝）均值 ~+0.005~0.01、负目标组（橙）~−0.012；**active 越小目标绝对幅度越大** → 用 `coef=1/(0.007*(active/10+105))+1` 把目标范围"展平"再训练、预测时反变换。这是"目标分布随样本规模漂移"的通用处理。

**图 2：大跳变回撤示例（2nd）**（topic 395264）——`../../intel/godaddy-microbusiness-density-forecasting/bodies/395264_img/01.png`

*读图结论*：CFIPS 48155 的 active 从 ~10 急升到 ~140 再回落到 ~60——2021 方法学变更/异常堆积后的回撤；这正是"识别跳变→视作暂时冲击→平滑/回撤"策略的依据，也是 Dec 与 Mar 两个月 gap 的价值。

**图 3：Hugo 的 XGB 逐折 CV（12 折）**（topic 394822）——`../../intel/godaddy-microbusiness-density-forecasting/bodies/394822_img/01.jpg`

*读图结论*：GAP-2 模型在 TS=26..38 → TS=29..40 的 12 个验证折上逐折 SMAPE 2.14–2.655，总 CV 2.343；选择口径（population 0.7 分位、density>0.5、黑名单，1693 县）+ Last Value 拼接预测——**面板时序 CV 的完整设计图**。

## 10. 对既有笔记/playbook 的修订点

1. `notes/tabular/godaddy-microbusiness-density-forecasting.md` 升级：补齐 8 节作者/票数；方案谱系扩为 6 方案对照矩阵；新增倍率建模、census 口径修正、探针机制与伦理、小县分流、目标展平、图证与失败学。
2. `playbook/tabular.md`（面板时序节）增补：
   - **相对指标 → 倍率/比值/年化率目标 + 连乘还原**；
   - **口径审计清单**（分母/统计口径变更、方法学跳变、异常县）；
   - **县/实体规模分流**（小实体 last value + 取整，大实体建模）；
   - **榜单探针的公式化灵敏度**与"数据质量优先于探针"的纪律。
3. `playbook/00-通用方法论.md` 增补："**先修评测口径，再修模型**"（census 换分母类陷阱）与"**探针是信息交易**"（用提交次数购买隐藏标签，可靠性随数据质量波动）。

## 11. 出处

- 线性回归基线（Chris Deotte，196 票）：https://www.kaggle.com/competitions/godaddy-microbusiness-density-forecasting/discussion/373099
- 基线修正（Chris Deotte，141 票）：https://www.kaggle.com/competitions/godaddy-microbusiness-density-forecasting/discussion/389215
- 3rd 倍率 GRU（84 票）：https://www.kaggle.com/competitions/godaddy-microbusiness-density-forecasting/discussion/418287
- 1st（@kaggleqrdl，48 票）：https://www.kaggle.com/competitions/godaddy-microbusiness-density-forecasting/discussion/395131
- Giba RAPIDS SVR（36 票）：https://www.kaggle.com/competitions/godaddy-microbusiness-density-forecasting/discussion/395011
- 6th 目标展平（24 票）：https://www.kaggle.com/competitions/godaddy-microbusiness-density-forecasting/discussion/417821
- Hugo 复盘（24 票）：https://www.kaggle.com/competitions/godaddy-microbusiness-density-forecasting/discussion/394822
- 2nd 数据清洗（Daniel Phalen，19 票）：https://www.kaggle.com/competitions/godaddy-microbusiness-density-forecasting/discussion/395264
- 未收录缺口（登记备查）：17 条 write-up 标记中的其余条目
