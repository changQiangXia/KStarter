#!/usr/bin/env python3
"""校验 notes/ 与 people/profiles/ 中所有 Kaggle 讨论链接是否对应该比赛的真实 topic id。

方法：从摘要里提取 discussion 链接，解析出 slug 与 topic id，再到
intel/<slug>/topics.json 中确认该 id 存在。防止凭记忆写错链接。
"""

from __future__ import annotations

import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SCAN_DIRS = (ROOT / "notes", ROOT / "people" / "profiles")
INTEL = ROOT / "intel"

LINK = re.compile(r"https://www\.kaggle\.com/competitions/([a-zA-Z0-9\-]+)/discussion/(\d+)")


def main() -> None:
    topic_cache: dict[str, set[int]] = {}
    problems: list[str] = []
    checked = 0

    notes = [p for d in SCAN_DIRS if d.exists() for p in sorted(d.rglob("*.md"))]
    for note in notes:
        text = note.read_text()
        for slug, topic_id in LINK.findall(text):
            checked += 1
            if slug not in topic_cache:
                topics_file = INTEL / slug / "topics.json"
                if topics_file.exists():
                    try:
                        topic_cache[slug] = {t["id"] for t in json.loads(topics_file.read_text())}
                    except (json.JSONDecodeError, KeyError):
                        topic_cache[slug] = set()
                else:
                    topic_cache[slug] = set()
            if not topic_cache[slug]:
                problems.append(f"{note.relative_to(ROOT)}: 找不到 {slug} 的 topics.json（无法校验）")
                continue
            if int(topic_id) not in topic_cache[slug]:
                problems.append(
                    f"{note.relative_to(ROOT)}: {slug} 中不存在 topic {topic_id}"
                )

    print(f"检查链接 {checked} 条")
    if problems:
        print(f"发现问题 {len(problems)} 条：")
        for item in problems:
            print("  -", item)
        sys.exit(1)
    print("全部通过 ✅")


if __name__ == "__main__":
    main()
