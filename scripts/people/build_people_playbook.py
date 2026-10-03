#!/usr/bin/env python3
"""跨人专题：从人档数据生成 analysis/people/PLAYBOOK.md。

输入：people/roster 最新快照、people/posts/gm_posts.jsonl、
      people/competitions/gm_competitions.csv、data/competitions_last5y.csv
输出：analysis/people/PLAYBOOK.md

包含：声音榜、领域×人（按比赛类型找人）、组队网络、高票经验帖、发言时间线。
依赖 build_gm_profiles.py 的领域映射，避免两处重复维护。
"""

from __future__ import annotations

import argparse
import csv
import json
import pathlib
import sys
from collections import Counter, defaultdict
from itertools import combinations

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "people"))

from build_gm_profiles import domains_of, latest_roster  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--competitions", default=str(ROOT / "people" / "competitions" / "gm_competitions.csv"))
    parser.add_argument("--out", default=str(ROOT / "analysis" / "people" / "PLAYBOOK.md"))
    args = parser.parse_args()

    roster = list(csv.DictReader(latest_roster(ROOT / "people" / "roster").open(encoding="utf-8")))
    url = {r["handle"]: r["user_url"] for r in roster}
    name = {r["handle"]: r["display_name"] for r in roster}
    meta = {r["name"]: r for r in csv.DictReader((ROOT / "data" / "competitions_last5y.csv").open(encoding="utf-8"))}

    posts = defaultdict(list)
    for line in (ROOT / "people" / "posts" / "gm_posts.jsonl").open(encoding="utf-8"):
        if line.strip():
            rec = json.loads(line)
            posts[rec["person"]].append(rec)

    comps = defaultdict(list)
    comps_path = pathlib.Path(args.competitions)
    if comps_path.exists():
        for r in csv.DictReader(comps_path.open(encoding="utf-8")):
            comps[r["handle"]].append(r)

    lines = [
        "# 前 50 选手跨人专题（2026-10 快照）",
        "",
        "> 数据：竞赛榜前 50 + 近 5 年归档比赛公开榜匹配 + 归档讨论区公开发言。",
        "> 明细档案见 `people/profiles/<handle>.md`，总表见 `analysis/people/OVERVIEW.md`。",
        "",
    ]

    # §1 声音榜
    lines += ["## 1. 声音榜：谁在公开区持续输出", ""]
    lines += ["| 选手 | 发言 | 主题 | 评论 | 获票合计 | 最高票帖 | 时间跨度 |", "| --- | --- | --- | --- | --- | --- | --- |"]
    voice = sorted(posts.items(), key=lambda kv: -len(kv[1]))[:15]
    for handle, recs in voice:
        topics = sum(1 for r in recs if r["kind"] == "topic")
        votes = sum(int(r.get("votes") or 0) for r in recs)
        best = max(int(r.get("votes") or 0) for r in recs)
        ds = sorted(r["date"] for r in recs if r.get("date"))
        span = f"{ds[0][:10]} ~ {ds[-1][:10]}" if ds else ""
        lines.append(
            f"| [@{handle}]({url[handle]}) | {len(recs)} | {topics} | {len(recs)-topics} | {votes} | {best} | {span} |"
        )
    total_posts = sum(len(v) for v in posts.values())
    lines += ["", f"共 {len(posts)} 人有公开发言，合计 {total_posts} 条。", ""]

    # §2 领域 × 人
    lines += ["## 2. 领域 × 人：按比赛类型找谁", ""]
    domain_people: dict[str, list[tuple[str, int, int]]] = {}
    if comps:
        for handle, recs in comps.items():
            agg: dict[str, list[int]] = defaultdict(list)
            for r in recs:
                valid = r.get("lb_quality", "ok") == "ok"
                rank = int(r["rank"]) if valid and str(r["rank"]).isdigit() else 10**9
                for d in domains_of(meta.get(r["slug"], {}).get("tags", "")):
                    agg[d].append(rank)
            for d, ranks in agg.items():
                domain_people.setdefault(d, []).append((handle, len(ranks), min(ranks)))
        for d, people in sorted(domain_people.items(), key=lambda kv: -len(kv[1])):
            people.sort(key=lambda x: (-x[1], x[2]))
            shown = "、".join(
                f"[@{h}]({url[h]})（{n} 场/最佳 {b if b < 10**9 else '—'}）" for h, n, b in people[:8]
            )
            lines.append(f"- **{d}**：{shown}")
        lines.append("")
        lines.append("> 计数为该领域已匹配的参赛场次，最佳为该领域内的最小名次；同一个人可出现在多个领域。")
    else:
        lines.append("_尚无公开榜匹配数据。_")
    lines.append("")

    # §3 组队网络
    lines += ["## 3. 组队网络：前 50 之间的同队关系", ""]
    team_rows = defaultdict(set)
    for handle, recs in comps.items():
        for r in recs:
            key = (r["slug"], r["team_name"])
            team_rows[key].add(handle)
    edges = Counter()
    for key, members in team_rows.items():
        for a, b in combinations(sorted(members), 2):
            edges[(a, b)] += 1
    if edges:
        lines += ["| 组合 | 同队场次 |", "| --- | --- |"]
        for (a, b), n in edges.most_common(15):
            lines.append(f"| [@{a}]({url[a]}) × [@{b}]({url[b]}) | {n} |")
        degree = Counter()
        for (a, b), n in edges.items():
            degree[a] += n
            degree[b] += n
        lines += ["", "连接度最高：" + "、".join(f"[@{h}]({url[h]}) {n}" for h, n in degree.most_common(8)), ""]
    else:
        lines.append("_在已匹配的公开榜记录中没有发现前 50 成员同队。_")
    lines.append("")

    # §4 高票经验帖
    lines += ["## 4. 高票经验帖：先读这些", ""]
    all_posts = [r for recs in posts.values() for r in recs if r["kind"] == "topic"]
    top = sorted(all_posts, key=lambda r: -int(r.get("votes") or 0))[:20]
    lines += ["| 票 | 选手 | 日期 | 比赛 | 主题 |", "| --- | --- | --- | --- | --- |"]
    for r in top:
        link = f"https://www.kaggle.com/competitions/{r['slug']}/discussion/{r['topic_id']}"
        title = r.get("topic_title", "").replace("|", "/")[:60]
        lines.append(
            f"| {r.get('votes',0)} | [@{r['person']}]({url[r['person']]}) | {r.get('date','')[:10]} "
            f"| `{r['slug']}` | [{title}]({link}) |"
        )
    lines.append("")

    # §5 时间线
    lines += ["## 5. 发言时间线（按年）", ""]
    by_year = Counter(r["date"][:4] for recs in posts.values() for r in recs if r.get("date"))
    lines.append("、".join(f"{y} {n} 条" for y, n in sorted(by_year.items())))
    lines.append("")

    out = pathlib.Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines), encoding="utf-8")
    print(f"playbook -> {out} ({len(lines)} lines)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
