# ISIC 2024 深读：GBDT 元模型 × 图像 OOF 特征 × 患者内相对化

> 赛事：Research ｜ 主题 cv（医学影像 + 表格）｜ 2739 队 ｜ 代码赛 ｜ 指标：ISIC pAUC-aboveTPR（高 TPR 区间的部分 AUC，越高越好）
> 材料基础：`digests/isic-2024-challenge.md`（6 篇正文：1st/2nd/9th/12th + 296 票数据帖 + 67 票增广帖；80 条讨论索引）+ 10 张图（533196×5 / 532642×2 / 517141×3）
> 深读时间：2026-10（Tier A #31）

## 0. 一句话重述：这道题真正在考什么

题面是"3D-TBP 皮肤病变裁剪图 + 元数据 → 恶性二分类"，实际被考的是**极端不平衡下的表格-图像融合排序赛**：

1. **正样本约 0.1%**：训练集 393 张恶性 vs 40 万+ 良性（约 1:1000）；指标 pAUC 只统计高 TPR 区间 → "在最可疑样本上的排序"决定一切，阈值与校准无关。
2. **标准结构 = GBDT 主模型 + 图像模型 OOF 分数当特征**：四队全部沿用同一骨架，差异在特征工程、采样、噪声注入与集成细节；图像模型单独只有 ~0.15，融合后到 ~0.18（9th/12th 数字）。
3. **患者内相对化（ugly duckling）是领域先验**：临床判读看"该病变对这名患者是否异常"，1st 的 LOF、2nd 的患者内标准化、12th 的 KNN(k=5) 都在把绝对特征转成相对特征。
4. **外部/合成数据的边界**：往届 ISIC 数据直接混训失败（2nd 的域分类器 AUC 0.99 证明分布差异），但预训练式使用有效（1st 私榜 +0.002）；SD 合成数据提升单模型却对最终集成无增益。

一句话：**这是一场"元模型工程"比赛**——树模型是主体，图像模型是特征源，患者是归一化单位，CV 纪律决定公私榜排名。

## 1. 材料与角色

