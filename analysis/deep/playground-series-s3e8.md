# Playground Series S3E8（宝石价格预测）轻量深读（Tier B）

> 赛事：Playground ｜ 主题 tabular（钻石/宝石回归，RMSE）｜ 734 队 ｜ 标准赛 ｜ 指标：RMSE
> 材料基础：`digests/playground-series-s3e8.md`（6 篇正文：8th 392860 / 2nd 392828 / 3rd 392824 / ChatGPT 特征 389472 / 几何特征 389207 / 6th 392820；49 条主题索引）+ 7 张归档图
> 轻读时间：2026-10（Tier B B16）

## 1. 一句话重述与数字账

预测宝石（钻石）价格（RMSE）。本场的经验集中在两处：①**几何与有序类别特征**——x/y/z 是长/宽/高，衍生体积/密度/表面积/比例；cut/clarity/color 本质是**有序数值量表**，当类别处理反而更差；②**"人工估价师"式后处理**——8th 按（carat 窗 × cut × clarity × color）分组，把测试预测裁剪到训练组的分位上/下界（Q3+1.5·IQR 上界 +0.2，下界裁剪再 +1.1），直接把成绩推到前 10。2nd 则用 1816 个模型的两级栈拿第 2，并警告"重复行 exploit 公榜涨、私榜跌"。

| 关键数字 | 值 | 来源 |
| --- | --- | --- |
| 8th（392860） | 先"修离群值"→ CV 大涨但 LB 变差（发现模型本来就会压缩离群）；改做**分组合法性裁剪**：按 carat 滑窗（0.15）× cut × clarity × color 分组（>5 条记录），预测超过上界 → `Q3+1.5·IQR`（+0.2 LB）；预测低于组内训练最小值 → 抬到最小值（**再 +1.1 LB，直接进前 10**） | 392860 |
| 2nd（392828） | 两级栈共 **1816 个模型**（L1 1709 个 XGB/CAT/LGBM/Ridge + L2 105 个 Ridge/blend/NN）；L1 选择用"CV 阈值从 574 逐 0.1 下探"，最优 cutoff **572.6**，L2 用 Ridge；FE 贡献 **-1.5 CV**（cut/clarity/color 当有序数值 + 长宽比）、原数据 **-1.6 CV**；**重复行 exploit：公榜 -0.05 但私榜 +0.1 → 最终放弃** | 392828 |
| 3rd（392824） | 用尽量多的特征组合；自写"逐列剔除"特征选择，并**同时盯 RMSE 与折间标准差**（容忍度：+0.015 RMSE 换 -0.01 std），把平均 std 从 4.5 降到 3.8；Optuna（1000 轮/lr 0.1）后再拉长到 10000 轮/lr 0.01（ESR 300）；XGB/LGB/CAT 在多个数据集上训练并取 10 seed 平均 | 392824 |
| ChatGPT 特征（389472） | 57 票：体积 `x*y*z`、密度 `carat/volume`、台面百分比、深度百分比、对称性、表面积、深度/台面比；并给出"先让 ChatGPT 解释领域 → 要求数学衍生 → 要求代码"的提示词模板 | 389472 |
| 几何特征（389207） | 38 票：确认 x/y/z = 长/宽/高；体积、表面积、密度、三轴比例、标准差等；3D 散点显示 x/y/z 与价格近似线性 | 389207 |
| 6th（392820） | 3 天、8 次提交拿第 6：AutoGluon（8 折 1 层栈，LGB/CAT/XGB/RF/NNTorch/NNFastAI + 伪标签版本，约 13h）+ AutoXGB（24h HPO），按 CV 加权集成；两个数据集都用 | 392820 |

## 2. 逐方案对照矩阵

| 维度 | 8th | 2nd | 3rd | 6th |
| --- | --- | --- | --- | --- |
| 核心 | 分组分位裁剪 | 1816 模型两级栈 | 多数据集 + 多 seed | AutoGluon/AutoXGB |
| FE | 几何 + 有序类别 | cut/clarity/color 有序 + 长宽比 | 大量特征组合 | 公开方案 |
| 后处理 | **上/下界裁剪（+1.3）** | 放弃重复行 exploit | 以 std 为选择目标 | 加权集成 |
| 结果 | 8th | 2nd | 3rd | 6th |

## 3. 共识、分歧与裁决

### 共识一：几何衍生 + 有序类别数值化是核心 FE（2nd/3rd/389472/389207；置信度中高）

