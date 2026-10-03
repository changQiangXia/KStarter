#!/usr/bin/env python3
"""从 intel/ 讨论区纯文本中抽取 GM 的发言（主题帖 + 评论树节点）。

输入：people/roster/gm_top50_*.csv（最近快照）、intel/<slug>/bodies/*.txt
输出：people/posts/gm_posts.jsonl、people/posts/summary.csv
"""

from __future__ import annotations

import argparse
import csv
import json
import pathlib
import re
from collections import Counter

ROOT = pathlib.Path(__file__).resolve().parents[2]

HEADER_TOPIC = re.compile(r"^Topic #(\d+):\s*(.*)$")
HEADER_AUTHOR = re.compile(r"^\s*Author:\s*(.+?)\s*$")
HEADER_POSTED = re.compile(r"^\s*Posted:\s*(.+?)\s*$")
HEADER_VOTES = re.compile(r"^\s*Votes:\s*(\d+)\s+Comments:\s*(\d+)")
COMMENT = re.compile(r"^([│ ]*)([├└]─)\s*(.+?)\s*\((\d{4}-\d{2}-\d{2}[^)]*)\)\s*(?:\[([+-]?\d+)\])?\s*$")


def normalize(name: str) -> str:
    return re.sub(r"[^a-z0-9]", "", name.lower())


def load_roster(path: pathlib.Path) -> dict[str, dict]:
    people = {}
    for row in csv.DictReader(path.open(encoding="utf-8")):
        for key in {normalize(row["display_name"]), normalize(row["handle"])}:
            if key:
                people[key] = row
    return people


def latest_roster(roster_dir: pathlib.Path) -> pathlib.Path | None:
    manifest = roster_dir / "manifest.json"
    if manifest.exists():
        latest = json.loads(manifest.read_text()).get("latest")
        if latest and (roster_dir / latest).exists():
            return roster_dir / latest
    snaps = sorted(roster_dir.glob("gm_top*.csv"))
    return snaps[-1] if snaps else None


def clean_lines(lines: list[str]) -> str:
    out = []
    for line in lines:
        line = re.sub(r"^[│ ]*", "", line)
        line = re.sub(r"^[├└]─\s*", "", line)
        out.append(line.strip())
    text = " ".join(x for x in out if x)
    return re.sub(r"\s+", " ", text).strip()


def parse_file(path: pathlib.Path, slug: str, people: dict[str, dict], min_chars: int):
    lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
    topic_id, title, author, posted, votes = "", "", "", "", 0
    for line in lines[:15]:
        m = HEADER_TOPIC.match(line)
        if m:
            topic_id, title = m.group(1), m.group(2)
        m = HEADER_AUTHOR.match(line)
        if m:
            author = m.group(1).strip()
        m = HEADER_POSTED.match(line)
        if m:
            posted = m.group(1)
        m = HEADER_VOTES.match(line)
        if m:
            votes = int(m.group(1))

    if author and normalize(author) in people:
        person = people[normalize(author)]
        body = clean_lines(lines[8:])
        yield {
            "person": person["handle"],
            "display_name": person["display_name"],
            "kind": "topic",
            "slug": slug,
            "topic_id": topic_id,
            "topic_title": title,
            "date": posted,
            "votes": votes,
            "parent": "",
            "text": body,
        }

    stack: list[tuple[int, str]] = []
    i = 0
    while i < len(lines):
        m = COMMENT.match(lines[i])
        if not m:
            i += 1
            continue
        indent, _, name, ts, score = m.groups()
        depth = len(indent) // 2
        stack = [s for s in stack if s[0] < depth]
        parent = stack[-1][1] if stack else ""
        stack.append((depth, name))
        body_lines = []
        j = i + 1
        while j < len(lines) and not COMMENT.match(lines[j]):
            if lines[j].strip():
                body_lines.append(lines[j])
            j += 1
        text = clean_lines(body_lines)
        if normalize(name) in people and len(text) >= min_chars:
            person = people[normalize(name)]
            yield {
                "person": person["handle"],
                "display_name": person["display_name"],
                "kind": "comment",
                "slug": slug,
                "topic_id": topic_id,
                "topic_title": title,
                "date": ts,
                "votes": int(score) if score else 0,
                "parent": parent,
                "text": text,
            }
        i = j


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--roster", default="")
    parser.add_argument("--roster-dir", default=str(ROOT / "people" / "roster"))
    parser.add_argument("--intel", default=str(ROOT / "intel"))
    parser.add_argument("--out", default=str(ROOT / "people" / "posts" / "gm_posts.jsonl"))
    parser.add_argument("--summary", default=str(ROOT / "people" / "posts" / "summary.csv"))
    parser.add_argument("--min-chars", type=int, default=12)
    args = parser.parse_args()

    roster_path = pathlib.Path(args.roster) if args.roster else latest_roster(pathlib.Path(args.roster_dir))
    if not roster_path or not roster_path.exists():
        print("ERROR: 找不到 roster，先运行 scripts/people/fetch_gm_roster.py", file=sys.stderr)
        return 1
    people = load_roster(roster_path)

    out_path = pathlib.Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    counts: Counter = Counter()
    dates: dict[str, list[str]] = {}
    topics: Counter = Counter()
    n_posts = 0
    with out_path.open("w", encoding="utf-8") as fh:
        for txt in sorted(pathlib.Path(args.intel).glob("*/bodies/*.txt")):
            slug = txt.parents[1].name
            for rec in parse_file(txt, slug, people, args.min_chars):
                fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
                n_posts += 1
                counts[rec["person"]] += 1
                dates.setdefault(rec["person"], []).append(rec["date"])
                topics[(rec["person"], rec["kind"])] += 1

    summary_path = pathlib.Path(args.summary)
    with summary_path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh)
        writer.writerow(["handle", "display_name", "records", "topics", "comments", "first_date", "last_date"])
        for person, n in counts.most_common():
            d = sorted(x for x in dates[person] if x)
            writer.writerow(
                [
                    person,
                    people[[k for k, v in people.items() if v["handle"] == person][0]]["display_name"],
                    n,
                    topics[(person, "topic")],
                    topics[(person, "comment")],
                    d[0] if d else "",
                    d[-1] if d else "",
                ]
            )
    print(f"roster: {roster_path.name} ({len({v['handle'] for v in people.values()})} people)")
    print(f"gm_posts: {n_posts} records -> {out_path}")
    print(f"summary: {len(counts)} people -> {summary_path}")
    for person, n in counts.most_common(10):
        print(f"  {person}: {n}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
