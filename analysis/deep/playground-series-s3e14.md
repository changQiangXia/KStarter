# Playground Series S3E14（野生蓝莓产量预测）轻量深读（Tier B）

> 赛事：Playground ｜ 主题 tabular（农业回归，MAE）｜ 1875 队 ｜ 标准赛 ｜ 指标：Mean Absolute Error
> 材料基础：`digests/playground-series-s3e14.md`（6 篇正文：1st 410627 / 4th 410639 / 13th 410652 / 189th 410700 / 后处理技巧 407327 / 3rd 410787；71 条主题索引）+ 10 张归档图
> 轻读时间：2026-10（Tier B B15）

## 1. 一句话重述与数字账

预测野生蓝莓产量（MAE）。本场的两个决定性事实：①目标只有 **776 个唯一值**（15,289 行训练），**把预测吸附到最近的唯一目标值**即可 +0.3 MAE（80 票的 post-processing trick，全场基本都在用）；②`fruitset/fruitmass/seeds` 与目标近似线性且能在原始数据里查到确定映射——1st 由此做出"**定点修正 + 风险分级提交**"的夺冠组合，其中 `fruitset=0.335339 & fruitmass=0.233554 → yield=1945.53061` 是最大的单点金矿。

| 关键数字 | 值 | 来源 |
| --- | --- | --- |
| 1st（410627） | 发现异常固定映射（如 fruitset 0.335339 + fruitmass 0.233554 → 1945.53061），**自动遍历 fruitset/fruitmass 的共同取值（覆盖测试集 2073 条）**并用原始数据里查到的 yield 覆盖预测（"核弹"）；随后是**风险瀑布**式提交分级：Serious Incident（>4 条命中 >3）→ Zone With Consequences（>3>2）→ Dangerous Zone（>2>1）→ Ground Zero（>1>0，未提交，私榜 327.2715 最好）；8 个一级 OOF + LAD 回归融合（LAD vs scipy.minimize 对比）；最终故意选两份最高风险提交（公榜最高=私榜最高）；自述 5 个月打磨、多次被洗牌教训 | 410627 |
| 后处理技巧（407327） | 80 票：训练集只有 776 个唯一目标 → `oof_preds = unique_targets[np.abs(oof_preds - unique_targets).argmin()]`；CV 与 LB 各约 +0.3 MAE | 407327 |
| 4th（410639） | 复现一圈公开 notebook（paddykb FLAML、adaubas LAD/PCA/PLS、tetsutani OptunaWeights、zhukovoleksiy 等）→ 用自研 **hillclimbers** 模块做爬山融合（支持负权重、目标/指标/精度参数）；后处理同时用在 CV 折内与折间；hill climb 把 MAE 从 336.26 降到 335.97 | 410639 |
| 13th（410652） | 2×CatBoost（离散特征当类别）+ 7×LGBM（不同特征集）+ 2×RF（1200 棵树、`oob_score=True`，**用 OOB 当 OOF**）；LADRegression（`fit_intercept=False`）融合；CV 与公榜高度一致 → 只提交 4 次；用 CV 单指标决策 | 410652 |
| 189th（410700） | 零 alpha Ridge（=线性回归）拟合 fruitset/fruitmass/seeds 的 1 主成分 → 残差交给 LGBM/CatBoost（含正/负残差分开建模、多项式特征、one-hot 版本），全程用 LADRegression 无截距融合；自述做法"有点复杂" | 410700 |
| 3rd（410787） | train+原始数据；`fruit_seed = fruitset × seeds`；丢弃 RainingDays 与 AverageOfUpperTRange；标准化；按 fruitset 的折内 TE；4 LGBM + 4 CatBoost + HGB + RF + Huber + PassiveAggressive + KNN，用 OptunaWeights；再与 LAD 栈 | 410787 |
| 社区 | "337 分的一些技巧"（69 票 / 48 评论，adaubas 的 PLS/PCA/LAD）；"快速 FE 想法"（60 票 / 28 评论）；"7th private / 3rd public 的简单集成 + 后处理"（53 票）；蜂/温雨/克隆尺寸子集（27 票）；"合成数据的麻烦"（24 票）；"要不要用完所有列"（22 票）；蜂与蓝莓科普（22 票） | 索引 |

## 2. 逐方案对照矩阵

| 维度 | 1st | 4th | 13th | 3rd |
| --- | --- | --- | --- | --- |
| 核心 | 定点修正 + 风险分级 | hillclimbers 爬山融合 | LAD 融合（OOB 当 OOF） | OptunaWeights + LAD 栈 |
| 后处理 | 吸附 + 原数据覆盖（多档风险） | 折内 + 折间吸附 | 吸附 | 吸附 |
| 特征结构 | fruitset/fruitmass/seeds 线性 | 公开 notebook 派生 | 离散列类别化 | fruit_seed + TE |
| 提交策略 | 故意最高风险两份 | — | 只提交 4 次、信 CV | — |
| 结果 | 1st | 4th | 13th | 3rd |

