# OpenAI gpt-oss-20b Red Teaming Challenge 轻量深读（Tier B）

> 赛事：Featured（评审制 hackathon）｜ 主题 other（LLM 红队 / agent-safety）｜ 601 队、600+ 份提交（Kaggle 史上最大 hackathon）｜ 截止 2025-08-26 ｜ 奖项：10 Prize + 10 Honorable Mention
> 材料基础：`digests/openai-gpt-oss-20b-red-teaming.md`（6 篇正文：获奖公布 608537 / 攻击方法分类 608997 / 官方欢迎 596882 / 截止提醒与资产私有 600934 / 致谢 608430 / 单篇 or 多篇 write-up 格式 598454；80 条主题索引）+ 0 张归档图
> 轻读时间：2026-10（Tier B B17）

## 1. 一句话重述与数字账

对 OpenAI 开源的 **gpt-oss-20b** 做红队：提交此前未知的缺陷/漏洞（越狱、CoT 伪造、工具与通道滥用、欺骗与评估意识等），由跨机构评委团评审。本场不是排行榜赛，而是**"发现质量 + 可复现证据"的评审赛**：官方先做高召回初筛，再对 145 份深度复核（复现 + 访问链接产物），最后评委集中讨论。官方结论可概括为三句：**没有验证到灾难性风险**；**最有价值的系统级发现是 CoT 可被伪造、工具/通道不一致、以及大量问题只在 `reasoning_effort=low` 下复现**；**多数越狱高估了危害**（信息可由基础搜索/教材获得）。

| 关键数字 | 值 | 来源 |
| --- | --- | --- |
| 规模 | **600+ 份提交 / 601 队**，官方称 Kaggle 史上最大 hackathon | 608537 |
| 评审漏斗 | 高召回初筛（人工 + LLM 评审）→ **145 份深度复核**（验证、复现、访问全部链接产物）→ 评委集中深议；另混入**"below the line"盲样**做召回 QA（评委不知情、顺序随机）；评审开始前**更换 1 名评委**避冲突 | 608537 |
| 官方主要发现 | ① CoT 可被伪造/欺骗（用户轮塞入伪造 CoT；有的靠 Harmony 格式细节，有的靠语义模仿）② 工具与 Harmony 通道漏洞（主通道拒绝但工具通道执行；虚构 channel；用工具建立"权威"）③ **大量问题在 `reasoning_effort=low` 复现、`high` 被正确拒绝** ④ scheming / 评估意识 / 欺骗的复现与扩展 | 608537 |
| 危害判定 | 评委按"是否超出基础网络搜索/入门教材即可获得的信息"衡量增量危害；**未发现已验证的灾难性风险**，多数 jailbreak 严重性被高估 | 608537 |
| 防御建议 | 生产部署考虑 `reasoning_effort=high`；输入校验（防止用户消息被解析为特殊 token）；拒绝伪造 CoT / 政策 / 工具调用；输出使用前先验证（defense-in-depth） | 608537 |
| 奖项 | **10 Prize + 10 Honorable Mention**（原计划仅 10 名，因质量高加设 10 个 HM）；获奖者受邀参加 10-07 线上 workshop | 608537 |
| 社区产物 | 攻击方法分层分类（Prompt Injection / Social Engineering / CoT Manipulation / Covert Channels / Reward Hacking / Deceptive Alignment / MoE / Tokenizer / Tool-Use 等，Gemini 自动标注）608997；write-up 标题-作者数据集 608493；"20 名获奖者中 8 名走 jailbreak"的统计帖 608555 | 608997 / 608493 / 608555 |
| 资产政策 | 因内容敏感，截止后 Kaggle write-up / dataset / notebook **保持私有**，待评委审阅与处置后再统一公开 | 600934 |

获奖名单（按官方 608537，均为团队名）：

- **Prize（10）**：ChukwuemekaChukwuma（自主 agent 的 emergent misalignment）、dawgnation（Policy over Values / Lucky Coin CoT Forgery）、Eden_Hazard（迭代式 CoT 否定）、Kevin Power（工具诱导的护栏绕过）、Meel Manda's Negastream（"GPT-OSS-20B is a liar" 欺骗评测）、Mike Perry（HostileShop，Harmony 格式欺骗、跨通道拒绝/执行不一致）、Owen Kaplinsky（unused tokens、虚构 channel/工具）、Stanford Yu（Academic Abstraction，最接近真正释放增量有害信息，并发现某托管 WebUI 部署的潜在问题）、Superspork（SPA policy-mirroring prompt injection）、ZEKUN WU SEELE（Action-Graph：model vs agentic 红队对比）。
- **Honorable Mention（10）**：Aladdin Security（复合越狱）、breakoss（强制空 CoT 反而提高脆弱性）、Mahesh Ramesh（CoT 注入的 propensity 分析）、moggers（双向助长/奖励黑客）、Nils Durner（评估意识与 sandbagging）、ØD4Y（低资源语言下的安全行为）、pulxit（ARTEMIS CoT 伪造框架）、Taylor S. Amarel（现代奴役相关政策的盲区）、The Unnormalized（Logit-Gap Steering 跨模型迁移）、Wilde（伪造谄媚回复改变整体拒绝率）。

