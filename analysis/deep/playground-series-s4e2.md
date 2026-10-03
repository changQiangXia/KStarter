# Playground Series S4E2（肥胖风险多分类）轻量深读（Tier B）

> 赛事：Playground ｜ 主题 tabular（6 类肥胖等级分类，合成数据）｜ 3587 队 ｜ 标准赛（20/80 公私划分）｜ 指标：Accuracy
> 材料基础：`digests/playground-series-s4e2.md`（6 篇正文：4th 480939 / 2nd 481062 / 6th 480795 / 24th 480927 / 70th 480787 / 启动资源 472392；80 条主题索引）+ 0 张归档图
> 轻读时间：2026-10（Tier B B12）

## 1. 一句话重述与数字账

6 类肥胖等级分类（Accuracy 指标），数据量小、公私榜 20/80 划分，**大洗牌是主旋律**（4th 本人移动了 255 名）。本场的经验高度一致：**特征工程几乎无效、基础编码 + XGB/LGBM 集成是主配方；信任 CV、别追公开榜；概率阈值/指标优化是独立增益**。2nd 甚至把"加原始数据 4 次 + 只用 XGB/LGBM + 概率阈值化"做到亚军，而堆叠与伪标签在 2nd 手里全部无效、在 4th 手里却是第 4 名。

| 关键数字 | 值 | 来源 |
| --- | --- | --- |
| 4th（480939） | 洗牌移动 **255 名**；XGB 元学习器堆叠（输入 = AutoXGB/AutoGluon + LightAutoML + 自训 XGB/LGBM 的概率）；AutoGluon 集成权重 CatBoost_r9 0.363 / LGBM_r131 0.253 / XGB×2 0.099 / NN 0.077…；训练用 log_loss、最终按 Accuracy 优化；提交 = 9 份预测**逐行取最大类**；原始数据拼接 | 480939 |
| 2nd（481062） | 原始数据被加入 **4 次**；5 折 HPO → 20 折最终训练；只用 XGB+LGBM；z-score + one-hot；概率阈值化（CV 平均权重）；自述"CV 升、LB 降 = 过拟合点，此时要靠集成" | 481062 |
| 6th（480795） | 经典树集成 + 1 个 NN（Optuna 调参，提供不同错误模式）+ 网格搜索集成权重；策略 = "把公榜当一折"，只提交 CV 与公榜都不偏离的模型 | 480795 |
| 24th（480927） | XGB（MEstimate 编码）+ LGBM（one-hot）集成；10 折分层；主要增益来自权重微调；明确"不加特征（BMI 等无效）"；"Trust CV over LB" + MLflow 记录 | 480927 |
| 70th（480787） | "trust CV is all you need"：CV 0.918（提交的是 0.916 的版本）；论证——合成竞赛 train/test 同分布可信 CV，时序/小样本不可 | 480787 |
| 社区 | 启动资源合集 91 票；"BMI has flaws" 41 票；CALC 缺类别 33 票 / 32 评论；"multiclass vs multiclass_ova 精度大涨" 30 票 / 32 评论；"标签有序但分类器不建模顺序" 19 票 / 28 评论；"种子是超级食物" 15 票 / 23 评论；洗牌分析 37 票 | 索引 |

## 2. 逐方案对照矩阵

| 维度 | 4th | 2nd | 6th | 24th | 70th |
| --- | --- | --- | --- | --- | --- |
| 主模型 | XGB 元堆叠（多来源概率） | XGB+LGBM | 树集成 + NN | XGB+LGBM | 公开 notebook 派生 |
| 特征 | 分箱 + log1p + 多项式 + one-hot + 原始数据 | 基础 z-score + one-hot（不加 FE） | 原特征 | 原特征（无 FE） | — |
| 原始数据 | 拼接 | **加入 4 次** | — | — | — |
| 折数 | — | 5 → 20 折 | — | 10 折 | — |
| 关键动作 | 伪标签 + 9 份行级最大类 + Accuracy 优化 | 概率阈值化 | 权重网格 + NN 稳定器 | 权重微调 | 只信 CV |
| 结果 | 4th | 2nd | 6th | 24th | 70th |

## 3. 共识、分歧与裁决

### 共识一：本场特征工程基本无效，基础编码 + 树集成是主配方（2nd、24th、6th；置信度高）

