# BirdCLEF 2025 深读：多轮 Noisy Student 自训练工程

> 赛事：Research ｜ 主题 audio（鸟类声景识别）｜ 2031 队 ｜ 代码赛 ｜ 指标：BirdCLEF ROC AUC（206 类多标签）
> 材料基础：`digests/birdclef-2025.md`（6 篇：1st 263 票/recipe 119/2024 技法汇总 73/5th 69/系列索引 55/2nd 54；80 条索引）+ 11 张图
> 深读时间：2026-10（Tier A #52）

## 0. 一句话重述：这道题真正在考什么

题面是"声景中 206 类鸟类（含两栖/昆虫）多标签识别，ROC AUC"，实际被考的是**半监督自训练工程**：

1. **范式已经变了**：2nd 原话——"2023 之前是 Additional Data is All You Need，2024 起变成 Journey Down the Rabbit Hole of Pseudo Labels"。头部全部依赖对未标注 soundscapes 的伪标签迭代；1st 的监督基线只到公榜 **0.872**，四轮自训练后 **0.930**。
2. **Noisy Student 的三个旋钮**：① 伪标数据必须以 **MixUp** 方式混入（简单拼接失败；mix 比例 0→1.0 对应 0.872→0.898，1.0 最好）；② 每轮伪标要做 **power transform**（概率取幂，压制"自信噪声"，否则第 3 轮起不收敛）；③ **Stochastic Depth（drop_path=0.15）**只在自训练有效——这三点共同定义了"noisy student"。
3. **预训练是第二引擎**：2nd 用 Xeno-Canto 大规模预训练（7400–7800 类）把 0.83–0.84 抬到 0.86–0.87；但只用往届竞赛数据预训练反而变差——**预训练语料的规模与多样性是关键**。
4. **输入/架构/推理**：20s chunk（1st 的时长对照 5/10/15/20/30s = 0.842/0.864/0.87/0.872/0.872）+ SED head + 小 EfficientNet（B0/B3/v2s/nfnet_l0）；**framewise 重叠平均**（1D 版滑窗 TTA，+0.002–0.003）；平滑/delta-shift TTA/OpenVINO。
5. **稀有类与家族标签陷阱**：Insecta 的科级标签（Cicadidae/Gryllidae/Tettigoniidae）实际与特定区域物种绑定——混入家族级数据有害；改成"按 Xeno-Canto 物种打新标签"训练专用模型才有效（+0.002–0.003）。
6. **验证的失效与例外**：2nd 实测 <1% AUC 差异时 CV 与 LB 几乎无相关；1st 直接"只用 public LB"（host 明示公私同分布，且事后证明诚实）。这与多数场次相反，是本场可登记的例外（对照 T18）。

一句话：**这是一场"自训练工程"比赛**——模型小、数据少，胜负在伪标签的混合方式、降噪变换与迭代停止点上。

## 1. 材料与角色

