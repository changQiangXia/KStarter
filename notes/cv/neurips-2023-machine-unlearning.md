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

## 6. 出处

- 讨论区索引：`intel/neurips-2023-machine-unlearning/topics.md`（80 条）
- 已收录 write-up（6 篇）：
  - 2nd（35 票）：https://www.kaggle.com/competitions/neurips-2023-machine-unlearning/discussion/458721
  - 5th（30 票）：https://www.kaggle.com/competitions/neurips-2023-machine-unlearning/discussion/458531
  - 6th 简洁方案（13 票）：https://www.kaggle.com/competitions/neurips-2023-machine-unlearning/discussion/458740
