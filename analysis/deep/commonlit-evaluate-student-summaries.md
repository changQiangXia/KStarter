# CommonLit 摘要评估深读：主题多样性 × Head Mask × 长上下文鲁棒性

> 赛事：Featured ｜ 主题 nlp（学生摘要评分）｜ 2064 队 ｜ 代码赛 ｜ 指标：Mean Weighted Columnwise RMSE（content + wording 两目标，越低越好）
> 材料基础：`digests/commonlit-evaluate-student-summaries.md`（8 篇：2nd 142 票/离线 pip 129/4th 81/1st 59/9th 58/5th 47/3rd 43/7th + 120 条讨论索引）+ 3 张图（447293×2 可用 / 446524×1 为头像）
> 深读时间：2026-10（Tier A #46）

## 0. 一句话重述：这道题真正在考什么

题面是"给学生的摘要按 content 与 wording 两维打分（加权列 RMSE）"，实际被考的是**主题分布漂移下的鲁棒性与输入工程**：

1. **训练只有 4 个 prompt，测试有 122 个**：主题/材料分布差异巨大，公共榜只占 13% 数据 → shakeup 剧烈。所有头部方案的首要动作是**扩主题多样性**：1st 用 LLM 生成 500 个新主题（700–2000 字材料 + 问题）与每主题 10 条不同质量摘要，再做 **meta pseudo label 3 轮**；2nd 为每个 prompt 生成 10 个问题变体（共 44 个）。
2. **Head Mask 是最大单点技巧**（2nd 自述"magic"）：mean pooling 只覆盖学生答案 tokens（其余 token 权重置 0），在难 prompt 上提升尤其大——本质是让"表示对齐评分对象"。
3. **长度工程**：训练 maxlen 896–1280 → 伪标阶段 1280–2048 → 推理 1792–4200（9th）；4th 的 850→1500 推理延长同样涨分。**更长上下文 = 更多材料证据**，但需要 PL/两阶段训练配合。
4. **辅助任务**：Feedback 3.0 六维（cohesion/syntax/…）伪标辅助损失（2nd，0.5/0.5 隔步）、38 类内容类型上的 ArcFace（4th）——多任务正则 + 集成多样性。
5. **模型几乎是常量**：DeBERTa-v3-large（decoder 模型更差、base 模型差）；分数差来自数据/池化/长度/集成策略。1st 明确"我们只用了开源代码，没有改模型"。
6. **鲁棒性优先的提交策略**：4th 用"1 fulltrain × 7 模型"替代 4fold 单模型（压缩 fold 信息、允许更多集成）；9th 因 prompt `814d6b` 分布离群而做双 CV 方案；7th 只信本地 13% 之外的 CV。

一句话：**这是一场"主题多样性 + 池化/长度工程"的鲁棒性比赛**——模型不动，全部功夫在数据与输入/池化的对齐上。

## 1. 材料与角色

