# CMI Detecting Sleep States 深读：事件级指标的两级流水线

> 赛事：Featured ｜ 主题 tabular（传感器时序）｜ 1868 队 ｜ 代码赛 ｜ 指标 事件级 F1（多档容差，onset/wakeup 平均）（2023-11-21 截止）
> 材料基础：`digests/child-mind-institute-detect-sleep-states.md`（8 节：1st/2nd/3rd/4th×2/7th/11th + 社区 UNet2D）+ 36 张图
> 深读时间：2026-10（Tier A #26）

## 0. 一句话重述：这道题真正在考什么

题面是"从腕表传感器时序检测入睡/醒来事件"，实际被考的是**为"事件级容差指标"设计完整的两级检测系统**：

1. **数据几何**：12 步/分钟 × 1440 分钟 = **17280 步/夜**（每步 5 秒）；每晚最多 2 个事件；同受试者多夜 → 必须按 series 分组；
2. **指标结构决定一切**：事件匹配有**多档容差**（12/36/60/… 步，即 1–30 分钟量级）；提交时间戳在 30 秒内的差异不影响分数；AP/F1 奖励"追加低分预测"（11th 的 +0.050、2nd 的第三阶段）——**把指标读透就能白拿分**；
3. **目标整形**：衰减/Gaussian 目标（1st/penguin）、逐 epoch 衰减（1st 的 +19pt）、容差扩张（3rd）、near-miss 忽略（7th）——把"点定位"软化到"容差窗口内放置质量"；
4. **两级流水线是标准形态**：一级序列模型（CNN↓→GRU→CNN↑ / UNet+Transformer / Wavenet / 1D-CNN-UNet）+ 二级候选重排（LGBM 重打分、1st 的逐点得分估计与贪心选择、7th 的 stacking、11th 的 rerank）；
5. **公开榜不可信**：3rd"被公开榜搞晕"、4th 的 WBF 公开涨私榜跌、7th"公开榜不值得信任，专注 CV"——本场私有更贴近 CV。

一句话：**这是一场"指标驱动的系统设计"比赛**——模型结构（GRU/UNet/Wavenet）差异不大；分差来自目标整形、候选重排、后处理与"追加预测"的套利。

## 1. 材料与角色

