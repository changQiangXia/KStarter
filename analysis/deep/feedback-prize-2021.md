# Feedback Prize 2021 深读：两级架构 × 跨域融合

> 赛事：Featured ｜ 主题 nlp ｜ 2058 队 ｜ 代码赛 ｜ 指标 TextOverlapF-beta（跨度重叠，≥50% 重叠计对）（2022-03-15 截止）
> 材料基础：`digests/feedback-prize-2021.md`（8 节正文：1st/2nd/3rd/4th/6th + NER starter + 相关赛事汇总 + hengck23 见解）+ 9 张图
> 深读时间：2026-10（Tier A #12）

## 0. 一句话重述：这道题真正在考什么

题面是"在学生作文里圈出 7 类论述要素"，实际被考的是**把跨度抽取拆成"局部 token 模型 + 非局部跨度决策"的两级系统**，并用**跨领域（目标检测）的融合技术**把多个异质模型拼起来。降解为 5 步：

1. **token 级神经模型**：长文本（1536–2048 token）上的 token classification（BIO），解决"每个位置像什么"；
2. **跨度级决策**：把 token 概率转成候选跨度特征，用 **GBM 堆叠**做每类二分类/长度修正——处理 token 模型看不见的非局部信息（边界稳定性、全局布局、类间竞争）；1st 的 +0.036 CV 全在这一步；
3. **跨模型/跨分词器融合**：不同 backbone 的 tokenizer 不同、subword 不可直接平均 → **跨度级融合**（WBF 平均起止位置 / 实体级 50% 重叠分组平均），tokenizer 无关；
4. **指标感知的后处理**：指标只要求 50% 重叠 → 修复断链跨度、按类规则合并/去重（Lead/Position/Concluding 至多一个）、按预测长度调整边界（Evidence <45 词则前移起点 9 词）；
5. **工程细节**：offset_mapping（保留换行 `\n`）> word_ids；BIO 序列有转移约束 → beam search 解码；长文本模型的配置改造（DeBERTa 任意长度、Funnel 改 max_position、BigBird 全注意力、LSG 把 512 扩到 1536）。

一句话：**这道题是"span = box"这一跨域类比的全家桶**——token 模型决定上限，span 级融合与后处理决定名次。

## 1. 材料与角色

