# Leash Bio - Predict New Medicines with BELKA

> 主题：science ｜ 子类：— ｜ 领域：化学/药物发现 ｜ 类别：Featured
> 截止：2024-06-11 ｜ 队伍数：1200+ ｜ 机制：代码赛 ｜ 指标：shared AP（平均精度）
> 数据来源：`intel/leash-BELKA/`（120 条主题索引 + 8 篇 write-up 正文）

## 1. 任务与数据

- **预测目标**：预测小分子与三种靶蛋白的结合活性；分子由**组合式构建块（building block）** 拼装而成。
- **数据形态**：SMILES / 构建块 ID / 3D 构象等多表示；训练数据为实验测得的活性。
- **构造陷阱**：
  - 分子由共享构建块组合产生 → **同一构建块在不同分子间高度重复**，随机切分会导致严重泄漏。
  - 因此出现了 **shared / non-shared** 两套评估视角，必须分别对待。

## 2. 验证方案

| 方案 | 使用者 | 说明 |
| --- | --- | --- |
| 分层 K 折（20 折） | 11th | 关注构建块层面的泄漏 |
| shared / non-shared 分组评估 | 2nd/13th | 对含共享与非共享构建块的分子用不同方案 |
| 提交预算管理 | 2nd/13th | 明确记录"用完 480 次提交" |

## 3. 方案谱系

| 方案 | 名次 | 关键点 |
| --- | --- | --- |
| 多表示 + 多模型集成 | 1st | CNN + 图模型 + 树模型，多表示（SMILES/指纹/构建块） |
| **仅用构建块 ID 的 Embedding + MLP** | 11th 的发现 | 该模型 shared AP 达 65.5，**超过不看构建块含义的 SMILES+CNN1d** —— 说明组合结构本身含大量信号 |
| 按共享/非共享分支建模 + CNN/GBDT/GNN 集成 | 2nd / 13th | 针对性处理两类分子 |
| 5th / 14th | 集成与工程 | 14th 的标题"All We Need is Frequent Checkpointing"提示**长时训练的断点续训工程**很关键 |

## 4. 关键技巧

- **构建块 ID 本身就是强特征**：不要只盯着分子字符串表示。
- **多表示融合**：SMILES 序列、分子指纹、构建块、3D 构象各自建模型再融合。
- **自监督预训练（SSL）**：利用大规模未标注分子（11th）。
- **工程可用性**：频繁 checkpoint 应对训练中断/时限。
- **提交预算**：本场提交次数有限，需要规划实验节奏。

## 5. 可迁移性评估

- **可直接迁移**：
  - **检查数据的组合式结构**（构建块/模板/前缀）——往往存在强信号与泄漏风险。
  - 多表示融合是分子/序列任务的通用手段。
  - 长时训练的 checkpoint 与恢复机制。
- **需要前提**：
  - 需要化学工具链（RDKit、GNN 框架）与 3D 构象生成。
- **不建议照搬**：
  - 随机切分（会造成构建块层面的泄漏）。

## 6. 对新手的关键启示

1. **先分析数据的生成机制**（组合式？模板式？），这决定了验证与特征。
2. **最简单的表示（ID 嵌入）可能出乎意料地强**，先试再上复杂模型。
3. **工程细节（checkpoint、提交预算）在真实赛程里会直接影响名次**。

## 7. 轻读结论（2026-10 补）

**一句话**：DEL 结合预测的三大要点——**共享/非共享构建块必须分开打**、**预训练任务（MLM→ECFP 预测）比模型结构重要**、**验证要高频（0.01 epoch）且按构建块切分**。

- 1st（85 票）：4 层 8 头/dim32/43 token 的浅模型 + **两阶段自训预训练（MLM → SMILES→ECFP）**，把 train+test+外部数据全用于 MLM；留出 3% 构建块（~900 万样本）做验证；无效清单：复杂分词、>6 层、多输入、ZINC 预训练、自定义损失。
- 14th（61 票）：共享/非共享分开；非共享"一个 epoch 内就过拟合"→ **每 0.01 epoch 存点**；CV 按 BB1/BB2/BB3 切 5 折；ChemBERTa-77M-MTR；11 seed × 2 折 → 19 模型集成。
- 2nd 公榜/13th 私榜：共享块用 CNN+XGB+LGBM+GNN 逐蛋白加权；非共享块用**排名集成**（消除尺度差）；两份提交 pub 0.488/0.529，priv 0.275/0.277。
- 5th：**字符分词 + 学习式 CNN 嵌入**（优于 BPE/atom 系）；CNN1d+Transformer+Mamba 集成；CNN1d 用高 eps/低 momentum 抗 BN 不稳；每网络用不同折换多样性。
- 事件：**指标中途变更公告（68 票）**；训练集瘦身帖（90 票）。

**裁决**：先按"构建块是否共享"分层，再谈模型；表示学习靠自监督目标设计；大样本快速过拟合时验证频率是超参；指标变更后必须重估全部历史结论。

**悬案**：3rd–13th 方案缺失；非共享部分公榜-私榜巨差（0.529→0.277）机制未解释；1st 权重未完整恢复。

## 8. 图表证据

![2nd 的非共享块 ChemBERTa 模型](../../intel/leash-BELKA/bodies/519133_img/02.png)

**图 1**（topic 519133）：ChemBERTa 两个变体（TabNet 版 / 64 维 FC 版）+ MLP Block 内部结构，用于非共享块的排名集成。

## 9. 出处

- 讨论区索引：`intel/leash-BELKA/topics.md`（120 条）
- 已收录 write-up（8 篇）：
  - 1st（85 票）：https://www.kaggle.com/competitions/leash-BELKA/discussion/519020
  - 2nd public / 13th private（68 票）：https://www.kaggle.com/competitions/leash-BELKA/discussion/519133
  - 14th（61 票）：https://www.kaggle.com/competitions/leash-BELKA/discussion/518951
  - 11th（33 票）：https://www.kaggle.com/competitions/leash-BELKA/discussion/518993
  - 5th（34 票）：https://www.kaggle.com/competitions/leash-BELKA/discussion/521894
  - 88th GNN+域适应（42 票）：https://www.kaggle.com/competitions/leash-BELKA/discussion/519135
  - 训练集瘦身（90 票）：https://www.kaggle.com/competitions/leash-BELKA/discussion/491472
  - 指标变更公告（68 票）：https://www.kaggle.com/competitions/leash-BELKA/discussion/503232
- 轻读全本：`analysis/deep/leash-BELKA.md`（Tier B 轻读：对照矩阵/裁决/证据分级/悬案 + 1 图证）
