# TPS Dec 2021 深读：物理范围修复 × 合成数据过拟合陷阱 × 公开 blend 的马戏团

> 赛事：Playground ｜ 主题 tabular（多分类）｜ 1188 队 ｜ 标准赛 ｜ 指标：Categorization Accuracy（7 类森林覆盖类型）
> 材料基础：`digests/tabular-playground-series-dec-2021.md`（6 篇正文：TPS 教训 116 / 特征修复 62 / 2nd 54 / 2021 解法索引 51 / focal loss 23 / 收官祝贺 13；80 条主题索引）+ 0 张可用归档图（293072_img 为空目录，HTML 内 1 个 `<img>` 未下载）
> 深读时间：2026-10（Tier A #60，Batch 6 收官场）

## 0. 一句话重述：这道题真正在考什么

题面是"预测森林覆盖类型（7 类，Accuracy）"，数据是用 CTGAN 类生成器对 UCI Covertype 原始数据做的**合成副本**——真正的考题是**在"字段有物理含义"的合成数据上，区分"物理修复"与"分布还原"**：

1. **物理范围审计 = 全场最大单点增益**：`Aspect`（罗盘角）出现 (-360,720) 区间外的越界值，按 0–359 循环量修正（±360）；三个 `Hillshade`（灰度）越界 → 截断到 [0,255]；负距离 → 置 0。社区爆款帖（62 票）报告同一网络即 **0.95631→0.95656→0.95673**；评论区另一独立验证（负距离置 0）**+0.0053**。
2. **"把合成数据改得像原始数据"是过拟合陷阱**：2nd（54 票）自述数十次尝试（把竞赛数据向原始 Covertype 靠拢、额外裁剪、土壤掩码——"某些树根本不在某些土壤上生长"）**CV 极好但测试失败**；最终只有**欧氏距离、曼哈顿距离、Aspect 修复**幸存。裁决规则：**修复物理上不可能的值 = 收益；强制还原原始分布 = 损失**。
3. **单模会收敛到同一处 → 多样性只能人为制造**：2nd 观察到"几乎所有模型架构收敛结果相同"，突破口是 (a) 10 个最优模型的 soft voting；(b) **同架构、不同 batch_size** 的再投票。最终名次由"自己的 0.9707 模型 ×3 + 三个他人已验证模型（去伪标签）"的务实 blend 拿到第 2。
4. **公开 notebook 经济的饱和效应**：2nd 两次被"30 人复制同一 notebook / 几十人复制同一 blend 冲到 0.9709–0.9711"打到心态——Playground 的公开复现速度让分数快速饱和；差异化只剩"自己独有的强单模"或"精选+去伪标签的策展能力"。
5. **方法论层**：116 票的年度教训帖给出可迁移原则（90% 数据 / 9% 模型 / 1% 调参；先有模型再调参；EDA 必须回答"so what"；看 fork 数而非票数）；focal loss 帖给出不平衡数据的损失级方案；2021 全年 TPS 解法索引帖是跨场谱系素材。

一句话：**这是一场"物理审计 + 抗同质化 blend + 公开代码策展"的比赛**——特征修复决定入场，差异化和伪标签判断决定名次。

## 1. 材料与角色

