# BirdCLEF 2026

> 主题：audio ｜ 子类：— ｜ 领域：生物声学 ｜ 类别：Research
> 截止：2026-06-03 ｜ 队伍数：4094 ｜ 机制：代码赛 ｜ 指标：物种识别（mAP 类）
> 数据来源：`intel/birdclef-2026/`（80 条主题索引 + 6 篇 write-up 正文）

## 1. 任务与数据

- 预测目标：由野外录音（soundscape）识别鸟种（多标签、类别极多）。
- 数据形态：长录音 + 弱标签（只有"这段里出现过某鸟种"）+ 少量强标注；**类别极度不平衡**。
- 构造陷阱：
  - 弱标签下的时间定位困难（需要切窗 + 多实例学习）；
  - 训练与测试可能来自不同地域/录音设备；
  - 主办方本届**首次引入独立验证集**（1st 在致谢里专门提到 "Validation!!"）——说明此前 BirdCLEF 长期缺少可靠验证。

## 2. 方案谱系

| 方案 | 名次 | 关键点 |
| --- | --- | --- |
| **Noisy Student 半监督 + 蒸馏** | 1st | 用未标注数据自训练（Noisy Student）再蒸馏；作者提到"每天都有新的公开 notebook 出现，且常常过拟合" |
| 多样集成 + 伪标签 + 分类群专家（taxon specialist） | 2nd | 针对鸟类分类学结构做专家模型 |
| 简单模型 | 10th | 简单方案也能进前十 |
| 不用 Perch（预训练模型）的方案 | 11th | 刻意不依赖外部预训练模型 |
| **纯 Claude-Code 自动化方案（后被取消资格）** | 101st | 用 Claude Code 构建**全自动竞赛求解器**（附 token 消耗与工作流图），人工每天只花 1-2 小时看报告；但最终被移除出比赛 |

## 3. 关键技巧

- **半监督 + 伪标签是弱标签音频任务的主力**（Noisy Student、自训练、蒸馏）。
- **分类学先验**：按属/科构建专家模型（taxon specialist）。
- **预训练模型的取舍**：是否使用 Perch 等生物声学预训练模型是重要决策（11th 明确选了"不用"）。
- **自动化 agent 的边界**：101st 的自动求解器展示了 LLM agent 端到端跑竞赛的可行性，但**被取消资格**——说明赛制对自动化提交/使用有明确限制，需先读规则。

## 4. 可迁移性评估

- **可直接迁移**：
  - 弱标签 → **切窗 + 多实例 + 伪标签**的范式（音频、视频、医学影像通用）；
  - 按类别层级（分类学）构建专家模型；
  - 预训练模型的使用要有明确取舍理由。
- 需要前提：音频处理（频谱图/特征）与大量未标注数据。
- 不建议照搬：全自动参赛（可能违反规则，本场已有先例）。

## 5. 对新手的关键启示

1. **弱标签任务的核心是"伪标签 + 时间定位"**。
2. **类别层级结构（分类学）是免费先验**。
3. **全自动 agent 参赛有规则风险**（101st 被取消资格）——先读规则再动手。

## 6. 轻读结论（2026-10 补）

**一句话**：Perch 蒸馏 + 5s 集成 + 多轮 Noisy Student 的标准化配方；同时是"AI 编码代理参赛边界"的治理分水岭。

- 1st（169 票）：Perch v2/AudioProtoPNet cosine 蒸馏 → 微调 + 自训练（1 轮 0.946 / 2 轮 **0.950** / 3 轮 0.949）；LSS 注入标签和归一化 0.5、PL 上限 0.75、双注入器分样本；Site-22 mask +0.002；属级专家 +0.001~0.002；两个域定制验证；终分公 0.967/私 0.961。
- 2nd（53 票）：Perch 蒸馏 +0.02 但增相关性 → 弃用保多样性；4 轮伪标；soft AUC+0.25 BCE；XC 预训练骨干破 0.930；验证不可靠（LSS AUC-LB 相关 0.2）→ LB 主信号。
- 事件：101 名纯 Claude-Code（自动 autoresearch + 邮件授权提交）被移除；LLM 工具使用大讨论（142/60 票帖）。

**裁决**：蒸馏可塑但增相关；自训练要控注入强度/来源隔离；5s 是甜点；验证优先做域拆分；"人做 idea + agent 做工程"是合规安全区。

**悬案**：移除的规则依据未收录；3rd 方案缺失。

## 7. 图表证据

![1st 的完整管线](../../intel/birdclef-2026/bodies/704752_img/01.png)

**图 1**（topic 704752）：蒸馏（Perch/AudioProtoPNet→CNN）→ 微调+自训练 → 定制后处理 → rank 集成 → 两次提交。

## 8. 出处

- 讨论区索引：`intel/birdclef-2026/topics.md`（80 条）
- 已收录 write-up（6 篇）：
  - 1st Noisy Student + 蒸馏（169 票）：https://www.kaggle.com/competitions/birdclef-2026/discussion/704752
  - 2nd 多样集成 + 分类群专家（53 票）：https://www.kaggle.com/competitions/birdclef-2026/discussion/704399
  - 11th 不用 Perch（46 票）：https://www.kaggle.com/competitions/birdclef-2026/discussion/704264
  - 101st 全自动 Claude-Code 方案（48 票，被取消资格）：https://www.kaggle.com/competitions/birdclef-2026/discussion/704391
  - Claude-Code 结果讨论（142 票）：https://www.kaggle.com/competitions/birdclef-2026/discussion/681146
- 轻读全本：`analysis/deep/birdclef-2026.md`（Tier B 轻读：对照矩阵/裁决/证据分级/悬案 + 1 图证）
