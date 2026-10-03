# Open Problems Multimodal 深读：稀疏计数表示 × 目标分解 × 域偏移与公榜污染

> 赛事：Featured ｜ 主题 science（单细胞多组学）｜ 1220 队 ｜ 标准赛 ｜ 指标：Mean Pearson（赛后经历数据更新/rescore，历史称 MeanPearsonOld）
> 材料基础：`digests/open-problems-multimodal.md`（6 篇：1st/2nd/3rd + 作弊事件帖 + 领域知识帖 + 上届冠军索引；80 条讨论索引）+ 15 张图（366961×11 / 366453×2 / 346888×2）
> 深读时间：2026-10（Tier A #36）

## 0. 一句话重述：这道题真正在考什么

题面是"两个逐细胞向量回归：Multiome（染色质可及性 DNA → RNA 表达）与 CITEseq（RNA → 蛋白）"，实际被考的是**稀疏计数数据的表示工程 + 域偏移下的验证设计**：

1. **表示是第一杠杆**：原始计数（counts）要经过"归一化（CLR / log1p / 行中位数）→ 稳定变换 → 低秩表示（SVD / LSI / tSVD）→ z-score"才能喂给 MLP/GBDT；3rd 说"preprocessing contributed greatly"，2nd 说 CLR 是"best normalization"。
2. **目标侧同样要分解**：1st 把 RNA 目标做 tSVD 插补 → 行归一 → 去列中位数 → 降到 128 维；用 MSE 在分解空间训练，再反变换回原空间用 correlation loss 对齐 Pearson——**优化空间与评估空间分离**。
3. **公榜不可信**：2nd 说"我们从头到尾公榜第一，却被时间域偏移洗掉"；3rd 训练了一个"测试数据来源分类器"，准确率高到直接判定"信任 LB 是危险的"。私榜含 unseen day+donor，验证必须按 donor/day 分组（out-of-day groupkfold）。
4. **赛事治理阴影**：最高票帖是"Massive and organized cheating"（147 票，付费保银牌广告 + 可疑队伍排名 20–37 + 账号行为模式）；另有"Leak in public test set"（94 票）与"Data Update and Rescore"（50 票）——本场是研究"榜单污染"的珍贵样本。

一句话：**这是一场"表示工程 + 验证设计"的比赛**——模型（MLP/CatBoost/LightGBM）都是标准件，名次由预处理与"信什么榜"决定；同时它也是 Kaggle 治理问题的经典案例。

## 1. 材料与角色

