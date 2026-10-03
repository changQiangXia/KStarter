# LMSYS Chatbot Arena 深读：奖励模型起点 × 蒸馏 × A/B 对称性

> 赛事：Research ｜ 主题 nlp（LLM 评测）｜ 1849 队 ｜ 代码赛 ｜ 指标 log loss（2024-08-12 截止）
> 材料基础：`digests/lmsys-chatbot-arena.md`（6 篇正文：16th/3rd/2nd/1st/9th/5th）+ 2 张图（本场图片资产极少）
> 深读时间：2026-10（Tier A #11，Batch 2 首篇）

## 0. 一句话重述：这道题真正在考什么

题面是"预测人类更喜欢哪个模型回答"，实际被考的是**在 Kaggle 2×T4 16GB 的推理约束下，把 70B 级判断力压缩进 9B 模型**。降解为 6 步：

1. **选起点**：从 **reward model / pair-preference model**（RLHFlow、ArmoRM、FsfairX-Gemma2-RM）而不是 chat model 出发——"比较"这个任务已在成对偏好数据上预训练好（3rd/9th/5th/2nd 独立汇合）；
2. **教师信号**：70B/72B 教师 logits 蒸馏（1st）或 500k/240k/45k 伪标签（3rd/2nd/9th）；纯数据路线也能第 5（5th）；
3. **抹平位置偏差**：A/B 交换 TTA 或训练期"全交换、同一 optimizer.step 累积梯度"（2nd +0.003；各家 TTA +0.003~0.015）；
4. **截断方向**：**左截断**（保留最近轮次）是 16th 的最大单步之一（0.890→0.885）；9th 同样 `truncation_side="left"`；
5. **推理工程**：**8-bit 推理 > 4-bit**（分数不降且更快——16th/9th/5th/3rd 四方独立结论）；varlen 无 padding、按长度动态批、双 GPU 流水线；
6. **泄漏时代的数据纪律**：本场发生数据泄漏事件；伪标签（PL）在泄漏子集上的优势不转移，曾把 CV/LB 相关性打断（3rd）；终局私榜数字（0.96898/0.9859/0.9828）与公开阶段不可同口径比较。

一句话：**这道题的分差几乎全部来自"起点 + 教师信号 + 对称性"三件事**，模型结构（都是 9B + 序列分类头）反而不是变量。

## 1. 材料与角色

