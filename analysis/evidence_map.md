# 规律 × 数字证据映射（Evidence Map）

> 由 `scripts/build_evidence_map.py` 从 `analysis/claims.csv`（1850 行）生成；每条规律给出最多 5 条最相关数字证据，按「官方 > 图证 > 原文数字 > 自述」与场次匹配排序。
> 用途：写方案/做复盘时直接引用；引用前回 `analysis/deep/<slug>.md` 核对上下文。

## 1. L114–L133：Tier B 新规律的证据台账

### L114 指标结构套利
| 场次 | 断言 | 数字 | 证据类型 |
| --- | --- | --- | --- |
| `playground-series-s3e25` | 样本权重（74 票 / 35 评论） | 论证：若 10001 个样本里 5000 个误差 ≤0.4、其余 5000 个误差千万，分数仍是 0.4；因此只管"可能成为中位数"的样本。实现：对 `AE ≤ 0.06` 或 `≥ 0.7` 的样本给 **0.01 权重**，同一 LGB | 可复算-原文数字 |
| `playground-series-s3e25` | 数据分箱（54 票 / 42 评论） | 9 个档位（1.75/2.55/3.75/4.75/5.75/6.55/7.75/8.75/9.75）：**9533 个样本在 ±0.25 内、873 个在外（89.5%）**；若测试同分布，**猜对约 56% 即可 MedAE=0.25* | 可复算-原文数字 |
| `playground-series-s3e25` | 基线/分布 | LAD Stacker 基线 **LB 0.49737**；树模型（RF/GB/XGB/LGBM/HistGB 及集成）最低约 **0.49**；NN 被社区报告明显更强；**200+ 份提交卡在 0.25** | 可复算-原文数字 |
| `playground-series-s3e8` | 8th（392860） | 先"修离群值"→ CV 大涨但 LB 变差（发现模型本来就会压缩离群）；改做**分组合法性裁剪**：按 carat 滑窗（0.15）× cut × clarity × color 分组（>5 条记录），预测超过上界 → `Q3+1.5·IQ | 可复算-原文数字 |
| `playground-series-s3e8` | 2nd（392828） | 两级栈共 **1816 个模型**（L1 1709 个 XGB/CAT/LGBM/Ridge + L2 105 个 Ridge/blend/NN）；L1 选择用"CV 阈值从 574 逐 0.1 下探"，最优 cutoff **572.6* | 可复算-原文数字 |

### L115 目标随机性检验
| 场次 | 断言 | 数字 | 证据类型 |
| --- | --- | --- | --- |
| `playground-series-s5e9` | 随机目标检验 | 原目标 XGB vs **100 个打乱目标** XGB，z∈[-2,2] 判"随机"；近 6 场回归 **3/6 随机**：S4E12 保险、S5E2 背包、S5E9 BPM；S4E9 二手车、S5E4 播客、S5E5 卡路里有信号；** | 可复算-原文数字 |
| `playground-series-s4e12` | 社区：NaN 与目标（552165，126 票 / 87 评论） | 数据中**部分 NaN 与目标强相关**：以 Annual Income 为例，NaN 的平均保费 ≈485，**低于所有非 NaN 分箱（560–820）**（图 1）——"NaN 不能按均值填补，否则会抹掉信息"；三种处理法：① 交给能 | 可复算-图证 |
| `playground-series-s5e2` | 数据信号解释（564056） | 原数据集 10% 行有重复（作者复制了 5%）；合成把 5e4 行扩成 4e6 行 ≈ **每行 80 份副本**；因此 10% 的行可用 KNN k=1 直接找到孪生行、90% 的行有 ~79 个同源行；`groupby` 聚合的作用就是 | 可复算-原文数字 |
| `playground-series-s4e12` | 1st（554328） | 单模型 XGBoost + **611 个特征**；编码体系：对每个类别列给出 **原始列 + 6 种表示**（label、TE mean、CE、TE median/min/max/nunique）；**组合生成新类别列**（2–6 列任意 | 可复算-原文数字 |
| `playground-series-s5e2` | 1st（565539） | **单模型 XGBoost（500 特征，1×A100）**；T4 版 138 特征同样夺冠；一个月训练 **300+ XGB**、尝试**上千个 FE 想法**（RAPIDS cuDF-Pandas 加速）；核心特征：`groupby(C | 可复算-原文数字 |

### L116 实体块切分/分组 CV
| 场次 | 断言 | 数字 | 证据类型 |
| --- | --- | --- | --- |
| `scrabble-player-rating` | CV 核心问题 | 数据中同一玩家的历史**整体落在 train 或 test**；作者从 KFold 改 **GroupKFold（nickname 分组）** 后分数"substantially worse"；**StratifiedGroupKFold* | 未分级 |
| `playground-series-s3e22` | 实体复用怪癖 | 按 hospital_number × outcome 透视可见同一编号多次出现、甚至"死 5 次"；"horse treated > 1 time" 语义与合成数据叠加 | 可复算-原文数字 |
| `playground-series-s3e22` | 洗牌烈度 | 36 票专帖用 public-private 散点划出 **7 个区域**（region 2/6 = 公榜好私榜崩；region 3/4/5 = CV 可信者私榜反弹）；29 票"Beware of the public LB!"；"Out | 可复算-原文数字 |
| `playground-series-s3e22` | 领域文献（438620） | AI 预测需手术/存活：Decision Tree / MLP / Bayes 等，**76%（需手术）、85%（存活）**准确率；Cox 术后模型：存活率 10 天 **0.87** → 100 天 **0.82** → 600 天 ** | 可复算-原文数字 |
| `playground-series-s3e9` | CV vs 公开榜 | CV **5407** 样本（一次测量）vs 公开榜 **721** 样本（随机变量）；作者用 7 次提交只是好奇，主张 **≤2 次** | 可复算-原文数字 |

### L117 评审闭环
| 场次 | 断言 | 数字 | 证据类型 |
| --- | --- | --- | --- |
| `pokemon-tcg-ai-battle-challenge-strategy` | 高分特征（官方总结） | ① 用自建评测（self-play arena、对冻结对手的联赛、固定对手评测集）驱动迭代，并说清"分析后改了什么"② 展示组件贡献（通用 vs 专用策略、有/无搜索、两副牌对比、rating/胜率随时间）③ 讨论失败的尝试（端到端组牌、联 | 可复算-官方 |
| `pokemon-tcg-ai-battle-challenge-strategy` | 资格摩擦 | Simulation 报名截止 **2026-08-09 23:59 UTC**；多帖反映 write-up 完成后无法进入 Simulation（735276 / 734869 / 735402 / 735996 / 740873 / 7 | 可复算-原文数字 |
| `pokemon-tcg-ai-battle-challenge-strategy` | 平台摩擦 | 草稿被 "ssssssadasfsd" 覆盖 bug、已提交 write-up 无法删除（forumMessages.update 权限）、组队 bug、两份 EN 卡表 218 张不一致（含未翻译日文）、卡库 bug + 先手 deck- | 可复算-原文数字 |
| `nfl-big-data-bowl-2024` | 数据质量问题 | "Is there a Data Discrepancy?"（14 票 / 6 评论）；preSnap 胜率列命名错位（447011）；部分 play 位置"滞后"；tackles 数据不一致；追踪数据缺失；passresult 缺失；ba | 可复算-原文数字 |
| `pokemon-tcg-ai-battle-challenge-strategy` | 规模 | Simulation **6807 队**；Strategy **942 份 write-up**；Top 20 授奖、**Top 8 晋级第二轮**（YouTube 直播） | 可复算-原文数字 |

### L118 评审可信度工程
| 场次 | 断言 | 数字 | 证据类型 |
| --- | --- | --- | --- |
| `openai-gpt-oss-20b-red-teaming` | 评审漏斗 | 高召回初筛（人工 + LLM 评审）→ **145 份深度复核**（验证、复现、访问全部链接产物）→ 评委集中深议；另混入**"below the line"盲样**做召回 QA（评委不知情、顺序随机）；评审开始前**更换 1 名评委**避 | 可复算-原文数字 |
| `openai-gpt-oss-20b-red-teaming` | 官方主要发现 | ① CoT 可被伪造/欺骗（用户轮塞入伪造 CoT；有的靠 Harmony 格式细节，有的靠语义模仿）② 工具与 Harmony 通道漏洞（主通道拒绝但工具通道执行；虚构 channel；用工具建立"权威"）③ **大量问题在 `reaso | 可复算-官方 |
| `bigquery-ai-hackathon` | 评审流程（硬门槛） | 每份**人工阅读**并多次评估；按 rubric 权重，**缺多个 artifact 的直接过滤**；**必须使用三大类之一**（无 BigQuery AI 则过滤）；**公开可访问**是要求；每个获奖提交都被评委**实际复现/验证**（必 | 未分级 |
| `pokemon-tcg-ai-battle-challenge-strategy` | 高分特征（官方总结） | ① 用自建评测（self-play arena、对冻结对手的联赛、固定对手评测集）驱动迭代，并说清"分析后改了什么"② 展示组件贡献（通用 vs 专用策略、有/无搜索、两副牌对比、rating/胜率随时间）③ 讨论失败的尝试（端到端组牌、联 | 可复算-官方 |
| `bigquery-ai-hackathon` | 奖项 | 三类各 1 名"Best in X"+前三：GenAI（TriLink / AI Patent Analyst / ESG Reports Agent）、Vector Search（SpeakAura AI / ReDrugAI / Cau | 可复算-原文数字 |

### L119 危害增量判定
| 场次 | 断言 | 数字 | 证据类型 |
| --- | --- | --- | --- |
| `openai-gpt-oss-20b-red-teaming` | 官方主要发现 | ① CoT 可被伪造/欺骗（用户轮塞入伪造 CoT；有的靠 Harmony 格式细节，有的靠语义模仿）② 工具与 Harmony 通道漏洞（主通道拒绝但工具通道执行；虚构 channel；用工具建立"权威"）③ **大量问题在 `reaso | 可复算-官方 |
| `openai-gpt-oss-20b-red-teaming` | 社区产物 | 攻击方法分层分类（Prompt Injection / Social Engineering / CoT Manipulation / Covert Channels / Reward Hacking / Deceptive Alignme | 可复算-原文数字 |
| `openai-gpt-oss-20b-red-teaming` | 防御建议 | 生产部署考虑 `reasoning_effort=high`；输入校验（防止用户消息被解析为特殊 token）；拒绝伪造 CoT / 政策 / 工具调用；输出使用前先验证（defense-in-depth） | 未分级 |
| `openai-gpt-oss-20b-red-teaming` | 规模 | **600+ 份提交 / 601 队**，官方称 Kaggle 史上最大 hackathon | 可复算-官方 |
| `openai-gpt-oss-20b-red-teaming` | 评审漏斗 | 高召回初筛（人工 + LLM 评审）→ **145 份深度复核**（验证、复现、访问全部链接产物）→ 评委集中深议；另混入**"below the line"盲样**做召回 QA（评委不知情、顺序随机）；评审开始前**更换 1 名评委**避 | 可复算-原文数字 |

### L120 分层学习率
| 场次 | 断言 | 数字 | 证据类型 |
| --- | --- | --- | --- |
| `planttraits2024` | 1st（PlantHydra） | 三头：回归头（归一化性状）+ 分类头（**17,396 个"物种"**）+ 软分类头（按 softmax 权重对物种性状加权求和），三头权重可训练；DINOv2 ViT-b/l + **PlantCLEF 2024 西南欧植物预训练**；元 | 可复算-原文数字 |
| `planttraits2024` | 6th（AutoGluon） | TIMM 图像特征 + 表格特征 → Transformer 融合（略优于 MLP）；**标签链**（按论文 R² 顺序逐个预测）；EVA 系列最强：`eva_large_patch14_336` private **0.483**、`ev | 可复算-原文数字 |
| `planttraits2024` | 赛事事故 | 有选手用 `sample_submission.csv` 提分 → 官方**更新测试集（图片+test.csv）并重置 LB**；`sample_submission.csv` 在新测试集上从正分变成 **-33.38** | 可复算-官方 |
| `planttraits2024` | 9th（DINOv2+CatBoost） | DINOv2 [giant] embedding + 表格 → **CatBoost 原生处理 embedding**（含降维）；public **0.51162** / private **0.51238**；2 阶多项式特征小增益；** | 可复算-原文数字 |
| `planttraits2024` | 公开基线进展 | 纯表格 +0.02486（480563）；表格 + ImageNet 特征 ≈0.22（489515）；EfficientNetB0 仅正分 +0.08921（486973）；sample_submission + 表格 = 0.3584（ | 可复算-原文数字 |

### L121 身份辅助任务
| 场次 | 断言 | 数字 | 证据类型 |
| --- | --- | --- | --- |
| `planttraits2024` | 1st（PlantHydra） | 三头：回归头（归一化性状）+ 分类头（**17,396 个"物种"**）+ 软分类头（按 softmax 权重对物种性状加权求和），三头权重可训练；DINOv2 ViT-b/l + **PlantCLEF 2024 西南欧植物预训练**；元 | 可复算-原文数字 |
| `planttraits2024` | 6th（AutoGluon） | TIMM 图像特征 + 表格特征 → Transformer 融合（略优于 MLP）；**标签链**（按论文 R² 顺序逐个预测）；EVA 系列最强：`eva_large_patch14_336` private **0.483**、`ev | 可复算-原文数字 |
| `planttraits2024` | 赛事事故 | 有选手用 `sample_submission.csv` 提分 → 官方**更新测试集（图片+test.csv）并重置 LB**；`sample_submission.csv` 在新测试集上从正分变成 **-33.38** | 可复算-官方 |
| `planttraits2024` | 9th（DINOv2+CatBoost） | DINOv2 [giant] embedding + 表格 → **CatBoost 原生处理 embedding**（含降维）；public **0.51162** / private **0.51238**；2 阶多项式特征小增益；** | 可复算-原文数字 |
| `planttraits2024` | 数据质量争议 | 极端标签值处理（9 票 / 10 评论）；"Poor labeling"（7 票）；为何不给物种（7 票）；性状数 6 vs 聚合数据 33（5 票）；单位为题；负 X4；R² 只计正值的规则被质疑 | 可复算-原文数字 |

### L122 提交契约
| 场次 | 断言 | 数字 | 证据类型 |
| --- | --- | --- | --- |
| `autonomous-agent-prediction-beta` | 官方失败清单（9 票 / 11 评论） | ① 多工具只支持全是 search 工具（gemini-2.5-* 仅单工具；deepseek-r1-0528 不支持工具）② skill 名必须 lowercase kebab-case ③ agent 没交有效预测（思考死循环烧 tok | 可复算-官方 |
| `autonomous-agent-prediction-beta` | 社区技巧/坑 | LB 0.823 模板（利用 "freeroll" fallback 规则 + Gemini Pro，2 票）；`select_submission` 实测收益上限 +0.0005、最差 −0.0166（0 票 / 5 评论）；本地评测 ` | 可复算-原文数字 |
| `bigquery-ai-hackathon` | 奖项 | 三类各 1 名"Best in X"+前三：GenAI（TriLink / AI Patent Analyst / ESG Reports Agent）、Vector Search（SpeakAura AI / ReDrugAI / Cau | 可复算-原文数字 |
| `gan-getting-started` | 资源大盘（24 票） | 书籍（Goodfellow DL ch20、Chollet ch8、GANs in Action）；模型族（GAN/DCGAN/cGAN/SS-GAN/InfoGAN/ACGAN/WGAN/WGAN-GP/LSGAN/Pix2Pix/Cyc | 可复算-原文数字 |
| `gan-getting-started` | 提交/评测坑 | zip 里没有图片、Evaluator 找不到 images.zip、output file not found、如何提交预测、PyTorch 是否可用/是否必须 TPU；有 starter 报告 LB 61.3 | 可复算-原文数字 |

### L123 平台能力配给
| 场次 | 断言 | 数字 | 证据类型 |
| --- | --- | --- | --- |
| `autonomous-agent-prediction-beta` | 预算讨论 | "LLM 预算只有 $2？"（11 票）；能否用 Kaggle Benchmarks 额度加预算；超预算怎么办；每 session 60 分钟 | 可复算-原文数字 |
| `gemini-long-context` | 配额与限流 | 免费额度（9 票 / 30 评论）、quota 提升、**429 ResourceExhausted**（多帖）、**503/504 超时 600s**、Vertex 视频 502/503/429、context caching 403—— | 可复算-原文数字 |
| `autonomous-agent-prediction-beta` | 官方失败清单（9 票 / 11 评论） | ① 多工具只支持全是 search 工具（gemini-2.5-* 仅单工具；deepseek-r1-0528 不支持工具）② skill 名必须 lowercase kebab-case ③ agent 没交有效预测（思考死循环烧 tok | 可复算-官方 |
| `bigquery-ai-hackathon` | 云额度 | 新用户 90 天 **$300** 试用 + BigQuery 免费层 + 填表再给的 **$50** 额度（每周发放、先到先得）+ 无信用卡者可领多个 **$5 instrumentless credits** | 可复算-原文数字 |
| `llm-prompting-with-makersuite` | 评审规模 | 官方评估 **200+ 份提交**，选出 **7 个类别各 1 名获奖**（Developer Tools / Data Science Tools / Education & Interactive Tutors / Utilities  | 可复算-官方 |

### L124 RL 课程+热启动
| 场次 | 断言 | 数字 | 证据类型 |
| --- | --- | --- | --- |
| `lux-ai-season-2-neurips-stage-2` | 训练课程 | 16×16 → 32×32 → 64×64，每段 **80M 步**，后段用前段最佳 checkpoint 热启动；向量化环境 **1024/1024/512**；16×16 用相邻工厂 spawn hack | 可复算-原文数字 |
| `lux-ai-season-2-neurips-stage-2` | 奖励与稳定性 | generation/resources 各统计量除以 **5M 步窗口的 EMA 标准差** + WinLoss(+1/-1/0)；通过改奖励权重即可切换策略（32/64 更奖励 ore/metal/机器人）；32×32 KL **>0. | 可复算-图证 |
| `lux-ai-season-2-neurips-stage-2` | 社区设施 | 上手资源帖 16 票（官方教程 + Lux S2 前 10 方案 + Lux 2021/Kore/Hungry Geese）；Parametrix.ai 的 PPO 基线 + 往季 episode 下载；第三方统计站（score growt | 可复算-官方 |
| `lux-ai-season-2-neurips-stage-2` | 模型 | DoubleCone 风格 + 额外 4× 下采样（感受野到 64×64）；**4,719,403 参数**；value 输出 14；policy 每位置 29 个 logit（24 单位 + 4 工厂 + 1 放置）；动作类型/子动作按独 | 可复算-图证 |
| `lux-ai-season-2-neurips-stage-2` | 算力 | Lambda Cloud **1×A10**/实例；大地图用 A100 翻倍 mini-batch；PyTorch bfloat16 autocast + 梯度累积；进度停滞则提前停训 | 可复算-原文数字 |

### L125 RL 收益拐点
| 场次 | 断言 | 数字 | 证据类型 |
| --- | --- | --- | --- |
| `lux-ai-season-2-neurips-stage-2` | 奖励与稳定性 | generation/resources 各统计量除以 **5M 步窗口的 EMA 标准差** + WinLoss(+1/-1/0)；通过改奖励权重即可切换策略（32/64 更奖励 ore/metal/机器人）；32×32 KL **>0. | 可复算-图证 |
| `lux-ai-season-2-neurips-stage-2` | 社区设施 | 上手资源帖 16 票（官方教程 + Lux S2 前 10 方案 + Lux 2021/Kore/Hungry Geese）；Parametrix.ai 的 PPO 基线 + 往季 episode 下载；第三方统计站（score growt | 可复算-官方 |
| `lux-ai-season-2-neurips-stage-2` | 模型 | DoubleCone 风格 + 额外 4× 下采样（感受野到 64×64）；**4,719,403 参数**；value 输出 14；policy 每位置 29 个 logit（24 单位 + 4 工厂 + 1 放置）；动作类型/子动作按独 | 可复算-图证 |
| `lux-ai-season-2-neurips-stage-2` | 训练课程 | 16×16 → 32×32 → 64×64，每段 **80M 步**，后段用前段最佳 checkpoint 热启动；向量化环境 **1024/1024/512**；16×16 用相邻工厂 spawn hack | 可复算-原文数字 |
| `lux-ai-season-2-neurips-stage-2` | 算力 | Lambda Cloud **1×A10**/实例；大地图用 A100 翻倍 mini-batch；PyTorch bfloat16 autocast + 梯度累积；进度停滞则提前停训 | 可复算-原文数字 |

### L126 规则优先/RL 局部化
| 场次 | 断言 | 数字 | 证据类型 |
| --- | --- | --- | --- |
| `kore-2022-beta` | DQN 基线（tf.js） | 输入 **2×8**（player/enemies 分组；kore、船数（总/外/内）、船坞数、早/中/晚标志，部分 log2）；输出 4 个动作（DO_NOTHING/MINE/BUILD_SHIP/BUILD_SHIPYARD）交给规则 | 可复算-原文数字 |
| `lux-ai-season-2-neurips-stage-2` | 社区设施 | 上手资源帖 16 票（官方教程 + Lux S2 前 10 方案 + Lux 2021/Kore/Hungry Geese）；Parametrix.ai 的 PPO 基线 + 往季 episode 下载；第三方统计站（score growt | 可复算-官方 |
| `kore-2022-beta` | 1st（规则型，58 票 / 24 评论） | 七个顺序模块：① 船坞防御（算清"现有+在途"后补最小兵，必要时从最近船坞调兵）② 船坞进攻（算清夺取所需兵力）③ 直接攻击（拦截敌方舰队，路线避开敌线）④ **相邻攻击**（牺牲己方舰队换取对敌 2–3 倍伤害）⑤ 扩张（kore 盈余且 | 可复算-原文数字 |
| `kore-2022-beta` | 社区反思（11 票） | 读官方 notebook 起步；尝试 Q-learning **完全没打出成绩**，最终高分主要来自"改官方示例"；RL 的难点包括**延迟奖励**（船返航后 kore 才变化，奖励要回溯到早前动作） | 可复算-官方 |
| `maze-crawler` | 最终排名 | **1 Maksim Savelev 2006.5 > 2 bunterrrr 1953.4 > 3 Genematon 1796.4**；1st 估计对 bunterrrr 约 53/47，且 rating 变化 ±5 不对称收敛慢 | 可复算-图证 |

### L127 近镜像鲁棒性
| 场次 | 断言 | 数字 | 证据类型 |
| --- | --- | --- | --- |
| `maze-crawler` | 最终排名 | **1 Maksim Savelev 2006.5 > 2 bunterrrr 1953.4 > 3 Genematon 1796.4**；1st 估计对 bunterrrr 约 53/47，且 rating 变化 ±5 不对称收敛慢 | 可复算-图证 |
| `maze-crawler` | 1st 关键常数 | `MINER_PHASE_END=350`、`MIN_NODE_SBD=30`、**`ENERGY_CAP=3000`（一次性锁存：到 3000 后永久停止采矿转为猎杀）**、`WORKER_PHASE_START=400`、`SCOUT_ | 可复算-原文数字 |
| `maze-crawler` | tiebreak 细节 | 矿工 = **300 能量**；在敌人曼哈顿距离 ≤5 时于"工厂刚离开的格子"（`OPPOSITE[last_move_dir]`）放矿工；预测 1–2 tick 内将被卷出的矿工按已死处理，避免"矿工与工厂同 tick 死亡"输掉 ti | 可复算-原文数字 |
| `maze-crawler` | 终局规则 | 工厂相撞或一方被卷出；**相撞由存活机器人总能量决定**；多数强队选择"攒能量等 500 步后的 tiebreak" | 可复算-原文数字 |
| `maze-crawler` | 3rd 路线 | **JAX 环境移植 + 行为克隆 bootstrap + PPO self-play**；小型网络（棋盘 CNN + 标量信息通路）；奖励=胜负 + 少量能量 shaping；大样本评估；自述弱点：自对弈池同质 → 能量强、战斗弱 | 自述 |

### L128 密度分层后处理
| 场次 | 断言 | 数字 | 证据类型 |
| --- | --- | --- | --- |
| `iwildcam2022-fgvc9` | 1st（不训练） | 基于 MegaDetector 检测过滤；观察"阈值 0.95 会**高密度图少算、低密度图多算**"，以**每图 8 个预测**为界分两类：高密度图用**置信度 0.0 + NMS(IoU=0.2) + 抑制小框**（public 0.2 | 可复算-图证 |
| `iwildcam2022-fgvc9` | 9th（重工程） | MegaDetector v4 检测 → 训练 **YOLOv5** 第二检测器 → **WBF 加权框融合**（public/private **0.275/0.265**，高于 2021 冠军基线）→ 对 8 类群居物种（白唇西貒 2、 | 可复算-原文数字 |
| `iwildcam2022-fgvc9` | 官方数据资产 | DeepMAC 实例掩码（对 MegaDetector V4 框）随赛程发布，可用竞赛数据页或 GitHub 下载，配可视化 notebook | 可复算-官方 |
| `iwildcam2022-fgvc9` | 数据问题 | 重复数据（324436）；序列乱序（324425）；sample submission 格式疑问（317140）；wrap-up 截止 6/10（328927） | 可复算-原文数字 |
| `iwildcam2022-fgvc9` | 社区参考 | 往届 Wildcam（2019–2021）热门 notebook 与获奖方案合集（16 票）；起步 notebook 5 个（CNN、数据提取、DeepMAC 掩码可视化、GPS 聚类、TF starter） | 可复算-原文数字 |

### L129 域适应组合
| 场次 | 断言 | 数字 | 证据类型 |
| --- | --- | --- | --- |
| `sorghum-id-fgvc-9` | 3rd（328593） | 消融表：base（resnet50@512）0.73 → 直方图均衡 +0.03 → **IBN-ResNet +0.05** → bnn-neck +0.005 → 最后卷积 stride=1 +0.005 → **ArcFace(s=3 | 可复算-原文数字 |
| `hotel-id-to-combat-human-trafficking-2022-fgvc9` | 1st（328281） | 5 模型集成（1024×1024 与 384×384 两种尺寸），**ArcFace** 训练，嵌入 1536D → 拼接后 **PCA 到 3072D（保留 99% 方差）** → KNN；无后处理/重排；**BlendFlip 贡献约  | 自述 |
| `sorghum-id-fgvc-9` | 2nd（329414） | 只用本届数据；RegNetY-16.0GF；960 从 1024 裁剪；private：base@512 **84.1** → 960 **91.9** → 伪标签 **95.1** → dropout **95.3** → 集成 **95 | 可复算-原文数字 |
| `hotel-id-to-combat-human-trafficking-2022-fgvc9` | 2nd（328345） | 50K+FGVC9；按 **md5 去重**（同 md5 不同类别删除）后保留 **45,769 个类别**；方向模型把图旋正；先全量 10–20 epoch，再对 FGVC9 的 **3116 类微调 40 epoch（+0.03）**； | 可复算-原文数字 |
| `hotel-id-to-combat-human-trafficking-2022-fgvc9` | 3rd（328237） | 多骨干（Swin、ConvNeXt、ResNet200D、EfficientNet + DOLG，尺寸 384–1024）；用 FGVC8 外部数据 + KNN 伪标签 + 均值聚合；**logits 优于 KNN**；推理约 2 小时；最 | 可复算-原文数字 |

### L130 标签病态松弛
| 场次 | 断言 | 数字 | 证据类型 |
| --- | --- | --- | --- |
| `geolifeclef-2022-lifeclef-2022-fgvc9` | 无效尝试 | 2nd：环境协变量与 GPS 直接入 CNN（坐标 MLP 各种编码都欠拟合）、taxonomy 辅助任务、直方图密度预测、长尾专门处理（**"什么都不做"最好**，因为测试集同样长尾）；1st：多标签聚合、其他骨干、无迁移学习、三骨干分工 | 可复算-原文数字 |
| `geolifeclef-2024` | 数据访问 | PA 数据在 Kaggle；**原始栅格在 Seafile**，需分组下载 zip；官方建议 `python download.py --data output --raster --presence-only --all-variable | 可复算-官方 |
| `geolifeclef-2022-lifeclef-2022-fgvc9` | 2nd 单模配方 | 两条不共享参数的 CNN 分支：RGB；海拔+NIR+NDVI → concat → **dropout 0.45** → 17,034 类 softmax CE；Inception-v4 比 ResNet-50 约 **+2%**；Ima | 可复算-原文数字 |
| `geolifeclef-2022-lifeclef-2022-fgvc9` | 1st 集成 | ① ResNet34 双模态（NIR+G+B）+ 3 层 FCN（环境向量 + lat/lon + country + 海拔均值/极差 + landcover "dothot" 编码）→ 17k 分类层；② MobileNetV3-larg | 可复算-原文数字 |
| `geolifeclef-2024` | 周边 | FGVC11 其他 Kaggle 赛（数据格式相近，可多赛复用）；官方 Discord；CLEF 2025 是否会继续（9 评论） | 可复算-官方 |

### L131 原数据先对抗验证
| 场次 | 断言 | 数字 | 证据类型 |
| --- | --- | --- | --- |
| `playground-series-s3e18` | 11th（423642） | 删 `HeavyAtomMolWt` 与 `fr_COO2`（99% 与 fr_COO 相同）、删 `FpDensityMorgan1 == -666` 记录、去重 → 训练 **15824 行**；EC1 CatBoost+LGBM+XG | 可复算-原文数字 |
| `playground-series-s3e18` | "两场比赛"证据（图） | EC1：KNN(1180) 0.6981、LR 0.7005、ET(12) 0.7073、RF(45) 0.7087、Ensemble 0.7092；EC2：LR 0.5773、KNN(490) 0.5859、RF(80) 0.5865、E | 可复算-原文数字 |
| `playground-series-s3e18` | 清洗/异常清单 | `FpDensityMorgan1=-666`（"trains to hell"）；`fr_COO/fr_COO2` 出现 test 有 train 无的取值；`NumHeteroatoms` 40/48 两边都没有；负氢原子数；`Heav | 可复算-原文数字 |
| `playground-series-s3e18` | EC2 最佳单模型 | **Bagged KNN**（KNN 套在 BaggingClassifier 里，log1p + StandardScaler + distance 权重）——30 票 / 24 评论专帖 | 可复算-原文数字 |
| `playground-series-s3e18` | 特征选择 | EC1 约 **19 个重要特征**，EC2 只有约 **7 个**；10 个高度相关特征（BertzCT/ExactMolWt/HeavyAtomMolWt/Chi 系列）可 PCA 合 1 | 可复算-原文数字 |

### L132 LLM 验证义务
| 场次 | 断言 | 数字 | 证据类型 |
| --- | --- | --- | --- |
| `maze-crawler` | 最终排名 | **1 Maksim Savelev 2006.5 > 2 bunterrrr 1953.4 > 3 Genematon 1796.4**；1st 估计对 bunterrrr 约 53/47，且 rating 变化 ±5 不对称收敛慢 | 可复算-图证 |
| `data-assistants-with-gemma` | 中期获奖配方 ③ | @lucamassaron《Data Science AI Assistant with Gemma 2b-it》：**从零手写 RAG**（`generate_summary_and_answer()`，Wikipedia API 造数据 | 可复算-原文数字 |
| `openai-to-z-challenge` | 技术素材（社区） | NASA Amazon LiDAR 处理成 DTM（18 票）；"DEM is all you need"；高光谱影像；Major TOM embeddings 候选点搜索；RAG-LLM 方案；NDVI/土壤筛选交互地图 | 可复算-图证 |
| `data-assistants-with-gemma` | 讨论区热度 | 置顶 Q&A **81 评论**；Gemma 发布帖 50 票；"ANY csv + 简单 prompt" 21 票；量化/动态量化 21 票；"原创 vs 抄 notebook" 20 票；抄袭帖 6 票 / 5 评论；"不精调 Gemm | 可复算-原文数字 |
| `maze-crawler` | 1st 关键常数 | `MINER_PHASE_END=350`、`MIN_NODE_SBD=30`、**`ENERGY_CAP=3000`（一次性锁存：到 3000 后永久停止采矿转为猎杀）**、`WORKER_PHASE_START=400`、`SCOUT_ | 可复算-原文数字 |

### L133 评审赛激励设计
| 场次 | 断言 | 数字 | 证据类型 |
| --- | --- | --- | --- |
| `nfl-big-data-bowl-2026-analytics` | 冠军生态资源 | 2025 冠军 @VishakhSandwar 的开源补充：**帧级 coverage scheme + 球员级 coverage 细节**数据集；基于 Udit Ranasaria & Pavel Vabishchevich 的 Tran | 可复算-原文数字 |
| `playground-series-s3e25` | 样本权重（74 票 / 35 评论） | 论证：若 10001 个样本里 5000 个误差 ≤0.4、其余 5000 个误差千万，分数仍是 0.4；因此只管"可能成为中位数"的样本。实现：对 `AE ≤ 0.06` 或 `≥ 0.7` 的样本给 **0.01 权重**，同一 LGB | 可复算-原文数字 |
| `data-assistants-with-gemma` | 中期获奖配方 ③ | @lucamassaron《Data Science AI Assistant with Gemma 2b-it》：**从零手写 RAG**（`generate_summary_and_answer()`，Wikipedia API 造数据 | 可复算-原文数字 |
| `data-assistants-with-gemma` | 赛制 | 无排行榜、评审制；**中期奖：前 5 周 5 个公开 notebook**；**25 份 swag** 给上传文档良好的 Gemma 模型变体并在提交中使用的人；最终截止 2024-04-14 | 可复算-原文数字 |
| `data-assistants-with-gemma` | 中期获奖配方 ① | @jacoporepossi《Text Summarization with Gemma》：**Transformers gemma-2b-it + LangChain**（Stuffing / MapReduce / Refine 管线） | 可复算-原文数字 |

## 2. T28–T37：新张力的证据台账

### T28 随机目标 vs 合成痕迹
| 场次 | 断言 | 数字 | 证据类型 |
| --- | --- | --- | --- |
| `playground-series-s5e9` | 随机目标检验 | 原目标 XGB vs **100 个打乱目标** XGB，z∈[-2,2] 判"随机"；近 6 场回归 **3/6 随机**：S4E12 保险、S5E2 背包、S5E9 BPM；S4E9 二手车、S5E4 播客、S5E5 卡路里有信号；** | 可复算-原文数字 |
| `playground-series-s5e2` | 数据信号解释（564056） | 原数据集 10% 行有重复（作者复制了 5%）；合成把 5e4 行扩成 4e6 行 ≈ **每行 80 份副本**；因此 10% 的行可用 KNN k=1 直接找到孪生行、90% 的行有 ~79 个同源行；`groupby` 聚合的作用就是 | 可复算-原文数字 |
| `playground-series-s5e2` | 1st（565539） | **单模型 XGBoost（500 特征，1×A100）**；T4 版 138 特征同样夺冠；一个月训练 **300+ XGB**、尝试**上千个 FE 想法**（RAPIDS cuDF-Pandas 加速）；核心特征：`groupby(C | 可复算-原文数字 |
| `playground-series-s5e2` | 3rd（565653） | 距离特征（属性映射后两两平方差）；**COMBO = 类别×100 + Weight Capacity**；外部数据集的价格统计（mean/std/min/max/median + missing 标志）；cuDF 分组聚合 + cuML  | 可复算-原文数字 |
| `playground-series-s5e2` | 5th（565583） | 赛程过半都不信有信号；向原作者求证 → 目标确实是随机采样，但复制结构仍可利用；25 模型 AutoGluon 集成 CV 38.593/LB 38.853（gap 0.26，疑似过拟合）vs Ridge 版 CV 38.639/LB 38 | 可复算-原文数字 |

### T29 多目标拆 vs 合
| 场次 | 断言 | 数字 | 证据类型 |
| --- | --- | --- | --- |
| `playground-series-s3e18` | "两场比赛"证据（图） | EC1：KNN(1180) 0.6981、LR 0.7005、ET(12) 0.7073、RF(45) 0.7087、Ensemble 0.7092；EC2：LR 0.5773、KNN(490) 0.5859、RF(80) 0.5865、E | 可复算-原文数字 |
| `playground-series-s3e18` | 11th（423642） | 删 `HeavyAtomMolWt` 与 `fr_COO2`（99% 与 fr_COO 相同）、删 `FpDensityMorgan1 == -666` 记录、去重 → 训练 **15824 行**；EC1 CatBoost+LGBM+XG | 可复算-原文数字 |
| `playground-series-s3e18` | EC2 最佳单模型 | **Bagged KNN**（KNN 套在 BaggingClassifier 里，log1p + StandardScaler + distance 权重）——30 票 / 24 评论专帖 | 可复算-原文数字 |
| `playground-series-s3e18` | 特征选择 | EC1 约 **19 个重要特征**，EC2 只有约 **7 个**；10 个高度相关特征（BertzCT/ExactMolWt/HeavyAtomMolWt/Chi 系列）可 PCA 合 1 | 可复算-原文数字 |
| `playground-series-s3e18` | 规模与数据 | **1047 队**；38 列 / **14.8k 行**；目标是 EC1/EC2（训练里还有 EC3–EC6，但测试里没有）；原始数据集 3 个 csv、每个 200–500 列 | 可复算-原文数字 |

### T30 伪标签增益 vs 不可证
| 场次 | 断言 | 数字 | 证据类型 |
| --- | --- | --- | --- |
| `playground-series-s5e9` | 26th（610264） | 54 特征（XGB/LGB/Cat 重要性 + permutation + SHAP）；**18 个模型**（6 XGB-Optuna、4 LGBM、3 HistGBR、2 YDF、Ridge、ElasticNet、NN）；从测试残差取 3 | 可复算-原文数字 |
| `sorghum-id-fgvc-9` | 3rd（328593） | 消融表：base（resnet50@512）0.73 → 直方图均衡 +0.03 → **IBN-ResNet +0.05** → bnn-neck +0.005 → 最后卷积 stride=1 +0.005 → **ArcFace(s=3 | 可复算-原文数字 |
| `sorghum-id-fgvc-9` | 2nd（329414） | 只用本届数据；RegNetY-16.0GF；960 从 1024 裁剪；private：base@512 **84.1** → 960 **91.9** → 伪标签 **95.1** → dropout **95.3** → 集成 **95 | 可复算-原文数字 |
| `sorghum-id-fgvc-9` | 1st（329049） | ConvNeXt base；5 折集成；把竞赛数据与 FGVC8 合并成 **223 类**（原 100 类）；private：convb+100 类 0.952 → +223 类 0.954 → 集成 0.957 → +伪标签 0.962 | 可复算-原文数字 |
| `geolifeclef-2022-lifeclef-2022-fgvc9` | 1st 集成 | ① ResNet34 双模态（NIR+G+B）+ 3 层 FCN（环境向量 + lat/lon + country + 海拔均值/极差 + landcover "dothot" 编码）→ 17k 分类层；② MobileNetV3-larg | 可复算-原文数字 |

### T31 分组 CV vs LB
| 场次 | 断言 | 数字 | 证据类型 |
| --- | --- | --- | --- |
| `playground-series-s3e9` | CV vs 公开榜 | CV **5407** 样本（一次测量）vs 公开榜 **721** 样本（随机变量）；作者用 7 次提交只是好奇，主张 **≤2 次** | 可复算-原文数字 |
| `scrabble-player-rating` | CV 核心问题 | 数据中同一玩家的历史**整体落在 train 或 test**；作者从 KFold 改 **GroupKFold（nickname 分组）** 后分数"substantially worse"；**StratifiedGroupKFold* | 未分级 |
| `playground-series-s3e22` | 洗牌烈度 | 36 票专帖用 public-private 散点划出 **7 个区域**（region 2/6 = 公榜好私榜崩；region 3/4/5 = CV 可信者私榜反弹）；29 票"Beware of the public LB!"；"Out | 可复算-原文数字 |
| `playground-series-s3e22` | 领域文献（438620） | AI 预测需手术/存活：Decision Tree / MLP / Bayes 等，**76%（需手术）、85%（存活）**准确率；Cox 术后模型：存活率 10 天 **0.87** → 100 天 **0.82** → 600 天 ** | 可复算-原文数字 |
| `playground-series-s3e9` | 1st 最终对比 | GB+RF+Ridge（含 LGBM 变体）≈ **12.03** 最好；单 Ridge ≈ **12.16**；GB 单独 ≈12.07；LGBM ≈12.09；RF ≈12.10（见 394592_img/01） | 可复算-图证 |

### T32 主动终局 vs 被动 tiebreak
| 场次 | 断言 | 数字 | 证据类型 |
| --- | --- | --- | --- |
| `maze-crawler` | tiebreak 细节 | 矿工 = **300 能量**；在敌人曼哈顿距离 ≤5 时于"工厂刚离开的格子"（`OPPOSITE[last_move_dir]`）放矿工；预测 1–2 tick 内将被卷出的矿工按已死处理，避免"矿工与工厂同 tick 死亡"输掉 ti | 可复算-原文数字 |
| `maze-crawler` | 终局规则 | 工厂相撞或一方被卷出；**相撞由存活机器人总能量决定**；多数强队选择"攒能量等 500 步后的 tiebreak" | 可复算-原文数字 |
| `maze-crawler` | 1st 三层结构 | ① 移动：first-move BFS，对每个可达格打分的**单一评分函数**（jump-aware）；② 经济：`node > bfs` 采矿（矿工 TRANSFORM 成矿、工厂坐矿收能）+ 低 sbd 转 worker 保命；③ 战斗 | 未分级 |
| `maze-crawler` | 1st 关键常数 | `MINER_PHASE_END=350`、`MIN_NODE_SBD=30`、**`ENERGY_CAP=3000`（一次性锁存：到 3000 后永久停止采矿转为猎杀）**、`WORKER_PHASE_START=400`、`SCOUT_ | 可复算-原文数字 |
| `maze-crawler` | 最终排名 | **1 Maksim Savelev 2006.5 > 2 bunterrrr 1953.4 > 3 Genematon 1796.4**；1st 估计对 bunterrrr 约 53/47，且 rating 变化 ±5 不对称收敛慢 | 可复算-图证 |

### T33 规则型 vs RL
| 场次 | 断言 | 数字 | 证据类型 |
| --- | --- | --- | --- |
| `kore-2022-beta` | 社区反思（11 票） | 读官方 notebook 起步；尝试 Q-learning **完全没打出成绩**，最终高分主要来自"改官方示例"；RL 的难点包括**延迟奖励**（船返航后 kore 才变化，奖励要回溯到早前动作） | 可复算-官方 |
| `lux-ai-season-2-neurips-stage-2` | 社区设施 | 上手资源帖 16 票（官方教程 + Lux S2 前 10 方案 + Lux 2021/Kore/Hungry Geese）；Parametrix.ai 的 PPO 基线 + 往季 episode 下载；第三方统计站（score growt | 可复算-官方 |
| `kore-2022-beta` | 1st（规则型，58 票 / 24 评论） | 七个顺序模块：① 船坞防御（算清"现有+在途"后补最小兵，必要时从最近船坞调兵）② 船坞进攻（算清夺取所需兵力）③ 直接攻击（拦截敌方舰队，路线避开敌线）④ **相邻攻击**（牺牲己方舰队换取对敌 2–3 倍伤害）⑤ 扩张（kore 盈余且 | 可复算-原文数字 |
| `kore-2022-beta` | DQN 基线（tf.js） | 输入 **2×8**（player/enemies 分组；kore、船数（总/外/内）、船坞数、早/中/晚标志，部分 log2）；输出 4 个动作（DO_NOTHING/MINE/BUILD_SHIP/BUILD_SHIPYARD）交给规则 | 可复算-原文数字 |
| `maze-crawler` | 最终排名 | **1 Maksim Savelev 2006.5 > 2 bunterrrr 1953.4 > 3 Genematon 1796.4**；1st 估计对 bunterrrr 约 53/47，且 rating 变化 ±5 不对称收敛慢 | 可复算-图证 |

### T34 LLM 加速器 vs 风险源
| 场次 | 断言 | 数字 | 证据类型 |
| --- | --- | --- | --- |
| `openai-gpt-oss-20b-red-teaming` | 官方主要发现 | ① CoT 可被伪造/欺骗（用户轮塞入伪造 CoT；有的靠 Harmony 格式细节，有的靠语义模仿）② 工具与 Harmony 通道漏洞（主通道拒绝但工具通道执行；虚构 channel；用工具建立"权威"）③ **大量问题在 `reaso | 可复算-官方 |
| `maze-crawler` | 最终排名 | **1 Maksim Savelev 2006.5 > 2 bunterrrr 1953.4 > 3 Genematon 1796.4**；1st 估计对 bunterrrr 约 53/47，且 rating 变化 ±5 不对称收敛慢 | 可复算-图证 |
| `maze-crawler` | 1st 关键常数 | `MINER_PHASE_END=350`、`MIN_NODE_SBD=30`、**`ENERGY_CAP=3000`（一次性锁存：到 3000 后永久停止采矿转为猎杀）**、`WORKER_PHASE_START=400`、`SCOUT_ | 可复算-原文数字 |
| `openai-gpt-oss-20b-red-teaming` | 社区产物 | 攻击方法分层分类（Prompt Injection / Social Engineering / CoT Manipulation / Covert Channels / Reward Hacking / Deceptive Alignme | 可复算-原文数字 |
| `openai-to-z-challenge` | 成本争议（最高热帖） | "Who is paying for API?" **48 票 / 23 评论**；"Can this competition have a low entry barrier?" 35 票 / 14 评论；"paywall feels o | 可复算-原文数字 |

### T35 API 成本 vs 额度/自部署
| 场次 | 断言 | 数字 | 证据类型 |
| --- | --- | --- | --- |
| `openai-to-z-challenge` | 成本争议（最高热帖） | "Who is paying for API?" **48 票 / 23 评论**；"Can this competition have a low entry barrier?" 35 票 / 14 评论；"paywall feels o | 可复算-原文数字 |
| `autonomous-agent-prediction-beta` | 预算讨论 | "LLM 预算只有 $2？"（11 票）；能否用 Kaggle Benchmarks 额度加预算；超预算怎么办；每 session 60 分钟 | 可复算-原文数字 |
| `autonomous-agent-prediction-beta` | 官方失败清单（9 票 / 11 评论） | ① 多工具只支持全是 search 工具（gemini-2.5-* 仅单工具；deepseek-r1-0528 不支持工具）② skill 名必须 lowercase kebab-case ③ agent 没交有效预测（思考死循环烧 tok | 可复算-官方 |
| `bigquery-ai-hackathon` | 云额度 | 新用户 90 天 **$300** 试用 + BigQuery 免费层 + 填表再给的 **$50** 额度（每周发放、先到先得）+ 无信用卡者可领多个 **$5 instrumentless credits** | 可复算-原文数字 |
| `llm-prompting-with-makersuite` | 评审规模 | 官方评估 **200+ 份提交**，选出 **7 个类别各 1 名获奖**（Developer Tools / Data Science Tools / Education & Interactive Tutors / Utilities  | 可复算-官方 |

### T36 评审透明度 vs 自包含
| 场次 | 断言 | 数字 | 证据类型 |
| --- | --- | --- | --- |
| `med-gemma-impact-challenge` | 评审透明度 | 落选者请求"分项评分或 rubric"（3 票 / 8 评论）；官方未承诺公开 | 可复算-官方 |
| `med-gemma-impact-challenge` | 部署坑 | "MedGemma 27B Deployment Challenges"（5 票 / 11 评论）；"Hosting MedGemma on VertexAI seems Broken"（3 票）+"VertexAI is still Br | 可复算-官方 |
| `pokemon-tcg-ai-battle-challenge-strategy` | 高分特征（官方总结） | ① 用自建评测（self-play arena、对冻结对手的联赛、固定对手评测集）驱动迭代，并说清"分析后改了什么"② 展示组件贡献（通用 vs 专用策略、有/无搜索、两副牌对比、rating/胜率随时间）③ 讨论失败的尝试（端到端组牌、联 | 可复算-官方 |
| `bigquery-ai-hackathon` | 评审流程（硬门槛） | 每份**人工阅读**并多次评估；按 rubric 权重，**缺多个 artifact 的直接过滤**；**必须使用三大类之一**（无 BigQuery AI 则过滤）；**公开可访问**是要求；每个获奖提交都被评委**实际复现/验证**（必 | 未分级 |
| `bigquery-ai-hackathon` | 奖项 | 三类各 1 名"Best in X"+前三：GenAI（TriLink / AI Patent Analyst / ESG Reports Agent）、Vector Search（SpeakAura AI / ReDrugAI / Cau | 可复算-原文数字 |

### T37 窄分带 vs 噪声
| 场次 | 断言 | 数字 | 证据类型 |
| --- | --- | --- | --- |
| `playground-series-s3e25` | 样本权重（74 票 / 35 评论） | 论证：若 10001 个样本里 5000 个误差 ≤0.4、其余 5000 个误差千万，分数仍是 0.4；因此只管"可能成为中位数"的样本。实现：对 `AE ≤ 0.06` 或 `≥ 0.7` 的样本给 **0.01 权重**，同一 LGB | 可复算-原文数字 |
| `playground-series-s5e9` | 领先者悬念 | 作者 3 周未参赛，发现一个**未选用**的提交 private **26.40277** / public **26.38692**，"会大幅击败当前第一"；截图见 609999 | 可复算-原文数字 |
| `playground-series-s3e25` | 数据分箱（54 票 / 42 评论） | 9 个档位（1.75/2.55/3.75/4.75/5.75/6.55/7.75/8.75/9.75）：**9533 个样本在 ±0.25 内、873 个在外（89.5%）**；若测试同分布，**猜对约 56% 即可 MedAE=0.25* | 可复算-原文数字 |
| `playground-series-s3e25` | 基线/分布 | LAD Stacker 基线 **LB 0.49737**；树模型（RF/GB/XGB/LGBM/HistGB 及集成）最低约 **0.49**；NN 被社区报告明显更强；**200+ 份提交卡在 0.25** | 可复算-原文数字 |
| `playground-series-s5e9` | 26th（610264） | 54 特征（XGB/LGB/Cat 重要性 + permutation + SHAP）；**18 个模型**（6 XGB-Optuna、4 LGBM、3 HistGBR、2 YDF、Ridge、ElasticNet、NN）；从测试残差取 3 | 可复算-原文数字 |

## 3. Playbook 数字锚点

### tabular
| 场次 | 断言 | 数字 | 证据类型 |
| --- | --- | --- | --- |
| `playground-series-s3e25` | 样本权重（74 票 / 35 评论） | 论证：若 10001 个样本里 5000 个误差 ≤0.4、其余 5000 个误差千万，分数仍是 0.4；因此只管"可能成为中位数"的样本。实现：对 `AE ≤ 0.06` 或 `≥ 0.7` 的样本给 **0.01 权重**，同一 LGB | 可复算-原文数字 |
| `playground-series-s3e18` | 11th（423642） | 删 `HeavyAtomMolWt` 与 `fr_COO2`（99% 与 fr_COO 相同）、删 `FpDensityMorgan1 == -666` 记录、去重 → 训练 **15824 行**；EC1 CatBoost+LGBM+XG | 可复算-原文数字 |
| `playground-series-s3e22` | 洗牌烈度 | 36 票专帖用 public-private 散点划出 **7 个区域**（region 2/6 = 公榜好私榜崩；region 3/4/5 = CV 可信者私榜反弹）；29 票"Beware of the public LB!"；"Out | 可复算-原文数字 |
| `playground-series-s3e22` | 领域文献（438620） | AI 预测需手术/存活：Decision Tree / MLP / Bayes 等，**76%（需手术）、85%（存活）**准确率；Cox 术后模型：存活率 10 天 **0.87** → 100 天 **0.82** → 600 天 ** | 可复算-原文数字 |
| `playground-series-s3e23` | 单模型 vs 集成（bar chart） | **Ensemble(HGB+RF+NY) 0.79220** > ET(leaf=100) 0.79136 > HistGB 0.79121 > Nyström-LR 0.79112 > RF(leaf=150) 0.79107 > Po | 可复算-原文数字 |
| `playground-series-s3e23` | #2 八模型集成 | 无变换基线 CV **0.793** / LB **0.790**；输入 log 变换后树模型小幅提升；6 树爬山集成 LB **0.7907**（该版本私榜 **0.79379**）→ +Nyström LR **0.79099** →  | 可复算-原文数字 |
| `playground-series-s3e8` | 8th（392860） | 先"修离群值"→ CV 大涨但 LB 变差（发现模型本来就会压缩离群）；改做**分组合法性裁剪**：按 carat 滑窗（0.15）× cut × clarity × color 分组（>5 条记录），预测超过上界 → `Q3+1.5·IQ | 可复算-原文数字 |
| `playground-series-s3e8` | 2nd（392828） | 两级栈共 **1816 个模型**（L1 1709 个 XGB/CAT/LGBM/Ridge + L2 105 个 Ridge/blend/NN）；L1 选择用"CV 阈值从 574 逐 0.1 下探"，最优 cutoff **572.6* | 可复算-原文数字 |
| `playground-series-s3e8` | 3rd（392824） | 用尽量多的特征组合；自写"逐列剔除"特征选择，并**同时盯 RMSE 与折间标准差**（容忍度：+0.015 RMSE 换 -0.01 std），把平均 std 从 4.5 降到 3.8；Optuna（1000 轮/lr 0.1）后再拉长到 | 可复算-原文数字 |
| `playground-series-s3e9` | CV vs 公开榜 | CV **5407** 样本（一次测量）vs 公开榜 **721** 样本（随机变量）；作者用 7 次提交只是好奇，主张 **≤2 次** | 可复算-原文数字 |
| `playground-series-s5e9` | 26th（610264） | 54 特征（XGB/LGB/Cat 重要性 + permutation + SHAP）；**18 个模型**（6 XGB-Optuna、4 LGBM、3 HistGBR、2 YDF、Ridge、ElasticNet、NN）；从测试残差取 3 | 可复算-原文数字 |
| `scrabble-player-rating` | CV 核心问题 | 数据中同一玩家的历史**整体落在 train 或 test**；作者从 KFold 改 **GroupKFold（nickname 分组）** 后分数"substantially worse"；**StratifiedGroupKFold* | 未分级 |
| `playground-series-s3e18` | "两场比赛"证据（图） | EC1：KNN(1180) 0.6981、LR 0.7005、ET(12) 0.7073、RF(45) 0.7087、Ensemble 0.7092；EC2：LR 0.5773、KNN(490) 0.5859、RF(80) 0.5865、E | 可复算-原文数字 |
| `playground-series-s3e18` | 清洗/异常清单 | `FpDensityMorgan1=-666`（"trains to hell"）；`fr_COO/fr_COO2` 出现 test 有 train 无的取值；`NumHeteroatoms` 40/48 两边都没有；负氢原子数；`Heav | 可复算-原文数字 |
| `playground-series-s3e23` | 数据审计线索 | 准重复观测（13 票）、完全相关特征、原始数据预处理（9 票）、"Important information regarding features"、"Sometimes more is better... well a bit bette | 可复算-原文数字 |

### cv
| 场次 | 断言 | 数字 | 证据类型 |
| --- | --- | --- | --- |
| `iwildcam2022-fgvc9` | 1st（不训练） | 基于 MegaDetector 检测过滤；观察"阈值 0.95 会**高密度图少算、低密度图多算**"，以**每图 8 个预测**为界分两类：高密度图用**置信度 0.0 + NMS(IoU=0.2) + 抑制小框**（public 0.2 | 可复算-图证 |
| `geolifeclef-2022-lifeclef-2022-fgvc9` | 1st 集成 | ① ResNet34 双模态（NIR+G+B）+ 3 层 FCN（环境向量 + lat/lon + country + 海拔均值/极差 + landcover "dothot" 编码）→ 17k 分类层；② MobileNetV3-larg | 可复算-原文数字 |
| `geolifeclef-2022-lifeclef-2022-fgvc9` | 2nd 单模配方 | 两条不共享参数的 CNN 分支：RGB；海拔+NIR+NDVI → concat → **dropout 0.45** → 17,034 类 softmax CE；Inception-v4 比 ResNet-50 约 **+2%**；Ima | 可复算-原文数字 |
| `herbarium-2022-fgvc9` | 1st 单模消融（private） | Swin-B224 基线 **0.78442** → +多级 CE（family/genus/species）**0.79544** → LR 2e-4→5e-4 **0.80501** → +5crop **0.80981** → sub | 可复算-原文数字 |
| `hotel-id-to-combat-human-trafficking-2022-fgvc9` | 2nd（328345） | 50K+FGVC9；按 **md5 去重**（同 md5 不同类别删除）后保留 **45,769 个类别**；方向模型把图旋正；先全量 10–20 epoch，再对 FGVC9 的 **3116 类微调 40 epoch（+0.03）**； | 可复算-原文数字 |
| `iwildcam2022-fgvc9` | 9th（重工程） | MegaDetector v4 检测 → 训练 **YOLOv5** 第二检测器 → **WBF 加权框融合**（public/private **0.275/0.265**，高于 2021 冠军基线）→ 对 8 类群居物种（白唇西貒 2、 | 可复算-原文数字 |
| `planttraits2024` | 1st（PlantHydra） | 三头：回归头（归一化性状）+ 分类头（**17,396 个"物种"**）+ 软分类头（按 softmax 权重对物种性状加权求和），三头权重可训练；DINOv2 ViT-b/l + **PlantCLEF 2024 西南欧植物预训练**；元 | 可复算-原文数字 |
| `planttraits2024` | 6th（AutoGluon） | TIMM 图像特征 + 表格特征 → Transformer 融合（略优于 MLP）；**标签链**（按论文 R² 顺序逐个预测）；EVA 系列最强：`eva_large_patch14_336` private **0.483**、`ev | 可复算-原文数字 |
| `planttraits2024` | 赛事事故 | 有选手用 `sample_submission.csv` 提分 → 官方**更新测试集（图片+test.csv）并重置 LB**；`sample_submission.csv` 在新测试集上从正分变成 **-33.38** | 可复算-官方 |
| `sorghum-id-fgvc-9` | 3rd（328593） | 消融表：base（resnet50@512）0.73 → 直方图均衡 +0.03 → **IBN-ResNet +0.05** → bnn-neck +0.005 → 最后卷积 stride=1 +0.005 → **ArcFace(s=3 | 可复算-原文数字 |
| `fathomnet-out-of-sample-detection` | 4th 训练 | EfficientNetV2B0（ImageNet 预训练）+ 128 维 Dense + 输出层；输出层按正负样本不均衡初始化；两阶段微调（先冻结 base，再解冻 2 个顶层）；**label smoothing 0.1** 在噪声标签 | 可复算-原文数字 |
| `fathomnet-out-of-sample-detection` | 评测问题 | metric 的 **AUC 部分有 bug**，官方修复后重新计分；另有 MAP@20 与评测代码不一致、评测报错、null 提交等帖 | 可复算-官方 |
| `fathomnet-out-of-sample-detection` | 上手门槛 | 图片需从源站下载且慢；官方 `download_images.py` 参数报错；submit 格式/规则（额外数据集）问题多 | 可复算-官方 |
| `geolifeclef-2022-lifeclef-2022-fgvc9` | 无效尝试 | 2nd：环境协变量与 GPS 直接入 CNN（坐标 MLP 各种编码都欠拟合）、taxonomy 辅助任务、直方图密度预测、长尾专门处理（**"什么都不做"最好**，因为测试集同样长尾）；1st：多标签聚合、其他骨干、无迁移学习、三骨干分工 | 可复算-原文数字 |
| `herbarium-2022-fgvc9` | 骨干对比（private） | swinv2-B 0.86282 > swin-B 0.86055 > convnext-B 0.85956 > swin-L 0.85607 > cswin-L 0.8501 > deit-iii B 0.8495 > efficient | 可复算-原文数字 |

### nlp
| 场次 | 断言 | 数字 | 证据类型 |
| --- | --- | --- | --- |
| `autonomous-agent-prediction-beta` | 官方失败清单（9 票 / 11 评论） | ① 多工具只支持全是 search 工具（gemini-2.5-* 仅单工具；deepseek-r1-0528 不支持工具）② skill 名必须 lowercase kebab-case ③ agent 没交有效预测（思考死循环烧 tok | 可复算-官方 |
| `llm-prompting-with-makersuite` | 评审规模 | 官方评估 **200+ 份提交**，选出 **7 个类别各 1 名获奖**（Developer Tools / Data Science Tools / Education & Interactive Tutors / Utilities  | 可复算-官方 |
| `openai-gpt-oss-20b-red-teaming` | 官方主要发现 | ① CoT 可被伪造/欺骗（用户轮塞入伪造 CoT；有的靠 Harmony 格式细节，有的靠语义模仿）② 工具与 Harmony 通道漏洞（主通道拒绝但工具通道执行；虚构 channel；用工具建立"权威"）③ **大量问题在 `reaso | 可复算-官方 |
| `autonomous-agent-prediction-beta` | 社区技巧/坑 | LB 0.823 模板（利用 "freeroll" fallback 规则 + Gemini Pro，2 票）；`select_submission` 实测收益上限 +0.0005、最差 −0.0166（0 票 / 5 评论）；本地评测 ` | 可复算-原文数字 |
| `openai-gpt-oss-20b-red-teaming` | 社区产物 | 攻击方法分层分类（Prompt Injection / Social Engineering / CoT Manipulation / Covert Channels / Reward Hacking / Deceptive Alignme | 可复算-原文数字 |
| `wikipedia-image-caption` | 论文/实现（14 票） | awesome-image-captioning 仓库；Compositional Neural Module Networks、CapWAP、Scene Graph、Diverse Captioning 等；PyTorch ImageCa | 可复算-原文数字 |
| `autonomous-agent-prediction-beta` | 系列化 | 官方奖品描述暗示系列赛（每人只发一次周边）；"会是月度系列吗"（10 票 / 4 评论） | 可复算-官方 |
| `gemini-long-context` | 配额与限流 | 免费额度（9 票 / 30 评论）、quota 提升、**429 ResourceExhausted**（多帖）、**503/504 超时 600s**、Vertex 视频 502/503/429、context caching 403—— | 可复算-原文数字 |
| `gemini-long-context` | 社区争议 | "The Illusion of Merit: Unmasking the Voting Manipulation on Kaggle"（8 票 / 5 评论）；非确定性 notebook 结果讨论（2 票 / 5 评论）；"Kaggle  | 可复算-原文数字 |
| `gemma-language-tuning` | 官方适配样板 | Gemma Developer Day Tokyo 发布"如何让 Gemma 2 更擅长日语"的视频——教其他语言适配的参考 | 可复算-官方 |
| `kaggle-measuring-agi` | 奖池 | **Grand Prizes $25k × 4**（MEDLEY-BENCH / LearningBench / GAUGE / Metaproteus）+ **Track Prizes $10k × 10**（每赛道 2 个）= **$2 | 可复算-原文数字 |
| `kaggle-measuring-agi` | 提交硬门槛 | "Action needed if your dataset is private" **66 评论**；"Important submission info" 37 评论；"Unable to submit my writeup"、"I  | 可复算-原文数字 |
| `kaggle-measuring-agi` | 冠军发现样例 | GAUGE：某前沿模型 270 题里**一次都不弃权**（monitoring 有、control 无）；EphLangBench：10 模型 × 200 题的临时语言通过率 **7%–89%**；ABC：15 模型 × 2160 例显示选 | 可复算-原文数字 |
| `llm-prompting-with-makersuite` | 获奖范式 | 开发工具类 @ajaysadhu：**system prompt + 多组"乱格式输入→规范 YAML 输出"示例**，多次测试证明稳定；教育类 @hoangpham51：输出 **JSON + answer matrix + 示例答案** | 可复算-原文数字 |
| `llm-prompting-with-makersuite` | 社区副产物 | MPWolke 的"Kaggle 游戏/模拟赛巡礼"长帖（ConnectX / Halite / Kore / Lux AI / AI Village CTF 等，14 票）成为错位选题的示范：MakerSuite 不可用时改讲"agent | 可复算-原文数字 |

### science
| 场次 | 断言 | 数字 | 证据类型 |
| --- | --- | --- | --- |
| `med-gemma-impact-challenge` | 部署坑 | "MedGemma 27B Deployment Challenges"（5 票 / 11 评论）；"Hosting MedGemma on VertexAI seems Broken"（3 票）+"VertexAI is still Br | 可复算-官方 |
| `geolifeclef-2024` | 数据访问 | PA 数据在 Kaggle；**原始栅格在 Seafile**，需分组下载 zip；官方建议 `python download.py --data output --raster --presence-only --all-variable | 可复算-官方 |
| `geolifeclef-2022-lifeclef-2022-fgvc9` | 1st 集成 | ① ResNet34 双模态（NIR+G+B）+ 3 层 FCN（环境向量 + lat/lon + country + 海拔均值/极差 + landcover "dothot" 编码）→ 17k 分类层；② MobileNetV3-larg | 可复算-原文数字 |
| `geolifeclef-2022-lifeclef-2022-fgvc9` | 2nd 单模配方 | 两条不共享参数的 CNN 分支：RGB；海拔+NIR+NDVI → concat → **dropout 0.45** → 17,034 类 softmax CE；Inception-v4 比 ResNet-50 约 **+2%**；Ima | 可复算-原文数字 |
| `med-gemma-impact-challenge` | HAI-DEF 模型族 | CXR Foundation（3 个 EfficientNet-L2 编码器，图像+放射报告）；Path Foundation（病理 patch 的 ViT 自监督）；Derm Foundation（BiT ResNet-101x3，16K | 可复算-原文数字 |
| `planttraits2024` | 1st（PlantHydra） | 三头：回归头（归一化性状）+ 分类头（**17,396 个"物种"**）+ 软分类头（按 softmax 权重对物种性状加权求和），三头权重可训练；DINOv2 ViT-b/l + **PlantCLEF 2024 西南欧植物预训练**；元 | 可复算-原文数字 |
| `planttraits2024` | 6th（AutoGluon） | TIMM 图像特征 + 表格特征 → Transformer 融合（略优于 MLP）；**标签链**（按论文 R² 顺序逐个预测）；EVA 系列最强：`eva_large_patch14_336` private **0.483**、`ev | 可复算-原文数字 |
| `planttraits2024` | 赛事事故 | 有选手用 `sample_submission.csv` 提分 → 官方**更新测试集（图片+test.csv）并重置 LB**；`sample_submission.csv` 在新测试集上从正分变成 **-33.38** | 可复算-官方 |
| `geolifeclef-2022-lifeclef-2022-fgvc9` | 无效尝试 | 2nd：环境协变量与 GPS 直接入 CNN（坐标 MLP 各种编码都欠拟合）、taxonomy 辅助任务、直方图密度预测、长尾专门处理（**"什么都不做"最好**，因为测试集同样长尾）；1st：多标签聚合、其他骨干、无迁移学习、三骨干分工 | 可复算-原文数字 |
| `geolifeclef-2024` | 周边 | FGVC11 其他 Kaggle 赛（数据格式相近，可多赛复用）；官方 Discord；CLEF 2025 是否会继续（9 评论） | 可复算-官方 |
| `med-gemma-impact-challenge` | HAI-DEF 局限（官方） | 面向**分类**任务；预后任务待评估；**不支持分割与生成**；端侧/低延迟需蒸馏 | 可复算-官方 |
| `phase-ii-widsdatathon2022` | 常见问题 | `alt_prec` 含义（313830）；MIT starter dataset 疑问（312012）；CCAI 缺 `parsing-e-obs.ipynb`（313736）；页数限制（334287）；能否用 Tableau（32166 | 可复算-原文数字 |
| `planttraits2024` | 9th（DINOv2+CatBoost） | DINOv2 [giant] embedding + 表格 → **CatBoost 原生处理 embedding**（含降维）；public **0.51162** / private **0.51238**；2 阶多项式特征小增益；** | 可复算-原文数字 |
| `geolifeclef-2022-lifeclef-2022-fgvc9` | 学术交付 | CLEF working note **强制**：6/1 截止，轻审后 6/13 反馈、7/1 终稿；收入 CEUR-WS 并分配 DOI；**无法复现的 run 可能从正式结果中移除** | 可复算-原文数字 |
| `geolifeclef-2024` | working note 时间线 | 竞赛 5/24 截止 → **6/7 论文截稿** → 6/21 录取通知 → 7/8 camera-ready；CEUR-WS 出版，择优进 Springer LNCS，最佳论文获 CLEF 注册费 | 可复算-原文数字 |

### sim-agent
| 场次 | 断言 | 数字 | 证据类型 |
| --- | --- | --- | --- |
| `autonomous-agent-prediction-beta` | 官方失败清单（9 票 / 11 评论） | ① 多工具只支持全是 search 工具（gemini-2.5-* 仅单工具；deepseek-r1-0528 不支持工具）② skill 名必须 lowercase kebab-case ③ agent 没交有效预测（思考死循环烧 tok | 可复算-官方 |
| `maze-crawler` | 最终排名 | **1 Maksim Savelev 2006.5 > 2 bunterrrr 1953.4 > 3 Genematon 1796.4**；1st 估计对 bunterrrr 约 53/47，且 rating 变化 ±5 不对称收敛慢 | 可复算-图证 |
| `pokemon-tcg-ai-battle-challenge-strategy` | 高分特征（官方总结） | ① 用自建评测（self-play arena、对冻结对手的联赛、固定对手评测集）驱动迭代，并说清"分析后改了什么"② 展示组件贡献（通用 vs 专用策略、有/无搜索、两副牌对比、rating/胜率随时间）③ 讨论失败的尝试（端到端组牌、联 | 可复算-官方 |
| `lux-ai-season-2-neurips-stage-2` | 奖励与稳定性 | generation/resources 各统计量除以 **5M 步窗口的 EMA 标准差** + WinLoss(+1/-1/0)；通过改奖励权重即可切换策略（32/64 更奖励 ore/metal/机器人）；32×32 KL **>0. | 可复算-图证 |
| `lux-ai-season-2-neurips-stage-2` | 社区设施 | 上手资源帖 16 票（官方教程 + Lux S2 前 10 方案 + Lux 2021/Kore/Hungry Geese）；Parametrix.ai 的 PPO 基线 + 往季 episode 下载；第三方统计站（score growt | 可复算-官方 |
| `autonomous-agent-prediction-beta` | 社区技巧/坑 | LB 0.823 模板（利用 "freeroll" fallback 规则 + Gemini Pro，2 票）；`select_submission` 实测收益上限 +0.0005、最差 −0.0166（0 票 / 5 评论）；本地评测 ` | 可复算-原文数字 |
| `kore-2022-beta` | 1st（规则型，58 票 / 24 评论） | 七个顺序模块：① 船坞防御（算清"现有+在途"后补最小兵，必要时从最近船坞调兵）② 船坞进攻（算清夺取所需兵力）③ 直接攻击（拦截敌方舰队，路线避开敌线）④ **相邻攻击**（牺牲己方舰队换取对敌 2–3 倍伤害）⑤ 扩张（kore 盈余且 | 可复算-原文数字 |
| `kore-2022-beta` | DQN 基线（tf.js） | 输入 **2×8**（player/enemies 分组；kore、船数（总/外/内）、船坞数、早/中/晚标志，部分 log2）；输出 4 个动作（DO_NOTHING/MINE/BUILD_SHIP/BUILD_SHIPYARD）交给规则 | 可复算-原文数字 |
| `kore-2022-beta` | 社区反思（11 票） | 读官方 notebook 起步；尝试 Q-learning **完全没打出成绩**，最终高分主要来自"改官方示例"；RL 的难点包括**延迟奖励**（船返航后 kore 才变化，奖励要回溯到早前动作） | 可复算-官方 |
| `kore-2022-beta` | 平台问题 | 同舰队/合并/船坞碰撞结算不符合直觉（315895）；最大航程修复（313989）；新导弹防御（316848）；kore 分布非随机（316092）；spawn 公式疑问；可视化碰撞 bug；**50 队只有 1 个公开 notebook* | 可复算-官方 |
| `lux-ai-season-2-neurips-stage-2` | 模型 | DoubleCone 风格 + 额外 4× 下采样（感受野到 64×64）；**4,719,403 参数**；value 输出 14；policy 每位置 29 个 logit（24 单位 + 4 工厂 + 1 放置）；动作类型/子动作按独 | 可复算-图证 |
| `maze-crawler` | 1st 关键常数 | `MINER_PHASE_END=350`、`MIN_NODE_SBD=30`、**`ENERGY_CAP=3000`（一次性锁存：到 3000 后永久停止采矿转为猎杀）**、`WORKER_PHASE_START=400`、`SCOUT_ | 可复算-原文数字 |
| `pokemon-tcg-ai-battle-challenge-strategy` | 资格摩擦 | Simulation 报名截止 **2026-08-09 23:59 UTC**；多帖反映 write-up 完成后无法进入 Simulation（735276 / 734869 / 735402 / 735996 / 740873 / 7 | 可复算-原文数字 |
| `autonomous-agent-prediction-beta` | 系列化 | 官方奖品描述暗示系列赛（每人只发一次周边）；"会是月度系列吗"（10 票 / 4 评论） | 可复算-官方 |
| `kore-2022-beta` | 定位与规模 | **58 队**；beta 预览，**无现金/积分/奖牌**；4p → 2p（官方中途调整）并延期一周 | 可复算-官方 |

### multimodal
| 场次 | 断言 | 数字 | 证据类型 |
| --- | --- | --- | --- |
| `med-gemma-impact-challenge` | 部署坑 | "MedGemma 27B Deployment Challenges"（5 票 / 11 评论）；"Hosting MedGemma on VertexAI seems Broken"（3 票）+"VertexAI is still Br | 可复算-官方 |
| `openai-gpt-oss-20b-red-teaming` | 官方主要发现 | ① CoT 可被伪造/欺骗（用户轮塞入伪造 CoT；有的靠 Harmony 格式细节，有的靠语义模仿）② 工具与 Harmony 通道漏洞（主通道拒绝但工具通道执行；虚构 channel；用工具建立"权威"）③ **大量问题在 `reaso | 可复算-官方 |
| `geolifeclef-2024` | 数据访问 | PA 数据在 Kaggle；**原始栅格在 Seafile**，需分组下载 zip；官方建议 `python download.py --data output --raster --presence-only --all-variable | 可复算-官方 |
| `med-gemma-impact-challenge` | HAI-DEF 模型族 | CXR Foundation（3 个 EfficientNet-L2 编码器，图像+放射报告）；Path Foundation（病理 patch 的 ViT 自监督）；Derm Foundation（BiT ResNet-101x3，16K | 可复算-原文数字 |
| `openai-gpt-oss-20b-red-teaming` | 社区产物 | 攻击方法分层分类（Prompt Injection / Social Engineering / CoT Manipulation / Covert Channels / Reward Hacking / Deceptive Alignme | 可复算-原文数字 |
| `planttraits2024` | 1st（PlantHydra） | 三头：回归头（归一化性状）+ 分类头（**17,396 个"物种"**）+ 软分类头（按 softmax 权重对物种性状加权求和），三头权重可训练；DINOv2 ViT-b/l + **PlantCLEF 2024 西南欧植物预训练**；元 | 可复算-原文数字 |
| `planttraits2024` | 6th（AutoGluon） | TIMM 图像特征 + 表格特征 → Transformer 融合（略优于 MLP）；**标签链**（按论文 R² 顺序逐个预测）；EVA 系列最强：`eva_large_patch14_336` private **0.483**、`ev | 可复算-原文数字 |
| `planttraits2024` | 赛事事故 | 有选手用 `sample_submission.csv` 提分 → 官方**更新测试集（图片+test.csv）并重置 LB**；`sample_submission.csv` 在新测试集上从正分变成 **-33.38** | 可复算-官方 |
| `data-assistants-with-gemma` | 中期获奖配方 ① | @jacoporepossi《Text Summarization with Gemma》：**Transformers gemma-2b-it + LangChain**（Stuffing / MapReduce / Refine 管线） | 可复算-原文数字 |
| `data-assistants-with-gemma` | 中期获奖配方 ③ | @lucamassaron《Data Science AI Assistant with Gemma 2b-it》：**从零手写 RAG**（`generate_summary_and_answer()`，Wikipedia API 造数据 | 可复算-原文数字 |
| `data-assistants-with-gemma` | 中期获奖配方 ⑤ | @inoueu1《Make A Smart Python Assistant with Gemma》：在 **Magicoder 数据集**上训 LoRA，用 **CODAL-Bench** 检验可执行性，与 GPT-4-Turbo / G | 可复算-原文数字 |
| `gemini-long-context` | 配额与限流 | 免费额度（9 票 / 30 评论）、quota 提升、**429 ResourceExhausted**（多帖）、**503/504 超时 600s**、Vertex 视频 502/503/429、context caching 403—— | 可复算-原文数字 |
| `gemini-long-context` | 社区争议 | "The Illusion of Merit: Unmasking the Voting Manipulation on Kaggle"（8 票 / 5 评论）；非确定性 notebook 结果讨论（2 票 / 5 评论）；"Kaggle  | 可复算-原文数字 |
| `geolifeclef-2024` | 周边 | FGVC11 其他 Kaggle 赛（数据格式相近，可多赛复用）；官方 Discord；CLEF 2025 是否会继续（9 评论） | 可复算-官方 |
| `med-gemma-impact-challenge` | HAI-DEF 局限（官方） | 面向**分类**任务；预后任务待评估；**不支持分割与生成**；端侧/低延迟需蒸馏 | 可复算-官方 |