| 帖子 | 作者 | 票数 | 角色与独有信息 |
| --- | --- | --- | --- |
| [446573](https://www.kaggle.com/competitions/commonlit-evaluate-student-summaries/discussion/446573) 2nd | — | 142 | **Head Mask**（mean pooling 仅答案 tokens）；prompt question 增强（10 变体/44 个）；Feedback 3.0 六维辅助类伪标（0.5/0.5 隔步）；PL 使 CV .4581→.4476 并解锁 base 模型；5 模型集成（LSTM layer/sequence pooling）；失败：AWP、SWA |
| [435153](https://www.kaggle.com/competitions/commonlit-evaluate-student-summaries/discussion/435153) 离线 pip | — | 129 | 离线安装任意 pypi 包的通用方法（公共工具） |
| [446524](https://www.kaggle.com/competitions/commonlit-evaluate-student-summaries/discussion/446524) 4th | — | 81 | **1 fulltrain × 7 模型**（sub2 最佳私榜 0.45515）；推理 maxlen 850→1500；对 original prompt 做 attention pooling；ArcFace 38 类辅助；标点后补空格 |
| [447293](https://www.kaggle.com/competitions/commonlit-evaluate-student-summaries/discussion/447293) 1st | — | 59 | **meta pseudo label 3 轮**（Google 论文）；LLM 生成 500 主题 + 每主题 10 条多质量摘要；两阶段（PL 2 epoch → train 2–3 epoch）；按输入长度排序推理（7h vs 9h 限制）；"head mask + meta-PL 组合单模型可达 .43+" |
| [446539](https://www.kaggle.com/competitions/commonlit-evaluate-student-summaries/discussion/446539) 9th | — | 58 | prompt `814d6b` 离群 → 双 CV（含/不含）；3 seeds；两个 deberta-v3-large（全文/仅摘要）+ LSTM；SmoothL1、lr 8e-6、EMA .995；**推理 token_len 4200**；CV .495 / 私 .457 |
| [446584](https://www.kaggle.com/competitions/commonlit-evaluate-student-summaries/discussion/446584) 5th | — | 47 | summary+question+title+prompt_text；maxlen 1536；冻结 embedding+18 层；无 dropout；DeBERTa+LGB（Nelder-Mead 权重）；CV .4748；失败：LLM 数据、LGB stacking、其他模型 |
| [446686](https://www.kaggle.com/competitions/commonlit-evaluate-student-summaries/discussion/446686) 3rd | — | 43 | 简单管线 + EMA（必需）+ 差分 LR；CLS+答案 meanpool 拼接；**反向自动纠错增强**（fold3 私 0.453）；推理 1500；10 checkpoints 混合；失败：decoder 模型、AWP/FGM/WD/手工特征/GBT |
| [446534](https://www.kaggle.com/competitions/commonlit-evaluate-student-summaries/discussion/446534) 7th | — | — | 增益表：+prompt_text **+0.03**、freeze **+0.01**、不同输入混合 +0.01、LGBM +0.005；groupkfold(prompt_id)；公榜只 13% |

**材料缺口（受"不扩采"约束，登记备查）**：**1st 的详细解法一直"on the way"（未收录）**——head mask + meta-PL 的完整配方缺失；"Beware of Grade Distribution Gaps"(431545,64 票)、"Autocorrect is LGPL"(433208,74)、"Rotate Content 30 degrees"(430705,65)、Single Model CV-LB(424330,61)、input text/max length(432815,52)、wording prediction(424372,41)、Onboarding(424162,113) 未收录。

## 2. 逐方案对照矩阵

| 维度 | 1st | 2nd | 3rd | 4th | 5th | 9th |
| --- | --- | --- | --- | --- | --- | --- |
| 输入 | prompt text 引入模型（改开源代码） | "Think step by step…" + question + [SEP] + "Pay attention…" + text + [SEP] + prompt_text | prompt+question+text；token_type_ids 分段 | 两输入 pair + original prompt | summary+question+title+prompt_text | summary_text [SEP] question+[SEP]+prompt_text |
| 池化 | — | **Head Mask（仅答案）** + LSTM layer/sequence pooling | CLS + 答案 meanpool 拼接 | 对 original prompt 做 attention pooling | — | 两个 Large（全文/仅摘要）+ LSTM |
| 长度 | 推理按长度排序（7h） | 训练 896–1280（PL 后 1280–2048）；推理 1792/2048 | 推理 1500 | 训练 850 → 推理 1500 | maxlen 1536 | **推理 4200** |
| 数据/伪标 | **LLM 500 主题 ×10 质量摘要 + meta-PL 3 轮**；两阶段 2+2–3 epoch | prompt question ×10 增强；PL（CV .4581→.4476） | 相似样本合并 + 反向自动纠错增强（fold3 私 0.453） | 只用官方 4 prompt；fulltrain | 尝试 LLM 数据/伪标（失败） | 官方数据；3 seeds |
| 辅助损失 | — | Feedback 3.0 六维（0.5/0.5 隔步） | — | ArcFace 38 类 | — | — |
| 训练技巧 | — | layerwise LR、冻结底部 8 层、关 dropout、multisample dropout | **EMA（必需）**、差分 LR | 冻结/层wise | 冻结 embedding+18 层、无 dropout | SmoothL1、lr 8e-6、EMA 0.995 |
| 集成 | 单 4fold deberta-large（细节未发布） | 5 模型（不同 backbone/pooling/长度） | 10 checkpoints 混合 | **1 fulltrain × 7** | DeBERTa+LGB | 双模型+3 seeds |
| 成绩 | 冠军（细节未发布） | CV .4476（PL 后） | 私榜 ~0.453（fold3 增强）| sub2 私 **0.45515** | CV .4748 | 公/私 0.456/0.457 |
| 失败清单 | （未发布） | AWP、SWA | decoder 模型、AWP/FGM/WD/常数 LR/手工特征/GBT | — | LLM 数据、LGB stacking、其他模型、文本预处理 | — |

## 3. 共识、分歧与裁决

### 共识一：DeBERTa-v3-large 是唯一主干，分数来自数据/池化/长度（4/4 明确）

3rd："Deberta is the king"，decoder 模型更差；
5th：其他模型（含 deberta-v3-base 带 prompt_text）表现差很多；
2nd：PL 前 base 模型训不起来；
1st：只改预处理、不动模型。

**裁决**：这是编码器分类/回归任务的成熟期赛道；创新点全部转移到**输入构造、池化与数据侧**。置信度：高。

### 共识二：prompt_text 必须进输入（7th 量化 +0.03，2nd/4th/5th/1st 同向）

7th：+prompt_text **+0.03 CV**（单项最大）；
2nd：输入含 prompt_text，且对问题部分做 head mask 外的正常 attention；
4th：original prompt 做 attention pooling；
5th：四段全输入。

**裁决**：评分需要"对照材料判断内容是否覆盖"；没有 prompt_text，模型只能评语言质量。**这是内容维度的信息前提**。置信度：高。

### 共识三：推理长度 > 训练长度，且 PL/两阶段解锁更长训练（4th/2nd/9th）

4th：850 训练 → 1500 推理，CV/公榜提升；
2nd：训练 896–1280，PL 后 1280–2048，推理 1792/2048；
9th：推理 token_len 4200。

**裁决**：长上下文保留更多材料证据；推理延长是"零训练成本"的涨分点，但训练端想延长需要 PL/两阶段（否则标签噪声/过拟合）。置信度：高。

### 共识四：主题多样性是上限（1st/2nd 的核心）

1st：LLM 生成 500 主题 + 每主题 10 条多质量摘要，meta-PL 3 轮；两阶段训练；
2nd：每 prompt 生成 10 个问题变体（共 44）；
3rd：反向自动纠错增强（未完成但 fold3 私 0.453）；
5th：LLM 伪标失败（抓取 prompt_text）。

**裁决**：测试 122 主题 vs 训练 4 主题的漂移下，**扩主题/材料多样性的收益最大**；但合成数据的质量与训练协议（两阶段/meta-PL）决定成败（1st 成功 vs 5th 失败）。置信度：中高。

### 分歧一：Head Mask vs 其他池化

2nd：Head Mask 单项最大（"magic"，难 prompt 提升大）；
3rd：CLS + 答案 meanpool 拼接；
4th：prompt 部分 attention pooling；
5th：未用特殊池化（仍第 5）。

**裁决**：共同点是"**池化要聚焦评分对象或关键段**"；head mask 是最直接的实现（只在答案 tokens 上平均）。它不是唯一路径，但性价比最高、最可复制。置信度：高。

### 分歧二：伪标签的收益条件

2nd：PL 使 CV .4581→.4476 并解锁 base 模型；
1st：meta-PL 3 轮是"最关键、最耗时"的部分；
5th：LLM 伪标无效；
3rd：反向纠错增强有效但未完成。

**裁决**：PL 需要"教师质量 + 两阶段协议 + 与长度/主题扩展配合"；单纯把外部文本过一遍模型生成标签（5th）不够。**meta-PL（用学生模型→教师→再学生）是更系统的路线**。置信度：中高。

### 分歧三：鲁棒性策略（fulltrain vs KFold；双 CV）

4th：1 fulltrain ×7 模型，压缩 4fold 信息、允许更多集成，避免 per-prompt 方差；
9th：prompt `814d6b` 离群 → 两套 CV（含/不含），最终私榜更认可"包含"版；
7th：groupkfold(prompt_id)；公榜只 13%。

**裁决**：4→122 的 prompt 漂移下，**训练用全 prompt、验证按 prompt 分组、提交选稳健**；离群 prompt 的验证结论不可靠（9th 的对照）。置信度：高。

## 4. 增量数字账

| 动作 | 数字 | 来源 |
| --- | --- | --- |
| 2nd Head Mask | 单项最大提升（"magic"），难 prompt 3b9047/814d6b 提升尤其大 | 2nd |
| 2nd 伪标签 | CV **0.4581 → 0.4476**；解锁 deberta-v3-base | 2nd |
| 2nd 长度 | 初始训练 896–1280 → PL 1280–2048；推理 1792（large）/2048（base） | 2nd |
| 2nd 集成 CV | 5 模型：.460/.468/.464/.466/.461（不同 backbone/pooling） | 2nd |
| 2nd 辅助 | Feedback 3.0 六维（cohesion/syntax/vocabulary/phraseology/grammar/conventions），loss 0.5+0.5 隔步 | 2nd |
| 4th 提交对照 | sub2（best cv，7 模型）CV .4639 / 公 .42979 / 私 **0.45515**；sub1（9 模型）私 .45785；sub3 私 .45597 | 4th |
| 4th 长度实证 | 850 训练：fold CV .4505/.5595/.5051/.5024；推理 1500 后 .4527/.5588/.4614/.5013（难 prompt 改善明显） | 4th |
| 7th 增益表 | +prompt_text **+0.03**；freezing **+0.01**；不同输入混合 +0.01；LGBM +0.005；公榜只 13% 数据 | 7th |
| 5th | DeBERTa CV .4816、LGBM .5513、集成 **.4748**；冻结 embed+18 层；maxlen 1536 | 5th |
| 9th | CV .495；分 prompt：814d6b **.604982**、ebad26 .431438、3b9047 .49692、39c16e .483208；公 .456/私 .457；推理 token_len 4200 | 9th |
| 3rd | 反向自动纠错增强：fold3 私 **0.453**（优于其最终 mix）；EMA 必需 | 3rd |
| 1st | 500 主题 ×10 摘要；meta-PL 3 轮；两阶段 2 + 2–3 epoch；按长度排序推理 7h（限制 9h） | 1st |
| 赛事 | 2064 队；平均加权列 RMSE（content+wording） | 元数据 |

**结构校验（2 处吻合）**

1. 2nd 的 PL 后 CV .4476 与其"训练长度放大 + base 模型可训"的叙述自洽 ✓；
2. 4th 的"sub2 最佳 CV 也是最佳私榜"与"public 极不稳定"的动机一致 ✓。

## 5. 机制推演

**M1｜为什么主题多样性是上限**：模型要学的是"按 rubric 评估摘要"这一元技能，而不是记忆材料内容；训练 4 主题 → 测试 122 主题要求元技能泛化。LLM 生成新主题 + 多质量摘要把监督扩到主题空间；meta-PL 用学生模型的预测做教师信号，反复迭代，等于"自我扩充课程"。2nd 的 question 增强是同一思路的轻量版。

**M2｜Head Mask 的机制**：mean pooling 若平均了 prompt/question 的 token 表示，会把"题目语义"混入摘要表示，评分头需要额外容量去抵消；只在答案 tokens 上池化让表示与评分对象天然对齐。对"材料相似但摘要质量不同"的对比样本尤其关键（难 prompt 提升大）。

**M3｜长上下文的信息论**：内容维度需要核对摘要是否覆盖材料要点；输入越长，覆盖判断的证据越全。推理端延长是免费的（无训练代价）；训练端延长受标签噪声限制（高 maxlen 下的长尾样本噪声更大）→ 先用 PL 预训练再精调（2nd），或两阶段（1st）。

**M4｜多任务辅助的信号**：Feedback 3.0 六维与 content/wording 相关（语法/衔接影响 wording），作为辅助头提供额外梯度；ArcFace 在 38 类内容类型上做度量学习，迫使表示区分主题/类型 → 泛化 + 集成多样性。两者都属"免费正则"。

**M5｜prompt 离群与验证陷阱**：814d6b 的措辞分布与其他 prompt 不同，导致"在其他 prompt 上的 CV"无法预测它；9th 的双 CV 对照说明**包含离群 prompt 与否会改变结论**，而私榜更认可包含版（更难、更接近测试）。这是 T10"公开榜/验证是否代表测试"的微观案例。

**M6｜fulltrain 的方差-偏差权衡**：4fold 让每个模型只见 75% 数据，per-prompt 方差大；fulltrain 用满数据、方差低，但失去折间集成。4th 用"多架构/多 maxlen 的 fulltrain 模型集成"补多样性——**数据量 << 主题数时，用数据换方差比用折换集成更划算**。

## 6. 证据分级

| 断言 | 等级 | 说明 |
| --- | --- | --- |
| 2nd Head Mask/PL/长度 | 自述 + inference notebook/权重数据集 | 中高 |
| 4th 提交对照表与长度实证 | 自述 + 表格 + 私榜数字 | 中高 |
| 7th 增益表 | 自述（具体百分比） | 中 |
| 5th/9th/3rd | 自述（代码公开） | 中 |
| 1st meta-PL/500 主题 | 仅 brief + 2 张提示词图；**详细解法未发布** | 中（方向可信，配方缺失） |
| 离线 pip | 可复现工具帖 | 高 |
| Grade gaps/autocorrect/license 争议 | 仅标题（未收录） | 低（登记） |

## 7. 边界条件与反事实

- **反事实 1**：不做主题多样性扩增 → 4→122 的分布漂移下泛化差（1st/2nd 的核心动机）。
- **反事实 2**：普通 attention mask 做 mean pooling → 2nd 称 CV 大幅落后（尤其难 prompt）。
- **反事实 3**：不延长推理长度 → 材料证据不足（4th 的 850→1500 实证）。
- **反事实 4**：只用 KFold 单模型 → 推理预算不允许更多集成（4th 的 fulltrain 动机）。
- **反事实 5**：LLM 伪标不加协议（5th）→ 无提升；meta-PL/两阶段（1st/2nd）才有效。
- **边界**：依赖可获取的评分对象与材料文本（prompt_text 可从 commonlit.org 抓，但存在 license 不确定性——3rd 因此放弃增强）；纯作文无材料任务不适用"内容覆盖"部分。

## 8. 悬案与失败学

**悬案**

1. **1st 的详细解法始终未发布**（"on the way"）：head mask + meta-PL 的完整配方、"0.43+ 单模型"的说法无法验证——本次深读最大缺口。
2. **数据/许可问题**：Grade Distribution Gaps(431545)、Autocorrect LGPL(433208)、Rotate Content(430705)、commonlit.org 文本 license（3rd 放弃增强）未收录。
3. Single Model CV-LB(424330) 与 input/maxlen 实验(432815) 未收录——CV-LB 关系的系统分析缺失。
4. 1st 的 meta-PL 3 轮如何避免自我强化噪声、教师模型如何选择，细节缺失。

**失败学（跨队合集）**

- 模型类：decoder 模型（3rd/5th）、deberta-v3-base 带 prompt_text（5th）。
- 数据类：LLM 额外数据/伪标（5th）、commonlit.org 增强（3rd，license 顾虑）。
- 训练类：AWP、SWA（2nd/7th）、FGM、WD、常数 LR（3rd）。
- 集成类：LGB stacking（5th）、手工特征/GBT（3rd）、同 prompt 其他摘要拼接（5th）。
- 工程类：不做长度排序 → 9h 超时（1st）。

## 9. 图表证据

> 路径相对本文件（`analysis/deep/`）：`../../intel/commonlit-evaluate-student-summaries/bodies/<topic>_img/NN.jpg`

**图 1：1st 的 LLM 主题生成流水线**（topic 447293）——`../../intel/commonlit-evaluate-student-summaries/bodies/447293_img/01.jpg`

*读图结论*：以竞赛 4 个 prompt 为示例，让 LLM 扮演"写作老师"生成新的 topic question + 700–2000 字材料，重复 500 次。**主题空间扩增**是 1st 数据策略的第一步。

**图 2：1st 的摘要质量生成提示词**（topic 447293）——`../../intel/commonlit-evaluate-student-summaries/bodies/447293_img/02.jpg`

*读图结论*：对每个生成主题，让 LLM 产出 10 条"content/wording 质量各不相同"的摘要（≤30 tokens），为 meta-PL 提供成对的质量梯度监督。**合成数据按两条评分维度设计**——与本场指标一致。

*（本场归档图片极少：446524 的唯一图片为用户名头像，不内嵌；其余方案无图。）*

## 10. 对既有笔记/playbook 的修订点

1. `notes/nlp/commonlit-evaluate-student-summaries.md` 升级：补 8 篇作者/票数、六方案 × 9 维对照、数字账（+0.03/+0.01、.4581→.4476、0.45515、4200）与 2 张图证；新增"主题多样性"与"Head Mask"节。
2. `playbook/nlp.md`（文本评分/回归节）增补：
   - **评分对象感知的池化**：Head Mask（只在答案 tokens 上平均）；池化边界 = 预测对象；
   - **主题/prompt 多样性扩增**：LLM 生成主题+多质量样本、question 变体增强、meta-PL 两阶段协议；
   - **长度工程**：推理长度 > 训练长度；训练端延长用 PL/两阶段配合；
   - **辅助任务**：相关维度（Feedback 六维）伪标辅助头、内容类型 ArcFace；
   - **鲁棒提交**：fulltrain×N 集成、prompt 分组 CV、离群 prompt 双 CV 对照。
3. `playbook/00-通用方法论.md` 增补：**"池化边界=预测对象"**（评分/抽取任务通用）；**"主题漂移下用数据换方差"**（4th 的 fulltrain 逻辑）。
4. `analysis/THEORY.md`（Batch 5 末汇总 v0.5）候选：
   - **L75｜评分任务的池化对齐**（head mask；证据 = 2nd + 结构化任务）；
   - **L76｜主题漂移：多样性扩增优先于模型优化**（1st/2nd/3rd）；
   - **L77｜推理长度延长是零训练成本涨分项**（本场 4/4）。

## 11. 出处

- 2nd（142 票）：https://www.kaggle.com/competitions/commonlit-evaluate-student-summaries/discussion/446573
- 离线 pip（129 票）：https://www.kaggle.com/competitions/commonlit-evaluate-student-summaries/discussion/435153
- 4th（81 票）：https://www.kaggle.com/competitions/commonlit-evaluate-student-summaries/discussion/446524
- 1st（59 票，brief）：https://www.kaggle.com/competitions/commonlit-evaluate-student-summaries/discussion/447293
- 9th（58 票）：https://www.kaggle.com/competitions/commonlit-evaluate-student-summaries/discussion/446539
- 5th（47 票）：https://www.kaggle.com/competitions/commonlit-evaluate-student-summaries/discussion/446584
- 3rd（43 票）：https://www.kaggle.com/competitions/commonlit-evaluate-student-summaries/discussion/446686
- 7th：https://www.kaggle.com/competitions/commonlit-evaluate-student-summaries/discussion/446534
- 缺口登记（未收录正文）：1st 详细版（未发布）、424162、433208、430705、431545、424330、432815、424372 等
