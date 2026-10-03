# Playbook：NLP / LLM

> 版本：v1.0（定稿）｜ 依据：`notes/nlp/` 全部 35 篇摘要（该主题 35/35 已完成）
> 覆盖：判别/抽取（Jigsaw×2、Feedback×3、NBME、PII、Patent、CHAIi、AI4Code、EEDI、CommonLit、Writing、Essay 2.0、LLM Detect）、
> 生成式（Deep Past、Drawing、Prompt Recovery）、推理与 RAG（Science Exam、AIMO 1/2/3、ARC 2024/25、Nemotron、Konwinski）、
> agent/交互（20 Questions、Agent Security）、LLM 评测/偏好（LMSYS、WSDM、You Can't Please Them All）、社区（Gemma Tuning）

## 1. 主题地图：五条赛道，先判断你在哪类

| 赛道 | 代表比赛 | 胜负手 | 算力门槛 |
| --- | --- | --- | --- |
| **判别/抽取** | Jigsaw、Feedback 系列、NBME、PII、Patent | 防泄漏验证 + 数据质量 | 单卡可入场 |
| **生成式** | Deep Past、Drawing、Prompt Recovery | 语料/输出工程 + 指标拆解 | 单卡到多卡 |
| **RAG / 推理问答** | Science Exam、AIMO 1/2/3、ARC、Nemotron | 检索质量 / 数据构造 / 推理预算 | 多卡到 48h TTT |
| **agent / 交互** | 20 Questions、Agent Security、Konwinski | 模块化 + 规则与模型的边界 | 中等，偏工程 |
| **LLM 评测/偏好** | LMSYS、WSDM、You Can't Please Them All | 校准 + 逆向黑盒评分器 | 多卡微调 |

## 2. 跨主题的第一性结论（全部 35 场反复验证）

1. **数据工程 > 模型结构**：Deep Past（冠军原话"Data Quality Dictates Everything"，原版 ByT5 零结构改动）、LLM Detect（CV 失效时扩数据多样性才是出路）、AIMO2（筛选高质量推理轨迹 > 模型规模）。"挑数据"的收益稳定高于"改网络"。
2. **按来源分组验证是文本任务的生命线**：Jigsaw Toxic（Union-Find 防文本泄漏）、CommonLit（训练 4 题目 vs 测试 122 题目）、Patent（组结构泄漏）、MAP（近重复必须同折）。随机 K 折在文本赛里几乎总虚高。
3. **"信 CV 还是信 LB"要论证，不能站队**：CHAIi 是少见的 LB 可信案例；LLM Detect 是 CV 完美但 LB 崩掉的经典反例；Nemotron 有选手自省"无本地验证、只看榜"的教训。先量化 CV-LB 相关性再分配预算（Feedback ELL 的做法）。
4. **指标先拆解再优化**：多分项加权（Drawing、Feedback ELL 六维、CommonLit 两列）先弄清各分项口径；排序指标按 k 截断（EEDI MAP@25）；对数损失要校准概率（LMSYS、Feedback Effectiveness）。
5. **分布迁移是 2024 后的主旋律**：隐藏测试来自不同模型（LLM Detect）、测试期出现新规则（Jigsaw Agile 的 TTT/在线蒸馏）、测试集只有单一实体（ARC 的 per-task 适应）。"推理期适配"从加分项变成必选项。

## 3. 方法工具箱

### 3.1 判别式：分类 / 跨度 / 排序

- **基线与集成**：DeBERTa 系微调 + 多池化/多长度/多基座 → **爬山法**选权重（Feedback ELL）；小样本多目标回归的标准配方。
- **跨度任务**：滑窗 + 重叠合并；边界与最小长度后处理（Feedback 2021、NBME）；跨领域借技术——**Weighted Box Fusion 从检测迁移到 NLP**（Feedback 2021）。
- **半监督**：MLM 中间训练 + 伪标签（NBME：无标注 ≫ 有标注时首选）；合成数据补大类空间（EEDI 用 LLM 造缺失类样本）。
- **大标签空间改检索/重排**：EEDI 2500 类不要当分类头，做"语义检索 + 重排"。
- **排序任务当"成对关系 + 重建"**：AI4Code 的顺序预测范式可迁移到任意排序问题；评估注意局部顺序误差。
- **分组对比**：同一组的候选一起输入做批量比较（Patent），信息量大于逐对判断。

### 3.2 生成式：翻译 / SVG / 改写

