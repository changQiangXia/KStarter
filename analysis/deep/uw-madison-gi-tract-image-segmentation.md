# UWMGI 2022 深读：部分标注分层 × CLS 门控 × 2.5D/3D 融合

> 赛事：Research ｜ 主题 cv（医学 MRI 多类分割）｜ 1548 队 ｜ 代码赛 ｜ 指标：Dice + 3D Hausdorff（赛事中途引入 Hausdorff）
> 材料基础：`digests/uw-madison-gi-tract-image-segmentation.md`（6 篇：MONAI-3D/资源汇总/1st/2.5D/5th/3rd；80 条讨论索引）+ 3 张图（337197×1 / 320060×2）
> 深读时间：2026-10（Tier A #35）

## 0. 一句话重述：这道题真正在考什么

题面是"MRI 逐切片分割胃/小肠/大肠（3 类语义分割）"，实际被考的是**部分标注与空切片下的工程分层**：

1. **部分标注 + 错误标注**：大量切片没有器官、部分切片无标注、社区另有"错误 mask"大讨论（319963，70 票）；直接全量硬训会被负样本与噪声主导——1st 把数据分成"anno-only / 全量 / 排除肠末端 ambiguous 5 层"三种训练策略，分别喂给不同模型。
2. **空切片必须门控**：1st/3rd 用分类器先判"这一层有没有目标"（1st：阈值 0.6 且正像素 >12 才算正），负层直接输出零 mask；5th 用后过滤（<50px 丢弃）替代。
3. **2.5D vs 3D 是互补而非对立**：3D（MONAI/ SegResNet）给 z 方向一致性与更好的 Hausdorff；2.5D 给训练效率与多样性；冠军把两者 logits 按 0.4/0.6 融合（阈值 0.4），5th 用 9 个 2.5D（x/y/z 三轴切法）×3 个 3D 做多样性集成。
4. **指标中途改为 Dice + 3D Hausdorff**：MONAI 作者用新指标重新微调与选模（LB 0.860→0.872）；3rd 直接试 Hausdorff 损失失败——**指标换 ≠ 损失换，先换选模与后处理**。

一句话：**这是一场"数据分层 + 空切片门控 + 2.5D/3D 融合"的工程赛**——冠军结构里没有一个部件是单纯的模型选择。

## 1. 材料与角色

