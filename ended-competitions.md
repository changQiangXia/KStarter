# Kaggle 已结束比赛全景

> 数据口径：2026-10-03 通过 Kaggle 网站分页接口抓取全站比赛，共 **756 场**，其中已结束 **735 场**。
> 原始数据见 `data/competitions_all.json`，已结束比赛明细见 `data/competitions_ended.csv`，抓取脚本见 `scripts/fetch_competitions.py`。
> 近 5 年（2021-10-03 起）的完整清单与年度明细见 `last-5-years.md` / `data/competitions_last5y.csv`。

## 1. 总量与分布

| 指标 | 数值 |
| --- | --- |
| 全站比赛 | 756（已结束 735 / 进行中 21） |
| Featured | 326 |
| Research | 190 |
| Playground | 164 |
| Community | 25 |
| Recruitment | 17 |
| Getting Started | 7 |
| Masters | 6 |
| 代码赛（kernel-only 提交） | 149 / 735（20%） |
| 提供公开解法 | 651 / 735（89%） |
| 设置奖牌 | 466 / 735（63%） |
| 累计奖金 | 约 3,732 万美元 |

## 2. 年度趋势

| 年份 | 结束场次 | 其中代码赛 | 奖金总额(USD) |
| --- | --- | --- | --- |
| 2010 | 8 | 0 | 3,317 |
| 2011 | 15 | 0 | 72,050 |
| 2012 | 42 | 0 | 591,130 |
| 2013 | 46 | 0 | 1,460,050 |
| 2014 | 34 | 0 | 950,180 |
| 2015 | 44 | 0 | 898,500 |
| 2016 | 34 | 0 | 1,160,000 |
| 2017 | 39 | 0 | 3,500,000 |
| 2018 | 46 | 0 | 2,272,500 |
| 2019 | 58 | 5 | 1,310,000 |
| 2020 | 57 | 20 | 2,167,000 |
| 2021 | 59 | 22 | 1,365,500 |
| 2022 | 55 | 20 | 1,858,000 |
| 2023 | 65 | 24 | 3,258,000 |
| 2024 | 46 | 22 | 4,153,576 |
| 2025 | 48 | 21 | 7,932,152 |
| 2026 | 39 | 15 | 4,368,540 |

（2026 年为部分年度，统计截至 10-03）

观察：

- 结束场次长期稳定在每年 40–65 场，2024 年后略有下降。
- **奖金总额在 2025 年跳到 793 万美元，为历史最高**，主要由 AI 大额奖推动：AIMO Progress Prize 3（220 万）、ARC Prize 2025（100 万）、Gemini 3 hackathon（50 万）。
- 代码赛（提交 notebook、平台重跑）比例常年占总量的 1/3 左右，是必须提前识别的机制。
- Playground 已月度化：近 12 个月就有 9 场 `playground-series-s6eX`，是练手和验证流水线的主要来源。
- 2026 年大额奖金继续集中在 LLM / agent / 科研方向，传统表格赛奖金规模明显更小。

## 3. 近 12 个月结束的比赛（自 2025-10-03 起，共 50 场）

`代码赛` 列标 C 的表示只能提交 notebook（平台重跑）。

