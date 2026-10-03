# KStarter 失败学手册（Failures & Open Problems）

> 由 `scripts/build_failures.py` 扫描 264 篇深读生成（原始条目 1964 条，覆盖 264 场）；上半部分为人工归纳的十二大失败模式，下半部分按分类展开代表性条目；完整机器可读版见 `analysis/failures.csv`。
> 用法：开赛/复盘时把失败模式当检查清单；引用某条时回 `analysis/deep/<slug>.md` 与原文 topic 核对。

## 0. 分类统计

| 分类 | 条目数 |
| --- | --- |
| 数据/标签 | 635 |
| 其他 | 352 |
| 评审/材料 | 266 |
| 模型/训练 | 208 |
| 验证/CV | 202 |
| 平台/提交 | 187 |
| 特征/后处理 | 97 |
| 复现/规模 | 17 |

## 1. 十二大失败模式

### F1 验证口径与榜单不一致
- **机制**：CV 与 LB 的样本量/分布/泄漏方向不同，公开榜噪声或分布红利把选模带偏；小测试集上排名接近随机变量。
- **预防**：先量 CV/LB 样本量比与相关性；实体/时间泄漏先排除；LB 只验证绝对水平；保留 OOF 证据。
- **关联规律/张力**：L4/L6/L31/L116/T3/T31/T37
- **典型证据**：
  - `s3e9`：CV 5407 样本 vs 公榜 721 样本：测量 vs 随机变量；公开 notebook 无 CV 不抄
  - `s5e9`：榜首分带仅 26.38–26.41；未选用提交反而更高（609999）
  - `planttraits2024`：列顺序不一致导致 CV/LB 大幅偏离（487985）

### F2 实体/重复/泄漏
- **机制**：同一实体（玩家、马、酒店、图）跨 train/test 或重复出现，历史统计与目标形成泄漏；GroupKFold 分数更低但更真实。
- **预防**：先做实体键审计与重复检测；用 GroupKFold/时间切分；对重复行/近重复图登记处理规则。
- **关联规律/张力**：L2/L116/T31
- **典型证据**：
  - `scrabble-player-rating`：同一玩家历史整体落在 train 或 test；GroupKFold 分数显著变差（372554）
  - `s3e22`：同一 hospital_number 的马会死多次（441284/438825）
  - `herbarium-2022-fgvc9`：图像重复/数据泄漏报告（323906）

### F3 数据缺失、坏值与口径漂移
- **机制**：错误哨兵值（-666）、缺失编码不一致、test 端 OOD 类别、tracking 错位、语义口径不清，会让派生特征与结论同时失真。
- **预防**：逐列 train/test diff、哨兵值扫描、事件对齐与可视化抽检；先写口径表再建模。
- **关联规律/张力**：L19/L21/T7/T10
- **典型证据**：
  - `s3e18`：FpDensityMorgan1=-666；fr_COO/fr_COO2 出现 test 有 train 无的取值（419692/419651）
  - `nfl-big-data-bowl-2024`：位置滞后、缺失 tracking/ball_snap/passresult、plays 与 tracking 矛盾（448035/451985/452944）
  - `nfl-big-data-bowl-2025`：球轨迹不准、输入数据互相矛盾（551782/543709）

### F4 长尾与不平衡处理失效
- **机制**：长尾下重采样/加权并不总有效；测试同样长尾时「均衡化」反而伤 top-K 指标；类别层级错误与无图类别让训练目标本身失真。
- **预防**：先确认评测集分布；能归并的稀有类归并 unknown；用度量损失/多级监督替代盲目重采样。
- **关联规律/张力**：L130/L121
- **典型证据**：
  - `herbarium-2022-fgvc9`：class-aware sampling 与 data cleaning 均无效；靠 subcenter-ArcFace/多级 CE（329299）
  - `geolifeclef-2022`：长尾「什么都不做」最好；多标签聚合失败（328637/327055）
  - `fathomnet-out-of-sample-detection`：290 类中 157 类无图；<10 图类别归 unknown（398752/413092）

### F5 指标结构/评测实现误读
- **机制**：按指标名字猜测行为；未读官方 metric 实现（AUC 部分 bug、MAP@20 与评分代码不一致、逐列 AUC vs 堆叠 GINI），导致选模与提交策略错误。
- **预防**：下载官方 metric 实现做单元校验；把指标数学结构写成实验（中位数型/排序型/阈值型/容差型）。
- **关联规律/张力**：L30/L114/L52
- **典型证据**：
  - `fathomnet-out-of-sample-detection`：metric 的 AUC 部分有 bug，官方修复重算；MAP@20 与评分代码不一致（404769/410140）
  - `s3e18`：逐列 AUC 平均 vs 堆叠 GINI 口径不同（421149）
  - `s3e25`：MedAE 只取决于中位误差样本（455888）

### F6 无效的新增技巧与过拟合公榜
- **机制**：公开 notebook/热门技巧在无 CV 证明时复制；Optuna 参数不经种子检验；PCA/t-SNE/聚类在结构化特征上无效；集成在低信号目标上过拟合。
- **预防**：任何技巧必须过「同折 CV 对照」；Optuna 换种子复跑；低信号目标设预算上限。
- **关联规律/张力**：L41/L113/L125
- **典型证据**：
  - `s3e9`：Optuna 参数换 KFold 种子后不存活（394592）
  - `s3e23`：PCA/t-SNE/聚类均无提升（450315）
  - `s5e9`：伪标签/残差无 CV 对照；低信号场次集成收益不可证（610264/610016）

### F7 伪标签/外部数据/合成数据反噬
- **机制**：把检测器/教师输出当训练数据会误差传播；外部数据未做类别映射/对抗验证会引入分布错配；低质合成数据毒害训练。
- **预防**：外部数据先做映射与对抗验证；伪标签只在同折 CV 对照下启用；教师输出先过滤置信度。
- **关联规律/张力**：L17/L31/T6/T8/T21/T30
- **典型证据**：
  - `iwildcam2022`：用检测器结果训练会误差传播；1st 选择不训练只过滤（328965）
  - `hotel-id`：2nd 的 FGVC8 伪标签与 Hotel50K 均失败（328345）
  - `planttraits2024`：sample_submission 刷榜导致换测试集+重置 LB（486503）

### F8 提交/平台/预算工程事故
- **机制**：提交按钮失效、schema/zip 结构错误、PENDING、模型挂载方式、地区限制、API 预算/额度、TPU 排队——工程事故直接淘汰或压缩实验次数。
- **预防**：提前 48h 提交、本地 validate、保留截图凭证；赛前做成本模型与额度申领；准备自部署 fallback。
- **关联规律/张力**：L122/L123/T35
- **典型证据**：
  - `bigquery-ai-hackathon`：提交按钮失效/保存锁定多帖（608992/608986/609004）
  - `autonomous-agent-prediction-beta`：agent schema 校验失败、$2 预算、工具兼容问题（737407/723907/723806）
  - `gemini-long-context`：必须 Save&Run All 才挂载模型；当时全站仅 4 用户（541420）

### F9 评审/材料不可复核
- **机制**：获奖方案未归档、个人评分不公开、正文被压缩、0 图场次、站外图床不可达——大量结论只能停留在「自述/转引」层级。
- **预防**：把评审材料当二手证据，标注置信度；引用前回原文 topic；把缺口写进悬案而不是补造结论。
- **关联规律/张力**：L117/L118/T36
- **典型证据**：
  - `openai-gpt-oss-20b-red-teaming`：20 篇获奖 write-up 正文均未归档，仅官方评语（608537）
  - `med-gemma-impact-challenge`：落选者请求分项评分/rubric 未获承诺（685138）
  - `pokemon-tcg-strategy`：官方明确不公开个人评分与分项明细（742692）

