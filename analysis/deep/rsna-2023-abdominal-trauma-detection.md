# RSNA 2023 Abdominal Trauma Detection 轻量深读（Tier B）

> 赛事：Featured ｜ 主题 cv（医学 3D 多标签检测）｜ 1125 队 ｜ 代码赛 ｜ 指标：RSNA Trauma Metric（器官级 + 患者级加权）
> 材料基础：`digests/rsna-2023-abdominal-trauma-detection.md`（6 篇正文：1st 447449 / 2nd 447453 / 10th 447450 / 3rd 447464 / 往届汇编 427233 / PNG 数据 427427；80 条主题索引）+ 7 张图
> 轻读时间：2026-10（Tier B B03）

## 1. 一句话重述与数字账

腹部 CT 多器官损伤检测（肝/脾/肾/肠/造影剂外渗，多标签 + 患者级）。真正的考点是**两段式：3D 分割 → 器官裁剪 → 2.5D+RNN 分类**，以及**用器官可见性做软标签/帧采样**来压制标签噪声。

| 关键数字 | 值 | 来源 |
| --- | --- | --- |
| 1st（Team Oxygen） | 三部分：3D 分割出 masks/crops → 2.5D CNN+RNN（肾/肝/脾/肠）→ 另一路（肠+extravasation）；4 折 **患者级 GroupKFold**；384²；96 层 → (32,3,H,W) 2.5D；**软标签 = 患者级标签 × 器官可见度**；共享编码器 + 辅助分割损失（**+0.01~0.03**）；Coat Lite M/S + EffNetV2s + GRU；切片级 max 聚合；最佳单模 OOF **0.326**、集成 0.31x | 1st |
| 2nd（TheoViel） | 2D 模型 + RNN：先用 EffNetV2 判"每帧有哪些器官"来控制**帧采样**（正肠/外渗用帧级标签，其余随机）；器官 crop 模型（3D ResNet18 裁剪 → 2D CNN+RNN）；RNN 直接优化比赛指标（器官条件池化 + 每器官独立 logits）；11 类（肠/外渗 BCE + 肾/肝/脾 healthy/low/high CE）；重增广 + cutmix；`dicomsdl` GPU 流水线 <4h | 2nd |
| 3rd | 3D 分割（Qishen 代码）→ 器官 cube → 多配置 2.5D+3D 分类；**关键：肝 mask 输入、按器官分 batch 的 custom sampler、两种 crop 尺寸**；跨器官相关性用多类目标 | 3rd |
| 事件 | 截止延期引发 2nd 公开不满（"unjustified deadline extension"）；PNG 数据资源（174 票） | 2nd+主题索引 |

## 2. 逐方案对照矩阵

| 维度 | 1st | 2nd | 3rd |
| --- | --- | --- | --- |
| 分割→裁剪 | 3D seg masks + 研究级 crop | 3D ResNet18 器官 crop + 2D 器官分类控帧 | 3D seg（res18/50 平均）+ 两档放大 crop |
| 2.5D 序列 | 96 层→32×3 通道 | 1/2 帧、≤600 层、3 邻帧 | 15 帧×3 通道、分辨率对齐 |
| 标签设计 | 患者标签×可见度软标签 | 可见性分类器 + 帧级标签 | 多类（跨器官相关性） |
| 聚合 | 切片 max → 患者 | RNN（Dense+LSTM+max/avg/attention）+ 每器官 logits | 多种 neck（pooling/LSTM/GRU） |
| 损失 | BCE + Dice（辅助） | BCE + CE（11 类） | 多目标 |
| 骨干 | Coat/EffNetV2 + GRU | MaxVit/ConvNextV2/CoatNet + RNN | ConvNext/SE-ResNeXt/MaxVit/CaFormer/XCiT |

## 3. 共识、分歧与裁决

### 共识一：分割→裁剪是标准骨架（3/3）

