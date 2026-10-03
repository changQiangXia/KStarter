# Playground Series S4E3（钢板缺陷预测）轻量深读（Tier B）

> 赛事：Playground ｜ 主题 tabular（7 个缺陷标签，多标签/多类混合）｜ 2199 队 ｜ 标准赛 ｜ 指标：Mean Columnwise AUC
> 材料基础：`digests/playground-series-s4e3.md`（6 篇正文：1st 488065 / 2nd 488106 / 3rd 488127 / 目标解释 481015 / 多标签讨论 480817 / BlueCast 482923；80 条主题索引）+ 0 张归档图
> 轻读时间：2026-10（Tier B B14）

## 1. 一句话重述与数字账

预测钢板表面缺陷的 7 个二元标签（Pastry / Z_Scratch / K_Scratch / Stains / Dirtiness / Bumps / Other_Faults），指标是 Mean Columnwise AUC。本场的核心是**多标签 vs 多类 vs 每标签独立二分类的形态选择**：原始 UCI 数据是多类（每行一个缺陷），竞赛合成数据几乎也是单标签（仅 **21 行**有两个标签）；1st 把 8 类 + 1 个噪声类做成 9 类多分类再加 8 个二分类后堆叠；2nd 用 4 个多类模型 + OOF 权重优化；3rd 则坚持多标签并称 CV/LB 略优。

| 关键数字 | 值 | 来源 |
| --- | --- | --- |
| 1st（488065） | **Noise Contrastive XGB**：4 个 XGB 做"原始 8 类 + 噪声第 9 类"的多分类；另建 8 个二分类 XGB；12 个模型堆叠（帖极短，无细节） | 488065 |
| 2nd（488106） | 合成 + 原始数据合并、**剔除多标签行**（占比极小）；3 个自造特征（比值、min-max 归一化、乘积）+ **丢掉 7 个特征**；4 个多类模型（XGB/LGBM/CatBoost/HGBC）× 10 折 + Optuna；用同折 OOF 做 3 模型 Nelder-Mead 权重优化；最后与公开提交按直觉权重（结果等权更有效）混合；自述"公开 notebook 等权混合"公 0.89684 / 私 0.88923；失败：伪标签、XGB 元堆叠、改用 roc_auc 指标 | 488106 |
| 3rd（488127） | 明确按**多标签**建模（CV 与公榜优于多类）；PyBoost + AutoGluon + 公开提交；"Mediocres et Impera"（取最信任的做平均）；选中提交私 0.88936（第 3），**未选的最佳私 0.88944（本可第 2）**；OpenFE 特征；失败：单模型、原始数据 | 488127 |
| 目标与数据（481015、480805） | 7 类缺陷定义（Pastry/Z_Scratch/K_Scratch/Stains/Dirtiness/Bumps/Other_Faults）；原数据是多类、竞赛数据"几乎"是多类；21 个多标签行不是噪声（485992） | 481015 / 480805 |
| 多标签方法论（480817） | 60 票帖整理"这到底是不是 multi-label"的历史讨论（S3E18 的"两个比赛合一"、多标签分层折、MultiLabel 模型清单等） | 480817 |
| 社区 | "有时候少即是多：丢掉 6 个特征"（33 票）；类别不平衡讨论（多条）；SigmoidOfArea 观察；随机种子影响；把 RF 加入集成反而变差（486429） | 索引 |

## 2. 逐方案对照矩阵

| 维度 | 1st | 2nd | 3rd |
| --- | --- | --- | --- |
| 问题形态 | 9 类多分类 + 8 二分类 | 多类（4 模型） | **多标签** |
| 原数据 | 用作分类来源 | 合并并剔多标签行 | 不用（自述无效） |
| 特征 | — | 3 个新特征、丢 7 个 | OpenFE |
| 融合 | 12 模型堆叠 | OOF Nelder-Mead + 等权公开混合 | PyBoost+AutoGluon+公开平均 |
| 私榜 | 1st | 2nd | 0.88936（3rd；未选 0.88944） |

