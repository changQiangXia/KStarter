# Playground Series S6E7（学生健康风险）轻量深读（Tier B）

> 赛事：Playground ｜ 主题 tabular（3 分类，Balanced Accuracy）｜ 3355 队 ｜ 标准赛 ｜ 指标：Balanced Accuracy
> 材料基础：`digests/playground-series-s6e7.md`（6 篇正文：4th 732487 / 2nd 731904 / 29th 561 行处 / 135th 669 行处 / 生成模型帖 770 行处 / S6E7 方案 814 行处；71 条主题索引）+ 4 张图
> 轻读时间：2026-10（Tier B B10 收官）

## 1. 一句话重述与数字账

预测学生健康风险三分类（at-risk 85.87% / fit 5.77% / unhealthy 8.36%），指标是 Balanced Accuracy（各类召回的平均）。真正的考点是**"决策规则必须与指标对齐"**：4th 只把 `argmax(p)` 换成 `argmax(p/class_prior)` 就让 OOF BA 从 0.892 跳到 **0.951**，并因此从公榜第 414 逆转到私榜第 4（分数只差 -0.0001，名次涨了 410）。

| 关键数字 | 值 | 来源 |
| --- | --- | --- |
| 4th（732487，#414 → #4） | 模型：**FT-Transformer，7 折 × 每折 4 个独立初始化成员**；特征：13 个原始 + **39 个"多分类精确值目标编码"**（所有目标派生特征只在训练折内拟合）；**最大增益 = 把决策从 `argmax(p)` 改为 `argmax(p / class_prior)`：OOF BA 0.89187 → 0.95063**；最终公榜 0.95094（414 名）→ 私榜 0.95084（4 名）；结论："**让决策规则对齐指标，然后信任干净的 OOF、不要追公榜的微小差异**" | 732487 |
| 2nd（731904） | 18 个基模型（LGBM/XGB/CatBoost/FT-Transformer/RealMLP/HGBC 的多样实现）；两步优化：① **单纯形约束的多分类权重优化（SLSQP）**：优化 18×3=54 个参数（每类内归一化），直接最小化 OOF LogLoss——**0.105495（等权）→ 0.086310**；权重显示 FT-Transformer 主导（三类分别为 71.81%/62.45%/50.28%），XGBoost-OvR 在 Class 2 占 45.59%；② **不做非线性元学习**，只用直接线性混合（避免在 OOF 元数据上过拟合）；③ **类乘子用 Nelder-Mead 在完整 OOF 上调**（`C0=0.1240、C1=1.4998、C2=1.2502`）并在测试集原样应用（不使用任何测试标签或榜面反馈）——BA 从 0.889132 提升到 **0.950737** | 731904 |
| 29th/135th | FT-Transformer + 精确值目标编码（29th）；135th 为"第一次完整参赛"的复盘 | 561/669 行处 |
| 社区侧 | "Trust your CV：目前的 CV-LB 关系"（27 票）、"**Rank11 approach**"（22 票，含 stacker 剪枝轨迹图）、"9 个 notebook 的研究轨迹"（19 票）、"**一个配置从 0.903 到 0.950**"（12 票）、"LightGBM+Optuna 管线 0.95014"（8 票）、"**几乎穷尽的 S6E7 阅读：为什么 86% 准确率只得 0.33**"（8 票）、"原始数据集的合理生成模型"（770 行处） | 社区 |

## 2. 逐方案对照矩阵

| 维度 | 4th | 2nd |
| --- | --- | --- |
| 模型 | FT-Transformer（7 折×4 成员） | 18 个基模型（含 FT-Transformer/RealMLP/HGBC） |
| 特征 | 13 原始 + 39 精确值目标编码（折内拟合） | — |
| 融合 | 单族 | **SLSQP 单纯形约束的类特定权重（54 参数，最小化 OOF LogLoss）** |
| 决策规则 | **`argmax(p/class_prior)`**（BA 0.892→0.951） | **Nelder-Mead 类乘子 [0.124, 1.500, 1.250]**（BA 0.889→0.951） |
| 名次 | 私榜 #4 | 私榜 #2 |

## 3. 共识、分歧与裁决

### 共识一：决策规则（先验校正）是本场最大的单点增益（4th/2nd）

