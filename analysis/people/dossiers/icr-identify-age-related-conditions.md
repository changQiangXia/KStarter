# ICR - Identifying Age-Related Conditions

> `icr-identify-age-related-conditions` ｜ Featured ｜ 指标 Weighted Multiclass Loss ｜ 6430 队 ｜ 截止 2023-08-10

本页汇总该场 **2 条 ≥50 票 GM 主题帖**、**8 条断言**、**2 条高票评论**。

## GM 主题帖

| 票 | 选手 | 日期 | 主题 |
| --- | --- | --- | --- |
| 382 | [@cdeotte](https://www.kaggle.com/cdeotte) | 2023-05-24 | [How To Balance Training And Boost  CV and LB Score!](https://www.kaggle.com/competitions/icr-identify-age-related-conditions/discussion/412507) |
| 64 | [@cdeotte](https://www.kaggle.com/cdeotte) | 2023-08-11 | [Silver Medal - LB=0.39 - Sliding Time Cross Validation!](https://www.kaggle.com/competitions/icr-identify-age-related-conditions/discussion/431067) |

## 断言（条件→动作→机制→结果）

| 选手 | 等级 | 阶段 | 动作（节选） | 出处 |
| --- | --- | --- | --- | --- |
| @cdeotte | A | 验证设计 | 按日期排序、给无日期样本随机分配日期，再滑动 START/END 窗口，每折验证为窗口内全部行；理由：XGB 把时间当特征时会成为最重要特征（即使无日期样本随机 fillna），说 | [icr-identify-age-related-conditions#431067-01](https://www.kaggle.com/competitions/icr-identify-age-related-conditions/discussion/431067) |
| @cdeotte | A | 验证设计 | 易时段 OOF balanced log loss 0.15、难时段 0.40；作者推断 public 是易时段、private 是难时段；其时间 CV 模型 CV 0.27 /  | [icr-identify-age-related-conditions#431067-02](https://www.kaggle.com/competitions/icr-identify-age-related-conditions/discussion/431067) |
| @cdeotte | A | 后处理 | 逐折找最优 top/bottom 阈值并画图；取中位 bottom 阈值时，若 private 是随机时段则只有 50% 概率有效；要评估 private 需按 private 规 | [icr-identify-age-related-conditions#431067-03](https://www.kaggle.com/competitions/icr-identify-age-related-conditions/discussion/431067) |
| @cdeotte | A | 复盘与流程 | 两种风险方案：LB probing 伪标签、保守 PP 阈值；结果都伤了 private；作者最终选择它们冲一失败；干净的 time-CV 模型拿到银牌 | [icr-identify-age-related-conditions#431067-04](https://www.kaggle.com/competitions/icr-identify-age-related-conditions/discussion/431067) |
| @cdeotte | A | 数据理解 | train/public/private 正类都约 17.5%，但 EJ=B 占比 64%/62%/50%；private 的 EH、FD 有 NaN（train 无）；priva | [icr-identify-age-related-conditions#431067-05](https://www.kaggle.com/competitions/icr-identify-age-related-conditions/discussion/431067) |
| @cdeotte | B | 建模与训练 | 训练时给正类 4.7x 样本权重，使正负类重要性相当 | [icr-identify-age-related-conditions#412507-01](https://www.kaggle.com/competitions/icr-identify-age-related-conditions/discussion/412507) |
| @cdeotte | C | 后处理 | 预测阶段把概率转成 odds、按 boost 缩放后再转回概率 | [icr-identify-age-related-conditions#412507-02](https://www.kaggle.com/competitions/icr-identify-age-related-conditions/discussion/412507) |
| @cdeotte | C | 验证设计 | 对每种方法分别训练并计算 OOF CV，再选用最优者 | [icr-identify-age-related-conditions#412507-03](https://www.kaggle.com/competitions/icr-identify-age-related-conditions/discussion/412507) |

## 高票评论

| 票 | 选手 | 日期 | 摘录 | 出处 |
| --- | --- | --- | --- | --- |
| 16 | @cpmpml | 2023-08-11 | Well done! I am so happy the winner did not win by sheer luck. That you used a deep learning model of your own | [430843](https://www.kaggle.com/competitions/icr-identify-age-related-conditions/discussion/430843) |
| 11 | @cdeotte | 2023-08-11 | Congratulations. Great work! I also like DNN and I am happy to see DNN win. What did this submission score on  | [430843](https://www.kaggle.com/competitions/icr-identify-age-related-conditions/discussion/430843) |

## 关联资产

- 深读：`analysis/deep/icr-identify-age-related-conditions.md`
- 结构化摘要：`notes/tabular/icr-identify-age-related-conditions.md`
- 归档讨论区：`intel/icr-identify-age-related-conditions/`（主题 2 条有 ≥50 票帖，图证 6 个）