## 3. 共识、分歧与裁决

### 共识一：先把"多标签/多类"的形态定下来（480817、480805、485992；置信度高）

原数据多类、竞赛数据几乎单标签（21 行多标签）；社区用 60 票帖讨论"是不是多标签"，2nd/1st 走多类、3rd 走多标签都能进前三。**裁决**：不要预设问题形态——先用多标签分层折 + 形态对照（多类 / 多标签 / 每标签二分类）确定建模结构。置信度：高。

### 共识二：特征精简（丢 6–7 个特征）+ 少量比值特征（2nd、社区；置信度中高）

2nd 丢掉 7 个特征并只加 3 个；社区"drop 6 features"帖 33 票。**裁决**：该数据集的特征冗余/噪声明显，先做减法。置信度：中高。

### 分歧一：原始数据用不用（2nd/1st vs 3rd；置信度中）

1st/2nd 用了原始数据（2nd 还剔除多标签行），3rd 明确说原数据无效。**裁决**：与 S3E17/S3E3 同型——原数据可用但必须以折内方式验证；本场差异可能来自用法（合并 vs 仅多类）。置信度：中。

### 共识三：公开 OOF/提交的等权混合已经很强（2nd、3rd；置信度中高）

2nd 的公开 notebook 等权混合公 0.89684/私 0.88923；3rd 也把公开提交作为组成部分。**裁决**：本场公开资产质量高；但 2nd/3rd 都出现"未选的最佳提交"，选择纪律仍是关键。置信度：中高。

### 技巧：noise contrastive 多分类（1st；置信度中）

给 8 个类别加一个"噪声"类做软对比，再与逐标签二分类堆叠。**裁决**：把"无缺陷/其他"显式建成一类，可让模型学到更清晰的类间关系；思路可迁移到多标签问题。置信度：中（原帖信息极少）。

## 4. 证据分级

| 断言 | 等级 | 说明 |
| --- | --- | --- |
| 2nd 的特征/集成/失败清单 | 自述（含代码链接） | 中高 |
| 3rd 的多标签对照与未选最佳提交 | 自述（含分数） | 中高 |
| 1st 的 noise-contrastive 结构 | 自述（极简，无细节） | 中 |
| 原数据多类 / 21 行多标签 | 多个讨论帖 | 中高 |
| 特征精简的增益 | 2nd + 33 票帖 | 中 |

## 5. 悬案与缺口（登记）

- 1st 的具体实现/分数未给出；4th–7th 未收录；
- 多标签行（21 个）如何处理最优未定论；
- SigmoidOfArea、随机种子等社区观察未展开；
- **图证缺口**：本场归档 0 图。

## 6. 图表证据

无可用图证（本场归档 0 图，图证缺口已登记）。

## 7. 出处

- 1st noise contrastive XGB（25 票）：https://www.kaggle.com/competitions/playground-series-s4e3/discussion/488065
- 2nd OOF 集成（57 票 / 23 评论）：https://www.kaggle.com/competitions/playground-series-s4e3/discussion/488106
- 3rd Mediocres et Impera（22 票 / 11 评论）：https://www.kaggle.com/competitions/playground-series-s4e3/discussion/488127
- 目标与特征解释（63 票 / 19 评论）：https://www.kaggle.com/competitions/playground-series-s4e3/discussion/481015
- 多标签 vs 多类讨论（60 票 / 30 评论）：https://www.kaggle.com/competitions/playground-series-s4e3/discussion/480817
- 原数据是多类（25 票）：https://www.kaggle.com/competitions/playground-series-s4e3/discussion/480805
- 丢掉 6 个特征（33 票）：https://www.kaggle.com/competitions/playground-series-s4e3/discussion/482401
- 21 个多标签行不是噪声（5 票）：https://www.kaggle.com/competitions/playground-series-s4e3/discussion/485992
