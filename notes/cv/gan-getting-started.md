# I'm Something of a Painter Myself（GAN 入门赛，精选）

> 主题：cv ｜ 子类：— ｜ 领域：生成（梵高风格迁移） ｜ 类别：Getting Started ｜ 截止：2026-06-30 ｜ 队伍数：0 ｜ 指标：评审/后处理内核（代码赛）
> 出处：`intel/gan-getting-started/`（80 条主题索引 + 6 篇正文）

## 任务

Kaggle 经典 **CycleGAN 入门赛**：把照片转成莫奈风格，用 MiFID 等指标评估生成质量；submission 通过 notebook 输出，是无数人接触 GAN 的第一站。

## 关键要点

- **资源型条目**（本场讨论区几乎全是学习资料汇编）：
  - 书籍：《GANs in Action》（含标准/条件/损失/图像翻译四类 GAN 的代码谱系：GAN、DCGAN、cGAN、InfoGAN、ACGAN、WGAN/WGAN-GP、LSGAN、Pix2Pix、CycleGAN）；
  - 论文清单：原版 GAN、GAN 概览、大规范研究（Are GANs Created Equal?）、正则化与归一化研究、Top-10 入门论文；
  - 往届 GAN 比赛与 notebook 索引。
- 赛事定位：Getting Started 级——**学习价值 > 竞争价值**；CycleGAN 的非配对图像翻译思想可迁移到任何风格化任务。

## 可迁移要点

- GAN 的学习路径：DCGAN（基础）→ 条件类（cGAN/ACGAN）→ 损失改进（WGAN-GP/LSGAN）→ 图像翻译（Pix2Pix/CycleGAN）。
- 生成任务评价体系（MiFID 类）与业务视觉指标不同，入门时先接受"指标不完美"。
- 资源汇编帖是进入新领域的标准入口（参见通用方法论 §9）。

## 出处

- 完整 GAN 资源汇编：https://www.kaggle.com/competitions/gan-getting-started/discussion/178253
- GAN 全面科普（论文清单）：https://www.kaggle.com/competitions/gan-getting-started/discussion/180515
