# Child Mind Institute - Detect Sleep States

> 主题：tabular（传感器时序）｜ 子类：— ｜ 领域：医疗 ｜ 类别：Featured
> 截止：2023-11-21 ｜ 队伍数：1868 ｜ 机制：代码赛 ｜ 指标：事件级 F1（onset / wakeup）
> 数据来源：`intel/child-mind-institute-detect-sleep-states/`（120 条主题索引 + 8 篇 write-up 正文）

## 1. 任务与数据

- **预测目标**：由腕表传感器（加速度/心率）时序检测**入睡与醒来事件**（事件级 F1，非逐点分类）。
- **数据形态**：多夜长序列（单夜约 17280 步 = 12 步/分钟 × 1440 分钟）；事件标注稀疏。
- **构造陷阱**：
  - **事件级指标**：逐点准确率高不等于事件检出的分数高，需要命中窗口容差。
  - 序列极长，需要下采样/分层建模。
  - 同受试者多夜 → 必须按受试者分组验证。

## 2. 验证方案

| 方案 | 使用者 | 说明 |
| --- | --- | --- |
| 按 Series Id 的 GroupKFold | 4th | 避免同一受试者的多夜跨折 |
| CV-LB 对齐 | 1st | CV 0.8206 / 公开 0.768 / 私榜 0.829（相当于第 9 名） |
| 事件级后处理单独验证 | 4th | 用加权框融合做事件合并 |

## 3. 方案谱系

| 方案 | 名次 | 关键点 |
| --- | --- | --- |
| CNN（下采样）→ 残差 GRU → CNN（上采样），单模型 | 1st | 单模型结构为主，配合后处理；强调 CV 提升路径 |
| 改进 UNet + Transformer + **加权框融合**后处理 | 4th | 以整夜 17280 步为输入，输出 onset/wakeup 双通道；框融合做事件级合并 |
| GRU + UNet + LightGBM 组合 | 3rd | 深度 + 树模型互补 |
| GRU/CNN/Transformer 的 GPU 深度方案 | 11th | 多架构集成 |

## 4. 关键技巧

- **编码器-解码器式的时序结构**（下采样 → 序列模型 → 上采样）适合"长序列 + 事件定位"。
- **事件级后处理**：框融合（Weighted Box Fusion）再次出现在事件检测任务中（与 Feedback 2021 跨度融合同理）。
- **按受试者分组验证**：医学时序的底线。
- **单模型 + 后处理**也能夺冠（1st 以单模型为主）。
- **多架构互补**：GRU/UNet/Transformer/树模型各有贡献。

## 5. 可迁移性评估

- **可直接迁移**：
  - "**下采样 → 时序模型 → 上采样**"的定位范式。
  - **事件级指标必须做事件合并/容差后处理**（框融合或峰值合并）。
  - 按实体（患者/受试者）分组验证。
- **需要前提**：
  - 长序列训练需要显存与高效数据管线。
- **不建议照搬**：
  - 用逐点指标优化事件级任务（需要专门的容差与后处理）。

## 6. 对新手的关键启示

1. **先搞清指标是"逐点"还是"事件级"**——两者的优化方式完全不同。
2. **后处理在事件检测里是刚需**（合并、容差、去重）。
3. **长序列先做结构设计**（降采样/分块），再谈模型。
4. 与 CMI 传感器（行为识别）对照：同一赛事系列，任务从分类变成事件检测，方法差异明显。

## 7. 出处

- 讨论区索引：`intel/child-mind-institute-detect-sleep-states/topics.md`（120 条）
- 已收录 write-up（8 篇）：
  - 1st（168 票）：https://www.kaggle.com/competitions/child-mind-institute-detect-sleep-states/discussion/459715
  - 2nd（177 票）：https://www.kaggle.com/competitions/child-mind-institute-detect-sleep-states/discussion/459627
  - 3rd（77 票）：https://www.kaggle.com/competitions/child-mind-institute-detect-sleep-states/discussion/459599
  - 4th（68 票）：https://www.kaggle.com/competitions/child-mind-institute-detect-sleep-states/discussion/459637
  - 11th（186 票）：https://www.kaggle.com/competitions/child-mind-institute-detect-sleep-states/discussion/459596
