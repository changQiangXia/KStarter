#!/usr/bin/env python3
"""查看批量采集进度：进程状态、已完成场次、主题/正文/图片数量与失败记录。"""

from __future__ import annotations

import csv
import json
import pathlib
import subprocess

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
INTEL = ROOT / "intel"
STATUS = INTEL / "_batch_status.jsonl"


def process_alive() -> str:
    result = subprocess.run(["pgrep", "-af", "batch_collect.py"], capture_output=True, text=True)
    lines = [l for l in result.stdout.splitlines() if "pgrep" not in l]
    return lines[0] if lines else "（未运行）"


def main() -> None:
    rows = list(csv.DictReader((ROOT / "data" / "competitions_last5y.csv").open()))
    done_dirs = {p.name for p in INTEL.iterdir() if (p / "DONE").exists()} if INTEL.exists() else set()

    records = []
    if STATUS.exists():
        for line in STATUS.read_text().splitlines():
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError:
                continue

    topics = sum(r.get("topics", 0) for r in records)
    bodies = sum(r.get("bodies", 0) for r in records)
    images = sum(r.get("images", 0) for r in records)
    failures = [r["slug"] for r in records if r.get("status") == "no_topics"]

    print(f"进程：{process_alive()}")
    print(f"完成：{len(done_dirs)} / {len(rows)} 场")
    print(f"累计：讨论主题 {topics} 条，正文 {bodies} 篇，图片 {images} 张")
    if failures:
        print(f"无讨论区（{len(failures)}）：{', '.join(failures[:8])}")

    remaining = [r["name"] for r in rows if r["name"] not in done_dirs]
    if remaining:
        print(f"下一批：{', '.join(remaining[:5])}")


if __name__ == "__main__":
    main()
