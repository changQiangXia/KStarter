# Playground Series S5E10 - 道路事故风险预测

> 主题：tabular ｜ 子类：— ｜ 领域：交通（合成数据） ｜ 类别：Playground
> 截止：2025-10-31 ｜ 队伍数：4082 ｜ 机制：标准赛 ｜ 指标：MSE（RMSE）
> 数据来源：`intel/playground-series-s5e10/`（75 条主题索引 + 6 篇 write-up 正文）

## 1. 任务与数据

- 预测目标：路段事故风险（回归，RMSE）；60% 训练 / 40% 测试的 Playground 划分。
- 竞争格局：**史上最挤的分数带之一**——前 4 名同为 0.05563，其后约 200 人同为 0.05564；名次主要由第 5–6 位小数决定。
- 原数据生成函数已知（规则+系数），Lasso 的系数可直接对应目标公式——线性基线异常强（10×10 重复 K 折约 2 分钟即 0.058 级）。

## 2. 验证方案

- 主流 5–10 折；1st 用 10×10 重复 K 折做模型间比较；3rd 验证发现"7 折 + 按目标分层"带来小幅稳定增益。
- 3rd 的全流程：L1 五基模（TabM、TabM 残差、XGB、LGBM、MLP）→ L2 堆叠 NN → L3 YDF 元模型（并入原始特征）→ L4 最终集成。
- 1st 的 12 份候选提交在前 5 位小数全部相同——**分数带内的选择几乎靠纪律与运气**，保存多份候选至关重要。

## 3. 模型家族

| 方案 | 使用者层次 | 关键点 | 出处 |
| --- | --- | --- | --- |
| GP 特征 + 多 NN 集成 + CatBoost 基线式二级学习 → 爬山 | 1st | Lasso 作探针；GP 特征只在集成阶段有用 | topic 614086 |
| 100 折重训的 2 类模型（XGB/TabM）互栈 | 5th | 一切模型都重训 100 折以便同折互栈 | topic 614079 |
| 四级堆叠（含 YDF 元模型） | 3rd | 层数多但每层简单 | topic 614114 |

## 4. 关键技巧

- **Lasso/SGD 当探针**：快速拟合 + 读系数，直接对照已知生成公式验证特征方向（1st 的 EDA 级用法）。
- **GP（遗传编程）特征**：单独没用、加到单模没用，但在**集成阶段**给 11 个 GP 特征换来 0.00001 增益——与朴素公式复现不同，有用的是"能带来多样性的 GP 特征"。
- **CatBoost 作二级学习器**：把一级模型的预测当 baseline 再学残差（比手工残差更自动），连 CatBoost 自己的预测也能被再次提升（本场 + 0.00002 级）。
- **100 折互栈**（5th）：统一所有模型为 100 折，NN 多吃数据 + 同折可栈，收益稳定。
- 极挤分数带中，"2 段集成 + 爬山最后一步"是常见定稿结构。

## 5. 可迁移性评估

- **可直接迁移**：Lasso 探针；集成阶段才引入的多样性特征；CatBoost baseline 二次学习；同折重训（100 折）互栈；多候选提交。
- **需要前提**：回归任务且原生成公式可近似；算力允许 100 折（可降为 20–50 折）。
- **不建议照搬**：指望 GP 复现公式本身带来增益（它带来的是多样性而非精度）；在 5 位小数分数带里迷信单次 CV 差异。

## 6. 对新手的关键启示

- 先跑 2 分钟的高正则线性模型：若它已接近榜内分数，说明任务信号以线性/已知公式为主，重注押在多样性而非花式建模。
- "特征在单模无效、在集成有效"很常见——别急着删掉备用特征表示。
- 分数带极挤时，模型档案管理（每个实验的 OOF/权重/提交文件）比再压 1e-5 更重要。

## 7. 轻读结论（2026-10 补）

**一句话**：分数饱和到第 5 位小数（前 4 同分 0.05563、其后 ~200 队同分 0.05564）——可行增益只有 1e-5 级，且来自**改变误差结构**：残差提升、GP 特征、以强模型为 baseline 的二次集成、100 折/伪标签、元特征精选。

- 1st（614086）：多表示 × 多模型族；**Lasso 反推出生成公式**；**11 个 GP 特征在集成阶段 +0.00001**；**CatBoost 以 Keras 集成为 baseline（自动残差提升）+0.00002**；最后二级爬山；前 12 个提交 5 位小数相同。
- 5th（614079）：只造 XGB+TabM 两族的变体；**100 折**训练 TabM/XGB 并做 stacking；伪标签重训；一份提交与最佳公开 notebook 50/50。
- 8th（614207）：XGB（残差版，5–55 折）+ TabM×3 + GBM/NN/AutoGluon；**元特征去重（|ρ|>0.9995）+ Greedy NNLS/LassoCV 精选到 4–6 列**。
- 14th（614089）：70+ 个 HC 变体；更低 CV 来自含负权重的激进 HC，但最终选保守版——"更低 CV 不一定更好"。
- 公共起点：**XGB Boosting over Residuals（67 票）**。

**裁决**：饱和赛优先"改误差结构"而非加模型；合成数据先逆向生成函数；提交选择按过拟合风险而非最低 CV；NN 多折/多 seed 重训是高性价比稳定性来源。

**悬案**：2nd–4th/6th–7th/9th–13th 方案缺失；GP 特征公式未完整给出；"高值被系统性低估"未细读。

## 8. 图表证据

![1st 的集成流程图](../../intel/playground-series-s5e10/bodies/614086_img/01.png)

**图 1**（topic 614086）：五种表示 → 六族模型 → 三级一级集成（含"CatB ensemble with baseline"红色节点吸收 GP 特征）→ 爬山二级集成。

## 9. 出处

- 1st：GP 特征与多层集成：https://www.kaggle.com/competitions/playground-series-s5e10/discussion/614086
- 5th：One Hundred Folds!：https://www.kaggle.com/competitions/playground-series-s5e10/discussion/614079
  - 3rd：从基模到四级堆叠：https://www.kaggle.com/competitions/playground-series-s5e10/discussion/614114
  - 8th（少而精 + 元特征精选）：https://www.kaggle.com/competitions/playground-series-s5e10/discussion/614207
  - 14th（HC 保守 vs 激进）：https://www.kaggle.com/competitions/playground-series-s5e10/discussion/614089
  - XGB 残差提升（67 票）：https://www.kaggle.com/competitions/playground-series-s5e10/discussion/610828
- 轻读全本：`analysis/deep/playground-series-s5e10.md`（Tier B 轻读：对照矩阵/裁决/证据分级/悬案 + 1 图证）
