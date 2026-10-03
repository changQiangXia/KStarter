# people/：以"人"为中心的资产区

> 从"按比赛搜索"扩展到"按人搜索"：记录 Kaggle 竞赛榜前 50 选手的近 5 年公开战绩与公开区言论。
> 快照日期：2026-10-04（名单以 `roster/manifest.json` 的 latest 为准）。

## 结构

| 路径 | 内容 | 是否入库 |
| --- | --- | --- |
| `roster/gm_top50_<date>.csv` | 竞赛榜前 50 名单快照（rank/积分/奖牌/主页）+ `manifest.json` | ✅ |
| `competitions/gm_competitions.csv` | 人 × 比赛 × 名次/分数/提交数/团队成员（来自公开榜） | ✅ |
| `competitions/summary.csv` | 每人匹配到的比赛数与最佳名次 | ✅ |
| `posts/gm_posts.jsonl` | 归档讨论区中这些人的主题帖与评论（含日期/票数/父节点/正文） | ✅ |
| `posts/summary.csv` | 每人发言数（主题/评论）与时间跨度 | ✅ |
| `profiles/<handle>.md` | 个人档案：战绩表 + 公开言论 + 方法关键词 | ✅ |
| `data/cache/people_lb/` | 原始 leaderboard zip/CSV 与抓取状态（脚本缓存） | ❌（gitignore） |

## 生成流程

```bash
PY=/root/miniconda3/envs/kaggle/bin/python
$PY scripts/people/fetch_gm_roster.py --count 50          # 榜单快照
$PY scripts/people/fetch_leaderboards.py                  # 264 场公开榜（断点续跑）
$PY scripts/people/extract_gm_posts.py                    # 归档讨论区发言
$PY scripts/people/build_gm_profiles.py                   # 人档 + 总览
```

## 覆盖与边界

- 榜单匹配只覆盖 KStarter 归档的 **264 场近 5 年比赛**；公开榜不可下载/已关闭的比赛会记录状态但不产出记录。
- 发言只覆盖这 264 场的讨论区归档（1567 个主题、含完整评论树）；未归档比赛与站外平台不计。
- 身份匹配：公开榜 `TeamMemberUserNames`、讨论区作者显示名，按 handle/显示名归一化匹配；团队/改名/删号会造成漏配。
- 快照是时点数据：榜单与奖牌会变化，历史快照保留在 `roster/`。