## 3. 共识、分歧与裁决

### 共识一：吸附到唯一目标值是全场标配（407327 + 所有前排；置信度高）

776 个唯一值 + 高 R²（约 0.83）意味着预测落在真值附近的概率高；吸附几乎无损且至少 +0.3 MAE。**裁决**：离散目标回归赛先做"唯一值吸附"体检。置信度：高。

### 共识二：fruitset/fruitmass/seeds 的线性结构 + LAD 融合是本场的两种主武器（1st、4th、13th、189th、adaubas 帖；置信度中高）

PLS/PCA 线性投影反复出现；LADRegression（最小绝对偏差，天然匹配 MAE）被 1st/13th/189th/3rd 采用。**裁决**：MAE 赛优先用 LAD 类融合器；目标近似线性时先做投影/查表。置信度：中高。

### 事件一：定点修正的收益与风险（1st；置信度中高）

同一对本应唯一的 (fruitset, fruitmass) 在合成数据里被复制到多行；1st 用原始数据值覆盖，收益以"整数"计，并用风险分级控制敞口。**裁决**：这类"查表修正"是高收益高风险动作，必须配提交分级与验证。置信度：中高。

### 事件二：公开 notebook 生态与工具化（4th、13th、社区；置信度中高）

4th 全部一级模型来自公开 notebook，用自研 hillclimbers 只做融合；13th 也是公开+自研混合。**裁决**：当公开基模质量高时，差异化在融合器与后处理。置信度：中高。

### 技巧：OOB 当 OOF（13th；置信度中）

RF 的 `oob_score=True` 让 1200 棵树的模型在 10 分钟内产出可用 OOF。**裁决**：对慢模型这是低成本加入集成的路径；需确认 OOB 与 CV 口径一致性。置信度：中。

## 4. 证据分级

| 断言 | 等级 | 说明 |
| --- | --- | --- |
| 1st 的定点修正、风险分级与 pipeline 图 | 自述 + 7 张图 | 高 |
| 后处理吸附 +0.3 MAE | 自述 + 80 票社区验证 | 高 |
| 4th 的 hillclimbers 与公开 notebook 清单 | 自述 + 代码 | 中高 |
| 13th 的 OOB-as-OOF 与 LAD | 自述 | 中 |
| 189th 的残差分解 | 自述 | 中 |
| 3rd 的 OptunaWeights 配方 | 自述 | 中 |

## 5. 悬案与缺口（登记）

- #2（private）、#5–#12、#14+ 方案未收录；
- 定点修正对私榜风险的精确评估未量化（作者用分级近似）；
- PLS/PCA 与 LAD 的对照细节在 adaubas 帖中未细读；
- **图证缺口**：无（10 张图，本深读内嵌 2 张）。

## 6. 图表证据

![1st 的完整模型管线](../../intel/playground-series-s3e14/bodies/410627_img/02.png)

**图 1**（topic 410627，1st）：12 个公开 notebook 的一级 OOF → LAD/scipy 融合（权重 0.00–0.37）→ 后处理 Phase 1 → 风险分档（Zone With Consequences / Dangerous Zone / Ground Zero）→ 最终提交（Ground Zero 私榜 327.2715 未提交）。

![hill climbing 的 MAE 曲线](../../intel/playground-series-s3e14/bodies/410639_img/02.png)

**图 2**（topic 410639，4th）：hillclimbers 的 CV MAE vs 模型数——第 1 个模型 336.26，5 个模型降到 335.97（前 3 个贡献最大）。

## 7. 出处

- 1st（133 票 / 57 评论）：https://www.kaggle.com/competitions/playground-series-s3e14/discussion/410627
- 后处理技巧（80 票 / 18 评论）：https://www.kaggle.com/competitions/playground-series-s3e14/discussion/407327
- 4th hillclimbers（50 票 / 16 评论）：https://www.kaggle.com/competitions/playground-series-s3e14/discussion/410639
- 13th（21 票 / 17 评论）：https://www.kaggle.com/competitions/playground-series-s3e14/discussion/410652
- 189th（10 票）：https://www.kaggle.com/competitions/playground-series-s3e14/discussion/410700
- 3rd（12 票）：https://www.kaggle.com/competitions/playground-series-s3e14/discussion/410787
- 337 分技巧（69 票 / 48 评论）：https://www.kaggle.com/competitions/playground-series-s3e14/discussion/409242
- 快速 FE 想法（60 票 / 28 评论）：https://www.kaggle.com/competitions/playground-series-s3e14/discussion/406448
- 简单集成 + 后处理（53 票 / 13 评论）：https://www.kaggle.com/competitions/playground-series-s3e14/discussion/410666
