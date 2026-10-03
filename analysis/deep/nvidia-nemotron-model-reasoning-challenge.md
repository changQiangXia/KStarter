# Nemotron 推理赛深读：确定性求解器 → 可学习 CoT 轨迹

> 赛事：Featured ｜ 主题 nlp/reasoning（puzzle 推理）｜ 4185 队 ｜ 标准赛 ｜ 指标：NVIDIA Nemotron Metric（答案解出率；数值相对误差 ≤1e-2）
> 材料基础：`digests/nvidia-nemotron-model-reasoning-challenge.md`（8 篇：1st 140 票/2nd/3rd/18th/10th/公 2 私 6/88th/7th；120 条索引）+ 进度奖正文 `bodies/689915.txt`（241 票）+ 11 张图
> 深读时间：2026-10（Tier A #48）

## 0. 一句话重述：这道题真正在考什么

题面是"提升 Nemotron-3-Nano-30B（30B MoE，3B 激活参数）的推理能力"——每题给若干输入-输出示例，推断隐藏变换并应用到 query；**只能提交 rank≤32 的 LoRA**；评测 vLLM、temp=0、max_tokens=7680、答案在 `\boxed{}`，**评测时不能运行程序**。实际被考的是**把确定性程序翻译成模型可模仿的 CoT 轨迹**：

1. **主路线是"确定性求解器 + SFT 蒸馏"**：1st/2nd/3rd/10th/18th/88th/progress prize 所有头部方案都用代码写 reasoner 生成 teacher CoT，再用标准 LoRA SFT 让模型模仿；2nd 明确"focal loss/token 重加权/多阶段都没赢过标准交叉熵"。
2. **CoT 是训练目标，不是解题记录**：huikang 的 6 条设计原则（deterministic / simple / coverage / within-limit / tokenization-aware / generalizable）；18th 的"短、局部、无隐藏计算、引用完整、每步只依赖已引入的小规则"；10th 用逐 token logprob 找脆弱步骤。
3. **记忆 vs 计算的分工**：cryptarithm 全搜索 ~5e10 候选无法在 7680 token 内逐 token 展开 → 1st 预计算 **4205 个签名目录**让模型背下来，再用 DFS 只做一致性检查；bit manipulation 用 HEX 压缩列 + 规则序列修复。**不可能逐步计算的部分，让模型记住有限中间结构**。
4. **长尾类别决定名次**：bit（1602 题）+ cryptarithm（823 题）是最大分差来源；progress prize 目标解出率 87.7% 中 bit 85.1%、crypt 8%，而 cipher/numeral/unit/gravity 都可 100%。
5. **训练-服务对齐是隐藏胜负手**：Tinker 的 LoRA 合并需要 SVD（损失 ~25% 奇异质量）→ 2nd 换 Megatron-Bridge 后端后 bit 精度 0.81→0.89；还有 QKV 交错、专家权重融合等格式坑。
6. **小测试集的验证纪律**：public LB 在 0.86 有"墙"、波动大；3rd 实测 validation↔private r=0.898 而 validation↔public r=0.365；10th 用 validation 选提交（公 0.860/私 0.880）胜过按公榜选（0.872/0.852）。

一句话：**这是一场"用代码写出最优策略、再把它蒸馏进小模型"的比赛**——简单 SFT + 精心设计的 CoT 打败了 RL、复杂损失与更大模型蒸馏。

## 1. 材料与角色

