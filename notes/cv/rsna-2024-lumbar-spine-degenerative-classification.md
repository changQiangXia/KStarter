# RSNA 2024 - Lumbar Spine Degenerative Classification

> 主题：cv ｜ 子类：— ｜ 领域：医疗影像 ｜ 类别：Featured
> 截止：2024-10-08 ｜ 队伍数：1874 ｜ 机制：代码赛 ｜ 指标：加权对数损失（多部位多类别）
> 数据来源：`intel/rsna-2024-lumbar-spine-degenerative-classification/`（80 条主题索引 + 6 篇 write-up 正文）

## 1. 任务与数据

- 预测目标：对腰椎 MRI 的每个椎间盘层面，分别判断三类退行性病变的严重程度（椎管狭窄 / 神经根管狭窄 / 关节下狭窄），多类别多部位。
- 数据形态：每例包含矢状面与轴状面多个 MRI 序列；需要先定位椎间盘层面，再做分级。
- 构造陷阱：
  - 定位与分级耦合：层面定位错误会直接导致后续分级全错，是典型的两阶段问题。
  - 序列数量与方向不固定，需要统一处理流程。
  - 多类别加权损失对类别不平衡与权重设置敏感。

## 2. 验证方案

| 方案 | 使用者 | 说明 |
| --- | --- | --- |
| 分层 K 折（按病例） | 多数 | 避免同一病例的多个序列跨折 |
| 分阶段验证 | 1st / 3rd | 定位阶段与分级阶段分别评估 |
| 社区数据集作为坐标参考 | 1st | 借用公开坐标数据集校准定位阶段 |

## 3. 方案谱系

| 方案 | 名次 | 关键点 |
| --- | --- | --- |
| 两阶段：先产出坐标/标签表（含 instance_number 预测），再分级 | 1st | 把第一阶段拆成"实例编号预测 + 坐标预测"两个子问题 |
| 两阶段：矢状面按椎间盘层面裁剪、轴状面按层面分配 + 椎管位置裁剪，再用 Center / Side 双分类器 | 3rd | 针对不同病变类型设计专用分类头 |
| 两阶段流水线 | 2nd / 4th | 见讨论区 |
| 入门材料与阅读清单（社区） | 通用 | 提供起步资源 |

## 4. 关键技巧

- **"定位 → 裁剪 → 分类"是医学影像多实例任务的通用骨架**。
- **按解剖结构设计分类头**（中心型病变用 Center Classifier，侧方型用 Side Classifier），比统一头更贴合标注语义。
- **借力社区数据与 notebook**：1st 明确说自己的解法建立在社区 notebook 与公开数据集之上。
- **处理不固定输入**：规范序列数量与方向，是两阶段流水线的前置条件。
- **类别权重按指标定义设置**，不凭经验。

## 5. 可迁移性评估

- 可直接迁移：两阶段（定位 + 分类）范式（适用于一切"多部位分别判断"的检测任务）；按病变类型设计专用头；以社区基线为起点。
- 需要前提：医学影像处理经验（DICOM、序列方向、层面定位）；MRI 序列训练需要较大显存。
- 不建议照搬：直接端到端单阶段（定位错误会污染全流程）。

## 6. 对新手的关键启示

1. 多实例医学任务先解决"在哪"，再解决"是什么"。
2. 分类头的设计要贴合标注语义（中心 vs 侧方）。
3. 社区基线不是抄，而是起点。

## 7. 图表证据：4th 方案管线图（图证）

![RSNA 2024 4th place solution pipeline](../../intel/rsna-2024-lumbar-spine-degenerative-classification/bodies/539443_img/01.png)

*图：4th place solution 的完整管线（原帖 https://www.kaggle.com/competitions/rsna-2024-lumbar-spine-degenerative-classification/discussion/539443 ；本地文件 `intel/rsna-2024-lumbar-spine-degenerative-classification/bodies/539443_img/01.png`）*

从图中可确认/补全正文未写全的结构：

- **三路输入**：矢状面两路 + 轴状面一路，各自独立进入定位分支；
- **定位阶段不对称**：两路矢状面走"层级检测 → 关键点检测"两级，轴状面只做关键点检测（不需要层级定位）；
- **分级阶段四个子模型**：1 个"多视角输入-多条件输出" + 3 个"单视角输入-单条件输出"；
- **融合方式**：MLP + LGBM + XGBoost 三个元模型之上，再用 **Nelder-Mead** 搜权重——比正文的"元分类器融合"更具体；
- 启示：该方案把"多部位多类别"进一步拆成"每条件独立子模型 + 条件特异融合"，是比"单模型多头"更彻底的分解策略。

## 8. 出处

- 讨论区索引：`intel/rsna-2024-lumbar-spine-degenerative-classification/topics.md`（80 条）
- 已收录 write-up（6 篇）：
  - 1st（105 票）：https://www.kaggle.com/competitions/rsna-2024-lumbar-spine-degenerative-classification/discussion/540091
  - 2nd（98 票）：https://www.kaggle.com/competitions/rsna-2024-lumbar-spine-degenerative-classification/discussion/539452
  - 3rd（65 票）：https://www.kaggle.com/competitions/rsna-2024-lumbar-spine-degenerative-classification/discussion/539453
  - 4th（76 票）：https://www.kaggle.com/competitions/rsna-2024-lumbar-spine-degenerative-classification/discussion/539443
  - 入门材料（137 票）：https://www.kaggle.com/competitions/rsna-2024-lumbar-spine-degenerative-classification/discussion/503433