| 帖子 | 作者 | 票数 | 角色与独有信息 |
| --- | --- | --- | --- |
| [527596](https://www.kaggle.com/competitions/lmsys-chatbot-arena/discussion/527596)（16th） | Chris Deotte | 205 | **系统化 LoRA/QLoRA 调参配方**：alpha 决定 backbone LR（=alpha/rank×head_LR）；公共 notebook 从 0.941 到 0.885 的 11 步逐项账；405B-as-judge 三种合成法全失败 |
| [527629](https://www.kaggle.com/competitions/lmsys-chatbot-arena/discussion/527629)（1st） | sayoulala | 196 | **Distill is all you need**：70B/72B 教师逐折出软标签 → 9B 学生 logits 蒸馏；5 折 LoRA 直接平均；GPTQ 8-bit + TTA；CV/LB 高度一致 |
| [527685](https://www.kaggle.com/competitions/lmsys-chatbot-arena/discussion/527685)（2nd） | tascj（+liushuzhi、kapenon） | 107 | **唯一全程全参数训练**（无 LoRA）；full swap 同 step 累积梯度 +0.003；240k PL；varlen 无 padding 训练/推理工程最细 |
| [527766](https://www.kaggle.com/competitions/lmsys-chatbot-arena/discussion/527766)（3rd） | Mark Tenenholtz & Raja | 59 | **reward-model 起点 + 500k 软标签**；关闭 Gemma2 softcapping +0.002；PL 打断 CV/LB 相关性的观察 |
| [527669](https://www.kaggle.com/competitions/lmsys-chatbot-arena/discussion/527669)（5th） | Team Danube（Psi、dott1718、ilu000） | 59 | **无 PL、无蒸馏**的反例路线：UltraFeedback 奖励预训练 +20 个点；两模型（正序+交换序）融合 |
| [527704](https://www.kaggle.com/competitions/lmsys-chatbot-arena/discussion/527704)（9th） | Ebi | 39 | gemma2 + chat-1m PL（45k 过滤样本）；8bit 推理；左截断；按 token 区间条件推理 llama3 省时间 |

**材料缺口（未扩采，登记备查）**：索引里另有 11 条 write-up 未收录，含 [4th（529067）](https://www.kaggle.com/competitions/lmsys-chatbot-arena/discussion/529067)、[18th QLoRA 高秩（527595）](https://www.kaggle.com/competitions/lmsys-chatbot-arena/discussion/527595)、[21st PL+特征工程（527627）](https://www.kaggle.com/competitions/lmsys-chatbot-arena/discussion/527627)、[13th 域适应+Focal（540876）](https://www.kaggle.com/competitions/lmsys-chatbot-arena/discussion/540876)、[19th（528288）](https://www.kaggle.com/competitions/lmsys-chatbot-arena/discussion/528288)、[156th（527938）](https://www.kaggle.com/competitions/lmsys-chatbot-arena/discussion/527938) 等；泄漏事件的原始讨论亦未收录。

## 2. 逐方案对照矩阵

| 维度 | 1st sayoulala | 2nd tascj | 3rd Mark & Raja | 5th Danube | 9th Ebi | 16th Chris |
| --- | --- | --- | --- | --- | --- | --- |
| 起点模型 | llama3-70B、qwen2-72B（教师）→ gemma2-9B（学生） | gemma2-9b/27b、ArmoRM-Llama3-8B | FsfairX-Gemma2-RM、RLHFlow pair-pref LLaMA3-8B | gemma2-9b + UltraFeedback 奖励预训练 | gemma2-9b-it、RLHFlow RM LLaMA3-8B | gemma2-9b-it（从公共 notebook 起步） |
| 训练方式 | LoRA r64/a128 全线性（9B）、QLoRA（70B/72B） | **全参数** BF16 + Kahan 优化器 | QLoRA r64/a16 全线性 | 全参/QLoRA 未明说（H2O LLM Studio） | LoRA r32/a64（gemma）、r128/a128（llama3） | QLoRA/LoRA（r16→r1024 阶梯） |
| 教师/伪标签 | **logits 蒸馏**（5 折教师出分布） | 240k PL（110k 1M + 130k 外部） | **500k+ 软标签**（1M 配对生成 + ORPO-DPO） | **无** | chat-1m PL（~45k） | 无（+33k 数据集） |
| A/B 对称 | TTA（infer 长度 2000） | **full swap 同 step**；格式增强 +0.001 | TTA（交换）~0.007 | 两模型：一正序一交换序 | 训练交换模型替代 TTA | TTA 0.941→0.926 |
| 截断/长度 | train 1024 | max 4340（含指令） | 1800 train / 8k PL / 4k+3k 推理 | 8k 可跑，最终 4k | train 1536 / infer 1792，left | max 2048→3072，**left 截断** |
| 推理优化 | GPTQ 8bit；5 折 LoRA 平均 | varlen 无 padding、triton 算子、双 GPU 流水线 | vLLM 按轮数批、ctranslate2 对比 | 双 GPU 分工、按长度批、INT8+fp16 | **8bit 代替 4bit**、merge_and_unload、动态批 | fp16 训/8bit 推（+10% 速度） |
| 关键成绩 | LB 0.882 → TTA 0.876 | 终融合 0.868（旧 LB） | 单模 0.895；+PL 0.880@8k | 单折 ~0.880，融合 ~0.873 | 0.890 → 0.881 | 单模 CV 0.878 / LB 0.888 |

## 3. 共识、分歧与裁决

### 共识一：reward model 起点 > chat model 起点（4/6 家独立采用）

- 3rd 的发现路径最有说服力：先观察到 RewardBench 前排模型**微调后**比 base/instruct 版更强 → 追查到它们预训练于 UltraFeedback 等偏好数据 → 自己拿 gemma2-9b 在公开奖励数据上预训练；
- 5th 用实验坐实机制：UltraFeedback 二分类 win/loss 预训练"提升最多约 20 个点"（原文 '20 points'，口径存疑，量级 0.02）；
- 9th 直接用 RLHFlow pair-preference LLaMA3 权重；2nd 的 stage-1 也包含 ArmoRM-Llama3-8B。

**裁决**：偏好任务上，"比较能力"可以预训练获得；下游微调只需适配格式与领域。置信度高（4 家、含消融式对照）。

### 共识二：A/B 交换是几乎免费的系统性增益（6/6 家）

TTA 交换收益：16th 第一步就 +0.015（0.941→0.926）；3rd ~0.007；2nd 训练期 full swap 稳定 +0.003（且要求同一 optimizer.step 累积原样本与交换样本梯度——否则等效于两倍 batch 的噪声正则，增益不稳定）；9th 干脆训一个交换版模型替代 TTA；5th 用"一正序一交换序"两模型融合。

**机制**：位置偏好使 P(A 胜｜原序) ≠ 1−P(A 胜｜交换序)；交换平均消除一阶位置项。置信度高。

### 共识三：8-bit 推理优于 4-bit（分数不降且更快）

16th："LoRA fp16 训 + 8bit 推 比 QLoRA 4bit 训推快 10%，且能跑 max 3072"；9th："8-bit 量化未观察到分数下降"、`merge_and_unload()`；3rd 明说悔恨没早发现 8bit 更快；5th 用 bitsandbytes INT8 + fp16 compute 跑通两模型 8k。

**机制**：分类 logit 对量化噪声比对生成 token 更敏感——4-bit 的有效位数不足会伤害 logit 校准；而 bitsandbytes 的 4bit 反量化开销在推理时反而更重。置信度高（4 家独立）。

### 分歧一：全参数 vs LoRA

2nd 明确"基于以往经验没试 LoRA，只用全参数"（单 A100 80G 训 7B，两卡训 9B，靠 BF16 + Kahan 求和）；1st/3rd/9th/16th 全部 LoRA/QLoRA；2nd 的 ArmoRM 还做了输入交换，最终 LB 0.868。

**裁决**：这是资源约束下的等价选择——LoRA 是"平民化"路径（16th：9B 只需训 200k 参数）；全参在单机多卡可用时上限略高但显存与工程门槛高（2nd 需要 flash-attn varlen + transformer_engine 才跑得顺）。两者未在同一控制变量下比较，不构成方法优劣证据。置信度中。

### 分歧二：伪标签/蒸馏是必需杠杆吗？

- 支持方：1st（蒸馏是标题级主张："Distill is all you need"）；2nd（240k PL）；3rd（500k+ PL，单模 0.895→0.880）；9th（+0.006）；
- 反对方：5th **完全不用** PL/蒸馏/1M 数据，靠奖励预训练 + 两模型融合拿到第 5。

**裁决**：PL/蒸馏提供 +0.006~0.015 量级的增益，但当起点已是强奖励模型时并非必需；且 PL 有副作用——3rd 观察到"PL 让 CV/LB 相关性断裂（CV 数值低很多）"，怀疑与泄漏子集有关。**在存在数据泄漏的评测里，PL 的增益最可疑**（PL 由在泄漏子集上占优的模型生成）。置信度中高。

### 分歧三：截断策略与上下文长度

16th：左截断是最大单步之一（0.890→0.885），理由是保留最近轮次；9th 同样 left；3rd 说"不做花哨截断，推理时延长序列也没帮助"（train 1800）；2nd 直接 4340 全量；1st 训练只用 1024 却靠蒸馏。

**裁决**：截断方向的影响随"对话轮数分布 × 模型上下文能力"变化；语料以多轮为主时左截断占优（保住末轮），单轮长文场景差异小。无普适最优，需按任务分布验证。置信度中。

## 4. 增量数字账

**16th 的公共 notebook 改良阶梯（本场最完整的单变量账，LB 越低越好）**

| 步骤 | 改动 | LB |
| --- | --- | --- |
| 起点 | @emiz6413 公共 notebook | 0.941 |
| 1 | TTA=True | 0.926 |
| 2 | r16→r64、a32→a16、freeze16→0 | 0.913 |
| 3 | 加模块 down/up/o/gate + r64/a4 | 0.903 |
| 4 | 加入 33k 去重数据（100%） | 0.899 |
| 5 | max 1024→2048 | 0.895 |
| 6 | r64→**r1024** | 0.894 |
| 7 | fp16 训 + 8bit 推（+10% 速度） | 0.894 |
| 8 | 推理 max 3072 | 0.893 |
| 9 | 两个不同 Gemma2 的 TTA | 0.891 |
| 10 | 3 头推理（偏好/model_a/model_b，弃后两输出） | 0.890 |
| 11 | **左截断** | 0.885 |

**其余关键数字**

| 方案 | 数字 |
| --- | --- |
| 1st | 5 折 CV：qwen72b 0.875/0.881/0.869/0.880/0.875；llama3-70b 0.874/0.877/0.877/0.873/0.873；蒸馏 gemma9b **0.862/0.876/0.858/0.872/0.868**（学生逐折不输 70B 教师）；LB 0.882 → TTA 0.876；最终 PB 0.96898 |
| 2nd | stage1：9b 0.891 / 27b 0.883 / ArmoRM 0.899 → 平均融合 0.876；stage3 两模型 0.884/0.890 → 融合 0.876~0.877；ArmoRM 旧 LB 0.873 → 全量数据 0.869 → 2:1 融合 **0.868**；full swap +0.003；格式增强 +0.001 |
| 3rd | Gemma2-RM 单模 ≈0.895；+500k PL 后 0.880（8k 无 TTA）；关 softcapping +0.002；TTA ~0.007；第二轮 PL 无增量 |
| 5th | 奖励预训练最多 +~0.020（口径存疑）；单折 ~0.880；融合 ~0.873 |
| 9th | 0.890 → 换序模型替代 TTA 0.887 → +chat-1m PL 0.881（private 0.9859）→ +llama3 融合 0.881（private 0.9828） |
| 16th | 单模 CV 0.878 / LB 0.888（赛后发布） |

**可复算校验（3 处算术吻合）**

1. LoRA 参数量 ∝ rank：16th 自述 r16≈50k、r64≈200k → 比值 4 = 64/16 ✓；
2. 2nd 的 240k PL = 110k（lmsys-1m）+ 130k（其他数据集）✓；
3. 9th 的 token 预算：train 256×6=1,536；infer 256×7=1,792 ✓。

**alpha 比例规则（16th，可检验）**：backbone LR =（alpha/rank）× head_LR。同一 head LR 下最优 alpha 与 rank 无关：LR 2e-4 → alpha=4；LR 2e-5 → alpha=192；LR 6e-5 → alpha=64。三条观测一致支持"alpha 补偿 LR"的线性关系（192/4=48≈2e-4/2e-5=10 的对数差？——严格说是 alpha∝1/LR 的近似，具体比值待独立验证；登记为待核）。

## 5. 机制推演

**M1｜奖励起点为何有效**：偏好判断=成对比较任务；UltraFeedback/Arena-hard/mt-bench 等奖励数据已让模型学会"读两个回答并输出优劣"的表示，下游只需把输出头换成 3 分类并适配领域。chat 模型要先学会"比较"本身（5th 只给二分类 win/loss 就触发同样增益，说明"学比较"而非"学具体奖励格式"是关键）。

**M2｜logits 蒸馏 > 硬伪标签**：教师输出的是分布（软标签），携带类间相似性与不确定性（暗知识）；9B 学生在 5 折教师集成上拟合，逐折 CV（0.858–0.876）与 70B 教师（0.869–0.881）几乎重叠——**容量被压缩 8 倍而精度不丢**，这正是"推理约束下的蒸馏"命题的实证。硬 PL（argmax/one-hot）信息量少，且由泄漏子集生成时会把泄漏优势一起蒸进学生（M6）。

**M3｜A/B 交换的数学与实现细节**：位置偏差项 b 使 logit 差 d 在交换后近似 −(d+2b)；平均两次即消 b。2nd 的细节最有价值：把原样本与交换样本放进**同一次 optimizer.step**（梯度累积），等价于对"对称对"做一次精确更新；若当作两个独立样本，噪声使增益从 0.003 变得不稳定。

**M4｜左截断的机制**：多轮对话中，决定偏好的通常是最后几轮；长历史 prompt 占据 token 预算会挤掉末轮。16th 在 1024 预算下左截断 = 信息密度最大化（+0.005，全场最大单步之一）。边界：单轮长文档/代码任务里左截断会切掉题干，需反向处理。

**M5｜8-bit vs 4-bit 的数值解释**：分类 logit 是连续量，量化误差直接进入 log loss；4-bit 的 scale 粒度在 logit 尾部（决定 tie/close call）误差大；而生成任务对单个 token 的 logit 误差容忍度高（采样/argmax 缓解）。工程上 bnb 4-bit 的反量化在每次前向都发生，8-bit 的向量化更高效。故"8-bit 又快又准"。

**M6｜PL 与泄漏的相互作用**：当测试集与公开语料（lmsys-1M）重叠时，PL 由模型对"可能见过的样本"生成 → 学生继承了泄漏优势；这种优势在 CV（干净子集）上不可见，在（被重评的）私榜上也未必保留。3rd 观察到的"CV/LB 相关性断裂（CV 低很多）"与此一致。**教训：泄漏存在时，伪标签/蒸馏的评测协议必须去除重叠样本，否则一切数字都不可信。**

## 6. 证据分级

| 断言 | 等级 | 说明 |
| --- | --- | --- |
| 16th 的 11 步 LB 阶梯 | **可读取（帖内数字）** | 逐步单变量，但为顺序累积（非随机消融）；部分步含噪声（末步 ±0.002） |
| 1st 的逐折 CV 表 | **可读取（帖内表）** | 学生 0.862–0.876 vs 教师 0.869–0.881 |
| 2nd 的阶段数字 | **可读取（帖内表）** | 教师/融合/旧 LB 齐全 |
| A/B 交换增益（0.003–0.015） | **多家自述一致** | 量级一致（交换实现不同）；无一方给出置信区间 |
| 8-bit ≥ 4-bit | **四家自述一致** | 缺精确对照表；方向性置信度高 |
| 奖励预训练"+~20 points" | **弱（口径不明）** | 'points' 可能指 0.020；无法核验 |
| "PL 打断 CV/LB 相关性" | **自述（3rd）** | 机制推测（泄漏）未证实 |
| 泄漏事件本身 | **二手（简介级）** | 各帖只提及；原始讨论未收录，终局 PB 数字与公开阶段不同口径 |
| alpha 比例规则 | **自述 + 部分可复算** | 三条观测（2e-4/4、2e-5/192、6e-5/64）内部关系待更多验证 |

## 7. 边界条件与反事实

- **硬约束是 T4×2 16GB**：一切路线围绕它设计——8-bit 推理、双 GPU 对半分工（5th）、按长度动态批（9th/5th）、条件推理（9th 的 llama3 只处理 ≤512 或 ≥1500 token）、训练上限 3072–4340。若换成 A100，方法选择会变（1st 的 70B 教师就用了 QLoRA 两卡）。
- **反事实（16th/3rd）**：若更早上 8-bit 推理，可同时获得 +10% 速度与更大 context，从而把 TTA/多模型预算提前释放——3rd 明确写"悔恨没早发现"。
- **反事实（5th）**：证明"无 PL 无蒸馏"也能第 5；若叠加 PL（其起点已是奖励预训练），上限大概率再 +0.005~0.01，但 PL 的泄漏风险也同时引入。
- **反事实（1st）**：若没有 70B/72B 教师，蒸馏路线不成立——该方法的前提是"你有更大的教师可用"；这与其他赛场的硬约束（无外部数据/无大模型）冲突。
- **口径警告**：9th 的 private 0.9859/0.9828、1st 的 PB 0.96898 与本阶段的 LB 0.876–0.89 不是同一评测；任何跨帖数字比较都需标注口径。

## 8. 悬案与失败学

**悬案**

1. **泄漏的具体结构与官方处理**（哪些样本重叠、如何重评）未收录原始讨论——本场所有终局数字因此带星号；
2. **PL 打断 CV/LB 相关性的机制**：泄漏说之外（例如软标签使模型更依赖分布内模式）没有替代解释和对照实验；
3. **alpha 比例规则的适用边界**：16th 的观测（alpha 与 rank 无关、补偿 LR）在别的模型/数据集上是否成立，未见独立复现。

**失败学**

| 失败 | 来源 | 教训 |
| --- | --- | --- |
| Llama3.1-405B-as-a-judge 造合成数据（3 种做法） | 16th | 教师强 ≠ 数据有用；本地 logloss ~0.95 的合成数据对训练零增益（分布不对齐） |
| Gemma2-27B 训不起来/调不出 | 2nd/3rd | 9B→27B 不是免费午餐；2nd 需 bs=80 + 关 grad_clip 才成功，3rd 直接放弃 |
| 预测"模型身份"辅助损失 | 3rd | 无增益（与 3 头的 16th 报告不一致——头部结构收益未定论） |
| Llama 3.1 微调差于 Llama 3 | 3rd | 版本更新≠更适合任务（数据配比差异） |
| PL 第二轮迭代 | 3rd | 无增量（一轮到位；伪标签自举的边际收益快速衰减） |
| 第 2 个数 Quantize/TTA 流程未跑通 | 1st | 一个提交因删除模型文件失败——提交工程的稳定性也是分数 |
| 时间不足导致 llama3 只覆盖部分样本 | 9th | 推理预算内做条件推理是权宜，损失覆盖度 |
| 3rd 早期文档：默认序列分类头初始化 | 2nd | ForSequenceClassification 头初始化导致早期高 loss，需重初始化 |

## 9. 图表证据

> 路径相对本文件（`analysis/deep/`）：`../../intel/lmsys-chatbot-arena/bodies/527596_img/NN.ext`。本场仅 2 张图（Chris Deotte 帖）。

**图 1：LoRA 的结构与双学习率（16th 帖，含正文未展示的公式细节）**（topic 527596）——`../../intel/lmsys-chatbot-arena/bodies/527596_img/01.png`

![lora diagram](../../intel/lmsys-chatbot-arena/bodies/527596_img/01.png)

*读图结论*：9B Gemma2 backbone 冻结 + 两组 LoRA 矩阵（各约 10 万参数）；**Head 学习率 2e-4；Backbone 学习率 =（alpha/rank）× 2e-4**——这就是 16th 调参配方的形式化（先固定 rank 扫 alpha，再固定 alpha 扫 rank）；三个头（preference / model A / model B）对应其"3 头推理 +0.001"的配置。

**图 2：三种多 GPU 并行方式（16th 帖的配图）**（topic 527596）——`../../intel/lmsys-chatbot-arena/bodies/527596_img/02.gif`

![parallel types](../../intel/lmsys-chatbot-arena/bodies/527596_img/02.gif)

*读图结论（GIF，218KB，GitHub 可渲染）*：数据并行（每卡完整模型、批并行）、模型并行（模型切分、批串行）、混合并行（都并行）。16th 的评注："HuggingFace trainer 只用前两种；Axolotl/DeepSpeed 才能用第三种"——这是"多卡利用率决定训练成本"的入门教材。

## 10. 对既有笔记/playbook 的修订点

1. `notes/nlp/lmsys-chatbot-arena.md` 升级：补齐 6 篇作者/票数/角色；方案谱系从 16th 单行扩为 7 维对照矩阵；新增奖励起点、蒸馏/PL 三态、A/B 交换数学、8-bit 判据、泄漏警告与图证节；修正出处（原仅列 3 篇）。
2. `playbook/nlp.md` 增补：
   - **偏好/排序任务的起点选择**：reward/pair-preference 模型 > chat 模型；奖励数据预训练清单；
   - **蒸馏三件套**：教师集成出软标签 → 学生 logits 蒸馏；硬 PL vs 软标签的信息差；PL 自举一轮到位；
   - **位置偏差消除**：训练期 full swap（同 optimizer.step）与推理 TTA 的互换关系；
   - **截断方向按任务分布选择**（多轮→左截断保末轮）；
   - **量化推理的位数选择**：分类/对数损失任务优先 8-bit。
3. `playbook/00-通用方法论.md` 增补：
   - **泄漏存在时 PL/蒸馏的评测协议**（去重叠后再评估，否则 CV/LB 都不可信）；
   - **终局口径警告**（重评后的私榜与公开阶段数字不可直接比较）；
   - **LoRA 双学习率规则**（alpha 补偿 backbone LR 的调参顺序）。

## 11. 出处

- 16th（Chris Deotte）：https://www.kaggle.com/competitions/lmsys-chatbot-arena/discussion/527596
- 1st（sayoulala）：https://www.kaggle.com/competitions/lmsys-chatbot-arena/discussion/527629
- 2nd（tascj）：https://www.kaggle.com/competitions/lmsys-chatbot-arena/discussion/527685
- 3rd（Mark Tenenholtz & Raja）：https://www.kaggle.com/competitions/lmsys-chatbot-arena/discussion/527766
- 5th（Team Danube）：https://www.kaggle.com/competitions/lmsys-chatbot-arena/discussion/527669
- 9th（Ebi）：https://www.kaggle.com/competitions/lmsys-chatbot-arena/discussion/527704
- 未收录缺口（登记备查）：527595（18th）｜527627（21st）｜528288（19th）｜529067（4th）｜527591（26th）｜527938（156th）｜540876（13th）等
