# Playground Series S5E12 - 糖尿病预测

> 主题：tabular ｜ 子类：— ｜ 领域：医疗（双重合成） ｜ 类别：Playground
> 截止：2025-12-31 ｜ 队伍数：4206 ｜ 机制：标准赛 ｜ 指标：ROC AUC
> 数据来源：`intel/playground-series-s5e12/`（59 条主题索引 + 6 篇 write-up 正文）

## 1. 任务与数据

- 预测目标：基于健康指标预测糖尿病诊断（二分类 AUC）。
- **数据被主办方刻意扭曲**：原始数据里强分离特征（HbA1c、空腹/餐后血糖、风险评分）被删除；部分连续特征被离散化/截断（waist_to_hip_ratio、systolic_bp、血脂等）；原数据本身近乎完美可分（XGB/LGB/CatB 原数据 AUC≈0.9998），而本赛模型只有 ~0.73——"数据损坏"本身就是赛题设计。
- 结论（社区共识）：**原数据在本场基本不应使用**（拼接或 TE 修饰都会引入偏离），与多数 Playground 相反。
- 额外结构：**ID 泄漏**——id 作为特征能提分，因为训练集尾部与测试集分布更接近。

## 2. 验证方案（本场的核心创新）

- **Post-cutoff CV**（2nd/1st 均采用）：用对抗验证找到"头部 vs 尾部"的分界 `CUTOFF_ID`；尾部（约 2.3 万行）分布贴近测试集 → 只用尾部做交叉验证，评分即偏高但更贴近 LB。
- **概念漂移发现**（2nd）：把头部按"与尾部的相似度"分 10 箱——越像测试集的样本，标签率越偏离尾部分布（0.52 vs 0.65）→ 单纯样本加权不够，需要 TE/建模层面都用尾部逻辑。
- 1st 的定稿纪律：监控 post-cutoff CV 与 Public LB 的 gap（0.00121 可接受），不在 CV 涨而 LB 掉时硬交。

## 3. 模型家族

| 方案 | 使用者层次 | 关键点 | 出处 |
| --- | --- | --- | --- |
| HC（爬山）选模 → Ridge 二阶段集成（Top-36, α=10） | 1st | Ridge 正则化换取泛化，公/私榜双升 | topic 665432 |
| ID 位移分析 + 尾部验证 + 加权/尾部 TE/伪标签 | 2nd | 样本权重 Tail 16× / Orig 8× / Head 1×；分位数映射修伪标签 | topic 665385 |
| 盲目 blender 批判 + 有原则的单模 | 社区 | 公开 notebook 过拟合 LB 的实证 | topic 651787 |
| 新手时间管理路线图（3–4 阶段） | 社区 | 前 2–3 天探索、编号实验、保存 OOF | topic 650676 |

## 4. 关键技巧

- **分布迁移侦探工作流**（本场可复用的最大资产）：对抗验证定位偏移 → 分箱观察 covariate/concept shift → 据此设计验证集与采样权重。
- 尾部 TE（只用 tail+orig 计算目标编码）、伪标签 + 分位数映射、以尾部均值为 margin 的残差提升（2nd 的单模清单）。
- **两阶段集成**（HC → Ridge）打破平台期；"CV 略低但泛化更好"的选择标准。
- 明确避开"分数看板"公开 notebook（blender 农场），从讨论区汲取信号（2nd 的做法）。

## 5. 可迁移性评估

- **可直接迁移**：对抗验证 + ID/分界分析；按"与测试集的相似度"分层验证与加权；两阶段集成；CV–LB gap 监控。
- **需要前提**：数据带时间/顺序结构（id 排序）才可能复现 ID 位移现象；概念漂移需要足够样本做分箱统计。
- **不建议照搬**：把"id 当特征"当通用技巧（属数据集特有问题）；直接拼接被扭曲的原数据。

## 6. 对新手的关键启示

- 当 CV 与 LB 长期背离，**先怀疑数据结构**（漂移、泄漏、被删除的特征），而不是继续调参。
- 榜单异常（高分 blender 遍地）时，回讨论区找"解释性帖子"——本场 2nd 是入坑 9 个月的新人，靠读懂讨论区拿下亚军。
- 月赛节奏建议（roadmap 帖）：尽早开始、编号实验、保存 OOF 与提交文件。

## 7. 出处

- 1st：HC + Ridge 两阶段集成：https://www.kaggle.com/competitions/playground-series-s5e12/discussion/665432
- 2nd：基于 ID 位移分析的获胜法：https://www.kaggle.com/competitions/playground-series-s5e12/discussion/665385
- 数据被刻意破坏的发现：https://www.kaggle.com/competitions/playground-series-s5e12/discussion/652262
- 新手月赛路线图：https://www.kaggle.com/competitions/playground-series-s5e12/discussion/650676