2nd 明确列出一串"没用的东西"：伪标签、AutoML（AutoGluon/FLAML/auto-sklearn）、特征工程（连 BMI 特征都无效）、ordinal 编码、sklearn stacking、加权集成；24th 同样"不加特征"；6th 只补了一个 NN。**裁决**：该数据集（合成肥胖数据）在原始特征空间里已包含几乎全部可用信号，加深 FE 只会过拟合 CV。置信度：高。

### 共识二：小数据 + 20/80 划分 → 必须信 CV、别追公榜（4th、2nd、6th、24th、70th；置信度高）

4th 洗牌 255 名；2nd 说"CV 升 LB 降就是过拟合点"；6th 把公榜当一折；24th 与 70th 直接喊"trust CV"。**裁决**：在此类 Playground 上，提交选择应以 CV（或 CV 与公榜的一致区间）为准，公榜微差是噪声。置信度：高。

### 共识三：原始数据拼接有稳定增益（4th、2nd；置信度中高）

2nd 的最佳方案把原始数据加了 4 次；4th 也把竞赛数据与原始数据拼接去重。**裁决**：合成数据 + 少量原始数据的组合优于纯合成；但重复次数属于超参，需 CV 验证。置信度：中高（两方自述）。

### 分歧一：堆叠与伪标签到底有没有用（4th vs 2nd；置信度中）

4th 用"XGB 元堆叠 + 伪标签"拿第 4；2nd 说 stacking 与伪标签都没有提升。**裁决**：在如此小的数据集上，堆叠/伪标签的收益高方差、强依赖实现与折数，不能当作稳定结论；两者都能进前列说明"基础模型 + 选择纪律"才是共同点。置信度：中（分歧保留）。

### 共识四：Accuracy 类的概率后处理是独立增益（4th、2nd；置信度中高）

4th 用公开的 Accuracy 优化代码（训练 log_loss、按概率优化阈值）；2nd 也用 CV 平均权重的概率阈值化。**裁决**：多分类 Accuracy 赛的"概率 → 决策"环节值得单独优化。置信度：中高。

## 4. 证据分级

| 断言 | 等级 | 说明 |
| --- | --- | --- |
| 4th 的堆叠配置与 AutoGluon 权重 | 自述（含权重清单） | 中高 |
| 2nd 的"有用/没用"清单 | 自述（结构完整） | 中高 |
| 6th/24th/70th 的 CV 优先策略 | 自述 | 中 |
| 洗牌 255 名与 20/80 划分 | 自述 + 社区洗牌分析帖 | 中高 |
| 社区话题（BMI/CALC/OVA/有序标签） | 高票帖 | 中高 |

## 5. 悬案与缺口（登记）

- 1st/3rd/5th 方案未收录；
- "multiclass vs multiclass_ova"（30 票 / 32 评论）的具体增益幅度未细读；
- "标签有序性"的处理（ordinal 建模）无成功案例；
- 种子效应（15 票 / 23 评论）与洗牌的关系未量化；
- **图证缺口**：本场归档 0 图，无直方图/权重图可内嵌。

## 6. 图表证据

无可用图证（本场归档 0 图，图证缺口已登记）。

## 7. 出处

- 4th 堆叠 + 伪标签（76 票 / 28 评论）：https://www.kaggle.com/competitions/playground-series-s4e2/discussion/480939
- 2nd 两模型 + 阈值化（12 票）：https://www.kaggle.com/competitions/playground-series-s4e2/discussion/481062
- 6th 树 + NN（27 票）：https://www.kaggle.com/competitions/playground-series-s4e2/discussion/480795
- 24th 简单集成（14 票）：https://www.kaggle.com/competitions/playground-series-s4e2/discussion/480927
- 70th trust CV（9 票）：https://www.kaggle.com/competitions/playground-series-s4e2/discussion/480787
- 启动资源（91 票 / 40 评论）：https://www.kaggle.com/competitions/playground-series-s4e2/discussion/472392
- BMI has flaws（41 票）：https://www.kaggle.com/competitions/playground-series-s4e2/discussion/476939
- multiclass vs OVA（30 票 / 32 评论）：https://www.kaggle.com/competitions/playground-series-s4e2/discussion/477862
- 洗牌分析（37 票）：https://www.kaggle.com/competitions/playground-series-s4e2/discussion/480792
- 有序标签讨论（19 票 / 28 评论）：https://www.kaggle.com/competitions/playground-series-s4e2/discussion/475438
