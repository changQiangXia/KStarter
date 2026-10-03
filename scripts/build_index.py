#!/usr/bin/env python3
"""生成 notes/INDEX.md：按主题列出全部比赛及其摘要状态，便于导航。"""

from __future__ import annotations

import csv
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
NOTES = ROOT / "notes"

THEME_ORDER = ["tabular", "cv", "nlp", "science", "sim-agent", "audio", "other"]
THEME_LABEL = {
    "tabular": "表格 / 时序",
    "cv": "计算机视觉",
    "nlp": "NLP / LLM",
    "science": "科学计算",
    "sim-agent": "优化博弈 / Agent",
    "audio": "音频",
    "other": "其他 / 元类",
}


def main() -> None:
    rows = list(csv.DictReader((ROOT / "data" / "themes.csv").open()))
    written = {p.stem: p for theme_dir in NOTES.iterdir() if theme_dir.is_dir()
               for p in theme_dir.glob("*.md")}

    lines = [
        "# 比赛摘要总目录",
        "",
        f"> 共 {len(rows)} 场；已完成摘要 {len(written)} 场。本文件由 `scripts/build_index.py` 生成。",
        "",
        "## 按主题",
        "",
    ]
    for theme in THEME_ORDER:
        group = [r for r in rows if r["theme"] == theme]
        if not group:
            continue
        done = [r for r in group if r["slug"] in written]
        lines += [f"### {THEME_LABEL[theme]}（{len(done)}/{len(group)}）", ""]
        for row in sorted(group, key=lambda r: r["slug"]):
            slug = row["slug"]
            mark = "✅" if slug in written else "⏳"
            note_path = written.get(slug)
            link = f"`{note_path.relative_to(ROOT)}`" if note_path else ""
            lines.append(
                f"- {mark} `{slug}` — {row['category']} · {row['deadline']} · {row['teams']} 队"
                + (f" · {link}" if link else "")
            )
        lines.append("")

    lines += [
        "## 说明",
        "",
        "- ✅ = 已完成结构化摘要；⏳ = 已采集待写，或尚未采集。",
        "- 结论汇总见 `playbook/`（六册）与 `LEARNING_PATH.md`。",
        "- 原始材料在 `intel/<slug>/`（讨论区索引 + 正文 + 图片）。",
        "",
    ]
    (NOTES / "INDEX.md").write_text("\n".join(lines))
    print(f"已生成 notes/INDEX.md：{len(rows)} 场，其中 {len(written)} 场有摘要")


if __name__ == "__main__":
    main()