| 帖子 | 作者 | 票数 | 角色与独有信息 |
| --- | --- | --- | --- |
| [452940](https://www.kaggle.com/competitions/child-mind-institute-detect-sleep-states/discussion/452940)（UNet2D，206 票） | 213tubo | 206 | 社区基建：feature extractor（CNN/LSTM/谱图/PANNs）→ UNet 热图 → decoder（UNet1D/LSTM/MLP/Transformer）；指标二分加速技巧 |
| [459596](https://www.kaggle.com/competitions/child-mind-institute-detect-sleep-states/discussion/459596)（11th，186 票） | Chris Deotte | 186 | **QA 头（1440 类 softmax）代替 NER**；"追加预测"技巧 +0.050；rerank +0.020；NMS+WBF +0.010 |
| [459627](https://www.kaggle.com/competitions/child-mind-institute-detect-sleep-states/discussion/459627)（2nd，177 票） | K_mat | 177 | **三阶段**：检测 → LGBM 按"≤2 事件/天"重打分 → 偏移预测+打分；消融 0.826→0.832→0.842→0.844 |
| [459715](https://www.kaggle.com/competitions/child-mind-institute-detect-sleep-states/discussion/459715)（1st，168 票） | sakami | 168 | **单模型 + 完整改进步进账**（0.7510→0.8206 CV）；衰减目标/周期过滤/min 特征；后处理让公开 0.768→0.790、私榜 0.829→0.852 |
| [459599](https://www.kaggle.com/competitions/child-mind-institute-detect-sleep-states/discussion/459599)（3rd，77 票） | Fnoa | 77 | 7 特征 GRU+UNET+LGB；**噪声检测**（同值重复）；反转序列增强 +0.01；消融表 |
| [459598](https://www.kaggle.com/competitions/child-mind-institute-detect-sleep-states/discussion/459598)（7th，70 票） | Ahmet Erdem | 70 | Wavenet（3 天分钟级）；near-miss 负标签；OHEM 50%；6 epoch×18s；stacking 只 +0.001 |
| [459637](https://www.kaggle.com/competitions/child-mind-institute-detect-sleep-states/discussion/459637)（4th Nikhil，68 票） | NikhilMishra | 68 | UNet+Transformer+GRU/LSTM；patch 降长；**WBF 公开涨 0.003、私榜跌 0.001** 的诚实记录 |
| [459597](https://www.kaggle.com/competitions/child-mind-institute-detect-sleep-states/discussion/459597)（4th penguin46，64 票） | penguin46 | 64 | 19200 步按 12 步 patch；1/8 位移 8× 平均；GGIR 缺失识别特征；reduce_rate 后处理 |

**材料缺口（未扩采，登记备查）**：38 条 write-up 标记中收录 8 节（5th/6th/8th/9th 等未收）。

## 2. 逐方案对照矩阵

| 维度 | 1st sakami | 2nd K_mat | 3rd Fnoa | 4th penguin46 | 7th Ahmet | 11th Chris |
| --- | --- | --- | --- | --- | --- | --- |
| 一级模型 | CNN↓→残差 GRU→CNN↑ | 1D-CNN UNet（事件+sleep/wake 双头） | GRU / UNET（7 特征） | Transformer/Wavenet/1DCNN + GRU；19200 patch 12 | Wavenet（3 天分钟级，双头 CE+BCE） | CNN-Transformer-GRU / Deep-GRU（TF） |
| 目标整形 | **逐 epoch 衰减的容差目标** | 检测 + 分类双头 | ±1 扩张、CE | Gaussian（var=36 步） | +3 偏移、near-miss=-1、OHEM | 1440 类 QA softmax |
| 二级/后处理 | **二级模型 + 容差得分 + 贪心折扣选择** | LGBM 重打分（≤2 事件/天）+ 第三阶段偏移 | 峰值间隔优化 | NMS-like reduce_rate 折扣 | 峰值选择 + LGBM stacking | 追加预测 + rerank + NMS/WBF |
| 数据/特征 | 日切块 0.35 偏移、周期过滤、分钟嵌入 | 峰值候选上下文 + 长周期特征 | 7 特征（std/噪声/时刻频率编码） | 24h 匹配计数、HDCZA、lags | 波动率窗口、同分钟前后天 diff | 日切块含双事件；块作为 crop 增强 |
| 成绩 | CV 0.8206；私榜 0.852（含 PP） | CV 0.844 | CV 0.840/公开 0.784/私榜 0.848 | CV 0.825/公开 0.784/私榜 0.840 | CV 0.826 | CV ~0.80 |

## 3. 共识、分歧与裁决

### 共识一：事件级指标必须"两级化"处理（全员）

一级模型输出逐点/逐分钟概率；二级对候选做全局重排：1st 的二级模型 + 容差得分贪心选择；2nd 的 LGBM 重打分（显式建模"≤2 事件/天"）；7th 的 stacking；11th 的 rerank；4th 的 NMS/WBF。**单靠逐点阈值都到不了前排**。

**裁决**：检测类指标（有多档容差 + 全局约束）的正确答案是"候选生成 + 全局重排"；把指标结构写进二级模型（1st 的 tolerance_12/36/60 求和）是最直接的优化。置信度最高。

### 共识二：目标整形要匹配指标的"容差几何"（多种实现）

1st 的衰减目标（每个 epoch 再衰减，让峰更细）贡献 +19pt；penguin 的 Gaussian（var=36 步）；3rd 的 ±1 扩张；7th 的 +3 偏移与 near-miss 忽略。**共同点：不要惩罚容差窗口内的偏移，不要奖励窗口外的锐度**。

**裁决**：先读指标的匹配规则，再设计 target（与 rogii 的"指标感知后处理"同族，L25）。置信度高。

### 共识三：公开榜噪声大，CV→私榜相关性更强（3rd/4th/7th 一致）

3rd："公开榜让人头晕，以为代码有 bug"；4th Nikhil：WBF 公开 +0.003 私榜 −0.001；7th："公开榜不值得信任，专注 CV"。1st 的 CV 0.8206 对私榜 0.829（"相当于第 9 名"），也说明 CV 校准良好。

**裁决**：本场应以 CV 为主、公开榜只做 sanity check（与 ubiquant 的"多轮口径"、llm-detect 的"公开陷阱"构成同一族边界条件）。置信度高。

### 分歧一：范式之争——NER（逐点分类）vs QA（1440 类选择）

11th 的 QA 头（每天 1440 类 softmax 选分钟）+ 单独分类器去假阳性；其余人用 NER/回归 + PP。11th 自评"不是公开 notebook 里的做法"，其模型 CV ~0.80。

**裁决**：QA 范式天然匹配"每天至多 2 个事件 + 容差匹配"，且便于用"追加预测"技巧；但它需要额外的假阳性分类器。两条路线都能到前排，无一方压制另一方。置信度中。

### 分歧二：WBF 到底有没有用？

feedback-2021 中 WBF 是夺冠关键；本场 4th Nikhil：WBF 公开 +0.003、**私榜 −0.001**（"so WBF hurt"），团队改用其精炼版；11th：NMS+WBF +0.010（CV/LB 一致）。7th/2nd 也用 WBF 类融合。

**裁决**：融合方法的收益依赖候选分布与容差结构；同一手法在不同场次/不同候选质量下符号可以翻转——**必须用私榜（或强 CV）验证**。置信度中高。

## 4. 增量数字账

| 动作 | 数字 | 来源 |
| --- | --- | --- |
| 1st 的改进步进账（CV） | baseline 0.7510 → 逐 epoch 衰减目标 +19pt → 周期过滤 +11pt → 周期 flag 入输入 +6pt → bs/hidden/层数调整 +11pt → 每日分数归一 +6pt → 去掉 month/day +7pt → 裁 30 分钟边缘 +4pt → 分钟特征接末层 +6pt = **0.8206** | 1st |
| 1st 的两级后处理 | 公开 0.768→**0.790**；私榜 0.829→**0.852** | 1st |
| 2nd 的三阶段消融 | 1st stage 0.826 → +LGBM 重打分 0.832 → +偏移预测 0.842 → +双模型集成 0.844 | 2nd |
| 3rd 的特征消融（CV/公开） | Just std 0.786/0.747；+噪声 0.803/0.756；+时刻信息 0.796/0.764；全部 **0.817/0.767** | 3rd |
| 3rd 的反转序列增强 | 本地 +0.01 | 3rd |
| 4th Nikhil | WBF 公开 0.79→0.793、私榜 −0.001；团队融合 CV 0.835/公开 0.793/私榜 0.845 | 4th Nikhil |
| 4th penguin | NN:GBDT:tubo=5:2:3；CV 0.825/公开 0.784/私榜 0.840 | penguin |
| 7th 的训练效率 | 6 epoch × **18 秒**/RTX3090；提交 30 分钟 | 7th |
| 7th 的 stacking | AUC 明显提升、指标仅 +0.001；另一 LSTM+Transformer 模型 +0.001 | 7th |
| 11th 的追加预测 | 每晚取第 1…30 个候选、第 k 个分数 /2^(k-1)：**CV +0.050** | 11th |
| 11th 的 rerank | CatBoost+1D/2D-UNet+Mel+ResNet/EffNet 等重打分：CV +0.020 | 11th |
| 11th 的融合 | NMS+WBF：+0.010 | 11th |
| 4th Nikhil 的 patch | 17280 → 17280//patch（patch 3–6）→ 序列缩短、训练可行 | 4th Nikhil |
| penguin 的 8× 平均 | 19200 步按 1/8 位移滑窗，每位置预测 ~8 次平均 | penguin |

**可复算校验（3 处吻合）**

1. 17280 步/夜 = 12 步/分 × 60 分 × 24 时 ✓（每步 5 秒）；
2. 2880 = 86400/30（3rd 的 30 秒粒度）✓；19200/12 = 1600（penguin 的 patch 长度）✓；
3. 11th：200 用户 × ~30 夜 × 2 事件 ≈ **12,000** 个首个候选 ✓（其"追加 30 个猜测/夜"的账目自洽）。

## 5. 机制推演

**M1｜为什么衰减目标有效**：多档容差指标只要求"预测落在窗口内"；刚性 0/1 目标迫使模型在单步上过度自信，而沿容差递减的软目标让概率质量在窗口内均匀铺开；逐 epoch 继续衰减是把"检测"逐步退火成"定位"（1st：+19pt，全场单步最大）。**推论：换任何"容差型事件指标"，第一件事是把 target 改成与容差同形状的核。**

**M2｜为什么需要"按天的全局重排"**：一级模型只看局部窗口，无法表达"这一晚最多 2 个事件、且候选之间互相竞争"；二级 LGBM 用候选上下文（排名、间隔、跨天统计）做 day-level 重排——2nd 的对照（第 3 候选 0.20 vs 第 1 候选 0.19 谁更重要）正是其动机。**指标含全局约束时，局部最优必须升级为全局最优。**

**M3｜AP 类指标的"追加预测"为什么白拿分**：排序型指标中，若新预测的分数低于已提交的所有预测，它只会增加分母/可能命中真值，按构造不会降低 AP；11th 把每晚取到 Top-30（除以 2^k 降权）→ +0.050。**这是"读指标定义"的直接套利（与 llm-prompt-recovery 的指标攻击、rsna 的多阈值提交同族）。**

**M4｜周期过滤的机制**：设备被摘下时，GGIR 用同日其他时间均值填充 → 产生 24h 周期信号；识别并过滤它（1st 规则式检测 + 输入 flag + 输出滤除）避免把"设备缺失"当睡眠事件。**领域语义（传感器佩戴表）是这条规则的来源。**

**M5｜长序列工程为何决定上限**：17280–19200 步的原始序列无法直接进 RNN；各家用下采样（30s）、patch（12 步）、日切块、滑窗重叠平均来"在可训练的计算量内保留定位精度"；1st 的块边缘裁剪 30 分钟（+4pt）说明边界伪影是真实误差源。

**M6｜公开榜噪声的来源与对策**：公开子集小 + 事件级指标的双重随机性（每夜 1–2 个事件的匹配）+ 提交时间戳容差 → 公开榜的方差远大于 CV；因此 3rd/7th 明确"以 CV 为准"，4th 用团队融合稳定选择。**事件稀疏 + 小榜 = 榜单排序不可信（与 rogii/L6 同构）。**

## 6. 证据分级

| 断言 | 等级 | 说明 |
| --- | --- | --- |
| 1st 的逐步 +pt 账 | **可读取（帖内 log）** | 9 步递进，单变量为主 |
| 1st 的后处理增益（公开 +0.022/私榜 +0.023） | **可读取** | 与最终分数一致 |
| 2nd 的三阶段消融 | **可读取（表）** | 0.826→0.844 逐步 |
| 3rd 的特征消融 | **可读取（图）** | CV/公开双列；CV 与公开排序部分不一致 |
| 11th 的 +0.050/+0.020/+0.010 | **自述（强）** | 有机制解释与代码 |
| 4th 的 WBF 私榜 −0.001 | **自述（诚实的负面）** | 团队仍用其精炼版 |
| penguin 的 GGIR 特征 | **自述** | 引用 tatamikenn 的 HDCZA notebook |
| 7th 的 18s/epoch | **自述** | 硬件 RTX3090 |

## 7. 边界条件与反事实

- **指标绑定**：所有"目标整形/后处理"技巧都依赖"多档容差 + AP/F1 结构"；若换成逐点 ROC/AUC，答案完全不同（1st 的 +19pt 目标衰减将不再成立）。
- **反事实（11th）**：若不做"追加预测"，直接损失 ~0.05 CV——这是本场最大的单项免费收益；若 QA 头配更好的假阳性分类器，其模型上限可能进一步提升。
- **反事实（4th Nikhil）**：若以公开榜为准选 WBF 版本，私榜会低 0.001（团队选择了精炼版后处理）——**融合方法的符号在不同候选质量下翻转**。
- **反事实（1st）**：若不做周期过滤与输入 flag，CV −17pt（11+6）；若忽略块边缘（不裁 30 分钟），CV −4pt。
- **边界（数据语义）**：装置缺失的周期模式、GGIR 的均值填充、同值重复噪声——这些"数据管线人造痕迹"是特征与过滤器的来源；换采集设备/处理管线，技巧需重做。

## 8. 悬案与失败学

**悬案**

1. **NER vs QA 的范式上限**：11th 的 QA 路线 CV ~0.80，未与同资源 NER 严格对照；
2. **公开榜方差的量化**：无官方样本量/匹配方差估计，"公开不可信"是经验结论；
3. **LGBM 二级的完整潜力**：3rd 只在最后一天做出贡献（+0.002 私榜），2nd 的二级是核心——树模型在事件重排上的上限未被完全挖掘。

**失败学**

| 失败 | 来源 | 教训 |
| --- | --- | --- |
| WBF 直接套用（公开涨、私榜跌） | 4th Nikhil | 融合方法的收益要按私榜/强 CV 验证 |
| ranking 重排器（reranker） | penguin | 未成功；候选重排需要专门设计（2nd 的 LGBM 成功） |
| 直接用匹配数量做回归目标 | penguin | 无效；软标签才是正解 |
| 更长序列 / BigBird 稀疏注意力 / focal loss / 伪标签 / 复制粘贴增强 / 手工标注 | penguin | 负面清单：长序列与复杂注意力不划算 |
| stacking AUC 提升但指标不动 | 7th | 排序指标对 AUC 式改进不敏感 |
| 追求公开榜排名 | 3rd/7th | 公开方差吞掉模型差异；专注 CV |
| 只做峰值检测（无二级重排） | 1st/2nd 的对比 | 单点后处理到不了前排 |

## 9. 图表证据

> 路径相对本文件（`analysis/deep/`）：`../../intel/child-mind-institute-detect-sleep-states/bodies/<topic>_img/NN.ext`

**图 1：1st 的模型结构（CNN 下采样 → 残差 GRU → CNN 上采样）**（topic 459715）——`../../intel/child-mind-institute-detect-sleep-states/bodies/459715_img/01.jpeg`

*读图结论*：DownConv1/2/3 → GRU → UpConv1/2/3 → Critical Point Probabilities——长序列"下采样→序列建模→上采样"的标准定位范式的直接图证。

**图 2：1st 的衰减容差目标**（1st）——`../../intel/child-mind-institute-detect-sleep-states/bodies/459715_img/02.png`

*读图结论*：以事件（step≈4970）为中心的三角衰减核，随距离分档降到 0——目标形状与指标的容差几何同构；且每个 epoch 继续衰减（图中为某一时刻的 target 形态）。

**图 3：2nd 的三阶段流水线**（topic 459627）——`../../intel/child-mind-institute-detect-sleep-states/bodies/459627_img/01.png`

*读图结论*：1st stage 1D-CNN UNet（sleep/wake + event 双头）→ 峰值候选（STEP/SCORE/EVENT 表）→ **2nd stage LGBM 按"≤2 事件/天"重打分**（图中直接画出"第 3 候选 0.32 vs 次日第 1 候选 0.25"的动机）→ 3rd stage 偏移预测（1522/9202/…）与分数预测 → 拼接成 submission。

**图 4：11th 的 QA 头（1440 类 softmax）**（topic 459596）——`../../intel/child-mind-institute-detect-sleep-states/bodies/459596_img/03.png`

*读图结论*：一天 1440 分钟 = 1440 个类，onset=1 为正确分钟——把"事件检测"转成"QA 式选择"，与逐点 NER 的区别一目了然（配合其"追加预测"技巧使用）。

**图 5：3rd 的特征消融（CV 与公开排序不一致）**（topic 459599）——`../../intel/child-mind-institute-detect-sleep-states/bodies/459599_img/04.png`

*读图结论*：Just std 0.786/0.747 → +noise 0.803/0.756 → +time 0.796/0.764 → all 0.817/0.767。**注意 +time 的 CV 低于 +noise 但公开更高**——正是本场"公开榜噪声大、排序不可信"的微观证据。

## 10. 对既有笔记/playbook 的修订点

1. `notes/tabular/child-mind-institute-detect-sleep-states.md` 升级：补齐 8 节作者/票数；方案谱系扩为 6 方案对照矩阵；新增目标整形、两级流水线、追加预测套利、周期过滤、公开榜方差、图证与失败学。
2. `playbook/tabular.md`（事件/时序节）增补：
   - **容差型事件指标的 target 设计**（衰减/Gaussian 核 + 逐 epoch 退火）；
   - **两级化配方**（序列模型候选 + 全局重排 LGBM/贪心选择）；
   - **排序型指标的追加预测规则**（低分追加不伤 AP → 主动追加）；
   - **长序列工程**（下采样/patch/滑窗平均/边缘裁剪）；
   - **数据管线人造痕迹**（设备缺失周期、同值重复噪声）作为特征与过滤器。
3. `playbook/00-通用方法论.md` 增补："**先把指标写成代码**"——本场的 +0.05 追加与 +19pt 目标衰减都来自逐字阅读指标定义；与 llm-prompt-recovery 的"指标病理学"、rsna 的阈值网格同族。

## 11. 出处

- UNet2D 社区帖（213tubo，206 票）：https://www.kaggle.com/competitions/child-mind-institute-detect-sleep-states/discussion/452940
- 11th（Chris Deotte，186 票）：https://www.kaggle.com/competitions/child-mind-institute-detect-sleep-states/discussion/459596
- 2nd（K_mat，177 票）：https://www.kaggle.com/competitions/child-mind-institute-detect-sleep-states/discussion/459627
- 1st（sakami，168 票）：https://www.kaggle.com/competitions/child-mind-institute-detect-sleep-states/discussion/459715
- 3rd（Fnoa，77 票）：https://www.kaggle.com/competitions/child-mind-institute-detect-sleep-states/discussion/459599
- 7th（Ahmet Erdem，70 票）：https://www.kaggle.com/competitions/child-mind-institute-detect-sleep-states/discussion/459598
- 4th Nikhil（68 票）：https://www.kaggle.com/competitions/child-mind-institute-detect-sleep-states/discussion/459637
- 4th penguin46（64 票）：https://www.kaggle.com/competitions/child-mind-institute-detect-sleep-states/discussion/459597
- 未收录缺口（登记备查）：38 条 write-up 标记中的其余条目（5th/6th/8th/9th 等）
