# people/：以"人"为中心的资产区

> 从"按比赛搜索"扩展到"按人搜索"：记录 Kaggle 竞赛榜前 50 选手的近 5 年公开战绩与公开区言论。
> 快照日期：2026-10-04（名单以 `roster/manifest.json` 的 latest 为准）。

## 结构

| 路径 | 内容 | 是否入库 |
| --- | --- | --- |
| `roster/gm_top50_<date>.csv` | 竞赛榜前 50 名单快照（rank/积分/奖牌/主页）+ `manifest.json` | ✅ |
| `competitions/gm_competitions.csv` | 人 × 比赛 × 名次/分数/提交数/团队成员（来自公开榜） | ✅ |
| `competitions/summary.csv` | 每人匹配到的比赛数与最佳名次 | ✅ |
| `competitions/coverage.csv` | 每场比赛的公开榜状态（`ok`/`no_zip`）与匹配人数，边界可审计 | ✅ |
| `posts/gm_posts.jsonl` | 归档讨论区中这些人的主题帖与评论（含日期/票数/父节点/正文） | ✅ |
| `posts/summary.csv` | 每人发言数（主题/评论）与时间跨度 | ✅ |
| `claims/gm_claims.csv` | GM 断言库：条件/动作/机制/结果 + 逐字引用 + 证据等级（无逐字引用不入库） | ✅ |
| `claims/p1_coverage.csv` | P1 抽取台账：152 条 ≥50 票主题帖的进度与验收口径（覆盖率 ≥90%） | ✅ |
| `profiles/<handle>.md` | 个人档案：战绩表 + 比赛领域分布 + 公开言论 + 方法关键词（总览：`analysis/people/OVERVIEW.md`） | ✅ |
| `analysis/people/PLAYBOOK.md` | 跨人专题：声音榜 / 领域×人 / 组队网络 / 高票经验帖 | ✅ |
| `data/cache/people_lb/` | 原始 leaderboard zip/CSV 与抓取状态（脚本缓存） | ❌（gitignore） |

## 生成流程

```bash
PY=/root/miniconda3/envs/kaggle/bin/python
$PY scripts/people/fetch_gm_roster.py --count 50          # 榜单快照
$PY scripts/people/fetch_leaderboards.py                  # 264 场公开榜（断点续跑）
$PY scripts/people/extract_gm_posts.py                    # 归档讨论区发言
$PY scripts/people/build_gm_profiles.py                   # 人档 + 总览
$PY scripts/people/build_people_playbook.py               # 跨人专题
$PY scripts/people/verify_claims.py                       # 断言：引用/数字/链接/元数据校验
$PY scripts/people/build_claim_coverage.py                # P1 台账：抽取覆盖率
$PY scripts/verify_links.py                               # 校验 notes + 人档的讨论链接
```

## 断言库（claims/）

- 粒度：一条断言 = 一个可执行动作（含适用条件、机制、结果数字），不是一段摘要。
- 必填溯源：`quote` 必须是原文正文的逐字子串，`source_url`/`topic_id`/`date`/`votes` 与归档一致，
  `result` 中的数字必须能在原文复现；`evidence_type` 沿用 `analysis/claims.csv` 词表。
- 证据等级：A（原文可复算数字 + 名次/团队背书）、B（有数字无独立背书）、C（无数字的经验判断）。
- 口径：`quote` 只取主题帖正文（不含评论）；`lb_unusable` 标记 Kaggle 冻结榜（分数全 0）涉及的断言。
- P1 范围：≥50 票的主题帖；先 10 条校准样例，确认后全量抽取。
- 验收：`build_claim_coverage.py --min-coverage 0.9` 返回零（status=done 比例 ≥90%）；全量后按票数档 × 领域 × 证据等级分层抽 30 条人工审计。

## 数据规模（2026-10-04 快照）

| 指标 | 数值 |
| --- | --- |
| 名单 | 50 人（37 GRANDMASTER + 13 MASTER） |
| 公开榜抓取 | 264 场 → 241 场 `ok`、23 场 `no_zip` |
| 人-赛记录 | 1842 条，覆盖 50/50 人、236 场比赛 |
| 公开区发言 | 2467 条 / 47 人（主题 211 + 评论 2256，2021-08 ~ 2026-10） |
| 链接校验 | 1903 条 Kaggle 讨论链接全部命中 `intel/<slug>/topics.json` |

## 覆盖与边界

- 段位口径：统计对象是**竞赛榜前 50**（2026-10-04 快照：37 名 GRANDMASTER + 13 名 MASTER），不是"全部 GM 选手"。
- 榜单匹配只覆盖 KStarter 归档的 **264 场近 5 年比赛**；公开榜不可下载/已关闭的比赛在 `coverage.csv` 记为 `no_zip` 但不产出记录。
- 发言只覆盖这 264 场的讨论区归档（1567 个主题、含完整评论树）；未归档比赛与站外平台不计。
- 身份匹配：公开榜 `TeamMemberUserNames`、讨论区作者显示名，按 handle/显示名归一化匹配；团队/改名/删号会造成漏配。
- 快照是时点数据：榜单与奖牌会变化，历史快照保留在 `roster/`。
