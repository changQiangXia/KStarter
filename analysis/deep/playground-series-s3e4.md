# Playground Series S3E4（信用卡欺诈检测）轻量深读（Tier B）

> 赛事：Playground ｜ 主题 tabular（二分类，极不平衡）｜ 641 队 ｜ 标准赛 ｜ 指标：ROC AUC
> 材料基础：`digests/playground-series-s3e4.md`（6 篇正文：30th 382447 / 时间结构 380771 / 54th 382443 / 相关性 381087 / 10th 382539 / 7th 382589；67 条主题索引）+ 6 张归档图
> 轻读时间：2026-10（Tier B B12）

## 1. 一句话重述与数字账

信用卡欺诈二分类（99.8% 负 / ~0.2% 正），且数据按时间切分：**train = 0–33.5 小时、test = 33.5–48 小时**（非重叠窗口）。本场的两个结论都很锋利：①**必须用时间感知的 CV**（随机 KFold 会高估）；②**原始数据的盲目拼接是陷阱**——30th 自述若不加原始数据可得 0.8333（足以第 1），加了只能第 30；54th 只用 132 行"时间截止之后"的原始欺诈样本，反而用单 CatBoost 无调参进前 6%。特征侧，V20/V23/V27/V28 与 Amount 的比值是"钱在哪里"的强信号，单用可达 ~0.8 AUC。

| 关键数字 | 值 | 来源 |
| --- | --- | --- |
| 30th（382447） | TimeSeriesSplit 调参；最终 = **50 个同参 XGB 平均**（5 折 ×10 次 StratifiedKFold）；用了全量赛方数据 + 原始数据的欺诈实例；两个增益：① V 特征减当日均值（私榜 +0.0015，公榜无变化）；② (V14,V21) 组合在训练集是纯组 → 对测试中 466 条同组样本直接判 0（公私榜 +0.0004）；**自述若不用原始数据 = 0.8333，可拿第 1** | 382447 |
| 时间结构（380771） | train/test 时间窗不重叠（0→33.5h / 33.5→48h）；建议验证集比训练集前移 14.5 小时、把 Time 归一化/分桶（morning/afternoon/evening）；提示公榜可能主要由最前几小时决定 | 380771 |
| 54th（382443） | 对抗验证显示 train/test/original 三个分布差异巨大；只用 **132 行**原始欺诈（`Class==1 and Time>120580`，即赛方训练时段之外的样本）；最终单 CatBoost、**不做超参调优** | 382443 |
| 相关性（381087） | V20/V23/V27/V28 为"money features"：`V20/Amount`、`V23/Amount`、`V27/V28` 及比值组合，**只用少数比值特征就能到 LB ~0.8**；fraud 几乎全部落在 V20/Amount≈0（"欺诈者直接刷满额度"） | 381087 |
| 10th（382539） | Time→Hour/Day；采用公开的除法特征；**CatBoost + 自定义 Focal Loss**；10 折 StratifiedKFold 平均；Optuna TPE 约 50 次迭代（depth/lr/l2/subsample/min_data_in_leaf + focal gamma） | 382539 |
| 7th（382589） | 以 soupmonster 的时序特征选择 + 多分类器为底做流程化集成（附流程图）；自述"简单但冗长" | 382589 |
| 社区 | 原始数据重复行（31 票 / 18 评论、14 票）；"这数据集与原版不同、更难分类"（28 票 / 30 评论）；对抗验证（25 票 / 16 评论）；"完美 CV"（21 票 / 34 评论）；可疑金额（30 票 / 13 评论）；对数尺度画预测（23 票） | 索引 |

## 2. 逐方案对照矩阵

| 维度 | 30th | 54th | 10th | 7th |
| --- | --- | --- | --- | --- |
| 模型 | 50×XGB 平均 | 单 CatBoost（零调参） | CatBoost + Focal Loss | 多分类器流程集成 |
| 验证 | TimeSeriesSplit + 5×10 折 | 公开 CV 策略 | 10 折 Stratified | 沿用时序特征选择 |
| 原始数据 | 全量 + 原始欺诈行（拖累） | 132 行（Time>120580） | 两者都用 | — |
| 关键特征 | 日均值差、V14×V21 纯组 | 时间截断 | Hour/Day + 除法特征 | 公开方案派生 |
| 结果 | 30th（不加原始→0.8333） | 54th（单模） | 10th | 7th |

## 3. 共识、分歧与裁决

### 共识一：必须用时间感知 CV（380771、30th、54th；置信度高）

train/test 窗口不重叠（0–33.5h vs 33.5–48h）；380771 明确建议"验证集前移 14.5 小时"，30th 用 TimeSeriesSplit 调参、最终再用多折平均。**裁决**：任何随机切分都会把"未来"泄漏进训练；时间序列赛的 CV 要模拟预测区间的分布位移。置信度：高。

