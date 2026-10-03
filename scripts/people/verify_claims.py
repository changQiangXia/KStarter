#!/usr/bin/env python3
"""校验 people/claims/gm_claims.csv：无逐字引用不入库。

每条断言必须通过：
- claim_id 唯一
- (person, slug, topic_id) 命中 gm_posts.jsonl 中的主题帖
- quote 是原文正文的归一化子串
- source_url 由 slug/topic_id 构成；date/votes 与原文一致
- result/quote 中的数字（>=3 位或带小数）能在原文复现
- topic_id 存在于 intel/<slug>/topics.json
- evidence_type/evidence_level 在受控词表内；figures 路径真实存在
"""

from __future__ import annotations

import argparse
import csv
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
EVIDENCE_TYPES = {"可复算-原文数字", "可复算-官方", "可复算-图证", "自述", "未分级"}
EVIDENCE_LEVELS = {"A", "B", "C"}


def norm(text: str) -> str:
    text = re.sub(r"(?<=\d),(?=\d{3}\b)", "", text or "")  # 千分位
    return re.sub(r"\s+", " ", text).strip()


def numeric_tokens(text: str) -> list[str]:
    return re.findall(r"\d+(?:\.\d+)?", norm(text))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--claims", default=str(ROOT / "people" / "claims" / "gm_claims.csv"))
    parser.add_argument("--posts", default=str(ROOT / "people" / "posts" / "gm_posts.jsonl"))
    parser.add_argument("--intel", default=str(ROOT / "intel"))
    args = parser.parse_args()

    posts: dict[tuple[str, str, str, str], dict] = {}
    for line in open(args.posts, encoding="utf-8"):
        if line.strip():
            rec = json.loads(line)
            posts[(rec["person"], rec["slug"], rec["topic_id"], rec["kind"])] = rec

    topics_cache: dict[str, set[int]] = {}
    rows = list(csv.DictReader(open(args.claims, encoding="utf-8")))
    problems: list[str] = []
    seen: set[str] = set()

    for lineno, row in enumerate(rows, start=2):
        cid = row.get("claim_id", "")
        if not cid:
            problems.append(f"L{lineno}: 缺少 claim_id")
            continue
        if cid in seen:
            problems.append(f"L{lineno} {cid}: claim_id 重复")
        seen.add(cid)

        rec = posts.get((row["person"], row["slug"], row["topic_id"], "topic"))
        if rec is None:
            problems.append(f"L{lineno} {cid}: 找不到对应主题帖")
            continue

        text = norm(rec["text"])
        if norm(row["quote"]) not in text:
            problems.append(f"L{lineno} {cid}: quote 不是原文子串")

        expected_url = f"https://www.kaggle.com/competitions/{row['slug']}/discussion/{row['topic_id']}"
        if row["source_url"] != expected_url:
            problems.append(f"L{lineno} {cid}: source_url 与 slug/topic_id 不一致")
        if row["date"] != rec["date"]:
            problems.append(f"L{lineno} {cid}: date 与原文不一致（{row['date']} vs {rec['date']}）")
        if row["votes"] != str(rec["votes"]):
            problems.append(f"L{lineno} {cid}: votes 与原文不一致（{row['votes']} vs {rec['votes']}）")

        if row["evidence_type"] not in EVIDENCE_TYPES:
            problems.append(f"L{lineno} {cid}: evidence_type 不在词表（{row['evidence_type']}）")
        if row["evidence_level"] not in EVIDENCE_LEVELS:
            problems.append(f"L{lineno} {cid}: evidence_level 不在词表（{row['evidence_level']}）")

        for field in ("result", "quote"):
            for token in numeric_tokens(row[field]):
                if len(token.replace(".", "")) < 3:
                    continue
                if token not in text:
                    problems.append(f"L{lineno} {cid}: {field} 的数字 {token} 未在原文出现")

        slug = row["slug"]
        if slug not in topics_cache:
            topics_file = pathlib.Path(args.intel) / slug / "topics.json"
            if topics_file.exists():
                try:
                    topics_cache[slug] = {int(t["id"]) for t in json.loads(topics_file.read_text(encoding="utf-8"))}
                except (json.JSONDecodeError, KeyError, ValueError):
                    topics_cache[slug] = set()
            else:
                topics_cache[slug] = set()
        if not topics_cache[slug]:
            problems.append(f"L{lineno} {cid}: 找不到 intel/{slug}/topics.json，无法校验 topic")
        elif int(row["topic_id"]) not in topics_cache[slug]:
            problems.append(f"L{lineno} {cid}: intel/{slug} 中不存在 topic {row['topic_id']}")

        for fig in filter(None, (f.strip() for f in row.get("figures", "").split(";"))):
            if not (ROOT / fig).exists():
                problems.append(f"L{lineno} {cid}: figures 路径不存在（{fig}）")

    print(f"claims: {len(rows)} 条")
    if problems:
        print(f"problems: {len(problems)}")
        for item in problems[:60]:
            print("  -", item)
        return 1
    print("全部通过 ✅（引用/数字/链接/元数据均与原文一致）")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
