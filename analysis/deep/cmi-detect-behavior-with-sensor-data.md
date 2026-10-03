# CMI Detect Behavior 深读：设备取证 × 组合标签 × 无重复后处理

> 赛事：Featured ｜ 主题 tabular（多模态传感器）｜ 2657 队 ｜ 代码赛 ｜ 指标 CMI_2025（18 类手势 + 朝向，逐序列 API 评分）（2025-09-02 截止）
> 材料基础：`digests/cmi-detect-behavior-with-sensor-data.md`（8 节：1st/2nd/4th/5th/6th/12th + 赛前思考帖 + agent 实验帖）+ 6 张图
> 深读时间：2026-10（Tier A #28）

## 0. 一句话重述：这道题真正在考什么

题面是"用 IMU/THM/TOF 传感器识别 18 类手势"，实际被考的是**三件与模型无关的事**：

1. **设备取证**：训练/测试里存在**戴反的设备**（180° 绕 z 轴）、**左手佩戴**、**缺失传感器**（TOF 0%/20%/100% 缺失、rot 缺失）——先修正数据（翻转/镜像/剔除/分模式建模），再谈网络；
2. **组合标签 + 无重复约束**：每个受试者只录了 51 个有效 (orientation, gesture) 对 × 2 种初始行为 = **102 条序列**，且每个组合标签唯一 → 把预测升级为"每受试者 102 类的**无重复指派问题**"（2nd/4th 用 Hungarian 最大化联合对数似然），后处理一项值 +0.02~0.03；
3. **序列间关系**：API 逐条、乱序给测试序列 → 同一受试者的历史信息可用但顺序随机；5th 用"受试者维度 Transformer"显式建模序列间关系（+0.02），4th/5th 同时记录其**方差**（重提交 0.868–0.880，"选择像抽奖"）。

一句话：**这是一场"数据修正 + 后处理结构利用"的比赛**——分模态 CNN/GRU 是公共件；名次差在谁能把"102 条/受试者、每标签唯一"的结构写进决策。

## 1. 材料与角色

