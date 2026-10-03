# Playground Series S3E16 - 螃蟹年龄预测（MAE，与生成模型搏斗）

> 主题：tabular ｜ 子类：— ｜ 领域：生物测量（合成数据） ｜ 类别：Playground
> 截止：2023-06-12 ｜ 队伍数：1429 ｜ 机制：标准赛 ｜ 指标：MAE
> 数据来源：`intel/playground-series-s3e16/`（76 条主题索引 + 6 篇 write-up 正文）

## 1. 任务与数据

- 预测目标：螃蟹年龄（MAE）；合成数据 + 原数据 + 公开的生成模型/库（本场的独特资源）。
- 数据特性：存在大量随机性（1st 判断"部分数据偏随机"）→ 保险起见用稳健集成；测试集目标范围比训练集窄（无 >20 / <4 岁）。

## 2. 验证方案

- **让验证规模对齐测试集**（2nd 的核心技巧）：测试 5.6 万样本，5 折 → 每折需≈5.5 万；于是生成 20 万合成样本 + 7.4 万训练 = 27.4 万，折大小与测试集相当，**CV–LB 相关性显著改善**。
- 1st：CV 与 LB 都只信一半 → 双份"安全型"提交（互证）。

## 3. 模型家族

| 方案 | 使用者层次 | 关键点 | 出处 |
| --- | --- | --- | --- |
| 多样化模型平均（保险型）+ Optuna 权重实验 | 1st | 诚实复盘"乱但有效" | topic 416766 |
| 目标范围拟合 + 合成数据补折 + 4 模型集成 | 2nd | 首赛即亚军 | topic 416903 |
| 暴力集成 + 后处理 | 3rd | 公私榜错位应对 | topic 416783 |

## 4. 关键技巧

- **与生成模型直接对话**（1st 的探索线，非常规但启发大）：用生成库的缺失值填补与采样函数、把生成器载入 Transformers 取目标 token logits 当特征、甚至把生成器微调成序列分类器——其中微调方案事后被证明是其最优（1.33383，可惜未选）。
- **目标范围裁剪训练数据**（2nd 的最大增益）：测试无 >21/<3 岁的螃蟹 → 训练时裁掉极端年龄（留 1–2 岁余量），模型专注测试分布。
- 合成数据的目的不是"更多"而是"对齐折规模"：本例把 CV 与 LB 拉近。
- 1st 的诚实复盘值得保留：过程混乱 + 130 特征 + 多次换路，最终靠稳健平均兜底。

## 5. 可迁移性评估

- **可直接迁移**：验证折规模对齐测试集；按测试目标范围裁剪训练样本；生成模型/库可用时的"非常规挖掘"；稳健平均兜底策略。
- **需要前提**：生成模型或合成器可用（资源与算力）；目标范围先验可靠。
- **不建议照搬**：把生成器微调当通用路线（成本高、结论不确定）；训练范围裁剪过度（边界样本是信号）。

## 6. 对新手的关键启示

- **"验证集要与测试集同规模"** 是比调参更值钱的元技巧（2nd 靠它把 CV–LB 拉齐）。
- 测试集的范围先验可直接变成训练裁剪——分布对齐从数据侧做起。
- 数据疑似偏随机时，稳健平均比激进的权重搜索更可靠。

## 7. 轻读结论（2026-10 补）

**一句话**：本场数据由**可获取的生成模型**合成——逆向/调用生成器（补数据、域对齐）是最强路线；2nd 的两个最大增益是"**删掉测试域不可能出现的年龄**"和"**用生成器补 20 万行**"；1st 甚至把生成模型微调成序列分类器（1.33383，但他没敢信）。

- 1st（416766）：两份"安全"提交（简单平均 / Optuna 学权重 1.33566）；尝试过 200 万+ 合成行（增益小）、生成模型的缺失值填补与采样函数（"Age is"下一个词预测）、logits 取平均喂 Tabular/TabTransformer/CatBoost（一般）、**HF 微调成序列分类（自己最好的 1.33383，未入选）**；CatBoost 最稳。
- 2nd（416903）：**删掉 age>21 或 <3 的训练行（对齐测试域）**（最大增益）；用官方合成模型生成 ~20 万行并合成 ~27.4 万行训练集，5 折每折 ~5.5 万≈测试 5.6 万（提升 CV-LB 相关性）；Optuna + XGB/LGBM/CatBoost/HGBR；配置清单标注 `add_synthetics`/`drop_bigAges` 为"非常好"（图 1）。
- 5th（416769）：无预处理；**仅 4 个比率特征**；10 折 + 5 模型 + **LADRegression**（与 MAE 指标匹配）拿第 5。
- 11th：复盘"什么有效/什么无效"。
- 社区：round or not（37 票）、1.33708 特征工程（48 票）、最离奇相关性（21 票）。

**裁决**：先查生成器是否公开；按测试域裁剪训练数据；集成器损失对齐指标（MAE→LAD）；非主流强模型放第二提交对冲。

**悬案**：3rd/4th/6th–10th 方案缺失；1st 的 130 特征与 Optuna 细节未展开；生成模型库名未明确。

## 8. 图表证据

![2nd 的配置与逐项效果标注](../../intel/playground-series-s3e16/bodies/416903_img/01.png)

**图 1**（topic 416903）：`add_synthetics=True`、`drop_bigAges=True` 标注为"非常好"；standard scaler 优于 minmax；比率/体积类特征为负面。

## 9. 出处

- 1st：实验生成模型与安全集成：https://www.kaggle.com/competitions/playground-series-s3e16/discussion/416766
- 2nd：Open-Close 尝试与合成数据补折：https://www.kaggle.com/competitions/playground-series-s3e16/discussion/416903
  - 3rd：暴力集成与后处理：https://www.kaggle.com/competitions/playground-series-s3e16/discussion/416783
  - 5th（LAD 集成）：https://www.kaggle.com/competitions/playground-series-s3e16/discussion/416769
  - 11th 复盘：https://www.kaggle.com/competitions/playground-series-s3e16/discussion/416819
  - 特征工程 1.33708（48 票）：https://www.kaggle.com/competitions/playground-series-s3e16/discussion/415721
  - round or not（37 票）：https://www.kaggle.com/competitions/playground-series-s3e16/discussion/413971
- 轻读全本：`analysis/deep/playground-series-s3e16.md`（Tier B 轻读：对照矩阵/裁决/证据分级/悬案 + 1 图证）
