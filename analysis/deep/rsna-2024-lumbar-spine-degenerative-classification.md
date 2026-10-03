# RSNA 2024 腰椎 MRI 深读：两阶段定位 × 级联误差吸收 × 按条件拆模型

> 赛事：Featured ｜ 主题 cv（医学影像 MRI）｜ 1874 队 ｜ 代码赛 ｜ 指标：RSNA Lumbar 加权对数损失（5 层面 × 5 条件列 × 3 类，共 25 列）
> 材料基础：`digests/rsna-2024-lumbar-spine-degenerative-classification.md`（1st/2nd/3rd/4th 四篇完整方案 + starter 阅读清单 + 124 票实验占位帖；80 条讨论索引）+ 20 张图（539443×3 / 539452×3 / 539453×5 / 540091×9）
> 深读时间：2026-10（Tier A #33）

## 0. 一句话重述：这道题真正在考什么

题面是"腰椎 MRI 每个椎间盘层面、每类病变的严重度三分类"，实际被考的是**一条级联流水线的系统工程**：

1. **解剖定位先于分级**：25 个评分列（5 层面 L1/L2…L5/S1 × [scs, nfn_l, nfn_r, ss_l, ss_r]）都锚定在"哪一层面、哪一侧、椎管在哪"上；四强全部采用"定位 → 裁剪 → 分级"两阶段，没有一队把 25 列当纯多标签问题硬训。
2. **第一阶段误差是第一风险**：1st 实测层面预测 ±0 只有 67–71%（sagt2/scs），约 30% 样本带 ±1 误差；因此收益最大的工程不是换更强分类器，而是让分级模型**见过定位误差**（1st 的 instance_number 随机位移 ±2 被作者称为 crucial；3rd/4th 用伪标签与关键点归一化压缩误差影响）。
3. **按条件拆模型**：SCS 的最佳视角（sagT2 + axial）、NFN（sagT1）、SS（axial）不同；"每个条件一组独立子模型 + 条件特异融合"是四强的共同形态（1st 三类 severity 模型、3rd Center/Side 双分类器、2nd 逐目标独立、4th condition-separated pooling）。

一句话：**这是一场"先修坐标、再修分级"的比赛**——分类器只是流水线的最后一环；分差主要来自定位鲁棒性、标注噪声处理与集成结构，而非 backbone 选择。

## 1. 材料与角色

