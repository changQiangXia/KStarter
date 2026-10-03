# RSNA 2022 - Cervical Spine Fracture Detection

> 主题：cv ｜ 子类：— ｜ 领域：医疗影像 ｜ 类别：Featured
> 截止：2022-XX-XX ｜ 队伍数：1000+ ｜ 机制：代码赛 ｜ 指标：加权多标签（椎骨级骨折检测）
> 数据来源：`intel/rsna-2022-cervical-spine-fracture-detection/`（80 条主题索引 + 6 篇 write-up 正文）

## 1. 任务与数据

- 预测目标：在颈部 CT 中逐**椎骨（C1–C7）**判断是否存在骨折，并给出患者级汇总。
- 数据形态：DICOM 序列 + 分割标注（椎骨掩码）；多标签、类别不平衡。
- 构造陷阱：
  - **椎骨定位**是前置条件（C1–C7 编号错误会直接导致标签错配）；
  - 数据中存在不同扫描协议与层厚差异；
  - 标注成本高（3rd 明确希望"减少标注依赖"的方案）。

## 2. 方案谱系

| 方案 | 名次 | 关键点 |
| --- | --- | --- |
| 两阶段（椎骨定位/分割 → 逐椎骨分类） | 1st | 代码公开；1st 的方案与代码帖累计 222 + 147 票，是本场最重要的参考 |
| 降低标注依赖的路线 | 3rd | 作者明确目标是"需要更少标注工作的方案，便于扩展"；提供训练/推理代码、幻灯片与讲解视频 |
| 数据说明帖 | 社区高票（179 票） | 逐项解释 DICOM 与分割文件的用法——**入门材料本身也是高价值产出** |

## 3. 关键技巧

- **先定位再分类**：分割/定位椎骨是逐椎骨预测的前提。
- **分割监督作为辅助任务**：提升定位精度。
- **减少标注依赖**：用弱监督/自监督降低对分割标注的需求（3rd 的方向）。
- **公开材料要完整**（代码 + 幻灯片 + 视频），便于社区复用。

## 4. 可迁移性评估

- **可直接迁移**：
  - **结构化医学影像任务的两阶段范式**（定位 → 分类）；
  - 用分割做辅助任务提升主任务；
  - 追求"低标注依赖"的方案设计（更易扩展到新数据）。
- 需要前提：DICOM 处理、3D 分割工具链。
- 不建议照搬：跳过分割直接做全图多标签（标签错配风险高）。

## 5. 对新手的关键启示

1. **"定位 → 分类"在 RSNA 系列里是最稳定的骨架**（2022 颈椎、2023 腹部、2024 腰椎、颅内动脉瘤都是这个套路）。
2. **社区数据说明帖的价值常被低估**（本场最高票之一）。
3. **可扩展性（少标注）本身是方案优势**。

## 6. 出处

- 讨论区索引：`intel/rsna-2022-cervical-spine-fracture-detection/topics.md`（80 条）
- 已收录 write-up（6 篇）：
  - 1st（222 票）：https://www.kaggle.com/competitions/rsna-2022-cervical-spine-fracture-detection/discussion/362607
  - 1st 代码（147 票）：https://www.kaggle.com/competitions/rsna-2022-cervical-spine-fracture-detection/discussion/362787
  - 3rd（59 票）：https://www.kaggle.com/competitions/rsna-2022-cervical-spine-fracture-detection/discussion/362643
  - 数据与提交详解（179 票）：https://www.kaggle.com/competitions/rsna-2022-cervical-spine-fracture-detection/discussion/340612
