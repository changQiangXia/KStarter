# 外部题解索引（kaggle-solutions）

> 来源：[faridrashidi/kaggle-solutions](https://github.com/faridrashidi/kaggle-solutions)（MIT License, Farid Rashidi），commit `dc9a449d8484`，抓取 2026-10-06；本地 clone 放在 `data/cache/`（不入库）。
> 本目录只存派生索引：外部 721 场 / 全部题解链接 → 与本仓库 264 场逐条比对，标注已收录/未收录。

## 规模

- 外部索引：**721 场 / 4768 条链接**（description 3671 · code 1022 · kernel 75）。
- 本仓库覆盖：228 场有外部链接（共 2402 条，其中未收录 700 条）；35 场外部零链接；1 场外部无此赛事。
- 历史池（不在 264 场内）：2366 条链接，按年份集中在 2010–2021，可作为跨时代对照素材。

## 新增链接最多（未收录，本仓库覆盖场）

| 场次 | 新增 | 其中冠军 | 说明 |
| --- | --- | --- | --- |
| `rogii-wellbore-geology-prediction` | 30 | 1 | ROGII - Wellbore Geology Prediction |
| `deep-past-initiative-machine-translation` | 25 | 1 | Deep Past Challenge - Translate Akkadian to English |
| `birdclef-2026` | 24 | 1 | BirdCLEF+ 2026 |
| `cmi-detect-behavior-with-sensor-data` | 22 | 1 | CMI - Detect Behavior with Sensor Data |
| `map-charting-student-math-misunderstandings` | 20 | 1 | MAP - Charting Student Math Misunderstandings |
| `physionet-ecg-image-digitization` | 20 | 1 | PhysioNet - Digitization of ECG Images |
| `ariel-data-challenge-2025` | 19 | 1 | NeurIPS - Ariel Data Challenge 2025 |
| `make-data-count-finding-data-references` | 19 | 1 | Make Data Count - Finding Data References |
| `biohub-cell-tracking-during-development` | 18 | 1 | Biohub - Cell Tracking During Development |
| `csiro-biomass` | 18 | 1 | CSIRO - Image2Biomass Prediction |
| `neurogolf-2026` | 18 | 1 | The 2026 NeuroGolf Championship |
| `vesuvius-challenge-surface-detection` | 18 | 1 | Vesuvius Challenge - Surface Detection |
| `neurips-open-polymer-prediction-2025` | 16 | 1 | NeurIPS - Open Polymer Prediction 2025 |
| `ai-agent-security-multi-step-tool-attacks` | 15 | 0 | AI Agent Security - Multi-Step Tool Attacks |
| `playground-series-s6e2` | 15 | 1 | Predicting Heart Disease |

新增链接里的排名分布（前 10）：rank 1×36、rank 2×36、rank 3×36、rank 4×34、rank 5×38、rank 6×32、rank 7×29、rank 8×34、rank 9×27、rank 10×25。

## 外部零链接 / 缺赛事（本仓库覆盖场）

- 外部零链接 35 场：`pokemon-tcg-ai-battle-challenge-strategy`、`autonomous-agent-prediction-beta`、`gan-getting-started`、`5-day-ai-agents-intensive-vibecoding-course-with-google`、`gemma-4-good-hackathon`、`kaggle-measuring-agi`、`med-gemma-impact-challenge`、`google-tunix-hackathon`、`nfl-big-data-bowl-2026-analytics`、`gemini-3`、`bigquery-ai-hackathon`、`openai-gpt-oss-20b-red-teaming`、`google-gemma-3n-hackathon`、`meta-kaggle-hackathon`、`openai-to-z-challenge`、`gemma-language-tuning`、`nfl-big-data-bowl-2025`、`gemini-long-context`、`geolifeclef-2024`、`data-assistants-with-gemma`、`nfl-big-data-bowl-2024`、`playground-series-s3e25`、`lux-ai-season-2-neurips-stage-2`、`llm-prompting-with-makersuite`、`2023-kaggle-ai-report`、`playground-series-s3e18`、`fathomnet-out-of-sample-detection`、`nfl-big-data-bowl-2023`、`lux-ai-2022-beta`、`scrabble-player-rating`、`big-data-derby-2022`、`tabular-playground-series-oct-2022`、`nfl-big-data-bowl-2022`、`wikipedia-image-caption`、`kaggle-survey-2021`
- 外部无此赛事 1 场：`phase-ii-widsdatathon2022`

## 链接健康与口径

- 域名分布：www.kaggle.com 4345、github.com 315、blog.kaggle.com 92、www.csie.ntu.edu.tw 2、homepages.inf.ed.ac.uk 2、glowingpython.blogspot.com 1。
- 需注意的链接：{'insecure_http': 6, 'legacy_blog': 92}（`legacy_blog` 为已停服的 blog.kaggle.com；抽样 25 条 HTTP 校验，24 条 200、1 条为 blog.kaggle.com）。
- 去重口径：URL 规范化（`/c/` ≡ `/competitions/`、去 query、去尾斜杠、主机小写）；`in_kstarter_docs=1` 表示该链接已出现在本仓库策展文档（README/analysis/notes/playbook/people/digests/templates/docs，不含 intel 原始层）。

## 用法

- 给 `notes/` / `analysis/deep/` 补外部题解：查 `delta_links.csv`（按 slug + rank 排好），把高排名链接补进对应「出处」节。
  `in_scope=1` 的 700 条是 264 场内可补链接，`in_scope=0` 的 2234 条是历史池链接。
- 优先清单：`coverage_by_comp.csv` 里 `new_rank_le3` 或 `new_links` 大的行（本轮共 48 场前三名新增链接）。
- 下游消费：KExperienceSkill 的 `tools/import_external_links.py` 会读取本目录 CSV，生成 skill 侧外链资产与冠军方案索引。

## 复现

```bash
git clone --depth 1 https://github.com/faridrashidi/kaggle-solutions data/cache/kaggle-solutions
python scripts/build_external_index.py
```

> 许可：kaggle-solutions 为 MIT License（Copyright (c) 2018-2026 Farid Rashidi）；本目录仅派生链接与元数据，保留来源署名；原始 YAML 不入库。
