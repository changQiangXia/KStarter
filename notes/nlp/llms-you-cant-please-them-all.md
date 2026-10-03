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

## 7. 轻读结论（2026-10 补）

**一句话**：LLM-as-a-Judge 的提示注入对抗赛——**攻击工程（000/999/099/909/990）+ 本地代理评委验证 + 公榜分区探针**三者叠加决定名次。

- 5th：418 次提交（攻击 327）；用"e=0/1、相似度=0"的三类攻击**2 次提交**定出三分区公测索引数（i%3 实测 115/79/106）；最优 split 后 avg_s<0.2、补词过 avg_e≥5.0 阈值 → 30.050（6 seed 复测稳定）。
- 3rd：本地 Gemma2B/9B + Llama3B（+8B）8bit 验证；消融：无验证 28.8（私）→ 3 模型 29.92 → 4 模型 30.01；seed 1143 近完美 split（102/100/98）；private 是随机 70%。
- 1st：本地 Gemma/Qwen/Phi + Qwen 词表/NINE/韩文/Base64/白俄文注入；seed 1144；12 篇文章；承认运气。
- 评委身份三队猜测不一致（gemma/gemma/llama vs Gemma/Qwen/Phi）——代理相关性取代真实身份。

**数字账精选**：5th 30.050 六测；3rd 30.01（私）；1st 80 票方案；旧 metric 30.0 exploit（71 票，对新评委失效）。

**事件**：20.293 notebook 泄漏争议（49+46 票）；平台治理与攻击资产扩散问题。

**悬案**：指标精确公式；评委真实身份；999 零除假设；2nd/4th 方案未收录（4th 39 票在 digest 但未入库正文）。

## 8. 图表证据

**本场无归档图片**（`intel/llms-you-cant-please-them-all/bodies/` 无 `*_img`），无法内嵌图证。

## 9. 出处

- 讨论区索引：`intel/llms-you-cant-please-them-all/topics.md`（80 条）
- 已收录 write-up（6 篇）：
  - 1st（80 票）：https://www.kaggle.com/competitions/llms-you-cant-please-them-all/discussion/566372
  - 3rd（39 票）：https://www.kaggle.com/competitions/llms-you-cant-please-them-all/discussion/566515
  - 4th（39 票）：https://www.kaggle.com/competitions/llms-you-cant-please-them-all/discussion/566479
  - 5th（52 票）：https://www.kaggle.com/competitions/llms-you-cant-please-them-all/discussion/566322
- 轻读全本：`analysis/deep/llms-you-cant-please-them-all.md`（Tier B 轻读：对照矩阵/裁决/证据分级/悬案）