| 帖子 | 作者 | 票数 | 角色与独有信息 |
| --- | --- | --- | --- |
| [689915](https://www.kaggle.com/competitions/nvidia-nemotron-model-reasoning-challenge/discussion/689915) 进度奖 | huikang | 241 | **CoT 设计六原则**；目标函数=最大化轨迹最小 logprob（阈值 0.69）；只 SFT、拒绝 RL 与大模型蒸馏；逐类目标解出率与实测（总 85%）；成本 ~$282；Tinker→提交适配器转换（SVD 损失、专家融合） |
| [709231](https://www.kaggle.com/competitions/nvidia-nemotron-model-reasoning-challenge/discussion/709231) 1st | — | 140 | 记忆 vs 计算分工：cryptarithm **签名目录（4205 signatures）+ DFS** → 公 0.89/私 0.908；bit 的 HEX 压缩 + 规则修复 + extra training → **公 0.91/私 0.920**，未选最佳私 0.932；合成 890M+590M tokens |
| [711703](https://www.kaggle.com/competitions/nvidia-nemotron-model-reasoning-challenge/discussion/711703) 2nd | — | — | 简单 CE 最优；bit 合成 trace 0.9906 vs LoRA 生成 0.9732；**Tinker→Megatron-Bridge：bit 0.81→0.89**；QKV 交错 bug；训练细节（57.6k 例、EP=4、per-expert LoRA 888M、r=32） |
| [709136](https://www.kaggle.com/competitions/nvidia-nemotron-model-reasoning-challenge/discussion/709136) 3rd | — | — | **两阶段训练**：stage1 记忆模式（drills）→ stage2 学执行；同数据 12K：直接 12/17 vs 两阶段 16/17（私 0.888→0.900）；validation↔private r=0.898 vs public r=0.365 |
| [715330](https://www.kaggle.com/competitions/nvidia-nemotron-model-reasoning-challenge/discussion/715330) 18th | — | — | "确定性求解器 → 可学习轨迹"的系统总结；**最大错误=没有本地验证**；合成分被公榜误导过早放弃（私榜其实更好） |
| [708535](https://www.kaggle.com/competitions/nvidia-nemotron-model-reasoning-challenge/discussion/708535) 10th | — | — | 纯确定性老师（oracle 覆盖 90.6%）→ 模型接近 oracle；用 validation 选提交获更好私榜；排除失败轨迹反而降分；两阶段/课程/3× priority 均无净增益 |
| [709120](https://www.kaggle.com/competitions/nvidia-nemotron-model-reasoning-challenge/discussion/709120) 公 2/私 6 | — | — | **逐域 LB 探针**（其他域输出 dummy → 纯单域信号）；bit 模板表（18 个公式覆盖 train）；hex 计算+速查表 |
| [708539](https://www.kaggle.com/competitions/nvidia-nemotron-model-reasoning-challenge/discussion/708539) 88th | — | — | 不改 reasoner（87.8%）：目标不是"解更难的题"，而是"**别丢已经能解的题**"；合成数据改进闭环 |
| [712395](https://www.kaggle.com/competitions/nvidia-nemotron-model-reasoning-challenge/discussion/712395) 7th | — | — | bit 用字符串匹配+回溯（>96% 验证）；**单 bit tokenization + dynamic loss masking** 教假说/自评/回溯 |

**材料缺口（受"不扩采"约束，登记备查）**："Strategy to solve 85% of bit manipulation"(690307,111)、"Answers To Everything Data: 100% Solve Rate"(688461,158)、"Visualize problems and completions"(684212,149)、"Why GRPO is Painfully Slow"(690161,63)、LLM 性能对照(684283,63)、起步资源(681745,60)、"97.2% Gold-Conditioned Symbolic Solver"(698293,56)、数据集幻觉质疑(684192,55) 等未收录——**bit 解法的独立详解与"gold-conditioned 泄漏"争议**是主要缺口。

## 2. 逐方案对照矩阵

| 维度 | 进度奖 huikang | 1st | 2nd | 3rd | 10th | 7th |
| --- | --- | --- | --- | --- | --- | --- |
| CoT 来源 | 确定性程序（六原则） | 确定性程序 + 目录记忆 | 确定性程序（bit 最深） | 两阶段：模式→执行 | 纯确定性程序 | 字符串匹配+回溯 |
| 训练 | SFT（min-logprob 目标） | SFT（标准 CE，LoRA r32） | SFT（标准 CE） | stage1 记忆 + stage2 执行 | SFT（标准 CE） | SFT + dynamic loss masking |
| 记忆 vs 计算 | 尽量不记忆答案 | **背签名目录 + DFS** | 背 bit 模板/模式 | 阶段化记忆 | 尽量过程化 | bit 结构搜索 |
| bit 方案 | 列/规则匹配 + 85% | HEX 压缩 + 规则序列修复 | 模板枚举 + hex 计算 | 含在整体 | 重写 reasoner 匹配真实结构 | 单 bit token + 回溯 >96% |
| cryptarithm | 仅 concat/rev_concat（~8%） | 签名目录 → 42.9% solver/38.1% 模型 | 基本不动（9.6%） | 两阶段后 ~30% deduce | 9% | 未训 |
| 后端 | Tinker（SVD 转换损失） | — | **Megatron-Bridge（精确映射）** | 自建 RTX PRO 6000 | — | — |
| 验证 | 自建 950 验证 | 15% 划分 + LB 平均 | 合成数据 + train 全量验证 | 10% 分层 holdout；r 分析 | 950 划分；按 validation 选提交 | 验证集 |
| 成绩 | 0.85（目标 0.877） | 公 0.91/私 **0.920**（未选 0.932） | 公 0.884/私 0.908 | 私 **0.900** | 公 0.860/私 0.880 | 金区 |
| 失败清单 | SVD 损失 / 训练-服务错位 | （未详列） | focal/reweight/multi-stage、Tinker SVD、QKV bug | 无验证、合成过早放弃 | 课程/两阶段/3× priority/排除失败轨迹/LoRA merge | 未训符号题 |

## 3. 共识、分歧与裁决

### 共识一：确定性求解器 → SFT 蒸馏是唯一主路线（7/7）

所有头部方案：写代码求解器 → 生成 CoT → 标准 LoRA SFT；无 RL、无大模型蒸馏（huikang 的显式赌注：**策略已知时只需模仿**；2nd/3rd/10th 用标准 CE）。

**裁决**：在"评测 temp=0、不能执行程序、变换空间可由代码枚举"的设定下，最优策略就是"写出算法再教模型背算法"；RL 的意义被结构性削弱。置信度：高。

### 共识二：CoT 的可学习性 > 求解器的正确性（18th/10th/88th/huikang）

18th：trace 要"短、局部、无隐藏计算、引用完整"；10th：用逐 token logprob 找脆弱步骤；88th：目标不是解更难的题，而是别丢已可解的题；huikang：每步只依赖已引入的小规则。

**裁决**：**求解器能力是上限，CoT 可学习性决定能否兑现**；两者独立优化，且后者更常被忽视。置信度：高。

### 共识三：标准 CE 足够，复杂训练方案不划算（2nd/10th 的对照实验）

2nd：focal loss、token loss 重加权、多阶段训练"none convincingly beat standard LoRA SFT"；
10th：curriculum、两阶段、3× priority、LoRA merge/seed soup 都无净增益；排除失败轨迹反而降分；
3rd 的两阶段是唯一例外的成功（见分歧）。

**裁决**：数据（CoT）质量主导，损失/课程/合并是二阶项；**先修 teacher，再谈 trick**。置信度：中高。

### 共识四：小测试集 + public 墙 → validation 是唯一可靠信号（3rd/10th/18th）

3rd：validation↔private r=0.898、↔public r=0.365；public LB 有明显 0.86 墙；
10th：按 validation 选的提交（公 0.860/私 0.880）优于按 public 选的（0.872/0.852）；
18th：最大错误=没有本地验证 → 探索发散、提交选择失败。

**裁决**：测试集小（~500）且噪声大，public LB 每 0.01≈3 题；**必须建分层 holdout（含增广样本隔离）并用它选提交**。置信度：高。

### 分歧一：记忆 vs 计算——huikang 的"不记忆"原则 vs 1st 的"签名目录"

huikang：不要训练模型背答案，要通用；
1st：cryptarithm 全搜索不可展开 → **预计算 4205 个签名目录并让模型背诵**，再用 DFS 检查一致性；
3rd：把记忆独立成 stage1（drills）——12K 数据直接训 12/17，两阶段 16/17；
2nd：bit 也靠记忆模板/模式。

**裁决**：原则应精确化为"**不背答案，但可以背可复用的有限中间结构**"（签名目录、模板、规则表）；是否记忆取决于搜索空间能否在 7680 token 内展开。3rd 的两阶段是"记忆与应用分离"的架构化实现。置信度：高（多处独立证据）。

### 分歧二：训练后端/适配器格式（Tinker vs Megatron-Bridge vs 自建）

huikang：Tinker 产出适配器需转换（专家解融合、gate+x SVD、lm_head），SVD 只保留 75% 奇异质量 → 训练-服务错位；
2nd：换 Megatron-Bridge（精确 PEFT 映射）后 bit 0.81→0.89；还发现 QKV 交错 bug；
3rd：自建单卡训练（RTX PRO 6000）。

**裁决**：**LoRA 的"训练格式 = 部署格式"是硬约束**；转换损失会吃掉数据/算法收益，选基础设施前先核对映射。置信度：高。

### 分歧三：失败/低置信轨迹是否训练

10th：排除失败轨迹**降分**（rule_unknown 的 fallback 轨迹有信号）；
88th：保留可解样本的完整覆盖；
2nd：简化/清理 trace。

**裁决**：模型需要学会"规则不确定时如何给出最可能的猜测"（guess 类题占分），因此**失败模式要作为 fallback 模式保留**，而不是删除。置信度：中高。

## 4. 增量数字账

| 动作 | 数字 | 来源 |
| --- | --- | --- |
| 赛事机制 | Nemotron-3-Nano-30B（30B MoE/3B active）；LoRA rank≤32；temp=0；max_tokens **7680**；9 类 9500 训练题 | 元数据/各帖 |
| 进度奖目标/实测 | 目标解出率 87.7%（8333/9500）→ 实测 85%；bit 目标 1364/1602=85.1%；cipher/numeral/unit 100%、gravity 100%、equation 76.6%、crypt 7.9% | 689915 |
| 进度奖成本/规模 | 27,850,703 tokens（获胜解）/598,958,637（总）；~$212.48 Tinker+~$60 Modal+$10 订阅；min-logprob 阈值 0.69 | 689915 |
| 1st 数据 | 主训练 220k 样本/890.1M tokens；extra 140k/590.7M；validation 1,424；类别最大 cryptarithm 120k+40k | 1st |
| 1st cryptarithm | 签名目录 **4205 signatures**；枚举 100×100×22 规则；示例 ABCCCDD 15 候选（add 1/flip_add 8/flip_add+1 6）；solver 42.94%/模型 38.09%（deduce）、12.80%/12.20%（guess） | 1st |
| 1st bit | solver 97.50% → 模型 93.45%（train.csv within budget）；HEX 列压缩；规则序列修复 | 1st |
| 1st 其他类别（solver→模型） | cipher 100→99.49、numeral 100→100、unit 100→100、gravity 100→99.87、equation deduce 95.47→95.30、guess 52.94→52.21 | 1st |
| 1st 成绩 | 公 0.91/私 **0.920**；未选最佳私 **0.932**；训练 119h（主）+51h（extra） | 1st |
| 2nd | bit 合成 trace 0.9906 vs LoRA 0.9732（train.csv）；总合成 0.9107 vs LoRA 0.9074；公 0.884/私 0.908；Tinker→Megatron bit **0.81→0.89**；57,600 例、EP=4、per-expert LoRA ~888M、r=32 | 2nd |
| 3rd 两阶段 | 12K 同数据：直接 12/17 vs 两阶段 16/17；最终 ablation 12/17（私 0.888）vs 16/17（私 0.900）；stage1 44,136 例/159M tokens/25.2h；stage2 72,377 例/299M/32.7h | 3rd |
| 3rd 验证 | validation↔private r=0.898、↔public r=0.365；public↔private r=0.220；0.85 公榜提交私榜 0.90 | 3rd |
| 10th | oracle 覆盖 90.6%（bit 98.8%、crypt 9.0%、equation guess 41.2%）；公 0.860/私 0.880；按 validation 选提交优于按 public（0.872/0.852） | 10th |
| 88th | reasoner 87.8%（几乎未改）；目标"别丢可解题" | 88th |
| 7th | bit >96% 验证（>98% 预期）；单 bit token；dynamic loss masking | 7th |

**结构校验（2 处吻合）**

1. 1st 的类别题数（1602+732+823+1576×2+1594+1597=9500）与赛事总题数一致 ✓；
2. 3rd 的 private r=0.898 与 10th 的"按 validation 选提交更好"相互印证 ✓。

## 5. 机制推演

**M1｜为什么"确定性 CoT + SFT"打败 RL**：评测 temp=0 且最大 token 预算固定，目标不是探索最优策略，而是**让固定算法被逐 token 复现**。如果答案可由代码计算，最优策略已知；RL 只在策略未知时有价值。min-logprob 目标（最大化轨迹最弱 token 的 logprob）直接优化"整条轨迹可被贪心复现"的概率——比平均 CE 更贴合评测。

**M2｜记忆与计算的边界**：cryptarithm 完整的"数字×规则"搜索 ~5e10，任何逐 token 轨迹都无法在 7680 token 内展开。1st 的解法把搜索分解为：**签名（重复结构）→ 预计算候选目录（可背）→ DFS 一致性检查（可执行）**。bit manipulation 同理：把"按位枚举全部规则"换成"规则库匹配 + HEX 列压缩 + 修复"。**可背诵的有限中间结构 = 把不可展开搜索折叠成可学习轨迹**。

**M3｜训练-服务对齐的量化影响**：Tinker 的 LoRA 需要 SVD 合并 gate/x 投影（rank 64→32）并解融合专家权重，只保留 ~75% 奇异质量 → 训练时使用的方向在推理时被截断，表现为"写不出 \boxed、重复 token、模板漂移"。2nd 换后端后 bit 0.81→0.89，说明**基础设施的映射精度 = 分数**。

**M4｜小测试集的统计力学**：测试 ~500 题（公/私各 250），0.01≈3 题；public 墙（0.86）可能是分布/难度断层。3rd/10th 的相关性分析证明 validation 是唯一稳定信号；2nd 的逐域 dummy 探针（其他域输出 `I will ignore this problem`）是把 public LB 变成"单域测量仪"的工程手段。

**M5｜长尾类别的边际收益**：bit+crypt 占 25% 题目但难度最高；头部差距几乎全在这两个域（1st 的 crypt 42.9% vs 进度奖 8%；7th 的 bit >96% vs 进度奖 85%）。**先提高 solver 覆盖率（新洞察），再提高 trace 可学习性（蒸馏）**，两者缺一不可（10th 的 oracle=90.6% 而模型≈oracle，说明 solver 上限直接约束模型）。

**M6｜"猜测"类样本的价值**：query 操作符未出现（guess 类）时没有唯一解，正确行为是"给出最可能的猜测"；10th 排除失败轨迹反而降分、1st/3rd 专门为 guess 设计 fallback 逻辑——**模型必须学会在信息不足时按先验下注**，这既是覆盖也是校准问题。

## 6. 证据分级

| 断言 | 等级 | 说明 |
| --- | --- | --- |
| 进度奖六原则/解出率/成本 | 自述 + 公开代码/日志/notebook | 高 |
| 1st 签名目录/类别覆盖表/分数曲线 | 自述 + 图 + 代码链接 | 高 |
| 2nd 后端对照（0.81→0.89）与训练细节 | 自述 + GitHub | 高 |
| 3rd 两阶段/相关性图 | 自述 + 图 | 高 |
| 10th oracle/提交选择 | 自述 + 表 | 中高 |
| 18th 方法论总结 | 自述（叙事为主） | 中 |
| 88th/7th | 自述 | 中 |
| "Answers to Everything"数据集（未收录） | 仅标题 | 低（登记） |

## 7. 边界条件与反事实

- **反事实 1**：若用 RL/大模型蒸馏替代确定性 CoT → huikang 的赌注 + 2nd/3rd/10th 的实践都指向 SFT 足够（策略已知）。
- **反事实 2**：若不做签名目录记忆 → cryptarithm 无法在 token 预算内展开（1st 的 42.9%→8% 量级差）。
- **反事实 3**：若不在 trace 里用 HEX 压缩/单 bit token → bit 类超预算或分词错位（1st/7th 的工程）。
- **反事实 4**：若用 Tinker 而不解决 SVD 对齐 → bit 掉 ~0.08（2nd 实证）。
- **反事实 5**：若按 public LB 选提交 → 10th 的 0.872/0.852 vs 0.860/0.880 反例。
- **边界**：结论依赖"任务可由代码求解 + 评测禁止执行程序 + 输出在 7680 token 内"；开放生成/无确定解任务不适用"目录记忆"路线。

## 8. 悬案与失败学

**悬案**

1. **"Answers To Everything Data: 100% Solve Rate"（688461，158 票）未收录**：是否存在覆盖全类别的答案式数据/泄漏红利，未得到核实。
2. "97.2% Gold-Conditioned Symbolic Solver"（698293）与"数据集幻觉"质疑（684192）未收录——gold-conditioned 求解是否利用了答案，属于规则灰区。
3. bit 解法详解（690307，111 票）未收录；7th 的 arXiv 预印本未收录。
4. 评测 serving 与训练的对齐细节（vLLM 版本、LoRA 加载路径）只在零散帖中出现。

**失败学（跨队合集）**

- 训练类：focal loss/token reweighting/multi-stage（2nd）；curriculum/两阶段/3× priority 重复/排除失败轨迹/LoRA merge/seed soup（10th）；长 epoch 未提（各队基本 1 epoch）。
- 基础设施类：Tinker SVD 损失（huikang/2nd）；Megatron QKV 交错提取 bug（2nd）；适配器 key 前缀/专家格式（huikang）。
- 流程类：没有本地验证 → 探索发散与提交错选（18th/3rd/10th 的共识教训）；合成数据方向被 public 分误导而过早放弃（18th）。
- 覆盖类：cryptarithm 求解器覆盖不足是多数队的上限（10th 9%、88th 9%、2nd 9.6%）。

## 9. 图表证据

> 路径相对本文件（`analysis/deep/`）：`../../intel/nvidia-nemotron-model-reasoning-challenge/bodies/<topic>_img/NN.ext`

**图 1：1st 的 LB/验证分数曲线**（topic 709231）——`../../intel/nvidia-nemotron-model-reasoning-challenge/bodies/709231_img/01.png`

*读图结论*：Public（蓝）/Private（红）/Validation（黑）随步数上升；红点标出未选中的 **0.932 私榜**峰；public 明显低于 private 且更平（0.86 墙）。**同一次训练不同 checkpoint 的私榜波动巨大**——选提交必须靠 validation。

**图 2：3rd 的验证/LB 相关性**（topic 709136）——`../../intel/nvidia-nemotron-model-reasoning-challenge/bodies/709136_img/02.png`

*读图结论*：Validation↔Private r=**0.898**、↔Public r=0.365；Public↔Private r=0.220。**本地验证是唯一可靠信号**，public LB 几乎随机。

**图 3：逐域 LB 探针（公 2/私 6）**（topic 709120）——`../../intel/nvidia-nemotron-model-reasoning-challenge/bodies/709120_img/01.jpg`

*读图结论*：其他域输出 dummy、只让 bit 域真做（`ignore_bit-12.6k-v2` 718/800、1424/1602 → 0.148/0.160；对照 `bit-5k` 0.124/0.140）。**把小测试集的 public LB 变成单域测量仪**。

**图 4：88th 的合成数据改进闭环**（topic 708539）——`../../intel/nvidia-nemotron-model-reasoning-challenge/bodies/708539_img/01.PNG`

*读图结论*：Analyze train.csv → Build generator → Train on synthetic → Evaluate vs original → Compare gap → Fix missing factors，循环直至合成数据逼近原始分布。**合成题生成不是一次性工作，而是收敛环**。

## 10. 对既有笔记/playbook 的修订点

1. `notes/nlp/nvidia-nemotron-model-reasoning-challenge.md` 升级：补 8 篇+进度奖作者/票数、六方案 × 8 维对照、数字账（4205 签名、0.81→0.89、r=0.898、900/908/920/932）与 4 张图证；新增"记忆 vs 计算"与"训练-服务对齐"节。
2. `playbook/nlp.md`（推理赛/CoT 蒸馏节）增补：
   - **确定性求解器 + SFT 主路线**；CoT 六原则（deterministic/simple/coverage/limit/tokenization/generalizable）；
   - **记忆 vs 计算边界**：可展开的用过程，不可展开的背有限中间结构（签名目录/模板/规则表）；
   - **min-logprob 目标**：逐 token 检查最弱环节（阈值化），比平均 CE 更贴近贪心复现；
   - **训练-服务对齐**：LoRA 格式/SVD 转换/专家融合/QKV 提取必须验证；
   - **小测试集纪律**：建分层 holdout、逐域 dummy 探针、按 validation 选提交。
3. `playbook/00-通用方法论.md` 增补：**"CoT 是训练目标，不是解题记录"**；**"把不可展开的搜索折叠成可背诵的中间结构"**；**"验证对齐的优先级高于 LB"**。
4. `analysis/THEORY.md`（Batch 5 末汇总 v0.5）候选：
   - **L81｜策略已知时 SFT > RL**（评测 temp=0 的推理赛）；
   - **L82｜记忆-计算边界：折叠不可展开搜索**（签名目录；证据 = 1st/3rd/2nd）；
   - **L83｜训练-服务对齐即分数**（Tinker SVD 0.81→0.89）。

## 11. 出处

- 进度奖（huikang，241 票）：https://www.kaggle.com/competitions/nvidia-nemotron-model-reasoning-challenge/discussion/689915
- 1st（140 票）：https://www.kaggle.com/competitions/nvidia-nemotron-model-reasoning-challenge/discussion/709231
- 2nd：https://www.kaggle.com/competitions/nvidia-nemotron-model-reasoning-challenge/discussion/711703
- 3rd：https://www.kaggle.com/competitions/nvidia-nemotron-model-reasoning-challenge/discussion/709136
- 18th：https://www.kaggle.com/competitions/nvidia-nemotron-model-reasoning-challenge/discussion/715330
- 10th：https://www.kaggle.com/competitions/nvidia-nemotron-model-reasoning-challenge/discussion/708535
- 公 2/私 6：https://www.kaggle.com/competitions/nvidia-nemotron-model-reasoning-challenge/discussion/709120
- 88th：https://www.kaggle.com/competitions/nvidia-nemotron-model-reasoning-challenge/discussion/708539
- 7th：https://www.kaggle.com/competitions/nvidia-nemotron-model-reasoning-challenge/discussion/712395
- 缺口登记：690307、688461、684212、690161、684283、681745、698293、684192 未收录正文
