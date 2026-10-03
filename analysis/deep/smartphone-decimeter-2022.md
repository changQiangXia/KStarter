# Google Smartphone Decimeter Challenge 2022 轻量深读（Tier B）

> 赛事：Research ｜ 主题 tabular/优化（GNSS 定位）｜ 573 队 ｜ 标准赛 ｜ 指标：SmartphoneDecimeter（水平误差分位数）
> 材料基础：`digests/smartphone-decimeter-2022.md`（6 篇正文：5th 340692 / 1st 341111 / 3rd 341305 / How to approach 323548 / 6th 341226 / 上届冠军 322510；75 条主题索引）+ 11 张图
> 轻读时间：2026-10（Tier B B02）

## 1. 一句话重述与数字账

从手机原始 GNSS 观测（伪距/多普勒/载波相位 ADR）估计分米级轨迹。真正的考点是**物理优化（因子图/最小二乘）而不是 ML**：基站差分、精确星历、鲁棒损失、以及手机型号/数据质量细节。

| 关键数字 | 值 | 来源 |
| --- | --- | --- |
| 1st（上届冠军，连冠） | FGO（GTSAM）**两阶段**：先多普勒估速度（去外点+Akima 插值+可判停）→ 再伪距（基站修正）+ADR 时差+速度约束联合估位置；Huber M-估计替代 switchable constraints（收敛快、效果近）；全测试约 **30 分钟**；赛后发现基站坐标偏移后补交：公 **1.372**/私 **1.197**（当时最好） | 1st |
| 1st 的机型 quirks | 直接从 `gnss_log.txt` 转伪距更准（device_gnss.csv 缺值）；XiaomiMi8 多普勒有 **600ms** 时钟偏移；SamsungS20/Mi8 的不确定度不可信→用仰角误差模型；Pixel4 的 HardwareClockDiscontinuedCount 变化→周跳、ADR 不可用 | 1st |
| 5th | 单一全局优化（TensorFlow 自定义求解器 + 增广拉格朗日）：状态=位置/速度/加速度/**jerk**（ECEF 分段三次 Hermite）；QP 平滑给初值；地基 UNAVCO 15s + IGS MGEX 精密星历 + NGL 基站坐标 + 电离层数据；**完全不用 ML/IMU**（GT 只用于检查）；对伪距/多普勒/ADR 全部加 switchable constraints | 5th |
| 事件 | "Some ground truths are wrong"（39 票）；测试含与训练不同区域（OAK/LAX）；Pixel4 部分 run 的 ADR 无效 | 1st+主题索引 |

## 2. 逐方案对照矩阵

| 维度 | 1st | 5th |
| --- | --- | --- |
| 优化框架 | GTSAM FGO，两阶段（速度→位置） | TensorFlow 自定义全局优化（增广拉格朗日） |
| 状态 | 位置/速度/接收机钟 | 位置/速度/加速度/jerk + 钟差/ISRB + switch 变量 |
| 鲁棒性 | Huber M-估计 | 对每类观测的 switchable constraints |
| 差分/星历 | NGS CORS 30s 单基站 + 广播星历 | UNAVCO 15s + IGS MGEX 精密星历 + NGL 坐标 + 电离层 |
| ML/IMU | 尝试加速度积分失败；无 ML | 完全不用 ML/IMU |
| 关键增益 | 两阶段 + 机型专项修正；基站坐标偏移修正 | 状态方程（jerk 常数）+ 不确定度加权 + 全局优化 |

## 3. 共识、分歧与裁决

### 共识一：这是物理优化赛，ML 不是主力（1st/5th）

1st 是 GNSS 研究者、核心是 FGO；5th 明说"没用 ML，GT 只用于检查"；上届经验也如此。**裁决**：在观测模型清晰、可做差分的定位任务里，先做物理优化；ML 只可能在误差建模/外点分类等局部有位置。置信度：高。

### 共识二：载波相位（ADR）是分米级的前提，但可用性差（1st/5th）

1st："没有 ADR 达不到分米级"；Pixel4 某些 run 的 ADR 无效；5th 把 ADR 作为全局优化的一类观测并加权。**裁决**：ADR/多普勒缺一不可，但必须处理周跳、时钟不连续与机型差异。置信度：高。

### 共识三：基站差分 + 精密星历 + 鲁棒损失是标准组合（2/2）

单/多基站、广播/精密星历、Huber/switchable constraints 都在用。**裁决**：差分消除公共误差、精密星历省去轨道拟合、鲁棒核处理城市多路径。置信度：高。

### 共识四：数据质量与评测公平性存在硬伤（1st + 39 票帖）

部分 ground truth 错误、基站坐标偏移、测试区域与训练不同（OAK/LAX）、Pixel4 的 ADR 问题。**裁决**：赛前/赛中做"数据审计"并公开问题；结果解释要带数据质量折扣。置信度：高。

### 分歧一：单阶段 vs 两阶段优化

1st 明确"速度与位置分开估"是今年精度提升的关键（便于插值/停走判断）；5th 把全部观测放进一个全局优化。**裁决**：两阶段在缺测/隧道多的数据上更稳；单阶段在实现上更优雅。两者都到前 5。置信度：中高。

### 分歧二：基站数量与外部数据

1st 单基站（后悔没做多基站集成）；5th 用多基站+电离层+精密星历。**裁决**：外部差分数据越多越可能提升，但工程量与基线长度会引入新误差项。置信度：中。

### 失败学（1st）

加速度计积分估速（大量时间、无增益）；用学习动态调 Huber 参数（无法超过按 run 固定参数）；tightly-coupled 逐卫星距离优化（失败但有研究潜力）。**裁决**：在强物理模型下，学习类"调参"收益有限。置信度：中高。

## 4. 证据分级

| 断言 | 等级 | 说明 |
| --- | --- | --- |
| 1st 的两阶段/机型修正/补交分数 | 自述（作者为 GNSS 研究者） | 中高 |
| 5th 的状态空间/求解器细节 | 自述 + 公式图 | 中高 |
| 基站坐标偏移与 GT 错误 | 1st + 39 票帖 | 高（事件存在） |
| ML 无效 | 两队独立结论 | 中高 |

## 5. 悬案与缺口（登记）

- 2nd/4th 方案未收录；"How to Approach"（65 票）与上届冠军（322510）未细读。
- 官方对 GT 错误/基站坐标偏移的回应与 rescore 未收录。
- 多基站集成、tightly-coupled 的潜力未量化。

## 6. 图表证据

![5th 的全局优化计算图](../../intel/smartphone-decimeter-2022/bodies/340692_img/03.png)

**图 1**（topic 340692）：红色=可训练变量（位置/速度/加速度/ISRB/钟差/switch/jerk），蓝色=常量（卫星位置/速度、观测），底部为伪距/多普勒/ADR/jerk 四类损失 → 评价函数。**"把所有 GNSS 观测写进一张因子图"的完整形态**。

## 7. 出处

- 5th（44 票）：https://www.kaggle.com/competitions/smartphone-decimeter-2022/discussion/340692
- 1st（72 票）：https://www.kaggle.com/competitions/smartphone-decimeter-2022/discussion/341111
- 3rd（24 票）：https://www.kaggle.com/competitions/smartphone-decimeter-2022/discussion/341305
- How to Approach（65 票）：https://www.kaggle.com/competitions/smartphone-decimeter-2022/discussion/323548
- 6th（31 票）：https://www.kaggle.com/competitions/smartphone-decimeter-2022/discussion/341226
- 上届冠军（42 票）：https://www.kaggle.com/competitions/smartphone-decimeter-2022/discussion/322510