1st 用 3D 分割做研究级 crop；2nd 用 3D ResNet18 裁器官并喂 crop 模型（"对肾/肝/脾提升明显"）；3rd 用分割 cube + 两档 crop。**裁决**：先把器官定位/裁剪，再做损伤分类——医学 3D 分类的通用降噪结构。置信度：高。

### 共识二：用"器官可见性"处理切片级标签噪声（1st/2nd/3rd）

1st：软标签=患者标签×可见度；2nd：可见性分类器控制帧采样；3rd：mask 输入（肝）与分器官 batch。**裁决**：多标签切片任务里，"这一帧里器官是否存在/可见"是必须建模的中间变量。置信度：高。

### 共识三：2.5D + 序列聚合（RNN/GRU）优于纯 3D（3/3）

三队都是"2D CNN + RNN/GRU/LSTM"为主，3D 只用于分割/裁剪。**裁决**：算力/数据条件下 2.5D+序列模型是性价比最优。置信度：高。

### 共识四：辅助分割损失/多任务稳定训练（1st 明证）

1st：共享编码器 + 辅助分割损失 +0.01~0.03；2nd/3rd 也训练分割与分类的多任务。**裁决**：辅助任务提供空间正则，是小数据医学赛的稳定器。置信度：中高。

### 分歧一：聚合器设计

1st 简单 max 聚合；2nd 用重调 LSTM + 器官条件池化直接优化指标；3rd 试多种 neck。**裁决**：简单聚合已很强，RNN 的增益来自"按器官条件化 + 直接优化指标"；复杂度需消融。置信度：中。

### 分歧二/事件：规则变更（截止延期）

2nd 公开抱怨延期改变竞争结果；1st 与 2nd 的竞争持续到最后一刻。**裁决**：规则中途变更对参赛者体验与结果可信度伤害大；登记为治理事件。置信度：高（事实）。

## 4. 证据分级

| 断言 | 等级 | 说明 |
| --- | --- | --- |
| 1st 的软标签/辅助损失/分数 | 自述 + 图 + 代码 | 中高 |
| 2nd 的帧采样/RNN 设计 | 自述 + 管道图 + 代码 | 中高 |
| 3rd 的关键三招（mask/sampler/crop） | 自述 | 中 |
| 截止延期争议 | 2nd 公开帖 | 高（事件） |
| 各队分数（0.31x/0.326） | 自述 | 中 |

## 5. 悬案与缺口（登记）

- 4th–9th 方案未收录；"Clarification on Provided Labels/Annotations"（78 票）与"prompt based prediction"（85 票）未收录。
- 延期对最终名次的具体影响不可量化；2nd 的完整消融未细读。
- PNG 数据（174 票）与往届 RSNA 汇编（427233）未细读。

## 6. 图表证据

![2nd 的两段式管线](../../intel/rsna-2023-abdominal-trauma-detection/bodies/447453_img/01.png)

**图 1**（topic 447453）：2D 器官分类（EffNetV2）/3D 器官分割（ResNet18）→ crop/mask → 2D+2.5D 损伤分类（ConvNextV2/MaxVit、CoatNet+RNN）→ Series 分类（Dense+LSTM+Max/Avg/Attention → Concat → MLP → 11 类）。**本场标准骨架的全景**。

## 7. 出处

- 1st（447449）：https://www.kaggle.com/competitions/rsna-2023-abdominal-trauma-detection/discussion/447449
- 2nd（447453）：https://www.kaggle.com/competitions/rsna-2023-abdominal-trauma-detection/discussion/447453
- 10th（447450）：https://www.kaggle.com/competitions/rsna-2023-abdominal-trauma-detection/discussion/447450
- 3rd（447464）：https://www.kaggle.com/competitions/rsna-2023-abdominal-trauma-detection/discussion/447464
- 往届汇编（427233）：https://www.kaggle.com/competitions/rsna-2023-abdominal-trauma-detection/discussion/427233
- PNG 数据（427427）：https://www.kaggle.com/competitions/rsna-2023-abdominal-trauma-detection/discussion/427427
