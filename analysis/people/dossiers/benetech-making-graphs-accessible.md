# Benetech - Making Graphs Accessible

> `benetech-making-graphs-accessible` ｜ Featured ｜ 指标 Benetech Mixed Data Type Matching Score ｜ 608 队 ｜ 截止 2023-06-19

本页汇总该场 **1 条 ≥50 票 GM 主题帖**、**5 条断言**、**0 条高票评论**。

## GM 主题帖

| 票 | 选手 | 日期 | 主题 |
| --- | --- | --- | --- |
| 64 | [@conjuring92](https://www.kaggle.com/conjuring92) | 2023-06-20 | [2nd Place Solution [Updated with Code Link]](https://www.kaggle.com/competitions/benetech-making-graphs-accessible/discussion/418430) |

## 断言（条件→动作→机制→结果）

| 选手 | 等级 | 阶段 | 动作（节选） | 出处 |
| --- | --- | --- | --- | --- |
| @conjuring92 | A | 建模与训练 | 基于 matcha-base 的 image-to-text：阶段一用大量合成图做域适应，阶段二用过采样的真实/抽取图特化；阶段二分 scatter 与非 scatter 两个模型 | [benetech-making-graphs-accessible#418430-01](https://www.kaggle.com/competitions/benetech-making-graphs-accessible/discussion/418430) |
| @conjuring92 | A | 数据工程 | 合成数据 700k：100k 水平条、100k 垂直条与直方图、100k 点图、200k 线图、200k 散点；底表 25% 来自 Wikipedia 表格加 75% 合成 XY； | [benetech-making-graphs-accessible#418430-03](https://www.kaggle.com/competitions/benetech-making-graphs-accessible/discussion/418430) |
| @conjuring92 | A | 数据工程 | Datamix 1 用于域适应：比赛合成 60k×3 加比赛抽取 1.1k×16 加自产 700k 加 Bartley 25k；Datamix 2/3 分别针对 scatter 与 | [benetech-making-graphs-accessible#418430-04](https://www.kaggle.com/competitions/benetech-making-graphs-accessible/discussion/418430) |
| @conjuring92 | A | 工程/流程 | EMA 权重、梯度裁剪、cosine 加线性 warmup；增广含随机色调曲线/亮度对比/HSV、多种模糊与高斯噪声、downscale；max_patches 与 max_len | [benetech-making-graphs-accessible#418430-05](https://www.kaggle.com/competitions/benetech-making-graphs-accessible/discussion/418430) |
| @conjuring92 | B | 特征与数据工程 | 输入图像无 prompt，输出以特殊 token 分段（chart_type、num_point、x_span、y_span），数值统一科学计数法；把 histogram 作为附加 | [benetech-making-graphs-accessible#418430-02](https://www.kaggle.com/competitions/benetech-making-graphs-accessible/discussion/418430) |

## 高票评论

_无 ≥10 票评论_

## 关联资产

- 深读：`analysis/deep/benetech-making-graphs-accessible.md`
- 结构化摘要：`notes/cv/benetech-making-graphs-accessible.md`
- 归档讨论区：`intel/benetech-making-graphs-accessible/`（主题 1 条有 ≥50 票帖，图证 1 个）
