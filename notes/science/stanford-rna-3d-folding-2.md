# Stanford RNA 3D Folding Part 2

> 主题：science ｜ 子类：— ｜ 领域：结构生物学 ｜ 类别：Featured
> 截止：2025-06-30 ｜ 队伍数：1200+ ｜ 机制：代码赛 ｜ 指标：结构相似度评分（TM-score 类）
> 数据来源：`intel/stanford-rna-3d-folding-2/`（80 条主题索引 + 6 篇 write-up 正文）

## 1. 任务与数据

- **预测目标**：由 RNA 序列预测其三级结构（3D 坐标），按结构相似度评分。
- **数据形态**：序列 + 实验解析结构；数据量小、结构标注昂贵。
- **构造陷阱**：
  - **评测集本身在变化**（社区帖 "The moving target that rendered RNA 3D Pt2 competition..."），说明数据/评测存在动态调整。
  - 蛋白质/RNA 结构预测高度依赖**同源模板**与**预训练结构模型**，是否允许使用预训练权重影响极大。
  - 本地算力是硬约束（本场多数方案在 2×T4 上完成）。

## 2. 验证方案

| 方案 | 使用者 | 说明 |
| --- | --- | --- |
| 本地验证 + 公开榜双目标优化 | 8th | 明确写"在 GPU 配额允许下，同时优化验证与公开榜" |
| 多版本提交对照 | 8th | 两个 notebook 仅计算调度与随机种子不同，用于观察方差 |
| 结构相似度指标的本地复现 | 多数 | 必须本地实现评分函数 |

## 3. 方案谱系

| 方案 | 名次 | 关键点 |
| --- | --- | --- |
| 五模型集成 | 1st | 见讨论区 |
| **BPP-Protenix**：把碱基配对概率（BPP）作为特征融入 Protenix | 2nd（公开第 1） | 用领域特征增强通用结构预测模型 |
| 模板建模（TBM）+ Protenix | 8th | 只使用 Kaggle 资源（2×T4）；两版本仅调度与种子不同 |

## 4. 关键技巧

- **领域特征注入**：碱基配对概率（BPP）这类领域先验能显著增强通用结构模型（2nd）。
- **模板建模（TBM）**：有同源模板时优先用，成本低、精度稳（8th）。
- **算力适配**：在 2×T4 上完成训练与推理，需要精简模型与调度优化。
- **多样性来源**：不同的计算调度与随机种子也能构成集成多样性（8th 的两版本）。
- **对评测变化的敏感度**：本场评测集有变动，需要关注主办方公告并快速重跑。

## 5. 可迁移性评估

- **可直接迁移**：
  - **领域先验特征 + 通用大模型**的组合方式（BPP 入模是范例）。
  - 模板/检索式方法作为低成本强基线。
  - 用调度/种子差异构造集成多样性。
- **需要前提**：
  - 需要结构生物学工具链（Protenix、模板库）与结构解析工具。
- **不建议照搬**：
  - 忽视本地算力限制直接照搬大模型全流程（会在推理阶段超时）。

## 6. 对新手的关键启示

1. **科学结构预测 = 领域特征 + 通用模型**，两者缺一不可。
2. **算力有限时，模板/检索方法优先**（成本低且常接近最优）。
3. **评测集会变**：关注主办方公告，方案要能快速重跑。

## 7. 轻读结论（2026-10 补）

**一句话**：每个目标交 5 个预测取最优 → 真正的目标是**"候选集合的多样性与覆盖率"**；本场的通用配方 = TBM（模板，靠检索/排序）+ AlphaFold3 系（Protenix/Boltz2）+ RNAPro（扩散精化），按**序列长度与显存预算**分配槽位。

- 1st（689386）：**长度自适应分配**——<250 nt：Boltz2×2+RNAPro+Protenix+DRFold2；250–999：TBM+Boltz2+RNAPro×2+Boltz2；**≥1000：TBM×3+Protenix×2**（RNAPro/Boltz2 会 OOM）；TBM 用模板池全局比对 + 指数加权采样 + 缺口插值/外推 + 键长键角与自避让后处理；最终 priv 0.49669。
- 2nd（691133，公榜第 1）：**把 BPP（碱基配对概率）矩阵线性嵌入 AlphaFold3 Pairformer 的 z_init**（1→128），槽位 = TBM+RNAPro×2+BPP-Protenix×2；自称"几乎唯一改结构的方案"。
- 3rd（689697）：**LightGBM 预测 query-template TM-score**（19.8 万对；含 RNA 相似度、PubMedBERT 文本相似度、BLOSUM62 蛋白相似度、DNA、配体 Tanimoto、链数特征）选 top-2 模板；槽位 TBM×2+Protenix×2+RNAPro；双 T4 并行。
- 6th（686777）：TBM 造多样假设 + Protenix(no-MSA) → **把两者输出当模板喂给 RNAPro（交叉授粉）**；>1000 nt 直接 TBM×5。
- 8th（687113）：TBM 加 ViennaRNA 二级结构 + 匈牙利算法做链匹配；Protenix token 512→768；缺失链用其他链缩放坐标填充。

**裁决**：多预测取最优的赛制要按"覆盖率"设计提交；模板检索/排序是独立的可优化模块；2×T4 的运行时约束会直接改写方案结构；BPP 类生物先验的跨任务迁移是少见的架构增益点。

**悬案**：4th/5th/7th/10th 方案缺失；BPP-Protenix 无消融；"移动靶"争议无官方结论；本场仅 1 张归档图。

## 8. 图表证据

![RNAPro 推理管线与对比](../../intel/stanford-rna-3d-folding-2/bodies/668412_img/01.png)

**图 1**（topic 668412）：RNAPro = 序列/MSA/RNA LM/模板 → 48 层 Pairformer → 扩散模块 → 结构；柱状图显示其私榜明显优于 AlphaFold3/Eigen/odal/TBM 等基线（且 RNA-only 子集同样领先）。

## 9. 出处

- 讨论区索引：`intel/stanford-rna-3d-folding-2/topics.md`（80 条）
- 已收录 write-up（6 篇）：
  - 1st（25 票）：https://www.kaggle.com/competitions/stanford-rna-3d-folding-2/discussion/689386
  - 2nd（21 票）：https://www.kaggle.com/competitions/stanford-rna-3d-folding-2/discussion/691133
  - 8th（16 票）：https://www.kaggle.com/competitions/stanford-rna-3d-folding-2/discussion/687113
  - 评测集变动讨论（15 票）：https://www.kaggle.com/competitions/stanford-rna-3d-folding-2/discussion/686651
  - 2nd BPP-Protenix（21 票）：https://www.kaggle.com/competitions/stanford-rna-3d-folding-2/discussion/691133
  - 3rd TM-score 模板排序（16 票）：https://www.kaggle.com/competitions/stanford-rna-3d-folding-2/discussion/689697
  - 6th 交叉授粉（23 票）：https://www.kaggle.com/competitions/stanford-rna-3d-folding-2/discussion/686777
  - RNAPro 管线（26 票）：https://www.kaggle.com/competitions/stanford-rna-3d-folding-2/discussion/668412
- 轻读全本：`analysis/deep/stanford-rna-3d-folding-2.md`（Tier B 轻读：对照矩阵/裁决/证据分级/悬案 + 1 图证）