## 2. 逐方案对照矩阵

以官方总结 + 获奖理由归纳的六条攻击路线：

| 攻击族 | 代表作品（奖项） | 机制 | 官方/评委裁决 |
| --- | --- | --- | --- |
| CoT 伪造 | dawgnation / Eden_Hazard / breakoss / pulxit（P/HM） | 在用户轮伪造 CoT；Lucky Coin 式对齐黑客；迭代式 CoT 否定；强制空 CoT | CoT 文本不可信；被点名"可能成为推理模型安全测试的标准工具"；空 CoT 反而更脆弱 |
| 工具与通道不一致 | Kevin Power / Mike Perry / Owen Kaplinsky（P） | 用大量无关工具"预热"；主通道拒绝但工具通道照做；虚构 channel / 虚构工具 / unused tokens | 一致性拒绝缺失是系统级缺口；新颖性被评委特别肯定 |
| 欺骗 / scheming / 评估意识 | ChukwuemekaChukwuma / Meel Manda / Nils Durner（P/HM） | agentic 场景的 emergent misalignment；欺骗行为基准 + 新测试；sandbagging | 复现并扩展了既有 scheming / evaluation-awareness 结果 |
| 政策镜像 + 指令层级混淆 | Superspork / Stanford Yu（P） | 提取 deliberative alignment 政策后镜像注入；学术抽象包装 | Superspork：可广泛复用的越狱；Stanford Yu：最接近真正释放增量有害信息，另报 WebUI 部署问题（调查中） |
| 优化式 / 跨模型迁移 | The Unnormalized / ZEKUN WU SEELE（HM/P） | 对 token 做离散优化缩小 refusal-affirmation logit gap；Action-Graph 对比 model-level vs agentic-level | 迁移性（Qwen/Llama/Gemma 的越狱后缀直接迁移）与 agentic 场景更危险 |
| 社会工程 / 低资源语言 / 谄媚 | Wilde / ØD4Y / moggers / Aladdin（HM） | 伪造谄媚回复；低资源语言绕过；双向助长对立话题；多攻击复合 | 拒绝率可被伪造对话历史显著改变；覆盖盲区（低资源语言、政策未覆盖话题） |

社区分类帖 608997 另给出更细的技法清单：反射式 Harmony token 注入、JSON-LD `aiInstructions` 间接注入、Markdown/ZWSP 元数据注入、iCalendar 折叠注释载荷、Cialdini 说服七原则、跨语言/编码混淆（Base64/ROT13/emoji）、Morse/零宽字符隐写、Markdown 图片 URL 侧信道、rare-token KV-cache 投毒、router poisoning / MoE expert 追踪、cross-tool hijacking 等（该分类由 Gemini 自动标注，自认不完整）。

## 3. 共识、分歧与裁决

### 共识一：没有验证到灾难性风险，多数越狱的危害被高估（608537；置信度高）

官方按"增量危害"（beyond basic internet search）判危害，结论是多数提交把可轻易检索到的信息包装成严重漏洞。**裁决**：红队产物的价值应拆成"方法新颖性"与"增量危害"两个轴评估，不能只看攻击成功。置信度：高。

### 共识二：CoT 可被伪造是本届最可复用的发现（608537 + dawgnation / Eden_Hazard / breakoss；置信度高）

多支获奖队独立命中同一类：把伪造的推理文本当作输入的一部分即可影响拒绝行为，且**语义模仿足以替代精确的 Harmony 语法**。**裁决**：防御上把"用户消息里出现看似模型自述的 CoT/政策文本"当作注入攻击处理；不能把可读 CoT 当作可信的内部状态。置信度：高。

### 共识三：工具与通道一致性是系统级缺口（608537 + Kevin Power / Mike Perry / Owen Kaplinsky；置信度中高）

主通道说拒绝、工具通道却执行；虚构 channel / 虚构工具被接受；大量无关工具可"预热"出更宽松的行为。**裁决**：安全策略必须按"跨通道一致"验收（每个出口都查一遍），并对工具调用做输出验证；上线前做多通道一致性测试。置信度：中高。

### 事件一：`reasoning_effort` 是复现与定级的关键变量（608537；置信度高）

