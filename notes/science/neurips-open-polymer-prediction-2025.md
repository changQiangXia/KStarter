# NeurIPS - Open Polymer Prediction 2025

> 主题：science ｜ 子类：— ｜ 领域：材料/化学 ｜ 类别：Featured
> 截止：2025-09-15 ｜ 队伍数：2240 ｜ 机制：代码赛 ｜ 指标：多目标回归（5 个聚合物性质）
> 数据来源：`intel/neurips-open-polymer-prediction-2025/`（120 条主题索引 + 8 篇 write-up 正文）

## 1. 任务与数据

- **预测目标**：由聚合物 SMILES 预测 5 个性质（含玻璃化转变温度 Tg 等）。
- **数据形态**：分子序列（SMILES）+ 多目标回归；训练样本有限，**允许使用外部数据**。
- **构造陷阱**：
  - **外部数据与官方数据的标签存在系统性偏移**（8th 发现 POINT2 数据的 Tg 整体低约 20°C），不校正会引入偏差。
  - 测试集与训练集存在分布差异，冠军明确指出 Tg 需要**后处理校正**。

## 2. 验证方案

| 方案 | 使用者 | 说明 |
| --- | --- | --- |
| 多目标分别验证 | 1st | 按性质分别建模与评估（非多任务） |
| 外部数据交集对照 | 8th | 用同一 SMILES 在两份数据中的差值估计系统偏移 |
| 公开基线起步 | 社区 | "Jump-starting" 帖提供数据与入门材料 |

## 3. 方案谱系

| 方案 | 名次 | 关键点 |
| --- | --- | --- |
| BERT + AutoGluon + Uni-Mol 集成 | 1st | 两个独特贡献：**Tg 预测的后处理分布校正** + **在 PI1M 伪标签子集上预训练 BERT**；另有外部数据与表格特征技巧 |
| GATv2Conv 图神经网络融合 | 3rd | 新手参赛者：Uni-Mol 本地算力不够，转向 GNN；强调数据预处理的重要性 |
| 外部数据（POINT2）+ 偏移校正 | 8th | 发现外部数据整体偏移（Density -0.118 等），校正后才可用 |
| 多模型集成 | 2nd / 20th | 常规集成路线 |

## 4. 关键技巧

- **外部数据必须做偏移校正**：同一分子在两份数据中的标签差异是估计系统误差的直接证据。
- **伪标签预训练**：在无标签的大规模分子库（PI1M）上先用伪标签预训练 BERT，再迁移到目标任务。
- **按性质分别建模**：5 个目标各自独立建模，而不是多任务共享头。
- **图神经网络 vs 预训练分子模型**：算力有限时 GATv2 等 GNN 是可行的替代路线。
- **后处理**：针对已知的分布差异对特定性质做校正。

## 5. 可迁移性评估

- **可直接迁移**：
  - **整合外部数据前先做"重叠样本差异分析"**——这是任何跨数据源合并的必备步骤。
  - 伪标签预训练（无标签大规模领域数据 → 目标任务）。
  - 多目标按性质分别建模。
- **需要前提**：
  - 需要分子建模工具链（RDKit、Uni-Mol、GNN 框架）。
  - 外部数据的授权与质量可控。
- **不建议照搬**：
  - 直接混用外部数据而不检查偏移。
  - 直接照搬重型预训练分子模型的流程（本地算力可能不足，3rd 的教训）。

## 6. 对新手的关键启示

1. **外部数据不是免费午餐**：先做重叠样本比对，量出偏移再决定怎么用。
2. **按目标分别建模**通常比强行多任务更稳。
3. **算力不够就用轻量图网络**，不必硬上预训练大模型。
4. **后处理校正分布差异**是"数据理解"的直接变现。

## 7. 出处

- 讨论区索引：`intel/neurips-open-polymer-prediction-2025/topics.md`（120 条）
- 已收录 write-up（8 篇）：
  - 1st（116 票）：https://www.kaggle.com/competitions/neurips-open-polymer-prediction-2025/discussion/607947
  - 2nd（17 票）：https://www.kaggle.com/competitions/neurips-open-polymer-prediction-2025/discussion/608984
  - 3rd（23 票）：https://www.kaggle.com/competitions/neurips-open-polymer-prediction-2025/discussion/607991
  - 8th（36 票）：https://www.kaggle.com/competitions/neurips-open-polymer-prediction-2025/discussion/608069
  - 20th（32 票）：https://www.kaggle.com/competitions/neurips-open-polymer-prediction-2025/discussion/607803
