# OpenAI gpt-oss-20b Red Teaming Challenge（精简）

> 主题：other ｜ 子类：hackathon ｜ 类别：Featured ｜ 截止：2025-08-26 ｜ 队伍数：601 ｜ 指标：评审制
> 出处：`intel/openai-gpt-oss-20b-red-teaming/`（80 条主题索引 + 6 篇正文）

## 任务

对 OpenAI 开源的 gpt-oss-20b 做**红队测试**：发现并提交此前未知的缺陷/漏洞（对抗性提示、越狱、能力边界等），由 OpenAI 评审。

## 关键要点

- 官方定位：这是 OpenAI 对开源模型安全承诺的一部分（**安全评测的公开化**）。
- 评审强调"覆盖话题广、技术手段多样"——说明评审看重**发现的多样性与新颖性**，而非单一指标。
- 与 `ai-agent-security-multi-step-tool-attacks` 对照：**红队/安全评测已成为独立赛道**，且从"攻击 agent"扩展到"攻击开源模型"。

## 可迁移要点

- 安全评测类比赛：**多样性 + 可复现的证据**比单点强度更重要（要能清楚复现触发路径）。
- 值得作为了解 LLM 安全边界的入口。

## 轻读结论（2026-10 补）

- **评审制红队赛**：601 队 / 600+ 份提交（Kaggle 史上最大 hackathon）；高召回初筛（人工 + LLM）→ **145 份深度复核**（验证/复现/查链接）→ 评委集中讨论，并混入盲样做召回 QA、为避冲突换过 1 名评委；最终 **10 Prize + 10 Honorable Mention**（608537）。
- **官方三条主线**：① CoT 可被伪造/欺骗（用户轮塞伪造 CoT；靠 Harmony 格式细节或语义模仿均可）；② 工具与通道漏洞（主通道拒绝但工具通道执行、虚构 channel、用工具建立"权威"）；③ **大量问题只在 `reasoning_effort=low` 复现、`high` 正确拒绝**；另有 scheming / 评估意识 / 欺骗的复现扩展（608537）。
- **危害判定口径**：未发现已验证的灾难性风险；多数 jailbreak 高估危害（信息可由基础网络搜索/入门教材获得）。防御建议：输入校验（防用户消息被当特殊 token）、拒绝伪造 CoT/政策/工具调用、输出验证，生产可考虑 `reasoning_effort=high`（608537）。
- **可复用方法**：Lucky Coin 式 CoT 伪造（dawgnation）、迭代 CoT 否定（Eden_Hazard）、工具预热（Kevin Power）、跨通道不一致（Mike Perry）、虚构 channel/工具（Owen Kaplinsky）、policy mirroring（Superspork）、Logit-Gap 跨模型迁移（The Unnormalized）、伪造谄媚回复改变拒绝率（Wilde）；community 分类帖（608997）整理了 Prompt Injection / 社会工程 / CoT 操纵 / 隐蔽通道 / Reward Hacking / Deceptive Alignment / MoE / Tokenizer / 工具滥用九大类。

## 图表证据

本场 0 张归档图（0/0），**图证缺口已登记**；社区配套攻击分类数据集为站外链接（608997），未下载归档。

## 出处

- 讨论区索引：`intel/openai-gpt-oss-20b-red-teaming/topics.md`
- 获奖公布与评审说明（608537）：https://www.kaggle.com/competitions/openai-gpt-oss-20b-red-teaming/discussion/608537
- 攻击方法分层分类（608997）：https://www.kaggle.com/competitions/openai-gpt-oss-20b-red-teaming/discussion/608997
- 官方欢迎（596882）：https://www.kaggle.com/competitions/openai-gpt-oss-20b-red-teaming/discussion/596882
- 截止提醒与资产私有（600934）：https://www.kaggle.com/competitions/openai-gpt-oss-20b-red-teaming/discussion/600934
- 官方 next steps（602389）：https://www.kaggle.com/competitions/openai-gpt-oss-20b-red-teaming/discussion/602389
