# Regression of Used Car Prices

> `playground-series-s4e9` ｜ Playground ｜ 指标 Mean Squared Error ｜ 3066 队 ｜ 截止 2024-09-30

本页汇总该场 **1 条 ≥50 票 GM 主题帖**、**3 条断言**、**1 条高票评论**。

## GM 主题帖

| 票 | 选手 | 日期 | 主题 |
| --- | --- | --- | --- |
| 63 | [@cdeotte](https://www.kaggle.com/cdeotte) | 2024-09-14 | [Which Features Interact? and How To Leak Free Target Encode with RAPID](https://www.kaggle.com/competitions/playground-series-s4e9/discussion/533961) |

## 断言（条件→动作→机制→结果）

| 选手 | 等级 | 阶段 | 动作（节选） | 出处 |
| --- | --- | --- | --- | --- |
| @cdeotte | A | 数据理解 | brand 与 milage 排第 3（电车里程影响小）；model 与 int_col 第 4（不同品牌偏好内饰色）；accident 与 model_year 强（新车出事故掉 | [playground-series-s4e9#533961-02](https://www.kaggle.com/competitions/playground-series-s4e9/discussion/533961) |
| @cdeotte | A | 验证设计 | 5 折中每折 fit_transform 训练、再 transform 验证与测试（不能先对全 train 算 TE）；TE 自身的 fit_transform 还要内部 5 折（ | [playground-series-s4e9#533961-03](https://www.kaggle.com/competitions/playground-series-s4e9/discussion/533961) |
| @cdeotte | B | 特征与数据工程 | 先分箱（如 milage 每 1000 一箱），再拼接成字符串列（brand-milage），得到新类别特征后用 target encoding；用 Lasso 训全部 bi-gr | [playground-series-s4e9#533961-01](https://www.kaggle.com/competitions/playground-series-s4e9/discussion/533961) |

## 高票评论

| 票 | 选手 | 日期 | 摘录 | 出处 |
| --- | --- | --- | --- | --- |
| 14 | @cdeotte | 2024-09-14 | The best way to evaluate new features is to use our local CV score. If CV score improves when we add the new f | [533961](https://www.kaggle.com/competitions/playground-series-s4e9/discussion/533961) |

## 关联资产

- 深读：`analysis/deep/playground-series-s4e9.md`
- 结构化摘要：`notes/tabular/playground-series-s4e9.md`
- 归档讨论区：`intel/playground-series-s4e9/`（主题 1 条有 ≥50 票帖，图证 2 个）
