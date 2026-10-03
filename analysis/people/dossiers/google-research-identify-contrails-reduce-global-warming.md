# Google Research - Identify Contrails to Reduce Global Warming

> `google-research-identify-contrails-reduce-global-warming` ｜ Research ｜ 指标 contrails_global_dice ｜ 954 队 ｜ 截止 2023-08-09

本页汇总该场 **1 条 ≥50 票 GM 主题帖**、**3 条断言**、**0 条高票评论**。

## GM 主题帖

| 票 | 选手 | 日期 | 主题 |
| --- | --- | --- | --- |
| 76 | [@tascj0](https://www.kaggle.com/tascj0) | 2023-08-10 | [9th place solution](https://www.kaggle.com/competitions/google-research-identify-contrails-reduce-global-warming/discussion/430479) |

## 断言（条件→动作→机制→结果）

| 选手 | 等级 | 阶段 | 动作（节选） | 出处 |
| --- | --- | --- | --- | --- |
| @tascj0 | A | 数据理解 | 发现 polygon 转 binary mask 时最左点未包含而最右点包含，导致图像与 mask 错位；给出原始、普通翻转、正确翻转三种图文序列对照 | [google-research-identify-contrails-reduce-global-warming#430479-01](https://www.kaggle.com/competitions/google-research-identify-contrails-reduce-global-warming/discussion/430479) |
| @tascj0 | A | 特征与数据工程 | 方案 1：训练用错位组合、推理用一致翻转加 TTA；方案 2：训练与推理都把图像平移 +0.5 像素，增广恢复正常（warpAffine 矩阵 [2,0,1.5;0,2,1.5]  | [google-research-identify-contrails-reduce-global-warming#430479-02](https://www.kaggle.com/competitions/google-research-identify-contrails-reduce-global-warming/discussion/430479) |
| @tascj0 | B | 建模与训练 | 只用 false_color 图与 UNet；强 backbone 帮助很大；用全部个体标注训练有帮助；小模型上伪标签有效但没时间用到大队列 | [google-research-identify-contrails-reduce-global-warming#430479-03](https://www.kaggle.com/competitions/google-research-identify-contrails-reduce-global-warming/discussion/430479) |

## 高票评论

_无 ≥10 票评论_

## 关联资产

- 深读：`analysis/deep/google-research-identify-contrails-reduce-global-warming.md`
- 结构化摘要：`notes/cv/google-research-identify-contrails-reduce-global-warming.md`
- 归档讨论区：`intel/google-research-identify-contrails-reduce-global-warming/`（主题 1 条有 ≥50 票帖，图证 0 个）
