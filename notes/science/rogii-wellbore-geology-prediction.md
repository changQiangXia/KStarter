# ROGII - Wellbore Geology Prediction

> 主题：science ｜ 子类：— ｜ 领域：地球科学 ｜ 类别：Featured
> 截止：2026-08-05 ｜ 队伍数：6125 ｜ 机制：代码赛 ｜ 指标：MSE
> 数据来源：`intel/rogii-wellbore-geology-prediction/`（120 条主题索引 + 8 篇 write-up 正文）

## 1. 任务与数据

- **预测目标**：水平井钻井过程中，沿井身的伽马射线（GR）测井曲线与参考井（typewell）比对，预测钻头在岩层柱中的相对高度 **TVT**。
- **数据形态**：一维测井序列 + 地质参考曲线；本质是**序列对齐 / 状态估计**问题，而非普通回归。
- **构造陷阱**：
  - 排行榜在私榜发生大洗牌（6th 自述"公开第 20、私榜第 6"），说明公开榜可被过拟合。
  - 少数"主导井"会对验证分数产生过大影响，验证集设计必须对井的抽样稳健（2nd）。
  - 公开代码/数据包与本地划分不一致会引入**数据泄漏式作弊**（7th 明确记录 agent 犯过这个错）。

## 2. 验证方案

| 方案 | 使用者 | 说明 |
| --- | --- | --- |
| 井级分组 CV + 对主导井稳健的验证设计 | 2nd | 明确以"对少数主导井不敏感"为验证目标 |
| 五折 CV 对照公开/私榜 | 36th | CV 5.7 / public 6.3 / private 6.9，量级一致 |
| 物理模型 + 神经网络双轨对照 | 3rd、6th | 以物理基线（粒子滤波）为参照判断神经网络收益是否真实 |

## 3. 模型家族

| 方案 | 名次 | 关键点 |
| --- | --- | --- |
| 2D 对齐 + 交叉熵损失（网格化 TVT） | 1st | 把问题重构为对齐任务；代码主要由 Codex/GPT-5.5/5.6 编写 |
| AnchorCNN：预测条件转移分布 P(dTVT｜TVT) + 动态规划精确解码 | 2nd | 在**物理一致的合成数据**上训练；用 Claude Code 辅助 |
| 物理轨迹生成（HMM / 粒子滤波）+ 神经模型 + SoftMax 门控融合 | 3rd | 生成多条物理可行轨迹，再逐位置选择 |
| 粒子滤波群（91 个不同设置）+ 神经网络融合 | 6th | 全流程围绕粒子滤波构建 |
| HMM + UNet | 7th | "agent is all you need"：承认自己没完全理解解法 |
| 堆叠 UNet：把每口井当作图像（256 深度桶 × MD 列） | 26th | 合成井预训练 + 交叉熵，整型网格化输出期望值 |
| 全自动 agent 实验（codex --yolo 两周，2×L4） | 36th | 单模型 CV 5.706；人工只做方向决策 |

## 4. 关键技巧

- **物理模型与神经网络的混合**是本题主流：粒子滤波/HMM 提供物理可行的轨迹先验，神经网络做误差互补与融合。
- **问题重构**：1st 把它当作 2D 对齐任务用交叉熵训练；2nd 建模条件转移分布并用动态规划解码；26th 把井转为图像做分割式预测。
- **合成数据预训练**：用物理一致的合成井扩充训练（2nd、26th）。
- **输出解码**：预测分布而非点值，再用期望值/DP 得到路径（2nd、26th）。
- **AI agent 工程化**：1st、2nd、7th、36th 都明确由编码 agent 承担主要实现工作；7th 总结的教训是"要反复审计 agent 是否引入了数据泄漏"。

## 5. 可迁移性评估

- **可直接迁移**：
  - **序列对齐类问题**（把回归重构为对齐/状态估计）是通用范式，适用于任何"沿轨迹的隐状态推断"任务。
  - 物理模型 + 神经网络混合：物理模型负责可行域，神经网络负责残差，是科学计算类比赛的标准打法。
  - 合成数据预训练 + 分布输出 + 期望/DP 解码。
  - 验证集要**对少量主导样本稳健**，否则会被个别井带偏。
- **需要前提**：
  - 粒子滤波/ HMM 需要可写出的状态转移与观测模型（本题有明确物理意义）。
  - 长程 agent 自动实验需要 GPU 与工具链支持（36th 用 2×L4 两周）。
- **不建议照搬**：
  - 直接引用公开 bundle 数据（可能造成划分泄漏）。
  - 盲目信任 agent 生成的实验结论，需要人工审计数据划分。

## 6. 对新手的关键启示

1. **先把问题重构对**（回归 → 对齐/状态估计），收益远大于调模型。
2. **有物理模型就用**：它是低成本强基线，也是神经网络的互补项。
3. **验证集要防"个别样本主导"**——尤其在样本数少、样本异质性强的任务里。
4. **AI 编码 agent 已成一线战力**，但必须审计它是否偷偷用了泄漏数据；本场多支队伍踩过这个坑。

## 7. 出处

- 讨论区索引：`intel/rogii-wellbore-geology-prediction/topics.md`（120 条）
- 已收录 write-up（8 篇）：
  - 1st（184 票）：https://www.kaggle.com/competitions/rogii-wellbore-geology-prediction/discussion/733220
  - 2nd（44 票）：https://www.kaggle.com/competitions/rogii-wellbore-geology-prediction/discussion/733432
  - 3rd（40 票）：https://www.kaggle.com/competitions/rogii-wellbore-geology-prediction/discussion/733319
  - 6th（60 票）：https://www.kaggle.com/competitions/rogii-wellbore-geology-prediction/discussion/733226
  - 7th（40 票）：https://www.kaggle.com/competitions/rogii-wellbore-geology-prediction/discussion/733154
  - 26th（74 票）：https://www.kaggle.com/competitions/rogii-wellbore-geology-prediction/discussion/733136
  - 36th（53 票）：https://www.kaggle.com/competitions/rogii-wellbore-geology-prediction/discussion/733181
  - 9th（35 票）：https://www.kaggle.com/competitions/rogii-wellbore-geology-prediction/discussion/733150
