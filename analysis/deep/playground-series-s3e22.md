# Playground Series S3E22（马疝痛存活预测）轻量深读（Tier B）

> 赛事：Playground ｜ 主题 tabular（马匹疝痛 3 分类，F1）｜ 1541 队 ｜ 标准赛 ｜ 截止 2023-10-02
> 材料基础：`digests/playground-series-s3e22.md`（6 篇正文：入门材料 438603 / 领域文献 438620 / LB shakeup 444654 / 14th 复盘 444642 / 死多次的怪癖 441284 / 获奖模型发布疑问 444892；80 条主题索引）+ 1 张归档图
> 轻读时间：2026-10（Tier B B18）

## 1. 一句话重述与数字账

用术前/术中临床指标预测马匹疝痛（colic）的结局（lived / died / euthanized），指标 F1。本场是"**小数据 + 合成数据 + 大奖牌洗牌**"的典型教材：公开/私榜名次大面积翻转（社区作图分出 7 个区域），14th 自述**未选用的版本私榜 0.77121 反而高于选中版本 0.76818**；同时 50 票的怪癖帖证明同一 hospital_number 的"马"会死多次——合成实体复用必须当作结构信号处理。

| 关键数字 | 值 | 来源 |
| --- | --- | --- |
| 规模与指标 | **1541 队**；F1（3 分类：lived/died/euthanized）；社区提示 **micro-F1 在此等价于 accuracy** | 索引 / 440333 |
| 洗牌烈度 | 36 票专帖用 public-private 散点划出 **7 个区域**（region 2/6 = 公榜好私榜崩；region 3/4/5 = CV 可信者私榜反弹）；29 票"Beware of the public LB!"；"Out of the top 11 teams, 7 made only 1 or 2 submissions" | 444654 / 438637 / 444630 |
| 14th（444642） | 公开 notebook 版本 34 私榜 **0.76818**（第 14）；**未选用的版本 29 私榜 0.77121**；作者判断 20/80 划分下比赛"相当随机"，并猜测前排多为单模型 | 444642 |
| 实体复用怪癖 | 按 hospital_number × outcome 透视可见同一编号多次出现、甚至"死 5 次"；"horse treated > 1 time" 语义与合成数据叠加 | 441284 / 438825 |
| 目标分布探测 | 25 票帖"用一次提交揭示公开榜的目标分布"（利用提交分数反推 LB 组成） | 438889 |
| 领域文献（438620） | AI 预测需手术/存活：Decision Tree / MLP / Bayes 等，**76%（需手术）、85%（存活）**准确率；Cox 术后模型：存活率 10 天 **0.87** → 100 天 **0.82** → 600 天 **0.75**；epiploic foramen entrapment 风险比 **RR=2.1**；术后 colic 发生率 **29%**（≥1 次） | 438620 |
| 数据边界 | 原始数据对比警告（441019）；Made-Up Values（440699）；test 端 lesion_3 只有一个唯一值（438615）；类别取值 train/test 不一致（441977） | 索引 |

## 2. 逐方案对照矩阵

| 维度 | 入门/领域线（438603 / 438620） | 前排工程线（14th 444642） | 复盘/结构线（444654 / 441284） |
| --- | --- | --- | --- |
| 目标 | 用列字典 + 兽医文献建立特征直觉 | 预置预处理 + 集成，控过拟合 | 解释洗牌、发现实体复用 |
| 特征 | 临床语义（水灰比式启发：PCV、蛋白、腹围等） | notebook 全流程 | hospital_number 复用结构 |
| 验证 | 强调 micro-F1=accuracy | 反复强调勿过拟合；20/80 划分噪声大 | "只依赖 CV" |
| 结论 | 领域变量可映射 | LB 选择不可靠，未选中版本更好 | 提交要分散以对冲洗牌 |

## 3. 共识、分歧与裁决

### 共识一：本场必须只信 CV，公榜名次会大面积翻转（444654 / 438637 / 444626 / 444641；置信度高）

7 区域散点图直接展示 region 2/6 的"公榜高、私榜崩"与 region 3/4/5 的"CV 可信者反弹"；有专帖确认私榜与 CV 对齐。**裁决**：小数据合成赛按熵最大化原则选提交（多样模型 + 多 seed），以 CV 决定取舍，公榜只做 sanity check。置信度：高。

### 共识二：hospital_number 是实体键而非唯一 ID，复用既是泄漏源也是分组键（441284 / 438825；置信度高）