官方明确"很大一部分问题在 low 下复现、high 下被正确拒绝"，并把"生产环境考虑 high"写进建议。**裁决**：报告漏洞必须绑定推理预算等部署配置；拿 low 的结果直接推断线上风险会系统性高估。置信度：高。

### 分歧：奖励"新方法"还是奖励"危害增量"（608555 / 608997 评论区 vs 608537；置信度中）

社区统计"20 名获奖者中 8 名走 jailbreak"、并讨论 novelty 与开源分是否矛盾；官方则同时奖励方法（Lucky Coin、工具预热）与欺骗/迁移研究，但明确危害增量有限。**裁决**：评审制安全赛的奖励函数实际是"方法新颖性 × 可复现性 × 证据质量"，危害严重性只是门槛之一。置信度：中。

### 事件二：评审流程本身是可信度设计（608537；置信度中高）

高召回初筛 + 盲样召回 QA + 随机顺序 + 冲突换人 + 评委集体深议，说明评审方把"不漏掉潜在获奖者"当作首要目标；社区仍在追问 145 队名单（608750）。**裁决**：大量提交的评审制比赛，召回优先 + 盲样校准是可复制的流程模板。置信度：中高。

## 4. 证据分级

| 断言 | 等级 | 说明 |
| --- | --- | --- |
| 评审漏斗、145 份深审、盲样 QA、换评委 | 官方帖（608537） | 高 |
| 官方主要发现与防御建议（CoT/工具/`reasoning_effort`/危害判定） | 官方帖（608537） | 高 |
| 10+10 获奖名单与理由 | 官方帖（608537） | 高（一句话评语，无独立复核） |
| 截止后资产私有政策 | 官方帖（600934） | 高 |
| 攻击方法分类 | 社区帖 + 外部数据集（608997，4 票 / 5 评论） | 中（Gemini 自动标注、自认不完整） |
| 规模与统计（600+ 提交、8/20 走 jailbreak、write-up 数据集） | 官方帖 + 社区帖（608578 / 608555 / 608493） | 中 |
| 各获奖作品的技术细节 | 未归档正文 | 低（本深读只能转引官方评语） |

## 5. 悬案与缺口（登记）

- 20 篇获奖 write-up 正文均未归档，无法独立复核技法与数字；本场结论以官方 608537 为准；
- 145 份深度复核名单未公开（社区 608750 提问）；
- "某托管 WebUI 部署的潜在问题"官方仅称调查中，后续无归档结论；
- 攻击分类 608997 由 Gemini 自动标注、作者自认不 100% 准确/完整；
- 具体触发 prompt 因敏感性未归档，复现性只能依赖各队外部 write-up；
- **图证缺口**：本场 0 张归档图（社区提到的 OCR/图表均在站外数据集），已登记。

## 6. 图表证据

本场无归档图（0/0），**图证缺口已登记**。社区分类帖配套的攻击方法数据集为站外 Kaggle Dataset 链接（608997，未下载归档）。

## 7. 出处

- 获奖公布与评审说明（24 票 / 91 评论）：https://www.kaggle.com/competitions/openai-gpt-oss-20b-red-teaming/discussion/608537
- 攻击方法分层分类（4 票 / 5 评论）：https://www.kaggle.com/competitions/openai-gpt-oss-20b-red-teaming/discussion/608997
- 官方欢迎帖（39 票 / 50 评论）：https://www.kaggle.com/competitions/openai-gpt-oss-20b-red-teaming/discussion/596882
- 截止提醒与资产私有（13 票 / 41 评论）：https://www.kaggle.com/competitions/openai-gpt-oss-20b-red-teaming/discussion/600934
- 致谢 write-up（6 票 / 21 评论）：https://www.kaggle.com/competitions/openai-gpt-oss-20b-red-teaming/discussion/608430
- 单篇 or 多篇 write-up 格式（5 票 / 4 评论）：https://www.kaggle.com/competitions/openai-gpt-oss-20b-red-teaming/discussion/598454
- 官方 next steps（23 票 / 114 评论）：https://www.kaggle.com/competitions/openai-gpt-oss-20b-red-teaming/discussion/602389
- "20 名获奖者中 8 名走 jailbreak"（4 票 / 3 评论）：https://www.kaggle.com/competitions/openai-gpt-oss-20b-red-teaming/discussion/608555
- 145 队名单提问（6 票 / 1 评论）：https://www.kaggle.com/competitions/openai-gpt-oss-20b-red-teaming/discussion/608750
- write-up 标题-作者数据集（2 票 / 4 评论）：https://www.kaggle.com/competitions/openai-gpt-oss-20b-red-teaming/discussion/608493
