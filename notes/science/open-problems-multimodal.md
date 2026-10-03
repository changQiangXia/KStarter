# Open Problems - Multimodal Single-Cell Integration

> 主题：science（多组学）｜ 子类：— ｜ 领域：生物信息 ｜ 类别：Research
> 截止：2022-10-XX ｜ 队伍数：1600+ ｜ 机制：代码赛 ｜ 指标：多任务回归（多组学）
> 数据来源：`intel/open-problems-multimodal/`（80 条主题索引 + 6 篇 write-up 正文）

## 1. 任务与数据

- 预测目标：单细胞多组学整合任务（由多组学特征预测目标模态，含 RNA / 蛋白等），多任务回归。
- 数据形态：**高维稀疏计数矩阵**（单细胞测序数据）+ 供体/批次信息。
- 构造陷阱：
  - 数据极度稀疏、噪声大；
  - **批次效应与供体差异**是主要干扰；
  - 目标需做变换（对数/标准化）才能稳定训练。

## 2. 验证方案

| 方案 | 使用者 | 说明 |
| --- | --- | --- |
| 按供体分组 CV | 多队 | 避免同一供体跨折 |
| 多任务分别评估 | 1st | 各目标单独度量 |

## 3. 方案谱系

| 方案 | 名次 | 关键点 |
| --- | --- | --- |
| 多组学模型 + **tSVD 插补** + 输入/目标预处理流水线 | 1st | 预处理占据主要篇幅：输入端做标准化与降维，目标端做变换与插补 |
| 信息检索技术迁移 | 2nd / 3rd | 3rd 用 **Okapi BM25 替代 TF-IDF**、用 **LSI（muon 实现）** 做降维 |
| 多方案 | 7th | 见讨论区 |

## 4. 关键技巧

- **把单细胞矩阵当"文本-词项"处理**：BM25、TF-IDF、LSI 等 IR 工具在稀疏计数数据上同样有效。
- **插补（tSVD）**：稀疏数据的低秩补全能显著改善下游任务。
- **目标变换**：对计数型目标做稳定化变换（对数等）。
- **按供体分组验证**：生物学重复必须隔离。
- **没有生物学背景也能做好**（3rd 自述）——工具与验证方法比领域知识更关键。

## 5. 可迁移性评估

- **可直接迁移**：
  - **把 IR 方法（BM25/LSI）迁移到稀疏计数数据**上，是一条成熟且低成本的路线。
  - 低秩插补处理稀疏矩阵。
  - 按实体（供体/患者/批次）分组验证。
- 需要前提：需要生物学数据结构的基本理解（细胞 × 基因的稀疏矩阵）。
- 不建议照搬：不做目标变换直接回归。

## 6. 对新手的关键启示

1. **跨领域方法迁移**（IR → 生物信息）成本低、收益明确。
2. **稀疏数据先插补/降维，再建模**。
3. **没有领域背景也能参赛**——关键是尊重数据特性与验证纪律。

## 7. 出处

- 讨论区索引：`intel/open-problems-multimodal/topics.md`（80 条）
- 已收录 write-up（6 篇）：
  - 1st（104 票）：https://www.kaggle.com/competitions/open-problems-multimodal/discussion/366961
  - 2nd（95 票）：https://www.kaggle.com/competitions/open-problems-multimodal/discussion/366453
  - 3rd（70 票）：https://www.kaggle.com/competitions/open-problems-multimodal/discussion/366428
  - 7th（55 票）：https://www.kaggle.com/competitions/open-problems-multimodal/discussion/366471
