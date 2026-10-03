# NFL Player Contact Detection

> 主题：cv ｜ 子类：tracking ｜ 领域：体育 ｜ 类别：Featured
> 截止：2023-XX-XX ｜ 队伍数：900+ ｜ 机制：代码赛 ｜ 指标：F1（接触检测）
> 数据来源：`intel/nfl-player-contact-detection/`（80 条主题索引 + 6 篇 write-up 正文）

## 1. 任务与数据

- 预测目标：由比赛视频与追踪数据判断**哪些球员之间存在接触**（二分类，按球员对）。
- 数据形态：视频帧 + 追踪坐标 + 头盔标注；**测试集很小（61 个 play）**。
- 构造陷阱：
  - 测试集小 → **本地验证的重要性高于以往**（2nd 明确指出）；
  - 按 play/game 分组，避免同场次泄漏；
  - 正样本稀疏（接触是少数时刻）。

## 2. 方案谱系

| 方案 | 名次 | 关键点 |
| --- | --- | --- |
| 多模态（视频 + 追踪）+ StratifiedGroupKFold | 2nd | **按 game_key 分组**的 Stratified Group KFold；强调本地验证比以往更重要；主办方还提供了表格基线作为起点 |
| 其他方案 | 见讨论区 | |

## 3. 关键技巧

- **小测试集下的验证纪律**：分组 + 分层，确保本地估计可靠。
- **追踪数据 + 视频融合**（与 NFL 2026 轨迹预测同源）。
- **利用主办方提供的基线**启动（robikscube 的表格基线）。
- **按比赛（game）分组**是体育类数据的标准做法。

## 4. 可迁移性评估

- **可直接迁移**：
  - **小测试集时把验证做到极致**（分组、分层、多折）；
  - 多模态（视频 + 结构化追踪）融合；
  - 体育/医疗数据的"按场次/患者分组"。
- 需要前提：视频处理与追踪数据的特征工程。
- 不建议照搬：小测试集上追求模型复杂度。

## 5. 对新手的关键启示

1. **测试集越小，验证设计越重要**（本场只有 61 个 play）。
2. **模态互补**：视频给视觉证据，追踪给几何关系。
3. 与 NFL 2026（轨迹预测）对照：同一系列从"接触检测"到"轨迹预测"的任务演进。

## 6. 轻读结论（2026-10 补）

**一句话**：视频+追踪的接触事件检测——**追踪特征编码进 CNN + PP/PG 分开建模 + 邻域时序后处理**是三个稳定支点；测试仅 61 个 play，必须按 game_key 分组验证。

- 1st（138 票）：XGB 预处理 → **resnet50-irCSN**（动作识别）→ XGB 后处理；PP 用视频+追踪图（18 帧），PG 不用追踪（23 帧）；PP 邻域后处理 +0.005、**PG +0.04**；1 epoch+4 seed。
- 2nd Hydrogen（78 票）：24 帧×2 方向、端区+边线早融合、**5 通道追踪编码**（距离×128/同队/移动距离等）；stage2 LGBM + 50:50 平滑；CV 0.807/公 0.796/私 0.796。
- 共识：追踪先验直接编码；PP/PG 输入需求不同；邻域平滑必要；线性插值（追踪 10→60Hz/头盔框）利大于弊。

**分歧**：单段（2nd，防两阶段过拟合）vs 三段（1st，省算力）；追踪插值的噪声-收益权衡。

**悬案**：3rd/5th 未收录；MCC 阈值/不平衡细节缺失。

## 7. 图表证据

![2nd 的 CNN 架构](../../intel/nfl-player-contact-detection/bodies/391740_img/01.png)

**图 1**（topic 391740）：5 帧 × 多通道 → 2D Conv（EffNetV2）→ 3D Conv → 接触概率。

## 8. 出处

- 讨论区索引：`intel/nfl-player-contact-detection/topics.md`（80 条）
- 已收录 write-up（6 篇）：
  - 1st（138 票）：https://www.kaggle.com/competitions/nfl-player-contact-detection/discussion/391635
  - 2nd Team Hydrogen（78 票）：https://www.kaggle.com/competitions/nfl-player-contact-detection/discussion/391740
  - 4th（49 票）：https://www.kaggle.com/competitions/nfl-player-contact-detection/discussion/391719
- 轻读全本：`analysis/deep/nfl-player-contact-detection.md`（Tier B 轻读：对照矩阵/裁决/证据分级/悬案 + 1 图证）
