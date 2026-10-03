# Tier A 深读名单（60 场，冻结 v1）

> 选取规则：材料密度（正文数/方案帖数/机制帖数/图片数）× 系列重要性 × 主题平衡。
> 计分明细见 `analysis/_tier_a_scored.csv`（票数项已封顶）。
> 状态：⬜ 未开始 ｜ 🔄 进行中 ｜ ✅ 完成（深读 + 笔记回写 + 图证内嵌）
> 进度：Batch 1–4 ✅ 40/40 ｜ Batch 5 🔄 5/10 ｜ 总计 **45/60**（2026-10-03）

## 批次 1（10）

| # | slug | 主题 | 为什么选它 | 状态 |
| --- | --- | --- | --- | --- |
| 1 | `tabular-playground-series-nov-2022` | tabular | 机制标杆：输入是预测；−1.17→w≈3.2（示范已完成） | ✅ |
| 2 | `tabular-playground-series-feb-2022` | tabular | 随机数生成缺陷泄漏；重复样本；评估口径修正 | ✅ |
| 3 | `playground-series-s5e12` | tabular | 刻意破坏数据 + ID 泄漏 + concept shift + post-cutoff CV | ✅ |
| 4 | `amex-default-prediction` | tabular | 金融大场；清洗优先；蒸馏+半监督 | ✅ |
| 5 | `optiver-realized-volatility-prediction` | tabular | 消融思维 + 时间序逆向 + 近邻特征 | ✅ |
| 6 | `jigsaw-toxic-severity-rating` | nlp | Union-Find 防泄漏；排序一致性；私榜泄漏悖论 | ✅ |
| 7 | `petfinder-pawpularity-score` | cv | 增强配方；元数据辅助任务；SVR 头部特征 | ✅ |
| 8 | `rogii-wellbore-geology-prediction` | science | 物理混合 + 问题重构 + 大洗牌 | ✅ |
| 9 | `orbit-wars` | sim-agent | 推理预算决定方法；联盟自对弈 | ✅ |
| 10 | `hms-harmful-brain-activity-classification` | tabular | 弱标注信号→频谱→视觉模型；校准；标签来源双位移 | ✅ |

## 批次 2（10）

| # | slug | 主题 | 为什么选它 | 状态 |
| --- | --- | --- | --- | --- |
| 11 | `lmsys-chatbot-arena` | nlp | 人类偏好建模；LoRA/QLoRA 平民化 | ✅ |
| 12 | `feedback-prize-2021` | nlp | 跨度任务；WBF 跨域迁移 | ✅ |
| 13 | `feedback-prize-english-language-learning` | nlp | 多目标回归；爬山权重 | ✅ |
| 14 | `otto-recommender-system` | tabular | 召回-排序；共现规则进前三 | ✅ |
| 15 | `h-and-m-personalized-fashion-recommendations` | tabular | 推荐系统工业范本；时间切分 | ✅ |
| 16 | `ubiquant-market-prediction` | tabular | 缺失即信息；时间衰减 | ✅ |
| 17 | `rsna-breast-cancer-detection` | cv | 患者级分组底线；分阶段分辨率 | ✅ |
| 18 | `vesuvius-challenge-ink-detection` | cv | 大切块+上下文；几何增强对齐 | ✅ |
| 19 | `ventilator-pressure-prediction` | science | 控制逻辑覆盖 66%；ML 补残差 | ✅ |
| 20 | `santa-2025` | sim-agent | 全局+局部双层搜索；性能工程换分 | ✅ |

## 批次 3（10）

| # | slug | 主题 | 为什么选它 | 状态 |
| --- | --- | --- | --- | --- |
| 21 | `map-charting-student-math-misunderstandings` | nlp | 提示结构工程；量化+LoRA | ✅ |
| 22 | `llm-detect-ai-generated-text` | nlp | CV-LB 背离时转扩数据多样性 | ✅ |
| 23 | `llm-prompt-recovery` | nlp | 指标套利边界；均值基线 | ✅ |
| 24 | `jigsaw-agile-community-rules` | nlp | 规则测试期出现→TTT/在线蒸馏 | ✅ |
| 25 | `ai-agent-security-multi-step-tool-attacks` | nlp | 隐藏评分器；能测的测准 | ✅ |
| 26 | `child-mind-institute-detect-sleep-states` | tabular | 下采样→模型→上采样；事件级后处理 | ✅ |
| 27 | `child-mind-institute-problematic-internet-use` | tabular | 序数标签再离散化；高方差稳健 | ✅ |
| 28 | `cmi-detect-behavior-with-sensor-data` | tabular | 多模态传感器；缺失模式分模型 | ✅ |
| 29 | `predict-student-performance-from-game-play` | tabular | CV 噪声量化成特征准入门槛 | ✅ |
| 30 | `godaddy-microbusiness-density-forecasting` | tabular | 倍率建模；数据质量审计 | ✅ |

