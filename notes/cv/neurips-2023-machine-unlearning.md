# NeurIPS 2023 - Machine Unlearning

> 主题：cv ｜ 子类：unlearning ｜ 领域：AI 安全/隐私 ｜ 类别：Research
> 截止：2023-11-29 ｜ 队伍数：1188 ｜ 机制：代码赛 ｜ 指标：遗忘效果 + 保留性能（多指标）
> 数据来源：`intel/neurips-2023-machine-unlearning/`（80 条主题索引 + 6 篇 write-up 正文）

## 1. 任务与数据

- 预测目标：让图像分类模型**"遗忘"指定子集**（如特定类别/样本），同时保持其余性能——机器遗忘（machine unlearning）。
- 数据形态：CIFAR-10/100 等图像数据集 + 待遗忘子集定义。
- 构造陷阱：
  - **双重目标**：遗忘要彻底（不能再预测该子集），同时保留性能不能掉；
  - 评估含"重学习攻击"等对抗性检查；
  - 训练策略需要定制（不是常规分类训练）。

## 2. 方案特征

| 类型 | 说明 |
| --- | --- |
| 简化方案（6th） | 用相对简洁的策略实现遗忘（强调可控与稳健） |
| 主流路线 | ① 微调（gradient ascent on forget set + descent on retain set）；② 重新训练；③ 激活/权重扰动 |

## 3. 关键技巧

- **遗忘与保留的权衡**（多目标损失/约束）。
- **对抗性评估意识**：遗忘必须经得起"重学习"检验。
- **稳健性优先**（6th 强调简洁可控）。

## 4. 可迁移性评估

- **可直接迁移**：
  - 多目标权衡的训练设计（遗忘 + 保留，类似公平性与性能的权衡）；
  - 对抗性评估思维（成果要被攻击者检验）；
  - 隐私/安全类任务的稳健优先原则。
- 需要前提：对模型训练过程的可控修改能力。
- 不建议照搬：只做梯度上升（会破坏保留性能）。

## 5. 对新手的关键启示

1. **AI 安全/隐私已成为 Kaggle 独立赛道**（本场、AI Agent Security、gpt-oss 红队、RECOD 图像伪造）。
2. **"让模型忘掉"比"让模型学会"更难**（要同时满足多个互斥目标）。

## 7. 轻读结论（2026-10 补）

**一句话**：本届的实践结论是"**简单重置/蒸馏/微调 > 论文 SOTA 遗忘算法**"——6th 重置 conv1/fc + KL 蒸馏 + 三损失微调（私榜 0.07831，且不需要 forget set）；2nd 用"KL 打平 + 对抗微调"（CosineAnnealingLR +0.007）；而 5th/6th 都报告 SCRUB、RelaxLoss、class weights 等无效。

- 6th（458740）：conv1/fc 在"全量 vs 仅 retain"训练下的余弦相似度为负（-0.03/-0.014）→ 重置首末层；全类预热私榜 0.07219 vs 前两类预热私榜 0.07831（后者更优）。
- 2nd（458721）：1 轮 KL→均匀 + 8 轮对抗微调（forget 轮监督对比、温度 1.15、batch 256）；CosineAnnealingLR 使公榜 0.084→0.091。
- 5th（458531）：Conv2D 权重转置重训 3 轮 + 伪标签微调的两路集成（246+266 模型），私榜 0.0785/0.0756；RelaxLoss、SCRUB 等失败。
- 12th 公榜（458648）：相似度采样 bad teaching（好/坏教师 KL + 加权 + 先破坏后重建），因超时未进最终榜。
- 治理：不给积分/奖牌（50 票 / 34 评论）、公开 notebook 同质化（23 票）、评分失败（14 票）、"少 epoch 更好"（16 票）。

**裁决**：先把指标本地复现；优先简单可控的重置/蒸馏/微调方案并调好调度与温度；论文方法需要在本赛指标下重新验证；工程（超时/评分）风险要预留。

**悬案**：1st/3rd/4th/7th/9th 方案未收录；官方 metric 公式未整理。

## 8. 图表证据

![6th 的两阶段流程](../../intel/neurips-2023-machine-unlearning/bodies/458740_img/04.png)

**图 1**（topic 458740）：KL 蒸馏预热 + CE/软 CE/KL 微调。

![层间权重余弦相似度](../../intel/neurips-2023-machine-unlearning/bodies/458740_img/01.png)

**图 2**（topic 458740）：conv1/fc 的余弦相似度为负 → 重置首末层的依据。

![双教师 bad teaching 流程](../../intel/neurips-2023-machine-unlearning/bodies/458648_img/01.png)

**图 3**（topic 458648）：好/坏教师 + 相似度采样的双教师 KL 结构。

## 9. 出处

- 讨论区索引：`intel/neurips-2023-machine-unlearning/topics.md`（80 条）
- 已收录 write-up（6 篇）：
  - 2nd（35 票）：https://www.kaggle.com/competitions/neurips-2023-machine-unlearning/discussion/458721
  - 5th（30 票）：https://www.kaggle.com/competitions/neurips-2023-machine-unlearning/discussion/458531
  - 6th 简洁方案（13 票）：https://www.kaggle.com/competitions/neurips-2023-machine-unlearning/discussion/458740
  - 12th 公榜（14 票）：https://www.kaggle.com/competitions/neurips-2023-machine-unlearning/discussion/458648
  - 论文与代码合集（45 票）：https://www.kaggle.com/competitions/neurips-2023-machine-unlearning/discussion/438660
  - 无积分奖牌争议（50 票）：https://www.kaggle.com/competitions/neurips-2023-machine-unlearning/discussion/438567