| 帖子 | 作者 | 票数 | 角色与独有信息 |
| --- | --- | --- | --- |
| [325646](https://www.kaggle.com/competitions/uw-madison-gi-tract-image-segmentation/discussion/325646) 3D MONAI | yiheng | 162 | 最完整可复现的 3D 单系：patch 160×160×80 → 微调 224×224×80；v1 (dice+ce) LB 0.817 → v3 (dice+bce) 0.857 → v6（lr 调度/损失）0.872 → 5 折 0.877；公开数据/训练/推理管线 |
| [320060](https://www.kaggle.com/competitions/uw-madison-gi-tract-image-segmentation/discussion/320060) 资源汇总 | — | 140 | 数据事实：每扫描 144/80 切片、case=1–5 天（144–720 图）、4 种尺寸、首 1/末 ~8 切片无 mask；基线演进 DeepLabV3+ 0.810 → +ASPP+SE 0.817 → EffNetB0 UNet 0.828；"smart baseline"（用训练集匹配元数据的 RLE 提交）；指出应做 multilabel（sigmoid）而非 multiclass |
| [337197](https://www.kaggle.com/competitions/uw-madison-gi-tract-image-segmentation/discussion/337197) 1st | — | 127 | **CLS 门控**（4 UNet b4–b7，阈值 0.6 + >12 正像素）+ **SEG 三分层**（5 UNet + 2 UPerNet：anno-only / 去 ambiguous / 全量）+ **3D**（3 SegResNet，filters 12/20/32）；3D/2.5D logits 0.4/0.6 融合、阈值 0.4 |
| [337217](https://www.kaggle.com/competitions/uw-madison-gi-tract-image-segmentation/discussion/337217) 1st 2.5D | — | 56 | 2.5D stride=2 × 3 切片；640/512 训练 + RandomCrop 448；弹性/网格/光学畸变；flip TTA +0.001–0.002；effb4–b7 单模型 ~0.883、融合 0.889；CLS 全量/SEG 仅标注；BCE:Dice=1:3；fp16 省 ~50% 显存 |
| [337268](https://www.kaggle.com/competitions/uw-madison-gi-tract-image-segmentation/discussion/337268) 5th | — | 46 | **几何多样性集成**：9 个 2.5D（x/y/z 三轴切法）× 3 个 3D；单模型最高仅 0.875 → 简单平均 + 阈值 0.3 = 0.889 → <50px 丢弃 = 0.890 |
| [337468](https://www.kaggle.com/competitions/uw-madison-gi-tract-image-segmentation/discussion/337468) 3rd | — | 45 | 检测器裁剪（EffDet-D0，256）→ CLS+SEG 双分支 UNet（35 epoch = 7 cycles，EMA+SWA）；post：去 25px + "连续 3 正/负切片定起止"；5 折 0.877/0.886；失败清单（Hausdorff loss、亮度调整、外部 CT、正负平衡） |

**材料缺口（受"不扩采"约束，登记备查）**：2nd(337400,44 票)、"2.5D Image Training"(322549,124)、"MMsegmentation 模板"(323921,104)、"Best single model CV-LB"(320692,62)、"Loss functions"(329396,52)、"TransUNet+2.5D"(326035,52)、**"Incorrect masks"(319963,70) + 续帖(321979,43)**、**"LB could be wrong"(324934,47)**、"Hausdorff usage"(319215,40)、"Ensemble Tricks"(330336,40) 等未收录正文——标注错误与指标实现的社区争议是本次深读的最大信息缺口。

## 2. 逐方案对照矩阵

| 维度 | 1st | 5th | 3D MONAI (yiheng) | 3rd |
| --- | --- | --- | --- | --- |
| 总体 | CLS + 2.5D SEG + 3D，三组融合 | 9×2.5D(x/y/z) + 3×3D 全平均 | 纯 3D 单系（UNet→大 UNet） | 检测裁剪 → CLS+SEG（无 3D） |
| 空切片处理 | CLS 门控（0.6 + >12px） | 后过滤 <50px | 3D 体积整体预测 | CLS 分支 + 连续切片规则 |
| 数据分层 | 三分层：anno-only / 去 ambiguous 5 层 / 全量 | 未分层（全量+正样本） | public split（awsaf49） | SEG 只用正样本；检测器重标坏框 |
| 2.5D 构造 | stride=2，3 切片 | x/y/z 三轴各切一份（2.5Dx/y/z） | — | slice=3 与 slice=5 两族 |
| 3D 模型 | 3×SegResNet（12/20/32） | resnet-unet / effv2s-unet / effv2m-unet | 3D UNet；160×160×80 → 224×224×80 | — |
| 模型规模 | UNet b4–b7 + UPerNet convnext | effv2s/nfnet-l0/convnext-s/pvtv2b2/mitb2 等 | 由小到大逐步升级（v1→v5） | effb3–b7、effv2-l/m，320–416 |
| 损失 | dice-ce / ce / dice（分模型） | seg 常规（未展开） | dice+ce → dice+bce → 新指标微调 | ComboLoss（bce .5/dice .5/lovasz 1） |
| 指标感知 | 融合阈值 0.4 | 阈值 0.3 | v4 起用新指标（Dice+Hausdorff）微调/选模 | 选模用 TP/(TP+FP+FN)+Dice；Hausdorff loss 失败 |
| 融合/后处理 | 3D/2.5D = 0.4/0.6；阈值 0.4 | 全模型平均；<50px 丢弃 | 5 折权重集成 | 去 25px；连续 3 正/负切片定起止 |
| 成绩 | 榜首（未给总分） | pub 0.890 | 5 折 0.877 | 5 折 0.877/0.886 |
| 训练/推理 | — | 单模型最高 0.875 | 每版全流程公开 | 35 epoch/7 cycle；Kaggle GPU 两个月 + 租卡一个月 |

## 3. 共识、分歧与裁决

### 共识一：部分标注必须分层使用（1st 最精细，3rd/5th 方向一致）

1st：UPerNet 用"去 ambiguous"数据（肠末端 5 层不参与），UNet 只用 anno-only，3D 用全量；
3rd：SEG 只用正样本，检测器阶段人工重标坏框；
5th：未显式分层，但用后过滤兜底。

**裁决**：部分标注场景有三类污染——**缺失标注（≠空）、错误标注、语义模糊区**；处理方式是把"数据子集×模型角色"配对（干净子集训精细模型、全量训鲁棒模型），并在图上/规则上排除模糊区（1st 的 5-layer ambiguous）。置信度：中高（1st 有图 + 社区错误 mask 帖佐证）。

### 共识二：空切片要显式门控（1st/3rd 分类器，5th 后过滤）

1st：CLS 先判正负（0.6 阈值 + >12 正像素），负数直接零 mask；
3rd：CLS+SEG 双分支，保留分类器判正的分割结果；
5th：不设 CLS，直接对小面积预测（<50px）丢弃。

**裁决**：空切片/负切片占比高时，CLS 门控同时节约算力与抑制假阳性；后过滤是廉价近似（但无法省算力）。两种路径都有效，选择取决于推理预算。置信度：高。

### 共识三：2.5D 与 3D 互补，融合是上限最高解（4/4 中 3 队融合或双线）

1st：3D SegResNet + 2.5D UNet/UPerNet，logits 0.4/0.6；
5th：9×2.5D(x/y/z) + 3×3D 全平均（单模型 0.875 → 集成 0.889）；
MONAI：纯 3D 单系到 0.877（5 折）；
3rd：无 3D（资源限制），但 0.877 说明 3D 非必需。

**裁决**：3D 提供 z 一致性与更优 Hausdorff；2.5D 提供多样性、可扩展性与训练效率。**预算允许时融合；预算受限时 2.5D+CLS 仍可进前列**（3rd）。置信度：高。

### 分歧一：指标变更（加 3D Hausdorff）怎么应对

MONAI：v1–v3 以旧 Dice 选模（local 0.8789→0.9108），新指标下只有 0.8933；v4 起改用新指标微调/选模，LB 0.860→0.872；
3rd：直接把 Hausdorff 当损失 → 失败（不可导 + 对离群点敏感）；
5th：用 3D 模型 + 小区域过滤稳边界。

**裁决**：指标换时，优先改**选模协议与后处理**，其次改微调目标；不要直接把新指标当损失（Hausdorff 类指标不可导/离群敏感）。MONAI 的 v4→v6 曲线是"选模指标对齐竞赛指标"的直接证据。置信度：中高。

### 分歧二：集成规模与阈值

1st：分组加权（CLS 门控 + 3D/2.5D 权重）；
5th：12 模型简单平均，阈值 0.3（+后处理 0.890）；
3rd：cls+seg 组合 0.877/0.886。

**裁决**：大集成下简单平均 + 重扫阈值已足够（5th）；但阈值与模型集耦合——每次换集成必须重扫（1st 0.4 vs 5th 0.3）。置信度：中高。

### 补充共识：后处理的尺度与确定性

所有队伍都有小幅确定性后处理：1st 的 >12px 门控、3rd 的去 25px + 连续切片规则、5th 的 <50px 丢弃；量级 0.001–0.003，但几乎无成本、无过拟合风险。置信度：高。

## 4. 增量数字账

| 动作 | 数字 | 来源 |
| --- | --- | --- |
| 数据事实 | 每扫描 144（常见）/80（少）切片；case=1–5 天 → 144–720 图；4 种图像尺寸；首 1/末 ~8 切片无 mask | 资源帖 |
| 基线演进 | DeepLabV3+ 0.810（3 epoch）→ +ASPP+SE 0.817（7 epoch）→ EffNetB0 UNet（Dice+Focal）0.828 | 资源帖 |
| 1st CLS | 4 UNet（b4–b7）；阈值 0.6 + 正像素 >12 判正 | 1st |
| 1st SEG | 5 UNet（b4/2×b5/b6/b7）+ 2 UPerNet（convnext base/small）；三分层数据 | 1st |
| 1st 3D | 3 SegResNet（init_filters 12/20/32，PRELU+BN）；3D/2.5D logits 0.4/0.6；阈值 0.4 | 1st |
| 1st 2.5D | stride=2 ×3 切片；640/512 → RandomCrop 448；TTA +0.001–0.002；单模型 ~0.883、融合 0.889；fp16 省 ~50% 显存；BCE:Dice=1:3 | 1st 2.5D 帖 |
| 5th 集成 | 9×2.5D（x/y/z）+ 3×3D；单模型最高 0.875 → 平均+阈值 0.3 = 0.889 → <50px 丢弃 = **0.890** | 5th |
| 3rd 单折/5 折 | fold0：0.869–0.875（模型族）；5 折：0.873–0.879；cls+seg 0.877/0.886；seg+seg 0.879（未提交） | 3rd |
| 3rd 训练 | 检测器 256/5 epoch；分割 320–416、35 epoch（7 cycle）、lr 3e-4/5e-4；ComboLoss(bce .5/dice .5/lovasz 1) | 3rd |
| MONAI 版本链 | v1 160×160×80 dice+ce LB 0.817 → v2 224×224×80 0.840 → v3 dice+bce 0.857 → v4 新指标 0.860 → v5 multilabel 大 UNet 0.868 → v6 lr/损失 0.872 → 5 折 0.877 | MONAI |
| MONAI 局部分数 | v2 old-dice 0.8970 / new 0.8822；v3 old 0.9108 / new 0.8933（**旧指标选模高估 ~0.018**） | MONAI |

**结构校验（2 处吻合）**

1. case 图数范围：1–5 天 × 144 片 = 144–720 ✓（资源帖自洽）；
2. 1st 2.5D 的融合增益：单模型 ~0.883 → 融合 0.889（+0.006），与 5th 的 0.875→0.889（+0.014，模型数更多）方向一致。

## 5. 机制推演

**M1｜部分标注的三类污染**：① 缺失≠空——若把未标注切片当负样本，会教模型"有器官也输出空"；② 错误标注——社区"incorrect masks"高楼（70+43 票）说明噪声量级不可忽略；③ 语义模糊——肠管末端 5 层本身就无从判断。1st 的"数据子集×模型角色"配对同时缓解三者：精细模型吃干净子集，鲁棒模型吃全量，模糊区直接排除。

**M2｜CLS 门控为什么同时省算力与提分**：切片级空样本在顶/底与部分中部切片大量存在。若无门控：训练时负样本主导梯度（类别极端不平衡）；推理时低置信噪声在空切片上产生假阳性小区域（还吃后处理罚分）。CLS 先做二分类（全量数据都可训练，无标注缺失问题），再让分割只在正样本上学习——训练分布聚焦、推理零成本跳过负层。

**M3｜3D 为什么对 Hausdorff 特别重要**：Hausdorff 取的是最坏边界点距离，对单切片"闪烁"极敏感；2.5D 逐片预测在 z 方向缺乏一致性约束，容易产生孤立伪影。3D 卷积在 z 上平滑边界 → 最坏点距离下降。1st 的 0.4/0.6 加权融合与 MONAI 单系 0.877 是两个独立证据。

**M4｜指标切换的正确应对顺序**：MONAI 的版本链显示——old-dice 高的模型（0.9108）在新指标下只有 0.8933（高估 0.018）；改用新指标微调后 LB 从 0.840 涨到 0.872。机制：Dice 只关心区域重叠，Hausdorff 关心边界最坏点；旧指标选模会系统性偏向"内部填满但边界粗糙"的模型。3rd 直接优化 Hausdorff 失败（不可导/离群敏感），说明"对齐指标"应发生在**选模与后处理层**，而非损失层。

**M5｜几何视角多样性（5th 的 x/y/z 切法）**：把 3D 体积沿三个正交轴切 2.5D，同一解剖结构在不同切面上呈现不同纹理（轴向=器官轮廓、矢状/冠状=纵向走向）。模型误差在不同切面上去相关 → 简单平均即获 +0.014（单 0.875 → 集成 0.889）。这是"零成本多样性"：不换架构、不换数据，只换切片方向。

**M6｜阈值与后处理是"集成的一部分"**：1st 阈值 0.4 vs 5th 阈值 0.3 的差异不是谁对谁错，而是与模型集/融合权重耦合的输出校准点；5th 的 <50px 过滤、3rd 的 25px 过滤与连续切片规则都在修剪"小假阳性 + z 抖动"。这类小确定性收益（0.001–0.003）在多模型集成后仍稳定存在。

## 6. 证据分级

| 断言 | 等级 | 说明 |
| --- | --- | --- |
| MONAI 版本链数字 | **自述 + 全流程公开（数据/训练/推理 + 权重）** | 高（本场最可复现） |
| 1st 三分层 + CLS 门控 | 自述 + pipeline 图 | 中高 |
| 5th 0.875→0.889→0.890 | 自述（公开库链接） | 中高 |
| 3rd 0.877/0.886 与失败清单 | 自述 + inference 代码 | 中 |
| 资源帖数据事实与基线 | notebook 公开 | 中高 |
| 旧指标选模高估 ~0.018 | MONAI 对照表 | 中高（单队数字） |
| Hausdorff loss 失败 | 3rd 单队经验 | 低-中 |
| 错误标注规模 | 社区帖标题（正文未收录） | 低（登记） |

## 7. 边界条件与反事实

- **反事实 1**：若不处理空切片 → 负样本主导训练 + 空层假阳性；CLS（1st/3rd）或后过滤（5th）二者必居其一。
- **反事实 2**：若只做 2.5D → 缺 z 一致性，Hausdorff 受损；但 3rd 无 3D 仍达 0.877，说明 2.5D+大模型+后处理可补偿（非致命劣势）。
- **反事实 3**：若用旧 Dice 选模 → 新指标下系统性高估（0.9108 vs 0.8933），LB 排名受损；换选模协议是低成本动作。
- **反事实 4**：若直接以 Hausdorff 为训练损失 → 失败（3rd）；指标对齐应作用于选模/后处理。
- **边界**：3D 路线的显存门槛高（224×224×80 体积训练，5th 提到需 48G 单卡 A6000）；资源受限时 2.5D+CLS+集成是可行替代。

## 8. 悬案与失败学

**悬案**

1. 2nd place（337400）未收录，而 3rd 自称"similar to 2nd without 3D models"——四强中唯一缺失的结构。
2. **"Incorrect masks"（319963,70）+ 续帖（321979,43）未收录**：错误标注的规模、模式与修复方式未知；1st 的"without wrong annotated cases"只给结论。
3. **"LB could be wrong"（324934,47）+ "Hausdorff usage"（319215,40）未收录**：新指标实现与榜单行为争议——影响所有队伍的选模决策。
4. "2.5D Image Training"（322549,124）与 "MMsegmentation 模板"（323921,104）未收录：1st 的重要参考源（CarnoZhao/awsaf49 的公共资产）正文未存档。

**失败学（跨队合集）**

- 损失类：Hausdorff distance loss（3rd）；正负样本平衡（3rd）。
- 数据类：亮度调整（3rd，花了很多时间无收益）；外部 CT 数据（3rd，需 GAN 域适配）；"CenterCrop 去边"几乎无影响（1st 2.5D）。
- 资源类：无 3D（3rd 遗憾）；Kaggle GPU 两个月单模型仅 ~0.875（3rd 的自述曲线说明"大模型+租卡"阶段的必要性）。
- 隐藏提示：1st 明确"部分模型不用错误标注 case"——数据清洗是与架构同级的杠杆。

## 9. 图表证据

> 路径相对本文件（`analysis/deep/`）：`../../intel/uw-madison-gi-tract-image-segmentation/bodies/<topic>_img/NN.png`

**图 1：1st 的完整管线（三分层分割 + CLS 门控 + 清理）**（topic 337197）——`../../intel/uw-madison-gi-tract-image-segmentation/bodies/337197_img/01.png`

*读图结论*：中间"Segmentation"列有三路——**w/o ambiguous → UPerNet**（排除肠末端 5 层模糊区）、**Anno-only → UNet**（只用有标注切片）、**All-data → 3D 模型**（全量）；左侧竖条标注 head/anno/5-layer ambiguous/foot；下方 CLS 模型（All-data）→ `#pixels check` → Clean predictions。**"数据子集×模型角色"配对的完整结构图**，也是本文 M1/M2 的直接图证。

**图 2：ASPP 结构（资源帖引用的分割模块）**（topic 320060）——`../../intel/uw-madison-gi-tract-image-segmentation/bodies/320060_img/01.png`

*读图结论*：同一特征图用 rate 6/12/18/24 的并行空洞卷积重采样 → 多尺度上下文；资源帖的基线从 DeepLabV3+ 0.810 → ASPP+SE 0.817，是"**多尺度感受野对器官尺度差异有效**"的入门证据（胃/大小肠尺寸差异大）。

**图 3：SE（Squeeze-Excitation）结构（资源帖引用）**（topic 320060）——`../../intel/uw-madison-gi-tract-image-segmentation/bodies/320060_img/02.png`

*读图结论*：通道挤压（全局池化）→ 两层 FC + sigmoid → 逐通道重加权（excitation）。资源帖把它加进 DeepLabV3+ 后 LB +0.007——**通道注意力在小数据分割上的低成本增益**（后续 5th 的 convnext/segformer 内置同类机制）。

## 10. 对既有笔记/playbook 的修订点

1. `notes/cv/uw-madison-gi-tract-image-segmentation.md` 升级（现为浅版）：补 6 篇作者/票数、四方案 × 12 维对照、数字账（0.810→0.828、0.875→0.890、0.817→0.877、old/new 指标 0.9108/0.8933）与 3 张图证。
2. `playbook/cv.md`（医学分割节）增补：
   - **部分标注三层处理**：缺失≠空（子集分层）、错误标注（清洗/排除 case）、语义模糊区（规则排除）；
   - **空切片门控**：CLS 二分类 + 像素阈值（>12px）或后过滤（<50px）；
   - **2.5D/3D 融合**：3D 保 z 一致性（Hausdorff 友好）、2.5D 供多样性；logits 加权（0.4/0.6）与阈值重扫；
   - **几何视角多样性**：沿 x/y/z 三轴切 2.5D；
   - **指标切换应对**：选模指标对齐竞赛指标 > 直接改损失（Hausdorff 不可导）；
   - **后处理套餐**：小面积过滤 + 连续切片起止规则 + 门控阈值。
3. `playbook/00-通用方法论.md` 增补：**"训练损失/局部指标 ≠ 竞赛指标"**（选模协议是一等公民）；**"数据子集×模型角色配对"**（同一批数据按质量分层喂不同模型）。
4. `analysis/THEORY.md`（Batch 4 收尾扩 v0.4）候选：
   - **L51｜部分标注分层用法**：anno-only 训精细模型、全量训鲁棒模型、模糊区排除；证据 = 本场 1st（图）+ 3rd/5th 佐证。
   - **L52｜指标变更先改选模协议**：旧 Dice 选模高估 0.018（MONAI）；Hausdorff loss 失败（3rd）；证据方向一致。
   - **L53｜几何视角多样性**：x/y/z 三轴 2.5D 切法 + 全平均（5th 单 0.875→集成 0.889）。

## 11. 出处

- 3D MONAI（yiheng，162 票）：https://www.kaggle.com/competitions/uw-madison-gi-tract-image-segmentation/discussion/325646
- 资源汇总（140 票）：https://www.kaggle.com/competitions/uw-madison-gi-tract-image-segmentation/discussion/320060
- 1st（127 票）：https://www.kaggle.com/competitions/uw-madison-gi-tract-image-segmentation/discussion/337197
- 1st 2.5D 部分（56 票）：https://www.kaggle.com/competitions/uw-madison-gi-tract-image-segmentation/discussion/337217
- 5th（46 票）：https://www.kaggle.com/competitions/uw-madison-gi-tract-image-segmentation/discussion/337268
- 3rd（45 票）：https://www.kaggle.com/competitions/uw-madison-gi-tract-image-segmentation/discussion/337468
- 缺口登记（未收录正文）：2nd(337400)、322549、323921、320692、329396、326035、Incorrect masks(319963/321979)、LB could be wrong(324934)、Hausdorff usage(319215)、330336 等
