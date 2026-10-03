# Playground Series S5E12 - 糖尿病预测

> 主题：tabular ｜ 子类：— ｜ 领域：医疗（双重合成） ｜ 类别：Playground
> 截止：2025-12-31 ｜ 队伍数：4206 ｜ 机制：标准赛 ｜ 指标：ROC AUC
> 数据来源：`intel/playground-series-s5e12/`（59 条主题索引 + 6 篇 write-up 正文）

## 1. 任务与数据

- 预测目标：基于健康指标预测糖尿病诊断（二分类 AUC）。
- **数据被主办方刻意扭曲**：原始数据里强分离特征（HbA1c、空腹/餐后血糖、风险评分）被删除；部分连续特征被离散化/截断（waist_to_hip_ratio、systolic_bp、血脂等）；原数据本身近乎完美可分（XGB/LGB/CatB 原数据 AUC≈0.9998），而本赛模型只有 ~0.73——"数据损坏"本身就是赛题设计。
- 原数据用法存在三方观点（深读裁决为可统一）：**禁用"原样拼接"**，但"生成逻辑"可用——2nd 以 8× 权重并入训练、EDA 起点帖只做统计参考特征（mean/count 映射）、有帖子主张完全不用；三者的共同底线是"不要无处理混入"。
- 额外结构：**ID 泄漏**——id 作为特征能提分，因为训练集尾部与测试集分布更接近。

## 2. 验证方案（本场的核心创新）

- **Post-cutoff CV**（2nd/1st 均采用）：用对抗验证找到"头部 vs 尾部"的分界 `CUTOFF_ID`；尾部（约 2.3 万行）分布贴近测试集 → 只用尾部做交叉验证，评分即偏高但更贴近 LB。
- **概念漂移的量化证据**（2nd）：把 head 按"与 tail 的相似度"分 10 箱，目标率从 0.6436 单调降到 **0.5214**（tail 真值 0.6214）——越像测试集的样本标签率反而越低，说明标签函数本身在漂移；单纯样本加权不够，需要原数据逻辑（TE/加权）与尾部专训配合。
- 1st 的定稿纪律：监控 post-cutoff CV 与 Public LB 的 gap（0.00121 可接受），不在 CV 涨而 LB 掉时硬交。

## 3. 模型家族

| 方案 | 使用者层次 | 关键点 | 出处 |
| --- | --- | --- | --- |
| HC（爬山）选模 → Ridge 二阶段集成（Top-36, α=10） | 1st | Ridge 正则化换取泛化，公/私榜双升 | topic 665432 |
| ID 位移分析 + 尾部验证 + 加权/尾部 TE | 2nd | 权重 Tail 16×/Orig 8×/Head 1×；15 个单模 cutoff-AUC 台账（最强单模 nn_stacking 0.70616），Bagged HC 集成 **0.70771** | topic 665385 |
| 盲目 blender 批判 + 有原则的单模 | 社区 | 公开 notebook 过拟合 LB 的实证 | topic 651787 |
| 新手时间管理路线图（3–4 阶段） | 社区 | 前 2–3 天探索、编号实验、保存 OOF | topic 650676 |

## 4. 关键技巧

- **分布迁移侦探工作流**（本场可复用的最大资产）：对抗验证定位偏移 → 分箱观察 covariate/concept shift → 据此设计验证集与采样权重。
- 尾部 TE（只用 tail+orig 计算目标编码）、伪标签 + 分位数映射、以尾部均值为 margin 的残差提升（2nd 的单模清单）。
- **两条负结果（反直觉，值得记住）**：① "删掉高概念漂移特征"更安全是错的——lgb_safe 仅 0.67464，远低于 baseline 0.70435；② 单模伪标签在本场**低于**基线（0.70081/0.70231 vs 0.70435/0.70335）。
- **集成前先做互补性诊断**（盲融帖）：用 CDF + KS-stat 预判增益——同分低 KS 对（CatB/XGB，KS 0.0070）仅 +0.00016；低相关高 KS 对（XGB/RealMLP，Pearson 0.151、KS 0.0217）+0.00069，弱模拿 ~40% 权重，"分数相近才值得融"被证伪。
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

## 7. 图表证据（CDF 互补性诊断）

**图 1：CatB vs XGB（低 KS，低增益）** —— `intel/playground-series-s5e12/bodies/651787_img/01.png`

![CatB vs XGB CDF](../../intel/playground-series-s5e12/bodies/651787_img/01.png)

*读图*：两 CDF 几乎重合（Pearson 0.9893 / KS 0.0070）→ 集成增益 +0.00016。

**图 2：XGB vs RealMLP（高 KS，互补强）** —— `intel/playground-series-s5e12/bodies/651787_img/02.png`

![XGB vs RealMLP CDF](../../intel/playground-series-s5e12/bodies/651787_img/02.png)

*读图*：明显分离（Pearson 0.1507 / KS 0.0217），RealMLP 强于零类、XGB 强于正类 → 增益 +0.00069。**图中的 KS/Pearson 就是"该不该融"的预测量。**

## 8. 出处

- 1st：HC + Ridge 两阶段集成：https://www.kaggle.com/competitions/playground-series-s5e12/discussion/665432
- 2nd：基于 ID 位移分析的获胜法：https://www.kaggle.com/competitions/playground-series-s5e12/discussion/665385
- 数据被刻意破坏的发现：https://www.kaggle.com/competitions/playground-series-s5e12/discussion/652262
- 新手月赛路线图：https://www.kaggle.com/competitions/playground-series-s5e12/discussion/650676
