#!/usr/bin/env python3
"""P3：为有 ≥50 票 GM 主题帖的比赛生成 dossier（证据包）。

输出：analysis/people/dossiers/<slug>.md + analysis/people/DOSSIERS.md（索引）
"""

from __future__ import annotations

import argparse
import csv
import json
import pathlib
import re
from collections import defaultdict

ROOT = pathlib.Path(__file__).resolve().parents[2]


def latest_roster(roster_dir: pathlib.Path) -> pathlib.Path | None:
    manifest = roster_dir / "manifest.json"
    if manifest.exists():
        latest = json.loads(manifest.read_text()).get("latest")
        if latest:
            return roster_dir / latest
    snaps = sorted(roster_dir.glob("gm_top*.csv"))
    return snaps[-1] if snaps else None


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--posts", default=str(ROOT / "people" / "posts" / "gm_posts.jsonl"))
    parser.add_argument("--claims", default=str(ROOT / "people" / "claims" / "gm_claims.csv"))
    parser.add_argument("--comments", default=str(ROOT / "people" / "posts" / "gm_comments_highvote.csv"))
    parser.add_argument("--meta", default=str(ROOT / "data" / "competitions_last5y.csv"))
    parser.add_argument("--intel", default=str(ROOT / "intel"))
    parser.add_argument("--out-dir", default=str(ROOT / "analysis" / "people" / "dossiers"))
    parser.add_argument("--min-votes", type=int, default=50)
    args = parser.parse_args()

    meta = {r["name"]: r for r in csv.DictReader(open(args.meta, encoding="utf-8"))}
    topics = defaultdict(list)
    for line in open(args.posts, encoding="utf-8"):
        if not line.strip():
            continue
        r = json.loads(line)
        if r["kind"] == "topic" and int(r.get("votes") or 0) >= args.min_votes:
            topics[r["slug"]].append(r)

    claims = defaultdict(list)
    if pathlib.Path(args.claims).exists():
        for c in csv.DictReader(open(args.claims, encoding="utf-8")):
            claims[c["slug"]].append(c)

    comments = defaultdict(list)
    if pathlib.Path(args.comments).exists():
        for c in csv.DictReader(open(args.comments, encoding="utf-8")):
            comments[c["slug"]].append(c)

    # notes 路径索引
    notes_index = {}
    for p in (ROOT / "notes").glob("*/*.md"):
        notes_index.setdefault(p.stem, p)

    out_dir = pathlib.Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    index = []
    for slug in sorted(topics, key=lambda s: -len(topics[s])):
        m = meta.get(slug, {})
        ts = sorted(topics[slug], key=lambda r: -int(r["votes"]))
        lines = [
            f"# {m.get('title', slug)}",
            "",
            f"> `{slug}` ｜ {m.get('category','')} ｜ 指标 {m.get('metric','')} ｜ {m.get('teams','')} 队 ｜ 截止 {m.get('deadline','')}",
            "",
            f"本页汇总该场 **{len(ts)} 条 ≥{args.min_votes} 票 GM 主题帖**、**{len(claims.get(slug, []))} 条断言**、"
            f"**{len(comments.get(slug, []))} 条高票评论**。",
            "",
            "## GM 主题帖",
            "",
            "| 票 | 选手 | 日期 | 主题 |",
            "| --- | --- | --- | --- |",
        ]
        for r in ts:
            url = f"https://www.kaggle.com/competitions/{slug}/discussion/{r['topic_id']}"
            title = r.get("topic_title", "").replace("|", "/")[:70]
            lines.append(f"| {r['votes']} | [@{r['person']}](https://www.kaggle.com/{r['person']}) | {r['date'][:10]} | [{title}]({url}) |")

        lines += ["", "## 断言（条件→动作→机制→结果）", ""]
        if claims.get(slug):
            lines += ["| 选手 | 等级 | 阶段 | 动作（节选） | 出处 |", "| --- | --- | --- | --- | --- |"]
            for c in sorted(claims[slug], key=lambda c: (c["evidence_level"], -int(c["votes"]))):
                action = re.sub(r"\s+", " ", c["action"]).replace("|", "/")[:90]
                lines.append(f"| @{c['person']} | {c['evidence_level']} | {c['stage']} | {action} | [{c['claim_id']}]({c['source_url']}) |")
        else:
            lines.append("_无断言_")

        lines += ["", "## 高票评论", ""]
        if comments.get(slug):
            lines += ["| 票 | 选手 | 日期 | 摘录 | 出处 |", "| --- | --- | --- | --- | --- |"]
            for c in comments[slug][:15]:
                text = re.sub(r"\s+", " ", c["text"]).replace("|", "/")[:110]
                lines.append(f"| {c['votes']} | @{c['person']} | {c['date']} | {text} | [{c['topic_id']}]({c['source_url']}) |")
        else:
            lines.append("_无 ≥10 票评论_")

        # 图证与深读链接
        img_count = 0
        for r in ts:
            d = pathlib.Path(args.intel) / slug / "bodies" / f"{r['topic_id']}_img"
            if d.exists():
                img_count += sum(1 for _ in d.iterdir())
        lines += ["", "## 关联资产", ""]
        if (ROOT / "analysis" / "deep" / f"{slug}.md").exists():
            lines.append(f"- 深读：`analysis/deep/{slug}.md`")
        if slug in notes_index:
            lines.append(f"- 结构化摘要：`notes/{notes_index[slug].parent.name}/{slug}.md`")
        lines.append(f"- 归档讨论区：`intel/{slug}/`（主题 {len(ts)} 条有 ≥{args.min_votes} 票帖，图证 {img_count} 个）")
        lines.append("")

        (out_dir / f"{slug}.md").write_text("\n".join(lines), encoding="utf-8")
        index.append(
            {
                "slug": slug,
                "title": m.get("title", slug),
                "category": m.get("category", ""),
                "topics": len(ts),
                "claims": len(claims.get(slug, [])),
                "comments": len(comments.get(slug, [])),
            }
        )

    idx_lines = [
        "# 94 场 dossier 索引（P3）",
        "",
        f"> 覆盖 {len(index)} 场有 ≥{args.min_votes} 票 GM 主题帖的比赛；明细见 `analysis/people/dossiers/<slug>.md`。",
        "",
        "| 比赛 | 类别 | GM 帖 | 断言 | 高票评论 |",
        "| --- | --- | --- | --- | --- |",
    ]
    for r in sorted(index, key=lambda r: (-r["topics"], r["slug"])):
        idx_lines.append(f"| [`{r['slug']}`](dossiers/{r['slug']}.md) | {r['category']} | {r['topics']} | {r['claims']} | {r['comments']} |")
    (ROOT / "analysis" / "people" / "DOSSIERS.md").write_text("\n".join(idx_lines) + "\n", encoding="utf-8")

    print(f"dossiers: {len(index)} -> {out_dir}")
    print(f"index -> {ROOT / 'analysis' / 'people' / 'DOSSIERS.md'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
