# BirdCLEF 2022 深读：稀有类分组 × 损失分工 × 阈值校准

> 赛事：Research ｜ 主题 audio（鸟类声音识别）｜ 801 队 ｜ 代码赛 ｜ 指标：Weighted Categorization Accuracy（仅 21 个 scored birds）
> 材料基础：`digests/birdclef-2022.md`（6 篇：抄袭举报 177 票/实验分享 156/1st models 63/public#1-private#2 59/3rd 56/起点帖 51；80 条索引）+ 3 张图
> 深读时间：2026-10（Tier A #51，**Batch 6 首场**）

## 0. 一句话重述：这道题真正在考什么

题面是"识别声景中的鸟鸣，但只对 21 个 scored birds 计分"，实际被考的是**稀有类分工 + 阈值校准**：

1. **类内极端不平衡**：21 个计分鸟中 14 种有 ≥10 条训练样本（Group1），7 种极少（Group2，最少的 `maupar` 只有 1 条，被拆成 5 份使用）。稀有类不能与常见类共用一套损失与阈值。
2. **损失分工是 3rd 的核心发现**：focal loss 对小类召回更友好但更"保守"，BCE 对大类更准——**按样本量把鸟分成两组，Group1 用 BCE（CNN+SED）、Group2 用 focal（SED）**，配合逐鸟阈值可带来 0.02–0.03 提升（其对照：SED-BCE 私 0.7563 vs SED-focal 私 0.8135）。
3. **阈值是隐形大杠杆**：指标是"切片 → clipwise 概率 → 阈值 → 多标签准确率"；逐鸟阈值（0.05/0.35）、分位数阈值（测试分布自适应，0.25）、非目标分布 91 分位（等价固定 FPR）三种策略并存；3rd 直言"没有合适阈值就看不出模型真实性能"。
4. **骨架是 SED + secondary labels**：tattaka 的 BirdCLEF 2021 4th 方案（SED、clipwise/framewise/attention 头、BCE2wayLoss/BCEFocal2WayLoss）被 1st/3rd/起点帖全员复用；标签用软权重（primary 0.9995 / secondary 0.5 / other 0.0025）。
5. **BirdNET 事件**：主办方自己的 BirdNET 模型覆盖 20/21 scored birds，license 澄清后允许使用；public#1/private#2 方案靠它拿到公榜 0.91，但私榜跌到 0.84——**公榜红利的教科书案例**；1st 的最终融合也包含 BirdNET。
6. **治理插曲**：全站最高票帖（177）是"抄袭举报"——三个复制粘贴 kaerururu notebook 的 notebook 获得高赞；社区用举报与署名规范维护分享生态。

一句话：**这是一场"稀有类分工 + 阈值校准"的音频检测赛**——模型骨架是 SED/CNN，胜负在损失与阈值的分组设计。

## 1. 材料与角色

