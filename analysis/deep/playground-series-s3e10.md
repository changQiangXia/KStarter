# Playground Series S3E10（脉冲星识别）轻量深读（Tier B）

> 赛事：Playground ｜ 主题 tabular（天体物理二分类，Log Loss）｜ 807 队 ｜ 标准赛 ｜ 指标：Log Loss
> 材料基础：`digests/playground-series-s3e10.md`（6 篇正文：1st 396345 / 19th 396259 / 十届冠军汇编 394981 / 十届结构化复盘 395484 / 校准模板警告 393073 / 天体物理背景 392834；61 条主题索引）+ 2 张归档图
> 轻读时间：2026-10（Tier B B15）

## 1. 一句话重述与数字账

用射电望远镜的两类统计特征（积分脉冲轮廓与 DM-SNR 曲线的均值/标准差/峰度/偏度等）判断是否为脉冲星（Log Loss）。本场的结论与树模型的直觉相反：**加性模型（GAM）胜过 GBDT**——1st 用 GAM + 两个由 XGB/LASSO 生成的辅助特征夺冠；3rd 是 XGB+LGBM+GAM 的集成；跨十届的冠军复盘也把"Episode 10 的关键 = GAM"写进了结论。同时，本届产出了整个系列最有价值的社区资产之一：**前十届冠军方案的汇编与结构化复盘**。

| 关键数字 | 值 | 来源 |
| --- | --- | --- |
| 1st（396345） | **GAM**（paddykb 风格）+ 两个由 XGB 与 LASSO 生成的辅助特征；自述辅助特征"不那么重要"，去掉只略差；理由：变量少且已是高层特征 → FE 几乎不可能；树只能逼近连续关系；GAM 自带正则与内部 CV，便于自由加入交互/派生特征 | 396345 |
| 19th（396259） | 双模型集成（XGB/LGBM/CAT 加权）；**对 8 个基础特征做全组合/全排列**生成乘、加、比较、除特征；用 ExtraTrees 的 permutation importance 筛选；k-means 分组提升 CV 但公榜无改善 → **未提交（自述本可最佳）**；不用原始数据；只对 train 取整 | 396259 |
| 校准模板警告（393073） | 49 票：Log Loss 赛不要用混淆矩阵/ROC 曲线模板，应画**校准曲线 + 预测直方图**（给出 `CalibrationDisplay.from_predictions` 代码） | 393073 |
| 十届冠军汇编（394981） | 逐届冠军要点：E1 加州房价（地理特征 + AutoGluon）、E2 中风（one-hot + KNN 插补 BMI + 风险因子）、E3 员工流失（风险因子 + 加权集成）、E4 欺诈（不同 CV 策略 + focal loss）、E5 葡萄酒（单 XGB + 回归取整；3rd 公开 notebook 众数）、E6 巴黎房价（三段线性回归 + 分类器定档）、E7 预订取消（重复对标签泄漏）、E8 宝石价格（2 级 stacking）、E9 混凝土（ridge+RF+GBDT 异质集成）、E10 脉冲星（GAM） | 394981 |
| 结构化复盘（395484） | 按数据/FE/CV/建模/集成五块总结十届：原数据的三种用法与"必须排除出验证折"；对抗验证；SMOTE 等不平衡方法普遍无效；"信本地 CV"；加权集成最常见但需多样性（模型/CV/数据/公开 notebook 四个维度）；权重方法从简单平均到 Optuna/scipy/hill climbing/2 级 stacking；单模型胜出的反例（LGBM/XGB/RF/GAM） | 395484 |
| 其他讨论 | 天体物理科普（35 票）；概率校准（28 票）；"去掉异常值"（22 票 / 21 评论）；"偏度与峰度被调换了？"（22 票）；改为双周赛制（32 票） | 索引 |

## 2. 逐方案对照矩阵

| 维度 | 1st | 3rd | 19th | 7th（汇编信息） |
| --- | --- | --- | --- | --- |
| 模型 | GAM + XGB/LASSO 派生特征 | XGB+LGBM+GAM | XGB/LGB/CAT 加权 | 多项式回归+Boosting+GAM 多样集成 |
| FE | 基本无（关系形态优先） | — | 全组合/全排列 + 重要性筛 | — |
| 校准 | GAM 自带 | — | — | — |
| 提交 | 单一主线 | — | 未提交 CV 更好的分组版 | — |
| 名次 | 1st | 3rd | 19th | 7th |