- **低资源生成的第一投入是语料工程**：文档级平行语料 → LLM 切句对齐 → 人工抽检 → 继续预训练/微调 → 伪标签（Deep Past，含 OCR 文献挖掘）。
- **多生成 + 指标筛选**；可微渲染/可微优化用于结构化输出（Drawing 的 SVG）。
- **先量化简单基线**：LLM Prompt Recovery 里均值/模板基线意外地强——不先量化它就不知道投入产出比。
- **指标敏感性检查**：句向量类指标对长度与特殊 token 敏感，必须实验验证。

### 3.3 RAG 与推理

- **RAG：检索侧投入回报高于模型侧**；多检索管线集成 > 多模型集成；限时环境用加速工具换集成规模（Science Exam）。
- **推理训练通用配方**：写确定性求解器 → 生成"逐步可达"的推理链 → 筛选 → SFT/偏好优化（AIMO2、Nemotron）；ORM + 加权多数投票可训练期免改（AIMO1）。
- **推理工程派**（不训练）：多路并行 + 熵加权自洽投票 + 验证辅助 + 显存/缓存优化；提示词里显式约束（禁浮点、限工具）就是提分手段（AIMO3）。
- **TTT（测试时训练）**：测试分布与训练差异大时，在推理窗口内继续学习——ARC 2024/2025 与 Jigsaw Agile 独立得到同一结论。

### 3.4 agent / 交互 / 黑盒评分

- **信息增益驱动动作**：20 Questions 的提问策略 = 主动学习/诊断系统的通用打法；确定性规则处理规则部分、模型处理模糊部分，松耦合模块 + 测试用例控制风险。
- **黑盒评分器先逆向**：You Can't Please Them All 与 Agent Security 都证明"先建立本地快速评分回路"是第一步；能测的测准、测不到的用对冲保险（Agent Security 提交互补方案）。
- **答错重罚场景用 abstain**（Konwinski）；"定位 → 验证 → 修改 → 再验证"的 agent 流水线。
- **警惕指标套利**：Drawing 的 OCR 诱饵、Prompt Recovery 的对抗后缀与分词器缺陷——换指标即失效，不算技术积累。

### 3.5 LLM 微调与偏好建模

- **LoRA/QLoRA 是平民化标准**（LMSYS 16th 的 7B→72B 成长路径；MAP 的量化 + LoRA 合并控推理成本）。
- **长文本截断保首尾**（WSDM；LMSYS 同源结论）；位置偏差（A/B 顺序）与噪声票必须处理；概率输出要校准。
- **用领域奖励模型初始化再微调**（WSDM）；复用往届公开框架是最便宜的起点。

## 4. 验证清单（NLP 专用）

- 文本/实体级泄漏检查（TF-IDF 或嵌入 + Union-Find 分组）。
- 按"来源"分组：题目、作者、主题、生成模型、数据集批次。
- 显式量化 CV-LB 相关性，写下"信谁"的判据。
- 概率校准与阈值选择（QWK、logloss、MAP@k）。
- 指标边界测试：长度敏感性、特殊 token、截断位置。
- 隐藏测试压力测试：换一版生成模型/换一批题目，分数掉多少？

## 5. 常见坑

| 坑 | 证据 |
| --- | --- |
| 随机切分导致文本/题目泄漏 | Jigsaw Toxic、CommonLit、Patent、MAP |
| 训练集多来源拼接被忽视 | Essay Scoring 2.0（分数双峰是信号） |
| 只调模型不调检索 | Science Exam 冠军结论 |
| 用未筛选大规模语料训练 | AIMO2、Nemotron |
| CV 完美就以为稳了 | LLM Detect（LB 崩）、CHAIi（反向案例） |
| 把指标套利当技术 | Prompt Recovery、Drawing |
| 无本地验证只看榜 | Nemotron 自省帖 |
| 同一份 OOF 上调参选权重 | Feedback ELL 2nd 复盘 |

## 6. 年度演进

- **2021–2022（微调时代）**：DeBERTa 系 + 集成 + 后处理；Jigsaw Toxic、Feedback 三连、NBME、CHAIi、Patent、AI4Code。主题是"防泄漏 + 跨度/排序工程"。
- **2023（RAG 与生成抬头）**：Science Exam 确立"检索侧 > 模型侧"；Deep Past 走通语料工程；CommonLit/Linking Writing 强调来源验证；社区微调活动出现。
- **2024（LLM 平民化 + 迁移难题）**：QLoRA 普及（LMSYS）；LLM Detect 的"来源不可知"与 CommonLit 的"题目覆盖差"成为核心难度；AIMO1/ARC 首秀拉开推理赛序幕；Essay 2.0、PII、EEDI、MAP、20Q、Prompt Recovery 全面开花。
- **2025–2026（双路线分化 + agent 化）**：**训练派**（AIMO2、Nemotron：求解器→推理链→SFT）与**推理工程派**（AIMO3、ARC、Jigsaw Agile：TTT、自洽投票、预算管理）分庭抗礼；agent 与安全成为独立赛道（20Q、Agent Security、Konwinski）；黑盒 LLM 评委类比赛（Pleasing、WSDM）出现。