| 帖子 | 作者 | 票数 | 角色与独有信息 |
| --- | --- | --- | --- |
| [366313](https://www.kaggle.com/competitions/open-problems-multimodal/discussion/366313) Massive and organized cheating | — | 147 | 有组织作弊：小红书"保银牌"广告（失败不收钱、铜牌免费）；可疑队伍集中在 20–37 名；账号赛前只在随机帖发"Thank you!"类评论以脱离 novice 状态；呼吁收集证据 |
| [346888](https://www.kaggle.com/competitions/open-problems-multimodal/discussion/346888) 领域知识 | — | 132 | 中心法则 DNA→RNA→Protein；Multiome=ATAC→RNA、CITE=RNA→protein；提交格式（cell_id/gene_id → evaluations_ids.csv → sample_submission） |
| [366961](https://www.kaggle.com/competitions/open-problems-multimodal/discussion/366961) 1st | shu65 | 104 | 双管线 + tSVD 插补；CITE 基因选择（按 batch 相关性 + Reactome 通路）；目标分解 128 + 反变换；5 折按 donor+day；Optuna 80/20；集成（seed + batch 子集微调 + 全量预训练）；代码公开 |
| [348792](https://www.kaggle.com/competitions/open-problems-multimodal/discussion/348792) 上届冠军索引 | — | 96 | NeurIPS 2021 同题冠军录像 + 源码仓库；系列传承（同题二届） |
| [366453](https://www.kaggle.com/competitions/open-problems-multimodal/discussion/366453) 2nd | senkin | 95 | CLR 最优；4×LightGBM（不同特征）→ OOF → tSVD 作 NN meta；raw count 稀疏矩阵直接进 LGBM（feature_fraction 0.1）反哺 NN；BiGRU 替换/追加；cosine→MSE/Huber 多样性；ELU/Swish 处理负值；**"公榜从头到尾第一，但 time domain shift 不可预测"** |
| [366428](https://www.kaggle.com/competitions/open-problems-multimodal/discussion/366428) 3rd | makotu | 70 | BM25 替代 TF-IDF、LSI(muon) 降维；w2v/leiden/connectivity 特征；目标 SVD 128；~20 MLP + 3 CatBoost；**PB 相似度验证 + 测试来源二分类器（"信任 LB 危险"）**；自述无生物背景 |

**材料缺口（受"不扩采"约束，登记备查）**：Leak in public test set(349867,94 票)、Private 0.773 lessons(366395,76)、"It is a time series..."(363052,57)、7th(366471,55)、Exploiting the column names(349242,54)、364408(54)、12th(366455,53)、**Data Update and Rescore(350933,50)**、chronicles(348311,51)、ATAC-Gene 关联(349559,42) 等未收录正文——**泄漏机制、rescore 细节与中段名次方案是本次深读的三大信息缺口**。

## 2. 逐方案对照矩阵

| 维度 | 1st shu65 | 2nd senkin | 3rd makotu |
| --- | --- | --- | --- |
| 输入表示（Multiome） | TF-IDF（图 1）→ 预处理 → 模型 | CLR → tSVD → 行 z-score；raw counts；raw+raw target；log1p→tsvd（4 组特征喂 LGBM） | **BM25 替代 TF-IDF** → LSI(muon, 64 维) → 行 z-score |
| 补充特征 | 相关性选基因 + Reactome 通路（CITE） | 高相关原始特征；day-median 批次修正 | binary(16 SVD)、w2v 基因向量(16)、leiden 23 簇×16 SVD、连接矩阵 16 SVD |
| 目标预处理 | tSVD 插补 → log1p → 行归一 → 去列中位数 → tSVD 128；反变换 + 列中位数 | CLR/z-score；DSB（含负值） | SVD 128（MLP）；CatBoost 同目标 |
| 模型 | MLP + CatBoost（CITE 双管线）；GRU 未提 | **LightGBM（4 特征）→ meta tSVD → 双 NN**：BiGRU→Dense×2 / Dense×3→BiGRU | 4 层 MLP + CatBoost |
| 损失 | 分解空间 MSE + 原空间 correlation loss | cosine similarity → MSE/Huber（多模型多样性） | RMSE（multiome）/ correlation loss（cite） |
| 验证 | 5 折 group by donor+day；Optuna 80/20 | out-of-day groupkfold（逐特征检查每天都有增益）；早期 random kfold 与 LB 匹配是假象 | 10% "最接近 PB" 的训练数据作验证；测试来源二分类 |
| 集成 | seed 变化 + batch 子集微调（男/女/Day4,7）+ 全量预训练；推理取 5 预测均值 | 不同特征/损失/激活的 NN 与 LGBM | ~20 MLP + 3(2) CatBoost，CV 加权平均 |
| 公榜表现 | 冠军（私榜） | **公榜从头到尾第 1 → 私榜被洗** | 自述"最高 CV 的提交拿到最高私榜" |
| 代码 | GitHub 公开 | GitHub + notebook 公开 | GitHub + 数据集公开 |

## 3. 共识、分歧与裁决

### 共识一：预处理/表示是主杠杆（3/3）

3rd："Basically, pre-processing contributed greatly to the accuracy"；2nd：CLR 是最好的归一化（引 Nature 文章），并设计三路特征+批次修正；1st：整个 write-up 以 11 张预处理/结构图为主。

**裁决**：单细胞计数数据必须先做"文库归一 → 方差稳定变换 → 低秩表示 → 特征 z-score"；模型（MLP/CatBoost/LGBM）是标准件。置信度：高（三队独立）。

### 共识二：目标侧要分解 + 反变换（1st 完整给出，2nd/3rd 目标 z-score/SVD 同向）

1st：目标 tSVD 插补 → 128 维 SVD → 分解空间 MSE → 反变换 → 原空间 correlation loss；
3rd：目标 SVD 128 后 RMSE；
2nd：target z-score，DSB 目标含负值。

**裁决**：高维强相关输出先降维训练、再回到原空间评估，是"向量到向量回归"的通用结构——分解空间稳定可学，原空间指标（Pearson）决定选择。置信度：中高。

### 共识三：验证必须按 donor/day 分组，公榜只能确认不能选择（3/3 用不同方式表达同一结论）

1st：5 折按 donor+day 分组；
2nd：早期 random kfold 与 LB 匹配良好，但"time domain shift is unpredictable"，队内改用 out-of-day groupkfold 逐特征验证；
3rd：测试来源二分类准确率极高 → "dangerous to trust LB"，并用"最接近 PB 的 10% 训练数据"做验证。

**裁决**：本题 public/private 的划分（unseen donor vs unseen day+donor）制造了系统性域偏移；随机划分的 CV 与公榜相关性是伪相关。**私榜洗牌（2nd 从第 1 掉出）本身就是最强证据**。置信度：高。对照 T3/L6。

### 共识四：集成的多样性来自"表示/损失/结构"三处，而非规模（1st/2nd/3rd 都做异质集成）

1st：seed + batch 子集（男/女/Day4,7）+ 预训练来源；
2nd：4 组特征、余弦/MSE/Huber、BiGRU 前置/后置；
3rd：20 MLP + 2–3 CatBoost 的不同特征组合。

**裁决**：在低维表示上，小模型的误差去相关比单模型变强更值钱。置信度：中高。

### 分歧一：BM25 vs TF-IDF（3rd vs 1st 的输入表示）

3rd：用 Okapi BM25 替代 TF-IDF（+ muon 的 LSI）；
1st：Multiome 输入用 TF-IDF（图 1）。

**裁决**：BM25 的文档长度归一/词频饱和对稀疏计数更稳健，是 IR→生信迁移的具体实例；但 3rd 无消融，只能记为"值得尝试的替代表示"。置信度：中低。

### 分歧二：要不要 GRU/序列结构

2nd：BiGRU 替换第一层 Dense 或追加在最后，并配 cosine/MSE 双损失；
1st/3rd：纯 MLP/CatBoost。

**裁决**：并不矛盾——GRU 把"基因/特征序列"当有序序列建模，是特征次序先验；在 2 万级样本上，它与 MLP 属同一容量档，只是提供了集成多样性。置信度：中。

### 特别裁决：公榜污染的三重来源（作弊 + 泄漏 + 域偏移）

作弊帖（147 票）：有组织付费代打，指向 20–37 名段；
泄漏帖（349867，94 票，正文未收录）：公榜测试集存在信息泄漏；
域偏移（2nd/3rd）：public/private 的数据划分本身制造洗牌。

**裁决**：三者叠加使本场公榜几乎不可用于模型选择。对学习者的价值：**任何"公榜异常好但 CV 不涨"的改动都应按作弊/泄漏/偏移三类排查**，并以 private 与可复现性为最终依据。置信度：中高（证据帖 + 洗牌事实）。

## 4. 增量数字账

| 动作 | 数字 | 来源 |
| --- | --- | --- |
| 1st 验证 | 5 折 group by donor+day；Optuna 训练/验证 80/20 | 1st |
| 1st 目标链 | 行非零中位数归一 → log1p → tSVD 插补 → 行归一 → 去列中位数 → tSVD **n=128** → 反变换 + 列中位数 | 1st（图 3/5） |
| 1st CITE 基因选择 | 逐 batch 计算相关性，选多 batch 高相关基因；结合 Reactome 通路 | 1st |
| 1st 集成 | seed + batch 子集（男 only / 女 only / Day4,7 only）+ 全量预训练；推理 5 预测平均 | 1st |
| 2nd 预处理 | CLR（引 Nat Commun 2022）；sample 均值归一 + sqrt + z-score + day-median 批次修正；NN 前 row z-score | 2nd |
| 2nd LGBM 特征 | 4 组：lognorm+log1p→tsvd / raw→CLR→tsvd / raw / raw+raw target；**feature_fraction=0.1** | 2nd |
| 2nd NN | BiGRU+Dense×2（cosine, hidden 1800, GaussianDropout 0.2, ELU, lr 1e-3, Adam）与 Dense×3+BiGRU（MSE, hidden 1500, GDP 0.1, Swish, lr 5e-4, AdamW, target z-score）；均含伪标签 | 2nd（图） |
| 2nd 公榜 | "1st place of LB from start to end" → 私榜被洗 | 2nd |
| 3rd 表示 | BM25 → LSI **64 维**；binary 16 SVD；w2v 16 维（每细胞 top-100 基因）；leiden **23 簇** × 16 SVD；连接矩阵 16 SVD | 3rd |
| 3rd 模型 | 4 层 MLP（目标 SVD 128，RMSE）；multiome 约 20 MLP + 3 CatBoost；cite 约 20 MLP + 2 CatBoost；CV 加权 | 3rd |
| 3rd 验证 | 10% "接近 PB" 训练数据作验证；测试来源二分类"accuracy so high" | 3rd |

**结构校验（2 处吻合）**

1. 1st 的 Multiome/CITE 双管线在图中结构完全对称（输入→预处理→模型→输出→目标预处理→输出），与其"两条线独立"的自述一致；
2. 3rd 的 leiden 特征维度：23 簇 × 228942 特征 → SVD 16 → 23×16，与自述一致 ✓。

## 5. 机制推演

**M1｜稀疏计数为什么要"低秩表示 + 零位插补"**：scRNA/ATAC 的零值混合了"真实不表达"与"测序丢失"，直接回归会被零膨胀主导；tSVD 低秩重构给出零位的平滑估计（1st 的插补步骤），LSI/CLR 则通过变换让非零值的分布更接近可学的尺度。核心目标是把"离散计数"变成"连续低维信号"。

**M2｜目标分解训练 + 原空间评估的分离**：128 维 SVD 目标之间近似正交、尺度统一，MSE 稳定可收敛；但竞赛指标 Mean Pearson 定义在原空间（基因间相关），所以反变换后用 correlation loss 校准/选择。**"在好优化的空间训练、在要交卷的空间评估"**是本场最通用的结构（与检索赛的任务分解同族）。

**M3｜域偏移的两层结构**：public test 是 unseen donor（个体差异，1st 的 donor 分组覆盖）；private test 是 unseen day+donor（时间批次差异，2nd 的 out-of-day 覆盖）。random kfold 对两者都高估；"测试来源分类器准确率高"说明 public test 与训练分布在特征上可区分——**凡能轻易区分来源的切分，CV 就不可信**。

**M4｜批次修正的轻量做法**：2nd 的 day-median 减法（每个 batch 算列中位数得"中位样本"，从样本中减去）简单、低风险；1st 用 donor+day 分组验证而不是显式修正，3rd 用 leiden 簇均值平滑批次内的技术变异。三条路线都是"在不破坏生物信号的前提下压制技术噪声"。

**M5｜为什么小模型够用**：低秩表示已把每个细胞压到 64–128 维，样本量约 2 万级；任务近似"低维平滑回归"。此设定下容量收益有限，误差去相关（多损失/多结构/多子集）才是稳定的分数来源。GRU 只在"特征顺序有意义（基因序列/通路顺序）"时带来额外先验。

**M6｜公榜污染的识别信号**：① 公榜名次段异常聚集（20–37 名成片可疑）；② 账号历史只有无意义评论（伪装 contributor）；③ "改动只涨公榜不涨 CV"；④ 测试来源分类器高准确率（泄漏/重叠）。本场三帖（作弊/泄漏/rescore）共同说明：**榜单是外部状态，不是模型证据**——这也是 T3/L6/T10 的极端案例。

## 6. 证据分级

| 断言 | 等级 | 说明 |
| --- | --- | --- |
| 1st/2nd/3rd 方法与数字 | 自述 + 代码公开（1st/3rd GitHub，2nd notebook/GitHub） | 中高（可复现） |
| 公榜被域偏移洗牌 | 2nd 亲历 + 私榜结果 + 3rd 佐证 | 高 |
| 测试来源可分（3rd） | 单队分类实验（无数字） | 中 |
| "CLR 最佳归一化" | 2nd 自述（引论文） | 中 |
| BM25+LSI 优于 TF-IDF | 3rd 单队经验（无消融） | 中低 |
| 有组织作弊 | 证据帖（截图/账号模式）+ 129 评论 | 中（事实性强，官方处理未收录） |
| 公榜泄漏（349867） | 仅标题（正文未收录） | 低 |
| Data Update/Rescore | 仅标题（正文未收录） | 低 |

## 7. 边界条件与反事实

- **反事实 1**：若用随机 KFold → 早期 CV 与公榜相关良好，但私榜洗牌（2nd 亲历）；必须以 donor/day 分组。
- **反事实 2**：若不做目标变换/分解直接回归原始 counts → 零膨胀 + 尺度差异让 Pearson 极难优化；三队都做了变换（共同反证）。
- **反事实 3**：若以公榜做选择 → 2nd 的"全程第一"就是陷阱样本；只能用于确认无泄漏的单点改动。
- **反事实 4**：若移除作弊/泄漏污染 → 中段名次结构会变化；此类外部污染不可控，只能审计与上报。
- **边界**：本场结论依赖"训练与测试存在 day/donor 域划分"的赛制；同分布随机划分的比赛（如 jigsaw-acrc）中公榜仍可用（对照 T10 "由赛制决定"）。另外数据经历更新/rescore，历史分数（MeanPearsonOld）不可跨版本比较。

## 8. 悬案与失败学

**悬案**

1. **作弊事件的处理与影响名次未收录**：Kaggle 是否清榜、哪些队伍被处罚、奖牌是否重发——需要后续情报（当前只有指控与证据）。
2. **泄漏机制（349867）未收录**：public test 泄漏的具体形式（重叠细胞？元数据？）未知。
3. **Data Update and Rescore（350933）未收录**：数据更新与重算分的范围、对策略的影响未知。
4. "Exploiting the column names"（349242,54 票）未收录：特征名工程（cell_id/gene_id 模式）的具体收益不明。
5. 7th/12th 等中段方案未收录，无法验证"公榜可信度"在中段队伍的实际表现。

**失败学（跨队合集）**

- 验证类：random KFold（2nd 早期）→ 域偏移下失效；"信任公榜"（2nd/3rd 联手否证）。
- 表示类：不做目标变换/插补直接回归；把稀疏零当真实值。
- 模型类：在低秩表示上追求更大容量（1st/3rd 的小模型反证）。
- 治理类：参与付费代打（规则与信誉双重风险）；榜单异常段不要模仿。

## 9. 图表证据

> 路径相对本文件（`analysis/deep/`）：`../../intel/open-problems-multimodal/bodies/<topic>_img/NN.png`

**图 1：中心法则与两个子任务（领域知识帖）**（topic 346888）——`../../intel/open-problems-multimodal/bodies/346888_img/01.PNG`

*读图结论*：Multiome = 染色质可及性（DNA）→ 基因表达（RNA）；CITEseq = RNA → 蛋白水平；每行示例展示"向量的多个分量同时预测"。**整场比赛的领域坐标系**——向量到向量回归，而不是分类/单值预测。

**图 2：1st 的 Multiome 总管线**（topic 366961）——`../../intel/open-problems-multimodal/bodies/366961_img/01.png`

*读图结论*：输入是 TF-IDF 表示的染色质可及性 + 元数据（day、gender 等）；输出侧有独立的 Target preprocessing 作用于 RNA 目标。**"输入表示 + 元数据 + 目标变换"三要素结构**（CITE 管线同构，见图 6）。

**图 3：1st 的 Multiome 目标预处理链（含 tSVD 插补）**（topic 366961）——`../../intel/open-problems-multimodal/bodies/366961_img/03.png`

*读图结论*：RNA 原始计数 → 行非零中位数归一 → log1p → **用 tSVD 重构填充 0 位** → 行归一 → 减列中位数 → tSVD 降到 128 维。**"稀疏计数 → 稳定变换 → 零位插补 → 低秩分解"的标准链**，也是 M1 的直接图证。

**图 4：1st 的输出后处理与 Correlation Loss**（topic 366961）——`../../intel/open-problems-multimodal/bodies/366961_img/05.png`

*读图结论*：Linear（128 维）以 MSE 对分解目标训练 → 反变换回原空间 + 加回列中位数 → 与 library-size 归一后的 RNA 计算 **Correlation Loss**。**"分解空间训练 + 原空间评估"的双空间结构**（M2 的图证）。

**图 5：2nd 的完整管线（CLR + LightGBM meta + 双 NN/GRU）**（topic 366453）——`../../intel/open-problems-multimodal/bodies/366453_img/01.png`

*读图结论*：Raw Data 三路特征（CLR→tSVD→zscore；目标高相关特征→zscore；定制 tsvd&pca→zscore）→ LightGBM（预测→tsvd→zscore 作 meta）→ 两个 NN：NN1 BiGRU 前置（cosine loss、1800 hidden、ELU、lr 1e-3、Adam、拼接 3 隐藏层、伪标签）与 NN2 BiGRU 后置（MSE、1500 hidden、Swish、lr 5e-4、AdamW、target z-score、伪标签）。**"多表示 → 树 meta → 异质 NN"的集成结构与全部超参**一次呈现。

**图 6：1st 的 CITEseq 总管线**（topic 366961）——`../../intel/open-problems-multimodal/bodies/366961_img/07.png`

*读图结论*：RNA 表达 + 元数据（day、gender 等）→ 输入预处理 → 模型；RNA 目标经 Target preprocessing 参与训练（1st 此处做了按 batch 相关性 + Reactome 通路的基因选择，见正文）。**CITE 侧"元数据 + 目标基因筛选"的结构**。

## 10. 对既有笔记/playbook 的修订点

1. `notes/science/open-problems-multimodal.md` 升级（现为浅版）：补 6 篇作者/票数、三方案 × 10 维对照、数字账（tSVD 128、LSI 64、23 簇、BiGRU 双 NN）与 6 张图证；新增"公榜污染三重来源"节。
2. `playbook/science.md`（单细胞/组学节）增补：
   - **计数数据表示链**：文库归一 → 方差稳定（CLR/log1p/sqrt）→ 低秩（SVD/LSI/tSVD）→ z-score；
   - **零位插补**：tSVD 重构填充，区分"未观测"与"不表达"；
   - **目标侧双空间**：分解空间 MSE 训练 + 原空间 Pearson 评估（反变换 + 列中位数还原）；
   - **域偏移验证**：donor/day 分组；out-of-day groupkfold；"测试来源分类器"作泄漏检测；
   - **IR 迁移**：TF-IDF→BM25、SVD→LSI、基因序列 w2v。
3. `playbook/00-通用方法论.md` 增补：**"榜单是外部状态，不是证据"**（作弊/泄漏/域偏移三类污染 + 4 个识别信号）；**"在好优化的空间训练、在要交卷的空间评估"**。
4. `analysis/THEORY.md`（Batch 4 收尾扩 v0.4）候选：
   - **L54｜计数数据的表示链 + 零位插补**：证据 = 本场三队 + 上届同题；
   - **L55｜目标分解训练/原空间评估**：证据 = 1st 双空间图 + 检索赛的任务分解同构（llm-prompt-recovery 等）；
   - **L56｜可区分来源的切分不可信**：测试来源分类器准确率高 = CV 失效信号；证据 = 本场 3rd + 2nd 的洗牌；与 L6/T3/T10 同族；
   - 案例库条目：**榜单污染三件套（作弊/泄漏/rescore）**，登记为治理案例。

## 11. 出处

- 有组织作弊（147 票）：https://www.kaggle.com/competitions/open-problems-multimodal/discussion/366313
- 领域知识（132 票）：https://www.kaggle.com/competitions/open-problems-multimodal/discussion/346888
- 1st（shu65，104 票）：https://www.kaggle.com/competitions/open-problems-multimodal/discussion/366961
- 上届冠军索引（96 票）：https://www.kaggle.com/competitions/open-problems-multimodal/discussion/348792
- 2nd（senkin，95 票）：https://www.kaggle.com/competitions/open-problems-multimodal/discussion/366453
- 3rd（makotu，70 票）：https://www.kaggle.com/competitions/open-problems-multimodal/discussion/366428
- 缺口登记（未收录正文）：Leak in public test set(349867)、Private 0.773 lessons(366395)、It is a time series(363052)、7th(366471)、Exploiting the column names(349242)、364408、12th(366455)、Data Update and Rescore(350933)、 chronicles(348311)、ATAC-Gene(349559)