| 帖子 | 作者 | 票数 | 角色与独有信息 |
| --- | --- | --- | --- |
| [583577](https://www.kaggle.com/competitions/birdclef-2025/discussion/583577) 1st | — | 263 | **Multi-Iterative Noisy Student**：20s chunk；SED+framewise 重叠平均；power transform（1→1/0.65→1/0.55→1/0.6）；WeightedRandomSampler（按标签和加权）；drop_path 0.15；4 迭代 0.909→0.918→0.927→0.930；Amphibia/Insecta 专用模型；7 模型跨阶段集成；公 0.933/私 0.930 |
| [573066](https://www.kaggle.com/competitions/birdclef-2025/discussion/573066) Recipe 0.872 | — | 119 | mel 参数从 0.810→**0.859**（单参数调优）；FocalBCE；RandAug/erasing/时频掩码 + MixUp(p=1)；中层特征池化；CSV 人声过滤；集成 0.854–0.859→0.872 |
| [572928](https://www.kaggle.com/competitions/birdclef-2025/discussion/572928) 2024 技法汇总 | — | 73 | 上届 top10 技法表：伪标、SED、EfficientNet、集成、时序平滑、OpenVINO；外部数据混合结果 |
| [583312](https://www.kaggle.com/competitions/birdclef-2025/discussion/583312) 5th | — | 69 | 三阶段自蒸馏（train_audio → 自蒸馏 ×4-5 → +soundscapes ×2）；VAD+人工清理人声/稀有类段；13 模型；2.5s 重叠 + smoothing [0.1,0.8,0.1]；公 0.928/私 0.924 |
| [567499](https://www.kaggle.com/competitions/birdclef-2025/discussion/567499) 系列索引 | — | 55 | 2020–2024 历年竞赛与冠军链接（BirdCLEF 方法考古入口） |
| [583699](https://www.kaggle.com/competitions/birdclef-2025/discussion/583699) 2nd | — | 54 | 预训练（7400–7800 类）+ 伪标 2–3 轮 + 1/0.1 置信阈值 + 后处理（每文件 top 概率缩放 +0.005–0.01）+ TTA（+0.005–0.008）；人工听音清理 alien speech；发现"去掉无鸟段反而降分" |

**材料缺口（受"不扩采"约束，登记备查）**：Human voice in the recordings(568886,108 票)、"Why is it always sadness?"(567495,83)、Additional dataset for rare classes(570760,72)、Unstable Experiments(570402,55)、LB probing(570837,47)、CV vs LB(568303,45)、2025 Family Portrait(567672,43) 等未收录——**人声处理与稀有类数据**是主要缺口。

## 2. 逐方案对照矩阵

| 维度 | 1st | 2nd | 5th | Recipe |
| --- | --- | --- | --- | --- |
| Chunk/特征 | 20s；mel 224 bins、n_fft 4096、hop 1252；3×重复 mel | 5s；Spec→2D CNN | 10s；log(mel+1e-6) | — |
| 主干 | SED + effnet_b0/b3/b4、regnety、nfnet_l0 | SED/MLP + effnetv2_s、nfnet_l0 | SED + effnetv2_s/b3、effnet_b3_ns/b0_ns | EfficientNet（中层特征池化） |
| 预训练 | 引 2024 预训练经验 | **Xeno-Canto 7400–7800 类预训练**（关键） | 无（自蒸馏替代） | — |
| 自训练 | **Noisy Student**：MixUp(比例 1.0)+power transform+drop_path 0.15；4 迭代 | 伪标（阈值 0.5/0.1）+按类替换采样；2–3 迭代 | **自蒸馏**：teacher→伪标+原标签，权重重初始化；4–5 轮 + soundscapes 2 轮 | — |
| 采样/损失 | CE（理由：不平衡下更稳）；标签不归一化；WeightedRandomSampler | Focal+BCE；Balanced/平方权重/上采样 | Focal γ=2；稀有类复制 | FocalBCE |
| 推理/后处理 | framewise 重叠平均；平滑 [0.1,0.2,0.4,0.2,0.1]；delta shift；OpenVINO | 每文件 top 概率缩放；2.5s 重叠 TTA；5 折全提交 | 2.5s 重叠 + 平滑 [0.1,0.8,0.1]；OpenVINO | 后处理 + 集成 |
| 集成 | 7 模型跨阶段；**等权最好（私 0.935）** | 3 模型（不同预训练/迭代/采样） | 13 模型（4 组 seed） | 4 模型 0.854–0.859→0.872 |
| 验证 | 无好 CV，仅 public（host 保证） | 分层/按作者分组；高分段相关消失 | 5 折 | public |
| 成绩 | 公 0.933/私 0.930 | 公 0.922/私 0.918（TTA） | 公 0.928/私 0.924 | 公 0.872 |
| 失败清单 | 320+ 想法 95% 红（未列）；target XC 数据有害；family 标签混入有害 | 往届数据预训练、XC/iNat 数据、主数据软标签、time flip | CNN/1D 模型、过多增强、低排名类 power 后处理 | raw-wave 增强有害 |

## 3. 共识、分歧与裁决

### 共识一：伪标签自训练是主引擎（1st/2nd/5th + 2024 汇总）

1st：监督 0.872 → 4 轮自训练 0.930；
2nd：ablation baseline 0.83–0.84 → 预训练 0.86–0.87 → 伪标 1 0.89–0.895 → 伪标 2–3 0.90–0.91 → TTA 0.922 → 后处理 +0.005–0.01；
5th：3 阶段自蒸馏（stage1 0.839 → distill ×5 0.884 → +soundscapes 0.921）。

**裁决**：有未标注目标域音频时，自训练是最大的单项杠杆；本场三家用了不同变体（noisy student / 替换采样 / 迭代自蒸馏），方向一致。置信度：高。

### 共识二：预训练语料要"大而多样"（2nd 的对照；1st/5th 受益）

2nd：Xeno-Canto 7400–7800 类预训练 +0.03；只用往届竞赛数据预训练变差；新下载的 2025 快照不如 2024 预训练权重；
1st：2024 预训练经验 + 2025 专用模型。

**裁决**：预训练的价值来自**语料规模与物种多样性**，不是"再训一遍"；这与 T8（外部数据有效性条件性）一致。置信度：高。

### 共识三：SED + framewise + 重叠平均推理（1st/2nd/5th）

1st：framewise 重叠平均 +0.002–0.003；"1D 版滑窗分割"；
2nd：2.5s 重叠 TTA +0.005–0.008；
5th：2.5s 重叠 + 平滑。

**裁决**：把 chunk 当独立样本会浪费 SED 的帧级输出；重叠平均是最稳的推理端增益。置信度：高。

### 共识四：小 EfficientNet + 适度的增强/后处理（全员）

骨干集中在 B0/B3/v2s/nfnet_l0；增强有效项：MixUp/Sumix、增益/噪声、时频掩码（有争议）；后处理：时序平滑/hop 后缩放/OpenVINO。

**裁决**：CPU 推理限制决定模型规模上限；工程（量化、复用频谱、多进程）与后处理是必备项。置信度：高。

### 分歧一：伪标签的降噪方式

1st：**power transform**（概率取幂 >1），让多轮迭代继续收敛（1/0.65/0.55/0.6）；
2nd：阈值（>0.5 保留、<0.1 置零）+ 软标签；
5th：teacher 预测与原标签直接混合。

**裁决**：共同目标是"只保留高置信、压制低置信"；1st 的幂变换是**多轮迭代不崩**的关键（第 3 轮起尤其），比硬阈值更平滑。置信度：中高。

### 分歧二：验证与 LB 反馈

2nd：<1% AUC 差异时 CV-LB 无关（高分段散点图）；
1st：无好 CV，"只用 public"（host 明示公私同分布，事后证明诚实）；
5th：5 折 + 多 seed。

**裁决**：本场是 T18 的例外——host 明确公私同分布且实际相关良好，**LB 反馈可用**；但前提是 host 的诚实与多 fold/seed 集成把 LB 噪声降下来。不可默认迁移到其他场次。置信度：高（本场）/低（跨场）。

### 分歧三：数据清理的边界

2nd：去掉"无鸟段"**降低** LB（false positives 帮助泛化）；只清 alien speech；
5th：VAD+人工清理人声、并人工标注稀有类发声段。

**裁决**：清理应针对**异质干扰（人声/讲解/alien speech）**；"无目标段"可能提供正则化，删除需验证。置信度：中高。

### 分歧四：损失函数

1st：CE 最佳（在不平衡下惩罚过度代表类）；
2nd：Focal+BCE；5th：Focal γ=2；Recipe：FocalBCE。

**裁决**：损失可因训练方案不同而互换（1st 做过多组对照），**平衡策略与阈值/后处理比损失名更重要**。置信度：中。

## 4. 增量数字账

| 动作 | 数字 | 来源 |
| --- | --- | --- |
| 1st chunk 时长对照 | 5s 0.842 / 10s 0.864 / 15s 0.87 / 20s 0.872 / 30s 0.872（5 SED b0 集成） | 1st |
| 1st mix 比例对照 | 0 → 0.872；0.25 → 0.883；0.5 → 0.887；0.75 → 0.89；1.0 → **0.898** | 1st |
| 1st 迭代分数 | 监督 0.872（LB）→ 迭代 1 (power 1) 0.909 → 2 (1/0.65) 0.918 → 3 (1/0.55) 0.927 → 4 (1/0.6) **0.930**；第 5 次失效 | 1st |
| 1st drop_path | 0.15；自训练 +0.005（监督训练无增益） | 1st |
| 1st 推理 | framewise 重叠平均 +0.002–0.003；最终 7 模型等权私 **0.935**（公 0.933/私 0.930 的选中版） | 1st |
| 2nd 预训练 | 7400–7800 类 Xeno-Canto；0.83–0.84 → 0.86–0.87 | 2nd |
| 2nd 伪标 | 迭代 1 选 4,430 文件、迭代 2 选 1,483、迭代 3 选 1,437；阈值 0.5 保留 / <0.1 置零 | 2nd |
| 2nd 后处理/TTA | 每文件 top 概率缩放 +0.005–0.01；2.5s 重叠 TTA +0.005–0.008（0.917→0.922 公/0.91→0.918 私） | 2nd |
| 5th 阶段链 | stage1 0.839 → 蒸馏 ×5 0.884 → +soundscapes 0.921（effv2s）；最终 13 模型公 0.928/私 0.924 | 5th |
| Recipe | mel 参数 0.810→0.859；集成 0.854–0.859 → 0.872 | 573066 |
| 2nd 无鸟段实验 | 跳过无发声段 → LB 下降（保留整段更好） | 2nd |
| 1st Amphibia/Insecta 专用模型 | 700 物种/17,844 样本；min 1 样本/物种；+0.002–0.003 | 1st |
| 赛事 | 2031 队；ROC AUC；80 帖 | 元数据 |

**结构校验（2 处吻合）**

1. 1st 的 mix 比例与迭代分数两条曲线单调递增、互相独立，证明"混入（mixup）+ 幂变换"是叠加增益 ✓；
2. 2nd 的 3 轮伪标选样数量递减（4430→1483→1437）与"高置信样本越用越少"的直觉一致 ✓。

## 5. 机制推演

**M1｜Noisy Student 的数学直觉**：直接重复"教师输入→教师输出"不提供新信息，学生只能收敛到教师（甚至累积误差）；当输入被加噪（MixUp/drop path），学生要解释"为什么教师对干净输入给 A 高分"，就必须学**对噪声不变的特征**而不是记忆噪声。1st 的对照（mix 0→1.0 单调涨分；drop path 只在自训练有效）直接支持该机制。

**M2｜power transform 为什么能救多轮迭代**：多轮伪标后，噪声样本的"自信概率"（0.5–0.7）越来越多，若用 logits temperature 反向放大 >0.5 的概率会污染训练；对概率做幂 p>1（等价于把 <1 的概率整体压小、保持高峰形状）能保留真正的高置信信号、削减噪声地板（图 3），使第 3/4 轮继续收敛。

**M3｜伪标采样的信息权重**：soundscape 的"标签和（sum of max probs）"反映教师对该文件的确定程度；用它做 WeightedRandomSampler，等价于按教师置信度加权采样，弱标签文件（几乎是未标注）被降权。2nd 的"按原类分布采样、但以 0.4 概率替换为软标签"是另一种分布保持策略。

**M4｜framewise 重叠平均 = 时序 TTA**：SED 每个时间帧都输出预测；相邻 chunk 给同一帧不同的上下文，平均后降低方差并覆盖跨 chunk 事件。相比"中心 5s 取 max"，信息利用率显著更高（1st 的 1D 滑窗类比）。

**M5｜预训练与域适应的关系**：大规模 Xeno-Canto 预训练学到的是"鸟类声学的一般特征"；在当年数据微调时，模型只需适配本场分布。2nd 的"往届竞赛数据预训练失败"说明小语料预训练不足以提供可迁移表示（与 T8：预训练有效性取决于语料规模/多样性）。

**M6｜家族级标签的生物语义陷阱**：Insecta 的科级标签（如 Tettigoniidae）在标注体系里可能指"本地区某几个物种的集合"，而 Xeno-Canto 的同科录音来自全球不同物种；直接混训会让模型学到"科"的水平而不是本场目标。**标签的语义边界 ≠ 生物分类学边界**——按物种打新标签才有正收益。

## 6. 证据分级

| 断言 | 等级 | 说明 |
| --- | --- | --- |
| 1st 全流程与对照表 | 自述 + 3 张图 + 公开 inference notebook/数据集 | 高 |
| 2nd 预训练/伪标/TTA 阶梯 | 自述 + 图 + GitHub + paper | 高 |
| 5th 三阶段自蒸馏 | 自述 + 4 张图 + 代码/模型 | 中高 |
| Recipe mel 参数增益 | 自述（5 次提交/天调参） | 中 |
| 2024 技法汇总 | 二手汇总之表 | 中 |
| "无鸟段删除反而降分" | 2nd 单队实验 | 中 |

## 7. 边界条件与反事实

- **反事实 1**：无伪标自训练 → 1st 停在 0.872；2nd 停在 0.86–0.87。自训练是第一杠杆。
- **反事实 2**：伪标不与 MixUp 结合（单独拼接）→ 1st 明确失败；mix 比例 <1.0 → 0.883–0.89。
- **反事实 3**：不做 power transform → 第 3 轮迭代起不收敛/无增益。
- **反事实 4**：去掉"无鸟段" → 2nd 的 LB 下降（false positives 的正则化作用）。
- **反事实 5**：只用往届数据预训练 → 2nd 实测变差。
- **边界**：结论依赖"有足量未标注目标域音频 + 评测为 AUC + host 保证公私同分布（LB 反馈可用）"；无未标注数据或分布不一致的场次不适用。

## 8. 悬案与失败学

**悬案**

1. **1st 的第 5 次迭代为何失效**：只有"power 调整也无法继续"的现象，没有机制解释。
2. 2nd 的第 3 次伪标必须换 OOF 策略、且增益不再——未完全解释。
3. Human voice(568886)、rare-class 数据(570760)、Unstable Experiments(570402) 未收录——人声/稀有类的完整处理缺失。
4. 5th 的 seed 复用错误（Group A/B 同 seed）对集成影响未量化。

**失败学（跨队合集）**

- 1st：320+ 想法 95% 被否（未列）；target Xeno-Canto 数据通常有害；family 标签混入有害；第五轮迭代失效。
- 2nd：仅用往届数据预训练；XC/iNat 数据；主数据软标签；time-flip；去掉无鸟段。
- 5th：CNN/1D 模型；过多增强；低排名类 power 后处理（怕过拟合未用）。
- Recipe：raw-wave 上的任何增强/处理都有害。

## 9. 图表证据

> 路径相对本文件（`analysis/deep/`）：`../../intel/birdclef-2025/bodies/<topic>_img/NN.ext`

**图 1：1st 的完整训练/自训练循环**（topic 583577）——`../../intel/birdclef-2025/bodies/583577_img/01.png`

*读图结论*：监督（目标物种 + Amphibia/Insecta 专用模型）→ LB 反馈（0.887 教师）→ 自训练循环（伪标 soundscapes → power transform → 置信采样 → MixUp 混训 → 选新教师）；迭代 1–4 = 0.909/0.918/0.927/0.930；最终 7 模型跨阶段集成 0.933/0.930。**一图概括整篇解法**。

**图 2：power transform 的降噪效果**（topic 583577）——`../../intel/birdclef-2025/bodies/583577_img/03.jpg`

*读图结论*：蓝=第 3 轮原始伪标（噪声地板 + 高峰），橙=取幂 1.82 后：高置信峰保留（略降）、低置信噪声被压到 ~0。**多轮自训练不崩的关键变换**。

**图 3：2nd 的验证-LB 相关性在高分段消失**（topic 583699）——`../../intel/birdclef-2025/bodies/583699_img/04.png`

*读图结论*：Mean ROC AUC 0.97–0.98 区间，0.90+ 的公开分互不相关；"突破 0.9 后相关性决定休息"。**高分段的 CV 失效**，LB 反馈成为主信号（本场 host 诚实 + 多 fold 集成降噪）。

**图 4：5th 的三阶段自蒸馏**（topic 583312）——`../../intel/birdclef-2025/bodies/583312_img/02.png`

*读图结论*：stage1 监督；stage2 teacher→伪标+原标签→student（权重重初始化、迭代 4–5 次）；stage3 加入 train_soundscapes（1:1）。**自蒸馏的标准流水线图**（与 1st 的 noisy student 同族）。

**图 5：5th 的人机协同数据清理工具**（topic 583312）——`../../intel/birdclef-2025/bodies/583312_img/01.png`

*读图结论*：Streamlit 谱图标注器（VAD 筛出含人声文件后人工听音、标出鸟叫段）。**"清理什么"由人耳决定**——与 2nd 的"无鸟段保留"共同说明数据清理的边界。

## 10. 对既有笔记/playbook 的修订点

1. `notes/audio/birdclef-2025.md` 升级（现仅 43 行浅笔记）：补 6 篇作者/票数、四方案 × 9 维对照、数字账（0.872→0.930、mix 比例、幂变换、0.933/0.930）与 5 张图证；新增"Noisy Student 旋钮"与"验证例外"节。
2. `playbook/multimodal-audio-other.md`（音频识别节）增补：
   - **自训练配方（Noisy Student）**：伪标以 MixUp 混入（比例可到 1.0）、power transform 降噪、按置信度采样、drop_path、迭代停止；
   - **预训练**：大规模多样语料（Xeno-Canto）有效，小语料/往届数据无效；
   - **SED + framewise 重叠平均**（时序 TTA）；平滑/delta shift；
   - **稀有类与家族标签**：语义边界 ≠ 分类学边界，需按物种重标；
   - **验证失效的例外条款**：host 保证公私同分布时可用 LB 反馈，但需多 fold/seed 集成降噪。
3. `playbook/00-通用方法论.md` 增补：**"自训练必须加噪"**（重复伪标无信息增益）；**"伪标的置信压制（幂变换/阈值）是多轮迭代的保险丝"**；**"数据清理要区分异质干扰与无目标段"**。
4. `analysis/THEORY.md`（Batch 6 末汇总 v0.6）候选：
   - **L80｜Noisy Student 三旋钮**（mixup/幂变换/drop path；证据 = 本场 1st）；
   - **L81｜预训练语料的规模-多样性条件**（2nd 的对照 + T8 扩证）；
   - **L82｜framewise 重叠平均 = 时序 TTA**（1st/2nd/5th）。

## 11. 出处

- 1st（263 票）：https://www.kaggle.com/competitions/birdclef-2025/discussion/583577
- Recipe 0.872（119 票）：https://www.kaggle.com/competitions/birdclef-2025/discussion/573066
- 2024 技法汇总（73 票）：https://www.kaggle.com/competitions/birdclef-2025/discussion/572928
- 5th（69 票）：https://www.kaggle.com/competitions/birdclef-2025/discussion/583312
- 系列索引（55 票）：https://www.kaggle.com/competitions/birdclef-2025/discussion/567499
- 2nd（54 票）：https://www.kaggle.com/competitions/birdclef-2025/discussion/583699
- 缺口登记：568886、567495、570760、570402、570837、568303、567672 未收录正文
