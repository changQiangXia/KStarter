#!/usr/bin/env python3
"""统计第二阶段摘要进度：每个主题下已写 / 待写的比赛。"""

from __future__ import annotations

import collections
import csv
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent


def main() -> None:
    rows = list(csv.DictReader((ROOT / "data" / "themes.csv").open()))
    written = {p.stem for theme_dir in (ROOT / "notes").iterdir() if theme_dir.is_dir()
               for p in theme_dir.glob("*.md")}
    collected = {p.name for p in (ROOT / "intel").iterdir() if (p / "DONE").exists()}

    by_theme = collections.defaultdict(lambda: {"total": 0, "written": 0, "collected": 0})
    for row in rows:
        entry = by_theme[row["theme"]]
        entry["total"] += 1
        entry["written"] += row["slug"] in written
        entry["collected"] += row["slug"] in collected

    print(f"{'主题':<12}{'已写':>6}{'已采集':>8}{'总数':>6}")
    for theme, entry in sorted(by_theme.items(), key=lambda x: -x[1]["total"]):
        print(f"{theme:<12}{entry['written']:>6}{entry['collected']:>8}{entry['total']:>6}")
    print(f"{'合计':<12}{len(written):>6}{len(collected):>8}{len(rows):>6}")

    pending = [r["slug"] for r in rows if r["slug"] in collected and r["slug"] not in written]
    if pending:
        print(f"\n已采集待写摘要（{len(pending)}）：{', '.join(pending[:10])}")


if __name__ == "__main__":
    main()
