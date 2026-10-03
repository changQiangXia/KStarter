# Google Tunix Hackathon（精简）

> 主题：other ｜ 子类：hackathon ｜ 类别：Featured ｜ 截止：2026-01-12 ｜ 队伍数：319 ｜ 指标：评审制
> 出处：`intel/google-tunix-hackathon/`（80 条主题索引 + 6 篇正文）

## 任务

用 Google 的 JAX 原生 LLM 后训练库 **Tunix** 教模型推理（微调/后训练实践型黑客松），评审制。已从 nlp 归入 `other/hackathon`。

## 关键要点

- 官方提供**统一的 notebook 提交模板与 FAQ 帖**——评审制比赛中，格式合规是第一步。
- 主题标签包含 `tpu`、`reinforcement learning`、`text generation`：这类比赛的价值在于**上手新的训练框架与硬件栈**（JAX/TPU 生态）。
- 参赛量不大（319 队），适合作为"学习新工具链"的练手场。

## 可迁移要点

- **新框架类黑客松的收益在技能而非名次**：Tunix/JAX/TPU 的经验可直接迁移到推理与后训练工作。
- 提交前先读模板与 FAQ，避免格式性失分。

## 轻读结论（2026-10 补）

**一句话**：用 Tunix（JAX 原生后训练库）在 Kaggle TPU 上后训练 Gemma2 2B / Gemma3 1B 的评审制 hackathon：评测 = **单会话 45 分**（官方 API、9h 单会话、评委重跑复现）+ **自由模式 +15 分**（任意方法，但须交出可被 Tunix 加载的 Kaggle 模型 ID）；真正的第一约束是 **TPU 配额与排队**（v5e-8、9h/会话、20h/周、排队 6+ 小时，社区请求延期/提额）。

- 规则（651560）：不提供数据、自备且须公开复现；评测集私有、数学/编码权重降低；人工评委看 notebook+视频。
- 时间线（670878）：322 份提交、需逐份复现，预计 3 月公布；随后获奖名单（691572）。
- 技术讨论：GRPO 奖励设计、SFT vs RL、多会话加成澄清、TPU 报错（abstracted_axes、cache 1536>1024）等。

**裁决**：新硬件栈 hackathon 先解决算力调度与端到端复现；选题朝通用能力与领域任务；按数月周期等待评审。

**悬案**：获奖方案细节与自由模式分布未收录；本场 0 图。

## 图表证据

无可用图证（本场归档 0 图，图证缺口已登记）。

## 出处

- 讨论区索引：`intel/google-tunix-hackathon/topics.md`
- 提交模板与 FAQ：见该比赛讨论区 "[Important] submission template and FAQs"
