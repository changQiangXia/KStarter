# Home Credit - Credit Risk Model Stability

> 主题：tabular ｜ 子类：— ｜ 领域：金融 ｜ 类别：Featured
> 截止：2024-05-27 ｜ 队伍数：3856 ｜ 机制：代码赛 ｜ 指标：Home Credit 2023 - Gini Stability（Gini − 线性时间趋势惩罚）
> 数据来源：`intel/home-credit-credit-risk-model-stability/`（120 条主题索引 + 8 篇 write-up 正文 + 4 张图；深读升级 2026-10，Tier A #56）

## 1. 任务与数据

- **预测目标**：预测客户违约概率，指标为 **Gini × 稳定性**——含区分度项 + 时间趋势惩罚，不仅要求排序能力，还要求跨时间稳定。
- **数据形态**：32 个关系型文件、465 特征、436 描述；case_id 为根，internal/external 两源，按 depth 0（静态）/1（num_group1）/2（num_group1+num_group2）分层；字段后缀 P=DPD、M=类别掩码、A=金额、D=日期、T/L=未指明变换。
- **构造陷阱（本场最大特色）**：
  - 指标可被"钻空子"（metric hacking）：时间信息（WEEK_NUM）可从 `min_refreshdate_3813885D` 与 `date_decision` 的差值恢复（相关 0.9~0.99），恢复后对特定周区间的预测做下调即可抬分——与模型质量正交；
  - 比赛实际分成两个阶段：1st 明说 **Phase 1 = ML，Phase 2 = Metric Hack**；
  - 公开流传的对抗分类器 hack 只覆盖测试期 3~4 周，私榜脆弱（8th 因此从公 8 掉到私 253）；
  - 市场制度漂移（补助退坡/CARES Act 报告规则）使 Gini 有不可预测的随机趋势，被指标惩罚后**干净方案天花板锁死在 ≈0.52~0.53**。

## 2. 验证方案

| 方案 | 使用者 | 说明 |
| --- | --- | --- |
| StratifiedGroupKFold（group=WEEK_NUM），shuffle / no-shuffle 对比 | 1st | CV 差 ≤0.005 与 LB 弱相关，>0.01 才相关 |
| 5 折按周顺序切分 + 丢弃 slope 项 | 公开 8/私 253 | 简单 CV/时序 CV/带 gap 时序 CV/特定周留出全试过，均与 LB 不相关；**开始集成后相关性才改善** |
| SGKF / Multilabel SGKF / RollOut / HoldOut 全试 | 10th | 最终采用最信任的 SGKF(group=WEEK_NUM) |
| SGKF(k=5) + 堆叠 + 校准 | 13th、53rd | 单模 CV AUC ~0.85，堆叠 0.8593 |
| StratifiedKFold/SGKF + 周样本权 | 53rd | 日期特征除以 −365 归一 |
| 5 折 SGKF（全模型统一） | 57th | 10 折元分类器替代简单加权 |

**裁决**：制度性漂移下 CV 只能粗筛（没有队伍找到与 LB 稳定相关的 CV）；样本外分组 + 集成多样性是次优解。

## 3. 方案谱系

| 方案 | 名次（票数） | 关键点与数字 |
| --- | --- | --- |
| 模型池 + 中性下注 hack | 1st（175） | LGBM 0.4 + DNN 0.24 + CatBoost 0.36；CV 0.712/公 0.605；后处理 WEEK_NUM 1/2、REDUCE −0.03 → 公 0.654/私 **0.605**；无 hack 池上限 ≈0.53；双提交对冲 |
| 自研日期恢复法 | 公开 8/私 253（60） | `min_refreshdate` 锚定 2019-03-01 反推日期（87% 正确）；自研法私 0.560~0.617，公开流传法私 0.510~0.520；无 hack 上限 0.520；6 套数据处理器 |
| 特征/堆叠 + 年份后处理 | 13th（38） | 772→411 手工特征；10 模型 → RidgeClassifier 堆叠 0.8593 + 概率校准 + 5 seed；pmts_year_1139T 年份下调 |
| 只 hack 未来周组 | 10th（29） | WEEK_NUM 恢复（相关 0.99）；探针：测试周号最大 142、null 30~35%；周 92→130 线性下调（92 周 −0.04）；单 XGB |
| 纯 ML（无 hack） | 53rd（29） | 2 CatBoost + LGBM + NN；CV AUC 0.852~0.858；尝试 hack 后私榜反而更低 |
| 基础集成后冻结 | silver（29） | XGB/LGBM/CatBoost 基础集成；**hack 合法化时停止工作**，靠确定性拿银 |
| 多模型多样性集成（无 hack） | 57th（24） | 7 模型私 0.476~0.509（CatBoost 0.509）→ L3 集成私 **0.528**/公 0.605；hack 前在 top-10 |
| 数据理解帖 | 社区（375） | 32 文件 schema、depth/后缀语义、空值×大小可视化——全场的地图 |

