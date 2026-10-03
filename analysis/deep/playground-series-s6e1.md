# Playground Series S6E1（学生考试成绩）轻量深读（Tier B）

> 赛事：Playground ｜ 主题 tabular（教育，合成数据回归）｜ 4317 队 ｜ 标准赛 ｜ 指标：RMSE（≈8.57）
> 材料基础：`digests/playground-series-s6e1.md`（6 篇正文：1st 671371 / 2nd 671261 / 6th 671328 / 13th 671? / EDA 665965 / 伪标签 615 行处；80 条主题索引）+ 4 张图
> 轻读时间：2026-10（Tier B B08 收官）

## 1. 一句话重述与数字账

从学习习惯类特征预测考试成绩（RMSE≈8.57）。真正的考点是**"逆向合成公式 + 大集成"**：数据几乎由线性公式生成（图 1），社区用 GP/线性回归把生成式恢复到 RMSE≈8.97 的水平；随后是"几十到两百个模型的 Ridge 集成"，而 NN（尤其 TabM）在本场首次系统性地胜过 GBDT。

| 关键数字 | 值 | 来源 |
| --- | --- | --- |
| 1st（671371，49 票） | 两套特征集：① **NN 友好**（周期特征 + 恢复出的生成公式 + 数值列的类别副本 + 数字特征 + 组合特征与目标编码的 mean/std/skew）② **GBDT 友好**（生成公式 + 序数映射 + 类别副本 + 数字特征）；**专注做强单模**（最佳单模可排第 7）；单模分数：RealMLP 8.58742（CV）/8.58005（PB）、XGB 8.5948/8.5925、TabM 8.5965/8.5928、CatBoost、DeepTables、LGBM-dart…；**最终 190 个模型用 Ridge 集成**（HC/AutoGluon/CatBoost 集成器都更差）→ CV 8.56634 / LB 8.53096 / **PB 8.57273（含后处理）** | 671371 |
| 2nd（671261，55 票） | 主题即"**NN 有时胜过 GBM**"：TabM 单模"远远最好"（同样的数据下 XGB/CatBoost 都不如）；75 模型集成中**除 7 个外全是 NN**（其中 60 个 TabM）；做法：170–700 特征的各种组合 × 6 组超参 + **对 GP 公式的残差建模**（两条公式单独 RMSE 8.9703 / 8.9741）；总结"GBM 对 NN 没有绝对优势" | 671261 |
| 6th（671328） | "特征工程本场基本无效"（最佳单模 8.5950 CV），但**为集成服务有效**：训练 200+ 个 XGB（各种"古怪"特征），并混入公开 notebook 的伪标签/hillclimber/TabM/AutoGluon；**核心经验：永远保存 OOF、永远用同一 KFold 与 seed**——这样即使特征工程失败，事后集成仍可用；把 **Linear Regression 当"最强特征"**（树只看序，线性模型能吃 ^2/log 等单调变换）；三层嵌套 CV 防泄漏 | 671328 |
| 13th（"DiversitySlop"，173 模型） | 173 模型 + hill climbing + Ridge；**最大痛点=分数范围偏差**（低分被高估 10+、高分被低估 8+）→ 自定义 **target 相关的加权 MSE**（y≤27 权重 8、27<y≤35 权重 4、84≤y<92 权重 3、y≥92 权重 6，基线 2）；自评"必须想尽办法造多样性，hill climbing/stacking 才有用" | 671285 |
| 社区 | "**基础 EDA 显示大量线性关系**"（78 票，图 1）、"从往届 Playground 提炼的有效策略"（62 票）、"**恢复原始数据模型**"（44 票）、"**用 GBDT 方式做双重截尾 Tobit 模型**"（25 票，指出标签被截尾）、"盲混 vs 超越盲混"（22 票） | 社区 |

## 2. 逐方案对照矩阵

| 维度 | 1st | 2nd | 6th |
| --- | --- | --- | --- |
| 单模策略 | 做强单模（8 个族） | **TabM 为主（60 个）** | 200+ 个 XGB（特征各异） |
| 特征 | 两套特征集（NN/GBDT 分开） | 170–700 特征 × 6 超参 + GP 残差 | "古怪"特征 + 线性回归 |
| 集成 | **Ridge（190 模型）** | 75 模型（68 NN） | 事后大杂烩（含公开 notebook） |
| 关键纪律 | 后处理 | 残差建模 | **保存 OOF + 固定 KFold/seed + 三层嵌套 CV** |

