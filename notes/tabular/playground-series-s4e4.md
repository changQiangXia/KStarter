# Playground Series S4E4 - 鲍鱼年龄回归（MSLE，OpenFE 自动特征工程）

> 主题：tabular ｜ 子类：— ｜ 领域：生物测量（合成数据） ｜ 类别：Playground
> 截止：2024-04-30 ｜ 队伍数：2606 ｜ 机制：标准赛 ｜ 指标：MSLE（RMSLE）
> 数据来源：`intel/playground-series-s4e4/`（80 条主题索引 + 6 篇 write-up 正文）

## 1. 任务与数据

- 预测目标：鲍鱼年龄（环数）回归，RMSLE；合成数据 + 原数据；数据量大，洗牌较轻（5th 的观察）。
- 目标特性：离散取值的回归任务（合成自离散标签），催生了本场的"分类器 + 回归头"怪招。

## 2. 验证方案

- 主流 10 折；5th 实测 **15/20 折 > 5 折**（数据大、指标噪声小时可加深折数）。
- 2nd 的自动化数据审计：用 **AutoGluon 两样本判别 + Mann-Whitney U 检验**判断原数据是否存在分布偏移，以此决定是否并入原数据。
- 1st：原数据每折都用于训练、从不用于验证。

## 3. 模型家族

| 方案 | 使用者层次 | 关键点 | 出处 |
| --- | --- | --- | --- |
| 49 模型 + Nelder-Mead 加权（允许负权重） | 1st | OpenFE + 逐模型序列特征选择 | topic 499174 |
| 自动化工作流：两样本检验 + OpenFE + AutoGluon 选型 | 2nd | 为 AutoML Grand Prix 预演，意外拿亚军 | topic 499698 |
| 领域特征（表面积/失水/密度/BMI）+ 多模型 | 5th | 折数加深提升 | topic 499204 |

## 4. 关键技巧

- **OpenFE 自动特征生成 + 序列特征选择**（1st/2nd 的共同核心）：生成候选特征后用 SFS（逐个模型单独选约 20 个），代表特征如 `freq(Shell_weight)`、`(Whole_weight/Shucked_weight)`、`residual(Whole_weight)`、`log(...)`、`max(...)`——**自动 FE 在这种"特征可组合"的数据上收益巨大**。
- **RMSLE 的损失实现**：LGBM 自定义 MSLE / `gamma` 目标、XGB `reg:squaredlogerror`、其他模型 log1p→expm1。
- **负权重集成**：Nelder-Mead 在 OOF 上调权，最优解含负系数且和≈0.997，稳定优于非负归一化版本（"cheesy 但有效"）。
- **分类器 + 回归头**（社区怪招）：XGB 分类目标多类 softprob + softmax 回归头，单模 CV 一般但被优化器选入——离散目标可能有隐藏收益（作者也不完全理解原因）。
- 2nd 的工作流化审计（两样本检验判原数据）+ AutoGluon 特征剪枝。

## 5. 可迁移性评估

- **可直接迁移**：OpenFE/SFS 自动特征工程流程；两样本检验决定外部数据；RMSLE 的四种正确写法；负权重 Nelder-Mead 集成；深折在小噪声指标下的增益。
- **需要前提**：自动 FE 工具链（OpenFE）与算力；OOF 完整存档。
- **不建议照搬**：把"分类器+回归头"当通用技巧（机理不明）；不审计直接并入原数据。

## 6. 对新手的关键启示

- 特征可以自动生成：OpenFE + 代理模型剪枝，是"想不到好特征"时的系统解。
- 集成权重不必非负；在 OOF 上优化并在提交层面验证，比"看起来合理"更重要。
- 折数也是超参：数据大且噪声小时，加深折数常是免费的稳健性提升。

## 7. 出处

- 1st：OpenFE + Nelder-Mead 负权重集成：https://www.kaggle.com/competitions/playground-series-s4e4/discussion/499174
- 2nd：自动两样本检验 + 自动 FE 工作流：https://www.kaggle.com/competitions/playground-series-s4e4/discussion/499698
- 5th：领域特征与折数经验：https://www.kaggle.com/competitions/playground-series-s4e4/discussion/499204