| 帖子 | 作者 | 票数 | 角色与独有信息 |
| --- | --- | --- | --- |
| [295794](https://www.kaggle.com/competitions/feedback-prize-2021/discussion/295794)（NER starter，296 票） | Chris Deotte | 296 | 把任务形式化为 **segmentation（NER）vs detection（QA/框）** 的教材；Longformer/BigBird starter（0.595–0.630）；"断网提交"工作流 |
| [313177](https://www.kaggle.com/competitions/feedback-prize-2021/discussion/313177)（1st） | (⊙﹏⊙) | 282 | **两级架构的量级证据**：stage1 五模型集成 0.712 → stage2 LGB 跨度堆叠 0.748（+0.036）；170 特征、300 万召回样本 |
| [313389](https://www.kaggle.com/competitions/feedback-prize-2021/discussion/313389)（2nd） | Chris Deotte + Chun Ming + Udbhav | 203 | **后处理（~+0.008 CV）+ WBF 融合**（平均 0.700 → 0.741）；10 backbone × 3 折 = 27 模型 8h30m 提交 |
| [313424](https://www.kaggle.com/competitions/feedback-prize-2021/discussion/313424)（6th） | tascj | 165 | **YOLO 式跨度检测器**：objectness + 2 回归 + 分类；RoIAlign 聚到词级；NMS 后处理；自承 WBF 本地失败 |
| [313330](https://www.kaggle.com/competitions/feedback-prize-2021/discussion/313330)（4th） | Jungwoo Park | 149 | **分词器与解码细节**：offset_mapping 0.630 vs word_ids 0.595；\n 保真修复 DeBERTa-v2/v3；beam search；**实体级融合 +0.002** |
| [308992](https://www.kaggle.com/competitions/feedback-prize-2021/discussion/308992)（见解帖，147 票） | hengck23 | 147 | 题目层面的"作弊线索"：私榜与训练同主题（15 个）、claim/counterclaim 由位置决定、PERSUADE 语料——**主题先验未被充分利用** |
| [313235](https://www.kaggle.com/competitions/feedback-prize-2021/discussion/313235)（3rd） | Shujun + aerdem4 + thedrcat | 72 | **滑窗 DeBERTa 的最完整实现**（window 512/步进 384/保留中段 64:448）+ GRU 缝合；堆叠框架的工程改进（RAPIDS） |
| [295193](https://www.kaggle.com/competitions/feedback-prize-2021/discussion/295193)（相关赛事汇总） | Jonathan Besomi | 69 | 把本场放进"文本抽取/分类"的赛事谱系（CommonLit、Tweet Sentiment、Google QUEST、TPU QA） |

**材料缺口（未扩采，登记备查）**：索引里另有 15 条 write-up 未收录，含 [9th "deberta is the king"（313201）](https://www.kaggle.com/competitions/feedback-prize-2021/discussion/313201)、[10th（313718）](https://www.kaggle.com/competitions/feedback-prize-2021/discussion/313718)、[11th（313184）](https://www.kaggle.com/competitions/feedback-prize-2021/discussion/313184)、[8th（316071）](https://www.kaggle.com/competitions/feedback-prize-2021/discussion/316071)、[55th "Shortformer+滑窗+主题后处理"（313229）](https://www.kaggle.com/competitions/feedback-prize-2021/discussion/313229)、[12th 短跨度拉伸（313833）](https://www.kaggle.com/competitions/feedback-prize-2021/discussion/313833)、[全解汇总帖（313242）](https://www.kaggle.com/competitions/feedback-prize-2021/discussion/313242) 等。

## 2. 逐方案对照矩阵

| 维度 | 1st (⊙﹏⊙) | 2nd Chris 队 | 3rd Shujun 队 | 4th Jungwoo | 6th tascj |
| --- | --- | --- | --- | --- | --- |
| 核心范式 | token 集成 + **LGB 跨度堆叠**（两级） | 10 backbone 大集成 + **WBF 融合** | Longformer + 滑窗 DeBERTa-xl + **GBM 堆叠** | DeBERTa 家族多模型 + **实体级融合** | **YOLO 式检测**（objectness+回归+分类） |
| 长文本方案 | 分段拼接（512 模型）；longformer 直用 | 全部 1536（bigbird 1024）；Funnel 改配置、BigBird 全注意力、YOSO 关 lsh_backward | max_len 2048（再大退化）；滑窗 512/步进 384/取中段 | offset_mapping 重建子词标签 | RoIAlign token→word |
| 序列头 | token 分类 | token 分类 | transformer + **2 层 GRU** | token 分类 + **beam search 解码** | 1+2+7 头，词级聚合 |
| 关键特征/损失 | 170 特征（stage2）；AWP/FGM | 每模型 CE；PP 规则 | ~25 特征/类；instability=prob 差分平方均值 | 同 | 正样本=首词+最低代价词（YOLOX 思路） |
| 融合方式 | 概率平均 → LGB | **WBF 平均起止** | GBM 排序 + 允许 0.2 重叠解码 | **≥50% 重叠分组后平均起止** | 权重平均；NMS；自承 WBF 失败 |
| 后处理 | 采样选择（边界阈值+65% 长度）| 断链修复/至多一个类/长度调整 | 特征选择 + 解码重叠放宽 | beam search 修 BIO 合法性 | 仅 NMS |
| 成绩 | CV 0.748 / LB 0.742 | CV 0.741 / 公开 0.727 / 私榜 0.740 | CV≈0.7322（公开 notebook） | 公开 0.721–0.724 / 私榜 0.735 | 验证 0.723 / 公开 0.714 / 私榜 0.732（混合） |

## 3. 共识、分歧与裁决

### 共识一：两级架构（token 模型 → 跨度级决策）是本场的标准答案

1st 给出量级：stage1 五模型集成 CV 0.712/LB 0.706（含 PP）→ stage2 LGB 0.748/0.742，**两级差 +0.036**；把 LGB 直接套在 5 折 longformer 上：0.697→0.727（+0.030）。3rd 的整个堆叠框架（chase bowers 起源）逐类训练 7 个 GBM 二分类器；1st 的召回表显示候选召回 89.5%–97.4%（Rebuttal 最低 0.895）——**降阈值多召回，再用跨度特征筛选**是共同配方。

**裁决**：跨度任务的"局部序列标注"只是第一阶段；把概率转成候选跨度 + 非局部特征 + 类专属阈值/规则，才是拉开名次的部分。置信度高（1st/3rd 量级一致 + 社区框架传播）。

### 共识二：融合要在**跨度/实体层**做，而不是 token 层

- 2nd：token 概率平均/投票要么取并集要么取交集，BIO 平均还会产生双 B；WBF 平均起止坐标得到"两个模型预测的中间区间"（图中 model1 "…practice coding on" + model2 "coding on Kaggle…" → WBF "practice coding on Kaggle"）——平均 0.700 → 0.741；
- 4th：tokenizer 不同的模型无法在 subword 上合并概率 → 实体级融合（同类 ≥50% 重叠分组、平均起止）+0.002 LB；
- 6th：token 级 logits 先 RoIAlign 聚到词级再平均。

**裁决**：跨模型融合的公共坐标系要选在"任务对象层"（span/word），token 层是模型私有实现。置信度高（三家独立、机制清晰）。

### 共识三：指标感知的后处理是"免费分"

指标只要求 50% 重叠 → 2nd 的后处理列表全部围绕它（断链修复、按类至多一个、长度回移）合计 ~+0.008 CV；1st 的"高边界阈值 + 65% 长度选择"再 +0.008；4th 的 beam search 修复非法 BIO 转换；3rd 允许 ≤0.2 的跨度交叠（解码不再强制互斥，因为标签本身就存在相邻/交叠结构）。

**裁决**：先读透指标定义，再设计后处理；"合法地利用指标口径"是本场的公开红利（主办未禁止且指标如此设计）。置信度高。

### 分歧一：WBF 是否总可靠？

2nd 用 WBF 拿私榜 0.740；6th 明确说"WBF 在本地验证不 work，我也没搞清原因（可能我写错了）"。4th 的实体级融合（50% 分组平均）与 WBF 是同一思想的两种实现。

**裁决**：融合方法的收益依赖"模型的跨度分布是否同构"（阈值/长度分布不同会让平均偏移）；6th 的失败更像实现/参数问题而非方法否定。置信度中。

### 分歧二：最大模型 vs 模型多样性

6th：deberta-large + xlarge 两模型最好（验证 0.723），"ensemble 更多没帮助"；2nd：10 个异构 backbone（含 bigbird/yoso/funnel/LSG）融合到 0.741；1st：5 个异构模型（含 bart/distilbart）。

**裁决**：单看"模型数"无意义；2nd 的增益来自**异质 backbone（不同预训练目标/注意力机制）**，6th 的 large+xlarge 同族信息重复。多样性判据应看预测跨度分布的去相关性（与 THEORY L7/L13 一致）。置信度中高。

## 4. 增量数字账

| 动作 | 数字 | 来源 |
| --- | --- | --- |
| 两级架构（stage1→stage2） | CV 0.712→0.748（+0.036）；LB 0.706→0.742（+0.036） | 1st |
| LGB 堆叠（套在 5 折 longformer 上） | 0.697→0.727（+0.030） | 1st |
| stage2 中的采样选择技巧 | +0.008 | 1st |
| AWP/FGM 对抗训练 | CV +0.01；5 折 LB +0.003 | 1st |
| 后处理（逐模型） | CV ~+0.008 | 2nd |
| WBF 融合（10 模型平均 CV ~0.700） | CV 0.741 / 公开 0.727 / 私榜 0.740 | 2nd |
| offset_mapping vs word_ids（单折 bigbird） | 公开 0.630 vs 0.595（+0.035）；5 折 0.659 | 4th |
| 实体级融合 | LB +0.002 | 4th |
| 模型规模上限 | ≥xlarge 后变差（xxlarge 更差） | 4th |
| 上下文长度 | 2048 之后退化（3rd）；各模型 1536 训练/推理（2nd） | 3rd/2nd |
| 提交工程 | 27 个模型推理 8h30m（截 30→27）；6th 2 小时 | 2nd/6th |

**可复算校验（3 处算术吻合）**

1. 2nd：10 模型 × 3 折 = 30，去掉 3 折 → **27 个模型** ✓；
2. 2nd 的 WBF 示例：起点 (8+10)/2=9、终点 (11+13)/2=12 → "9 10 11 12" ✓；
3. 1st 的召回-精度结构：7 类召回 0.895–0.974（Rebuttal 最低），300 万候选样本 ≈ 平均每篇数百候选——降阈值召回后由 GBM 收束，逻辑自洽 ✓。

**两处口径注意**
1. 2nd 表格中的 "706/710/721" 为省略小数点写法（0.706 等）；
2. 4th 的"deberta-xlarge/xxlarge 更差"与 2nd 表中 xlarge CV 0.708 略低于 deberta-large 0.706–0.711 的观察一致——**大模型不必然更好，取决于任务与数据**。

## 5. 机制推演

**M1｜为什么两级架构有效**：token 模型的感受野/损失都作用在局部（每个 token 的 CE），而判分单元是**跨度**——跨度是否成立取决于边界概率、长度先验、类间竞争、文档全局布局（开头=Lead、结尾=Concluding）。这些是"非局部特征"，GBM 在 170 维候选特征上直接学"这个跨度是不是某类"比让 token 模型隐式编码容易得多。1st 的 +0.036 与 2nd 的后处理 +0.008 都是"在正确坐标系里解决问题"的回报。

**M2｜WBF 的数学与适用条件**：跨度=(start,end)。两模型给出 (s1,e1),(s2,e2)，WBF 取 ((s1+s2)/2,(e1+e2)/2)。当两模型的误差近似独立同分布时，平均降低方差；当两者分布系统不同（阈值/长度偏好不同）时，平均会产生"谁都不像"的跨度——这解释 6th 的失败（其解码阈值与长度分布可能与其他模型不同构）。**可迁移条件：融合前先校准各模型的跨度长度/阈值分布。**

**M3｜指标定义反向工程**：TextOverlapF-beta 的 50% 重叠容差意味着"边界不够准也别丢"——所以 2nd 敢做"Evidence <45 词则前移起点 9 词"这类基于长度先验的偏移；3rd 敢在解码时允许交叠。**后处理的自由度和指标宽容度成正比**；反之在 IoU/严格边界指标下这些技巧会反噬。

**M4｜分词器决定标签保真**：`word_ids` 路径需要 `.split()` 分词，会把 `\n` 与空白折叠掉；作文的段落结构（换行）正是 discourse 信号 → 单折差距 0.035。DeBERTa-v2/v3 的慢分词器不支持 offset_mapping、其 fast 版会吃掉 `\n`——4th 同时打了两个补丁才拿到正确分数。**长文本结构化任务里，tokenizer 的空白/换行行为是一等公民**。

**M5｜BIO 的转移约束必须显式建模**：greedy 逐 token argmax 会产出 I-Dog→I-Dog 这类非法序列（同置信度下 B-Cat→I-Cat 才是合法且更可能）；beam search（beam=4）+ 合法转移掩码，或结构化损失/CRF，都是同一机制的实现。4th 的图给出了最直观的反例（I-Dog 0.54/I-Dog 0.01 vs B-Cat 0.44/I-Cat 0.99）。

**M6｜检测式建模的取舍**（6th）：把跨度当 box（objectness + 起点距离 + 终点距离 + 类），用检测器的正样本设计（首词+最低代价词）绕开 BIO 的链式约束，后处理只剩 NMS；代价是丢弃了 token 级序列上下文，且与其他 token 模型的融合更麻烦（自承 WBF 失败）。**它适合"快速、独立、对象清晰"的设定，不适合"需要跨模型 tokenizer 融合"的设定。**

## 6. 证据分级

| 断言 | 等级 | 说明 |
| --- | --- | --- |
| 两级架构 +0.036（1st） | **可读取（帖内数字）** | 两阶段 CV/LB 完整；非随机消融但量级与其他队一致 |
| WBF 0.700→0.741（2nd） | **可读取（帖内表）** | 10 模型 CV 全表 + 融合分；示例图可复算 |
| offset_mapping +0.035（4th） | **可读取（帖内表）** | 同模型同折对照，干净 |
| 实体级融合 +0.002（4th） | **自述** | 无对照表细节 |
| 后处理 +0.008（2nd） | **自述** | 未给逐步账 |
| "WBF 本地不 work"（6th） | **自述（负面）** | 无法核验其原因 |
| hengck23 的主题先验 | **讨论级线索** | 未在收录方案中被充分利用 |
| 私榜分数（0.735–0.740） | **可读取** | 半公开期的私榜数字 |

## 7. 边界条件与反事实

- **指标口径是后处理的边界**：50% 重叠宽容度支撑了长度平移技巧；若换成严格 IoU/边界匹配，2nd 的 PP 一族大部分失效。
- **提交时长是硬约束**：2nd 的 27 模型 8h30m、6th 的 2 小时——融合规模被推理时间截断（2nd 主动砍 3 折）。反事实：若更小模型/更快算子，可加更多异构成员。
- **长文本上限的相互矛盾**：3rd 观察 2048 后退化；2nd 长序列成员 CV 并不占优（longformer 0.702、bigbird 0.675）。**上下文长度不是免费收益**——注意力模式与预训练分布决定了有效长度。
- **反事实（4th）**：若不做分词器 \n 补丁，DeBERTa-v2/v3 系列只有 ~0.68（低于 longformer），会被错误地弃用；实际补丁后 0.7019–0.7038。**"模型不行"经常是预处理问题。**
- **反事实（1st）**：其"伪标签 Wikipedia talk 150k"失败（4th 的尝试）说明外部语料的域不匹配是代价；hhe 的 15 主题线索指出真正的外部红利是"同主题自造数据"，未被完全开发。

## 8. 悬案与失败学

**悬案**

1. **主题先验到底值多少**：hengck23 指出私榜与训练同 15 个主题、claim/counterclaim 可由位置区分；收录方案只有 55th（未收录）明确做主题后处理——这条线的上限未知；
2. **WBF 的可靠性边界**：什么条件下 span-WBF 会失效（6th 的反例）没有系统结论；
3. **类不平衡与噪声类**（Rebuttal 召回最低 0.895、CV 噪声最大）如何进一步改善未定。

**失败学**

| 失败 | 来源 | 教训 |
| --- | --- | --- |
| word_ids 路径（剪掉 \n） | 4th | 结构化文本任务的分词器行为必须先审计 |
| DeBERTa-v2/v3 慢分词器/快分词器吞 \n | 4th | 同上；"模型差"可能是 tokenizer 差 |
| xxlarge 更大模型 | 4th | 规模超过任务/数据支持反而变差 |
| WBF 本地失败 | 6th | 融合前需校准成员分布；直接套用会无效 |
| Wikipedia talk 伪标签 150k | 4th | 域不匹配的外部数据无用 |
| 段落信息进输入、回译、位置权重、overlap 当标签、stage2 用 BERT | 1st | 5 个负面结果：在错误坐标系加特征/加算力都无效 |
| 最长上下文（>2048） | 3rd | 有效上下文 < 配置上限 |
| stage1 单折 bigbird（0.595）就下结论 | 4th | 多折与不同解码口径下排序会翻转 |

## 9. 图表证据

> 路径相对本文件（`analysis/deep/`）：`../../intel/feedback-prize-2021/bodies/<topic>_img/NN.ext`

**图 1：WBF 在跨度上的工作原理**（2nd，topic 313389）——`../../intel/feedback-prize-2021/bodies/313389_img/01.png`

![wbf](../../intel/feedback-prize-2021/bodies/313389_img/01.png)

*读图结论*：model1 预测 "…books, **practice coding on**"，model2 预测 "**coding on Kaggle, talk**…"；WBF 输出 "**practice coding on Kaggle**"（起点与终点分别平均）。这就是"平均坐标"相对并集/交集/BIO 平均的差异——保留了两个模型共识覆盖的中间区间。

**图 2：1st 的单模型 CV 全表（stage1 选型依据）**（1st，topic 313177）——`../../intel/feedback-prize-2021/bodies/313177_img/01.png`

![cv table](../../intel/feedback-prize-2021/bodies/313177_img/01.png)

*读图结论（正文只给最终集成）*：longformer-large-4096 各折 0.7065/0.7011/0.6939/0.7003/0.6959（均 0.6996）；roberta-large 均 0.6993；deberta-v2-xlarge 均 0.6948、xxlarge 均 0.6969；bigbird-base 均 0.6698；gpt2-large 仅 0.6019。**选 5 个成员时，单模 0.69–0.70 的异质家族（lf/roberta/deberta/bart 系）优于单个 0.71 的同族**——与 2nd 的集成哲学一致。

**图 3：实体级融合的 50% 重叠准则（代码）**（4th，topic 313330）——`../../intel/feedback-prize-2021/bodies/313330_img/03.png`

![entity ensemble](../../intel/feedback-prize-2021/bodies/313330_img/03.png)

*读图结论*：`group_overlapped_entities` 对同类实体按置信度排序后贪心分组，判据是"与组均值的重叠 ≥ 0.5"（用 max 归一化重叠）；这正是把指标口径直接变成融合规则——"50% 重叠即视为同一实体"。

**图 4：beam search 修复非法 BIO（代码与反例）**（4th）——`../../intel/feedback-prize-2021/bodies/313330_img/02.png`

![beam search](../../intel/feedback-prize-2021/bodies/313330_img/02.png)

*读图结论*：图中反例——t 处 `I-Dog 0.54 / B-Cat 0.44`，t+1 处 `I-Cat 0.99 / I-Dog 0.01`；greedy 会得到非法 `I-Dog → I-Dog`，beam search（beam=2，带合法转移掩码）得到 `B-Cat → I-Cat`。**序列标注的 argmax 不等于合法序列的 argmax**。

**图 5：3rd 的两级管线**（3rd，topic 313235）——`../../intel/feedback-prize-2021/bodies/313235_img/01.png`

![pipeline](../../intel/feedback-prize-2021/bodies/313235_img/01.png)

*读图结论*：Longformer + 滑窗 DeBERTa-xl → 候选跨度（带特征）→ 梯度提升模型 → 跨度预测。与 1st 的 "token 集成 → LGB" 完全同构——**不同队伍独立收敛到同一元架构**。

## 10. 对既有笔记/playbook 的修订点

1. `notes/nlp/feedback-prize-2021.md` 升级：补齐 8 节作者/票数/角色；方案谱系扩为 5 方案对照矩阵；新增两级架构数字账、WBF/实体级融合机制、分词器陷阱、beam search、主题先验悬案与图证节。
2. `playbook/nlp.md` 增补：
   - **跨度/抽取任务的两级配方**：token 模型（长文本+GRU 缝合）→ 候选跨度特征（~25–170 维）→ 类专属 GBM；
   - **跨度级融合三件套**：WBF（平均起止）、实体级 50% 重叠分组、NMS；
   - **指标感知后处理清单**（断链修复/类规则/长度平移/允许交叠）；
   - **分词器审计**：offset_mapping vs word_ids、`\n` 保真、fast/slow 行为差异；
   - **BIO 解码**：beam search + 合法转移掩码（或 CRF）。
3. `playbook/00-通用方法论.md` 增补："**坐标系原则**——在任务对象层（span/实体/框）而不是模型私有层（token/subword）做融合与统计"；"预处理 bug 会伪装成模型能力不足"（4th 的分词器两例）。

## 11. 出处

- NER starter（Chris Deotte，296 票）：https://www.kaggle.com/competitions/feedback-prize-2021/discussion/295794
- 1st（(⊙﹏⊙)，282 票）：https://www.kaggle.com/competitions/feedback-prize-2021/discussion/313177
- 2nd（Chris Deotte 队，203 票）：https://www.kaggle.com/competitions/feedback-prize-2021/discussion/313389
- 6th（tascj，165 票）：https://www.kaggle.com/competitions/feedback-prize-2021/discussion/313424
- 4th（Jungwoo Park，149 票）：https://www.kaggle.com/competitions/feedback-prize-2021/discussion/313330
- 见解帖（hengck23，147 票）：https://www.kaggle.com/competitions/feedback-prize-2021/discussion/308992
- 3rd（Shujun 队，72 票）：https://www.kaggle.com/competitions/feedback-prize-2021/discussion/313235
- 相关赛事汇总（Jonathan Besomi，69 票）：https://www.kaggle.com/competitions/feedback-prize-2021/discussion/295193
- 未收录缺口（登记备查）：313201（9th）｜313718（10th）｜313184（11th）｜316071（8th）｜313229（55th）｜313833（12th）｜313242（全解汇总）等
