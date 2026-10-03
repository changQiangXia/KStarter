# Essay Scoring 2.0 深读：双源数据不兼容 × QWK 阈值工程 × 小样本方差控制

> 赛事：Featured ｜ 主题 nlp（自动作文评分）｜ 2706 队 ｜ 代码赛 ｜ 指标：QWK（quadratic weighted kappa，1–6 序数，越高越好）
> 材料基础：`digests/learning-agency-lab-automated-essay-scoring-2.md`（8 篇：starter 218 票/更多数据 176/4th 95/2nd 总览 88/1st 86/6th/3rd/2nd 详版；120 条索引）+ 2 张图
> 深读时间：2026-10（Tier A #49）

## 0. 一句话重述：这道题真正在考什么

题面是"给 6–12 年级学生作文打 1–6 分（QWK）"，实际被考的是**两个数据来源的分布对齐**：

1. **训练集由两个来源拼接**：17,307 条 = **12,875 条 Persuade 语料 + 4,432 条 Kaggle-only**；两者评分标准不同（同 prompt 的分数分布不同；对抗验证 AUC 0.65–0.675 可分），而**测试几乎只含 Kaggle-only 风格的 5 个题目**（无 Persuade 记录）。
2. **两阶段训练是全员配方**：先在 Persuade（大源）预训练/MLM，再在 Kaggle-only（小源）微调——1st 实测 **+0.015 公榜**且显著改善 CV-LB 相关性；直接混训会让模型拟合大源分布（4th 的源标签实验）。
3. **QWK 的阈值化（float→int）是独立的大杠杆**：自定义切点（1/2 约 1.7、5/6 约 4.9）可比 0.5 舍入涨 ~0.01（4th：OOF 0.818→0.827）；但尾部分数稀疏 → 阈值方差大，必须多种子/多起点平均、避免在 4.5k 上 post-fit。
4. **微调数据只有 4.5k**：5 prompts × 6 档 → 种子方差极大；1st/2nd 都用 **3-seed 平均**与**简单平均集成**对抗过拟合；最佳私榜提交常常不是被选中的那个（2nd 的 0.844 未选、1st 的 0.841 恰是"按最佳 CV 选"的那个）。
5. **工程细节**：DeBERTa-v3-large + 回归（>分类）、去掉 dropout、maxlen 1024/1536（作文长尾到 1800 token）、添加 `\n`/双空格 token、prompt 不放进输入。

一句话：**这是一场"识别数据有几种来源、把测试源分布对齐"的比赛**——DeBERTa 回归 + 两阶段 + QWK 阈值优化是骨架；名次由小样本方差控制与提交选择决定。

## 1. 材料与角色