## 3. 共识、分歧与裁决

### 共识一：本场 GAM/加性模型优于纯 GBDT（1st、3rd、7th、十届复盘；置信度中高）

1st 的 GAM 拿第 1；3rd 与 7th 的集成里都有 GAM；结构化复盘把 GAM 列为 Episode 10 的关键。**裁决**：变量少、已是统计量、关系连续的任务上，加性模型的偏差-方差结构与正则更匹配。置信度：中高。

### 共识二：Log Loss 赛的诊断要靠校准而非分类模板（393073、393861；置信度中高）

49 票帖给出校准曲线 + 预测直方图的标准代码；社区另有概率校准专帖。**裁决**：指标决定诊断工具；logloss 下必须看校准。置信度：中高。

### 分歧：FE 是否值得（1st vs 19th；置信度中）

1st 认为 FE 几乎不可能；19th 用暴力组合特征取得 CV 提升（但分组版未提交）。**裁决**：该数据集上 FE 的边际收益小于"选对模型族"；暴力特征只在 CV 有收益时需谨慎。置信度：中。

### 事件：跨十届的社区元分析（394981、395484；置信度中高）

两篇帖子把前十届的冠军方案与主题化经验做成公共知识（原数据用法、CV 纪律、集成多样性、单模反例）。**裁决**：这是整个 Playground 系列最有复用价值的社区资产，应作为新场次的起手阅读。置信度：中高。

### 事件：提交选择（19th；置信度中）

19th 的 k-means 分组模型 CV 更好但公榜无改善，被放弃——自述本可最佳。**裁决**：与多场一致，CV 与公榜背离时需用第三种证据（如分折稳定性、校准）裁决。置信度：中。

## 4. 证据分级

| 断言 | 等级 | 说明 |
| --- | --- | --- |
| 1st 的 GAM 方案与理由 | 自述（含代码链接） | 中高 |
| 19th 的全组合特征与未提交说明 | 自述 + 截图 | 中 |
| 十届冠军汇编/结构化复盘 | 社区元分析（引用原始方案） | 中高 |
| 校准模板警告 | 高票帖 + 可复现代码 | 中高 |
| 天体物理背景 | 科普帖 | 低—中（背景） |

## 5. 悬案与缺口（登记）

- 2nd、4th–6th、8th–18th 方案未收录；
- "偏度/峰度被调换"的结论未定论；
- 十届汇编的原始方案细节未逐条核对（已作为 lineage 素材登记）；
- **图证缺口**：无（2 张图，本深读内嵌 1 张）。

## 6. 图表证据

![校准曲线与预测直方图](../../intel/playground-series-s3e10/bodies/393073_img/01.png)

**图 1**（topic 393073，49 票）：Log Loss 赛的正确诊断模板——左侧校准曲线（预测概率 vs 实际频率），右侧预测直方图（本场预测高度集中在 0 附近的小概率区）。

## 7. 出处

- 1st GAM（22 票 / 13 评论）：https://www.kaggle.com/competitions/playground-series-s3e10/discussion/396345
- 19th 全组合特征（13 票）：https://www.kaggle.com/competitions/playground-series-s3e10/discussion/396259
- 十届冠军汇编（32 票 / 6 评论）：https://www.kaggle.com/competitions/playground-series-s3e10/discussion/394981
- 十届结构化复盘（23 票 / 9 评论）：https://www.kaggle.com/competitions/playground-series-s3e10/discussion/395484
- 校准模板警告（49 票 / 14 评论）：https://www.kaggle.com/competitions/playground-series-s3e10/discussion/393073
- 天体物理背景（35 票 / 12 评论）：https://www.kaggle.com/competitions/playground-series-s3e10/discussion/392834
- 概率校准（28 票 / 5 评论）：https://www.kaggle.com/competitions/playground-series-s3e10/discussion/393861
- 去掉异常值（22 票 / 21 评论）：https://www.kaggle.com/competitions/playground-series-s3e10/discussion/393093
