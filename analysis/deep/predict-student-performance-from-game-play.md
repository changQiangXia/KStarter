# Predict Student Performance 深读：时长信号 × 噪声准入门槛 × 泄漏风波

> 赛事：Featured ｜ 主题 tabular（行为日志）｜ 2051 队 ｜ 代码赛（API）｜ 指标 Macro F1（18 个二分类问题）（2023-06-28 截止）
> 材料基础：`digests/predict-student-performance-from-game-play.md`（8 节：1st×2/4th/7th/9th/13th + 开局 EDA + 游戏攻略）+ 13 张图
> 深读时间：2026-10（Tier A #29）

## 0. 一句话重述：这道题真正在考什么

题面是"用游戏操作日志预测 18 个二分类问题"，实际被考的是**三件事**：

1. **时长/间隔是因果信号**：这是一款阅读教学游戏（Jo Wilder）——"在文本/房间/事件上花了多少时间、从事件 A 到事件 B 花了多久"就是阅读能力的代理；1st 的 GBDT 全靠 durations+counts（663/1993/3734 个特征/level_group），NN 用 **TimeEmbedding（4× ConvBlock）+ "时长×事件" 时间感知表示**；
2. **验证噪声必须量化**：18 个二分类的宏 F1 对小数据（~11.5k 会话）噪声极大；1st 把噪声量化为 **~0.0003**，特征只有"跨 10 个 bag 的 CV 均值 > 噪声"才准入；NN 用 4/5 折共识；私有测试仅 1450/1500 个会话（探针确认）→ 稳健优先；
3. **数据来源伦理与红利**：官方数据之外存在 **OpenGameData 开放门户**——1st 重建了 98% 训练会话与约 7000 个 LB 会话（即本场"泄漏"），主动上报主办方；补充数据在后续阶段仍带来 +0.002~0.004 的合法增益（4th/7th 同样使用）。

一句话：**这是一场"领域信号 + 实验纪律"的比赛**——模型（XGBoost/Conv1D）是公共件；分差来自谁能把"时间"建模对、把噪声门槛守得住、把泄漏处理得干净。

## 1. 材料与角色