## 4. 关键技巧

- **指标审计优先**：拿到复合指标先做"可操纵性审计"——区分度项之外的项能否被与模型无关的操作影响（本场：时间趋势惩罚 + 周号可恢复 = 竞赛变彩票）。
- **CV-LB 相关性量化**：按差幅分档（≤0.005 弱相关，>0.01 强相关）；**FE 增益比参数调优增益更可信**（1st）。
- **关系型多表聚合**：按 `numgroups` 排序后再做 first/last；时间窗聚合（合同结束 3/5/7 年、分期 1/6 月/1/2/3 年）；`num_group1=0` 是申请人本人；active/closed 重复列合并；多源同字段拼接但保留原列。
- **弱 CV 环境用二阶模型**：stacking + 概率校准 + seed 平均（13th +0.003；57th 元分类器 +0.002）。
- **特征级小增益**：CountEncoder 全量训练 +3e-3、>200 类别 collapse +0.003、高缺失子模型 top10 +2e-3、伪标签 +6e-3（10th）。
- **彩票环境的风险管理**：双提交对冲（No-Hack + Hack）；参数取分布中位数（DEVIDE=1/2、REDUCE=0.03）；避免只覆盖局部测试期的对抗 hack；或直接冻结提交（silver）。

## 5. 深读结论（2026-10 补）

**一句话**：这是一场"复合指标审计 + 日期泄漏恢复 + 参数下注"的比赛——它教给社区的第一课不是风控建模，而是指标设计缺陷如何摧毁排名的可比性。

- 干净方案上限三队独立：0.53（1st）/0.520（8th）/0.528（57th）；hack 版上限 0.60~0.62（1st 私 0.605、8th 自研 0.560~0.617）。
- 模型差距 0.00X vs hack 参数差距 0.0X（1st）：**模型分是入场券，下注分布决定名次**。
- 稳健 hack = 周号/日期恢复类（覆盖整段测试期）；脆弱 hack = 对抗分类器（只覆盖 3~4 周，私榜起点一改即失效）。
- 时间匿名化只移除了显式日期：差值、空值趋势、分布漂移都是恢复通道。
- 治理时间线：2 月揭发（130 票）→ 官方公告（83/34）→ 3 月暂停重启（96）→ 4 月 hack 合法化（73）→ 榜单失控 → 官方收尾（34）。

**数字账精选**：1st 集成 CV 0.712/公 0.605 → hack 公 0.654/私 0.605；8th 私 0.560~0.617 vs 公开法 0.510~0.520；10th 周 92→130 线性下调；57th 集成私 0.528。

**失败学**：1st 的 Transformer 族/K-means/收入税差分；8th 的子模型元特征、通胀/收入缩放、伪标签、对抗验证剔除；57th 的长清单（dart/ordered boosting/FastRGF/DAE/TabTransformer/各种 scaler…）；13th 的伪标签；53rd 的 hack 版本反而更差。

**悬案**：指标公式原文（475878/476449/476867/478716 未收录）；hack 组别语义（0→55 组 vs 92→142 组）；2nd~9th 方案缺失；57th 名次口径（标题 57th vs 正文 62nd）；官方是否判罚（508163 未收录）。

## 6. 图表证据

> 路径相对本文件（`notes/tabular/`）：`../../intel/home-credit-credit-risk-model-stability/bodies/<topic>_img/NN.ext`

![1st 的模型池与后处理流水线](../../intel/home-credit-credit-risk-model-stability/bodies/508337_img/01.png)