## 批次 4（10）

| # | slug | 主题 | 为什么选它 | 状态 |
| --- | --- | --- | --- | --- |
| 31 | `isic-2024-challenge` | cv | pAUC 优化；图像+元数据双线 | ✅ |
| 32 | `hubmap-hacking-the-human-vasculature` | cv | 标注噪声；细管损失 | ✅ |
| 33 | `rsna-2024-lumbar-spine-degenerative-classification` | cv | 定位→分类；每条件子模型（已做图证样板） | ✅ |
| 34 | `rsna-2022-cervical-spine-fracture-detection` | cv | 两阶段+分割辅助 | ✅ |
| 35 | `uw-madison-gi-tract-image-segmentation` | cv | 部分标注 masked loss | ✅ |
| 36 | `open-problems-multimodal` | science | IR 方法迁移到单细胞 | ✅ |
| 37 | `open-problems-single-cell-perturbations` | science | 度量学习/对抗验证 | ✅ |
| 38 | `neurips-open-polymer-prediction-2025` | science | 外部数据偏移 20°C；伪标签预训练 | ✅ |
| 39 | `stanford-ribonanza-rna-folding` | science | 结构相似度指标 | ✅ |
| 40 | `waveform-inversion` | science | 物理约束 + 领域解释帖 | ✅ |

## 批次 5（10）

| # | slug | 主题 | 为什么选它 | 状态 |
| --- | --- | --- | --- | --- |
| 41 | `ariel-data-challenge-2024` | science | 贝叶斯两年连胜；规模工程 | ✅ |
| 42 | `leap-atmospheric-physics-ai-climsim` | science | 算力-收益对照表 | ✅ |
| 43 | `g2net-detecting-continuous-gravitational-waves` | science | 经典匹配滤波 vs ML | ✅ |
| 44 | `deep-past-initiative-machine-translation` | nlp | 语料工程；ByT5 零结构改动 | ✅ |
| 45 | `kaggle-llm-science-exam` | nlp | 检索侧>模型侧 | ✅ |
| 46 | `commonlit-evaluate-student-summaries` | nlp | 来源分组验证 | ⬜ |
| 47 | `eedi-mining-misconceptions-in-mathematics` | nlp | 大标签空间→检索重排 | ⬜ |
| 48 | `nvidia-nemotron-model-reasoning-challenge` | nlp | 求解器→推理链；简单损失 | ⬜ |
| 49 | `learning-agency-lab-automated-essay-scoring-2` | nlp | 多来源拼接；QWK 阈值 | ⬜ |
| 50 | `pii-detection-removal-from-educational-data` | nlp | maxlen/stride 作为集成维度 | ⬜ |

## 批次 6（10）

| # | slug | 主题 | 为什么选它 | 状态 |
| --- | --- | --- | --- | --- |
| 51 | `birdclef-2022` | audio | 弱标签起步年的方法考古 | ⬜ |
| 52 | `birdclef-2025` | audio | 多轮伪标签流程化 | ⬜ |
| 53 | `nfl-health-and-safety-helmet-assignment` | cv | 检测→几何映射→配准三段式（已做图证样板） | 🔄 |
| 54 | `foursquare-location-matching` | tabular | 实体匹配四阶段 | ⬜ |
| 55 | `predict-energy-behavior-of-prosumers` | tabular | 在线学习机制 | ⬜ |
| 56 | `home-credit-credit-risk-model-stability` | tabular | 自定义指标拆解；分组分层 CV | ⬜ |
| 57 | `santa-2024` | sim-agent | 本地复现打分函数；k-opt/ILS/SA | ⬜ |
| 58 | `pokemon-tcg-ai-battle` | sim-agent | Pattern DB + 自对弈评估 | ⬜ |
| 59 | `ai-village-ctf` | sim-agent | 黑箱迭代搜索；节奏管理 | ⬜ |
| 60 | `tabular-playground-series-dec-2021` | tabular | 特征修复；软投票 | ⬜ |

> 名单调整原则：若某场深读发现材料不足（≤3 篇），转入"定点补采"清单并以相邻机制场替换。

## 进度小结

- Tier A 完成：**45/60**；Batch 5：#41 ariel-2024 ✅、#42 leap-climsim ✅、#43 g2net-continuous-gw ✅、#44 deep-past ✅、#45 kaggle-llm-science-exam ✅（检索侧决定上限/RAG 工程，图证 5 张）
- Batch 5 待办：#46 commonlit → #50 pii-detection（共 5 场）→ Batch 6 → Tier B 204 场 → 阶段二三
- 图证样板：kaggle-llm-science-exam（RAG 集成/缓存架构）、deep-past、g2net、ariel-2024、leap-climsim、rsna-2024、rsna-2022、uw-madison、multimodal、single-cell、polymer、ribonanza、waveform、isic-2024、hubmap、UBC-OCEAN