2nd 的 FE 对比图显示 Clarity FE 576.22 vs One-Hot 578.15（差约 1.9）；体积/密度/比例被多方采用。**裁决**：物理量纲数据先做几何衍生；有序类别保持数值序，不要 one-hot。置信度：中高。

### 事件：分组合法性裁剪是本届最大后处理增益（8th；置信度中高）

用训练组的分位上下界约束测试预测（上界 +0.2、下界 +1.1），把"估价师常识"注入提交；作者还发现"修数据"不如"修预测"。**裁决**：目标有分组合理区间时，对预测做分组截断比改训练数据更有效。置信度：中高。

### 分歧：重复行/原数据利用（2nd vs 8th/3rd；置信度中高）

2nd 实测重复行 exploit 公榜涨 0.05、私榜跌 0.1，最终放弃；原数据在 2nd 手里 -1.6 CV；8th/3rd 也都在处理原始/重复数据。**裁决**：原数据可入训练，但"用原数据价格覆盖测试重复行"是过拟合公榜的陷阱。置信度：中高。

### 共识二：大池 + 阈值递进选择 + Ridge 二级栈是稳健结构（2nd、3rd、6th；置信度中）

2nd 的 L1 cutoff 572.6、3rd 的多数据集多 seed、6th 的 AutoGluon 8 折栈都指向同一形态。**裁决**：中大规模数据上，模型池要大到能"筛出稳定子集"。置信度：中。

### 事件：CV 与折间 std 的双目标选择（3rd；置信度中）

3rd 用"RMSE + std"双目标做特征剔除，明确愿意为更低的方差牺牲一点 RMSE。**裁决**：当 CV-LB 噪声大时，把稳定性作为显式目标。置信度：中。

## 4. 证据分级

| 断言 | 等级 | 说明 |
| --- | --- | --- |
| 8th 的分组裁剪与增益 | 自述 + 多张图 | 中高 |
| 2nd 的 1816 模型与重复行对照 | 自述（含 FE 对比图） | 高 |
| 3rd 的双目标选择流程 | 自述 | 中高 |
| ChatGPT/几何特征清单 | 高票帖 + 可复现代码 | 中高 |
| 6th 的 AutoGluon/AutoXGB | 自述 | 中 |

## 5. 悬案与缺口（登记）

- 1st（392926）未收录正文；
- 8th 的裁剪阈值为经验值，缺少系统灵敏度分析；
- 原始数据与重复行的最优处理未定论；
- **图证缺口**：无（7 张图，本深读内嵌 2 张）。

## 6. 图表证据

![修离群后的训练分布](../../intel/playground-series-s3e8/bodies/392860_img/03.png)

**图 1**（topic 392860，8th）：price_per_carat vs carat（修离群后，按 cut/clarity/color 着色）——清除了与原始数据差异巨大的红框区域，为分组裁剪提供合法性区间。

![FE 变体对比](../../intel/playground-series-s3e8/bodies/392828_img/01.png)

**图 2**（topic 392828，2nd）：未调参 LGBM 上的 RMSE 对比——Clarity FE 576.22 最好，One-Hot 578.15 最差，验证"有序类别数值化 > one-hot"。

## 7. 出处

- 8th（26 票 / 7 评论）：https://www.kaggle.com/competitions/playground-series-s3e8/discussion/392860
- 2nd（27 票 / 10 评论）：https://www.kaggle.com/competitions/playground-series-s3e8/discussion/392828
- 3rd（26 票 / 11 评论）：https://www.kaggle.com/competitions/playground-series-s3e8/discussion/392824
- ChatGPT 特征（57 票 / 28 评论）：https://www.kaggle.com/competitions/playground-series-s3e8/discussion/389472
- 几何特征（38 票 / 10 评论）：https://www.kaggle.com/competitions/playground-series-s3e8/discussion/389207
- 6th AutoGluon+AutoXGB（18 票 / 3 评论）：https://www.kaggle.com/competitions/playground-series-s3e8/discussion/392820
- 4Cs 概念（28 票 / 5 评论）：https://www.kaggle.com/competitions/playground-series-s3e8/discussion/389465
- 帮助想法汇编（26 票 / 8 评论）：https://www.kaggle.com/competitions/playground-series-s3e8/discussion/390882
- 有序数值化（18 票 / 2 评论）：https://www.kaggle.com/competitions/playground-series-s3e8/discussion/389174
- 1st（15 票，未收录正文）：https://www.kaggle.com/competitions/playground-series-s3e8/discussion/392926
