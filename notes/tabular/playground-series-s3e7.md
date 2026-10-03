# Playground Series S3E7（酒店预订，AUC，重复对泄漏的公开处理）

> 主题：tabular ｜ 子类：— ｜ 领域：酒店（合成数据） ｜ 类别：Playground
> 截止：2023-02-27 ｜ 队伍数：678 ｜ 机制：标准赛 ｜ 指标：ROC AUC
> 数据来源：`intel/playground-series-s3e7/`（44 条主题索引 + 6 篇 write-up 正文）

## 1. 任务与数据

- 预订取消二分类（AUC）；全部数值列，但描述显示 `type_of_meal_plan`、`room_type_reserved`、`market_segment_type` 实为类别。
- **数据泄漏结构（本场核心）**：去掉 booking status 后有 **1531 对完全相同的记录**——562 对在训练集（**每对标签相反**）、253 对在测试集、716 对跨 train/test。

## 2. 验证方案

- 1st 为泄漏处理专门构造 holdout 验证"删除重复对是否有益"；
- 对抗验证（train vs 原数据）呈双峰 → 在原数据内部切掉与 train 最不像的 ~17% 子群，作为"两种原数据口径"做集成。

## 3. 模型家族

| 方案 | 使用者层次 | 关键点 | 出处 |
| --- | --- | --- | --- |
| 泄漏修正 + 类别三处理 + 双原数据口径集成 | 1st | 泄漏公开化后的标准答卷 | topic 390976 |
| 2nd | 前列 | 常规集成 | topic 390956 |
| 9th：XGB stack | 高位 | 堆叠线 | topic 390961 |

## 4. 关键技巧

- **重复对三态处理**（1st，堪称泄漏处理模板）：
  1) 跨集对（716 对）：把测试记录的预测设为训练伙伴的**相反标签**（+0.014）；
  2) 测试内对（253 对）：预测 0.5（siukeitin 的建议，+0.003）；
  3) 训练内对（562 对）：从训练集删除（提升 CV 可靠性）。
- 有趣的是社区很快发现了这个泄漏——**合成赛的泄漏常常是公开秘密**，抢时间窗口不如准备"处理模板"。
- 类别三姿势：原样/one-hot/LGBM categorical 各来一套，集成。
- 对抗验证的双峰发现 → 原数据的"局部子群剔除"对照（不删 vs 删 17%）。

## 5. 可迁移性评估

- **可直接迁移**：重复记录的三态处理框架；"先构造 holdout 验证泄漏策略"的纪律；对抗验证定位原数据中的异质子群。
- **需要前提**：能确认重复对与标签关系（本场"每对相反"是关键事实）；规则允许利用。
- **不建议照搬**：直接照抄泄漏用法而不验证私榜影响（见 S3E8 的反例：公榜 +0.05、私榜 −0.1）。

## 6. 对新手的关键启示

- 第一步检查"去标识列的完全重复行"，并统计其标签结构——本场泄漏贡献了 +0.017。
- 泄漏处理要写"模板"：跨集对、集内对、训练内对各不同处理。
- 合成数据的原数据常常内部不纯（双峰）——切子群做对照比整体用/弃更细。

## 8. 轻读结论（2026-10 补）

**一句话**：本场是"**重复行泄漏**"教科书：去掉目标后有 1531 对完全相同记录（训练内 562 对标签相反、测试内 253 对、跨集 716 对）——跨集对反值 +0.014、测试内对置 0.5 或 62 分位 +0.003；9th 赛后仅用 0.5 一招就从第 9 升到公榜第 1。除泄漏外，**特征工程被一致证明无效**，模型侧是深树 + 重集成 + 原数据混合（CV 只算竞赛数据）。

- 1st（390976）：三档重复处理 + 删训练重复；对抗验证发现原数据双峰 → 剔除 17% 的对照版；XGB exact/depth 12–13；4 XGB + 2 LGBM 平均。
- 2nd（390956）：按 booking date 分层；异常日期→月末；测试内对用最大化 OOF 的分位阈值覆盖；16 模型 Hill Climb + Nelder-Mead。
- 3rd（390979）：623 模型 + TF NN 栈；FE 无效（-0.004）；反值版与原版双提交对冲，反值版第 3。
- 9th（390961）：7 XGB Hill Climb + 泄漏后处理；0.5.csv 公 0.93252/私 0.92274 未被选。
- 4th（390962）：零 FE + 三模型 Optuna + scipy 逐折权重；伪标签无效。
- 社区：泄漏利用（38 票）、日期异常（29 票）、取消周期（26 票）、怪异数据点（20 票）。

**裁决**：先去重做泄漏分档处理（跨集反值/集内覆盖/训练内删除）；FE 不值得投入；原数据混合训练但 CV 只算竞赛数据；提交保留泄漏/非泄漏两条线。

**悬案**：5th–8th 未收录；0.5 vs 分位阈值无统一对照。

## 9. 图表证据

![原数据的对抗验证双峰](../../intel/playground-series-s3e7/bodies/390976_img/01.png)

**图 1**（topic 390976）：原数据内部双峰（两种来源）。

![0.5 泄漏提交 vs 被选提交](../../intel/playground-series-s3e7/bodies/390961_img/01.png)

**图 2**（topic 390961）：0.5.csv 双榜更优却未选中。

## 10. 出处

- 1st：重复对泄漏与三态处理：https://www.kaggle.com/competitions/playground-series-s3e7/discussion/390976
- 2nd 方案：https://www.kaggle.com/competitions/playground-series-s3e7/discussion/390956
- 9th：XGB stack：https://www.kaggle.com/competitions/playground-series-s3e7/discussion/390961
- 3rd：623 模型 + NN 栈：https://www.kaggle.com/competitions/playground-series-s3e7/discussion/390979
- 4th：简单方案：https://www.kaggle.com/competitions/playground-series-s3e7/discussion/390962
- 泄漏数据利用（38 票）：https://www.kaggle.com/competitions/playground-series-s3e7/discussion/388851
