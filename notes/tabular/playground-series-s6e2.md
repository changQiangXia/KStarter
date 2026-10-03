# Playground Series S6E2 - 心脏病预测

> 主题：tabular ｜ 子类：— ｜ 领域：医疗（合成数据） ｜ 类别：Playground
> 截止：2026-02-28 ｜ 队伍数：4370 ｜ 机制：标准赛 ｜ 指标：ROC AUC
> 数据来源：`intel/playground-series-s6e2/`（80 条主题索引 + 6 篇 write-up 正文）

## 1. 任务与数据

- 预测目标：基于 13 个临床特征预测心脏病存在与否（二分类，AUC）。
- 数据形态：由深度学习模型基于真实心脏病数据集生成的**合成数据**；原始数据集可获取，可作外部数据。
- 关键特性：信号接近线性、特征间交互极少——多个高分解法独立发现 GBDT 低深度（depth=2/3）最好、FM 不做特征工程也几乎打平、逻辑回归骨架很强。这与多数 Playground 的"交互丰富"画像相反。
- 已知陷阱：合成生成噪声惩罚过度工程；赛程中后期公开 notebook 集体过拟合公开榜，前 300 名私榜大洗牌。

## 2. 验证方案

- 主流 5/10 折 StratifiedKFold + 固定 seed；4th 额外跟踪 OOF–Public LB gap（本场健康值约 0.00185，gap 恶化即丢弃实验）。
- 1st 的 CV 纪律：**"Trust the CV–LB relation, not the best CV"**——CV 超过约 0.95578 后，CV 提升不再可靠兑现为 LB 提升（疑似 split overfitting），最终从 CV 0.95578–0.95580 区间选提交，放弃更高的 0.955865。
- 泄漏教训（69th 赛后复盘）：目标编码必须在 KFold 内嵌套完成；fold 外的 TE + 858 特征使 CV 虚高，移除该模型后私榜反而从前 100 边缘升到前 20。
- 理论讨论（1st）：嵌套 K-fold 是唯一完全无泄漏方案，但管理约 150 个 OOF 时成本过高；实践替代 = 固定折 + 限制元模型复杂度 + 监控 CV–LB 一致性。

## 3. 模型家族

| 方案 | 使用者层次 | 关键点 | 出处 |
| --- | --- | --- | --- |
| 多特征表示 × 全模型池（~150 个 OOF） | 1st | binning/数字位/全类别化/频率/gplearn/原数据统计/DVAE → Optuna 选子集 → Ridge | topic 679376 |
| RealMLP / TabM（周期嵌入 NN） | 3rd、22nd | 数值周期嵌入；NN 与 GBDT 打平甚至更强 | topic 679428、679389 |
| GBDT stumps（depth=2）+ one-hot | 4th、69th | 低深度隔离类别水平、抗合成噪声 | topic 679414、679367 |
| 逻辑回归 + 成对/三元 TE + logit 多项式 | 69th | 线性骨架精确控制交互度 | topic 679367 |
| 秩集成（rank averaging） | 3rd、4th、69th | 抗概率校准漂移与私榜抖动 | topic 679428 |

## 4. 关键技巧

- **特征**：追求"多表示"而非单一最优特征集（分箱 ×3 种、数字位、全类别化、频率编码、GP 特征、原数据 WoE/熵/TE、DVAE 隐表示）；原数据用于 TE/统计注入而非直接拼入 NN（会"搞糊涂"网络）。
- **训练**：全量重训 20 seed 平均、n_estimators = 1.25×CV 最优迭代（1st）；RealMLP 内部 8 子模型平均（4th）；周期嵌入（sine/cosine, dim=8）比线性嵌入强约 50 倍增益（topic 671783 的对照：+0.0013 vs +0.000027）。
- **集成**：Optuna 对 OOF 子集搜索（2500 trials，约 1/10 的 OOF 被稳定选中）→ Ridge 元模型；秩平均替代概率平均；树模型权重手动封顶 35%（4th 的"Purity > Diversity"）。
- **防抖**：以真实提交研究 CV–LB 轨迹分段；不追公开榜（榜被公开 notebook 污染，"Trust CV"成为社区共识）。

## 5. 可迁移性评估

- **可直接迁移**：多特征表示制造多样性；Optuna 子集选择 + Ridge 堆叠；秩平均；原数据统计注入；CV–LB 关系分段信任法；TE 嵌套折内。
- **需要前提**：合成数据且能拿到原始数据；~150 OOF 的算力；RealMLP/TabM 等现代 tabular DL 工具链。
- **不建议照搬**：无选择地平均全部 OOF（伤分）；深层 GBDT/高阶交互/非线性堆叠（本场验证失败）；盲信公开榜高分笔记本。

## 6. 对新手的关键启示

- "最好的 CV"不等于"最好的提交"：观察自己提交的 CV–LB 轨迹，找到可信区间再定稿。
- 集成 = 多样性生成 + 纪律性选择 + 简单稳健的组合；Ridge/秩平均往往优于更"聪明"的元模型。
- 现代 tabular 深度学习（周期嵌入）已能打平 GBDT——工具箱里加上 RealMLP/TabM。
- 赛后复盘（如 69th 的 TE 泄漏自检）是最被低估的提分环节。

## 7. 出处

- 1st place：Diversity, Selection, and Trusting the CV–LB Relation：https://www.kaggle.com/competitions/playground-series-s6e2/discussion/679376
- 3rd place：多特征集 + 秩集成 + 爬山：https://www.kaggle.com/competitions/playground-series-s6e2/discussion/679428
- 4th place：Less is More（stumps + 秩平均）：https://www.kaggle.com/competitions/playground-series-s6e2/discussion/679414
- 69th place：ChatGPT 协作 + 赛后泄漏复盘：https://www.kaggle.com/competitions/playground-series-s6e2/discussion/679367
- 22nd place：NN 再次优于 GBM 的论证：https://www.kaggle.com/competitions/playground-series-s6e2/discussion/679389
- 数值嵌入实验：线性 vs 周期：https://www.kaggle.com/competitions/playground-series-s6e2/discussion/671783