| 帖子 | 作者 | 票数 | 角色与独有信息 |
| --- | --- | --- | --- |
| [497832](https://www.kaggle.com/competitions/learning-agency-lab-automated-essay-scoring-2/discussion/497832) DeBERTa starter | cdeotte | 218 | **回归 > 分类**；回归必须去 dropout；maxlen 1024/1536；batch 敏感；添加 `\n`/双空格 token；CV 0.822/LB 0.800 |
| [496906](https://www.kaggle.com/competitions/learning-agency-lab-automated-essay-scoring-2/discussion/496906) 更多数据 | — | 176 | Persuade 2.0 共 25,996 条，**12,873 条与本赛重复** → 额外 8,689 条；辅助列（grade/gender/…）；**泄漏探针：测试不在 Persuade 中** |
| [516639](https://www.kaggle.com/competitions/learning-agency-lab-automated-essay-scoring-2/discussion/516639) 4th | — | 95 | 双源不兼容（[A]/[B] 标签 + 源分类头 + 分源头）；假设测试全为 non-Persuade；**45 预测集成**（deberta-large/v3-large/Qwen2-1.5B ×5 折×3 seed）；OOF 0.818→**0.827**（阈值）；动态 micro-batch；DeBERTa 提速 15%/30% |
| [516582](https://www.kaggle.com/competitions/learning-agency-lab-automated-essay-scoring-2/discussion/516582) 2nd 总览 | — | 88 | 两阶段（Kaggle-Persuade 预训练→Kaggle-Only 微调）；StratifiedKFold；A+B 验证与阈值搜索；**最佳 PB 0.844 未选中** |
| [516791](https://www.kaggle.com/competitions/learning-agency-lab-automated-essay-scoring-2/discussion/516791) 1st | — | 86 | 两阶段 +0.015；PL 两轮（+0.004–0.007）；阈值 Powell+15 起点+3 seed；3-seed 平均一切；最佳 CV 提交 0.841 私榜（多样性提交 0.837/0.838）；"rank 619 时信 CV" |
| [516814](https://www.kaggle.com/competitions/learning-agency-lab-automated-essay-scoring-2/discussion/516814) 6th | — | — | LB 探针给出测试 5 主题比例（Driverless 35.6%/FACS 24.6%/Venus 19.6%/Face on Mars 12.6%/Cowboy 7.6%）；**测试无 Persuade**；按主题权重验证；persuade flag；DeBERTa OOF→CDF 给 LGBM；relabeling |
| [516631](https://www.kaggle.com/competitions/learning-agency-lab-automated-essay-scoring-2/discussion/516631) 3rd | — | — | MLM + 两阶段；CV 0.836/公 0.832/私 0.839；**groupkfold(prompt_name) 公榜好私榜崩**；Persuade 2.0 因 license 未用（用了也几乎无差） |
| [516790](https://www.kaggle.com/competitions/learning-agency-lab-automated-essay-scoring-2/discussion/516790) 2nd 详版 | — | — | MLM 10 epoch + 两阶段；**ordinal regression（累积 BCE）**；阈值在全量训练集搜（只在 Kaggle-only 搜会 CV 好 LB 掉）；5 模型 hard voting（CV .8248/LB .831/私 .840） |

**材料缺口（受"不扩采"约束，登记备查）**：RAPIDS SVR starter(502554,140)、Mistral 7B baseline(494935,119)、CV 策略讨论(499959,110)、阈值优化帖(502279,99)、主题建模(498478,91)、单模型 CV-LB 线程(491101,77)、PERSUADE 2.0 链接(493962,70) 等未收录——**阈值优化的社区共识与主题分析**是主要缺口。

## 2. 逐方案对照矩阵

| 维度 | 1st | 2nd | 3rd | 4th | 6th |
| --- | --- | --- | --- | --- | --- |
| 双源处理 | 两阶段（old→new）；PL 两轮 | 两阶段 + MLM 10 epoch | MLM + 两阶段；验证用非 Kaggle-only | [A]/[B] 标签 + 源分类头；假设测试全 non-Persuade | persuade flag；验证按测试主题加权 |
| 模型/损失 | Deberta large（base 混入），MSE/BCE，CLS/Gem pooling | ordinal regression（累积 BCE）、BCE、MSE 多路 | base/large × mean/attention/LSTM 头 | deberta-large/v3-large/Qwen2-1.5B | DeBERTa + LGBM（OOF→CDF） |
| 阈值 | Powell + 15 起点 + 3 seed；1/2≈1.7、5/6≈4.9 | OptimizedRounder + 末阈值 for-loop；全量数据搜 | — | OOF 上搜；0.818→0.827 | 阈值优化失败 |
| PL/额外数据 | PL 老数据两轮（+0.004–0.007） | — | Persuade 2.0 未用（license） | 标签互换 + 蒸馏（未提交） | relabeling（|Δ|>2） |
| 验证 | prompt_id+score 分层 5 折；B 子集 | A+B 双验证；B 子集阈值参考 | 非 Kaggle-only 验证 | 早停看 non-Persuade | 5 主题加权 |
| 集成 | 简单平均（7 模型×3 seed=21 大模型）；预计算每模型阈值 | hard voting（5 模型）+ 简单平均对照 | backbone/head/maxlen 组合 | 45 预测平均 | DeBERTa+LGBM |
| 成绩 | 最佳 CV 提交私 **0.841**；多样性提交 0.837/0.838 | 选中 CV .8248/LB .831/私 .840；最佳私 .844 未选 | 私 0.839（CV/公/私一致） | OOF .827（阈值后） | 私 0.836（另有一个 0.837） |
| 失败清单 | GBDT、prompt 入输入、回译、分类、注意力池化、48h 效率赛 | classification、weighted blend、Reina、stacking、MoE、ranking、AWP | groupkfold(prompt_name) 私榜崩 | 标签互换蒸馏未提交 | 数据增强、阈值优化、拼写词典、半监督 |

## 3. 共识、分歧与裁决

### 共识一：双源不兼容 + 两阶段训练是核心（1st/2nd/3rd/4th 全员）

1st：pretrain(old)→finetune(new) **+0.015 公榜**且 CV-LB 相关性变好；
2nd：先 Kaggle-Persuade 再 Kaggle-Only，理由是"混合训练会让模型学大源分布"；
4th：[A]/[B] 标签 + 源分类头实验证明混训损害拟合；
3rd：两阶段 + 验证避开 Kaggle-only。

**裁决**：**先识别数据有几个来源**是本题第一动作；两阶段 = 大源学表示、小源学决策边界（与域适应同构）。置信度：高。

### 共识二：QWK 阈值化是第二大杠杆，且必须防过拟合（1st/2nd/4th）

4th：OOF 0.818→**0.827**（仅阈值化）；
1st：典型切点 1/2≈1.7、5/6≈4.9；Powell 最小化 1−QWK、15 个起点平均、3 seed；
2nd：末阈值（5 与 6 之间）单独搜索，涨 CV/LB/私榜。

**裁决**：QWK 对少数类敏感，阈值可以"移动预测"提升指标而不改善 MSE；但尾部分数稀疏 → 阈值方差大。**多种子 + 多起点 + 不在小验证集上 post-fit** 是纪律。置信度：高。

### 共识三：回归 > 分类；DeBERTa large + 长上下文 + 无 dropout（starter 实证 + 多队采用）

starter：回归（num_labels=1）CV 更高；回归必须去 dropout；maxlen 1024/1536 优于 512；
1st/4th：MSE/BCE 回归；3rd/2nd：回归 + ordinal。

**裁决**：序数评分本质是连续潜变量 → 回归保留了阈值优化的自由度；分类 hard label 丢信息。置信度：高。

### 共识四：小样本方差控制 = 3-seed 平均 + 简单集成（1st/2nd）

1st："3-seed 平均一切"是最大方差控制手段；只重做 finetune 换 seed 即可；
2nd：最佳私榜提交是**简单平均**（0.842–0.844），加权/投票反而略低；
1st：在 4.5k 上同时 post-fit 权重与阈值会严重过拟合。

**裁决**：Kaggle-only 仅 4.5k → 任何二次拟合都危险；**简单平均 + 预计算阈值**是稳健解。置信度：高。

### 分歧一：阈值在哪个集合上搜

2nd：只在 Kaggle-only 上搜阈值 CV 很好但 LB 掉 → 改回全量训练集搜；
1st：OOF（全量）上 Powell；
6th：阈值优化失败（其 LGBM 路线）。

**裁决**：阈值反映**分数分布**而非文本风格，应覆盖全量分布（尾部类别在 Kaggle-only 可能缺样本）；验证则看 B 子集/主题加权。置信度：中高。

### 分歧二：额外 Persuade 2.0 数据的价值

496906：可多拿 8,689 条；
1st："非文本依赖的额外数据几乎无差"；
3rd：用了也几乎无差（且 license 未明）；
4th：用源标签区分而不是混训。

**裁决**：额外同源数据的收益远小于"两阶段 + 源区分"；**分布错配时加同源数据≈无效**。置信度：中高。

### 分歧三：提交选择策略（本场最真实的痛点）

1st：按最佳 CV 选的提交私 0.841，多样性选择反而 0.837/0.838；
2nd：最佳私 0.844 未选中；
6th：50% CV + 50% LB 选到 0.836（另一个 0.837）；
3rd：强调 CV/公/私一致性。

**裁决**：CV（尤其 B 子集或按主题加权）比 LB 可靠，但分布漂移+小测试集下选择仍有运气成分；**留一个"最佳 CV"提交 + 一个"多样性"提交**是常见对冲（1st 的三提交策略）。置信度：中高。

## 4. 增量数字账

| 动作 | 数字 | 来源 |
| --- | --- | --- |
| 数据构成 | 17,307 = Persuade 12,875 + Kaggle-only 4,432；测试 5 主题、无 Persuade | 4th/6th/496906 |
| 对抗验证 | train vs test AUC 0.65–0.675 | 4th |
| 两阶段增益 | +0.015 公榜（1st）；CV-LB 相关性显著改善 | 1st |
| PL 增益 | +0.004–0.007（老数据两轮；第二轮 CV 大涨但 LB 降） | 1st |
| 阈值化增益 | OOF 0.818→**0.827**（4th）；切点 1/2≈1.7、5/6≈4.9 | 4th/1st |
| 1st 集成 | 7 模型 × 3 seed = 21 个 Deberta large；模型目录 ~2TB；最佳私 0.841（按 CV 选） | 1st |
| 2nd 集成 | 5 模型 hard voting：CV 0.8248/0.8239、LB 0.831、私 0.840；简单平均私 0.842–0.844 | 2nd |
| 3rd 成绩 | CV 0.836/公 0.832/私 0.839 | 3rd |
| starter | 回归 CV 0.822/LB 0.800（vs 分类基线更低）；maxlen 1024/1536 | 497832 |
| 作文长度 | 峰值 250–400 token，长尾到 1800 | 497832 图 |
| 6th 主题比例 | Driverless 35.6%、FACS 24.6%、Venus 19.6%、Face on Mars 12.6%、Cowboy 7.6% | 6th |
| 赛事 | 2706 队；QWK；120 帖 | 元数据 |

**结构校验（2 处吻合）**

1. 4th 的"测试全为 non-Persuade"与 6th 的"测试无 Persuade 记录"独立互证 ✓；
2. 1st 的"按最佳 CV 选提交胜出"与 2nd 的"最佳私榜未选中"共同说明 CV 选择优于 LB 选择 ✓。

## 5. 机制推演

**M1｜为什么两阶段能对齐分布**：两个源的 y|x 映射不同（评分标准不同）；直接混训时大源（Persuade，12.9k）主导损失，模型学到 Persuade 的决策边界。先在大源训语言/任务表示，再用小源微调，等价于**冻结表示、只适配决策边界**（域适应的经典两段式）。1st 的 +0.015 与 4th 的源标签实验是同一机制的两面。

**M2｜QWK 与阈值的经济学**：QWK 的混淆矩阵按距离平方加权，**移动切点可在牺牲少量准确率的情况下提升 Kappa**（尤其少数类 1/6 的召回）；回归输出是连续分数，阈值是"免费"的后处理自由度。但尾部（5/6）样本极少 → 阈值估计方差大 → 必须多种子/多起点平滑，且避免在 4.5k 上把权重与阈值一起拟合（双重过拟合）。

**M3｜小样本的方差结构**：4.5k 微调集 × 5 prompts → 单一 prompt 的分布偏移会主导种子间差异；3-seed 平均把"某次抽到坏 prompt 组合"的方差压掉。集成权重与阈值的二次拟合本质是在同一 4.5k 上二次消费信息 → 过拟合概率陡增。

**M4｜PL 的"分布翻译"机制**：用新数据训练的集成给老数据打分，把老数据的标签重新映射到新标准；第一轮（与真值平均）稳、第二轮（纯预测）激进。1st 的观察（CV 大涨/LB 降/私榜不差）说明其收益与风险都来自"标签再校准"——与 LEAP/ARIEL 的偏移修复同族。

**M5｜测试分布侦查**：adversarial validation（AUC 0.65–0.675）+ LB 主题探针（5 主题比例）+ Persuade 泄漏探针（无匹配）共同回答"测试是什么分布"。在训练/测试源不同且测试小的情况下，**侦查是选择模型与验证策略的前提**。

**M6｜提交选择的博弈**：QWK 阈值 + 分布漂移 + 小测试集 → CV-LB-私榜三角不完全相关；多队的最佳私榜提交未被选中（1st/2nd/6th）。**"最佳 CV + 多样性"双提交对冲**是在信息不足时的理性策略。

## 6. 证据分级

| 断言 | 等级 | 说明 |
| --- | --- | --- |
| 双源构成与测试无 Persuade | 多队独立 + 可复现探针 | 高 |
| 两阶段 +0.015 | 1st 自述（代码/流程公开） | 中高 |
| 阈值化增益 0.818→0.827 | 4th 自述 + 全量 OOF | 中高 |
| starter 回归 > 分类 | 公开 notebook（CV .822/LB .800） | 高 |
| 3-seed/简单平均的方差控制 | 1st/2nd 自述 | 中高 |
| 6th 的主题比例探针 | 单队探针（未验证） | 中 |
| 额外 Persuade 数据无效 | 1st/3rd 的自述对照 | 中 |

## 7. 边界条件与反事实

- **反事实 1**：单阶段混训 → 模型拟合 Persuade 分布（4th 的标签实验、1st 的 −0.015）。
- **反事实 2**：不做阈值优化 → QWK 掉 ~0.01（4th 的直接数字；1st 的 1.7/4.9 远超 0.5 舍入）。
- **反事实 3**：用 groupkfold(prompt_name) 验证 → 公榜好、私榜崩（3rd 的实证）。
- **反事实 4**：在 4.5k 上 post-fit 集成权重+阈值 → 过拟合（1st 的警告与"简单平均"选择）。
- **反事实 5**：只用 Kaggle-only 搜阈值 → CV 好/ LB 掉（2nd 的实证）。
- **边界**：结论依赖"能从数据中识别多个来源 + 测试只来自其一"；单一来源任务不需要两阶段，但"3-seed + 简单集成 + 阈值纪律"仍通用。

## 8. 悬案与失败学

**悬案**

1. 6th 的测试主题比例（35.6%/24.6%/…）是探针估计，未被官方/最终榜单验证。
2. Persuade 2.0 的 license 与"额外数据是否被官方允许"未定（3rd 明确因此未用）。
3. 1st 第二轮 PL 的"CV 大涨/LB 降/私榜不差"机制未完全解释（怀疑泄漏但未证实）。
4. QWK 阈值是否存在可迁移的理论最优值（尾部稀疏）——社区帖（502279）未收录。

**失败学（跨队合集）**

- 模型类：classification（starter/2nd/1st）、GBDT（1st）、attention pooling（1st）、stacking/MoE/ranking loss/AWP（2nd）、Reina（2nd）。
- 输入类：把 prompt 放进输入（1st）、回译（1st）。
- 阈值类：阈值优化失败（6th）；只在 Kaggle-only 上搜（2nd 的教训）。
- 数据类：额外 Persuade 数据（1st/3rd 收益有限）；数据增强/半监督（6th）。
- 工程类：最后 48h 才做效率方案（1st，ONNX 仍太慢）——**时间预算要留给提交选择与稳健性**。

## 9. 图表证据

> 路径相对本文件（`analysis/deep/`）：`../../intel/learning-agency-lab-automated-essay-scoring-2/bodies/<topic>_img/NN.png`

**图 1：作文 token 长度分布（starter）**（topic 497832）——`../../intel/learning-agency-lab-automated-essay-scoring-2/bodies/497832_img/01.png`

*读图结论*：峰值 250–400 token，长尾到 1800。**maxlen 512 截断大量内容**——1024/1536 的涨分来自这里；也解释了动态 micro-batch 拼批的必要性（4th）。

**图 2：2nd 的最终集成（5 模型 hard voting）**（topic 516790）——`../../intel/learning-agency-lab-automated-essay-scoring-2/bodies/516790_img/01.png`

*读图结论*：CoPE / ordinal / ordinal+clean / pet-like / multi-scale ordinal 五路各出 hard prediction（Nelder-Mead 阈值 + 末阈值 for-loop），再 hard voting；CV 0.8248/0.8239、LB 0.831、私 **0.840**。**阈值与投票是两条独立的决策链**。

## 10. 对既有笔记/playbook 的修订点

1. `notes/nlp/learning-agency-lab-automated-essay-scoring-2.md` 升级：补 8 篇作者/票数、五方案 × 9 维对照、数字账（+0.015、0.818→0.827、0.841/0.844/0.839）与 2 张图证；新增"双源对齐"与"QWK 阈值"节。
2. `playbook/nlp.md`（文本评分/QWK 节）增补：
   - **先做来源审计**（重复检测/对抗验证/探针）→ 两阶段（大源表示 → 小源决策边界）；
   - **QWK 阈值工程**：回归 + 优化切点（Powell/多起点/多种子）；阈值覆盖全量分布、避免 post-fit；
   - **小样本方差控制**：3-seed 平均、简单平均集成、只重做 finetune；
   - **PL 分布翻译**（老数据重打分）及其过拟合风险；
   - **提交选择对冲**（最佳 CV + 多样性双提交）。
3. `playbook/00-通用方法论.md` 增补：**"数据来源识别先于建模"**（本场双源）；**"序数指标：连续分数 + 阈值 = 额外自由度"**；**"小验证集上的二次拟合是双重过拟合"**。
4. `analysis/THEORY.md`（Batch 5 末汇总 v0.5）候选：
   - **L84｜多来源数据的分布对齐**：来源审计 + 两阶段；证据 = 本场 + isic/hubmap 的"域差异"同族；
   - **L85｜序数指标的阈值经济学**：连续预测 + 阈值优化；证据 = 本场 1st/2nd/4th；
   - **L86｜小样本：3-seed + 简单集成 > 拟合权重**（本场 + godaddy 的"选择即分数"同族）。

## 11. 出处

- starter（cdeotte，218 票）：https://www.kaggle.com/competitions/learning-agency-lab-automated-essay-scoring-2/discussion/497832
- 更多数据（176 票）：https://www.kaggle.com/competitions/learning-agency-lab-automated-essay-scoring-2/discussion/496906
- 4th（95 票）：https://www.kaggle.com/competitions/learning-agency-lab-automated-essay-scoring-2/discussion/516639
- 2nd 总览（88 票）：https://www.kaggle.com/competitions/learning-agency-lab-automated-essay-scoring-2/discussion/516582
- 1st（86 票）：https://www.kaggle.com/competitions/learning-agency-lab-automated-essay-scoring-2/discussion/516791
- 6th：https://www.kaggle.com/competitions/learning-agency-lab-automated-essay-scoring-2/discussion/516814
- 3rd：https://www.kaggle.com/competitions/learning-agency-lab-automated-essay-scoring-2/discussion/516631
- 2nd 详版：https://www.kaggle.com/competitions/learning-agency-lab-automated-essay-scoring-2/discussion/516790
- 缺口登记：502554、494935、499959、502279、498478、491101、493962 未收录正文
