# ARC Prize 2024

> 主题：nlp ｜ 子类：reasoning ｜ 领域：抽象推理 ｜ 类别：Featured
> 截止：2024-11-10 ｜ 队伍数：1427 ｜ 机制：代码赛 ｜ 指标：ARC-AGI-1 隐测试得分（$1.1M 奖金）
> 数据来源：`intel/arc-prize-2024/`（80 条主题索引 + 6 篇 write-up 正文）

## 1. 任务与数据

- 预测目标：解 ARC-AGI 抽象推理题（网格变换），在隐藏测试集评分。
- 数据形态：每题仅几个输入-输出示例；训练样本极少。
- 构造陷阱：**没有可迁移的"训练集"**——每题都是新任务，因此**推理期学习（test-time training / fine-tuning）**成为核心范式。

## 2. 方案谱系

| 方案 | 名次 | 关键点 |
| --- | --- | --- |
| **测试时微调**（MindsAI 路线）+ 额外学习输入分布 | 2nd | 除生成测试输出外，还训练模型生成新输入以学习输入分布（"Omni-ARC"）；作者提供了论文 |
| 后续方案 | 3rd / 4th | 见讨论区 |
| 领域综述：SOTA 的 5 类方法 | 社区帖 | 离散程序搜索 → 集成方案 → …（引自 ARC 官方指南） |

## 3. 关键技巧

- **测试时训练/微调（TTT）**：在每道题上现场学习，是 ARC 系比赛的主流范式。
- **多任务自监督**：让模型同时学"输出变换"和"输入分布"（生成新输入）。
- **离散程序搜索**：另一条主线，用搜索而非学习求解。
- **集成与往届方案复用**：本场大量方案基于 2020-2024 年间的公开成果迭代。

## 4. 可迁移性评估

- **可直接迁移**：
  - **TTT 思路**：当测试分布与训练分布差异大时，在推理阶段做适配（与 Jigsaw Agile Rules 的结论一致）。
  - 用辅助自监督任务（学习输入分布）增强推理期学习。
- 需要前提：推理期算力充足；题目可本地枚举/评估。
- 不建议照搬：依赖固定训练集的传统范式。

## 5. 对新手的关键启示

1. **"测试时学习"已经是被反复验证的范式**（ARC 2024/2025、Jigsaw Agile Rules）。
2. **领域长期积累很重要**：ARC 系方案逐年迭代、互相复用。
3. 与 ARC 2025 对照可见同一系列的演进：从 TTT → 合成数据难度阶梯。

## 6. 轻读结论（2026-10 补）

**一句话**：ARC 2024 的分野是 **TTT（测试时训练）+ LLM**（2nd，把小模型解出数从 11 提到 33）对 **DSL 搜索 + 树/CNN 集成**（3rd/4th）；4th 的结语承认"TTT 是当前 SOTA"。表示与规范化（多任务逼出表示、颜色重映射 +2%）比模型规模更值钱。

- 2nd（Omni-ARC）：Qwen2.5-0.5B + LoRA(128) 学 6 种 ARC 任务（原任务/生成输入/examples→code/code+input→output/code→inputs/inputs→code）；每题用 n−1 样本微调 ~300 步（bs=1，每次提交 100 个微调模型）；文本化网格表示；增强投票 + 与 2020 解法集成。
- 4th：DSL+DAG 搜索 + 决策树 + CNN；靠 2024 年更大的内核资源（30GB/12h）加深搜索、扩大集成；集成 = 多数投票 + 关键解豁免 + 按"新解题数"概率抽样。
- 3rd：得分 40 的 notebook；强调抵抗公榜过拟合、做通用解法。
- 21st：**颜色重映射**（按颜色频率排序重编码）给 icecuber 求解器 +2%。
- 社区：上手参考（101 票）、如何着手（85 票）、用 LLM 得 33 分（50 票）、tiny 模型（44 票）、400k 合成题（41 票）。

**裁决**：每题新规则的赛制优先投"测试时适配"；先规范表示再谈模型；集成按历史贡献加权并对关键解豁免投票。

**悬案**：**1st 方案未入库**；3rd 细节在 notebook；合成数据与 tiny 模型帖未细读。

## 7. 图表证据

![Omni-ARC 的六种任务形式](../../intel/arc-prize-2024/bodies/545671_img/02.png)

**图 1**（topic 545671）：同模型多任务训练（含 inputs→input、inputs→code 等），以逼出可复用的 ARC 表示。

## 8. 出处

- 讨论区索引：`intel/arc-prize-2024/topics.md`（80 条）
- 已收录 write-up（6 篇）：
  - 2nd（176 票）：https://www.kaggle.com/competitions/arc-prize-2024/discussion/545671
  - 3rd（18 票）：https://www.kaggle.com/competitions/arc-prize-2024/discussion/550328
  - 4th（15 票）：https://www.kaggle.com/competitions/arc-prize-2024/discussion/550414
  - SOTA 方法综述（13 票）：https://www.kaggle.com/competitions/arc-prize-2024/discussion/535811
  - 2nd Omni-ARC：https://www.kaggle.com/competitions/arc-prize-2024/discussion/545671
  - 21st 颜色重映射：https://www.kaggle.com/competitions/arc-prize-2024/discussion/550209
  - 用 LLM 得 33 分（50 票）：https://www.kaggle.com/competitions/arc-prize-2024/discussion/512910
  - 400k 合成题（41 票）：https://www.kaggle.com/competitions/arc-prize-2024/discussion/543953
- 轻读全本：`analysis/deep/arc-prize-2024.md`（Tier B 轻读：对照矩阵/裁决/证据分级/悬案 + 1 图证）