| 帖子 | 作者 | 票数 | 角色与独有信息 |
| --- | --- | --- | --- |
| [387864](https://www.kaggle.com/competitions/predict-student-performance-from-game-play/discussion/387864)（开局 EDA，228 票） | Chris Deotte | 228 | **行为特征来源**：逐屏点击散点（点 Grampa/笔记本/导航）、阅读停顿、弹窗是否缩放——"每个动作都在泄露预测信息" |
| [384796](https://www.kaggle.com/competitions/predict-student-performance-from-game-play/discussion/384796)（攻略，212 票） | pjmathematician | 212 | 游戏代码与问题参考答案——**领域知识版"作弊表"**（合法：来自游戏本身） |
| [420217](https://www.kaggle.com/competitions/predict-student-performance-from-game-play/discussion/420217)（1st，168 票） | Bertrand P | 168 | **噪声准入门槛 + 时间感知事件 + 两级训练 + 泄漏上报全记录**；TF Lite/Treelite 工程 |
| [420119](https://www.kaggle.com/competitions/predict-student-performance-from-game-play/discussion/420119)（7th/效率第 1，102 票） | Jack (rsakata) | 102 | 3 个 LGBM（按 level_group）+ "六键 groupby 时长求和"特征；原始数据 +0.002；3 分钟推理 |
| [420046](https://www.kaggle.com/competitions/predict-student-performance-from-game-play/discussion/420046)（9th，81 票） | Makotu | 81 | **Checkpoint 特征**（必经事件之间的用时）；逐问题 LGB+Cat 平均；前序问题概率特征 +0.001 |
| [420332](https://www.kaggle.com/competitions/predict-student-performance-from-game-play/discussion/420332)（1st 代码，67 票） | Bertrand P | 67 | 训练/预训练/推理四个 notebook 全公开 |
| [420077](https://www.kaggle.com/competitions/predict-student-performance-from-game-play/discussion/420077)（13th，52 票） | Takoi | 52 | 嵌套 CV（按 session_id 前缀切分）+ Transformer+GRU；0.66/0.34 融合 |
| [420349](https://www.kaggle.com/competitions/predict-student-performance-from-game-play/discussion/420349)（4th，48 票） | Joel Erikanders | 48 | **线性回归元模型**（含未来问题概率）；阈值三提交 0.60/0.62/0.64 |

**材料缺口（未扩采，登记备查）**：24 条 write-up 标记中收录 8 节（2nd/3rd/5th/6th 等未收）。

## 2. 逐方案对照矩阵

| 维度 | 1st Bertrand | 4th Joel | 7th Jack | 9th Makotu | 13th Takoi |
| --- | --- | --- | --- | --- | --- |
| 数据 | 重建 98% + 补充 ~20k 会话；37323 完整会话 | 原始数据 ~58k 会话训练，**只用 Kaggle 数据验证** | 原始数据 +0.002；最大 level 作特征 | Kaggle 数据 | 按 session_id 前缀做嵌套 CV |
| 特征 | durations+counts（663/1993/3734/组）；全会话交互 | 时间/序号/坐标差分；点位身份（拼接+枚举）；过滤 >99.9% 通用点（≤452 步） | **六键 groupby 时长求和** + 计数 + notification_click 间隔 | **checkpoint 特征**（必经事件间用时）；3009/9747/18610 个 | 类别计数/数值统计/下一动作聚合 |
| 模型 | XGBoost + Conv1D NN（TimeEmbedding + 时长×事件） | Transformer(1 层)/XGB/Cat + **线性回归元模型（含未来问题概率）** | 3×LGBM（按 level_group） | 逐问题 LGB+Cat 平均 | LGBM + Transformer+GRU（0.66/0.34） |
| 验证 | **10 bags × 5 折 + 噪声 0.0003 门槛 + 4/5 折共识** | CV 决策；阈值三提交 | 4 折 ×3 种子 | 10 折（+0.0005）+ 按答对数分层 | **嵌套 CV**（时间样式切分） |
| 阈值 | 全局 0.625（比逐问题稳） | 0.60/0.62/0.64 三提交 | 0.625 | — | — |
| 成绩 | CV/公开/私榜 **0.705/0.705/0.705** | 0.7044/0.702/0.703 | 0.7034/0.703/0.703 | 0.7024/0.700/0.702 | 0.7053/0.706/0.702 |

## 3. 共识、分歧与裁决

### 共识一：时长与事件间隔是主导信号（全员）

1st：durations+counts 是 GBDT 的全部主力，"duration 是杀手特征"；NN 的 TimeEmbedding（4 层 ConvBlock）+ `duration*(event+room+text+fqid)` 把时长注入事件表示；7th：六键 groupby 的 `elapsed_time_diff.sum()`；9th：checkpoint 特征（"每个玩家必经事件之间的用时"，如找到笔记本 → "Found it!"）；EDA 帖直接把"读文本停顿/点击位置"列为可预测特征。

**裁决**：行为日志任务的第一特征族是"时间在哪些业务实体上被消耗"；领域语义（阅读教学）给出了因果解释。置信度最高。

### 共识二：小数据 + 宏 F1 → 必须量化验证噪声并约束特征准入

1st 的定义最清晰：噪声 ~0.0003，10 bags 的 CV 均值超过噪声才准入；NN 用 4/5 折共识；4th/7th/13th 用多种子/多重复/嵌套 CV；1st 还指出**私有测试只有 1450/1500 会话**（<2000 极噪，5000 才能稳定 CV-LB 对齐）。

**裁决**：把"噪声水平"显式写成准入门槛（而非凭感觉加/删特征）是高噪声表格赛最可迁移的方法论。置信度最高。

### 共识三：全局阈值优于逐问题阈值（1st/7th 独立）

1st：逐问题阈值在 LB 上更"高分"但**更不稳健**，最终用全局 0.625；7th 同样 0.625；4th 做三阈值提交对冲（0.61 才是最优私榜）。

**裁决**：宏 F1 的阈值是典型的"过拟合点"，稳健姿势 = 全局阈值 + 提交层面少量对冲。置信度中高。

### 分歧一：previous/future 问题概率当特征

9th：前序问题概率作特征是 **+0.001**；4th：线性回归元模型不仅用过去，还用**未来问题**的概率（q2 用 q1-3、q7 用 q1-13、q16 用 q1-18）→ 终分 0.7044；1st 明确**拒绝**注入先前 level_group 的目标（"信息压缩、损失信号"，用全会话交互替代，+0.002）。

**裁决**：两种做法在"是否引入自回归结构"上相反；1st 的替代方案（全会话原始交互）在小数据上更稳，4th/9th 的概率注入在整合层面有效。**没有单方压制——取决于模型能否直接访问原始历史。**置信度中。

### 分歧二：NN 值不值得

1st：50/50 GBDT/NN 融合夺冠（NN 单独 CV 0.70175）；4th：Transformer 0.702 CV 进集成；13th：Transformer+GRU 进集成；9th：NN"试了 LSTM/MLP 都不贡献 CV"。

**裁决**：NN 的价值在"与 GBDT 的互补性"而非单体强度（典型 CV 差 0.00x 但融合 +0.002~0.005）；做过特征缩放的 Conv1D/RNN 是低成本异质成员。置信度中高。

## 4. 增量数字账

| 动作 | 数字 | 来源 |
| --- | --- | --- |
| 开放数据重建 | 1st 完美重建 98% 训练会话（后测 ~7000/11500 LB 会话）；修复"双游戏目标偏斜" +0.002 | 1st |
| 补充数据 | 1st：+0.003~0.004（早期）/+0.002（稳定）；7th：CV +0.002 | 1st/7th |
| 全会话交互替代先前目标注入 | +0.002 | 1st |
| 噪声水平 | **~0.0003**（10 bags 均值门槛）；NN 4/5 折共识 | 1st |
| 1st 的阶段分数 | 预训练 backbone CV 0.70025 → 端到端 0.70175 → 集成 **0.705**（公开/私榜同 0.705） | 1st |
| 1st 的工程 | 400k 参数 NN；TF Lite ≥6×；Treelite 2×；效率提交 0.702/0.699、<5 分钟 | 1st |
| 4th | ~58k 会话；Transformer 0.698/0.702 CV；XGB 0.7029；最终 CV 0.7044；阈值 0.60/0.62/0.64（0.61 才是私榜最优） | 4th |
| 9th | checkpoint 特征；特征数 3009/9747/18610；top-500 逐折重训；前序概率 +0.001；10 折 +0.0005；融合 0.7024 | 9th |
| 7th | 六键时长特征；原始数据 +0.002；4 折×3 种子；阈值 0.625；3 分钟推理 | 7th |
| 13th | 嵌套 CV；融合 0.7053/0.706/0.702 | 13th |
| 私有测试规模（探针） | 私榜 = API 前 **1450/1500** 个会话；<2000 噪声极大 | 1st |

**可复算/结构校验（2 处吻合）**

1. 问题分组：q1-3（level 0-4）+ q4-13（5-12）+ q14-18（13-22）= **18 问** ✓（端到端图）；
2. 1st 的会话账：37323 完整会话（含 23562 竞赛+日志）占 66376 总会话 ≈ 56%——与"补充数据把可用完整会话扩大近一倍"一致 ✓。

## 5. 机制推演

**M1｜为什么"时长"是因果特征而非相关特征**：Jo Wilder 是阅读教学游戏，玩家必须阅读文本才能推进；读得快 = 阅读能力强 → 答对率高。因此"在文本/房间/事件上的累计时长、事件间间隔"直接对应考核目标。**领域文献（教育研究）优先于数据挖掘：1st 读游戏研究论文找到 killer feature。**

**M2｜时间感知事件为什么用乘法**：事件表示（event/room/text/fqid 的嵌入之和）与时长嵌入做**逐维乘法**，等价于"用时间调制事件语义"（duration × (e1+e2+…) = Σ duration×ei）；若用拼接/加法，时长只能作为独立维度而无法调制每个事件。这个设计让 NN 以 400k 参数逼近 GBDT 的时长统计能力。

**M3｜两级训练为什么有效**：Level group 的 backbone 先在**所有可用会话**（含未完成的）上预训练 → 数据量最大化、表示通用；冻结后训练端到端头（1×/2×/3× d_model 拼接给不同问题组）→ 稳定且快。与"直接端到端"相比，预训练提供特征抽取器，头部只学组合。

**M4｜噪声门槛的统计意义**：宏 F1 在 18 个二分类上由小验证集估计；折间方差 ≈ 0.0003 量级。若一个特征的平均增益小于折间标准差，加入它等于引入噪声。10 bags（不同折组合）×5 折的均值把估计方差进一步压低——**"bag"就是"对验证集本身做 bagging"**。

**M5｜泄漏事件的机制与处置**：OpenGameData 是游戏开发方自己公开的数据门户；其中包含竞赛训练与 LB 会话的原始日志（同一游戏、同一玩家群体）。1st 重建后立即上报；主办方更新数据并释放 LB 会话；1st 随后又发现新泄漏（文件缺失）再次上报。**技术红利（补充数据）与伦理边界（不用被撤回的 LB 重评分数）被明确分开处理。**

**M6｜私有测试的时序侧信道**：API 按固定顺序服务会话，1st 通过探针确认私榜 = 前 1450/1500 个；他们没有利用"给哪些会话计时"来刷效率分（"gain a place but chose to not use this"）。**这是"能测的测准、能薅的不薅"的罕见组合。**

## 6. 证据分级

| 断言 | 等级 | 说明 |
| --- | --- | --- |
| 噪声 0.0003 与特征准入门槛 | **自述（强）+ 代码公开** | 10 bags 机制完整 |
| 时长/六键特征增益 | **多家一致（1st/7th/9th）** | 独立实现、方向一致 |
| 开放数据重建 98% | **自述（有公开代码/门户）** | 事后可复核 |
| 私榜 1450/1500 会话 | **探针自述** | 与"LB 0.708=(0.698+0.718)/2"的早期观测一致 |
| 4th 的阈值三提交 | **可读取** | 0.61 反事实为作者自述 |
| 9th 的 top-500 逐折选择 | **自述** | 防泄漏做法明确 |
| EDA 的行为特征列表 | **可读取（图）** | 点击散点/游戏截图 |
| 效率分数（1st/7th） | **可读取** | 3–5 分钟推理与分数并列 |

## 7. 边界条件与反事实

- **前提**：游戏数据可从官方门户补充（合法公开数据）；API 固定顺序服务（时序侧信道存在）；18 问共享 level_group 结构。
- **反事实（1st）**：若不做开放数据重建/补充，早期 CV 与最终差约 0.002~0.006（补充 +0.002、全会话交互 +0.002）；若不设噪声门槛，特征膨胀会把 CV 峰值当信号，私榜回落。
- **反事实（4th）**：若只提交 0.62 单阈值，私榜 0.703；三阈值对冲保住 0.703 并曾在 0.60 拿到公开最优；0.61 反事实 0.704（作者"no regrets"）。
- **反事实（9th）**：若不做前序概率特征，CV −0.001；若用 5 折而非 10 折，−0.0005——小增益但方向稳定。
- **伦理边界（本场核心）**：补充数据（合法）与 LB 泄漏（违规）是两件事；1st 的处理给出模板：**发现泄漏 → 上报 → 等主办方处置 → 不在被撤回的数据上做选择**。

## 8. 悬案与失败学

**悬案**

1. **泄漏的最终影响量级**：0.708=(0.698+0.718)/2 的早期推算说明公开 LB 约一半被重建，但重评后名次的公平性讨论未收束；
2. **previous/future 概率注入的边界**（9th +0.001 vs 1st 明确拒绝）缺少同条件对照；
3. **效率分的时序侧信道**（按前 N 个会话计时）存在但被 1st 主动放弃，其潜在量级未知。

**失败学**

| 失败 | 来源 | 教训 |
| --- | --- | --- |
| 逐问题阈值调优 | 1st | 公开更高但不稳；全局阈值更稳 |
| Transformer 直接上（2 小时/折，CV 0.685） | 1st | 计算换成 Conv1D 后 10× 提速、分数不降 |
| LGBM/CatBoost 并入集成 | 1st | ~0.001 更差且不融合，最终只用 XGBoost |
| MMoE 头 | 1st | 不优于简单 MLP |
| NN（LSTM/MLP）单独用 | 9th | 不贡献 CV；异质融合才有价值 |
| 坐标特征 | 1st/4th | 除少量坐标统计外几乎无用（点击行为只在开局 EDA 有信号） |
| 5 折 | 9th/1st | 10 折有小增益；折数也是超参 |
| 未量化噪声就加特征 | 1st 的核心警告 | 小数据宏 F1 的"改进"多数是噪声 |

## 9. 图表证据

> 路径相对本文件（`analysis/deep/`）：`../../intel/predict-student-performance-from-game-play/bodies/<topic>_img/NN.png`

**图 1：时间感知事件（1st 的 NN 表示核心）**（topic 420217）——`../../intel/predict-student-performance-from-game-play/bodies/420217_img/03.png`

*读图结论*：5 个输入（duration→TimeEmbedding；text/room/fqid/event_name→Embedding）；时长嵌入与各事件嵌入**逐元素相乘**后求和 → GAP → 24 维向量。等价于 `duration×(event+room+text+fqid)`——用时间调制事件语义。

**图 2：两阶段训练之预训练（1st）**——`../../intel/predict-student-performance-from-game-play/bodies/420217_img/05.png`

*读图结论*：每个 level_group 的 backbone 在**全部可用会话**（含未完成）上训练，配临时 MLP 头做 BCE——"embedder"阶段最大化数据利用。

**图 3：两阶段训练之端到端（1st）**——`../../intel/predict-student-performance-from-game-play/bodies/420217_img/06.png`

*读图结论*：冻结三个 level_group embedder；q1-3 用 1×d_model、q4-13 用 2×拼接、q14-18 用 3×拼接 → MLP/FF → BCE，以全局 F1 监控——**表示按问题组逐级加宽**。

**图 4：开局点击 EDA（Chris Deotte）**（topic 387864）——`../../intel/predict-student-performance-from-game-play/bodies/387864_img/04.png`

*读图结论*：11.5k 用户"第一次点击"的屏幕坐标散点（黄框=弹窗边界），可见 Grampa/笔记本/导航等簇——**点击位置与停顿时间就是特征来源**；19 个房间均有点击地图。

## 10. 对既有笔记/playbook 的修订点

1. `notes/tabular/predict-student-performance-from-game-play.md` 升级：补齐 8 节作者/票数；方案谱系扩为 5 方案对照矩阵；新增噪声准入门槛、时间感知事件、两级训练、泄漏事件时间线、阈值纪律、图证与失败学。
2. `playbook/tabular.md` 增补：
   - **行为日志的时长/间隔特征族**（业务实体聚合 + 必经事件 checkpoint）；
   - **噪声门槛协议**（bags×folds + 共识折 + >噪声才准入）；
   - **level/组结构的表示拼接**（1×/2×/3× 随问题组加宽）；
   - **阈值纪律**（全局 > 逐问题；提交层面小幅对冲）。
3. `playbook/00-通用方法论.md` 增补：
   - "**量化噪声再谈改进**"（与 pF1/CMC 的代理指标、rogii 的 LCO 同族）；
   - "**外部数据的合法性边界**"：公开门户补充数据可、被撤回的 LB 泄漏不可；发现泄漏上报而非利用。

## 11. 出处

- 开局 EDA（Chris Deotte，228 票）：https://www.kaggle.com/competitions/predict-student-performance-from-game-play/discussion/387864
- 游戏攻略（pjmathematician，212 票）：https://www.kaggle.com/competitions/predict-student-performance-from-game-play/discussion/384796
- 1st（Bertrand P，168 票）：https://www.kaggle.com/competitions/predict-student-performance-from-game-play/discussion/420217
- 7th/效率第 1（Jack，102 票）：https://www.kaggle.com/competitions/predict-student-performance-from-game-play/discussion/420119
- 9th（Makotu，81 票）：https://www.kaggle.com/competitions/predict-student-performance-from-game-play/discussion/420046
- 1st 代码（67 票）：https://www.kaggle.com/competitions/predict-student-performance-from-game-play/discussion/420332
- 13th（Takoi，52 票）：https://www.kaggle.com/competitions/predict-student-performance-from-game-play/discussion/420077
- 4th（Joel Erikanders，48 票）：https://www.kaggle.com/competitions/predict-student-performance-from-game-play/discussion/420349
- 未收录缺口（登记备查）：24 条 write-up 标记中的其余条目（2nd/3rd/5th/6th 等）