"同一匹马死 5 次"说明合成过程保留了多次就诊语义但没有实体去重。**裁决**：先按该键做 pivot/频次审计；若要利用需做严格的 group CV，避免把同实体样本拆到 train/test 造成评估虚高。置信度：高。

### 事件一：合成数据的"假值/分布漂移"必须逐列检查（440699 / 438615 / 441977 / 441019；置信度中高）

缺失值编码异常（`none` vs `None`）、test 端某 lesion 列只有一个取值、类别取值 train/test 不一致、原始数据与合成数据分布差异都被逐帖记录。**裁决**：建模前做"逐列 train/test 取值集合 diff"，并谨慎使用原始数据（441019）。置信度：中高。

### 事件二：领域文献可当特征地图，但要翻译成竞赛字段（438620 / 438603；置信度中）

AI 论文给出 76%/85% 的基线准确率与 PCV、切除长度、手术时长等风险因子；Cox 模型给出存活曲线。**裁决**：把文献变量对照到列字典（PCV、total_protein、abdominal distention、lesion 编码等），作为特征工程/分组审计的起点，而不是直接套用医学结论。置信度：中。

### 分歧：前排是单模型还是集成（444642 猜测 vs 444654 的"提交要分散"；置信度低）

14th 只是"assume"前排为单模型，归档中无前排方案可证；洗牌分析者则主张多元化提交对冲。**裁决**：在证据缺失时，按 CV 稳定性而非名次猜想组织方案。置信度：低（保持悬案）。

## 4. 证据分级

| 断言 | 等级 | 说明 |
| --- | --- | --- |
| 洗牌 7 区域与"只信 CV" | 自述 + 散点图（444654） | 中高（可复算） |
| 14th 的 0.76818 / 0.77121 | 自述 + notebook 版本（444642） | 中高 |
| 同一 hospital_number 多次死亡 | pivot 表 + 多帖（441284 / 438825） | 高 |
| micro-F1 = accuracy | 讨论帖（440333） | 高（定义事实） |
| 兽医文献数字（76%/85%、0.87→0.75、RR 2.1） | 论文引用（438620） | 中高（文献原文可查） |
| 前排单模型猜测 | 个人推测（444642） | 低 |

## 5. 悬案与缺口（登记）

- #1–#13 方案未归档，14th 是唯一可读名次；
- 获奖模型"发布"链接指向他人 notebook，发布状态存疑（444892）；
- 实体复用（hospital_number）能否合法利用、如何计入 CV 未定论；
- 原始数据可用性与合成数据差异未系统量化（441019）；
- **图证缺口**：无（1 张图，已内嵌）。

## 6. 图表证据

![S3E22 public-private 名次动态](../../intel/playground-series-s3e22/bodies/444654_img/01.png)

**图**（topic 444654）：public LB 对 private LB 的名次散点与 7 个区域划分——region 2/6 是"公榜高、私榜崩"，region 1 为稳定前排，region 3/4/5 是 CV 可信者在私榜反弹；本场"只信 CV、分散提交"的直接证据。

## 7. 出处

- Onboarding materials（62 票 / 28 评论）：https://www.kaggle.com/competitions/playground-series-s3e22/discussion/438603
- 兽医 AI/Cox 文献（32 票 / 4 评论）：https://www.kaggle.com/competitions/playground-series-s3e22/discussion/438620
- Inferring the LB shakeup（36 票 / 11 评论）：https://www.kaggle.com/competitions/playground-series-s3e22/discussion/444654
- 14th Solution（26 票 / 15 评论）：https://www.kaggle.com/competitions/playground-series-s3e22/discussion/444642
- 同一匹马死多次（50 票 / 26 评论）：https://www.kaggle.com/competitions/playground-series-s3e22/discussion/441284
- 获奖模型发布疑问（2 票 / 0 评论）：https://www.kaggle.com/competitions/playground-series-s3e22/discussion/444892
- Beware of the public LB!（29 票 / 11 评论）：https://www.kaggle.com/competitions/playground-series-s3e22/discussion/438637
- 用一次提交探测 LB 目标分布（25 票 / 5 评论）：https://www.kaggle.com/competitions/playground-series-s3e22/discussion/438889
- micro-F1 = accuracy（4 票 / 0 评论）：https://www.kaggle.com/competitions/playground-series-s3e22/discussion/440333
- 前 11 名 7 队只提交 1–2 次（2 票 / 0 评论）：https://www.kaggle.com/competitions/playground-series-s3e22/discussion/444630