| 帖子 | 作者 | 票数 | 角色与独有信息 |
| --- | --- | --- | --- |
| [296842](https://www.kaggle.com/competitions/tabular-playground-series-dec-2021/discussion/296842) TPS 2021 教训 | Remek Kinas | 116 | 全场最高票的方法论帖：练习/数据优先（90-9-1）/解法比想象简单/实验证伪/别过早调参/EDA 要有 so what/看 fork 数；"一年进 Top100 是可能的" |
| [293373](https://www.kaggle.com/competitions/tabular-playground-series-dec-2021/discussion/293373) 修复这四列 | Gulshan Mishra | 62 | **全场最大单点**：Aspect ±360 循环修正 + 三 Hillshade 截断；同网络 0.95631→**0.95656→0.95673**；评论区扩展出负距离→0（+0.0053）与 CTGAN bounds=None 的成因讨论 |
| [298304](https://www.kaggle.com/competitions/tabular-playground-series-dec-2021/discussion/298304) 2nd | SSS（sergiosaharovskiy） | 54 | 完整叙事：向原始数据靠拢的数十次失败（CV 好/测试崩）→ 只有距离特征+Aspect 修复幸存；10 模型 soft voting 与 batch_size 扰动两次突破；两次被复制党打击；伪标签对己无效；最终=自己 0.9707×3 + 3 个公开模型（去伪标签）；Graphviz 实验树 |
| [294062](https://www.kaggle.com/competitions/tabular-playground-series-dec-2021/discussion/294062) 2021 Tabular 解法索引 | Vadim Irtlach | 51 | 1–11 月 TPS 冠军/前列解法全链接（Jan–Nov）——**跨场方法谱系素材**（lineage 阶段用） |
| [293072](https://www.kaggle.com/competitions/tabular-playground-series-dec-2021/discussion/293072) Focal loss | Luca Massaron | 23 | 不平衡多分类的损失级方案：改 loss 而非重采样/加权；gamma 强调难样本；附 TF/Keras 多类 focal loss notebook |
| [298131](https://www.kaggle.com/competitions/tabular-playground-series-dec-2021/discussion/298131) 收官祝贺 | Luca Massaron | 13 | "巨大的 shake-up"；伪标签分歧现场：2nd 说无效、kaaveland 说他的版本有帮助（公 0.95697/私 0.95669，属早期模型代际）；Aspect 离散化+Top10 线性特征=999/1200 的民间记录 |

**材料缺口（受"仅 ≤3 篇场次定点补采"约束，登记备查）**：**1st/3rd 方案未收录**；高价值讨论未收录——[293373](https://www.kaggle.com/competitions/tabular-playground-series-dec-2021/discussion/293373) 的"Yet another score booster"（22 票）、[291844](https://www.kaggle.com/competitions/tabular-playground-series-dec-2021/discussion/291844) 缩减数据规模（56 票）、[293612](https://www.kaggle.com/competitions/tabular-playground-series-dec-2021/discussion/293612) 特征工程更新线程（47 票）、[292823](https://www.kaggle.com/competitions/tabular-playground-series-dec-2021/discussion/292823) Soil_Type+Wilderness_Area 求和（46 票）、[291871](https://www.kaggle.com/competitions/tabular-playground-series-dec-2021/discussion/291871) 不平衡处理（34 票）、[291832](https://www.kaggle.com/competitions/tabular-playground-series-dec-2021/discussion/291832) Covertype 原始数据指南（29 票）、[293362](https://www.kaggle.com/competitions/tabular-playground-series-dec-2021/discussion/293362) "不该用 accuracy"（29 票）、[292381](https://www.kaggle.com/competitions/tabular-playground-series-dec-2021/discussion/292381) "Train 和 test 不重叠"（23 票）、[292839](https://www.kaggle.com/competitions/tabular-playground-series-dec-2021/discussion/292839) 伪标签（23 票）、[295617](https://www.kaggle.com/competitions/tabular-playground-series-dec-2021/discussion/295617) 赛程过半的关键证据（24 票）。图证：293072_img 为空目录（`<img>` 未下载）。

## 2. 逐方案对照矩阵

| 维度 | 2nd（SSS） | Gulshan（62 票） | 社区其他 |
| --- | --- | --- | --- |
| 物理审计 | Aspect 修复（幸存）；额外裁剪/土壤掩码失败 | **Aspect ±360 + 三 Hillshade 截断**（0.95631→0.95673） | 负距离→0（+0.0053）；Aspect 离散化+Top10 线性特征（999/1200） |
| 向原始 Covertype 靠拢 | 数十次实验失败（CV 好/测试崩） | —（评论区讨论 CTGAN bounds=None 成因） | 土壤掩码等"领域正确"改法失败 |
| 距离特征 | **欧氏+曼哈顿距离（幸存）** | — | — |
| 模型 | 最优单模 0.9707；col_drop=['Id','Soil_Type7','Soil_Type15'] | TensorFlow NN | SeLU 网络、XGB/LGBM/CatBoost 各类 |
| 多样性 | 10 模型 soft voting；同架构不同 batch_size 再投票 | — | focal loss 处理不平衡；伪标签（争议） |
| 最终提交 | 自己 0.9707×3 + mlanhenke×1 + kaaveland×3 + ambrosm×2（去伪标签） | — | 多人复制同一 blend 达 0.9709–0.9711 |
| 态度/教训 | 两次被复制党打击；"实验树"管理；伪标签对己无效 | 分享修复细节 | "不该用 accuracy"的指标批评；shake-up |

## 3. 共识、分歧与裁决

### 共识一：物理范围审计是最高性价比动作（独立三处验证）

Gulshan（四列修复，0.95631→0.95673）、Samuel（负距离→0，+0.0053）、2nd（Aspect 修复是唯一幸存的"特征工程"）。**裁决**：非匿名化字段的比赛，第一步永远是"逐列物理范围审计"（循环量/灰度/距离/比例），修越界值几乎无成本、无过拟合风险。置信度：高。

### 共识二：合成数据的"领域还原"会过拟合（2nd + 评论区）

2nd 的数十次失败+土壤掩码失败+额外裁剪失败；评论区讨论 CTGAN `min_value/max_value=None` 是越界值的来源，"把数据拉回原始范围"改变了与测试分布的一致性。**裁决**：**修不可能值（局部、物理）有用；重造分布（全局、领域）有害**——两者必须分开决策。置信度：高。

### 共识三：单模同质化 → 必须人为制造多样性（2nd 的实证）

"几乎所有架构收敛相同"；突破口是 10 模型 soft voting 与 **同架构不同 batch_size** 的扰动投票。**裁决**：当模型家族收敛到同一解，多样性应来自训练扰动（batch/seed/采样）与跨家族混合，而不是继续加特征。置信度：高（单队强证据 + 与其它场软投票结论一致）。

### 分歧一：伪标签是否有效

2nd：自己的模型加伪标签**只变差**，最终版本剔除所有伪标签成分；kaaveland：他的版本伪标签"有帮助"（公 0.95697/私 0.95669，属早期代际，不能与 0.9707+ 代际直接比较）；收官帖主持人猜测"前排没用伪标签"。**裁决**：伪标签在合成数据上风险更高（会放大生成器伪影/训练-伪标签偏差），**对前排方案默认不用**；要用必须做"同代际消融"。置信度：中高。

### 分歧二：accuracy 是否是合适指标

社区帖（29 票）"我们真不该用 accuracy"——7 类不平衡、accuracy 奖励多数类；但赛制已定，后排方案无法改变。**裁决**：把指标批判转化为策略——用按类别的诊断（ambrosm 的"Eliminate cover type 4!"模型就是类级专门化）与 blend 来缓解；不要只盯总分。置信度：中。

### 分歧三：公开代码的价值与副作用

2nd 被"30 人复制同一 notebook""几十人复制同一 blend"两次打击；同时他最终 blend 也依赖 3 位公开作者（mlanhenke/kaaveland/ambrosm）的模型。**裁决**：Playground 生态里公开代码是**公共品 + 军备竞赛**双重角色；个人的最优策略是"独有强单模 + 对公共品做去伪标签/加权策展"，而不是参与无差别复制。置信度：中高。

## 4. 增量数字账

| 动作 | 数字 | 来源 |
| --- | --- | --- |
| 物理修复（Gulshan） | 同 NN：0.95631 → 0.95656（四列修复）→ **0.95673**（minor change） | 293373 |
| 负距离修复（Samuel） | 置 0：**+0.0053** | 293373 评论 |
| 2nd 幸存特征 | 只有欧氏距离、曼哈顿距离、Aspect 修复；土壤掩码/额外裁剪/原始数据靠拢（数十次实验）全部失败 | 298304 |
| 2nd 突破 | 10 模型 soft voting；同架构不同 batch_size 再投票；col_drop=['Id','Soil_Type7','Soil_Type15']；单模最好 0.9707 | 298304 |
| 2nd 终版 | 自己 0.9707×3 + 1+3+2 个公开模型（去伪标签）；两次被复制党超越（0.9709–0.9711） | 298304 |
| 伪标签分歧 | 2nd：变差；kaaveland：有帮助（公 0.95697/私 0.95669，早期代际）；主持人猜测前排不用 | 298131 |
| 民间记录 | Aspect 离散化 + Top10 线性特征：999/1200 | 298131 评论 |
| 教训帖数据观 | 90% 数据 / 9% 模型 / 1% 调参；有比赛生成 60+ notebook；看 fork 数 | 296842 |
| 赛事 | 1188 队；7 类；Accuracy；收官"巨大 shake-up" | 元数据+298131 |

**结构校验（2 处吻合 + 1 处口径限制）**

1. Gulshan 的"修复四列 → +0.00025/+0.00017"与 Samuel"负距离→0 → +0.0053"同向（物理修复为正收益），量级差异来自修复列的影响面 ✓；
2. 2nd 的"单模收敛一致 → 软投票突破"与其"最优单模 0.9707、最终 blend 击败 0.9709–0.9711 复制党"的叙事自洽 ✓；
3. ⚠ kaaveland 的 0.95697/0.95669 与 2nd 时代的 0.9707+ 不可直接比较（早期代际），伪标签结论按"同代际消融缺失"登记。

## 5. 机制推演

**M1｜合成数据的物理伪影为什么可修复且高收益**：CTGAN 类生成器按数值边缘分布采样，无法表达"角度是循环量""灰度有界""距离非负"这类**约束语义**；越界值对树/NN 都是分布外输入，模型要为它们浪费容量或产生偏差。做一次确定性的物理映射（循环折叠/截断/取非负）等价于把生成器没学到的约束补回去，且不改变测试分布的主体。**推论**：非匿名化 Playground 赛的第一步是"约束审计"。

**M2｜为什么"向原始数据靠拢"反而过拟合**：合成训练/测试共享同一个生成器过程；把训练特征改成原始 Covertype 的领域形态（土壤掩码等）等于在训练分布上引入与测试不一致的变换——CV 评估的是"变换后的合成训练集"，LB 评估的是"原始合成测试集"，两者错位。**推论**：区分"修复（去伪影）"与"还原（换分布）"，只在后者做 CV-LB 一致性检验。

**M3｜软投票 × 同架构扰动的机制**：合成数据的多分类边界由大量近等价解组成，单模选择噪声大；soft voting 平均概率降低方差；batch_size 扰动改变优化轨迹/正则化强度，制造"同族弱相关模型"——比跨家族模型更便宜且足够多样。**推论**：当特征工程收益枯竭时，训练扰动是最后一块稳定增量。

**M4｜公开 notebook 经济的饱和动力学**：一个强 notebook 被复制 N 次 → 榜单分数快速饱和（0.9709–0.9711）→ 名次差异变成"谁发现了额外的小增量"（物理修复、类级模型、blend 权重、去伪标签）。2nd 的"如果打不过就改进它"（把公共 blend 去伪标签并与自己的强单模混合）是理性博弈解：**公共品 + 私有强模 = 差异化最大化的组合**。

**M5｜伪标签在合成数据上的双重性**：伪标签利用测试输入的自监督一致性，可降低方差；但若教师模型拟合了生成器伪影，伪标签会把伪影"固化"进学生模型——在合成数据（伪影密集）上风险放大。2nd 的 0.9707 级模型变差、kaaveland 早期模型受益，符合"教师越强、伪影越多、收益越不确定"的假设。**推论**：伪标签必须与"教师质量/代际"绑定做消融，不能用跨代际成功案例做依据。

**M6｜Accuracy 指标下的类级策略**：7 类不平衡时，总分提升可能来自少数类的正确率变化；ambrosm 的"Eliminate cover type 4!"暗示对特定类做专门处理（剔除/重训/单独模型）能改善整体 blend。**推论**：不平衡分类的 blend 应按"类级一致性"选模型，而非只看总分。

**M7｜学习方法的复利**：116 票教训帖的核心不是技巧而是**流程**（实验证伪、数据优先、不过早调参、fork 数衡量影响力、聚焦）。与本场的技术结论互补：物理修复来自"知道数据在说什么"，而这一步只能被"领域审计流程"发现。

## 6. 证据分级

| 断言 | 等级 | 说明 |
| --- | --- | --- |
| 四列修复与分差（0.95631→0.95673） | 自述 + 公开 notebook + 评论独立复现 | 中高 |
| 负距离→0 增益 +0.0053 | 评论区自述 | 中 |
| 2nd 的失败/突破/终版组成 | 详细自述 + 公开 notebook 链接 + 树状实验管理 | 中高 |
| Batch_size 软投票突破 | 自述 | 中 |
| 伪标签分歧 | 双方评论（2nd vs kaaveland） | 中（跨代际，不可比） |
| "巨大 shake-up" | 主持人收官帖 | 高（事实） |
| 2021 TPS 解法索引 | 逐月链接（可核对） | 高（索引层面） |
| 教训帖原则（90-9-1 等） | 个人经验/观点 | 中 |
| 1st/3rd 方法、accuracy 指标讨论、伪标签主帖 | 未收录 | —（缺口） |

## 7. 边界条件与反事实

- **反事实 1（不做物理修复）**：Gulshan 停在 0.95631；Samuel 少 +0.0053；2nd 失去唯一幸存特征——在 0.97 级名校逐 0.0001 的赛末，这可能就是金/银边界。
- **反事实 2（继续"向原数据靠拢"）**：CV 会继续变好、LB 继续变差（2nd 的数十次失败）——这是"合成数据分布错位"的教科书案例。
- **反事实 3（不做训练扰动多样性）**：单模收敛一致 → 无法产生 blend 增益；2nd 的两个突破都不存在。
- **反事实 4（排斥公共品）**：2nd 若不采用 public 模型，只有 0.9707×3；若全盘复制（含伪标签），则跟随 0.9709–0.9711 的大流并可能被伪标签拖累。**去伪标签的策展组合**才是第 2 的路径。
- **反事实 5（伪标签做同代际消融）**：分歧本可被解决；本场没人给出"同代际 A/B"数字，因此结论只能保守。
- **边界**：全部结论依赖"字段非匿名化 + 数据为生成器合成 + 指标 accuracy + 公开 notebook 文化"。匿名化表格赛无法做物理审计；非合成数据无此伪影结构。

## 8. 悬案与失败学

**悬案**

1. **1st/3rd 方案未收录**：无法确认冠军是否也依赖物理修复与去伪标签（收官帖暗示前排不用伪标签）。
2. **"Train 和 test 数据不重叠"（292381，23 票）**：这帖的上下文（是否指合成数据无泄漏）未收录——影响"能否用泄漏类技巧"的判断。
3. **"不该用 accuracy"（293362，29 票）**：具体替代指标与论证未收录。
4. **"Yet another score booster"（293768，22 票）**：Gulshan 提到的另一处修复/增益未展开。
5. **shake-up 的成因**：收官"巨大 shake-up"与伪标签/公共 blend 的关系未量化。
6. **图证缺失**：293072_img 为空目录（HTML 内 1 个 `<img>` 未下载）。

**失败学（跨队合集）**

- 2nd：向原始 Covertype 靠拢（数十次实验，CV 好/测试崩）；土壤掩码；额外裁剪；伪标签（自己的模型变差）；一度想放弃；被复制党两次打击（组织层面）。
- Gulshan：早期 NN 基线 0.95631；未做修复前收益为 0。
- 社区：accuracy 指标对不平衡不友好；伪标签缺乏同代际验证；SeLU/距离特征之外的特征工程大面积无效（2nd 的观察）。
- 公开生态：复制同一 notebook/blend 导致分数饱和与名次噪声（既是"失败"也是环境事实）。

## 9. 图表证据

**本场无可用归档图片**：`293072_img/` 为空目录（293072.html 内有 1 个 `<img>` 标签但未落盘）；其余 5 个 HTML 无 `<img>`。按"只用仓库内已归档图片"约束，本场无法内嵌图证；图证缺口已登记（阶段二图片层可复核）。全部证据来自正文数字与跨篇对照。

## 10. 对既有笔记/playbook 的修订点

1. `notes/tabular/tabular-playground-series-dec-2021.md` 升级：补 6 篇作者/票数、2nd+社区三路对照、数字账（0.95631→0.95673、负距离 +0.0053、0.9707×3+公共模型、伪标签分歧）、机制 M1–M7、失败学与缺口（含图证缺失）。
2. `playbook/tabular.md`（Playground/合成数据节）增补：
   - **物理范围审计清单**：循环量（角度）±360、有界灰度 [0,255]、非负距离、比例约束——先修值，不造分布；
   - **修复 vs 还原的判据**：局部去伪影可做；全局向原始分布靠拢禁用（CV 会骗你）；
   - **同质化对策**：soft voting + 同架构 batch_size/seed 扰动；
   - **公共代码策展**：去伪标签、去低质成分后与私有强单模混合；
   - **伪标签纪律**：同代际消融才可信；合成数据默认保守。
3. `playbook/00-通用方法论.md` 增补：**"先做字段约束审计，再谈特征工程"**；**"CV 好/测试崩 = 训练分布被改动的警报"**；**"公开 notebook 饱和环境下的差异化公式：公共品策展 × 私有强单模"**。
4. `analysis/THEORY.md`（Batch 6 末汇总 v0.6）候选：
   - **L110｜合成数据物理修复律**（修约束语义值=稳定正收益；证据 = Gulshan/Samuel/2nd）；
   - **L111｜修复-还原分离律**（局部修复 vs 全局还原的 CV-LB 行为相反；证据 = 2nd 的数十次失败）；
   - **L112｜同质化环境多样性律**（单模收敛一致时，训练扰动软投票 > 新特征；证据 = 2nd 的两个突破）；
   - **L113｜公开代码策展律**（饱和榜单中，去伪标签的公共 blend + 私有强单模是最大化差异化的组合；证据 = 2nd 终版与复制党现象）。

## 11. 出处

- TPS 2021 教训（116 票）：https://www.kaggle.com/competitions/tabular-playground-series-dec-2021/discussion/296842
- 修复四列特征（62 票）：https://www.kaggle.com/competitions/tabular-playground-series-dec-2021/discussion/293373
- 2nd 方案（54 票）：https://www.kaggle.com/competitions/tabular-playground-series-dec-2021/discussion/298304
- 2021 Tabular 解法索引（51 票）：https://www.kaggle.com/competitions/tabular-playground-series-dec-2021/discussion/294062
- Focal loss（23 票）：https://www.kaggle.com/competitions/tabular-playground-series-dec-2021/discussion/293072
- 收官祝贺（13 票）：https://www.kaggle.com/competitions/tabular-playground-series-dec-2021/discussion/298131
- 未收录正文的关键讨论（真实 topic id，供后续定点补采/图片层参考）：293768、291844、293612、292823、291871、291832、293362、292381、292839、295617