| 帖子 | 作者 | 票数 | 角色与独有信息 |
| --- | --- | --- | --- |
| [321202](https://www.kaggle.com/competitions/birdclef-2022/discussion/321202) 抄袭举报 | — | 177 | 三个 copy-paste notebook（含标题自称复制）；呼吁举报；社区治理与署名规范 |
| [318081](https://www.kaggle.com/competitions/birdclef-2022/discussion/318081) 实验分享 | kaerururu | 156 | 公共训练/推理代码 + 4 分片 audio-to-numpy 数据集；被广泛复用（也解释了抄袭事件的对象） |
| [327047](https://www.kaggle.com/competitions/birdclef-2022/discussion/327047) 1st models | — | 63 | SED（tattaka）+ tf_efficientnet_b3_ns/eca_nfnet_l0；stride (2,2)→(1,1)；15s chunk；2 阶段（2021+2022 预训练→scored 过滤微调）；3 checkpoint 权重平均；居中 5s head + max；分位数阈值 0.25；最终融合含 BirdNET |
| [326950](https://www.kaggle.com/competitions/birdclef-2022/discussion/326950) public#1/private#2 | — | 59 | 双方案：① 自训 SED/CNN（私 0.79，未选）；② **BirdNET**：20/21 类重合、改 `species_list.txt`；主办方说明 license 允许；公榜 **0.91→私榜 0.84** 大跌 |
| [327193](https://www.kaggle.com/competitions/birdclef-2022/discussion/327193) 3rd | — | 56 | **bird split**：Group1（14 种，≥10 样本）用 BCE CNN+SED；Group2（7 种）用 focal SED；阈值 0.05 / 0.35 / 91 分位；8 CNN+8 SED+12 SED 集成；私榜最佳 0.8274（未选） |
| [308004](https://www.kaggle.com/competitions/birdclef-2022/discussion/308004) 起点帖 | tattaka | 51 | BirdCLEF 2021 4th 方案复用；提示推理耗时（~2h）与"音频赛集成通常有效" |

**材料缺口（受"不扩采"约束，登记备查）**：Previous Audio Competitions(307824,70)、Comment for beginners(324124,63)、7th place solution(326973,45)、评测指标解释帖(314999,49)、与上届变化(309213,56) 等未收录——**7th 方案与指标细节**是主要缺口。

## 2. 逐方案对照矩阵

| 维度 | 1st（models 部分） | 3rd | public#1/private#2 | kaerururu 实验 |
| --- | --- | --- | --- | --- |
| 模型 | SED（tattaka）+ effnet_b3_ns / eca_nfnet_l0；stride 改 (1,1) | CNN（2021 2nd 方案）+ SED（2021 4th） | BirdNET（主办方）+ 自训 SED/CNN | SED + 2nd label 训练 |
| 稀有类处理 | 加权 sampler/loss；2 阶段过滤 scored birds | **bird split + focal/BCE 分工**；小类过采样/手工拆分 | 依赖 BirdNET 覆盖 | 公共基线 |
| 标签 | secondary labels | 软权重 primary 0.9995/secondary 0.5/other 0.0025 | — | 2nd label notebook |
| 阈值 | 分位数阈值 0.25（单模型）；普通阈值 0.2–0.3（集成） | Group1 0.05（skylar 0.35）；Group2 非目标 91 分位 | 后处理 +（未细述） | — |
| 数据/增强 | Gaussian/Pink 噪声、OR-Mixup、背景噪声（2021 nocall/esc50） | mixup/cutmix/spec-augment/背景噪声混入（freefield1010/aicrowd2020/nocall） | BirdNET + 自有增强 | 公共数据集 |
| 验证 | 5 折分层；maupar 拆 5；只算 scored birds 的 LB 代理指标 | "找不到好 CV，主要靠公榜" | — | — |
| 集成 | 3 checkpoint 权重平均 + 多模型融合（含 BirdNET） | 28 模型（8 CNN+8 SED G1+12 SED G2）+ 时间平滑 | 单模型为主 | — |
| 成绩 | 单模型 Val 0.879/0.886、公 0.82、私 0.78 | best public 0.875/私 0.8126；safe 0.8556/0.8071；best private 0.8707/**0.8274**（未选） | BirdNET 公 0.91/私 0.84 | 公 0.71 |
| 失败清单 | —（models 帖未列） | PCEN、加权 BCE、rating 数据、pitch shift、coord-conv；部分增强 | 自训模型私 0.79（未选） | — |

## 3. 共识、分歧与裁决

### 共识一：稀有类必须与常见类分开处理（3rd 的 bird split；1st 的加权/两阶段；全员）

3rd：按样本量把 21 种鸟分成 Group1（≥10 样本，14 种）/ Group2（7 种）；
1st：按 primary_label 计算采样与损失权重，并在第二阶段只保留含 scored birds 的样本微调；
3rd 的对照：SED-BCE 私 0.7563 vs SED-focal 私 0.8135；bird split 组合 0.8052，后续提升到 0.8274。

**裁决**：极端不平衡下的正解是"按类群分组 + 组内选损失/阈值"，而不是全类统一。置信度：高（有分组前后对照）。

### 共识二：阈值校准是模型之外的第二引擎（3rd/1st 明确，多队默认）

3rd：Group1 0.05、skylar 0.35、Group2 用非目标分布 91 分位；"没有阈值就看不出真实性能"；
1st：分位数阈值（0.25）单模型更好、普通阈值（0.2–0.3）集成更好；
public#1：后处理中也要调阈值。

**裁决**：多标签分类指标下，阈值是每个模型集/每个类别都要重新校准的"最后一公里"；分位数阈值（对测试分布自适应）在单模型场景更稳。置信度：高。

### 共识三：SED + secondary labels + 背景噪声增强是骨架（4/4）

1st/3rd：tattaka 的 SED（2021 4th）为骨干；
标签：primary/secondary 软权重；
增强：背景噪声混合（freefield1010/aicrowd2020/2021 nocall）、mixup/cutmix/spec-augment。

**裁决**：音频弱标签赛的通用配方；背景噪声混入直接模拟测试声景的信噪比结构。置信度：高。

### 分歧一：BirdNET 的使用与公榜红利（本场最大争议）

public#1/private#2：直接用主办方 BirdNET（20/21 类重合，改 species_list），license 澄清后允许；公榜 0.91、私榜 0.84；
1st：把 BirdNET 放进最终融合（但自己的模型才是主贡献）；
3rd：**明确"我们没用 BirdNET"**。

**裁决**：BirdNET 在公榜上系统性高估（可能训练数据覆盖 public 片段），私榜红利不可依赖；允许使用但应把它当"外部强模型"审计（对照 T8/T18）。置信度：高（涨跌数字直接）。

### 分歧二：验证与提交选择

3rd："找不到好 CV，主要看公榜"；提交了两个（best public 0.875/0.8126 与低阈值安全版 0.8556/0.8071），最佳私榜 0.8274 未选；
1st：自建 5 折分层 + scored-bird 专用代理指标优化阈值。

**裁决**：阈值敏感 + 小测试集 → public/private 排序翻转频繁；**提交对冲（激进 + 保守）**优于选 public 峰值。置信度：高。

### 分歧三：增强/损失细节的有效性

3rd：mixup（最有影响）、背景噪声、spec-augment、cutmix 有效；PCEN、加权 BCE、rating 数据、pitch-shift、coord-conv 无效；
1st：Gaussian/Pink 噪声 + OR-Mixup + 背景噪声有效。

**裁决**：**模拟测试声景的增强（噪声/混音）**稳定有效；特征级（PCEN）与标签费率类改动无收益。置信度：中高。

## 4. 增量数字账

| 动作 | 数字 | 来源 |
| --- | --- | --- |
| 计分范围 | 仅 21 个 scored birds（152 类中的）；Group1 14 种 ≥10 样本；Group2 7 种（maupar 仅 1 条拆 5） | 3rd |
| 3rd 单模型 | CNN 无增强 0.7715/0.7278；CNN 增强 0.7761/0.7359（公/私） | 3rd |
| 3rd 纯集成 | CNN 集成 0.8327/0.7898；SED 4 折 0.8339/0.7823 | 3rd |
| 3rd bird split | 组合 0.8532/0.8052；更多模型 0.8750/0.8126（best public）；安全版 0.8556/0.8071；**best private 0.8707/0.8274（未选）** | 3rd |
| 3rd 损失对照 | SED-BCE 私 0.7563 vs SED-focal 私 0.8135；CNN-BCE 私 0.7678 | 3rd |
| 3rd 阈值 | Group1 0.05；skylar 0.35；Group2 非目标 91 分位 | 3rd |
| 1st 单模型 | effnet_b3_ns Val .8789/公 .82/私 .78；eca_nfnet_l0 Val .8864/公 .82/私 .78 | 1st |
| 1st 训练 | 15s chunk；stride (2,2)→(1,1)；2 阶段（2021+2022→scored 过滤）；3 checkpoint 平均；分位数阈值 0.25 | 1st |
| BirdNET | 公榜 0.91→私榜 0.84 大跌；CPU <2h vs 自训 GPU ~8h；20/21 类重合 | public#1 |
| 自训方案 | 私榜 0.79（未选）；Top5 邻域时序后处理（±5s 内检出则补 top5 类） | public#1 |
| 赛事 | 801 队；Weighted Categorization Accuracy；80 帖 | 元数据 |

**结构校验（2 处吻合）**

1. 3rd 的"focal 保小类、BCE 保大类"与其分组前后分数（0.8052→0.8274 私榜）自洽 ✓；
2. BirdNET 的"公高私低"与 public#1 的"public 红利"判断自洽 ✓。

## 5. 机制推演

**M1｜为什么 focal/BCE 需要分工**：focal loss 降低易样本权重 → 小类（样本极少）获得相对更大的有效梯度、召回高，但概率分布更保守（阈值处更敏感）；BCE 对样本充足的大类校准更好。**分组后每组用与自身样本量匹配的损失**，等价于类别级的损失条件化。

**M2｜阈值的经济学**：指标是"clipwise 概率 → 阈值 → 多标签准确率"，不同类别/损失的输出尺度不同；逐类阈值是不可省的校准自由度。分位数阈值用测试期分布自适应（对分布漂移稳健）；非目标分布 91 分位等价于把 FPR 固定，两者都是"用未标注测试分布做校准"的合法手段。

**M3｜secondary labels 的信息量**：声景录音常含多种鸟鸣；只标 primary 会丢弃信息。软权重（primary 1 / secondary 0.5 / other 0.0025）让模型从"可能标签"中学习，是音频弱标签赛的标准做法（与 cmi-behavior 的弱标注处理同族）。

**M4｜背景噪声混入为什么关键**：测试是长声景（多背景噪声），训练是近场录音；把训练片段与真实背景（freefield1010、aicrowd2020、2021 nocall）叠加，模拟测试的 SNR/信道结构 → 域适应式增强。比"换更复杂模型"更直接命中分布差异。

**M5｜BirdNET 的公榜红利**：主办方模型可能训练于覆盖 public LB 片段的公开数据，且本身是强模型；它在公榜上把分数推到 0.91，但私榜回落 0.84。**公榜与私榜的差距量化了"外部模型的红利"，也说明只信公榜的危险**（对照 T3/T8/T18）。

**M6｜治理生态**：高赞的复制粘贴 notebook 会抽走原创分享的激励；本场抄袭举报成为最高票帖。**知识分享生态需要署名/举报机制维护**，这也是 Kaggle 学习者应内化的规范（引用来源、注明 fork）。

## 6. 证据分级

| 断言 | 等级 | 说明 |
| --- | --- | --- |
| bird split 与损失对照 | 自述 + 3 张分布图 + 公开推理 kernel | 高 |
| BirdNET 公/私涨跌 | public#1 自述（含主办方 license 说明） | 高 |
| 1st 的 SED/两阶段/阈值 | 自述 + GitHub + kernel 链接 | 中高 |
| 抄袭举报 | 三个 notebook 可核 | 高 |
| kaerururu 实验帖 | 公共 notebook/数据集（可复现） | 高 |
| 3rd 的"找不到好 CV" | 自述 | 中 |

## 7. 边界条件与反事实

- **反事实 1**：全类统一损失/阈值 → 3rd 的组间对照（SED-BCE 私 0.7563 vs focal 0.8135；分组后 0.8274）。
- **反事实 2**：用 0.5 统一阈值 → 稀有类漏检/常见类误报；逐类阈值与分位数阈值是必需。
- **反事实 3**：只用 BirdNET → 公榜 0.91/私榜 0.84 的落差；私榜排名不可控。
- **反事实 4**：按 public 峰值选提交 → 3rd 的最佳私榜 0.8274 未选（选中的是 0.8126/0.8071）。
- **边界**：结论依赖"评分只覆盖部分类别 + 测试为长声景 + 允许阈值校准/多次提交"；闭集、均衡类别的音频分类不需要此类分工。

## 8. 悬案与失败学

**悬案**

1. **BirdNET 是否被正式认定为"允许的宿主红利"**：主办方在 issue 中同意不执行非商业条款，但对其是否构成不公平优势无结论；1st 的融合里也含 BirdNET。
2. **public→private 大跌的机制**未证实（可能 public 片段进入 BirdNET 训练数据）。
3. 7th 方案（326973）与指标解释帖未收录；"Previous Audio Competitions"（307824）未收录。
4. 3rd 的"找不到好 CV"具体尝试清单未展开。

**失败学（跨队合集）**

- 特征类：PCEN、加权 BCE（按类频次）、rating 数据、pitch-shift、coord-conv（3rd 的负结果）。
- 增强类：SED 上的 mixup、RandomLowpassFilter（3rd）；"augment only scored birds"、"multiply loss ×10"（3rd）。
- 流程类：复制粘贴 notebook（治理）；推理耗时 2h 未优化（起点帖）；只按公榜选提交（3rd 的教训）。

## 9. 图表证据

> 路径相对本文件（`analysis/deep/`）：`../../intel/birdclef-2022/bodies/<topic>_img/NN.png`

**图 1：小类鸟的预测分布（focal vs BCE）**（topic 327193）——`../../intel/birdclef-2022/bodies/327193_img/01.png`

*读图结论*：`hawhaw`（4 个目标样本）与 `hawpet1`（2 个）：SED-focal（紫/青）在目标样本上给出高峰、非目标压在低位；Slime-CNN/BCE（红/蓝）对非目标也给出中高概率。**focal 保小类**的直接图证。

**图 2：大类鸟的预测分布（BCE 更准）**（topic 327193）——`../../intel/birdclef-2022/bodies/327193_img/02.png`

*读图结论*：`skylar`（125 目标）/`warwhe1`（18 目标）：BCE 模型（红/蓝）对大类更可靠；因此大类用 BCE、并给 skylar 单独设 0.35 阈值。

**图 3：逐鸟非目标分布与阈值选择**（topic 327193）——`../../intel/birdclef-2022/bodies/327193_img/03.png`

*读图结论*：21 种鸟的非目标概率分布（中位数 0.010–0.038）；红色竖线=Group1 统一阈值 0.05；`skylar` 中位明显偏高 → 手动 0.35；Group2 用各自分布的 91 分位。**阈值必须逐类校准**的完整图证。

## 10. 对既有笔记/playbook 的修订点

1. `notes/audio/birdclef-2022.md` 升级（现仅 26 行浅笔记）：补 6 篇作者/票数、四方案 × 8 维对照、数字账（0.7563 vs 0.8135、0.8274 未选、0.91→0.84）与 3 张图证；新增"稀有类分组"与"阈值校准"节。
2. `playbook/multimodal-audio-other.md`（音频识别节）增补：
   - **稀有类分工**：按样本量分组，组内选损失（focal 保小类/BCE 保大类）与阈值；
   - **阈值工程**：逐类阈值、分位数阈值（测试分布自适应）、非目标分位（固定 FPR）；
   - **SED + secondary labels**：软权重弱标签、clipwise/framewise 双头；
   - **背景噪声混入**（freefield1010/aicrowd/nocall）模拟测试声景；
   - **公榜红利审计**：外部强模型（如 BirdNET）公榜高估，提交对冲（激进+保守）。
3. `playbook/00-通用方法论.md` 增补：**"阈值是分类指标的第二引擎"**（与 essay 的 QWK 阈值同族）；**"外部强模型的公榜红利"**（对照 T8/T18）；**分享生态规范**（署名/举报，反对复制粘贴）。
4. `analysis/THEORY.md`（Batch 6 末汇总 v0.6）候选：
   - **L77｜类群级损失条件化**（bird split；与 eedi 长尾、pii 稀有类加权同族）；
   - **L78｜阈值校准三策略**（逐类/分位数/非目标分位）；
   - **L79｜外部模型的公榜红利**（BirdNET 0.91→0.84）。

## 11. 出处

- 抄袭举报（177 票）：https://www.kaggle.com/competitions/birdclef-2022/discussion/321202
- 实验分享（156 票）：https://www.kaggle.com/competitions/birdclef-2022/discussion/318081
- 1st models（63 票）：https://www.kaggle.com/competitions/birdclef-2022/discussion/327047
- public#1/private#2（59 票）：https://www.kaggle.com/competitions/birdclef-2022/discussion/326950
- 3rd（56 票）：https://www.kaggle.com/competitions/birdclef-2022/discussion/327193
- 起点帖（51 票）：https://www.kaggle.com/competitions/birdclef-2022/discussion/308004
- 缺口登记：307824、324124、326973、314999、309213 未收录正文