| 帖子 | 作者 | 票数 | 角色与独有信息 |
| --- | --- | --- | --- |
| [503433](https://www.kaggle.com/competitions/rsna-2024-lumbar-spine-degenerative-classification/discussion/503433) Starter references | — | 137 | 往届 RSNA 2022 讨论聚合 + 解剖/低背痛 MRI 视频 5 条 + 论文 8 篇；领域语料入口 |
| [519628](https://www.kaggle.com/competitions/rsna-2024-lumbar-spine-degenerative-classification/discussion/519628) [placeholder] | — | 124 | 两篇脊柱狭窄 CNN 论文（DEEP SPINE、Radiology 2021）+ SpineAI 开源代码；"顺引文扩展"的阅读路径 |
| [540091](https://www.kaggle.com/competitions/rsna-2024-lumbar-spine-degenerative-classification/discussion/540091) 1st | 评论区署名 NANACHI | 105 | 3 类模型 2 阶段：instance_number 双任务（cls+reg）误差表、坐标预训练、裁剪像素配方表、MIL→bi-LSTM→0.33、失败清单 |
| [539452](https://www.kaggle.com/competitions/rsna-2024-lumbar-spine-degenerative-classification/discussion/539452) 2nd | inference code 署名 yujiariyasu | 98 | 轴/矢分离 + 逐目标独立小模型；hengck23 slice 分类 + YOLOX 区域检测；5 切片 MIL；**label noise 剔除 +1%**；spinal severe ×1.25 后处理 |
| [539443](https://www.kaggle.com/competitions/rsna-2024-lumbar-spine-degenerative-classification/discussion/539443) 4th | tattaka + yu4u | 76 | 关键点检测（2.5D+LSTM→UNet；20×256×256 回归）→ 裁剪 → 4 个分级子模型（多视角 Transformer + 单条件 2.5D）→ Nelder-Mead MLP + LGBM/XGB stacking |
| [539453](https://www.kaggle.com/competitions/rsna-2024-lumbar-spine-degenerative-classification/discussion/539453) 3rd | 代码库 Moyasii | 65 | CenterNet 双关键点检测 + 世界坐标层面分配；Center/Side 分类器；**Split LR 翻转（2×/10× 数据）**；30 模型集成 CV 0.3643；温度 0.91 |

**材料缺口（受"不扩采"约束，登记备查）**：5th(539472,35 票)、7th(539439,35 票)、8th(539548,32 票)、14th(539459,31 票)、9th(539690,29 票)、Summary(541279,29 票)、7th(539486,27 票) 共 7 条方案帖未收录正文。其中 **7th 标题 "Single Stage Model Wins!" 与前三名"一阶段失败"直接冲突**，见 §8 悬案 1。

## 2. 逐方案对照矩阵

| 维度 | 1st NANACHI | 2nd yujiariyasu | 3rd Moyasii | 4th tattaka+yu4u |
| --- | --- | --- | --- | --- |
| 总体结构 | 2 阶段 3 模型：instance_number→coordinate→severity | 轴/矢独立 + 每目标独立小模型（无共享定位网络） | 2 阶段：关键点定位+层面分配+crop → Center/Side 分类 | 关键点检测→裁剪→4 分级子模型→stacking |
| 定位方案 | sag：3D ConvNeXt 双任务（cls+reg）预测 instance_number；2D 回归坐标；axial 借 hengck23 | slice 分类（hengck23）+ YOLOX 区域（brendanartley 数据训练） | CenterNet：层面 EffNetB6+FPN、椎管 EffNetB4+FPN；世界坐标推 L1/S1 伪坐标 | 轴：2.5D+LSTM 分层面→UNet 左右关键点；矢：2.5D 找孔区左右切片 + 关键点；STIR 取中片 |
| 坐标标签源 | brendanartley 坐标数据集（预训练，优于 ImageNet 初始化） | brendanartley 共享数据训 YOLOX | 社区 Coordinate Pretraining Dataset + 伪标签全量化 + 人工审标 | 共享 Lumbar Coordinate Dataset |
| 分级输入 | 按条件裁剪 5 切片：scs=sagt2/axial，nfn=sagt1/axial，ss=axial | 5 切片 MIL；sag 以预测层面为中心，孔区用 spinal/subarticular 中间切片；axial ±2 切片 | sagT1/sagT2 各 15 片 + axial 10 片等间隔；axial 以椎管中心裁剪 | 多视角组：30 片组 + 5 片组；crop 边长=相邻关键点距×2 |
| 分级架构 | 1ch encoder→bi-LSTM→attention MIL；aux depth + 共享权重 aux class → concat 主头 | ConvNeXt-S + MIL(5 图) | 2D encoder + slice attention；Center/Side 双分类器（两组头结构做多样性） | 2D backbone→Transformer→condition-separated attention pooling + aux loss；单条件 2.5D CNN |
| 鲁棒化手段 | instance shift ±2（按各模型误差概率）+ xy ±10px + 几何增强 | label noise 剔除（\|Δ\|≥0.8）+ 左右半图统一 | Split LR 右翻转、弃层面/侧别独立样本（5×/10×）、伪标签、TTA | 关键点距离归一化、不足 30 片 padding、超 30 片插值 |
| 集成 | 5 fold × 2 任务；instance 用 median、coordinate 用 mean | 队员模型加权平均 | 30 模型平均（15 Center + 15 Side） | Nelder-Mead MLP + 每层独立 LGBM/XGB；nfn 输入拼接 scs/ss/nfn |
| 后处理 | — | spinal 最高 severe 值 ×1.25 | SCS logits 温度 0.91 | — |
| 报告数字 | 0.37→0.35→0.33（public LB） | OOF CV 0.3687；噪声清洗公/私榜各 +1% | CV：单模型 0.3858 → 30 模型 0.3643 | CV 与 LB 相关性好（未给数） |
| 失败清单 | Mamba/自注意力、aux 权重共享、错视角组合、长 epoch、大模型、ViT | 正文未列 | 一阶段、多层面多病种、按层面、按侧、3D-CNN、2.5D+Attn、2D+LSTM、Focal、长 epoch | 正文未列 |

**视角-条件匹配表（跨队归纳）**：scs→sagT2/STIR + axial；nfn→sagT1（+axial 侧向裁剪）；ss→axial。1st 明确验证"sagt1 给 scs、sagt2 给 nfn、sagt1+sagt2 给 ss"等组合无效。

## 3. 共识、分歧与裁决

### 共识一：两阶段"定位→裁剪→分级"（4/4）

1st 把阶段一拆成 instance_number + coordinate 两类模型落盘 `test_label_coordinates.csv`；2nd 用 slice 分类 + YOLOX 区域；3rd 用两个 CenterNet 分别找层面与椎管；4th 用关键点检测 + 距离归一化裁剪。**没有队伍端到端直接出 25 列。**

**裁决**：多部位医学影像的第一性结构是"先解决在哪，再解决多严重"；端到端会让"层面身份"与"病灶程度"在特征空间中纠缠。置信度：高（4 队一致 + 1st/3rd 明确把一阶段列入失败清单）。**保留张力**：7th 标题宣称单阶段可行（未收录正文，T13 候选）。

### 共识二：第一阶段误差必须被"吸收"，而不只是被压低

1st：±0=67–71%、±1≈27–31% → 训练时按误差分布随机位移 instance_number（±2），作者称 crucial for robustness；
3rd：伪标签用尽全部数据 + 手工校标 + 世界坐标几何分配（伪算 L1/S1）；
4th：关键点回归 + 距离归一化裁剪，把个体尺度差从输入中消除；
2nd：slice 分类 + YOLOX 区域，用检测框兜住解剖结构。

**裁决**：级联系统的期望损失由 `P(定位误差) × 分级敏感度` 决定；只优化定位器会撞上标注与解剖的噪声上限。三族有效解：① 把误差分布注入训练（1st 位移增强）；② 用伪标签/多假设覆盖（3rd）；③ 用坐标归一化让分类器对误差不敏感（4th）。置信度：中高（1st 有数字，其余为结构性证据）。

### 共识三：按条件拆子模型（4/4，粒度不同）

1st：scs/nfn/ss 三套 severity 模型，输入通道不同（各条件专属裁剪表）；
3rd：Center Classifier（SCS）+ Side Classifier（NFN/SS），Split LR 统一左右；
2nd：逐目标独立模型，non-spinal 只用左/右半图；
4th：同一 backbone 上每条件独立 attention pooling 头 + 条件特异 stacking 输入。

**裁决**：多部位多任务的最优分解粒度≈标注/视角结构；统一多头会把不同视角的信息互相干扰（3rd 的"多层面多病种"失败清单）。置信度：高（4 队形态一致）。

### 分歧一：MIL vs 2.5D vs Transformer——到底谁赢？

1st：attention MIL 使 LB 0.37→0.35，2.5D 较差；但作者在评论中承认 **MIL 的本地 CV 增益小于 LB 增益**；
3rd：失败清单同时列 2.5D+Attention 与 2D+LSTM，但它自己的分类器是"2D encoder + slice attention"（单样本内 15+15+10 片聚合，不是跨示例 MIL bag）；
4th：两种并存——多视角 Transformer（条件分离 pooling）与单条件 2.5D CNN（作者称其他视角组合"no significant results"）。

**裁决**：争的不是"MIL 三个字母"，而是聚合三件套：**切片集合 → attention 聚合 → 辅助监督**。同一结构名在 3rd 失败、在 1st/4th 成功 → 成败绑定到实现配置（切片数、聚合位置、aux 头）。1st 的 CV/LB 背离提示 MIL 收益可能含公榜红利（对照 L6/T3），复现须先做 CV 无泄漏审计。置信度：中。

### 分歧二：模型规模与训练时长——小模型共识

1st：convnext-large < base < small；ViT 全面弱于卷积；7 epoch（effv2s 14）；
3rd：10–20 epoch；ResNet18/MNasNet/EffNet-B4/ConvNeXt-N/T/MaxViT-N 集成；长 epoch 进失败清单；
2nd：ConvNeXt-S；4th：tiny 级 backbone（caformer_s18 / convnext_tiny / resnetrs50 / swinv2_tiny / maxxvitv2_nano）。

**裁决**：数据规模 + 标注噪声限制了容量收益；小模型 + 强增强 + 异构大集成的期望分数更高。置信度：高（4 队一致）。

### 分歧三：标注噪声的处理路径

2nd：teammate 发现噪声 → 用 ensemble OOF（CV 0.3687）剔除 \|label−pred\|≥0.8 的样本（对 moderate/severe 加系数）→ 公/私榜各 +1%；
3rd：社区讨论暴露 label noise → 人工复查并修正全部标注。

**裁决**：噪声真实存在（两队独立确认），两条路径都有效；自动阈值更快，但会把"难而正确"的样本混入删除集；人工审查更干净但不可扩展。任何自动清洗都必须在 CV 与 LB 双侧验证（2nd 恰为双侧 +1%）。置信度：中高。

## 4. 增量数字账

| 动作 | 数字 | 来源 |
| --- | --- | --- |
| instance_number 精度（sagt2/scs） | cls：±0 **71.08%** / ±1 27.04% / ±2 1.43% / >±2 0.44%；reg：67.48% / 30.59% / 1.61% / 0.31% | 1st |
| 1st 提升阶梯 | 2.5D 0.37 → attention MIL 0.35 → +bi-LSTM+aux+ensemble **0.33**（public LB） | 1st |
| 1st 误差吸收 | instance_number 位移 ±2（概率按误差分布）、xy ±10px、crop 后几何增强 p=0.5 | 1st |
| 1st 训练预算 | convnext-s **7 epoch** / effv2-s **14 epoch**；每任务 5 fold | 1st |
| 1st 裁剪配方（像素） | scs sagt2 96/32/40/40；nfn sagt1 96/64/32/32；axial 右 144/48/96/96、左 48/144/96/96；axial 加 ±20 抖动 | 1st |
| 2nd 噪声清洗 | ensemble OOF CV **0.3687**；阈值 \|Δ\|≥0.8；公/私榜各 **+1%** | 2nd |
| 2nd 后处理 | 每例 5 层面 spinal-severe 最大值 **×1.25** | 2nd |
| 3rd 集成 | 单模型 CV **0.3858** → 30 模型平均 **0.3643** | 3rd |
| 3rd 训练配置 | CE 权重 [1.0, 2.0, 4.0]；lr 2.5e-5 + OneCycleLR（warmup 3/10）；batch 2–8；drop_path 0.2/0.3 | 3rd |
| 3rd 输入 | sagT1/sagT2 各 15 片 + axial 10 片；数据倍率 5×（弃层面）/ 10×（再弃侧别） | 3rd |
| 3rd 后处理 | SCS 温度 **0.91**（图 6 另见第二参数 lr_t≈0.95–0.97） | 3rd |
| 4th 输入/融合 | 30×128×128 ×2 序列 + 5×128×128 ×2；每片 512 维；Nelder-Mead MLP + 每层 LGBM/XGB（输入维=模型数×3） | 4th |
| 1st CV/LB 背离 | MIL 的本地 CV 增益小于 LB 增益（无数字） | 1st 评论区 |
| 赛事规模 | 1874 队；25 个评分列 | 赛事元数据/结构 |

**结构校验（2 处吻合）**

1. 25 列 = 5 层面 × 5（scs + nfn_l/r + ss_l/r）✓；
2. 3rd 数据倍率：弃层面依赖 = 5×（5 层面样本共享），再弃侧别 = 10×（左右共享）✓ 与其 "five times / ten times" 自述自洽。

## 5. 机制推演

**M1｜为什么两阶段不可省**：分级标签只定义在"层面-条件"对上，层面坐标是解剖量而非图像特征。端到端训练会让网络把"这是第几层"与"这层多严重"混进同一组特征；1st 的误差表证明即使专门定位也只有 2/3 全对——该信息必须单独建模，且需要专门的中间监督（坐标/关键点），否则没有足够的梯度信号把它学出来。

**M2｜为什么关键点/坐标归一化优于 slot 分类**：层面数量与间距因人而异（脊柱曲度/身高），"把切片分到 5 个槽位"隐含固定间距假设。关键点把个体解剖差异显式参数化，随后按"相邻关键点距离×2"裁剪（4th）或按关键点均值距离定尺度（1st/2nd），把尺度差异从分类器输入中消除——误差从"系统性几何偏差"退化为"小扰动"。

**M3｜为什么 instance_number 位移增强是关键**：设第一阶段 ±0/±1/±2 概率≈0.70/0.30/0.01。若不增强，第二阶段训练分布=理想定位，而测试分布≈70% 理想 + 30% 错层；位移 ±2 让训练分布覆盖测试分布，并迫使 bi-LSTM/attention 利用邻层上下文判别。这是"把级联系统误差当数据增强"的通用范式（候选规律 L43）。作者原话：crucial for robustness of error of 1st stage。

**M4｜为什么 attention+bi-LSTM+aux 是 MIL 的有效形态**：5 张切片里通常只有 1–2 张切到病灶最重处，而标签属于整个 bag——attention 权重自动选关键切片；bi-LSTM 建模切片顺序（解剖连续性先验；1st 实验中 Transformer/自注意力反而更差）；aux depth 头在 bi-LSTM 后注入层间上下文，共享权重 aux class 头让每条流单独可预测（深监督），主头再做跨流融合。评论区互动显示作者认为 aux loss 增益比提问者预期更显著。

**M5｜为什么按条件拆（Center 型 vs Side 型）**：SCS 是椎管中央结构 → sagT2 最清 + axial 交叉验证；NFN/SS 是侧方/孔区结构 → sagT1 孔区切面 + axial 左右半。3rd 的 Center/Side 双分类器把视角语义编码进模型拓扑；Split LR 再把右半翻成左半，让"左右"不再作为独立稀疏模式学习 → 数据翻倍。2nd 的"non-spinal 只用左/右半图"是同一思想的轻量版。

**M6｜为什么噪声剔除能 +1%**：加权 log loss 下，一个把 moderate 标成 normal（或反向）的样本会持续贡献大梯度；MRI 分级天然有 inter-rater 差异 → 训练集必然混入错标。用强集成 OOF 预测与标签之差（≥0.8）近似"哪个样本可疑"，剔除后重训 = 用高置信模型给训练集做去噪。风险在于阈值同时切掉"难而正确"的样本，因此 CV 与 LB 双侧验证是必要条件（2nd 两侧同 +1%）。

## 6. 证据分级

| 断言 | 等级 | 说明 |
| --- | --- | --- |
| 1st 0.37→0.35→0.33（LB 阶梯） | 自述（notebook 公开，可复现） | 数字具体，但为 public LB；作者自认 CV 增益更小 |
| instance_number 误差表（71.08/67.48…） | 自述（细到 ±2 分桶，内部自洽） | cls/reg 双任务对比清晰 |
| 3rd 30 模型 CV 0.3643 / 单模型 0.3858 | 自述 + 代码开源 | 结构可复现 |
| 2nd 噪声剔除 +1% | 自述（无系数/占比细节） | 阈值 0.8 与类别系数的标定未公开 |
| 标注噪声存在 | 两队独立证词（2nd/3rd） | 中高，但"噪声占比"无数字 |
| Split LR（2×/10× 数据） | 3rd 自述 + pipeline 图 + 结构校验 | ✓ |
| 7th "单阶段可行" | 仅标题（正文未收录） | 低，登记悬案 |

## 7. 边界条件与反事实

- **反事实 1**：若不拆定位（端到端 25 列）→ 1st/3rd 失败清单直接覆盖该分支；但 7th 标题留下例外空间（见悬案 1）。
- **反事实 2**：若不做位移增强 → 30% 的 ±1 错层样本落在训练分布外；1st 称该增强 crucial（无消融数字，自述级）。
- **反事实 3**：若不处理噪声 → 2nd 少 +1%；3rd 手工审标说明噪声量级值得用人力处理。
- **反事实 4**：若换大模型/长 epoch → 1st 的 convnext-large/ViT、3rd 的长 epoch 均为负结果；本场容量收益 < 数据工程收益。
- **边界**：以上结论依赖"有坐标型中间标签可用"（官方坐标列/社区坐标数据集）。纯分类医学赛（无关键点标签）只能移植"两阶段 + 伪标签"骨架，不能直接套 CenterNet 关键点方案。

## 8. 悬案与失败学

**悬案**

1. **7th "Single Stage Model Wins!"（539439，35 票）与前三名"one-stage 失败"冲突**——正文未收录（不扩采约束），无法裁决：是单阶段配合了更强的内部定位头？还是两阶段蒸馏成单阶段？登记为后续选择性补读候选（同时登记 T13 候选张力）。
2. 1st 的 CV/LB 背离（MIL 的 CV 增益 < LB 增益）：是公榜过拟合还是 CV 划分差异？作者未解释 → 复现时须先做 CV 无泄漏审计（对照 L6/T3）。
3. 2nd 噪声清洗细节（系数/阈值标定/被删样本占比）未公开，+1% 不可复算。
4. 4th 的 stacking（Nelder-Mead MLP + 每层 LGBM/XGB）相对简单平均的增益无消融数字；评论区里的 CV 具体值在存档文本中丢失。

**失败学（跨队合集）**

- 结构类：一阶段、多层面多病种、多层面单病种、按层面专用、按侧专用（3rd）；Mamba/自注意力替代 bi-LSTM、aux 层权重共享、错视角输入组合（1st）。
- 训练类：长 epoch、Focal Loss（3rd）；大模型、ViT（1st）。
- 提示：同一结构名（2.5D+Attention、2D+LSTM）在 3rd 失败、却在 1st/4th 变体成功 → 失败学要记录到**配置级**（切片数、聚合位置、aux 拓扑），否则不可迁移。

## 9. 图表证据

> 路径相对本文件（`analysis/deep/`）：`../../intel/rsna-2024-lumbar-spine-degenerative-classification/bodies/<topic>_img/NN.png`

**图 1：1st 的 3 模型 2 阶段总管线**（topic 540091）——`../../intel/rsna-2024-lumbar-spine-degenerative-classification/bodies/540091_img/01.png`

*读图结论*：3D 模型（instance_number）→ 2D 模型（coordinate）→ `test_label_coordinates.csv` → 三类 severity（MIL 框）；SS 的 instance_number 由 sagt2 坐标经 hengck23 方法转到 axial——**SS 没有独立 3D 定位模型，轴向层面归属继承自矢状面**。这是"跨视角信息传递"的施工细节，正文文字未直说。

**图 2：1st 的 SCS 分级模型（bi-LSTM + Attention MIL + 双流 aux）**（topic 540091）——`../../intel/rsna-2024-lumbar-spine-degenerative-classification/bodies/540091_img/08.png`

*读图结论*：axial 与 sagt2 两条流各自 encoder→bi-LSTM→attention 加权；每流在 LSTM 后挂 aux depth 头（bs,5），在加权后有**共享权重**的 aux 分类头（橙框，bs,3）；最后 concat 双流特征进主头。这解释了"aux loss 为什么有效"：每个视角必须先单独学会预测（深监督），再做融合。

**图 3：3rd 的完整两阶段管线**（topic 539453）——`../../intel/rsna-2024-lumbar-spine-degenerative-classification/bodies/539453_img/01.png`

*读图结论*：矢状 T1、T2/STIR 各自 CenterNet 层面关键点→crop 5 层；axial 经"世界坐标层面分配"后由第二个 CenterNet 找椎管→crop；Stage 2 由 Center Classifier 出 SCS，Split LR 后 Side Classifier 出 NFN/SS（左右两路共享分类器）；标注"同分类器用于所有层面"——**层面无关的共享分类器 + 层面特异的输入裁剪**。

**图 4：4th 的多视角多条件模型（Transformer + condition-separated attention pooling）**（topic 539443）——`../../intel/rsna-2024-lumbar-spine-degenerative-classification/bodies/539443_img/02.png`

*读图结论*：4 组输入（30 片×2 序列 + 5 片×2）共享 2D backbone → 每片 512 维特征 → 位置编码 → Transformer → 每条件独立 attention pooling+linear 出主损失；另有从预 Transformer 特征直接接出的 aux loss 分支。**同一 backbone 上"每条件一套 attention head"，比多模型更省地实现条件分离**（正文称 attention pooling 前置与 aux loss 是关键技巧）。

**图 5：2nd 的轴向 YOLOX 区域检测**（topic 539452）——`../../intel/rsna-2024-lumbar-spine-degenerative-classification/bodies/539452_img/01.png`

*读图结论*：两行共 10 张轴向切片（每组 5 片）上的小白框 = YOLOX 检测的椎管区域；该区域仅用于 spinal 类预测，non-spinal 用左右半图。**用检测框兜住关键解剖结构替代坐标回归**，是轻量定位方案。

**图 6：3rd 的后处理参数搜索（Optuna slice plot）**（topic 539453）——`../../intel/rsna-2024-lumbar-spine-degenerative-classification/bodies/539453_img/05.png`

*读图结论*：纵轴 objective≈0.3685–0.3725，最优约 0.3685；右图 spinal_t≈0.91 与正文温度 0.91 吻合；左图 lr_t≈0.95–0.97 的第二个缩放参数正文未提——**图里信息多于文字**：后处理是两参数联合搜索，且最优区平缓（收益为小数点后第 3–4 位量级）。

## 10. 对既有笔记/playbook 的修订点

1. `notes/cv/rsna-2024-lumbar-spine-degenerative-classification.md` 升级：方案谱系扩为 4 方案 × 11 维对照；补数字账（71.08/67.48、0.37→0.33、CV 0.3643/0.3858、+1%）与图证 5 张。
2. `playbook/cv.md`（医学影像节）增补：
   - **两阶段骨架**：定位（关键点/层面/椎管）→ 坐标归一化裁剪 → 分级；中间产物落盘（`test_label_coordinates.csv` 模式）便于断点与集成；
   - **级联误差吸收三件套**：按第一阶段误差分布做位移增强（±k）；伪标签/多假设覆盖；关键点距离归一化；
   - **按标注语义拆头**：中央型（Center）/侧方型（Side）/视角专属输入；Split LR（右翻转）统一左右并翻倍数据；
   - **标注噪声**：强集成 OOF 高损失样本剔除或人工审标；阈值与类别系数必须记录。
3. `playbook/00-通用方法论.md` 增补：**"把上一阶段的系统误差当数据增强"**（级联/两阶段通用）；**"结构名不等于机制"**（失败学记到配置级）。
4. `analysis/THEORY.md`（Batch 4 收尾扩 v0.4）候选：
   - **L43｜级联系统误差 → 训练分布增强**：证据 = 1st ±2 位移（crucial）+ 3rd/4th 伪标签/坐标归一化；反例 = 7th 单阶段（待裁决）。
   - **L44｜按标注语义拆子模型 + 条件特异融合**：证据 = 本场 4 队形态 + 4th 的 nfn 拼接 scs/ss 输入。
   - **T13｜单阶段 vs 两阶段（医学多部位）**：7th 标题 vs 1st/3rd/4th 共识，待补正文。

## 11. 出处

- 1st（NANACHI，105 票）：https://www.kaggle.com/competitions/rsna-2024-lumbar-spine-degenerative-classification/discussion/540091
- 2nd（yujiariyasu，98 票）：https://www.kaggle.com/competitions/rsna-2024-lumbar-spine-degenerative-classification/discussion/539452
- 4th（tattaka + yu4u，76 票）：https://www.kaggle.com/competitions/rsna-2024-lumbar-spine-degenerative-classification/discussion/539443
- 3rd（Moyasii，65 票）：https://www.kaggle.com/competitions/rsna-2024-lumbar-spine-degenerative-classification/discussion/539453
- Starter 阅读清单（137 票）：https://www.kaggle.com/competitions/rsna-2024-lumbar-spine-degenerative-classification/discussion/503433
- [placeholder] 参考论文（124 票）：https://www.kaggle.com/competitions/rsna-2024-lumbar-spine-degenerative-classification/discussion/519628
- 未收录方案帖（缺口登记）：539472 / 539439 / 539486 / 539548 / 539690 / 539459 / 541279（7 条 write-up 候选，见 §8 悬案 1）