### F10 RL/Agent 训练失败
- **机制**：RL 在复杂环境里常打不过规则/示例微调；自对弈同质化导致策略偏科；延迟奖励与思考死循环烧光预算；训练收益在 20–30M 步后枯竭。
- **预防**：先规则基线；RL 配课程+快模拟器+对手多样性；用 KL/产量/胜率曲线早停；agent 赛先过 schema。
- **关联规律/张力**：L124/L125/L126/L127/T32/T33
- **典型证据**：
  - `kore-2022-beta`：1st 规则七模块；社区 Q-learning 打不过官方示例微调（317737/317955）
  - `maze-crawler`：1st 评分函数 BFS；3rd JAX+BC+PPO 自述自对弈池同质→战斗弱（717120/718158）
  - `lux-ai-season-2-neurips-stage-2`：32×32 KL>0.02、金属产量跌破 100 后收益枯竭（459891）

### F11 时间/成本/复现边界
- **机制**：算力/显存/内存/时长限制、随机种子、私有数据、版本依赖与平台环境差异，使历史分数与方案不可完全复现。
- **预防**：记录版本与种子；优先低成本可复现基线；把不可复现部分显式声明；用提前量对冲排队与超时。
- **关联规律/张力**：L28/L21
- **典型证据**：
  - `sorghum-id-fgvc-9`：71GB PNG → 14GB JPEG；测试图缺失/API 拉取问题（313266/313438/313691）
  - `geolifeclef-2024`：Seafile 栅格下载脚本报错、GLC 模块不可用（481283）
  - `wikipedia-image-caption`：URL 图片下载/内存/TSV 读取问题（272204/287955）

### F12 社区与规则风险
- **机制**：抄袭/引用缺失、upvote 影响评分、外部数据合规、规则中途变更、late submission 被拒——社区与规则风险会造成不公平或直接判负。
- **预防**：注明来源并给增量；规则含社区分则提前发布维护；外部数据/影片合规先问；beta 规则变化用版本开关。
- **关联规律/张力**：L133/L118/T17
- **典型证据**：
  - `s3e25`：基线被大量复制且不注明来源（458154）
  - `kaggle-measuring-agi`：rubric 含 15% 社区投票引发 upvote farming 争议（683674）
  - `planttraits2024`：sample_submission 套利导致测试集更换与 LB 重置（486503）

## 2. 分类明细（每类代表性条目）

### 数据/标签（635 条，展示 24 条）

