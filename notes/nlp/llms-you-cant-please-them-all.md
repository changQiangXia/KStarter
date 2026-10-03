# LLMs - You Can't Please Them All

> 主题：nlp ｜ 子类：— ｜ 领域：LLM 评测 ｜ 类别：Featured
> 截止：2025-08-0X ｜ 队伍数：2000+ ｜ 机制：代码赛 ｜ 指标：LLM 评委打分
> 数据来源：`intel/llms-you-cant-please-them-all/`（80 条主题索引 + 6 篇 write-up 正文）

## 1. 任务与数据

- **任务形式**：面对一个**黑盒 LLM 评委**（LLM-as-a-Judge），构造文本使其尽可能拿到高分——本质是"针对评委的优化问题"，而非传统 NLP 任务。
- **数据形态**：无固定训练集，答案空间由评委模型的行为定义。
- **构造陷阱**：
  - 评委模型未知，需要**先逆向其偏好**（社区称"解开谜题"）。
  - 打分函数可能对特定格式/语言/长度敏感，容易过拟合到评委的怪癖。

## 2. 验证方案

| 方案 | 使用者 | 说明 |
| --- | --- | --- |
| 本地复现评委行为 | 3rd | 借助社区线索推断评委模型，自建本地评分做快速迭代 |
| 多方案并列提交 | 多队 | 评委打分方差大，需要冗余 |

## 3. 方案谱系

| 方案 | 名次 | 关键点 |
| --- | --- | --- |
| 评委偏好逆向 + 攻击策略 | 1st / 3rd | 3rd 的核心攻击策略来自社区"用其他语言书写"的思路 |
| "谜题式"优化 | 5th | 把比赛当作解谜：破解 LLM 评委的偏好 + 最优分组（partitioning）问题 |
| 词表搜索 | 多队 | 自建词表效果不稳定、迭代慢（3rd 的教训） |

## 4. 关键技巧

- **先逆向评委**：确定判分模型的家族/行为，才能有效优化。
- **跨语言攻击**：用非英语文本绕过评委的语言偏好（3rd 的关键）。
- **本地快速评测回路**：没有本地评分就无法迭代。
- **组合优化**：分组/分配类子问题（partitioning）可以用算法手段求解。

## 5. 可迁移性评估

- **可直接迁移**：
  - **面对黑盒评分器时，第一件事是逆向它的行为**（与 AI Agent Security 的结论一致）。
  - 建立本地快速评分回路。
- **需要前提**：
  - 需要大量调用 LLM 的资源（或找到代理模型）。
- **不建议照搬**：
  - 把"针对评委的攻击"当作通用 NLP 技能——它高度依赖具体评委实现。

## 6. 对新手的关键启示

1. 这类比赛**不是 NLP 建模比赛**，是"理解评分器"的比赛——先认清这一点。
2. **本地评测回路是所有黑盒优化的前提**。
3. 社区共享的线索（评委家族、攻击方向）价值极高，但需要自己验证。

## 7. 出处

- 讨论区索引：`intel/llms-you-cant-please-them-all/topics.md`（80 条）
- 已收录 write-up（6 篇）：
  - 1st（80 票）：https://www.kaggle.com/competitions/llms-you-cant-please-them-all/discussion/566372
  - 3rd（39 票）：https://www.kaggle.com/competitions/llms-you-cant-please-them-all/discussion/566515
  - 4th（39 票）：https://www.kaggle.com/competitions/llms-you-cant-please-them-all/discussion/566479
  - 5th（52 票）：https://www.kaggle.com/competitions/llms-you-cant-please-them-all/discussion/566322