4th 除以类先验、2nd 用类乘子——两者本质相同（BA 的最优决策是 `argmax η_c/π_c`）；增益都是 +0.06 级别（0.89→0.95）。**裁决**：类别不均衡 + Balanced Accuracy 的赛题，**必须先做先验校正再谈模型**（与 S4E11/S6E6 的"用 AUC/log-loss 代理"互为补充：那两场说的是训练/验证指标，本场说的是最终决策）。置信度：高。

### 共识二：信任干净的 OOF，不追公榜（4th + 27 票帖）

4th 的 414→4 逆转让"trust OOF"具象化；社区专帖跟踪 CV-LB 关系；2nd 的乘子"只用 OOF、不用任何榜面反馈"。**裁决**：当决策规则对齐指标后，OOF 的排序比公榜前几百名的微小差异更可信。置信度：高。

### 共识三：精确值目标编码 + FT-Transformer 是本场的强组合（4th/29th）

4th 用 39 个多分类精确值目标编码（折内拟合）；29th 也是 FT-Transformer + 精确值 TE。**裁决**：低基数/类别型表格里，"精确值级"的目标编码比分箱/平滑编码更有效（与 S6E9 的多级取整 TE 相映）。置信度：中高。

### 分歧一：融合方式（单族 vs 大规模异构 + 单纯形权重）

4th 用单族 FT-Transformer（7 折×4 成员）并靠决策规则取胜；2nd 用 18 个异构模型 + SLSQP 权重（并把 OOF logloss 从 0.1055 压到 0.0863），但最终 BA 与 4th 相同（0.9507）。**裁决**：在决策规则正确的前提下，异构大融合的边际收益有限；把算力投在"决策层"性价比更高。置信度：中高。

### 事件：公榜"说谎"与排名洗牌（4th 的标题 + 社区多帖）

4th 的公榜 414 → 私榜 4；社区帖"为什么 86% 准确率只得 0.33"（普通准确率与 BA 的极端分歧）。**裁决**：Balanced Accuracy 赛里"高普通准确率"完全可能对应 0.33 的 BA——投票/排名指标必须按类审计。置信度：高。

## 4. 证据分级

| 断言 | 等级 | 说明 |
| --- | --- | --- |
| 4th 的 `p/prior` 增益（0.89187→0.95063）与 414→4 | 自述 + 完整数字 | 高 |
| 2nd 的 SLSQP 权重、logloss 改善与类乘子 | 自述 + 详细参数 + 公开代码 | 高 |
| 精确值目标编码（4th/29th） | 自述 | 中高 |
| "86% 准确率只得 0.33" | 社区帖 | 中高 |
| 原始数据生成模型 | 社区帖（770 行处） | 中 |

## 5. 悬案与缺口（登记）

- 1st/3rd 与 5th–10th 的方案未细读；"Rank11 approach"（22 票）与"9 notebook 研究轨迹"（19 票）未细读；
- 1st 的方案完全未入库（本场最大缺口）；
- 生成模型帖（770 行处）未细读；
- 归档 4 图：Rank11 的 stacker 剪枝轨迹图（图 1）为关键图证。

## 6. 图表证据

![Rank11 的 stacker 剪枝轨迹](../../intel/playground-series-s6e7/bodies/731729_img/01.png)

**图 1**（topic 731729，Rank11 approach）：三层子图——(a) stacker 剪枝过程中"平衡 logloss（蓝）"与"Balanced Accuracy（红）"的轨迹（BA 峰值 0.95093，标注 `C* @step 183 (m=25)`）；(b) 被剪掉成员的 solo CV 分布（橙点 + 滚动中位数）；(c) 正则化系数 `C*` 随剪枝步数的阶梯变化。展示了"融合/剪枝时同时盯 logloss 与目标指标"的实用做法。

## 7. 出处

- 4th（732487）：https://www.kaggle.com/competitions/playground-series-s6e7/discussion/732487
- 2nd（29 票）：https://www.kaggle.com/competitions/playground-series-s6e7/discussion/731904
- Trust your CV（27 票）：https://www.kaggle.com/competitions/playground-series-s6e7/discussion/718258
- Rank11 approach（22 票）：https://www.kaggle.com/competitions/playground-series-s6e7/discussion/731745
- 9 notebook 研究轨迹（19 票）：https://www.kaggle.com/competitions/playground-series-s6e7/discussion/719199
- "为什么 86% 准确率只得 0.33"（8 票）：https://www.kaggle.com/competitions/playground-series-s6e7/discussion/717018
