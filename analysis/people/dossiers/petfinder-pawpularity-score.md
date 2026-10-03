# PetFinder.my - Pawpularity Contest

> `petfinder-pawpularity-score` ｜ Research ｜ 指标 Root Mean Squared Error ｜ 3537 队 ｜ 截止 2022-01-14

本页汇总该场 **2 条 ≥50 票 GM 主题帖**、**6 条断言**、**1 条高票评论**。

## GM 主题帖

| 票 | 选手 | 日期 | 主题 |
| --- | --- | --- | --- |
| 329 | [@titericz](https://www.kaggle.com/titericz) | 2022-01-19 | [1st Place - Winning Solution - Full Writeup](https://www.kaggle.com/competitions/petfinder-pawpularity-score/discussion/301686) |
| 164 | [@cdeotte](https://www.kaggle.com/cdeotte) | 2022-01-15 | [6th Place - Multitask Learning](https://www.kaggle.com/competitions/petfinder-pawpularity-score/discussion/301015) |

## 断言（条件→动作→机制→结果）

| 选手 | 等级 | 阶段 | 动作（节选） | 出处 |
| --- | --- | --- | --- | --- |
| @titericz | A | 特征与数据工程 | 用预训练模型做特征提取把图像回归转成表格回归：取 ImageNet-1k 线性头输出（优于内部 embedding 层）；cuML SVR 加前向爬山多起点选特征集合；最终三组 S | [petfinder-pawpularity-score#301686-01](https://www.kaggle.com/competitions/petfinder-pawpularity-score/discussion/301686) |
| @cdeotte | A | 验证设计 | 最终两个提交分别选 best LB（CV 17.15 / LB 17.64）与 best CV（CV 16.98 / LB 17.78）；best CV 提交的 public ra | [petfinder-pawpularity-score#301015-01](https://www.kaggle.com/competitions/petfinder-pawpularity-score/discussion/301015) |
| @cdeotte | A | 集成与融合 | 每天训一个新模型、保存 OOF，与当前 best CV 集成和 best LB 集成分别等权比较；提升哪个就加入哪个；关键是多样性（尺寸、backbone、增广）而非单模强度 | [petfinder-pawpularity-score#301015-04](https://www.kaggle.com/competitions/petfinder-pawpularity-score/discussion/301015) |
| @cdeotte | A | 复盘与流程 | 自己用去年数据预训练或推理都无收益；但 top 方案用去年重复图（约 33% 图像）拼接去年 meta 特征有效 | [petfinder-pawpularity-score#301015-05](https://www.kaggle.com/competitions/petfinder-pawpularity-score/discussion/301015) |
| @cdeotte | B | 特征与数据工程 | 用随机方形裁剪（保留纵横比）代替压扁；随机裁剪同时充当增广 | [petfinder-pawpularity-score#301015-02](https://www.kaggle.com/competitions/petfinder-pawpularity-score/discussion/301015) |
| @cdeotte | B | 建模与训练 | 把 Cat/Dog 标签作为额外输出（辅助目标）而不是把 meta 输入模型；比赛 meta 无帮助 | [petfinder-pawpularity-score#301015-03](https://www.kaggle.com/competitions/petfinder-pawpularity-score/discussion/301015) |

## 高票评论

| 票 | 选手 | 日期 | 摘录 | 出处 |
| --- | --- | --- | --- | --- |
| 22 | @cdeotte | 2022-01-15 | Here are some ideas that come to mind change batch size change input image size change backbone use CNN vs. Tr | [301015](https://www.kaggle.com/competitions/petfinder-pawpularity-score/discussion/301015) |

## 关联资产

- 深读：`analysis/deep/petfinder-pawpularity-score.md`
- 结构化摘要：`notes/cv/petfinder-pawpularity-score.md`
- 归档讨论区：`intel/petfinder-pawpularity-score/`（主题 2 条有 ≥50 票帖，图证 4 个）
