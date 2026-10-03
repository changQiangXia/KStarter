# KStarter：Kaggle write-up 采集 · 深读 · 方法论提炼（2021-10 ~ 2026-10）

对 **264 场已结束比赛**做全量 write-up 采集、逐场结构化摘要、对照式深读与跨场规律归纳，
把社区经验压成**可检索、可追溯、可执行**的资产：一条结论能找到证据，一个数字能找到出处，
一个失败模式能找到预防动作。

---

## 30 秒速览：你想做什么，去哪里

| 你想做什么 | 去哪里 |
| --- | --- |
| 快速了解一场比赛 | `notes/<主题>/<slug>.md`（速览）→ `analysis/deep/<slug>.md`（深读） |
| 学一个方向的方法论 | `playbook/`（七册，含 v2 增补节 + 可打印检查清单） |
| 找跨场规律与适用边界 | `analysis/THEORY.md`（v0.7：L1–L133 + T1–T37） |
| 查某条规律的数字证据 | `analysis/evidence_map.md` → `analysis/claims.csv`（1850 条，带 evidence_type） |
| 找一张图 / 图证 | `analysis/images_index.csv`（1666 行，P1 已作证 502 / P2 待用 1164） |
| 追一个技法的来龙去脉 | `analysis/lineage.md`（9 族 52 节点 + 传播链 + 失败传播链） |
| 赛前避坑 / 开赛流程 | `analysis/failures.md`（12 类失败模式 + 1964 条）、`analysis/SOP.md`（操作手册） |
| 评估结论能不能用 | `analysis/limitations.md`（材料/证据/复现边界与使用建议） |
| 研究顶尖选手 / 按人找经验 | `people/profiles/<handle>.md`（竞赛榜前 50 人档）→ `analysis/people/PLAYBOOK.md`（跨人专题） |
| 从零打第一场 | `LEARNING_PATH.md` + `playbook/00-通用方法论.md` |
| 看原始材料（正文/评论/图） | `intel/<slug>/`（`topics.json` / `*.html` / `*.txt` / `*_img/`） |
| 做一份新场次的分析 | `analysis/SOP.md` §9 复盘模板 + `templates/` |

## 五层结构（一张图）

```text
intel/            原始采集层：讨论区索引、正文 HTML/纯文本、全部评论、内嵌图片（DONE 断点）
   │ build_digest.py
digests/          每场一文件：索引 + 正文纯文本（写摘要的输入）
   │ 摘要
notes/            264 篇结构化摘要：任务/数据、验证、模型家族、关键技巧、可迁移性、新手启示、出处
   │ 深读
analysis/deep/    264 篇深读：Tier A 60（完整 11 组件）+ Tier B 204（轻量 6 组件）
   │ 跨场归纳
analysis/         THEORY(v0.7) · evidence_map · claims · failures · lineage · limitations · SOP
   │ 回写
playbook/ 七册     通用 / 表格 / CV / NLP-LLM / 科学 / Agent / 多模态-音频-元类（v2 增补 + 检查清单）
LEARNING_PATH.md  新手分阶段路径（含跨领域迁移、黑箱迭代、提交与定稿）
```

## 规模与质量（2026-10 快照）

| 资产 | 规模 | 说明 |
| --- | --- | --- |
| 比赛 | **264/264** | tabular 106 · cv 49 · nlp 35 · science 23 · other 23 · sim-agent 22 · audio 6 |
| 摘要 | **264/264** | `notes/<主题>/<slug>.md`，出处仅用真实 topic id |
| 深读 | **264/264** | Tier A 60（11 组件）+ Tier B 204（轻读） |
| playbook | **7/7** | 均含 v2 增补节与检查清单 |
| 理论 | **L1–L133 + T1–T37** | `analysis/THEORY.md` v0.7（每条：命题→机制→范围→反例→证据） |
| 证据 | **evidence_map 394 行 / claims 1850 行** | 规律×数字证据；claims 带 `可复算-官方/图证/原文数字/自述/矛盾` 标记 |
| 失败学 | **12 类 + 1964 条** | `analysis/failures.md` + `failures.csv`（覆盖全部 264 场） |
| 图像索引 | **1666 行** | P1 已作证 502 / P2 待用 1164；归档图文件 1689 个（png 1486/jpg 136/jpeg 9/gif 28/svg 23/webp 5/bmp 2） |
| 谱系/批判 | **52 节点 + 1 篇** | `lineage.md`（含失败传播链）；`limitations.md` |
| 校验门禁 | 链接 **1564** / 图路径 **823** | 全通过；另对 `topics.json` 全量校验 1177（claims URL）/1666（图 URL）/448（failures topic id），0 错 |

## 三条阅读路径

1. **新手（0 → 第一场）**：`LEARNING_PATH.md` → `playbook/00-通用方法论.md` → 选一个 Playground/Getting Started 的
   `notes` → 同场 `analysis/deep` → 按 `analysis/SOP.md` 的开赛 90 分钟清单执行。
2. **参赛者（备赛/冲刺）**：`analysis/SOP.md`（总流程 + 提交前 48h 清单）→ `analysis/failures.md`（先避免 12 类坑）→
   对应主题的 `playbook` 检查清单 → `analysis/THEORY.md` 的 L/T 条目做假设检验。
3. **研究者/写作者**：`THEORY.md`（可证伪规律与张力）→ `evidence_map.md`（数字证据）→ `lineage.md`（方法谱系）→
   `limitations.md`（证据边界）→ `claims.csv`（全量断言检索）。

## 目录结构

