# HuBMAP - Hacking the Human Vasculature

> 主题：cv ｜ 子类：— ｜ 领域：医疗影像 ｜ 类别：Research
> 截止：2023-07-31 ｜ 队伍数：1021 ｜ 机制：代码赛 ｜ 指标：Dice / 血管检测
> 数据来源：`intel/hubmap-hacking-the-human-vasculature/`（80 条主题索引 + 6 篇 write-up 正文）

## 1. 任务与数据

- 预测目标：在肾脏病理切片中分割**血管结构**（细管状 + 点状）。
- 数据形态：WSI + 血管掩码；**标注噪声大**（不同标注者边界不一致）。
- 构造陷阱：标注噪声、细结构、WSI 切块。

## 2. 方案谱系

| 方案 | 名次 | 关键点 |
| --- | --- | --- |
| **"如何正确利用噪声标注"** | 3rd | 标题即方法：把标注噪声当作需要显式处理的变量（而非忽略）；作者提到"关注最新研究很重要" |

## 3. 关键技巧

- **噪声标注的处理范式**（多标注者一致性、软标签、损失加权）。
- **细管状结构的表示与损失**（与 Blood Vessel、Vesuvius 同源）。
- **跟踪最新研究**（3rd 明确经验）。

## 4. 可迁移性评估

- **可直接迁移**：
  - **标注噪声是常态**（医学影像尤甚）：用软标签/一致性过滤而非硬性信任；
  - 细管状结构的损失与后处理；
  - 跟踪最新论文的习惯。
- 需要前提：病理图像处理与分割框架。
- 不建议照搬：假设标注完美。

## 5. 对新手的关键启示

1. **把标注噪声当成一等公民**（本场 3rd 的核心主题）。
2. HuBMAP 系列（2022 Organ、2023 Vasculature）都强调"数据质量与标准化 > 模型"。
3. 与 Blood Vessel、Vesuvius、BYU 对照：**细结构/点目标的通用解法 = 连续表示 + 专用损失 + 后处理**。

## 6. 出处

- 讨论区索引：`intel/hubmap-hacking-the-human-vasculature/topics.md`（80 条）
- 已收录 write-up（6 篇）：
  - 公开 1 / 私榜 3（219 票）：https://www.kaggle.com/competitions/hubmap-hacking-the-human-vasculature/discussion/428296
  - 1st（82 票）：https://www.kaggle.com/competitions/hubmap-hacking-the-human-vasculature/discussion/429060
  - 7th（63 票）：https://www.kaggle.com/competitions/hubmap-hacking-the-human-vasculature/discussion/428295