| 帖子 | 作者 | 票数 | 角色与独有信息 |
| --- | --- | --- | --- |
| [515356](https://www.kaggle.com/competitions/isic-2024-challenge/discussion/515356) More Training Data | Nischay Dhankhar | 296 | 往届 ISIC 2017–2020 JPEG 数据集（重裁剪到 224/256、统一格式）；给出 2024 训练集正负比（393 vs 40 万+）与三届分布 |
| [533196](https://www.kaggle.com/competitions/isic-2024-challenge/discussion/533196) 1st | — | 149 | 10-seed t 检验特征准入（后期降到 p<0.2 靠公榜 → 公榜更好/私榜略差）；150 GBDT rank 平均；LOF 患者内特征；EVA02+EdgeNeXt；OOF 标准化 + 高斯噪声 σ=0.1；往届数据预训练 +0.002 私榜；SD1.5 合成 6000 张（个体有效、集成无效） |
| [532704](https://www.kaggle.com/competitions/isic-2024-challenge/discussion/532704) 2nd | — | 71 | Triple Stratified Leak-Free CV；54 GBDT × seed 平均；9 图像模型 / 5 训练设置（mixup、aux 表格、aux iddx 聚类、TIP 自监督）；患者内标准化 + Tabular Ugly Ducklings；外部数据失败 + 域分类器 AUC 0.99 |
| [532577](https://www.kaggle.com/competitions/isic-2024-challenge/discussion/532577) 9th | — | 81 | 3 条 tabular pipeline × 3 backbone；5% 负样本 + 正样本 ×10；只训 3 epoch；hill-climb 权重；发现 A.Resize 位置 bug（14.8→15.4–15.5）；CV 0.182 / LB 0.187 一致 |
| [532642](https://www.kaggle.com/competitions/isic-2024-challenge/discussion/532642) 12th | — | 65 | GLCM + KNN(k=5) ugly duckling 特征；OOF 加高斯噪声；4 GBDT（含 1 个不用图像特征）× 15 fold × 5 seed；best LB 0.183/0.171；FTTransformer 与伪标签失败 |
| [517141](https://www.kaggle.com/competitions/isic-2024-challenge/discussion/517141) Image Augmentations | — | 67 | 18 种增广在正/负样本上的可视化 + microscope 增广；历年 ISIC 冠军配方清单 |

**材料缺口（受"不扩采"约束，登记备查）**：3rd(532919)、4th(532760)、8th "Trust your CV"(532728)、7th "A good CV is all you need"(532687)、13th "God Bless CV"(532654)、11th(532595)、54th 特征工程(532644)、Benchmarking(527023,145 票)、LB probing(517139,130 票)、Private 24th/Public 1st(532564,81 票) 等均未收录正文。**8th/7th/13th 的标题集体指向"CV 至上"，与 1st 的"后期转向公榜导致私榜变差"构成同题张力**（见 §8）。

## 2. 逐方案对照矩阵

| 维度 | 1st | 2nd | 9th | 12th |
| --- | --- | --- | --- | --- |
| 主结构 | GBDT 集成 + 图像 OOF 特征 | GBDT 集成 + 图像 OOF 特征 | 3 条 tabular pipeline + 3 图像模型 → hill-climb | 4 GBDT + 图像 OOF + GLCM/KNN 特征 |
| 表格特征 | 公共 notebook + 患者内 LOF + 病变面积（总/按部位） | 公共 notebook 特征 + 患者内标准化（按 location/location_simple/anatom_site）+ Tabular Ugly Ducklings | 上下文统计（z-score/range/skew/kurtosis/max 比值）+ rank/groupby | GLCM + KNN(k=5) + age 差分 + 分位数 |
| 图像模型 | EVA02-small + EdgeNeXt-base（1:1 batch） | 9 个模型 / 5 设置：eva02_small、deit3_small、beitv2_base、convnextv2_tiny/nano、swinv2_small、resnext50、swin_tiny | effnet_b0 ×2、swinv2_tiny、convnextv2_tiny | EfficientViT-v2、EdgeNeXT-base、EffNet-B2/B0、EVA02 |
| 图像→表格 | 每模型标准化 OOF（p1 −0.44 / p99 4.99）+ 相对患者均值比率 + 高斯噪声 σ=0.1 | 0–3 个图像特征作 meta（数量做多样性） | 每 pipeline 用 1 个 backbone 的预测 | 5 模型 OOF + 高斯噪声 |
| 不平衡 | 每 batch 1:1 平衡 | 每 epoch 1:3 / 1:5 undersampling | 只用 5% 负样本、正样本 ×10 | 正上采样 + 负下采样 |
| 训练预算 | 200 epoch 上限、早停（容忍 10 次）；验证频率递增进 | 50–200 epoch，**不用早停** | **3 epoch** | 15 fold × 5 seed |
| CV 协议 | 5-fold Stratified Group + 10 seed t 检验（p 值准入） | Triple Stratified Leak-Free KFold | 5-fold SGKF + 5 seed 预筛 + LB 确认 | Triple Stratified |
| 集成 | 150 模型 rank 平均 → GBDT | 54 模型 × seed 平均 | hill-climb 权重 | 4 GBDT mean |
| 外部/合成 | 往届 3 类预训练（+0.002 私榜）；SD1.5 合成 6000 张（个体更好、集成未用） | 往届数据放弃（域分类器 AUC 0.99） | — | 往届数据、伪标签均失败 |
| 报告成绩 | 公榜 ~0.185→更好、私榜 0.173→略差 | 图像 CV 0.1515–0.1612 | 3 pipeline LB 0.183/0.183/0.180 → blend 0.186 → 最终 CV 0.182 / LB 0.187 | best LB 0.183/0.171；best CV 另训 |
| 失败清单 | hard negative 采样、往届数据混训、多增广平均预测、聚类 z-score（私榜无效） | 往届数据混训（含直方图匹配）；域差异未识别 | hard negatives、focal loss、mixup 进集成、stacking、**0.5 缩放/rank 集成、Dullrazor、发丝增广、lesion-id 权重、scratch 训练 | 往届数据、伪标签；FTTransformer（CV 0.178/LB 0.179/私 0.165）不如 GBDT |

## 3. 共识、分歧与裁决

### 共识一：图像模型的正确用法是"OOF 分数当特征"，不是直接加权（4/4）

四队都以 GBDT 为主模型；图像模型只通过 OOF 预测进入表格特征（1st 还做 per-model 标准化 + 相对患者均值比率）。**图像单模型 LB ~0.15 vs 融合后 ~0.18**（9th/12th）——表格线是主力，图像线是增量。

**裁决**：GBDT 能条件化图像分数（不同部位/年龄/图像质量下分数含义不同）并学习交互；直接加权平均做不到。前提是 OOF 必须无泄漏（患者隔离）。置信度：高（4 队同构 + 数字层级差）。

### 共识二：患者内相对特征是领域先验（3/4 明确、2nd 体系化）

1st：LOF 分数（CV 0.18149→0.18185）；2nd：患者内标准化（按 location/location_simple/anatom_site）+ Tabular Ugly Ducklings；12th：KNN(k=5) 近邻特征。临床逻辑：恶性判读的显著线索是"这颗痣对该患者不正常"。

**裁决**：医学筛查赛把绝对特征转成"患者内相对特征"是低成本高确定性的增益来源；pAUC 的头部排序区尤其受益。置信度：高（三队独立采用）。

### 共识三：极端不平衡的采样强度决定训练预算（3/4 有明确数字）

1st：batch 内 1:1；2nd：每 epoch 1:3–1:5 undersampling（50–200 epoch）；9th：5% 负样本 + 正样本 ×10（**只训 3 epoch**）；12th：正上采样 + 负下采样。

**裁决**：采样比率与 epoch 数是同一枚硬币的两面——每 epoch 见到的正样本越多，需要的 epoch 越少（9th 3 epoch vs 2nd 200 epoch）。选型应同时决定，不可分开调。置信度：中高。

### 分歧一：往届 ISIC 数据——混训失败 vs 预训练有效

支持方：515356 发布的高质量数据集获 296 票（社区大量使用）；1st 用往届数据训 3 类模型（bkl/melanoma/nevus）做预训练，CV 0.1756→0.1760、公榜 0.180→0.182、**私榜 0.163→0.165**。
反对方：2nd 直方图匹配后仍无提升，训练域分类器区分 ISIC2018 vs 2024 轻松达到 **AUC 0.99** → 放弃；12th 明确"use of past data"失败；515356 评论区也报告"用外部正样本混训导致 train pAUC 虚高、验证不涨"。

**裁决**：与 T8 既有结论完全一致——**预训练式（只迁移表示）有效，直接混训（改变训练分布/先验）失败**；且往届数据集阳性率 1.8%–18%，与本届 0.1% 的先验相差 1–2 个数量级，混训等于改变任务。域分类器 AUC 是量化"能不能混"的标准工具（0.99 → 不能）。置信度：高（三队 + 定量证据）。

### 分歧二：合成数据——个体有效 vs 集成无效

1st：SD1.5 在正样本上微调（50 epoch，batch 8，128×128）→ 生成 6000 张（2 分辨率 × 2 scheduler × 多 prompt）；合成模型在 CV/公榜/私榜上全面略优（图 3：CV 0.1559→0.161、私榜 0.1318→0.1346、公榜 0.1498→0.1508），合成数据模型集成单独看私榜 0.140 vs 真实 0.142；**但加入最终集成无增益 → 未采用**。

**裁决**：合成数据的价值要分两层看——"提升单个模型"与"提升模型集合多样性"不是一回事；若合成模型与真实模型误差高度相关（同 backbone/同数据配方），边际集成收益≈0。判断标准应是"合成模型是否覆盖真实模型的失败区"。置信度：中（单案例，但有完整数字与图证）。

### 分歧三：CV 纪律 vs 公榜依赖（本场最强张力）

1st：前中期用 10-seed 配对 t 检验（多重比较只测最重要改动）；**后期卡在 0.185–0.186 时降低阈值到 p<0.2 并主要靠公榜** → 最终公榜更好、私榜略差（自述的直接代价）。
2nd：自建 Triple Stratified Leak-Free CV（患者隔离 + 恶性比例分层 + 患者图像数分箱）。
9th：每个特征先过 5 seed 组合，再上 LB，最后 CV 0.182/LB 0.187 一致。
12th：同样 Triple Stratified。
未收录的 7th/8th/13th 标题（"A good CV is all you need"/"Trust your CV"/"God Bless CV"）进一步印证本场社区共识。

**裁决**：小提升（≤0.002）在多 seed 噪声内，必须用配对检验/leak-free CV 才可信；t 检验要控制多重比较；公榜可以确认但不能替代 CV——1st 的后期转向是"公榜过拟合"的教科书自述。置信度：中高（1st 亲历 + 三队协议 + 标题证据）。

## 4. 增量数字账

| 动作 | 数字 | 来源 |
| --- | --- | --- |
| 训练集正负比 | **393 恶性 vs 40 万+ 良性**（≈1:1000，0.1%） | 515356 |
| 往届数据集 | ISIC2020 32542/584；ISIC2019 20809/4522；ISIC2018 8197/785（裁剪到 224/256） | 515356 |
| 1st GBDT 规模 | CatBoost/LGBM/XGB × 5 fold × 10 seed = **150 模型**（基础 45 模型无显著差异）；全部训练 < 20 分钟；rank 平均 | 1st |
| 1st 特征准入 | 10 seed 配对 t 检验；只测最重要改动（多重比较）；后期阈值降到 p<0.2 | 1st |
| 1st LOF 增益 | CV 0.18149 → 0.18185 | 1st |
| 1st 往届预训练 | CV 0.1756→0.1760；公榜 0.180→0.182；**私榜 0.163→0.165** | 1st |
| 1st 合成数据（个体均值） | base vs synthetic：CV 0.1559→**0.161**；私榜 0.1318→**0.1346**；公榜 0.1498→**0.1508** | 1st（图 3） |
| 1st 合成数据（集成） | 合成模型集成私榜 0.140 vs 基线 0.142、公榜 ~0.157；加入最终集成无增益 | 1st |
| 1st OOF 噪声 | σ 测试 0.02/0.05/0.08/0.12，最终 **0.1**（LB 探针选定）；标准化预测 p1=−0.44 / p99=4.99 | 1st |
| 2nd GBDT 规模 | 每算法 18 变体 × 3 算法 = 54 模型；全量数据 seed 平均 n=5；num_boost_round 200–300 | 2nd |
| 2nd 图像模型 CV | resnext50 0.1515（最佳）～ swinv2_small 0.1612（最差）；eva02/deit3 0.1534–0.1537 | 2nd |
| 2nd 域差异 | ISIC2018 vs 2024 域分类器 **AUC 0.99** | 2nd |
| 9th pipeline | CV 0.177/0.175/0.175；LB 0.183/0.183/0.180；首次 blend +0.3 → 0.186；最终 CV 0.182 / LB 0.187 | 9th |
| 9th 图像模型 | effnet_b0 LB 0.155 与 0.158（TTA 0.161）；swinv2_tiny 0.159；convnextv2_tiny 0.158 | 9th |
| 9th 采样/预算 | 5% 负样本 + 正样本 ×10；**3 epoch**；lr 1e-4；BCE | 9th |
| 9th Resize bug | A.Resize 在增广列表开头 → 移到归一化前：LB 0.148 → 0.154–0.155 | 9th |
| 12th 结构 | GLCM + KNN(k=5) + 高斯噪声；4 GBDT（含 1 个无图像特征）× 15 fold × 5 seed；best LB 0.183/0.171（CV 0.1804） | 12th |
| 12th 图像模型 | EfficientViT-v2 0.156/0.153；EdgeNeXT 0.156/0.155；EffB2 0.1493/0.154；EffB0 0.151/0.144；EVA02 0.154/0.154 | 12th |
| 12th FTTransformer | CV 0.178 / LB 0.179 / 私榜 0.165（未采用） | 12th |

**结构校验（2 处吻合）**

1. 1st 合成数据结论方向一致：图 3（个体全面更优）与正文"加入最终集成无增益"并不矛盾——前者是单模型均值，后者是集合边际收益；
2. 12th 图像模型 LB/CV 离散度大（EffB0 CV 0.151→LB 0.144），与 1st 的早停过拟合警告、以及全场"LB 波动"主题吻合。

## 5. 机制推演

**M1｜为什么"图像 OOF 当 GBDT 特征"远优于直接加权**：GBDT 能用元数据条件化图像分数的含义（同一分数在不同部位/年龄/设备下价值不同），并自动学习"图像分数 × 表格特征"的交互；直接加权平均把图像模型当成与表格同质的证据，丢失条件化。代价是工程复杂度：OOF 必须无泄漏、预测必须可比（标准化/rank）、还要防特征过拟合（噪声）。

**M2｜早停 → OOF 偏乐观 → 必须加噪**：early stopping 用验证集选择最佳 epoch，OOF 预测因此"看过"验证集 → 当作训练特征时 CV 虚高。1st 与 12th 的解法相同：给 OOF 特征加高斯噪声（1st 用 σ=0.1、通过 LB 探针在 0.02–0.12 中选定；12th 直接加噪）。这是"用验证集预测当特征"的通用陷阱与修法。

**M3｜ugly duckling 的机制**：黑色素瘤判读不是绝对外观判断，而是"与患者自身其他痣的对比"——新发/变化/不典型者可疑。统计实现：患者内 z-score（2nd）、局部离群因子 LOF（1st）、近邻距离 KNN（12th）。pAUC 只关心头部排序 → 相对化把"对本人罕见"的病变推向高分，正对指标胃口。

**M4｜pAUC-aboveTPR 与 rank 集成**：指标只看高 TPR 区间的排序质量 → ① 校准/阈值无关，排名可比性最重要；② 1st 先 `.rank(pct=True)` 再平均，避免各模型分数尺度差异主导集成；③ 9th 用 hill-climb 直接在 CV 上搜权重。反之，9th 发现 "预测 ** 0.5 或 rank ensemble" 反而无效——说明变换要在正确的粒度上做。

**M5｜采样强度 ↔ epoch 预算的耦合**：9th 每 epoch 用 5% 负样本 + 正样本 ×10 → 一个 epoch 就能看到大量正样本，3 epoch 足够；2nd 用 1:3–1:5 的温和欠采样 → 需要 50–200 epoch 遍历信息。两者本质是同一参数的两种设置：**单位训练时间内的正样本曝光量**。据此可预测：采样越激进，越要防过拟合（9th 的 3 epoch 即是防过拟合的采样副作用管理）。

**M6｜域差异为何杀死混训、却不杀死预训练**：往届与本届的差异不只是画风（域分类器 AUC 0.99），还有阳性率先验（1.8%–18% vs 0.1%）与病变裁剪方式。直接混训同时改变了 P(x) 与 P(y|x)；预训练只在表示层吸收 P(x) 的结构，微调阶段用本届数据重建 P(y|x) → 先验被覆盖、域差异被洗掉一部分（1st 私榜 +0.002）。这解释了 T8 中"预训练有效、混训失败"的通用边界。

**M7｜合成数据的"个体-集成"悖论**：合成样本由图 2 可见两类问题——Derm-T2IM 产物带明显伪影（培养皿/标尺样式），1st 自产的 512 图常出现"多个独立痣"（不符合单病变输入分布）。这使合成模型在个体验证上表现好（学到更多恶性纹理），但与真实模型误差相关、且没覆盖真实模型的失败区 → 集成边际收益≈0。合成数据要进集成，需要"覆盖失败区"或"架构异构"，而不是"再来一个更好的单模型"。

## 6. 证据分级

| 断言 | 等级 | 说明 |
| --- | --- | --- |
| 393 正 vs 40 万+ 负 | **数据帖 + 官方规模** | 高 |
| 1st 合成数据个体更优 | **自述 + 图 3 柱状图** | 中高（有图证） |
| 1st 往届预训练 +0.002 私榜 | 自述（代码公开） | 中高 |
| 域分类器 AUC 0.99 | 2nd 自述（方法标准、结论方向由两队佐证） | 中高 |
| 9th Resize bug 0.148→0.154 | 自述（A.Resize 位置可复现） | 中 |
| 12th FTTransformer 数字 | 自述 | 中 |
| 1st 用 LB 探针选 σ=0.1 | 自述（无 CV 支撑；LB probing 是本场已登记的争议话题 517139） | 中低 |
| 7th/8th/13th "CV 至上" | 仅标题（正文未收录） | 低（方向性佐证） |

## 7. 边界条件与反事实

- **反事实 1**：若把图像模型直接与 GBDT 加权（而非 OOF 特征）→ 丢失条件化与交互；四队无一采用。结构性推断。
- **反事实 2**：若 OOF 特征不加噪 → 早停乐观偏差进入 GBDT 训练，CV 虚高（1st/12th 独立采用加噪，方向一致）。
- **反事实 3**：若只有图像线 → LB ~0.15；只有表格线 ~0.18（9th 的 pipeline 与图像模型数字直接对比）→ **表格元数据是本场主信息源**，与 petfinder（图像为主、元数据为辅）恰好相反。
- **反事实 4**：若直接混入往届数据 → 先验被改（阳性率差 1–2 个数量级）+ 域差异 AUC 0.99 → 失败；若只做预训练 → +0.002。
- **边界**：整套结构依赖 3D-TBP 的丰富元数据（tbp_* 系列）。纯图像、无元数据的比赛不可套用"GBDT 元模型"骨架；solo vs 团队也有影响（2nd 为团队、9th 为 solo 金）。

## 8. 悬案与失败学

**悬案**

1. **未收录的 3rd/4th/7th/8th/13th 方案（正文缺口）**：其中 7th "A good CV is all you need"、8th "Trust your CV"、13th "God Bless CV" 三连标题与 1st"后期转向公榜、私榜变差"的自述构成同题张力；补读后可作为 T3 的强证据。
2. **Public 1st / Private 24th（532564，81 票）未收录**：公榜过拟合的极端案例，与 1st 的轻微版本同源；机制未明。
3. **LB probing（517139，130 票）未收录**：1st 明确用探针选 σ，但探针方法与合规边界未在已收录材料里展开。
4. 合成数据为何"个体更好、集成无用"：缺少误差相关性/失败区覆盖分析（本文 M7 为机制推演，非实证）。
5. 2nd 的图像模型 CV 0.1515–0.1612 与最终 GBDT 融合分数之间缺少消融表（哪些设置贡献最大未量化）。

**失败学（跨队合集）**

- 数据侧：往届数据混训（2nd/12th）；外部正样本混训致 train pAUC 虚高（515356 评论区）；伪标签（12th）；hard negative 采样/挖掘（1st/9th）。
- 训练侧：focal loss 劣于 BCE（9th）；scratch 训练（9th）；mixup 个体可用但进集成常拖后腿（9th）。
- 融合侧：**0.5 缩放/rank 集成、ExtraTrees/LR stacking（9th）；多增广平均预测（1st）**。
- 特征侧：聚类 z-score 无私榜增益（1st）；Dullrazor 去毛、发丝增广、lesion-id sample weight（9th）；FTTransformer 不如 GBDT（12th）。
- 工程侧：A.Resize 位置错误（9th，+0.006 LB）——**增广顺序是容易被忽视的高性价比检查项**。

## 9. 图表证据

> 路径相对本文件（`analysis/deep/`）：`../../intel/isic-2024-challenge/bodies/<topic>_img/NN.png`

![1st 的合成数据生成管线：SD1.5 → 6000 张 → 训练（topic 533196）](../../intel/isic-2024-challenge/bodies/533196_img/01.png)

**图 1：1st 的合成数据生成管线（SD1.5 → 6000 张 → 训练）**（topic 533196）

*读图结论*：在**正样本**上微调 Stable Diffusion 1.5（50 epoch、batch 8、128×128），取 40/45/50 三个 checkpoint，再以 2 分辨率（512/128）× 2 scheduler × 多 prompt 生成 **6000 张**合成图，用于训练图像模型；正文只写"生成合成数据"，图给出了完整配方与规模。

![真实恶性病变 vs Derm-T2IM 合成 vs 1st 自产合成（512/128）（topic 533196）](../../intel/isic-2024-challenge/bodies/533196_img/02.png)

**图 2：真实恶性病变 vs Derm-T2IM 合成 vs 1st 自产合成（512/128）**（topic 533196）

*读图结论*：Derm-T2IM 产物带明显伪影（培养皿/标尺风格）；1st 自产的 512 图常出现"多颗独立痣"（偏离单病变输入分布）；128 图较接近真实但模糊。**合成数据的分布缺陷肉眼可辨**——这解释了 M7 的"个体有效、集成无用"与"未采用"决定。

![合成 vs 基线个体的 CV/公榜/私榜对比（topic 533196）](../../intel/isic-2024-challenge/bodies/533196_img/03.png)

**图 3：合成 vs 基线个体的 CV/公榜/私榜对比**（topic 533196）

*读图结论*：synthetic 组全面优于 base：CV 0.1559→**0.161**、私榜 0.1318→**0.1346**、公榜 0.1498→**0.1508**。图证了"合成数据对单模型有正收益"，与正文"最终集成未采用"形成关键区分。

![12th 的 best LB 模型结构：GLCM + KNN + 加噪 OOF + 4 GBDT（topic 532642）](../../intel/isic-2024-challenge/bodies/532642_img/01.png)

**图 4：12th 的 best LB 模型结构（GLCM + KNN + 加噪 OOF + 4 GBDT）**（topic 532642）

*读图结论*：meta（表格）与 image 两条输入线；图像线 = 5 个图像模型 OOF → **加高斯噪声**；表格线 = 公共 notebook 特征 + GLCM + KNN(k=5)；concat 后进 4 个 GBDT（含 1 个不用图像特征）做正上采样/负下采样，**15 fold × 5 seed** 后 mean；公榜 0.183 / 私榜 0.171 / CV 0.1804——本场"标准骨架"的结构图。

![microscope 增广示例：正/负样本（topic 517141）](../../intel/isic-2024-challenge/bodies/517141_img/03.png)

**图 5：microscope 增广示例（正/负样本）**（topic 517141）

*读图结论*：给图像叠加圆形视场 + 黑色背景，模拟"显微镜/皮肤镜"拍摄风格；来自历届 ISIC 冠军配方。**这类"采集设备风格增强"是针对设备域差异（本场域分类器 AUC 0.99 的另一面）的低成本手段**。

## 10. 对既有笔记/playbook 的修订点

1. `notes/cv/isic-2024-challenge.md` 升级：补 6 篇作者/票数、四方案 × 12 维对照、数字账（0.1% 正样本、150/54/3 epoch、AUC 0.99、合成数据三层数字）与 5 张图证。
2. `playbook/cv.md`（图像+表格混合赛节）增补：
   - **标准骨架**：GBDT 主模型 + 图像 OOF 分数当特征；OOF 要 per-model 标准化/rank、加高斯噪声、患者隔离；
   - **患者内相对特征（ugly duckling）**：z-score / LOF / KNN 距离，医学筛查通用；
   - **采样强度 ↔ epoch 预算耦合**：正样本曝光量是统一参数；
   - **域差异量化**：训练域分类器（AUC>0.9 慎混数据）；预训练可、混训不可；
   - **合成数据两层评估**：单模型增益 ≠ 集成增益，看失败区覆盖与误差相关性。
3. `playbook/00-通用方法论.md` 增补：**"OOF 特征回路"**（早停乐观 → 加噪/独立划分）；**"公榜依赖的代价"**（1st 自述后期转向公榜 → 私榜变差；配对 t 检验 + leak-free CV 是小提升的唯一可信尺子）。
4. `analysis/THEORY.md`（Batch 4 收尾扩 v0.4）候选：
   - **L45｜OOF 预测当特征时必须去乐观**：证据 = isic 1st σ=0.1、12th 加噪；旁证 = 各场 stacking 的折外纪律。
   - **L46｜患者/实体内相对特征**：证据 = isic（LOF/KNN/患者标准化三队）；与 godaddy 的县规模分流互为"实体归一化"家族。
   - **T8 扩证**：外部数据"预训练 +0.002 私榜 + 域分类器 AUC 0.99 + 混训失败"三连；
   - **T4 扩证**：合成数据"个体全面更优（有图）/集成无增益"。

## 11. 出处

- 1st（149 票）：https://www.kaggle.com/competitions/isic-2024-challenge/discussion/533196
- 2nd（71 票）：https://www.kaggle.com/competitions/isic-2024-challenge/discussion/532704
- 9th（81 票）：https://www.kaggle.com/competitions/isic-2024-challenge/discussion/532577
- 12th（65 票）：https://www.kaggle.com/competitions/isic-2024-challenge/discussion/532642
- 数据帖（296 票）：https://www.kaggle.com/competitions/isic-2024-challenge/discussion/515356
- 增广帖（67 票）：https://www.kaggle.com/competitions/isic-2024-challenge/discussion/517141
- 缺口登记（未收录正文）：3rd(532919) / 4th(532760) / 7th(532687) / 8th(532728) / 11th(532595) / 13th(532654) / 54th(532644) / Benchmarking(527023) / LB probing(517139) / Public1st-Private24th(532564) 等
