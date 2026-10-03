# MABe - Mouse Behavior Detection

> 主题：science（行为时序）｜ 子类：— ｜ 领域：神经科学 ｜ 类别：Research
> 截止：2025-12-15 ｜ 队伍数：1412 ｜ 机制：代码赛 ｜ 指标：行为识别（多标签/事件级）
> 数据来源：`intel/MABe-mouse-behavior-detection/`（80 条主题索引 + 6 篇 write-up 正文）

## 1. 任务与数据

- 预测目标：由多机位视频/姿态追踪数据识别小鼠的行为（多标签，含行为片段的时间定位）。
- 数据形态：多视角 + 姿态关键点序列；标注成本高、数据规模有限。
- 构造陷阱：
  - **没有公开的深度学习基线**（7th 明确说这正是吸引他的地方）——纯表格基线（XGBoost）反而很强；
  - 行为定义带边界模糊（行为片段起止点主观）；
  - 多视角/多主体需要聚合。

## 2. 方案谱系

| 方案 | 名次 | 关键点 |
| --- | --- | --- |
| **CNN-Transformer + 不变性特征** | 7th 金 | 作者目标明确：**"用一个神经网络打败最强的公开 XGBoost notebook"**；靠不变性特征（对尺度/视角/噪声稳健）取得突破 |
| 强表格基线（XGBoost） | 社区（Top 100） | 关键点序列统计特征 + 树模型即可进入前 100——**深度学习并非必需** |

## 3. 关键技巧

- **不变性特征**（尺度/视角/噪声）是姿态序列建模的关键（与 NFL 的手性增强同理）。
- **"先打败强基线"的目标设定**：7th 用公开 XGBoost 作为对照目标，方向明确。
- 姿态关键点序列 → 时序模型（CNN+Transformer）。
- 行为片段的边界处理（事件级后处理）。

## 4. 可迁移性评估

- **可直接迁移**：
  - 姿态/骨架序列的**不变性特征**（视角归一化、尺度归一化）；
  - 以强基线为靶子的开发方式；
  - 行为/事件级任务的边界后处理。
- 需要前提：姿态估计数据与序列建模能力。
- 不建议照搬：忽视表格基线直接上大模型。

## 5. 对新手的关键启示

1. **没有公开深度学习基线的比赛 = 机会，但先量化表格基线的高度**（本场 XGBoost 进前 100）。
2. **不变性特征**是动物/人体姿态任务的通用关键。
3. 与 CMI 传感器、HMS-EEG 对照：**生物信号类任务统一强调"多视角/多通道 + 分组验证 + 事件后处理"**。

## 6. 出处

- 讨论区索引：`intel/MABe-mouse-behavior-detection/topics.md`（80 条）
- 已收录 write-up（6 篇）：
  - 7th 金 CNN-Transformer（92 票）：https://www.kaggle.com/competitions/MABe-mouse-behavior-detection/discussion/663029
  - 2nd（46 票）：https://www.kaggle.com/competitions/MABe-mouse-behavior-detection/discussion/663083
  - 3rd（52 票）：https://www.kaggle.com/competitions/MABe-mouse-behavior-detection/discussion/663026
  - 1D 目标检测方案（42 票）：https://www.kaggle.com/competitions/MABe-mouse-behavior-detection/discussion/609063