| slug | 条目 | topic |
| --- | --- | --- |
| `ai-mathematical-olympiad-prize` | 1st（Numina/AI-MO，519303） | 三件套：① **把 DeepSeekMath-Base-7B 微调成"推理 agent"**（语言 + Python REPL 混合求解）② **带代码执行反馈的 TIR 解码算法** ③ 多套内部验证集；训练配方基于 **MuMath-Code 两阶段**（图 … | 519303 |
| `byu-locating-bacterial-flagellar-motors-2025` | 1st（583143，146 票） | 3D U-Net（编码器 = 预训练 ResNet200/101，随机 dropout + 梯度检查点；解码器仅 1 个反卷积块）；**标签 = 高斯热图、分辨率降 8 倍**（"指标对距离宽容，预测像素精确不重要"）；损失 = SmoothBCE 三项（主头 + 倒数第二特征… | 583143 |
| `dfl-bundesliga-data-shootout` | 1st（Team Hydrogen，359932，139 票） | **单阶段 2.5D+3D 混合模型**：输入 1024×1024 **灰度图**（比彩色泛化更好且更快），通道堆叠 3 个相邻帧；对当前帧 t=15，分别喂 5 个时间步（每步 3 帧：{8,9,10}…{20,21,22}），共 **15 帧**… | 359932 |
| `google-universal-image-embedding` | 1st（359316） | 完整时间线：① **预训练权重**——ImageNet-22K 权重 0.405；CLIP ViT-L 在 **LAION-400M 31ep 上 0.499**（试遍可用权重）；发现"只取嵌入向量的一部分算均值"可 **+0.010**（"平均太多值会让真实特征被稀释"），随机投影对弱权… | 359316 |
| `image-matching-challenge-2023` | 2nd（416873，49 票） | 主题即"**战胜 COLMAP 的随机性**"；关键动作：① **穷举所有图像对**（放弃检索排序），匹配数 <100 的对丢弃；② SP/SG 无上限关键点（kpt 阈值 0.005、match 0.2、Sinkhorn 20 轮）+ 半精度 + 关键点/匹配缓存；③ TTA … | 416873 |
| `leash-BELKA` | 1st（519020，85 票） | 架构极简：**4 层、8 头、dim=32、词表 43 token**（作者自述 atomInSmiles 用得"不太对"，实际接近字符级）；不用 ChemBERTa 等预训练；**两阶段预训练**：① MLM（15% 遮蔽：80% mask/10% random/10% 保留，… | 519020 |
| `playground-series-s4e4` | 1st（499174） | OpenFE 生成 + Sequential Feature Selection（每模型约 20 个附加特征，例：`freq(Shell_weight)`、`Whole_weight/Shucked_weight`、`log(Whole_weight)`、`residual(Whole_w… | 499174 |
| `playground-series-s3e11` | 4th（399489） | 5 模型（LGBM×2、XGB×2、CatBoost×1）；CV 用"原数据只入训练、只在校验合成数据"（原数据标 fold=-1）；`log(cost)` + RMSE；**最重要 FE**：`store_score = coffee_bar+video_store+salad_bar+… | 399489 |
| `playground-series-s6e5` | 1st（703562） | 最后一分钟提交、**以 0.00001 取胜**；186 个 OOF（182 个 L1 + 4 个 L2）；200–400 特征的重型 FE + 大量模型族（XGB/LGBM/CatBoost/RealMLP/TabM/HGB/RF/YDF/FT-Transformer/MLP-PLR…）… | 703562 |
| `nfl-health-and-safety-helmet-assignment` | [284940](https://www.kaggle.com/competitions/nfl-health-and-safety-helmet-assignment/discussion/284940) 9th | — | 64 | YOLOv5x 修漏（+0.057）；**shape context** 初始帧… | 284940 |
| `mayo-clinic-strip-ai` | 1st（357892） | tiling 后取**最暗的 16 块**；swin_large_patch4_window12_384 + **attention pooling**（CV 0.69→0.66，五折均值）；**MoCo-v3 预训练使五折 CV 方差 0.30→0.15**；损失/指标严格按赛题实现；5… | 357892 |
| `stanford-ribonanza-rna-folding` | [460121](https://www.kaggle.com/competitions/stanford-ribonanza-rna-folding/discussion/460121) 1st | — | 147 | 12 层 Transformer；**BPP 注入 6 头注意力** + **Dynamic P… | 460121 |
| `open-problems-single-cell-perturbations` | [459258](https://www.kaggle.com/competitions/open-problems-single-cell-perturbations/discussion/459258) 1st | Jean Kouagou | 50 | BioWordVec 0.767 → ChemBERTa … | 459258 |
| `home-credit-credit-risk-model-stability` | [507946](https://www.kaggle.com/competitions/home-credit-credit-risk-model-stability/discussion/507946) 公开 8 / 私有 253 | Evgeniia Grigoreva | 60 | 日期恢复法：`refres… | 507946 |
| `playground-series-s5e11` | 2nd（647288） | Ridge 集成 7 模型（5×LGBM + TabM + RealMLP）；另有一份"最佳单 LGBM"同样拿到第 2；特征 = 基数 >7 的列全部 TE + CE + **用原数据目标做 TE**；高基数 `annual_income`/`loan_amount` 用**分位/均匀分… | 647288 |
| `mitsui-commodity-prediction-challenge` | 15th（668673） | 推理期在线学习：每积满 7 个新标签重训一组模型（新 fold）；CombinatorialPurgedGroupKFold（5 splits）；集成 attention DNN（1024→768→512→384→256→424）+ residual DNN + autoencoder（… | 668673 |
| `tabular-playground-series-apr-2022` | 3rd（322269） | VD Brothers 队：10 折 GroupKFold（按 subject）；**shapelets**（tslearn 的 Keras 实现移植到 torch，加入 lr 调度/早停/条件特征，在已有特征之后挖掘互补形状）；单模 公 0.98052 / 私 0.97706；stack… | 322269 |
| `stanford-rna-3d-folding` | 3rd（609701） | 集成 DRfold2 + Protenix + Boltz-1；自建 rMSA（官方代码，**14 天**）；Protenix 在 GH200 96GB 微调、限 <800nt、整数据 ~1 天；**无 rMSA 微调无效**；<400nt 用 DRfold2（只保留 energy sel… | 609701 |
| `tabular-playground-series-dec-2021` | [298304](https://www.kaggle.com/competitions/tabular-playground-series-dec-2021/discussion/298304) 2nd | SSS（sergiosaharovskiy） | 54 | 完整叙事：向原始数据靠拢的数十次失败（CV 好/… | 298304 |
| `deep-past-initiative-machine-translation` | [684329](https://www.kaggle.com/competitions/deep-past-initiative-machine-translation/discussion/684329) 8th | — | 25 | byt5-xl；**2 阶段 SFT**（~350k 噪声 3 epoch →… | 684329 |
| `hotel-id-to-combat-human-trafficking-2022-fgvc9` | 2nd（328345） | 50K+FGVC9；按 **md5 去重**（同 md5 不同类别删除）后保留 **45,769 个类别**；方向模型把图旋正；先全量 10–20 epoch，再对 FGVC9 的 **3116 类微调 40 epoch（+0.03）**；**sub-center ArcFace（k=3，… | 328345 |
| `cafa-6-protein-function-prediction` | 3rd（709281，0.44640） | 坦白"基本是复现 U900 队 CAFA5-2nd 的开源代码 + 小改动"；用 **ESM2-t33-650M + ProtT5** 末层均值嵌入（ESM-IF 无效）；**把 CAFA5+CAFA6 训练集合并（145,382 蛋白）**；实现细节：`create_he… | 709281 |
| `lux-ai-2021` | 6th（293776） | 全 IL，RL 多次尝试失败；7 个输出（unit：CENTER/NORTH move、build city、NORTH transfer；citytile：build unit/research/do nothing）；**唯一一次前向/turn**（"per-unit 方案会被时限压死… | 293776 |
| `playground-series-s4e3` | 2nd（488106） | 合成 + 原始数据合并、**剔除多标签行**（占比极小）；3 个自造特征（比值、min-max 归一化、乘积）+ **丢掉 7 个特征**；4 个多类模型（XGB/LGBM/CatBoost/HGBC）× 10 折 + Optuna；用同折 OOF 做 3 模型 Nelder-Mead 权… | 488106 |

### 其他（352 条，展示 24 条）

| slug | 条目 | topic |
| --- | --- | --- |
| `lux-ai-season-2-neurips-stage-2` | 行动掩码 | 大量无效动作屏蔽 + 冲突取消（移动/转移/拾取冲突迭代取消）；规则示例：剩余步数不足不浇地衣、工厂格不转出资源、只能挖资源/敌方地衣/工厂地衣区旁废墟、只能在全资源+可挖区+己方单位+敌地衣的矩形内移动、只有 light 能自毁且仅限不可一击清除的敌地衣 | 459891 | 459891 |
| `playground-series-s4e6` | "3rd place solution: a single xgb model"（515983，30 票）与"Outlier detection to boost the score"（511076，34 票）未入库/未细读； | 511076 |
| `home-credit-credit-risk-model-stability` | **指标公式原文未收录**：`475878`、`476449`、`476867`、`478716` 未采集；"线性趋势惩罚"的精确形式（对哪些周、什么系数、是否含标准差项）无法复算，hack 的作用通道只能从行为反推。 | 475878 |
| `feedback-prize-2021` | **图 4：beam search 修复非法 BIO（代码与反例）**（4th）——`../../intel/feedback-prize-2021/bodies/313330_img/02.png` | 313330 |
| `santa-2024` | **"Each Optimal(?) Score has been revealed!"**：社区是否真的证明了各 sample 最优？28.5 / 191.x 与最优的差距（556784）。 | 556784 |
| `waveform-inversion` | **4th/5th/6th 方案（587500/587443/587460）未收录**——季军之后如何组织"物理 + 学习"的混合（尤其 FWI 精修与纯 DL 之间的第三条路）。 | 587443 |
| `open-problems-single-cell-perturbations` | **PYBOOST 的算法细节（SketchBoost）** 只在 #13 中概述，专帖(454700)与论文未收录——多目标 boosting 的实现是本场最重要的方法论产出。 | 454700 |
| `santa-2024` | **"Metric Revision and Rescore" 细节未收录**：指标改了什么、分数怎么变、是否影响最终名次（547676，27 票，55 评论）。 | 547676 |
| `asl-signs` | 44th（406302）/PyTorch 实验（391265）未细读；"Lovely lips"（45 票）与 tf-lite 转换帖未入库。 | 391265 |
| `tabular-playground-series-dec-2021` | **"Yet another score booster"（293768，22 票）**：Gulshan 提到的另一处修复/增益未展开。 | 293768 |
| `birdclef-2022` | 7th 方案（326973）与指标解释帖未收录；"Previous Audio Competitions"（307824）未收录。 | 307824 |
| `pii-detection-removal-from-educational-data` | H2O Danube 1.8B 的 LLM NER 路线（481135，85 票）未收录——与 DeBERTa 路线的对照不完整。 | 481135 |
| `deep-past-initiative-machine-translation` | **"Two practical stumbling blocks"（665209，75 票）**：社区公认的实用避坑帖未收录。 | 665209 |
| `arc-prize-2025` | 614436 团队最终成绩、"Post comp update"（652927）与 615018（29.72 分帖）未细读； | 614436 |
| `optiver-trading-at-the-close` | `462639` NN with no FE（63 票，"5.34X"）与最终 5.40 的关系（是否公开榜虚高）未厘清。 | 462639 |
| `jane-street-real-time-market-data-forecasting` | CatBoost 在线（556544，60 票）与 LGBM 推理加速（542697，45 票）两条工程线未细读； | 542697 |
| `playground-series-s3e16` | 11th（416819） | "什么有效、什么无效"的复盘帖（与 1st 的曲折过程呼应） | 416819 | 416819 |
| `data-assistants-with-gemma` | "can i get rankers solution or code?"（495318）无答复； | 495318 |
| `stanford-ribonanza-rna-folding` | 0.141 天花板的成因（458478）与 2A3/DMS 误差关系（451158）未收录。 | 451158 |
| `nvidia-nemotron-model-reasoning-challenge` | bit 解法详解（690307，111 票）未收录；7th 的 arXiv 预印本未收录。 | 690307 |
| `tabular-playground-series-dec-2021` | **"不该用 accuracy"（293362，29 票）**：具体替代指标与论证未收录。 | 293362 |
| `g2net-detecting-continuous-gravitational-waves` | **"alt accounts"（375369，32 票）**：榜单账户治理问题未收录。 | 375369 |
| `vesuvius-challenge-surface-detection` | 4th/Bronze/placeholder 帖（含 651532 的图）未细读。 | 651532 |
| `home-credit-credit-risk-model-stability` | **官方是否赛后处置**：`508163` 未收录；违规判罚/榜单修正无记录。 | 508163 |

### 评审/材料（266 条，展示 24 条）

| slug | 条目 | topic |
| --- | --- | --- |
| `rsna-miccai-brain-tumor-radiogenomic-classification` | 2nd–11th 方案未收录；**Fake Accounts In Competition（269396，107 票）**的处置与 "The real winner…"（100 票）未入库——本场治理问题严重；MRI 拍摄方法差异（252843，99 票）也未细读。 | 252843 |
| `kore-2022` | 2nd（340994）/ 3rd（342296）/ 4th（340157）/ 5th（339979）/ 10th（340159）/ 15–20th（336826）/ 60th（340115）等 write-up 未收录正文，只能从标题判定路线； | 336826 |
| `feedback-prize-effectiveness` | 4th–10th 方案未收录；`338271` Token Classification Approach（88 票）、`333277` 单模实验日志 0.624（90 票）、`332438` DeBERTa 综述（91 票）未收录。 | 332438 |
| `uw-madison-gi-tract-image-segmentation` | "2.5D Image Training"（322549,124）与 "MMsegmentation 模板"（323921,104）未收录：1st 的重要参考源（CarnoZhao/awsaf49 的公共资产）正文未存档。 | 322549 |
| `5-day-ai-agents-intensive-vibecoding-course-with-google` | **Unit 4（Day 4）与 Capstone 正文未收录**（主题索引有 Day4 709165、Capstone 709721、Wrap-up 609?）；本轻读缺 1/5 课程内容。 | 709165 |
| `santa-2024` | **L97｜黑箱评分器对齐律**（先精确复现+批量化+固定精度，再谈搜索；反例=批量与逐行 cuBLAS 差异污染爬山；证据 = 548249 + 本场全社区）； | 548249 |
| `data-assistants-with-gemma` | **最终获奖名单未归档**：索引有"Competition Prize Announcements"（499090，24 票 / 20 评论），正文未收录； | 499090 |
| `jpx-tokyo-stock-exchange-prediction` | 1st–3rd/5th–7th 的方案未入库；"猜测冠军方案"（173 票）与"往届 JQuants 冠军"（317250）未细读； | 317250 |
| `pokemon-tcg-ai-battle` | **榜单评分不一致（712621，79 票）**：症状、原因、官方处置均未收录——直接影响"评估系统能否信任"的结论强度。 | 712621 |
| `hull-tactical-market-prediction` | 归档 11 图全部来自 EDA 帖（610981），4th 的方法图（output/vol_scaling）未归档； | 610981 |
| `santa-2024` | 社区：批量评分未对齐导致分数错误（548249 之前的大量困惑）；cuBLAS 差异（GPUs 非确定性的经典坑）。 | 548249 |
| `linking-writing-processes-to-writing-quality` | **取消资格的原因**未在任何收录正文中说明（仅 467154 标题），官方 recap（468441）未收录。 | 467154 |
| `smartphone-decimeter-2022` | 2nd/4th 方案未收录；"How to Approach"（65 票）与上届冠军（322510）未细读。 | 322510 |
| `stanford-rna-3d-folding-2` | 归档仅 1 图（RNAPro 管线图，topic 668412），其余队伍的方法图未归档——图证缺口已登记。 | 668412 |
| `openai-gpt-oss-20b-red-teaming` | 20 篇获奖 write-up 正文均未归档，无法独立复核技法与数字；本场结论以官方 608537 为准； | 608537 |
| `data-assistants-with-gemma` | 评审 rubric、评委名单（社区问"Who are the judges?" 478869）未归档； | 478869 |
| `llm-prompting-with-makersuite` | 2 张归档图中 1 张为梗图（451608_img/01.jpg），无分析价值，未内嵌； | 451608 |
| `nfl-big-data-bowl-2022` | 2022 获奖作品正文与 judging 细节未归档（307969 只有标题级信息）； | 307969 |
| `pokemon-tcg-ai-battle-challenge-strategy` | 迟报名/资格争议的最终处理结果未归档（735276 / 740873 等无后续）； | 735276 |
| `playground-series-s4e6` | 归档 5 图：1 张决策树（509073）+ 4 张置信度散点（512220）。 | 509073 |
| `kore-2022` | "理解动作空间"（319857）与"高效最优路径"（336804）正文未细读； | 319857 |
| `nfl-player-contact-detection` | 往届 NFL 索引（370685）与 4th 的可视化（391719）未细读。 | 370685 |
| `novozymes-enzyme-stability-prediction` | 归档 11 图：GNN 架构图（图 1）与 376116 的分数截图为图证。 | 376116 |
| `google-gemma-3n-hackathon` | 获奖作品名单与评审标准（657756）未细读；获胜项目技术细节未归档； | 657756 |

### 模型/训练（208 条，展示 24 条）

| slug | 条目 | topic |
| --- | --- | --- |
| `rsna-intracranial-aneurysm-detection` | 1st（611846） | 三段式 coarse-to-fine：① **nnU-Net 粗定位**（1mm 间距、3 组血管区、Dice+CE）扫全图 → DBSCAN 去散点 → 以最大簇中心裁 140³ mm ROI；② 两个 nnU-Net 细分割（0.80×0.45×0.44mm，**Dice+CE+Ske… | 611846 |
| `lux-ai-season-2-neurips-stage-2` | Lux AI S2 的 NeurIPS 精英阶段（**仅 64 队**）：在 16×16/32×32/64×64 地图上训练 1v1 资源采集+工厂建造 agent。归档里唯一的技术正文（459891）给出了完整的工业级 RL 配方：**fork Jux 支持非 lockstep 向量化环境 → 16→32→64 地… | 459891 |
| `santa-2024` | [560597](https://www.kaggle.com/competitions/santa-2024/discussion/560597) 5th（CPMP 部分） | CPMP | 43 | SA 变体（全局上界接受）；multi-point 并行（N=最大 batch，A100 上 104）；k-opt… | 560597 |
| `rsna-2022-cervical-spine-fracture-detection` | [362643](https://www.kaggle.com/competitions/rsna-2022-cervical-spine-fracture-detection/discussion/362643) 3rd | darraghdog | 59 | **不用骨折 bbox**；只用分割的外接框 + 体积… | 362643 |
| `deep-past-initiative-machine-translation` | [684231](https://www.kaggle.com/competitions/deep-past-initiative-machine-translation/discussion/684231) 6th | — | 54 | 15 模型集成；PDF 三分类（image/text/**broken_tex… | 684231 |
| `ai-village-ctf` | [351804](https://www.kaggle.com/competitions/ai-village-ctf/discussion/351804) 21 解法摘要 | Vasilis Konstantakos | 11 | 逐题方法学：math=DBSCAN/PCA、hotdog=贴图、hotterdog=… | 351804 |
| `pokemon-tcg-ai-battle-challenge-strategy` | 高分特征（官方总结） | ① 用自建评测（self-play arena、对冻结对手的联赛、固定对手评测集）驱动迭代，并说清"分析后改了什么"② 展示组件贡献（通用 vs 专用策略、有/无搜索、两副牌对比、rating/胜率随时间）③ 讨论失败的尝试（端到端组牌、联赛训练、value-based MCTS、look-… | 742692 |
| `commonlit-evaluate-student-summaries` | [446686](https://www.kaggle.com/competitions/commonlit-evaluate-student-summaries/discussion/446686) 3rd | — | 43 | 简单管线 + EMA（必需）+ 差分 LR；CLS+答案 meanpool 拼接；**… | 446686 |
| `rsna-2024-lumbar-spine-degenerative-classification` | [540091](https://www.kaggle.com/competitions/rsna-2024-lumbar-spine-degenerative-classification/discussion/540091) 1st | 评论区署名 NANACHI | 105 | 3 类模型 2 阶段：insta… | 540091 |
| `lmsys-chatbot-arena` | [527669](https://www.kaggle.com/competitions/lmsys-chatbot-arena/discussion/527669)（5th） | Team Danube（Psi、dott1718、ilu000） | 59 | **无 PL、无蒸馏**的反例路线：UltraFeedb… | 527669 |
| `planttraits2024` | 9th（DINOv2+CatBoost） | DINOv2 [giant] embedding + 表格 → **CatBoost 原生处理 embedding**（含降维）；public **0.51162** / private **0.51238**；2 阶多项式特征小增益；**不同 embedding 的模型… | 510188 |
| `rsna-2024-lumbar-spine-degenerative-classification` | **7th "Single Stage Model Wins!"（539439，35 票）与前三名"one-stage 失败"冲突**——正文未收录（不扩采约束），无法裁决：是单阶段配合了更强的内部定位头？还是两阶段蒸馏成单阶段？登记为后续选择性补读候选（同时登记 T13 候选张力）。 | 539439 |
| `arc-prize-2024` | 21st（550209） | 一个小而妙的技巧：**先做颜色重映射（按各 pair 的输入/输出颜色频率排序后映射）**再喂给 icecuber 求解器 → 在集成里比 26% 基线 **+2%**；作者自述"1% 的精力，其余都是失败" | 550209 | 550209 |
| `tabular-playground-series-aug-2022` | 公开榜过拟合陷阱（41 票 / 24 评论）：https://www.kaggle.com/competitions/tabular-playground-series-aug-2022/discussion/348767 | 348767 |
| `stanford-rna-3d-folding` | 决赛 4th/5th/6th/7th/9th/10th 方案（609775 / 609713 / 610261 / 609921 / 609515）与"10th 如何集成"未细读； | 609515 |
| `rsna-2022-cervical-spine-fracture-detection` | metric weights 帖（340392，65 票）未收录：加权列 log-loss 的权重细节直接影响所有校准决策（3rd/5th 的损失设计）。 | 340392 |
| `cmi-detect-behavior-with-sensor-data` | agent 单模型直接上 | 583863 | 单 o3 模型 0.70；多模型规划（分工/评估）才到 0.82 | 583863 |
| `playground-series-s3e22` | 获奖模型"发布"链接指向他人 notebook，发布状态存疑（444892）； | 444892 |
| `kore-2022` | RL 侧仅有入门/工具帖（如 327460），无高质量 RL 方案可评估； | 327460 |
| `kore-2022-beta` | RL 失败的社区反思 | 个人帖（317955） | 中 | 317955 |
| `predict-energy-behavior-of-prosumers` | 1st 用 600 特征并称可裁到 100–200；3rd 90/77；5th 75/85；10th 76；12th 350/200；13th 裁到 top 300/400。粒度上：1st 再按 is_business 拆分失败（"split into more models given is_business eq… |  |
| `iwildcam2022-fgvc9` | 从相机陷阱**序列**里数动物（MAE 越低越好），官方提供 **MegaDetector V4** 检测与 **DeepMAC** 实例掩码，但没有训练所需的 GT 计数。1st 的答案出人意料地"反工程"：**不训练、不跟踪，只做检测过滤 + 每序列取最大计数**——按物体密度分两类图片分别调阈值/NMS，把 p… |  |
| `feedback-prize-2021` | **M5｜BIO 的转移约束必须显式建模**：greedy 逐 token argmax 会产出 I-Dog→I-Dog 这类非法序列（同置信度下 B-Cat→I-Cat 才是合法且更可能）；beam search（beam=4）+ 合法转移掩码，或结构化损失/CRF，都是同一机制的实现。4th 的图给出了最直观的反… |  |
| `home-credit-credit-risk-model-stability` | **M3｜为什么干净模型锁死在 0.53**：8th 指出测试期 Gini 的"下行斜率"来自市场条件（补助退坡、2022 冲击、CARES Act 报告扭曲）而非模型退化——这是随机趋势，不可预测也不可外推；指标却对这一斜率施加惩罚。于是任何诚实模型都要被扣掉一个与模型无关的常数 → 天花板固定。**推论**：这类… |  |

### 验证/CV（202 条，展示 24 条）

| slug | 条目 | topic |
| --- | --- | --- |
| `rogii-wellbore-geology-prediction` | **材料缺口（未扩采，登记备查）**：主题索引另有约 25 条 write-up 未收录，含 [4th（733480）](https://www.kaggle.com/competitions/rogii-wellbore-geology-prediction/discussion/733480)、[5th（7335… | 733150 |
| `recodai-luc-scientific-image-forgery-detection` | 2nd（694397） | 纯经典路线（无深度匹配）：YOLOv8-m 面板（3 类）与文本检测（~800 手标 + ~2000 合成，5 模型 WBF）；SIFT `contrast_threshold=0.001`（默认的 1/40）、<1024px 先 4× 放大；**G2NN（α=0.7）+ FLANN KD… | 694397 |
| `neurips-2023-machine-unlearning` | 6th（458740） | 选择性参数重置（**第一层 conv1 + 最后一层 fc**）+ 验证集 KL 蒸馏预热 + 微调（硬 CE + 软 CE + KL）；两版提交：全类预热 公 0.08383 / 私 **0.07219**；仅前两类（forget 集只含 0/1 类）预热 公 0.08324 / 私 *… | 458740 |
| `tabular-playground-series-jul-2022` | 1st（341023） | 只有 **14 个变量**与聚类相关；整数变量来自某种**混合泊松**（自建模型失败 → 与全场一样 power transform）；用 `GaussianMixture(n_components=42)` 跑浮点列即可发现结构；真结构 = **7 组 × 每 6 个子簇 = 42**；… | 341023 |
| `commonlit-evaluate-student-summaries` | [446573](https://www.kaggle.com/competitions/commonlit-evaluate-student-summaries/discussion/446573) 2nd | — | 142 | **Head Mask**（mean pooling 仅答案 tokens）；pro… | 446573 |
| `tabular-playground-series-mar-2022` | 1st（316271） | **单 LGBM、无后处理**（时间不够）；特征：似然编码（用 hour-minute × 地点交叉的最小/最大/中位/方差/均值）+ 滞后特征（对每个 x-y 方向组合在 day/weekday 上取均值/方差/中位/最小/最大与 1 区间位移，3/5/10 天滚动 + 扩展窗口）；**… | 316271 |
| `predict-energy-behavior-of-prosumers` | [472754](https://www.kaggle.com/competitions/predict-energy-behavior-of-prosumers/discussion/472754) 公开 3rd | Rafi Hai | 48 | LGBM l1、10k 迭代；**重训节奏消费 7 天/生产 4 … | 472754 |
| `autonomous-agent-prediction-beta` | 社区技巧/坑 | LB 0.823 模板（利用 "freeroll" fallback 规则 + Gemini Pro，2 票）；`select_submission` 实测收益上限 +0.0005、最差 −0.0166（0 票 / 5 评论）；本地评测 `run_local_eval.py`；Qwen 托管模型在 … | 724397 |
| `stanford-ribonanza-rna-folding` | [460316](https://www.kaggle.com/competitions/stanford-ribonanza-rna-folding/discussion/460316) 2nd | — | 42 | Squeezeformer + GRU head；BPP 2DConvNet 做注意力偏置（**−… | 460316 |
| `playground-series-s3e15` | 1st（414048） | 多样集成（树/神经网络/线性/KNN，即使单模更弱）；领域知识插补 + **按 author 的取值范围裁剪降噪**；author/geometry 类别编码；迭代树插补；10 折 CV 集成 RMSE **0.07265 ± 0.00202**（单模最好 0.0730）；失败：目标裁剪、… | 414048 |
| `stanford-rna-3d-folding` | 1st（609774） | 无 GPU；TBM 五步（检索 → 全局比对 → 坐标迁移 → 缺口几何重建 → 置信度自适应精化）；DRfold2 增强 = float64 打分、`torch.cdist` 向量化、预计算样条系数、PyTorch LBFGS、GPU 加速、Boltz-1 集成；DRfold2 失败自动… | 609774 |
| `konwinski-prize` | **图 1**（topic 568884，1st）：全流程时间线——相关单测/类函数/imports 三路上下文 → 生成 5 个 F2P 测试（3 个无上下文 + 2 个带上下文）→ 复现失败则 SKIP → 定位文件/类函数/细粒度编辑点（×2）→ 8 个修复补丁（每编辑点 4 个）→ F2P/P2P 验证 → … | 568884 |
| `playground-series-s4e6` | ravi20076（509665，32 票） | 24 小时赛的一天分成 4 段实验 + 1 次留底；baseline 0.83758（8 小时，公榜第 2）→ 调参无公榜变化（14 小时）→ 融合公开 kernel 得 0.83924（21 小时，第 8）→ 继续 blending 无提升 | 509665 | 509665 |
| `google-code-golf-2025` | **图 1**（topic 614124）：单会话多轮循环——每轮 Prompt → **4 份并行生成**（红=无效、绿=有效）→ 取最短有效码（55B/72B/91B/71B 中选 71B）→ **基于 AST 的规则化跟进提示** → 下一轮；展示了"并行采样 + 机械验证 + 最短选择"的完整闭环。 | 614124 |
| `lux-ai-2022-beta` | > 材料基础：`digests/lux-ai-2022-beta.md`（6 篇正文：资源与机制 363366 / 计划改动 365579 / Lux Eye 367091 / 官方欢迎 362825 / 活跃提交限制 363479 / 验证对局失败 363556；39 条主题索引）+ 0 张归档图 | 362825 |
| `isic-2024-challenge` | 反对方：2nd 直方图匹配后仍无提升，训练域分类器区分 ISIC2018 vs 2024 轻松达到 **AUC 0.99** → 放弃；12th 明确"use of past data"失败；515356 评论区也报告"用外部正样本混训导致 train pAUC 虚高、验证不涨"。 | 515356 |
| `playground-series-s4e2` | 24th（480927） | XGB（MEstimate 编码）+ LGBM（one-hot）集成；10 折分层；主要增益来自权重微调；明确"不加特征（BMI 等无效）"；"Trust CV over LB" + MLflow 记录 | 480927 | 480927 |
| `um-game-playing-strength-of-mcts-variants` | "Best Single Model CV LB thread"（532617，68 票）与"Generating Additional Training Data Offline"（533088，59 票）两条高票线未细读； | 532617 |
| `stanford-ribonanza-rna-folding` | **"How to check if your model generalizes to long sequences"（444653，60 票）未收录**——本场最重要的验证方法论帖之一。 | 444653 |
| `uw-madison-gi-tract-image-segmentation` | **"LB could be wrong"（324934,47）+ "Hausdorff usage"（319215,40）未收录**：新指标实现与榜单行为争议——影响所有队伍的选模决策。 | 319215 |
| `playground-series-s6e2` | **图 3**（topic 679389）：前 300 名的公榜排名 vs 私榜排名，大量点远低于对角线（公榜高私榜低）。**"盲 blend 陷阱"的直接证据**；色标为名次变化。 | 679389 |
| `hubmap-organ-segmentation` | **1st place（356201，48 票）的方案未入库**（本场材料缺口最大的一处）；"Some Insights"（89 票）与"Let's share CV"类帖未细读； | 356201 |
| `lux-ai-2022-beta` | 验证对局失败（12 票 / 6 评论）：https://www.kaggle.com/competitions/lux-ai-2022-beta/discussion/363556 | 363556 |
| `google-research-identify-contrails-reduce-global-warming` | "Single Model CV-LB Thread"（413153，47 票）、"One month to go 总结"（420629，110 票）两条高票线未细读； | 413153 |

### 平台/提交（187 条，展示 24 条）

| slug | 条目 | topic |
| --- | --- | --- |
| `rsna-2022-cervical-spine-fracture-detection` | **材料缺口（受"不扩采"约束，登记备查）**：2nd(365115,41 票,"Segmentation + 2.5D CNN + GRU Attention")、4th(364837,34 票,"CSN is all you need for 3D")、8th(362669,45)、32nd(362593,43)… | 340392 |
| `rsna-2022-cervical-spine-fracture-detection` | [362607](https://www.kaggle.com/competitions/rsna-2022-cervical-spine-fracture-detection/discussion/362607) 1st | haqishen | 222 | 128³ 3D 分割（r18d/effv2s+UNet，… | 362607 |
| `autonomous-agent-prediction-beta` | 官方失败清单（9 票 / 11 评论） | ① 多工具只支持全是 search 工具（gemini-2.5-* 仅单工具；deepseek-r1-0528 不支持工具）② skill 名必须 lowercase kebab-case ③ agent 没交有效预测（思考死循环烧 token、脚本吃满 session、直… | 723907 |
| `lmsys-chatbot-arena` | [527596](https://www.kaggle.com/competitions/lmsys-chatbot-arena/discussion/527596)（16th） | Chris Deotte | 205 | **系统化 LoRA/QLoRA 调参配方**：alpha 决定 backbone LR（=… | 527596 |
| `rsna-2024-lumbar-spine-degenerative-classification` | **材料缺口（受"不扩采"约束，登记备查）**：5th(539472,35 票)、7th(539439,35 票)、8th(539548,32 票)、14th(539459,31 票)、9th(539690,29 票)、Summary(541279,29 票)、7th(539486,27 票) 共 7 条方案帖未收录… | 539439 |
| `home-credit-credit-risk-model-stability` | **M7｜竞赛治理失败的时间线闭环**：2 月最早揭发（130 票）→ 官方公告修改（83/34）→ 3 月暂停/重启（96 票）→ 4 月 hack 复活并合法化（73 票）→ 榜单被 hack 分数淹没（505574/504467/505664）→ 收尾官方声明（34 票）。**推论**：当平台无法在规则层面消除… | 504467 |
| `open-problems-multimodal` | [366313](https://www.kaggle.com/competitions/open-problems-multimodal/discussion/366313) Massive and organized cheating | — | 147 | 有组织作弊：小红书"保银牌"广告（失败不收钱、铜牌免费… | 366313 |
| `ai-agent-security-multi-step-tool-attacks` | [738981](https://www.kaggle.com/competitions/ai-agent-security-multi-step-tool-attacks/discussion/738981)（7th，22 票） | Civitasmass | 22 | **迁移陷阱的完整记录**：123.730→… | 738981 |
| `autonomous-agent-prediction-beta` | > 材料基础：`digests/autonomous-agent-prediction-beta.md`（6 篇正文：起步与 Discord 723664 / 提交失败原因 723907 / 3rd 方案 737407 / 月度系列询问 723810 / 反馈征集 732744 / $2 预算 723806；30 条… | 723664 |
| `orbit-wars` | 7 | [713126](https://www.kaggle.com/competitions/orbit-wars/discussion/713126) | Nebraskinator | 40 | **Evoformer 迁移**：节点/边双流、边打分全发送、联合动作概率；SBR 搜索尝试失败 | 713126 |
| `ai-village-ctf` | **图 1：HOTTERDOG 求助帖的配图**（topic 344336，52 票）——把狗夹进热狗面包、画上芥末酱的图配上"为什么这都不行 :)"; 评论区给出真实方法论："从简单实验开始，证伪假设"。**一图代表本场的"直觉对抗"失败学与社区幽默**。 | 344336 |
| `konwinski-prize` | 8th（590920） | 基于 @huikang starter；关键词过滤（如含 "error" 的补丁）边际收益小；找到一组**权重配置**——失败很多但"成功时正确/错误比极高"——把提交集中在该配置上，两份提交都拿到金牌 | 590920 | 590920 |
| `lux-ai-2022-beta` | 计划改动（breaking） | 动作队列在能量不足时"等待"而非失败；地图改非对称；**竞标 (desired_placement, amount)** 决定放置顺序；交替放置；工厂可放任意位置但彼此有最小距离；双方工厂数相同 | 365579 | 365579 |
| `med-gemma-impact-challenge` | 提交物流事故 | 多帖：提交被拒/显示成功却错过、视频格式导致失败、晚 1 分钟关闭、多人请求迟到窗口、技术问题无法提交 | 678799 / 678798 / 678801 / 678790 / 678794 / 678915 / 678792 | 678790 |
| `tabular-playground-series-sep-2022` | SMAPE 的陷阱（30 票 / 4 评论）：https://www.kaggle.com/competitions/tabular-playground-series-sep-2022/discussion/349553 | 349553 |
| `autonomous-agent-prediction-beta` | 官方失败原因清单（9 票 / 11 评论）：https://www.kaggle.com/competitions/autonomous-agent-prediction-beta/discussion/723907 | 723907 |
| `neurips-2023-machine-unlearning` | 提交评分失败（14 票 / 12 评论）：https://www.kaggle.com/competitions/neurips-2023-machine-unlearning/discussion/442093 | 442093 |
| `ai-mathematical-olympiad-progress-prize-3` | 最难题目 | ACUTES 被唯一一名选手在两次评测中都解出（总成绩 43.5，$30k 最难奖）；ROLLER 两次评测无人解出；官方称 pass@N 高至 N=4000 仍可能失败 | 708484 | 708484 |
| `google-gemma-3n-hackathon` | 20 票的 Unsloth 微调帖（587725）与官方 audio/vision 微调 notebook（593950）正文未收录，微调路线效果无法评估； | 587725 |
| `llm-prompting-with-makersuite` | 447146 "Kaggle solution write-up" 是复制 sample_submission 的玩笑帖，不构成方案证据； | 447146 |
| `lux-ai-season-2-neurips-stage-2` | 规模与赛制 | **64 队**；Stage 2（精英阶段）；因 episode 失败延期到周一 | 索引 / 456054 | 456054 |
| `sorghum-id-fgvc-9` | 1st 的完整代码未在正文给出（仅 Kaggle notebook 路径）；"求 top1% 代码"（328477）无答复； | 328477 |
| `foursquare-location-matching` | 抄袭帖（319620，59 票）未收录——本场也发生过 notebook 抄袭争议。 | 319620 |
| `geolifeclef-2022-lifeclef-2022-fgvc9` | 2nd 的 +2%/+2% 消融与失败清单 | 亚军自述（328637） | 中高 | 328637 |

### 特征/后处理（97 条，展示 24 条）

| slug | 条目 | topic |
| --- | --- | --- |
| `deep-past-initiative-machine-translation` | [684345](https://www.kaggle.com/competitions/deep-past-initiative-machine-translation/discussion/684345) 2nd | wukeneth | 42 | vanilla byt5-large；三段 LLM 流水线（Br… | 684345 |
| `uw-madison-gi-tract-image-segmentation` | [337468](https://www.kaggle.com/competitions/uw-madison-gi-tract-image-segmentation/discussion/337468) 3rd | — | 45 | 检测器裁剪（EffDet-D0，256）→ CLS+SEG 双分支 UNet（35… | 337468 |
| `feedback-prize-2021` | [313424](https://www.kaggle.com/competitions/feedback-prize-2021/discussion/313424)（6th） | tascj | 165 | **YOLO 式跨度检测器**：objectness + 2 回归 + 分类；RoIAlign 聚到词级；N… | 313424 |
| `kaggle-measuring-agi` | > 材料基础：`digests/kaggle-measuring-agi.md`（6 篇正文：获奖公布 724918 / 收官 692562 / 投票权重争议 683674 / 提交失败 692560 / 校准 benchmark 683724 / 结果延期 716405；80 条主题索引）+ 1 张归档图 | 683674 |
| `playground-series-s3e23` | 无效尝试 | PCA（10 主成分解释 >99% 方差但掉分）、t-SNE 可视化、聚类 + cluster 目标编码——均无提升 | 450315 | 450315 |
| `learning-agency-lab-automated-essay-scoring-2` | QWK 阈值是否存在可迁移的理论最优值（尾部稀疏）——社区帖（502279）未收录。 | 502279 |
| `fathomnet-out-of-sample-detection` | OSD 的官方定义与最优阈值策略无归档说明（411135 在问）； | 411135 |
| `orbit-wars` | *读图结论*：左=每体 (20,10) 时间序列过 4×残差块（Conv1D k=5 d=128→GELU→残差→LayerNorm）+ GAP + 128→256 投影；右=ModernBERT XXS（7 层 4 头 d256，仅全局注意力）→ 每体 launch head 与 target head（对其它体的… |  |
| `open-problems-single-cell-perturbations` | 输入特征 | SMILES embedding / 目标编码（Quantile80 最优）/ Morgan 指纹与描述符基准（最终未用）；纯 ML 编码优于生物先验 | ChemBERTa(SMILES) + one-hot + 每 cell/drug 的 mean/std/分位数统计；Wikipedia 描述失败 … |  |
| `cmi-detect-behavior-with-sensor-data` | **M5｜为什么推理顺序会制造方差**：受试者第 N 条序列的可用历史取决于随机到达顺序；早期序列没有上下文（4th 用"置零历史类概率再按手势求和"退化处理），后处理质量随顺序波动 → 重提交分数抖动（0.868–0.880）。**在"流式评测 + 跨样本约束"的赛制里，方差是结构性的，选择提交本身是决策问题**（… |  |
| `rsna-2024-lumbar-spine-degenerative-classification` | **M2｜为什么关键点/坐标归一化优于 slot 分类**：层面数量与间距因人而异（脊柱曲度/身高），"把切片分到 5 个槽位"隐含固定间距假设。关键点把个体解剖差异显式参数化，随后按"相邻关键点距离×2"裁剪（4th）或按关键点均值距离定尺度（1st/2nd），把尺度差异从分类器输入中消除——误差从"系统性几何偏差… |  |
| `eedi-mining-misconceptions-in-mathematics` | 失败清单 | hard mining/cross-device negatives/自定义 batch/双向编码器/LoRA merge/QwQ | 自训 retriever 反而降分 | 多种选项编码/QwQ/multi-step rerank/prompt 加参考 | concat/平均向量、full-data … |  |
| `h-and-m-personalized-fashion-recommendations` | `notes/tabular/h-and-m-personalized-fashion-recommendations.md` 升级：补齐 8 节作者/票数；方案谱系扩为 6 方案对照矩阵；新增召回特征（策略×排名）、BPR、窗口×候选网格、负采样/K 甜区、51st/52nd 极简基线、图证与失败学。 |  |
| `stable-diffusion-image-to-prompts` | 给一张 Stable Diffusion 生成的图，预测它对应的提示词——但由于指标只比较**句子嵌入的余弦相似度**，任务实际退化成"**预测句向量**"（预测文本的语法/顺序几乎不重要）。真正的考点是**自造大规模"提示词-图像"对 + 加速生成 + 用多 backbone 回归句向量**。 |  |
| `rsna-2024-lumbar-spine-degenerative-classification` | **裁决**：多部位医学影像的第一性结构是"先解决在哪，再解决多严重"；端到端会让"层面身份"与"病灶程度"在特征空间中纠缠。置信度：高（4 队一致 + 1st/3rd 明确把一阶段列入失败清单）。**保留张力**：7th 标题宣称单阶段可行（未收录正文，T13 候选）。 |  |
| `march-machine-learning-mania-2023` | 1st 直接用通用基线；2nd 押"分区效应"这一体育统计学的结构量；5th 押"每回合效率"这套规范化特征。**裁决**：在基线极强时，领域增量必须针对基线的**具体盲区**（2nd 的 South Dakota State 案例）；泛泛加特征无效。置信度：中高。 |  |
| `tabular-playground-series-dec-2021` | 物理审计 | Aspect 修复（幸存）；额外裁剪/土壤掩码失败 | **Aspect ±360 + 三 Hillshade 截断**（0.95631→0.95673） | 负距离→0（+0.0053）；Aspect 离散化+Top10 线性特征（999/1200） |  |
| `child-mind-institute-problematic-internet-use` | `notes/tabular/child-mind-institute-problematic-internet-use.md` 升级：补齐 8 节作者/票数；方案谱系扩为 7 方案对照矩阵；新增插补消融、阈值优化三姿势、种子扫掠、QWK 目标陷阱、图证与失败学。 |  |
| `playground-series-s5e12` | 概念漂移下删特征 | 删"有毒"特征更安全（2nd 的 lgb_safe 假设） | 保留 + 加权/重建 | **反例成立**：lgb_safe 仅 0.67464，远低于 baseline 0.70435——直接删特征伤信号；置信度高（同表内对照） |  |
| `playground-series-s3e23` | PCA（10 成分 >99% 方差）掉分，t-SNE 无可分性，聚类 + target encoding 无提升。**裁决**：特征已是高相关代码度量的衍生集合时，优先"保留 + 变换"而不是降维；PCA 更适合压缩算力而非提分。置信度：中。 |  |
| `map-charting-student-math-misunderstandings` | **题目固定是前提**：15 题、每题误解集合预先确定 —— 一旦测试出现新题/新误解集合，"每题候选集"策略退化；98 票帖子专门讨论这一点（若测试同 15 题，可硬编码正确答案）。本场是"结构性先验"给的红利。 |  |
| `rsna-2022-cervical-spine-fracture-detection` | 失败清单 | 椎骨 cube 上的 3D CNN | Transformer、undersampling、骨折 bbox（弃用） | —（速通无消融） | mask 当通道、遮非分割区、切片级特征+2D CNN |  |
| `tabular-playground-series-sep-2022` | "SMAPE 的承诺与陷阱"（30 票）与"比率至上"（34 票）说明该指标对低值/比率敏感，需注意预测下限与比率特征。**裁决**：SMAPE 赛优先用比率/相对量特征，并对低销量做稳健处理。置信度：中。 |  |
| `optiver-trading-at-the-close` | 2nd/3rd/4th/5th/8th/10th+ 方案未收录；1st 的"magic features"（seconds_in_bucket_group 聚合、rank 特征）工程细节只有代码片段。 |  |

### 复现/规模（17 条，展示 17 条）

| slug | 条目 | topic |
| --- | --- | --- |
| `h-and-m-personalized-fashion-recommendations` | pos:neg≈1:300（3rd）→ 保留 30× 正样本；1st：每周 100–200 万负样本；Giba：每顾客随机 200–500 负样本；6th 的实验显示 120↔220 候选几乎无差、lambdarank 在 1000 候选时掉分（0.0400→0.0381）。 |  |
| `orbit-wars` | **排名从不收敛**：评测期 rank 在 6–28 间摆动（top10 时间占比 24.2%，11–18 占 73.9%），"最后几十局决定名次"；社区提出对齐/收敛方案（CPMP、Ascalon），官方未采纳。 |  |
| `birdclef-2024` | 2nd/5th 未细读；"Compare BirdCLEF 2023 vs 2024"（67 票）与内存优化帖（58 票）未入库。 |  |
| `playground-series-s6e8` | 1st 的 agent 编排成本（token/GPU/时间）未量化；其"ChatGPT Pro 发现的新 FE"未公开细节； |  |
| `march-machine-learning-mania-2026` | 1st 的 harry_Rating 手调 scaler 是"个人意见注入"，不可复现/不可迁移；伤病调整依赖人工录入。 |  |
| `vesuvius-challenge-ink-detection` | **多类输出（nothing/mask/ink）**：1st 说输出更干净但未充分评估——一个被时间截断的方向。 |  |
| `feedback-prize-english-language-learning` | **种子平均的量化收益**：本场未给出"单种子 vs 3 种子"的对照数字（5th 只说流程）； |  |
| `child-mind-institute-detect-sleep-states` | **公开榜方差的量化**：无官方样本量/匹配方差估计，"公开不可信"是经验结论； |  |
| `h-and-m-personalized-fashion-recommendations` | 冷启动商品硬排 | 1st | 无交互=永远进不了 top12，别浪费算力 |  |
| `march-machine-learning-mania-2026` | 市场的可复现性问题（3rd 抓取于 3-19；赔率/期货随时间变化）。 |  |
| `child-mind-institute-problematic-internet-use` | 相信单种子分数 | 7th 的方差示例 | 多种子投票才是"分数" |  |
| `leash-BELKA` | 1st 的权重未完全恢复（只有 light 版本），复现需重训； |  |
| `tabular-playground-series-feb-2022` | 悬案 3：EMD 全量计算是否真的可行（2nd 因算力放弃）； |  |
| `santa-2025` | 纯随机初始解（大 N） | 1st/共识 | ≥40 就失效 |  |
| `playground-series-s4e2` | 种子效应（15 票 / 23 评论）与洗牌的关系未量化； |  |
| `playground-series-s6e5` | agent 工作流的 token/算力成本未量化； |  |
| `tabular-playground-series-oct-2022` | 多时间窗辅助目标的量化增益未给出； |  |
