# Playground Series S6E8（手机成瘾预测）轻量深读（Tier B）

> 赛事：Playground ｜ 主题 tabular（nomophobia/手机成瘾二分类）｜ 3531 队 ｜ 标准赛 ｜ 指标：ROC AUC
> 材料基础：`digests/playground-series-s6e8.md`（6 篇正文：1st 738592 / 2nd 738856 / 7th 738650 / 14th 739004 / 248th 738626 / 233rd 738691；63 条主题索引）+ 9 张归档图
> 轻读时间：2026-10（Tier B B13）

## 1. 一句话重述与数字账

用手机使用行为预测成瘾标签（AUC）。本场是**"agentic data science"的里程碑**：1st 用 Codex GPT-5.6 Sol 自主跑了 4 天建成 380 模型集成，再让 GPT-5.6 与 Claude Fable 5 互相对战/分享，产生一个**单独就夺冠的模型**（18 个月来首次单模夺冠）；随后又把 ChatGPT Pro 与 NVIDIA Inference Hub 的 ~150 个 LLM 组织成"分布式智能"继续提分。技术侧的主信号则是**合成生成器伪影**：exact-value / stringified 目标编码在 7th 手里单加 9 列 TE 就 +0.00191。

| 关键数字 | 值 | 来源 |
| --- | --- | --- |
| 1st（738592） | 四阶段：①单个 Codex GPT-5.6 Sol 自主运行 4 天 → **380 模型集成**、公榜前 10；②加入 Claude Fable 5 + 另一个 GPT-5.6 对阵，产出**单模 RealMLP CV 0.97070 / LB 0.97174**、单模 XGB CV 0.97020 / LB 0.97030；**单模直接夺冠（18 个月来首次）**；③ChatGPT Pro 并行"数据包"（每次 2 小时、返回 ZIP）产出新 FE；④NVIDIA Inference Hub 约 150 个 LLM（Nemotron 3 Ultra / DeepSeek V4 Pro / Kimi K3 / Gemini 3.7 Flash / Opus 5 / Qwen 3.8 27B 等）被评估后分配任务；图 2 显示最终 449 模型、公榜 0.97206 | 738592 |
| 2nd（738856） | 四周流程：周 1 用 "RAW + 单特征组 + 原数据（行/列/不用）" 批量造 100–200 模型（OOF 0.97013 / 公 0.97120 / 私 0.97096）→ 周 2 强化（0.97035/0.97134/0.97109）→ 周 3 手工 FE（`fake_daily = social+work+game` 及三个反推变量，0.97052/0.97149/0.97120）→ 周 4 "怎么都不涨"（0.97055/0.97148/**私 0.97123**）；用了 **200+ 份公开预测**（自述比自建模型更多样）；建议练旧赛（S5E8/S5E11/S6E3/S6E5）、别调公榜 | 738856 |
| 7th（738650） | 清洗后 **556 条预测流（206 本地 + 350 公开）**；六组正则化 Logistic Regression（C=0.01–3）求秩平均；严格 OOF 提交：OOF 0.97088 / 公 0.97127 / 私 **0.97095**，10/10 折提升、成对分层 bootstrap 95% CI [+0.000020, +0.000039]；数据洞察：**exact-value TE 9 列 +0.00191**，train+test 频次、成对统计、十进制/舍入伪影有效 | 738650 |
| 14th（739004） | **36 个自训 + 278 组共享 OOF**（来源与许可证全列）；协议：StratifiedKFold(5, seed 42) 生成一次即固定、不再重抽；**密封折嵌套 OOF**（锁一折、其余四折做选择、回评密封折），任何采纳需预设 delta 且 5/5 折为正；组合器 = 标准化秩+logit 的 L2 逻辑回归（C=0.03，允许负权重）；共享预测需过完整性检查（行数、有限性、重算 AUC 误差 <1e-5、哈希去重、折证据、泄漏审查）；**公榜从未用于任何决策**；自训单独私榜 0.97063 → 最终 0.97109 | 739004 |
| 233rd（738691） | 对抗验证 AUC 0.5654（分布稳定）；FE = 屏幕时间账目残差 + 行为比值 + **多级 TE 晶格**（类别/分箱的二三元组合，smooth=20，15 折）；177 成员 OOF 栈 + 精英锚流做百分位秩平均；私榜 0.97101；结论：树模型在 ~0.9713 饱和、顶部靠大规模 GPU NN（MLP/ResNet）拉开 | 738691 |
| 社区 | 简单 XGB/EDA starter CV 0.96（24 票）；生成缺失的"原始数据集"（21 票）；"入门先查什么"（18 票 / 22 评论）；"0.97101 的 NN 分从哪来"（14 票）；"stringified TE + 秩平均 0.9689+"（9 票）；"我没过拟合，是私榜不懂我的艺术"（16 票） | 索引 |

## 2. 逐方案对照矩阵

| 维度 | 1st | 2nd | 7th | 14th | 233rd |
| --- | --- | --- | --- | --- | --- |
| 主体 | Agent swarm（Codex/Fable/ChatGPT Pro/~150 LLM） | 人工 FE + 大池模型 | 556 条流 + 6×LR | 314 列（36 自训+278 共享） | 177 成员栈 + 锚流 |
| 关键 FE | agent 自主发现 | fake_daily 等反推比值 | **exact-value TE** | 秩+logit 标准化 | TE 晶格（二三元组合） |
| 验证纪律 | 公榜提交自动迭代 | OOF 为主、公榜仅校验 | 权重 9 折学/1 折评 | **密封折嵌套 + 5/5 折门槛** | 对抗验证 + 15 折 |
| 融合 | 单模 + 大集成 | 大池 | 6 LR 秩平均 | L2 LR（C=0.03） | 百分位秩平均 |
| 私榜 | 1st（单模夺冠） | 0.97123（2nd） | 0.97095 | 0.97109 | 0.97101 |

## 3. 共识、分歧与裁决

### 共识一：合成生成器伪影是核心信号（7th、233rd、社区帖；置信度高）

7th 的 fold-safe exact-value TE 9 列直接 +0.00191；233rd 的 TE 晶格；另有"stringified TE + 秩平均"帖。**裁决**：这类 Playground 先做"生成过程逆向"——找重复取值/字符串化/小数位/频次差异，再做建模。置信度：高。

### 共识二：公开 OOF 生态 + 严格准入 + 线性融合成为主流（2nd、7th、14th、233rd；置信度高）

2nd 用了 200+ 公开预测；7th 556 条流；14th 278 组共享 + 完整性检查与许可证清单；融合器全部是 LR/Ridge 或秩平均。**裁决**：社区共享 OOF 是当前 Playground 的一等资源，但必须做重算校验、去重与泄漏审查；融合用低自由度线性模型。置信度：高。

### 事件一：Agent 分布式智能夺冠（1st、2nd；置信度中高）

1st 的四阶段（单 agent → 双 agent 竞争 → ChatGPT Pro 并行 → ~150 LLM swarm）在公开记录中第一次把"多 agent 协作 + 多模型供应商"作为冠军方案；2nd 也承认"vibe coding 与 AI agents 是我要补的课"。**裁决**：2026 年起，顶级表格赛的竞争维度已包含"如何编排 agent 群体"，而不仅是模型与特征。置信度：中高（自述，含图）。

### 共识三：单模与集成都能登顶，但前提是 FE 与验证纪律（1st vs 2nd/7th/14th；置信度中高）

1st 的单模 RealMLP 直接夺冠（18 个月首次）；2nd/7th/14th 用大池融合分别拿 2/7/14。**裁决**：单模上限被 agent 化的 FE 显著抬高；集成仍是稳健保险。置信度：中高。

### 事件二：验证纪律被推到新高度（14th、7th、2nd；置信度中高）

14th 的密封折嵌套 OOF + 5/5 折门槛 + 公榜零决策；7th 的 9 折学权重/1 折评 + bootstrap CI；2nd 反复强调"别调公榜"。**裁决**：在分数饱和（0.970–0.972）的赛场上，验证协议本身就是核心竞争力。置信度：中高。

## 4. 证据分级

| 断言 | 等级 | 说明 |
| --- | --- | --- |
| 1st 的四阶段 agent 流程与单模夺冠 | 自述 + 4 张图 | 中高（无法独立复现） |
| 7th 的 556 流、TE +0.00191、bootstrap CI | 自述（含公式与流水线图） | 高 |
| 14th 的密封折协议与完整性检查 | 自述（极详细，含许可证清单） | 高 |
| 2nd 的四周分数轨迹与公开预测用量 | 自述 | 中高 |
| 233rd 的对抗验证/晶格/177 栈 | 自述 | 中高 |
| 社区生成器伪影帖 | 多帖 | 中 |

## 5. 悬案与缺口（登记）

- 1st 的 agent 编排成本（token/GPU/时间）未量化；其"ChatGPT Pro 发现的新 FE"未公开细节；
- 3rd–6th、8th–13th 方案未收录；
- 共享 OOF 的许可证合规（unknown 许可）为 14th 自述处理方式，未逐项核对；
- **图证缺口**：无（9 张图，本深读内嵌 3 张）。

## 6. 图表证据

![Agent 四阶段架构](../../intel/playground-series-s6e8/bodies/738592_img/01.png)

**图 1**（topic 738592，1st）：Phase 1 单 Codex GPT-5.6 Sol 自主 agent → Phase 2 GPT-5.6 与 Fable 5 竞争 + 共享知识库 → Phase 3 ChatGPT Pro 并行 → Phase 4 NVIDIA Inference Hub 的 LLM 群体。

![堆叠进度与模型数](../../intel/playground-series-s6e8/bodies/738592_img/02.png)

**图 2**（topic 738592，1st）：按提交日期的公榜分数与模型数——Phase 1 结束约 300 模型、公榜进入 Top10 线；后续阶段最终 449 模型、公榜 0.97206。

![556 条预测流的严格 OOF 流水线](../../intel/playground-series-s6e8/bodies/738650_img/01.png)

**图 3**（topic 738650，7th）：1 级预测池（206 本地 + 350 公开 → 556 清洗流）→ 秩归一化 → 9 折拟合/1 折评估 → 6 个 Logistic Regression → 秩平均 → 外层混合 → 严格 OOF 主提交（OOF 0.97088 / 公 0.97127 / 私 0.97095）。

## 7. 出处

- 1st Distributed Intelligence（127 票 / 78 评论）：https://www.kaggle.com/competitions/playground-series-s6e8/discussion/738592
- 2nd Place（47 票 / 13 评论）：https://www.kaggle.com/competitions/playground-series-s6e8/discussion/738856
- 7th "One Simple Stack"（14 票）：https://www.kaggle.com/competitions/playground-series-s6e8/discussion/738650
- 14th 278 共享 OOF + 密封折（10 票）：https://www.kaggle.com/competitions/playground-series-s6e8/discussion/739004
- 248th 秩对齐融合（3 票）：https://www.kaggle.com/competitions/playground-series-s6e8/discussion/738626
- 233rd（4 票）：https://www.kaggle.com/competitions/playground-series-s6e8/discussion/738691
- 简单 XGB/EDA starter（24 票）：https://www.kaggle.com/competitions/playground-series-s6e8/discussion/736409
- 生成缺失原始数据集（21 票）：https://www.kaggle.com/competitions/playground-series-s6e8/discussion/732428
- 0.97101 NN 分数溯源（14 票）：https://www.kaggle.com/competitions/playground-series-s6e8/discussion/735404
- stringified TE + 秩平均（9 票）：https://www.kaggle.com/competitions/playground-series-s6e8/discussion/734063
