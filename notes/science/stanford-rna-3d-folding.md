# Stanford RNA 3D Folding（Part 1）

> 主题：science ｜ 子类：— ｜ 领域：结构生物学 ｜ 类别：Featured
> 截止：2024-XX-XX ｜ 队伍数：1800+ ｜ 机制：代码赛 ｜ 指标：结构相似度（TM-score 类）
> 数据来源：`intel/stanford-rna-3d-folding/`（80 条主题索引 + 6 篇 write-up 正文）

## 1. 任务与数据

- 预测目标：由 RNA 序列预测三级结构（3D 坐标）。
- 数据形态：序列 + 实验解析结构（PDB 体系）；样本量小、结构标注昂贵。
- 与 Part 2 的区别：本场（Part 1）受**算力限制更明显**，多队采用模板/检索式方法。

## 2. 方案谱系

| 方案 | 名次 | 关键点 |
| --- | --- | --- |
| **"没有 GPU"的路线选择** | 1st | 作者明确说明"没有 GPU，从头训练模型不现实"，因此选择检索/模板类方法并做精细实现 |
| **模板建模（TBM）** | 2nd | 作者有 CASP 参赛经验：从已知结构中找相似模板并迁移原子坐标 |
| 临时登顶方案 | 高票帖 | 见讨论区 |
| 3rd 方案 | 3rd | 见讨论区 |

## 3. 关键技巧

- **算力约束决定方法路线**：小算力下"检索 + 模板"往往优于从头训练（与 Part 2 的结论一致）。
- **领域数据处理能力**（PDB 解析、结构对齐）是核心壁垒。
- **模板检索 + 坐标迁移**：在结构预测里是最古老也最有效的方法之一。
- 关注评测细节：结构相似度指标需要本地精确复现。

## 4. 可迁移性评估

- **可直接迁移**：
  - **"先看算力预算，再选方法路线"**——小算力走检索/模板，大算力才考虑端到端训练。
  - 检索式方法（找相似样本迁移结果）在各领域的低算力场景通用。
- 需要前提：结构生物学工具链（PDB/CASP 体系）与对齐算法。
- 不建议照搬：无视算力约束强行端到端训练。

## 5. 对新手的关键启示

1. **算力也是约束条件**：冠军的胜利部分来自"认清自己没有 GPU"。
2. **检索/模板方法被低估**，在结构类任务里常是最优解。
3. 与 Part 2 对照可见同一问题的两条路线：**模板/物理方法** vs **预训练大模型 + 领域特征**。

## 7. 轻读结论（2026-10 补）

**一句话**：Part 1 的决定性结论是"**TBM/检索路线在本届封神**"——1st 没有 GPU，用模板建模五步流程 + 对 DRfold2 优化/选择模块的工程增强夺冠；2nd 把 RibonanzaNet 中间层表征拿来做远程同源检索（RBSSA），消融（私榜）full 0.56125 → 去 RBSSA 0.50551 → 再去标准 TBM 仅 0.37400；3rd 自建 rMSA 微调 Protenix，再与 DRfold2、Boltz-1 集成，私榜 0.54312。

- 1st（609774）：无 GPU；PDB_RNA 全量 CIF（93 种核苷酸变体映射、disorder-aware 提坐标）；TBM 五步 = 检索 → 全局比对 → 坐标迁移 → 缺口几何重建（C1'–C1' ≈5.9Å、正弦扰动、末端外推）→ 置信度自适应精化；DRfold2 增强 = float64 打分、`torch.cdist` 向量化、预计算样条、PyTorch LBFGS、Boltz-1 集成；失败自动回退 TBM。
- 2nd（609843）：RBSSA = 用 RibonanzaNet 解码器前表征做 Smith–Waterman 式 DP 对齐（cosine/dot），PDB 2025-05-21 经 MMseqs2 95% 聚成 4,779 簇（3,991 代表），300nt 目标搜索约 160 秒；Chai-1 + Boltz-1 补模板缺口；dot 版私榜 0.56966。
- 3rd（609701）：自建 rMSA 花 14 天；Protenix 微调（GH200 96GB、<800nt、约 1 天/轮）**无 rMSA 无效**；<400nt 用 DRfold2（只保留 energy selection + Arena）、>400nt 转 Protenix；Protenix+Boltz 提交 公 0.61253 / 私 0.54312。
- 其他：582377（0.484，纯 CPU / 无 GPU）用 TM-score 聚类 + Keras 五组分类；566906（121 票滚动实验帖）5 模型 lb 0.321、20 模型按能量选 best-5 的 CASP15 0.516/0.522；582295 用赛后新增 PDB 做 TBM 临时登顶、自述预期大跌；社区 AF3 基线 no-MSA 0.259 / rMSA 0.397。

**裁决**：模板检索/表征对齐是首位投入；best-of-5 指标下提交多样性 > 单模精度；RNA 基础模型可当"检索器/特征提取器"；算力充裕时 rMSA 微调 Protenix 可行，但 rMSA 是前提；公开榜分数受后期换榜与模板库时间敏感性影响，需打折看待。

**悬案**：决赛 4th/5th/6th/7th/9th/10th 写-up（609775/609713/610261/609921/609515）未细读；1st 私榜分数未披露；Ribonanza TM-score 与标准 TM-score 的差异未整理。

## 8. 图表证据

![DRfold2 基线与能量选择](../../intel/stanford-rna-3d-folding/bodies/566906_img/01.png)

**图 1**（topic 566906）：ribonanza-net 基线（CV 0.28 / CASP15 0.186 / LB 0.177）对比 simplified DRfold2——5 模型 LB 0.321、20 模型按能量选 best-5 的 CASP15 达 0.516/0.522。

![表征对齐与 Smith–Waterman 对比](../../intel/stanford-rna-3d-folding/bodies/609843_img/01.png)

**图 2**（topic 609843）：RBSSA 原理——把 Smith–Waterman 的匹配分替换为 RibonanzaNet 中间层位置特异向量的相似度（点积/余弦/皮尔逊）。

## 9. 出处

- 讨论区索引：`intel/stanford-rna-3d-folding/topics.md`（80 条）
- 已收录 write-up（6 篇）：
  - 1st（97 票）：https://www.kaggle.com/competitions/stanford-rna-3d-folding/discussion/609774
  - 2nd（16 票）：https://www.kaggle.com/competitions/stanford-rna-3d-folding/discussion/609843
  - 3rd（16 票）：https://www.kaggle.com/competitions/stanford-rna-3d-folding/discussion/609701
  - 0.484 单机方案（23 票）：https://www.kaggle.com/competitions/stanford-rna-3d-folding/discussion/582377
  - 方案说明（121 票）：https://www.kaggle.com/competitions/stanford-rna-3d-folding/discussion/566906
  - 临时登顶说明（20 票）：https://www.kaggle.com/competitions/stanford-rna-3d-folding/discussion/582295