## 3. 共识、分歧与裁决

### 共识一：先恢复生成式，再谈模型（社区 + 1st/2nd/6th）

EDA 帖指出大量线性关系（图 1）；"恢复原始数据模型"帖（44 票）与 2nd 的两条 GP 公式（RMSE≈8.97）都指向同一个生成式；1st/6th 都把该公式当核心特征/残差基线。**裁决**：合成数据赛的第一动作是"用线性/GP 恢复生成式"，把它作为特征、baseline 与残差目标。置信度：高。

### 共识二：NN 在本场不弱于 GBM（1st/2nd）

1st 的 RealMLP 是最佳单模（8.5874 CV）；2nd 的 TabM 单模"远远最好"，75 模型里 68 个是 NN。**裁决**：tabular 赛不应默认 GBM 优先；RealMLP/TabM 这一代 NN 值得与 GBDT 平起平坐地投入。置信度：高（两支队独立）。

### 共识三：特征工程的价值转移到"多样性"（6th + 1st）

6th 明说单模上 FE 失败但"对集成有效"；1st 也用两套特征集分别喂 NN/GBDT。**裁决**：FE 的产出应被视为"给集成池增加不同错误结构"，单模指标不是唯一评判。置信度：高。

### 分歧一：少量强模型 vs 海量模型

1st"少而强"（190 个但重点是强单模）；6th"多而杂"（200+ XGB + 公开 notebook）。**裁决**：两者都进前 6；海量模型的可行性依赖"统一的 KFold/seed + 保存 OOF"这一纪律，否则无法事后集成。置信度：中高。

### 事件：Tobit/截尾与指标细节（25 票帖）

社区指出目标存在截尾，可用"GBDT 版双重截尾 Tobit"建模。**裁决**：回归题要看标签的边界结构（截尾/离散化），它可能与生成式同等重要。置信度：中。

## 4. 证据分级

| 断言 | 等级 | 说明 |
| --- | --- | --- |
| 1st 的 190 模型 Ridge 与单模分数表 | 自述 + 表 | 高 |
| 2nd 的 TabM 优势与 GP 公式 | 自述 + 公式（可复算） | 高 |
| 6th 的 OOF/KFold 纪律与 LR 特征 | 自述 + 代码 | 中高 |
| 线性关系 EDA | 图 + 数据 | 高 |
| Tobit/截尾 | 社区帖 | 中 |

## 5. 悬案与缺口（登记）

- 3rd–5th/7th–12th 与 13th 的方案未细读；"往届 Playground 策略"（62 票）与"盲混之争"（23 票 / 39 评论）未细读；
- 1st 的"公式"未在材料中完整展开（只给了引用）；
- 2nd 的 75 模型清单未逐项列出；
- 归档 4 图：EDA 的线性关系图（图 1）与 6th 的 3 张图为图证。

## 6. 图表证据

![各特征与平均成绩的关系](../../intel/playground-series-s6e1/bodies/665965_img/01.png)

**图 1**（topic 665965）：11 个特征的分布与"平均 exam_score"曲线——`study_hours`（40→80+）、`class_attendance`（50→75）、`sleep_hours`、`sleep_quality`（60→68）、`facility_rating`（58→66）等几乎都是**单调近线性**；`course`/`study_method` 等类别列也呈明显阶梯。这张图直接解释了本场"恢复公式 + 线性回归当特征"的流行做法。

## 7. 出处

- 1st（49 票）：https://www.kaggle.com/competitions/playground-series-s6e1/discussion/671371
- 2nd（55 票）：https://www.kaggle.com/competitions/playground-series-s6e1/discussion/671261
- 6th（21 票）：https://www.kaggle.com/competitions/playground-series-s6e1/discussion/671328
- EDA（78 票）：https://www.kaggle.com/competitions/playground-series-s6e1/discussion/665965
- 恢复原始数据模型（44 票）：https://www.kaggle.com/competitions/playground-series-s6e1/discussion/665915
- Tobit 截尾（25 票）：https://www.kaggle.com/competitions/playground-series-s6e1/discussion/667296