| 截止 | 比赛 | 类别 | 机制 | 队伍数 | 奖金 | 评估指标 |
| --- | --- | --- | --- | --- | --- | --- |
| 2026-09-30 | `playground-series-s6e9` | Playground | 标准 | 3575 | SWAG | Roc Auc Score |
| 2026-09-29 | `biohub-cell-tracking-during-development` | Research | C | 3947 | $60,000 | CZI Biohub Zebrafish 133605 |
| 2026-09-13 | `pokemon-tcg-ai-battle-challenge-strategy` | Featured | 标准 | 939 | $240,000 |  |
| 2026-09-01 | `ai-agent-security-multi-step-tool-attacks` | Featured | C | 4186 | $50,000 | Agents Security Metric |
| 2026-08-31 | `playground-series-s6e8` | Playground | 标准 | 3531 | SWAG | Roc Auc Score |
| 2026-08-31 | `pokemon-tcg-ai-battle` | Featured | 标准 | 6807 | KNOWLEDGE | cabt_bo1 |
| 2026-08-06 | `autonomous-agent-prediction-beta` | Playground | 标准 | 570 | SWAG | Autonomous Agent Prediction Beta Metric |
| 2026-08-05 | `rogii-wellbore-geology-prediction` | Featured | C | 6125 | $50,000 | Mean Squared Error |
| 2026-07-31 | `playground-series-s6e7` | Playground | 标准 | 3355 | SWAG | Balanced Accuracy Score |
| 2026-07-15 | `neurogolf-2026` | Research | 标准 | 2963 | $50,000 | NeuroGolf Metric |
| 2026-07-07 | `orbit-wars` | Featured | 标准 | 4729 | $50,000 | orbit_wars |
| 2026-06-30 | `playground-series-s6e6` | Playground | 标准 | 2816 | SWAG | Balanced Accuracy Score |
| 2026-06-30 | `gan-getting-started` | Getting Started | C | 0 | KNOWLEDGE | PostProcessorKernel |
| 2026-06-30 | `maze-crawler` | Playground | 标准 | 459 | KNOWLEDGE | crawl |
| 2026-06-25 | `hull-tactical-market-prediction` | Featured | C | 3677 | $100,000 | Hull Competition Sharpe |
| 2026-06-19 | `5-day-ai-agents-intensive-vibecoding-course-with-google` | Featured | 标准 | 0 | — |  |
| 2026-06-15 | `nvidia-nemotron-model-reasoning-challenge` | Featured | 标准 | 4185 | $106,388 | NVIDIA Nemotron Metric |
| 2026-06-03 | `birdclef-2026` | Research | C | 4094 | $50,000 | Birdclef ROC AUC |
| 2026-06-01 | `cafa-6-protein-function-prediction` | Research | 标准 | 2259 | $50,000 | cafa6_metric_final |
| 2026-05-31 | `playground-series-s6e5` | Playground | 标准 | 3022 | SWAG | Roc Auc Score |
| 2026-05-18 | `gemma-4-good-hackathon` | Featured | 标准 | 1606 | $200,000 |  |
| 2026-04-30 | `playground-series-s6e4` | Playground | 标准 | 4315 | SWAG | Balanced Accuracy Score |
| 2026-04-22 | `recodai-luc-scientific-image-forgery-detection` | Research | C | 1564 | $55,000 | RecodAI F1 |
| 2026-04-16 | `kaggle-measuring-agi` | Featured | 标准 | 1063 | $200,000 |  |
| 2026-04-15 | `ai-mathematical-olympiad-progress-prize-3` | Featured | C | 4138 | $2,207,152 | 118448 AIMO 3 Multirun-Accuracy |
| 2026-04-07 | `march-machine-learning-mania-2026` | Featured | 标准 | 3462 | $50,000 | Mean Squared Error |
| 2026-03-31 | `playground-series-s6e3` | Playground | 标准 | 4142 | SWAG | Roc Auc Score |
| 2026-03-25 | `stanford-rna-3d-folding-2` | Featured | C | 1867 | $75,000 | Ribonanza TM-Score PermuteChains |
| 2026-03-23 | `deep-past-initiative-machine-translation` | Featured | C | 2674 | $50,000 | DPI BLEU / chrF++ |
| 2026-02-28 | `playground-series-s6e2` | Playground | 标准 | 4370 | SWAG | Roc Auc Score |
| 2026-02-27 | `vesuvius-challenge-surface-detection` | Research | C | 1391 | $200,000 | Vesuvius 2025 Metric |
| 2026-02-24 | `med-gemma-impact-challenge` | Featured | 标准 | 872 | $100,000 |  |
| 2026-01-31 | `playground-series-s6e1` | Playground | 标准 | 4317 | SWAG | Root Mean Squared Error |
| 2026-01-30 | `santa-2025` | Featured | 标准 | 3357 | $50,000 | Santa 2025 Metric |
| 2026-01-28 | `csiro-biomass` | Research | C | 3805 | $75,000 | R2 Score |
| 2026-01-22 | `physionet-ecg-image-digitization` | Research | C | 1424 | $50,000 | Physionet ECG Signal Extraction Metric |
| 2026-01-16 | `mitsui-commodity-prediction-challenge` | Featured | C | 1711 | $100,000 | MITSUI&CO. Commodity Prediction Metric |
| 2026-01-12 | `google-tunix-hackathon` | Featured | 标准 | 319 | $100,000 |  |
| 2026-01-06 | `nfl-big-data-bowl-2026-prediction` | Featured | C | 1899 | $50,000 | NFL_2025 |
| 2025-12-31 | `playground-series-s5e12` | Playground | 标准 | 4206 | SWAG | Roc Auc Score |
| 2025-12-17 | `nfl-big-data-bowl-2026-analytics` | Featured | 标准 | 277 | $50,000 |  |
| 2025-12-15 | `MABe-mouse-behavior-detection` | Research | C | 1412 | $50,000 | MABe F Beta |
| 2025-12-12 | `gemini-3` | Featured | 标准 | 4083 | $500,000 |  |
| 2025-11-30 | `playground-series-s5e11` | Playground | 标准 | 3724 | SWAG | Roc Auc Score |
| 2025-11-03 | `arc-prize-2025` | Featured | C | 1455 | $1,000,000 | Abstraction and Reasoning Challenge |
| 2025-10-31 | `playground-series-s5e10` | Playground | 标准 | 4082 | SWAG | Mean Squared Error |
| 2025-10-30 | `google-code-golf-2025` | Research | 标准 | 1142 | $100,000 | Code Golf Metric |
| 2025-10-23 | `jigsaw-agile-community-rules` | Featured | C | 2445 | $100,000 | 94635_Jigsaw_Rules_AUC |
| 2025-10-15 | `map-charting-student-math-misunderstandings` | Featured | C | 1857 | $55,000 | MAP@{K} |
| 2025-10-14 | `rsna-intracranial-aneurysm-detection` | Featured | C | 1147 | $50,000 | Mean Weighted Columnwise AUCROC |