**图 1：1st 的两段式方案总览**（topic 508337）——LGBM(0.4) + DNN(0.24) + CatBoost(0.36) → 集成（CV 0.712/公 0.605）→ 后处理（WEEK_NUM 1/2、REDUCE −0.03）→ 公 0.654/私 0.605。

![10th 的测试集探针表](../../intel/home-credit-credit-risk-model-stability/bodies/508588_img/01.png)

**图 2：10th 的测试集探针**（topic 508588）——测试周号最大 142、<92 组 53~56、null 30~35%、131~142 占 10~20%。

![数据 schema：depth 与来源](../../intel/home-credit-credit-risk-model-stability/bodies/473950_img/01.png)

**图 3：数据 schema**（topic 473950）——case_id 为根、internal/external、depth 0/1/2、P/M/A/D/T/L 变换后缀。

![文件大小与空值分布](../../intel/home-credit-credit-risk-model-stability/bodies/473950_img/02.png)

**图 4：文件大小 × 空值率**（topic 473950）——credit_bureau_a_2_* 最大（2.9G 起）；a_1_0 空值 75.2%、a_1_1 65.0%、static_cb 62.1%；tax_registry/base 为 0%。

## 7. 可迁移性评估

- **可直接迁移**：
  - 自定义/复合指标先做**可操纵性拆解**：区分度项是否与稳定性项独立可调；
  - CV-LB 相关性**量化分档**，FE 增益优先于调参增益；
  - 关系型多表：depth 语义 + 后缀语义 + 排序聚合 + 时间窗聚合 + 多源拼接；
  - 弱 CV 环境下 stacking + 校准 + seed 平均；
  - 彩票式环境的风险管理：双提交对冲、中性参数、或退出冻结。
- **需要前提**：指标含可独立操纵项、时间信息可恢复（差值/空值趋势/分布）；干净比赛不适用 hack 部分。
- **不建议照搬**：公开流传的对抗分类器 hack；任何具体 hack 参数（1/2、0.03、周区间）；把本场"干净方案上限 0.53"当作风控模型的通用上限。

## 8. 对新手的关键启示

1. **指标设计缺陷是竞赛风险**：识别—量化—对冲，而不是假设榜单永远公平。
2. **匿名化 ≠ 信息移除**：日期差值、空值率趋势、分布漂移都能恢复时间——检测时间泄漏是特征工程的一部分。
3. **CV 不相关时不要硬调参**：用集成多样性、二阶模型与"信任的单一分组方案"代替。
4. **干净方案也能进前 60**（0.528 ≈ 57/62 名 / 3856 队）；但若目标是名次，必须对 hack 下注做风险管理。
5. **能在 hack 合法化时停下**（silver）是一种被低估的策略。

## 9. 出处

- 讨论区索引：`intel/home-credit-credit-risk-model-stability/topics.md`（120 条）
- 已收录 write-up（8 篇）：
  - 数据理解（375 票）：https://www.kaggle.com/competitions/home-credit-credit-risk-model-stability/discussion/473950
  - 1st（175 票）：https://www.kaggle.com/competitions/home-credit-credit-risk-model-stability/discussion/508337
  - 公开 8/私有 253（60 票）：https://www.kaggle.com/competitions/home-credit-credit-risk-model-stability/discussion/507946
  - 13th（38 票）：https://www.kaggle.com/competitions/home-credit-credit-risk-model-stability/discussion/508113
  - 10th（29 票）：https://www.kaggle.com/competitions/home-credit-credit-risk-model-stability/discussion/508588
  - 53rd 无 hack（29 票）：https://www.kaggle.com/competitions/home-credit-credit-risk-model-stability/discussion/508242
  - silver（29 票）：https://www.kaggle.com/competitions/home-credit-credit-risk-model-stability/discussion/507971
  - 57th 无 hack（24 票）：https://www.kaggle.com/competitions/home-credit-credit-risk-model-stability/discussion/508124
- 深读全本：`analysis/deep/home-credit-credit-risk-model-stability.md`（11 组件 + 机制推演 M1–M7 + 4 图证）
- 缺口登记（未收录正文）：475878、476449、476867、478716、497167、497337、496898、501172、501744、505664、508163、475485、476463、477075、488466、505574、507556、507982、507959
