#!/usr/bin/env python3
"""P3：分层抽取 30 条断言做人工审计（票数档 × 领域 × 证据等级）。

输出：people/claims/audit_sample.csv（含机器校验列与空的审计列）
"""

from __future__ import annotations

import argparse
import csv
import pathlib
import random
import re

ROOT = pathlib.Path(__file__).resolve().parents[2]


def vote_bucket(votes: int) -> str:
    if votes >= 200:
        return "200+"
    if votes >= 100:
        return "100-199"
    return "50-99"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--claims", default=str(ROOT / "people" / "claims" / "gm_claims.csv"))
    parser.add_argument("--posts", default=str(ROOT / "people" / "posts" / "gm_posts.jsonl"))
    parser.add_argument("--out", default=str(ROOT / "people" / "claims" / "audit_sample.csv"))
    parser.add_argument("--n", type=int, default=30)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    texts = {}
    for line in open(args.posts, encoding="utf-8"):
        if line.strip():
            r = __import__("json").loads(line)
            if r["kind"] == "topic":
                texts[(r["person"], r["topic_id"])] = re.sub(r"\s+", " ", r["text"])

    rows = list(csv.DictReader(open(args.claims, encoding="utf-8")))
    rng = random.Random(args.seed)
    strata = {}
    for c in rows:
        key = (vote_bucket(int(c["votes"])), c["domain"].split(";")[0], c["evidence_level"])
        strata.setdefault(key, []).append(c)

    picked = []
    for key, items in sorted(strata.items()):
        picked.append(rng.choice(items))
    if len(picked) > args.n:
        picked = rng.sample(picked, args.n)
    rest = [c for c in rows if c not in picked]
    rng.shuffle(rest)
    while len(picked) < args.n and rest:
        picked.append(rest.pop())
    picked.sort(key=lambda c: c["claim_id"])

    out = pathlib.Path(args.out)
    with out.open("w", newline="", encoding="utf-8") as fh:
        fields = [
            "claim_id", "person", "votes", "evidence_level", "domain", "stage", "action_class",
            "condition", "action", "mechanism", "result", "quote", "source_url",
            "machine_quote_ok", "machine_numbers_ok", "audit_verdict", "audit_note",
        ]
        writer = csv.DictWriter(fh, fieldnames=fields)
        writer.writeheader()
        for c in picked:
            text = texts.get((c["person"], c["topic_id"]), "")
            quote_ok = c["quote"] in text
            numbers = [t for t in re.findall(r"\d+(?:\.\d+)?", c["result"]) if len(t.replace(".", "")) >= 3 or "." in t]
            numbers_ok = all(t in text for t in numbers)
            row = {k: c[k] for k in fields if k in c}
            row.update({"machine_quote_ok": quote_ok, "machine_numbers_ok": numbers_ok, "audit_verdict": "", "audit_note": ""})
            writer.writerow(row)
    print(f"audit sample: {len(picked)} -> {out}")
    print("strata:", len(strata))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
