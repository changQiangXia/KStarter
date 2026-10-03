# Jigsaw - Agile Community Rules

> 主题：nlp ｜ 子类：— ｜ 领域：内容审核 ｜ 类别：Featured
> 截止：2025-10-23 ｜ 队伍数：2445 ｜ 机制：代码赛 ｜ 指标：AUC
> 数据来源：`intel/jigsaw-agile-community-rules/`（120 条主题索引 + 7 节正文：1st/3rd/6th/7th/12th/120th + 规则公开；23 条 write-up 标记中其余未收录）

## 1. 任务与数据

- **预测目标**：给定"社区规则 + 评论"，判断该评论是否违反该规则（二分类，AUC）。
- **数据形态与核心难点**：
  - 训练集只有 **2 条规则**，测试集有 **6 条规则（其中 4 条全新）**；
  - 规则文本在测试时才可见 → 这是典型的**规则/分布迁移**任务，必须依赖推理期的适配能力。
  - 官方说明公开榜与私榜是**随机划分**，公开榜约占测试集的 30% —— 这一条直接改变了验证策略。
- **规则结构**（社区整理帖）：2 条公开（广告/法律建议）+ 4 条私榜（财务建议/医疗建议/非法活动/剧透）——新规则集中在"专业建议类"审核。
- **赛制关键**：test.csv 的带标签样例可作训练数据 + 12 小时推理窗口 → **Train-on-test 是全场共识**；本地 CV 无法模拟新规则（7th：与 LB 毫无相关）。

## 2. 验证方案

| 方案 | 使用者 | 说明 |
| --- | --- | --- |
| **以公开榜为验证集** | 1st、3rd | 官方确认公开/私榜随机划分，因此公开榜是私榜的无偏估计；1st 明确以此替代不可靠的本地 CV |
| 本地重建新规则样本 | 1st（尝试） | 为 4 条新规则生成逼真评论是"非平凡任务"，成本高 |
| 多模型对照 + 公开榜确认 | 3rd | 所有模型与最终集成都用公开榜验证 |
| 完全信任 LB（本地 CV 仅作冒烟） | 7th | "CV 与 LB 毫无相关"，测试数据量大 |

**与 ICR/Amex 等比赛的关键差异**：本场公开榜是可用的验证信号（随机划分 + 样本量充足），而 ICR/Amex 的公开榜是陷阱。**同一个技术动作在不同比赛里风险完全相反。**

## 3. 方案谱系

| 方案 | 名次 | 关键点 |
| --- | --- | --- |
| Train-on-test + 只算 Yes/No token 损失 + 6 模型集成 | 1st | 剔除 subreddit；候选 token 集 + log-odds；per-rule 排名融合（+0.002）；集成 0.9344/0.9293 |
| TTT + 双速子集成（慢 LLM/快小模型） | 3rd | 慢：8×Qwen2.5/3 7B-14B；快：bge/Qwen3-emb/DeBERTa；LoRA 预训练→TTT→末 token 嵌入→经典 ML |
| **DML 在线互蒸馏**（Qwen3-14B/8B/Guard-4B） | 6th | 无教师 + 软标签极尖（温度 KD 无效）；独立 0.921→DML 0.925；3-peer 0.93237/0.92781 |
| train-on-test + 安全预训练模型 | 7th | shieldgemma-9b 单模最佳 0.927/0.922；Qwen3-8B-Guard 优于 vanilla；vLLM Gemma2 fp16 解锁 hack |
| 无标签软标签预训练 DeBERTa | 12th | 0.912→0.924（2 seeds/1h）；Claude 审计采样；bf16-on-T4 慢 6× |
| RAG 检索 + 不确定 20% 重排 | 120th | Qwen3-0.6B 检索相似例；4× TTA；32B 只处理低置信样本；规则内排名融合 |

## 4. 关键技巧

- **Train-on-test / TTT**：用测试正负样例 + 规则在线微调——本场最大杠杆（全员）。
- **公开榜=验证集**（随机划分 + 30%）：与 ICR/Amex 的陷阱形成对照——**赛制决定技术动作对错**。
- **DML 在线互学习**：无教师时用 KL 互蒸馏；用 3-peer 多样性对冲错误相关性。
- **数据卫生**：剔除 subreddit（+0.007）、rule-body-label 去重、多数投票修标签、弃平票。
- **蒸馏/推理工程**：只算答案 token 损失；候选 token 集 + log-odds；LoRA 合并；Unsloth 14B@16GB T4；长度排序 + forward-only。
- **指标对齐融合**：AUC 按规则内排名后再平均融合（跨规则概率尺度不可比）。
- **领域预训练红利**：安全对齐模型（shieldgemma/Qwen-Guard）在内容审核上先验更强。