### 共识二：原始数据不能盲目拼接（30th、54th、社区对抗验证帖；置信度高）

30th 因加入原始数据从可夺冠跌到 30 名；54th 只加 132 行"赛方时段之外"的原始样本；对抗验证与"数据集与原版不同"帖都指出分布差异。**裁决**：先做对抗验证，再按时间/子集谨慎挑选原始数据；"CV+公榜都变好"也可能是分布假象。置信度：高。

### 共识三：V 特征比值是核心信号（381087、10th、30th；置信度中高）

`V20/Amount` 等比值把 ~0.8 AUC 直接做出来；10th 也用公开除法特征；30th 的当日均值差进一步强化。**裁决**：先构造少数强交互/比值特征，再谈模型与调参。置信度：中高。

### 共识四：极不平衡 + 高噪声下，简单方案同样进前列（54th、10th；置信度中）

54th 单 CatBoost 零调参；10th 公开特征 + focal loss + 少量 Optuna 即第 10。**裁决**：不平衡赛里 focal/类别权重只解决一部分问题；数据选择（时间与来源）比模型复杂度更关键。置信度：中。

### 事件：重复行与"完美 CV"的幻觉（381455、381483、381415；置信度中）

多条帖子指出三个数据集里存在大量重复行，"完美 CV"帖（21 票 / 34 评论）随后引发争议。**裁决**：重复行会让随机 CV 虚高；时间切分 + 去重是前置步骤。置信度：中。

## 4. 证据分级

| 断言 | 等级 | 说明 |
| --- | --- | --- |
| 30th 的 0.8333 反事实与两条增益 | 自述（具体到 +0.0015/+0.0004） | 中高 |
| 54th 的 132 行时间截断选择 | 自述 + 时间分布图 | 中高 |
| 381087 的比值特征 → LB ~0.8 | 自述 + 3 张散点图 | 中高 |
| 10th 的 CatBoost+Focal 细节 | 自述（含代码链接） | 中 |
| 时间窗结构（0–33.5h / 33.5–48h） | 专题帖 + 直方图 | 高 |
| 重复行/分布差异 | 多帖（含对抗验证） | 中高 |

## 5. 悬案与缺口（登记）

- 1st–6th、8th–9th 方案未收录；"完美 CV"（381415）的具体方法未细读；
- 原始数据 132 行子集的精确选择依据（Time>120580）只有图示；
- 7th 的流程图为图片，节点细节需回看原图；
- **图证缺口**：无（6 张归档图，本深读内嵌 3 张）。

## 6. 图表证据

![V15/V16 的时间位移](../../intel/playground-series-s3e4/bodies/380771_img/01.png)

**图 1**（topic 380771，44 票）：V15/V16 随时间变化——33.5h（约 120,580s）之后进入测试区间，特征分布明显位移，说明时间感知 CV 的必要性。

![交易时间的训练/测试切分](../../intel/playground-series-s3e4/bodies/382443_img/01.png)

**图 2**（topic 382443，54th）：Transaction by Time——蓝色为训练（0–120,580s）、红色为测试（120,580–175,000s），两个窗口完全不重叠。

![V20/Amount 的判别力](../../intel/playground-series-s3e4/bodies/381087_img/02.png)

**图 3**（topic 381087，46 票）：`V20/Amount` 散点——欺诈样本（橙）几乎全部贴近 0（刷满额度），是"比值特征"直接贡献 AUC 的证据。

## 7. 出处

- 30th（28 票）：https://www.kaggle.com/competitions/playground-series-s3e4/discussion/382447
- Use your Time wisely（44 票 / 24 评论）：https://www.kaggle.com/competitions/playground-series-s3e4/discussion/380771
- 54th 单模型（16 票 / 6 评论）：https://www.kaggle.com/competitions/playground-series-s3e4/discussion/382443
- Correlation tells the story（46 票 / 23 评论）：https://www.kaggle.com/competitions/playground-series-s3e4/discussion/381087
- 10th（17 票 / 5 评论）：https://www.kaggle.com/competitions/playground-series-s3e4/discussion/382539
- 7th 流程集成（22 票 / 9 评论）：https://www.kaggle.com/competitions/playground-series-s3e4/discussion/382589
- 原始数据重复行（31 票 / 18 评论）：https://www.kaggle.com/competitions/playground-series-s3e4/discussion/381455
- 与原版差异（28 票 / 30 评论）：https://www.kaggle.com/competitions/playground-series-s3e4/discussion/381305
- 对抗验证（25 票 / 16 评论）：https://www.kaggle.com/competitions/playground-series-s3e4/discussion/381089
- 完美 CV 讨论（21 票 / 34 评论）：https://www.kaggle.com/competitions/playground-series-s3e4/discussion/381415
