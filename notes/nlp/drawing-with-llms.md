# Drawing with LLMs（SVG 生成）

> 主题：nlp（生成式）｜ 子类：— ｜ 领域：图像生成 ｜ 类别：Featured
> 截止：2025-05-27 ｜ 队伍数：1309 ｜ 机制：代码赛 ｜ 指标：SVG Image Fidelity（视觉保真 + 文本还原）
> 数据来源：`intel/drawing-with-llms/`（80 条主题索引 + 6 篇 write-up 正文）

## 1. 任务与数据

- **任务形式**：根据文本提示生成 **SVG 矢量图**，由保真度指标打分（同时考察画面与其中的文字内容）。
- **数据形态**：提示词 + 参考图；无训练集，属于"零样本生成 + 指标优化"。
- **构造陷阱**：
  - **指标含 OCR 成分** → 是否在图中"画出提示词文字"会显著影响得分（社区出现 "OCR decoy" 这类做法）。
  - SVG 是结构化矢量格式，光栅化-生成-矢量化流程会引入失真。

## 2. 方案谱系

| 方案 | 名次 | 关键点 |
| --- | --- | --- |
| 多候选生成 + 筛选（含 OCR 诱饵与美学修饰） | 1st | 用 SSD-1B 生成 64 张候选 → 转 SVG → 补入 OCR 诱饵、提示文本与美学元素 → 逐张评分选优 |
| 扩散模型 + **可微 SVG 优化** | 3rd | VQA/AES 0.81/0.64；用 diffvg 类可微渲染直接把指标当损失优化 |
| SD3.5M + **DRaFT** + diffvg | 4th | 用强化式微调（DRaFT）对齐保真指标 |
| 初学者方案 | 13th | 说明该赛道对新手也友好 |

## 3. 关键技巧

- **多候选 + 选择器**：生成大量候选再按指标挑选，是零样本生成任务最稳的策略。
- **可微渲染优化**：把 SVG 参数当成可学习变量，直接用指标做梯度优化（diffvg）。
- **指标对齐微调**：DRaFT 类方法用指标反馈微调生成模型。
- **指标工程**：理解指标里 OCR/美学等分项的权重（本场出现针对 OCR 分项的诱饵做法）。

## 4. 可迁移性评估

- **可直接迁移**：
  - **"多生成 + 指标筛选"** 是生成式比赛的基础策略。
  - 可微渲染/可微优化在结构化输出任务中很有价值。
  - 生成任务的指标常是多分项加权 → 先拆解分项再做针对性优化。
- 需要前提：扩散模型与可微渲染工具链（diffvg 等）；GPU 资源。
- 不建议照搬：纯靠指标套利（OCR 诱饵）——不可迁移，且有规则风险。

## 5. 对新手的关键启示

1. **生成类任务的通用套路是"多采样 + 选择"**，选择器质量决定上限。
2. **先把指标的构成拆开**（视觉、文字、美学各占多少），再决定优化方向。
3. 结构化输出（SVG/代码）可以走"可微优化"路线，值得了解。

## 6. 出处

- 讨论区索引：`intel/drawing-with-llms/topics.md`（80 条）
- 已收录 write-up（6 篇）：
  - 1st（76 票）：https://www.kaggle.com/competitions/drawing-with-llms/discussion/581027
  - 2nd（39 票）：https://www.kaggle.com/competitions/drawing-with-llms/discussion/581023
  - 3rd（98 票）：https://www.kaggle.com/competitions/drawing-with-llms/discussion/581024
  - 4th（40 票）：https://www.kaggle.com/competitions/drawing-with-llms/discussion/581108
  - 13th（38 票）：https://www.kaggle.com/competitions/drawing-with-llms/discussion/581032
