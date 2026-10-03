# Playground Series S4E8 - 蘑菇毒性分类（Matthews 相关系数）

> 主题：tabular ｜ 子类：— ｜ 领域：生物（合成数据） ｜ 类别：Playground
> 截止：2024-08-31 ｜ 队伍数：2422 ｜ 机制：标准赛 ｜ 指标：Matthews Correlation Coefficient（MCC）
> 数据来源：`intel/playground-series-s4e8/`（80 条主题索引 + 6 篇 write-up 正文）

## 1. 任务与数据

- 预测目标：蘑菇是否有毒（二分类 MCC）；约 300 万行、变量数多、类别特征为主；部分列缺失率高。
- 关键线索：社区有人给出了**原数据集的精确解**——该解的"有毒概率"可作为新特征注入竞赛数据（1st 采纳）。

## 2. 验证方案

- 1st：近 80 个 OOF、最终用 72 个；AG 的 CV 策略自定防泄漏；Ridge 作主力集成器（速度+分数最平衡），Hill Climbing 在 >60 模型后需 2 小时但仍用到最后。
- 1st 的自省：赛后回看有 31 份提交 ≥ 私榜第二名分数（最早一份距截止两周）——**选择比生成更难**。

## 3. 模型家族

| 方案 | 使用者层次 | 关键点 | 出处 |
| --- | --- | --- | --- |
| 72 OOF + AutoGluon/Ridge 双路线 | 1st | 原数据精确解概率当特征 | topic 531823 |
| #4 | 4th | AGP 与主赛双线 | topic 531343 |
| AutoML Grand Prix 冠亚季（AutoGluon 分布式等） | 社区 | 自动化工作流 | topic 523656 |

## 4. 关键技巧

- **精确解特征**：把原数据精确解的概率作为特征（或至少作为多样性来源）——"原数据信号残留"的代理（1st）。
- **AutoGluon 的深挖实验**（1st）：发现 AG 内部 XGB/CatBoost 最弱 → 剔除不降分且省一半时间；最强组合几乎总是 GBM+XT（ExtraTrees）；把单模型用 AG 逐个跑再自集成 +0.0001；**用 Hill Climbing 选 8 个 OOF 喂给 AG** 得最优。
- **PPS（Predictive Power Score）**：类别特征与缺失多时的特征重要性工具（MI/相关系数失效时用它）；**高缺失率特征仍有显著价值**（别删）。
- "自信分歧覆盖"：若另一模型的预测概率 >0.99 则覆盖自己的预测——公开榜有涨分但私榜缩水，需谨慎。
- 工程细节：LGBM `num_threads` 按核心数设置提速；Kaggle 12 小时限制被反复击穿 → 云平台 32 CPU 替代方案。

## 5. 可迁移性评估

- **可直接迁移**：精确解/原数据信号的特征化；AG 内部模型解剖与裁剪；HC 选 OOF 再喂 AG 的两级流程；PPS 特征重要性；缺失率高的特征保留策略。
- **需要前提**：AG 与长时运行（12 小时限制要规避）；大内存环境。
- **不建议照搬**：自信分歧覆盖（私榜缩水）；不看 CV 的盲 blend（1st 也承认自己偶尔犯）。

## 6. 对新手的关键启示

- 高缺失特征别急着删：先看价值（PPS/单特征模型）。
- AutoML 也能"解剖"：找出内部弱模型剔除、给强模型更多时间，是低成本优化。
- 本场与 S4E9/S4E11 构成同一个教训：**生成易、选择难**——多做提交档案与选择纪律。

## 7. 轻读结论（2026-10 补）

**一句话**：近确定性任务（MCC~0.9855）拼的是**数据清洗 + 原始信号特征 + 巨量 OOF 集成 + 第 5 位小数的提交工程**。

- 主赛 1st（531823）：~80 OOF 用 72；Ridge/爬山/AutoGluon；把原始数据精确解概率当特征；31 个 ≥0.98512 提交，最佳私 0.98517；CV-LB 差 0.0001–0.0002；"盲 blend 也能在百万数据上过拟合"（shakeup）。
- AGP 1st（523656）：AutoGluon 分布式（SLURM+Ray 1000 CPU）+ TabRepo 组合 + 16 折 + log loss 早停 + 100 次后处理 + **舍入精度 6→8 位 tiebreak** → 0.98533（图 1）。
- 社区：高缺失特征仍有价值（69 票）；原始数据集帖（49 票）。

**裁决**：查原始数据源；巨量 OOF + 简单 meta；集成器精度/提交选择是独立竞争力；以 CV 为锚、盲 blend 只作保险。

**悬案**：2nd/3rd 未收录；KAN 细节未细读。

## 8. 图表证据

![AGP 1st 总览](../../intel/playground-series-s4e8/bodies/523656_img/01.jpg)

**图 1**（topic 523656）：清洗 → 默认/定制 AutoGluon（192 vCPU vs 1000 CPU）→ 贪婪后处理集成 → 提交。

## 9. 出处

- 1st：72 OOF 与 AG 深挖：https://www.kaggle.com/competitions/playground-series-s4e8/discussion/531823
- #4：https://www.kaggle.com/competitions/playground-series-s4e8/discussion/531343
- 高缺失特征仍有价值（PPS）：https://www.kaggle.com/competitions/playground-series-s4e8/discussion/523474
- 轻读全本：`analysis/deep/playground-series-s4e8.md`（Tier B 轻读：对照矩阵/裁决/证据分级/悬案 + 1 图证）
