#!/usr/bin/env python3
"""P1 断言抽取台账：≥50 票主题帖的工作清单与覆盖进度。

输入：people/posts/gm_posts.jsonl、people/claims/gm_claims.csv、data/competitions_last5y.csv
输出：people/claims/p1_coverage.csv

验收口径：≥90% 的 ≥50 票主题帖至少产出一条断言（status=done）。
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import pathlib
import re
import sys
from collections import Counter

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "people"))

from build_gm_profiles import domains_of  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--posts", default=str(ROOT / "people" / "posts" / "gm_posts.jsonl"))
    parser.add_argument("--claims", default=str(ROOT / "people" / "claims" / "gm_claims.csv"))
    parser.add_argument("--meta", default=str(ROOT / "data" / "competitions_last5y.csv"))
    parser.add_argument("--out", default=str(ROOT / "people" / "claims" / "p1_coverage.csv"))
    parser.add_argument("--min-votes", type=int, default=50)
    parser.add_argument("--min-coverage", type=float, default=0.9, help="验收门禁：done 比例下限")
    args = parser.parse_args()

    meta = {r["name"]: r for r in csv.DictReader(open(args.meta, encoding="utf-8"))}
    posts = [
        r
        for r in (json.loads(line) for line in open(args.posts, encoding="utf-8") if line.strip())
        if r["kind"] == "topic" and r["votes"] >= args.min_votes
    ]
    posts.sort(key=lambda r: (-r["votes"], r["person"]))

    claim_counts = Counter()
    claims_path = pathlib.Path(args.claims)
    if claims_path.exists():
        for row in csv.DictReader(claims_path.open(encoding="utf-8")):
            claim_counts[(row["person"], row["topic_id"])] += 1

    rows = []
    seen_text: dict[str, str] = {}
    for r in posts:
        m = meta.get(r["slug"], {})
        n = claim_counts.get((r["person"], r["topic_id"]), 0)
        text_hash = hashlib.sha1(re.sub(r"\s+", " ", r["text"]).strip().encode("utf-8")).hexdigest()
        dup_of = seen_text.get(text_hash, "")
        if not dup_of:
            seen_text[text_hash] = r["topic_id"]
        rows.append(
            {
                "person": r["person"],
                "slug": r["slug"],
                "topic_id": r["topic_id"],
                "votes": r["votes"],
                "date": r["date"][:10],
                "year": r["date"][:4],
                "domain": ";".join(sorted(domains_of(m.get("tags", "")))) or m.get("category", ""),
                "text_len": len(r["text"]),
                "claims": n,
                "status": "dup" if dup_of else ("done" if n else "pending"),
                "dup_of": dup_of,
            }
        )

    out = pathlib.Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    done = sum(1 for r in rows if r["status"] == "done")
    dup = sum(1 for r in rows if r["status"] == "dup")
    by_person = Counter(r["person"] for r in rows)
    by_domain = Counter(d for r in rows for d in r["domain"].split(";") if d)
    print(f"posts >= {args.min_votes} votes: {len(rows)} | people: {len(by_person)} | comps: {len({r['slug'] for r in rows})}")
    print(f"extracted: {done}/{len(rows)} ({100*done/len(rows):.0f}%) | verified duplicates: {dup} | claims: {sum(r['claims'] for r in rows)}")
    print("top people (posts):", ", ".join(f"{p} {n}" for p, n in by_person.most_common(8)))
    print("domains:", ", ".join(f"{d} {n}" for d, n in by_domain.most_common(8)))
    print(f"coverage -> {out}")
    coverage = (done + dup) / len(rows)
    print(f"coverage: {coverage:.0%} (target >= {args.min_coverage:.0%})")
    if coverage < args.min_coverage:
        print("coverage below target: P1 未完成")
        return 1
    print("coverage gate: PASS ✅")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