## 7. 新手学习路径（按顺序）

1. **验证与防泄漏**：`jigsaw-toxic-severity-rating` → `commonlit-evaluate-student-summaries`。
2. **跨度/抽取基本功**：`feedback-prize-2021`（后处理与融合）→ `nbme-score-clinical-patient-notes`（半监督）。
3. **排序与检索思维**：`us-patent-phrase-to-phrase-matching` → `eedi-mining-misconceptions-in-mathematics`。
4. **RAG 入门**：`kaggle-llm-science-exam`（只做检索也能学到大半）。
5. **推理赛**：`ai-mathematical-olympiad-prize`（ORM + 投票）→ `nvidia-nemotron-model-reasoning-challenge`（求解器 → 推理链）。
6. **LLM 微调**：`lmsys-chatbot-arena` 或 `wsdm-cup-multilingual-chatbot-arena`（LoRA/QLoRA 实战）。
7. **agent 与实战视野**：`llm-20-questions` → `konwinski-prize`、`ai-agent-security-multi-step-tool-attacks`。

> 算力提示：第 1–4 步单卡可完成；第 5 步视方案需要多卡/长时推理；第 7 步更吃工程能力而非算力。

## 8. v2 增补（Tier B 204 场，2026-10）

1. **提示词工程评审赛**：最小可靠范式 = system prompt + 多组 input/output 示例；让输出可机读（JSON + rubric）能同时降低评审成本、提高复用价值（makersuite 457016）。
2. **LLM 引用必须核验**：模型给出的来源/文献会幻觉（openai-to-z 584626）；把 LLM 输出当不可信输入，URL/事实/语义逐条核对（L132）。
3. **多语言模型适配**：Gemma 2 官方路径 = 参考汇编 → LoRA/QLoRA/TPU 指南 → 发布 Kaggle Models + 公开 notebook；机会在低资源语言与文化语境（gemma-language-tuning）。
4. **大规模图文检索**：图像走 URL 的数据集先做 I/O（feather/parquet/datatable/LMDB/HDF5 + 并发下载）；直接复用 Shopee 1st–161st 方案骨架（wikipedia-image-caption）。
5. **安全红队**：CoT 可伪造、工具/通道不一致、`reasoning_effort=low` 可复现而 `high` 拒绝；危害按"增量"（超出基础搜索多少）评估（L119，gpt-oss）。
6. **Agent 元竞赛**：提交的是 Agent Config（Google ADK）；60min/$2 预算下先本地 validate schema，再按"定向→CV→快基线锚点→迭代"工作流（L122/L123，autonomous-agent）。
7. **评测设计赛**：好 benchmark 要"超越记忆"且能判别；社区投票入分（15%）会引入曝光/互赏偏差（kaggle-measuring-agi）。
8. **长上下文应用**：赢家集中在长视频/代码库/大规模文本处理；注意模型挂载（Save&Run All）与配额限流（L123，gemini-long-context）。

## 9. 检查清单（v2，可打印）

- [ ] 任务形态判定：理解/生成/检索/安全/Agent，方法论完全不同（L119）
- [ ] 输出可机读（JSON/结构化）+ 评分口径写进 prompt（makersuite）
- [ ] few-shot 稳定性测试：同一 prompt 多次运行方差可接受
- [ ] LLM 引用/来源逐条核验（L132/F9）
- [ ] 大数据 I/O：URL→feather/parquet/LMDB + 并发下载（wikipedia）
- [ ] 相似赛方案总汇盘点（Shopee 1st–161st 等）（L113）
- [ ] Agent 赛：schema 本地校验、工具兼容、预算与超时（L122/L123）
- [ ] 安全赛：CoT 伪造/工具通道/`reasoning_effort` 三面都测（L119）
- [ ] 评测设计赛：判别力 + 社区投票偏差（kaggle-measuring-agi）
- [ ] 多语言：域内预训练/低资源评测，先测 base 能力再适配
- [ ] 提交字数/格式；模型挂载方式（Save&Run All）已演练（L123）
