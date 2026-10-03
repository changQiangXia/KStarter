# Foursquare - Location Matching

> `foursquare-location-matching` ｜ Featured ｜ 指标 Jaccard ｜ 1079 队 ｜ 截止 2022-07-07

本页汇总该场 **2 条 ≥50 票 GM 主题帖**、**8 条断言**、**1 条高票评论**。

## GM 主题帖

| 票 | 选手 | 日期 | 主题 |
| --- | --- | --- | --- |
| 92 | [@takoihiraokazu](https://www.kaggle.com/takoihiraokazu) | 2022-07-09 | [1st place solution](https://www.kaggle.com/competitions/foursquare-location-matching/discussion/336055) |
| 61 | [@philippsinger](https://www.kaggle.com/philippsinger) | 2022-07-19 | [3rd place solution](https://www.kaggle.com/competitions/foursquare-location-matching/discussion/338112) |

## 断言（条件→动作→机制→结果）

| 选手 | 等级 | 阶段 | 动作（节选） | 出处 |
| --- | --- | --- | --- | --- |
| @takoihiraokazu | A | 建模与训练 | 四阶段：1) 候选生成（经纬度欧氏距离加名称 embedding 余弦，各 top100，经 LGBM 各留 top20 共约 40）；2) 约 120 特征加 LightGBM（ | [foursquare-location-matching#336055-01](https://www.kaggle.com/competitions/foursquare-location-matching/discussion/336055) |
| @takoihiraokazu | A | 数据工程 | 把 train 与 test 按 name、lat、lon 绑定：加 train-train 真对（1）；移除与 train 绑定的假对（2）；移除 train-test 假对（3 | [foursquare-location-matching#336055-02](https://www.kaggle.com/competitions/foursquare-location-matching/discussion/336055) |
| @takoihiraokazu | A | 复盘与流程 | 最终提交同时包含三种版本：overfit with merge（private/public 0.976/0.976）、非 overfit v1 with merge（0.977/ | [foursquare-location-matching#336055-04](https://www.kaggle.com/competitions/foursquare-location-matching/discussion/336055) |
| @philippsinger | A | 建模与训练 | 一阶段 xlm-roberta-large ArcFace 度量学习（各列用 SEP 拼接，经纬度每 3 位拆分便于 tokenizer，NAN 填空串），全对相似度按阈值取候选； | [foursquare-location-matching#338112-01](https://www.kaggle.com/competitions/foursquare-location-matching/discussion/338112) |
| @philippsinger | A | 验证设计 | 最合理 CV：切出 600k 记录且 POI 唯一作验证、在剩余数据上训练（但少训一半数据）；距截止 6 周起改用 public LB 评估：时间足够、与 CV 相关好、可全量训练 | [foursquare-location-matching#338112-03](https://www.kaggle.com/competitions/foursquare-location-matching/discussion/338112) |
| @philippsinger | A | 复盘与流程 | 作者赛后才知道泄漏（论坛早有讨论）；期间选择被泄漏偏置（更长训练、更强过拟合在该数据上有效），但确保长训不伤 CV；赛后分析显示方案在无重叠数据上仍有竞争力 | [foursquare-location-matching#338112-04](https://www.kaggle.com/competitions/foursquare-location-matching/discussion/338112) |
| @takoihiraokazu | B | 验证设计 | 识别信号：CV-LB gap 大；max IOU 已高却 gap 异常；过拟合模型（no dropout、多 epoch）LB 更高；CV 上升后 CV-LB 相关性消失；FGM  | [foursquare-location-matching#336055-03](https://www.kaggle.com/competitions/foursquare-location-matching/discussion/336055) |
| @philippsinger | B | 建模与训练 | 初期 Triplet 类模型更易起步，但 ArcFace 调通后明显更优；ArcFace 需要额外稳定化才能收敛 | [foursquare-location-matching#338112-02](https://www.kaggle.com/competitions/foursquare-location-matching/discussion/338112) |

## 高票评论

| 票 | 选手 | 日期 | 摘录 | 出处 |
| --- | --- | --- | --- | --- |
| 12 | @philippsinger | 2022-07-19 | There is no magic in the code that would be interesting. Rather certain training tricks to make the training s | [338112](https://www.kaggle.com/competitions/foursquare-location-matching/discussion/338112) |

## 关联资产

- 深读：`analysis/deep/foursquare-location-matching.md`
- 结构化摘要：`notes/tabular/foursquare-location-matching.md`
- 归档讨论区：`intel/foursquare-location-matching/`（主题 2 条有 ≥50 票帖，图证 1 个）