## 5. 深读结论（2026-10 补）

- **这是一场"在线适配"比赛**：规则与样例在推理期才出现 → TTT/train-on-test 是唯一强起点；本地 CV 失效是结构性的而非操作问题。
- **公开榜可信度是赛制属性**：随机划分 + 30% 样本量使其成为无偏估计（1st 的论证）；与 llm-detect 的"公开榜陷阱"并置，构成 THEORY L4/L6 的边界条件。
- **无教师蒸馏的现实解**：DML（6th）用互学习绕过"需要更强教师"，并用 peer 多样性控制相关性；私榜 +0.004~0.006。
- **数据卫生与新规则的放大效应**：subreddit 剔除 +0.007、标签多数投票——规则迁移下伪相关被放大，清洗优先于建模。
- **12 小时窗口的预算学**：Unsloth/LoRA 合并/长度排序/不确定重排，全部为"多塞一个模型"；与 rsna/MAAP 的推理金字塔同构。

## 6. 图表证据

**图 1：DML 互学习结构**（6th，topic 613150）——`../../intel/jigsaw-agile-community-rules/bodies/613150_img/01.PNG`

![dml](../../intel/jigsaw-agile-community-rules/bodies/613150_img/01.PNG)

*读图*：两模型共享 prompt，双向 KL（p1↔p2）+ 各自 CE——没有教师，学生互为教师。

**图 2：RAG + ReRanker 管线**（Chris Deotte，topic 613168）——`../../intel/jigsaw-agile-community-rules/bodies/613168_img/01.png`

![rag](../../intel/jigsaw-agile-community-rules/bodies/613168_img/01.png)

*读图*：检索（Qwen3-0.6B）→ 4 样例注入 → 三路小模型 + 4× TTA → 只把不确定 20% 交给 32B 重排。

**图 3：6th 提交记录**（topic 613150）——`../../intel/jigsaw-agile-community-rules/bodies/613150_img/02.PNG`

![submission](../../intel/jigsaw-agile-community-rules/bodies/613150_img/02.PNG)

*读图*：selected submission 截图（3-peer DML 0.93237/0.92781 的物证）。

## 7. 可迁移性评估

- **可直接迁移**：
  - **"规则/指令在测试时才出现"这类任务，必须做推理期适配**（TTT、在线蒸馏）。
  - 先确认公开榜是否无偏（官方说明/划分方式），再决定是否可用作验证。
  - 分层模型集成（强模型 + 快模型）。
- **需要前提**：
  - 需要长推理窗口（本场 12 小时）与 GPU 资源。
  - 需要 LLM 微调/蒸馏工具链。
- **不建议照搬**：
  - 无脑把公开榜当验证——本场成立是因为官方说明了随机划分。
  - 直接套用 ICR 等"公开榜不可信"比赛的策略。

## 8. 对新手的关键启示

1. **验证策略没有通用答案**：公开榜能不能用，取决于赛制（随机划分？时间外推？样本量？）。
2. **测试时训练是"新规则"任务的标配思路**。
3. **蒸馏与互学习比单模型微调更稳**，尤其在分布会变的场景。
4. 即使是 RAG + 重排序这类"非微调"路线，也能拿到不错的成绩——**先确认资源与时间预算再选路线**。

## 9. 出处

- 讨论区索引：`intel/jigsaw-agile-community-rules/topics.md`（120 条）
- 已收录正文（7 节）：
  - 规则公开（c-number，127 票）：https://www.kaggle.com/competitions/jigsaw-agile-community-rules/discussion/607941
  - 1st（Guanshuo Xu，118 票）：https://www.kaggle.com/competitions/jigsaw-agile-community-rules/discussion/613305
  - 6th DML（ducnh279，107 票）：https://www.kaggle.com/competitions/jigsaw-agile-community-rules/discussion/613150
  - 7th（ktr，40 票）：https://www.kaggle.com/competitions/jigsaw-agile-community-rules/discussion/613215
  - 120th RAG（Chris Deotte，40 票）：https://www.kaggle.com/competitions/jigsaw-agile-community-rules/discussion/613168
  - 12th（losingself，39 票）：https://www.kaggle.com/competitions/jigsaw-agile-community-rules/discussion/613096
  - 3rd（Sergio Papadakis，35 票）：https://www.kaggle.com/competitions/jigsaw-agile-community-rules/discussion/613324
- 未收录缺口（登记备查）：23 条 write-up 标记中的其余条目（含 2nd/4th/5th）
- 深读全文：`analysis/deep/jigsaw-agile-community-rules.md`