## 4. 历史参赛人数 Top 15（已结束）

| 队伍数 | 截止 | 比赛 | 类别 | 奖金 |
| --- | --- | --- | --- | --- |
| 8751 | 2019-04-10 | `santander-customer-transaction-prediction` | Featured | $65,000 |
| 7176 | 2018-08-29 | `home-credit-default-risk` | Featured | $70,000 |
| 6807 | 2026-08-31 | `pokemon-tcg-ai-battle` | Featured | KNOWLEDGE |
| 6430 | 2023-08-10 | `icr-identify-age-related-conditions` | Featured | $60,000 |
| 6351 | 2019-10-03 | `ieee-fraud-detection` | Research | $20,000 |
| 6125 | 2026-08-05 | `rogii-wellbore-geology-prediction` | Featured | $50,000 |
| 5558 | 2020-06-30 | `m5-forecasting-accuracy` | Featured | $50,000 |
| 5156 | 2017-11-29 | `porto-seguro-safe-driver-prediction` | Featured | $25,000 |
| 5115 | 2016-05-02 | `santander-customer-satisfaction` | Featured | $60,000 |
| 4874 | 2022-08-24 | `amex-default-prediction` | Featured | $100,000 |
| 4729 | 2026-07-07 | `orbit-wars` | Featured | $50,000 |
| 4539 | 2018-03-20 | `jigsaw-toxic-comment-classification-challenge` | Featured | $35,000 |
| 4516 | 2019-06-03 | `LANL-Earthquake-Prediction` | Research | $50,000 |
| 4463 | 2018-08-20 | `santander-value-prediction-challenge` | Featured | $60,000 |
| 4436 | 2024-03-22 | `optiver-trading-at-the-close` | Featured | $100,000 |

## 5. 可复用结论

- **识别机制优先于识别赛道**：同样是 Featured，`isKernelsSubmissionsOnly` 决定要不要走 notebook 流程、能否离线推理、有无网络与时限约束。
- **大额奖金集中在 LLM / agent / 科学计算**：想拿奖金必须能跑大模型或领域模型，传统 GBDT 表格赛的奖金上限明显更低。
- **Playground 是最高性价比的练兵场**：每月一场、数据干净、评分快、竞争强度低于 Featured，适合验证流水线与集成策略。
- **agent / 对战型比赛在增多**：`pokemon-tcg-ai-battle`、`orbit-wars`、`santa-2025`、`maze-crawler` 这类比赛评分是 Elo 型，不能沿用静态榜单的心智模型。
- **89% 的比赛有公开解法**：历史比赛是低成本的学习材料，尤其适合先看前几名方案再决定切入点。

## 6. 数据说明与限制

- 列表接口是 Kaggle 网站自身的分页接口（公开的 `/api/v1/competitions/list` 每页硬上限 20 条且翻页失效），字段随平台改版可能变化。
- `teams` 是抓取时的参赛队伍数，非最终结算值；奖牌与名次以 Kaggle 官方为准。
- 奖金只统计 `reward.id == USD` 的现金奖，`SWAG`、`KNOWLEDGE` 等非现金奖励不计入。

## 7. 下一步可选方向

1. 选定若干场（如 AIMO 3、ARC Prize 2025、rogii、pokemon-tcg）做解法复盘，提炼可复用方法。
2. 按主题聚类（表格 / CV / NLP / agent / 科学）看各类比赛的演进与常用技术栈。
3. 把验证过的结论回写进 `agentic-kaggle-skill`，形成自己的竞赛 playbook。
