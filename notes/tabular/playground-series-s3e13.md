# Playground Series S3E13（MAP@3，小测试集的探榜之痛）

> 主题：tabular ｜ 子类：— ｜ 领域：—（合成数据） ｜ 类别：Playground
> 截止：2023-05-01 ｜ 队伍数：934 ｜ 机制：标准赛 ｜ 指标：MAP@3
> 数据来源：`intel/playground-series-s3e13/`（80 条主题索引 + 6 篇 write-up 正文）

## 1. 任务与数据

- 目标类别数少、**测试集很小**——由此引发本场标志性事件：**榜单被机器人探榜**（用反复提交反推测试样本），社区公开讨论"小测试集对所有参赛者的伤害"，并建议未来赛季加大数据量。
- 指标 MAP@3：每行给出 Top-3 排序，命中越前分越高（帖子含通俗解释与评估细节）。

## 2. 验证方案

- #4 的"无 CV"方案：目标类别层级少 → 低折 CV 不可靠，干脆转向稳健的简单模型与提交策略（并坦言"WITHOUT CV ;-)"）。
- 小测试集场景的通则：CV 噪声大、探榜收益大、选择风险高——三者叠加。

## 3. 模型家族

| 方案 | 使用者层次 | 关键点 | 出处 |
| --- | --- | --- | --- |
| #2 / #3 方案 | 前列 | 小数据多分类常规线 | topic 407829、406409 |
| #4 无 CV 简单模型 | 4th | 低折不可靠 | topic 406812 |
| MAP@3 指标解释 | 社区 | 评估语义 | topic 402411 |
| 探榜事件复盘 | 社区 | 赛制公平性讨论 | topic 405480 |

## 4. 关键技巧

- **小测试集的两难**：探榜可以反推测试样本（"cheating"帖），但无奖金的 Playground 里风险大、收益虚；作者的诉求是机制层面（更大的测试集）。
- MAP@k 类指标的建模姿势：输出每行候选排序而非单一标签；Top-k 截断评估（与 EEDI MAP@25、S5E6 同源）。
- 当类别层级少、数据小时，复杂 CV 的边际效用下降——用"提交选择纪律"替代。

## 5. 可迁移性评估

- **可直接迁移**：MAP@k 的评估与建模姿势；小测试集场景的风险识别（CV 噪声/探榜/选择）；"低折 CV 不可靠时"的替代验证思路。
- **需要前提**：明确规则对探榜的态度。
- **不建议照搬**：参与探榜（道德与规则风险）；在小测试集上追公开榜微差。

## 6. 对新手的关键启示

- 测试集大小决定比赛"玩法"：小测试集下 CV 噪声大、榜单可被探——先识别赛制风险再谈模型。
- MAP@k 类任务要理解"排序到前 k 位"的得分结构，后处理（重排/校准）价值高。

## 8. 轻读结论（2026-10 补）

**一句话**：小测试集 + MAP@3 → 公榜几乎不可信（#1 公 0.37196 → 私 0.53179；#5 纯合成版私榜反超混合数据版 0.51535 vs 0.500），并出现机器人探榜；技术主线是"症状 one-hot 的组合逻辑特征 + 稳健重复 CV"。

- #2（407829）：XGB + 4 折 CV；症状聚类 + 两两 AND/OR/XOR 生成 6000+ 特征，按 MAP@3 筛到 17 个组合特征 → 私榜 0.52521。
- #3（406409）：RepeatedStratifiedKFold 10×10；SVC 基线 0.367 → 疼痛类求和 0.375 → 多项式对 0.3937 → 0.3989；VarianceThreshold 0.1；五模型无权重集成 → 私榜 0.52302。
- #4（406812）：不用 CV，RandomForest + OOB + Optuna，自述 OOB 与公私榜完全相关。
- #5（406313）：纯合成数据版公榜更低（0.41501）但私榜 0.51535（第 5）；混合数据版公 0.43598 / 私 0.500。
- 探榜事件（405480，47 票 / 53 评论）：截图多名 [Deleted] 账号；社区建议加大测试集。
- 领域警告："DO NOT use medical knowledge on this data!"（35 票）——合成数据的标签机制优先于医学先验。

**裁决**：小测试集赛先把选择建立在重复 CV 上并留稳健提交；one-hot 症状数据优先做组合逻辑特征；原始数据是否加入必须用重复 CV 验证。

**悬案**：#1 正文未收录；探榜处置结果未知；图证仅截图与代码，无分布/位移图。

## 9. 图表证据

![探榜截图](../../intel/playground-series-s3e13/bodies/405480_img/01.png)

**图 1**（topic 405480）：榜单中多名 [Deleted] 账号——机器人探榜证据。

![症状聚类特征](../../intel/playground-series-s3e13/bodies/407829_img/01.PNG)

**图 2**（topic 407829）：症状名聚类求和生成 cluster_0–3。

![成对逻辑特征](../../intel/playground-series-s3e13/bodies/407829_img/02.PNG)

**图 3**（topic 407829）：两两 AND/OR/XOR 生成 6000+ 候选特征。

## 10. 出处

- 探榜事件与赛制讨论：https://www.kaggle.com/competitions/playground-series-s3e13/discussion/405480
- #4：没有 CV 的简单模型：https://www.kaggle.com/competitions/playground-series-s3e13/discussion/406812
- MAP@3 指标解释：https://www.kaggle.com/competitions/playground-series-s3e13/discussion/402411
- #2 方案（13 票）：https://www.kaggle.com/competitions/playground-series-s3e13/discussion/407829
- #3 方案（19 票）：https://www.kaggle.com/competitions/playground-series-s3e13/discussion/406409
- #5 双提交对照（36 票）：https://www.kaggle.com/competitions/playground-series-s3e13/discussion/406313