| 路径 | 内容 |
| --- | --- |
| `data/` | 比赛清单（`competitions_ended.csv` 735 场 / `competitions_last5y.csv` 264 场）、`themes.csv`、分布摘要 |
| `intel/<slug>/` | 每场原始材料：`topics.json`、`topics.md`、`bodies/*.html`、`bodies/*.txt`（含评论）、`bodies/*_img/`、`DONE` 断点标记 |
| `digests/<slug>.md` | 索引 + 正文纯文本汇总 |
| `notes/<主题>/<slug>.md` | 264 篇结构化摘要；`notes/INDEX.md` 为全量索引 |
| `people/` | **以人为中心资产**：竞赛榜前 50 快照（`roster/`）、公开榜人-赛记录（`competitions/`）、归档讨论区发言（`posts/`）、个人档案（`profiles/`）；规范见 `people/README.md` |
| `analysis/deep/<slug>.md` | 264 篇深读（Tier A 11 组件 / Tier B 轻读） |
| `analysis/THEORY.md` | 跨场可证伪规律（L）+ 张力（T） |
| `analysis/evidence_map.md` | L114–L133 / T28–T37 的数字证据台账 + 六册数字锚点 |
| `analysis/claims.csv` | 全量可量化断言（含 evidence_type / topic ids / source URL） |
| `analysis/failures.md` + `failures.csv` | 失败学手册与 1964 条原始条目 |
| `analysis/images_index.csv` | 1666 张归档图索引（路径/来源/上下文/优先级/内嵌位置） |
| `analysis/lineage.md` / `limitations.md` | 方法谱系（52 节点） / 批判与边界 |
| `analysis/SOP.md` | 开赛—收官操作手册（侦查/验证/指标/建模/评审交付/提交/复盘） |
| `analysis/people/OVERVIEW.md` | 竞赛榜前 50 总览（战绩/领域/发言/方法词），明细档案见 `people/profiles/` |
| `analysis/people/REPLICATION.md` / `TENSIONS.md` | 前 50 断言复现判定（同队合并证据单位）与 ≥10 组张力裁决 |
| `analysis/GOAL.md` / `DEPTH_PLAN.md` / `TIER_A.md` / `TIER_B.md` | 目标、方案、两档进度权威表 |
| `playbook/` | 七册主题方法论（v2 增补 + 检查清单） |
| `LEARNING_PATH.md` | 新手分阶段学习路径 |
| `scripts/` | 采集 / digest / 摘要 / 校验 / 分析生成器（可断点续跑、限流退避）；人档工具在 `scripts/people/` |
| `templates/` | 摘要模板（完整版 / 精简版） |

## 常用命令

```bash
PY=/root/miniconda3/envs/kaggle/bin/python

# 进度与索引
$PY scripts/notes_status.py                  # 摘要进度
$PY scripts/batch_status.py                  # 采集进度
$PY scripts/build_index.py                   # 重建 notes/INDEX.md

# 采集 / digest
$PY scripts/batch_collect.py --slugs a,b     # 定向采集（断点续跑）
$PY scripts/build_digest.py <slug>           # 生成某场 digest
$PY scripts/backfill_images.py               # 内嵌图回填（报告/下载）
$PY scripts/repair_missing_top.py [--fix]    # 缺陷检查 / 补采

# 质量门禁
$PY scripts/verify_links.py                  # 讨论链接真实性（notes/）
$PY scripts/verify_images.py                 # 相对图路径可渲染（notes/ + analysis/）

# 分析层再生成（确定性脚本）
$PY scripts/build_claims.py                  # → analysis/claims.csv
$PY scripts/build_images_index.py            # → analysis/images_index.csv
$PY scripts/build_failures.py                # → analysis/failures.csv
$PY scripts/build_failures_md.py             # → analysis/failures.md
$PY scripts/build_evidence_map.py            # → analysis/evidence_map.md
```

## 维护约定（新增一场 / 一批）

1. **采集**：`batch_collect.py --slugs ...` → `build_digest.py <slug>`（`DONE` 为合法 JSON 即完成，可断点续跑）。
2. **深读**：写 `analysis/deep/<slug>.md`（Tier A 11 组件 / Tier B 轻读），回写 `notes/<主题>/<slug>.md`。
3. **进度**：更新 `analysis/TIER_A.md` / `analysis/TIER_B.md` 的行状态与进度；目标/断点写在 `analysis/GOAL.md`。
4. **回流**：跑 `build_claims.py`、`build_images_index.py`、`build_failures.py` + `build_failures_md.py`、`build_evidence_map.py`；
   新技法/失败模式/规律分别补 `lineage.md`、`failures.md`、`THEORY.md`（并更新 `SOP.md`/playbook 检查清单）。
5. **验收**：`verify_links.py` + `verify_images.py` 必须全绿；新写链接只用 `topics.json` 里的真实 topic id。
6. **推送**：分批 commit/push（沿用容器低内存 + 代理策略，见 `docs/PUSH_TO_GITHUB.md`）。

## 数据与合规

- 只抓取 write-up 正文中的**内嵌图片**（属原帖内容）；站外图床（imgur 等）只保留 URL，不下载。
- 不复制代码原文；摘要保留原文链接与名次信息；不突出个人身份，按名次表述。
- 敏感/受限材料以链接与出处保留，不做二次分发；引用前请回到原帖核对。

## 相关文档

- `LEARNING_PATH.md`（学习路径）｜ `playbook/`（七册方法论）｜ `notes/README.md`（摘要说明）｜ `notes/INDEX.md`（264 场索引）
- `analysis/GOAL.md`（目标与断点）｜ `analysis/DEPTH_PLAN.md`（深读方案）｜ `analysis/TIER_A.md` / `TIER_B.md`（进度）
- `analysis/THEORY.md` / `evidence_map.md` / `claims.csv` / `failures.md` / `lineage.md` / `limitations.md` / `SOP.md`
