# Playground Series S3E3（AUC，"意外夺冠"与性能纪律）

> 主题：tabular ｜ 子类：— ｜ 领域：—（合成数据） ｜ 类别：Playground
> 截止：2023-01-23 ｜ 队伍数：665 ｜ 机制：标准赛 ｜ 指标：ROC AUC
> 数据来源：`intel/playground-series-s3e3/`（76 条主题索引 + 6 篇 write-up 正文）

## 1. 任务与数据

- 二分类 AUC；1st 的获奖方式朴实：**以公开 notebook（XGB+LGBM+CatBoost）为骨架 + 一段风险因子特征工程**，公开榜下滑时甚至忘记选提交——"That was unexpected..."。
- 特征工程核心（可复用的"风险因子"）：比值特征、多个阈值布尔（age<某值、某值区间）、分箱替换、条件组合（`(A>a)&(B<b)`）等——把连续变量转成领域化的风险标记。

## 2. 验证方案

- 常规 CV；社区帖"54th 经验教训"提示本类赛的分数带接近、选择与纪律决定档位。

## 3. 模型家族

| 方案 | 使用者层次 | 关键点 | 出处 |
| --- | --- | --- | --- |
| 公开骨架 + 风险因子 FE | 1st | 单一改动夺冠 | topic 380920 |
| 8th / 14th | 高位 | 常规线 | topic 381052 |
| Hill Climbing 集成教程 | 社区 | 权重搜索实操 | topic 379690 |

## 4. 关键技巧

- **风险因子特征模板**：比值、阈值布尔、区间标记、条件组合——医疗/信贷类表格的通用转换。
- **性能纪律（Avoid .apply()）**：用向量化二元运算（`df.Age.le(30).astype(int)`）替代 `.apply(lambda)`——小数据无感、大数据致命；这是可迁移的工程习惯而非本场特技。
- 1st 的运气成分（忘选提交仍夺冠）反衬：**分数带越挤，心态与纪律权重越大**。

## 5. 可迁移性评估

- **可直接迁移**：风险因子特征模板；向量化替代 apply；公开骨架+FE 的起步法。
- **需要前提**：特征可解释（医疗/金融场景）。
- **不建议照搬**：把"忘记选提交"当浪漫（纪律仍是正解）；在大数据上用 apply 写特征。

## 6. 对新手的关键启示

- 从公开 notebook 开始不丢人：**在它之上加对一段 FE 就能夺冠**。
- `.apply()` 换成向量化运算——写特征时顺手做的事。
- 公开榜下滑不等于没戏（本场冠军就是下滑中夺冠的）。

## 7. 出处

- 1st：意外夺冠与风险因子 FE：https://www.kaggle.com/competitions/playground-series-s3e3/discussion/380920
- 8th：常规线：https://www.kaggle.com/competitions/playground-series-s3e3/discussion/381052
- 性能纪律：Avoid .apply()：https://www.kaggle.com/competitions/playground-series-s3e3/discussion/379959