| 帖子 | 作者 | 票数 | 角色与独有信息 |
| --- | --- | --- | --- |
| [583863](https://www.kaggle.com/competitions/cmi-detect-behavior-with-sensor-data/discussion/583863)（agent 实验，151 票） | phalanx | 151 | AI agent 端到端跑通到公开 0.82（单 o3 模型仅 0.70）；"多模型规划"是关键 |
| [582388](https://www.kaggle.com/competitions/cmi-detect-behavior-with-sensor-data/discussion/582388)（赛前思考，137 票） | Ravi Ramakrishnan | 137 | **有效数据只有 ~5100 条序列**；警示 CMI 系列洗牌、少堆复杂集成、聚焦 FE 与实验跟踪 |
| [603592](https://www.kaggle.com/competitions/cmi-detect-behavior-with-sensor-data/discussion/603592)（6th，115 票） | Jack (rsakata) | 115 | **设备取证最完整**：左手/反置修正配方 + 反置检测模型（私榜 +0.013）；分组 1D-CNN + 手势段 U-Net + 100 网络平均 |
| [603594](https://www.kaggle.com/competitions/cmi-detect-behavior-with-sensor-data/discussion/603594)（2nd，113 票） | daiwakun | 113 | **阶段感知注意力 + 相位对齐 mixup + 102 类无重复后处理**（0.865→0.900 公开） |
| [603611](https://www.kaggle.com/competitions/cmi-detect-behavior-with-sensor-data/discussion/603611)（1st，81 票） | Ogurtsov 队（+Devin/zyz） | 81 | 大集成（IMU-only/全特征加权 logits）+ 受试者结构后处理 + 朝向模型；去 scaler 反而最好、x² 特征重要 |
| [603542](https://www.kaggle.com/competitions/cmi-detect-behavior-with-sensor-data/discussion/603542)（5th，79 票） | Ethan | 79 | **受试者维度 Transformer**（同受试者序列成批）；按历史量加权的 subject/sequence 双模型融合 |
| [603601](https://www.kaggle.com/competitions/cmi-detect-behavior-with-sensor-data/discussion/603601)（4th，59 票） | dott | 59 | 144 组合标签 + 无重复 max-llh 后处理；重提交 0.868–0.880 的方差实录 |
| [603564](https://www.kaggle.com/competitions/cmi-detect-behavior-with-sensor-data/discussion/603564)（12th，53 票） | Ruby | 53 | 特征工程细节最全：group conv 分箱、TOF 3D ResBlock、GRU+MHA(ROPE)、class-rank 集成、避免权重调优 |

**材料缺口（未扩采，登记备查）**：31 条 write-up 标记中收录 8 节（3rd/7th-11th 等未收）。

## 2. 逐方案对照矩阵

| 维度 | 1st Ogurtsov 队 | 2nd daiwakun | 4th dott | 5th Ethan | 6th Jack | 12th Ruby |
| --- | --- | --- | --- | --- | --- | --- |
| 目标 | gesture（+orientation 模型） | **组合标签（行为×朝向×手势，102 类）** | 组合标签（18×4×2=144） | gesture | gesture 18 类 + orientation 辅助 | gesture + 多任务辅助 |
| 数据修正 | 剔除戴反受试者；左手镜像；TOF -1→500；无 scaler | 4 缺失变体；左手翻转；戴反者全通道反号（除 z）；其 TOF 置 NaN | 左手翻转；rot 缺失用 acc 估计 | 公共特征/增强 | **完整左手/反置配方 + 反置检测模型**；thm<20→null；tof -1→255 | rot 符号恢复；左手翻转；THM 有效性；TOF 清洗归一 |
| 架构 | 分模态 stems + CNN/GRU/纯 CNN/dense GRU/TOF 3D-CNN bagging | SE-CNN + **阶段感知注意力**（3 阶段辅助头加权注意力） | CNN-attention-pooling 分支 + BERT 血统模型 | **序列编码 + 受试者维 Transformer**（subject-based） | 7 输入块分组 1D-CNN + 手势段 U-Net 双池化 + 多头损失 | group conv 分箱 + TOF 3D ResBlock + GRU+MHA(ROPE) 融合 |
| 训练/增强 | mixup 0.4 + TimeStretch；200–220 epoch；每折 3 run 取优 | 相位对齐 mixup；**测试时在线伪标签**（累积批→1 步微调 lr 5e-5） | Transition 首段/Gesture 末段丢弃、噪声、相位 mixup | 受试者采样比 0.5–0.8 重复采样 | 2 网络 × 50 seeds；RAdamScheduleFree；不用增广/EMA | onecycle+EMA+mixup；rot 翻转/世界系旋转/时间拉伸/掩码 |
| 后处理 | 受试者样本约束 + logits 加权 | **Hungarian 无重复联合最大化** | 无重复 max-llh + 早期历史置零 | 按历史量的融合权重；15 次提交反复评估 | **无后处理**（靠 100 模型平均 + 反置检测） | class-rank 平均 + voting（拒调权重） |
| 成绩 | private 第一 | 公开 0.900/私榜 0.878 | 选 0.876 私榜 | subject +0.02、融合 +0.01 | 5-seed CV 0.874–0.875；私榜 0.873 | CV 0.8458/0.906；公开 0.875/私榜 0.862 |

## 3. 共识、分歧与裁决

### 共识一：数据修正是第一优先级（设备取证）

- **戴反设备**：6th 定位到 SUBJ_019262/SUBJ_045235（acc_x/acc_y 分布翻转的直方图证据），给出完整修正配方（acc/rot 反号、rot +180°、thm/tof 交换、TOF 网格旋转），修正后两受试者准确率 >90% 且其他受试者小升；2nd 也独立修正（除 z 外全通道反号）；1st 直接**从训练与验证中剔除**这两名受试者。
- **左手**：全员镜像（acc_x 反号、rot y/z 反号、THM/TOF 传感器交换与网格翻转）。
- **rot 符号/语义**：12th 用点积恢复 quaternion 符号；TOF 的 -1 语义（"很远"）被 2nd 映射到 500、6th 映射到 255。

**裁决**：传感器比赛的"模型前科学"是设备取证；修正配方可跨队复用（且 6th 的反置检测模型在私榜 +0.013，说明测试也存在反置样本）。置信度最高。

### 共识二：缺失模式决定建模与推理路径

2nd 按 (rot 缺/不缺 × THM+TOF 缺/不缺) 训练 **4 个变体**；6th/1st 在 TOF 缺失 >50% 时切 IMU-only 预测；5th 的 >50% 规则相同；Ogurtsov 剔除 TOF 100% 缺失的序列。

**裁决**：多模态缺失不是"插补问题"而是"分模式建模问题"——不同传感器组合对应不同最优模型，推理时按缺失率切换。置信度高。

### 共识三：组合标签 + 无重复约束的后处理是最大后期杠杆

2nd：模型部分 0.865/0.858 → 加后处理 0.891/0.875（+0.026/+0.017）；再加在线伪标签 0.900/0.878。4th：独立发现同一结构（144 组合、每组合唯一），用无重复 max-llh；冠军也用受试者结构后处理。**结构事实：每受试者 51 对 × 2 = 102 条，每个组合标签至多出现一次。**

**裁决**：把"评测 API 的答题结构"翻译成约束优化（Hungarian/无重复指派）是本场的标准答案。置信度最高。

### 分歧一：是否用受试者级上下文（subject-based 建模）

5th：受试者维 Transformer 让 subject-based 比 sequence-based **+0.02**，但 API 乱序 → 需按历史量加权融合（+0.01）；4th：同样利用历史但指出"顺序随机导致显著方差，重提交 0.868–0.880，选择像抽奖"；2nd/6th 主要靠后处理而非模型内跨序列建模。

**裁决**：受试者级信息有效（+0.02 量级），但评测的乱序机制使其收益带方差；稳妥姿势 = 模型内建模 + 历史量感知融合 + 后处理兜底。置信度中高。

### 分歧二：增广/EMA 等常规手段的价值

6th：数据增广与 mixup"用不起来"、EMA 的收益被 seed averaging 吃掉；12th：多种增广（时间拉伸/掩码/TOF jitter）明确列出；2nd：相位对齐 mixup 有效；1st：缩放+噪声增广。结论不一。

**裁决**：本场有效增广与"相位结构"绑定（相位对齐 mixup、Transition/Gesture 段丢弃）；通用增广收益被强 bagging 稀释。置信度中。

## 4. 增量数字账

| 动作 | 数字 | 来源 |
| --- | --- | --- |
| 数据规模 | 训练 ~5100 条序列（1.2GB 数据但有效行数小）；测试 ~3500 条 | Ravi/2nd |
| 受试者结构 | 4 朝向 × 18 手势 = 72 对，实际只出现 **51** 对；每受试者 **51×2=102** 条序列 | 2nd |
| 2nd 的阶段分数 | 无伪标签/无后处理 0.862/0.854；+伪标签 0.865/0.858；**+后处理 0.891/0.875；两者都有 0.900/0.878** | 2nd |
| 4th 的方差实录 | 同一方案重提交私榜 0.868–0.880，选中 0.876 | 4th |
| 6th 的反置修正 | 两受试者修正后 >90% 准确率；反置检测模型私榜 **+0.013** | 6th |
| 6th 的 5-seed 平均 | 单 seed 0.864/0.862 → 5-seed 0.874/0.875；双网络集成 0.877 | 6th |
| 5th 的增益 | subject-based 比 sequence-based +0.02；双模型融合再 +0.01 | 5th |
| 5th 的 CV | imu-only 0.855 / all 0.898（按受试者 5 折） | 5th |
| 12th 的结果 | 单模 CV 0.8364（IMU）/0.9008（全特征）；集成 CV 0.8458/0.906；公开 0.875/私榜 0.862 | 12th |
| 1st 的工程细节 | 无 scaler 是早期最大提升；35 个 IMU 特征（含 x² 项）；94 分位裁剪 ~120 长度；200–220 epoch | 1st |
| agent 实验 | 单 o3 模型 IMU-only CV 0.70 → 多模型规划公开 0.82 | 583863 |

**可复算/结构校验（2 处吻合）**

1. 102 = 51 × 2 ✓（受试者内组合标签无重复的前提）；
2. 144 = 18 × 4 × 2 的潜在组合空间 vs 实际 102 个被录制的组合 ✓（4th 的"每标签至多一条"表述与 2nd 的口径一致）。

## 5. 机制推演

**M1｜为什么"组合标签 + 无重复"后处理有效**：API 的评分是逐序列的，但数据采集结构规定"每受试者每个组合标签只出现一次"；当你看到该受试者第 N 条序列时，前 N−1 条的高置信标签**必然占用**了对应类别 → 剩余类别是排除法可解的。Hungarian 以负对数概率为代价求全局指派，等价于"受试者级联合最大似然"，比逐条 argmax 的期望错误更低（2nd 的 +0.026 公开增益）。

**M2｜为什么戴反设备的修正是"群体级"收益**：180° 反置使 acc_x/acc_y 与正常群体分布互换（6th 的直方图证据）；不修正时模型要么把它们当过噪声、要么学到矛盾的映射。修正不仅救回两名受试者（>90%），还降低全局噪声（其余受试者小升）；而反置检测模型的价值说明**测试集也存在反置**（私榜 +0.013）。

**M3｜为什么按缺失模式分模型**：TOF 缺失率有三种离散状态（0%/20%/100%），不同状态的最优输入维度不同；把缺失样本塞进全特征模型会让网络学到"缺失即某类"的伪相关。分 4 变体 + 推理切换是"缺失感知"的最直接实现（与 hms 的标注源位移、efficientdet 系列的多分辨率同族思路不同，但同属"按数据形态分流"）。

**M4｜阶段感知注意力为什么必要**：手势序列含长过渡段（relax/move），普通时序注意力会被长段"吸走"；2nd 用 3 类阶段辅助头构造 3 组注意力并按阶段概率加权，等价于"先分段再加权池化"。6th 的 U-Net 手势段估计 + gesture/non-gesture 双池化、4th 的 Transition/Gesture 段丢弃/混合，都是同一机制的变体。**"事件结构先验"注入网络的三种实现。**

**M5｜为什么推理顺序会制造方差**：受试者第 N 条序列的可用历史取决于随机到达顺序；早期序列没有上下文（4th 用"置零历史类概率再按手势求和"退化处理），后处理质量随顺序波动 → 重提交分数抖动（0.868–0.880）。**在"流式评测 + 跨样本约束"的赛制里，方差是结构性的，选择提交本身是决策问题**（与 santa 的选择、llm-detect 的提交选择同族，L22）。

**M6｜为什么强 bagging 能替代后处理（6th 的反例）**：6th 用 100 个网络平均 + 反置修正 + 无后处理拿到 6th，说明**当单模质量足够高时，后处理的边际收益下降**；但 2nd/4th 的对照（后处理 +0.02~0.03）说明在同等模型质量下，结构约束仍是最便宜的分数。两条路线不矛盾：6th 的模型平均把"预测噪声"压到后处理可发挥的空间之外。

## 6. 证据分级

| 断言 | 等级 | 说明 |
| --- | --- | --- |
| 反置设备直方图证据 | **可读取（图）** | acc_x/acc_y 分布互换、acc_z 一致 |
| 102 条/受试者结构 | **可复算（数据统计）** | 72 对中 51 对出现；51×2 |
| 2nd 的后处理增益（+0.026 公开） | **可读取（表）** | 四组对照完整 |
| 4th 的重提交方差 | **自述（强）** | 0.868–0.880 实录 |
| 5th 的 +0.02/+0.01 | **自述** | 无逐折表 |
| 6th 的 5-seed/100 网络 | **可读取（表）** | 多种子对照 |
| 1st 的"无 scaler 最好" | **自述** | 早期实验结论 |
| agent 0.70→0.82 | **自述** | 单例 |

## 7. 边界条件与反事实

- **前提**：评测 API 的"逐序列 + 乱序"结构与"每受试者组合标签唯一"的数据采集设计 → 后处理成立。若评测一次性给全受试者序列（有序），subject-based 模型的方差会消失、后处理收益更稳定。
- **反事实（6th）**：若不训练反置检测模型，私榜 −0.013（其两次提交的差异直接量化了这项修正）；若不做左手/反置修正，部分受试者准确率损失 5–10pt。
- **反事实（2nd）**：若没有后处理，0.865/0.858 只有银牌区间；后处理 +0.026 公开/+0.017 私榜把它推到第 2。
- **反事实（4th）**：若按公开榜反复调参/选提交流程，0.868–0.880 的方差会被误读为"改进"；其选择是"重提交+挑一个"的期望值策略。
- **边界（模型 vs 后处理）**：6th 的无后处理路线与 2nd 的后处理路线都能高位，说明收益分配取决于模型质量与 bagging 强度；不可把后处理当作万能。

## 8. 悬案与失败学

**悬案**

1. **测试集反置/左手的真实比例**：6th 的检测模型私榜 +0.013 说明存在，但比例未知；
2. **受试者级上下文的方差机制**：5th/4th 都观察乱序导致分数波动，但"历史量-收益"的曲线未被建模；
3. **为何"无 scaler"最好**（1st）：与 BN 首层的交互未解释。

**失败学**

| 失败 | 来源 | 教训 |
| --- | --- | --- |
| 增广/mixup 直接套用 | 6th | 与相位结构不匹配的增广无效；其收益被 seed averaging 吃掉 |
| EMA（与 seed averaging 叠加时） | 6th | 集成手段之间会互相替代 |
| 复杂集成/盲目融合 | Ravi 的警示 | 小数据 + 洗牌指标：简单模型 + 强 FE 更稳 |
| 逐条 argmax（无结构后处理） | 2nd/4th | 放弃"无重复"先验等于白扔 +0.02 |
| 在公开榜上反复挑提交 | 4th/5th | 评分方差吞掉真实差异；选择需按期望值 |
| 把 rot/global_acc 当绝对特征 | 6th 的注记 | 依赖采集时朝向，真实部署应去掉或相对化 |
| agent 单模型直接上 | 583863 | 单 o3 模型 0.70；多模型规划（分工/评估）才到 0.82 |

## 9. 图表证据

> 路径相对本文件（`analysis/deep/`）：`../../intel/cmi-detect-behavior-with-sensor-data/bodies/<topic>_img/NN.ext`

**图 1：6th 的多模态分组网络（含手势段 U-Net 与多头损失）**（topic 603592）——`../../intel/cmi-detect-behavior-with-sensor-data/bodies/603592_img/01.png`

*读图结论*：7 个输入块（gesture_segment、acc、rot、derived_acc、rotvec_diff、thm、tof→Conv2d 空间塌缩）各自过**分组 1D-CNN**（首个卷积按通道分组）与 MLP；池化按 gesture/non-gesture 段分别做再拼接；输出三组预测（每块 1/12、IMU-only 1/4、全特征 1/4）——**多头损失 + 段感知池化的完整结构图**。

**图 2：反置设备的分布证据**（6th）——`../../intel/cmi-detect-behavior-with-sensor-data/bodies/603592_img/05.png`

*读图结论*：两名"rotated"受试者（蓝）的 acc_x/acc_y 分布与其余受试者（橙）**镜像互换**，而 acc_z 一致——正是"180° 绕 z 轴佩戴"的指纹，也是 x/y 反号修正的依据。

**图 3：5th 的受试者级 Transformer**（topic 603542）——`../../intel/cmi-detect-behavior-with-sensor-data/bodies/603542_img/01.png`

*读图结论*：batch=1 受试者；每条序列先 CNN→RNN/Transformer→attention pool 得 (seq_num, hidden)，再沿**受试者维度**做 Transformer 建模序列间关系，最后 MLP 输出 (seq_num, label_dim)——"跨序列上下文"的直接实现。

## 10. 对既有笔记/playbook 的修订点

1. `notes/tabular/cmi-detect-behavior-with-sensor-data.md` 升级：补齐 8 节作者/票数；方案谱系扩为 6 方案对照矩阵；新增设备取证（反置/左手/TOF 语义）、缺失模式分模型、组合标签无重复后处理、受试者级上下文与方差、图证与失败学。
2. `playbook/tabular.md`（传感器时序节）增补：
   - **设备取证清单**（佩戴方向直方图诊断、左右手镜像配方、rot 符号、TOF 特殊值语义）；
   - **缺失模式分流**（按传感器组合训练多变体 + 推理切换）；
   - **组合标签 + 无重复指派后处理**（Hungarian/max-llh；先验来自数据采集设计）；
   - **事件结构注入网络**（阶段注意力/段感知池化/相位对齐 mixup）；
   - **流式评测的方差管理**（期望值选择、重提交策略）。
3. `playbook/00-通用方法论.md` 增补："**读懂数据采集设计**"——采样结构（谁、录了几次、哪些组合）往往直接给出后处理约束与上限（本场 102 条/受试者是分数的金矿）。

## 11. 出处

- agent 实验（phalanx，151 票）：https://www.kaggle.com/competitions/cmi-detect-behavior-with-sensor-data/discussion/583863
- 赛前思考（Ravi Ramakrishnan，137 票）：https://www.kaggle.com/competitions/cmi-detect-behavior-with-sensor-data/discussion/582388
- 6th（Jack/rsakata，115 票）：https://www.kaggle.com/competitions/cmi-detect-behavior-with-sensor-data/discussion/603592
- 2nd（daiwakun，113 票）：https://www.kaggle.com/competitions/cmi-detect-behavior-with-sensor-data/discussion/603594
- 1st（Ogurtsov 队，81 票）：https://www.kaggle.com/competitions/cmi-detect-behavior-with-sensor-data/discussion/603611
- 5th（Ethan，79 票）：https://www.kaggle.com/competitions/cmi-detect-behavior-with-sensor-data/discussion/603542
- 4th（dott，59 票）：https://www.kaggle.com/competitions/cmi-detect-behavior-with-sensor-data/discussion/603601
- 12th（Ruby，53 票）：https://www.kaggle.com/competitions/cmi-detect-behavior-with-sensor-data/discussion/603564
- 未收录缺口（登记备查）：31 条 write-up 标记中的其余条目（3rd/7th–11th 等）
