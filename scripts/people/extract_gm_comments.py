#!/usr/bin/env python3
"""P3：抽取前 50 选手的高票评论（≥10 票）作为"现场层"证据。

输入：people/posts/gm_posts.jsonl（kind=comment）
输出：people/posts/gm_comments_highvote.csv
"""

from __future__ import annotations

import argparse
import csv
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--posts", default=str(ROOT / "people" / "posts" / "gm_posts.jsonl"))
    parser.add_argument("--out", default=str(ROOT / "people" / "posts" / "gm_comments_highvote.csv"))
    parser.add_argument("--min-votes", type=int, default=10)
    args = parser.parse_args()

    rows = []
    for line in open(args.posts, encoding="utf-8"):
        if not line.strip():
            continue
        r = json.loads(line)
        if r["kind"] != "comment" or int(r.get("votes") or 0) < args.min_votes:
            continue
        rows.append(
            {
                "person": r["person"],
                "slug": r["slug"],
                "topic_id": r["topic_id"],
                "topic_title": r.get("topic_title", ""),
                "date": (r.get("date") or "")[:10],
                "votes": r.get("votes", 0),
                "parent": r.get("parent", ""),
                "text": r.get("text", ""),
                "source_url": f"https://www.kaggle.com/competitions/{r['slug']}/discussion/{r['topic_id']}",
            }
        )
    rows.sort(key=lambda r: -int(r["votes"]))

    out = pathlib.Path(args.out)
    with out.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    print(f"high-vote comments: {len(rows)} (>= {args.min_votes} votes) -> {out}")
    print(f"people: {len({r['person'] for r in rows})} | comps: {len({r['slug'] for r in rows})}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
