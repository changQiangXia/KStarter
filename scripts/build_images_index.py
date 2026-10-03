#!/usr/bin/env python3
"""生成 analysis/images_index.csv：归档图片的路径/来源/上下文/优先级索引。

扫描 intel/<slug>/bodies/<topic>_img/ 下的所有图片，并结合：
- analysis/deep/*.md 与 notes/**/*.md 中的 Markdown 内嵌（alt 文本 = 上下文，P1）；
- digests/<slug>.md 中对应 topic 小节里的 [图 N: ...] 占位符（P2）；
- 其余未使用图片（P3，多为装饰图）。
输出仓库根相对路径，便于在 GitHub 直接定位；嵌入用的 ../../ 形式可从
analysis/deep/ 或 notes/<theme>/ 推导。
"""

from __future__ import annotations

import csv
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
INTEL = ROOT / "intel"
EXT = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".bmp"}

IMG_EMBED = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")
FIG_PLACEHOLDER = re.compile(r"\[图\s*\d+:\s*([^\]]*)\]")
TOPIC_HEAD = re.compile(r"^###\s+(.+)$")
SRC_LINE = re.compile(r"来源：https://www\.kaggle\.com/competitions/([^/]+)/discussion/(\d+)")


def collect_embeds() -> dict[str, list[tuple[str, str]]]:
    """resolved image path -> [(md relative path, alt), ...]"""
    used: dict[str, list[tuple[str, str]]] = {}
    for folder in ("notes", "analysis"):
        for md in sorted((ROOT / folder).rglob("*.md")):
            for alt, target in IMG_EMBED.findall(md.read_text(encoding="utf-8", errors="ignore")):
                if target.startswith(("http://", "https://")):
                    continue
                resolved = (md.parent / target.split("#")[0]).resolve()
                used.setdefault(str(resolved), []).append(
                    (str(md.relative_to(ROOT)), alt.strip())
                )
    return used


def digest_topic_context(slug: str) -> dict[str, list[str]]:
    """topic id -> list of [图 ...] placeholder texts (in order) from digests/<slug>.md."""
    digest = ROOT / "digests" / f"{slug}.md"
    result: dict[str, list[str]] = {}
    if not digest.exists():
        return result
    topic: str | None = None
    for line in digest.read_text(encoding="utf-8", errors="ignore").splitlines():
        head = TOPIC_HEAD.match(line.strip())
        if head:
            topic = None
            continue
        m = SRC_LINE.search(line)
        if m:
            topic = m.group(2)
            result.setdefault(topic, [])
            continue
        for placeholder in FIG_PLACEHOLDER.findall(line):
            if topic:
                result.setdefault(topic, []).append(placeholder.strip())
    return result


def main() -> None:
    used = collect_embeds()
    rows: list[dict[str, str]] = []
    for img in sorted(INTEL.glob("*/bodies/*_img/*")):
        if img.suffix.lower() not in EXT or not img.is_file():
            continue
        slug = img.parts[-4]
        topic_dir = img.parts[-2]
        topic = topic_dir[: -len("_img")]
        rel = img.relative_to(ROOT).as_posix()
        embeds = used.get(str(img.resolve()), [])
        embedded_in = "|".join(sorted({p for p, _ in embeds}))
        alt = embeds[0][1] if embeds else ""

        ctx_by_topic = digest_topic_context(slug)
        placeholders = ctx_by_topic.get(topic, [])
        # 图片目录内文件按名称排序，第 k 张对应 digest 第 k 个 [图] 占位符
        siblings = sorted(
            p.name
            for p in (INTEL / slug / "bodies" / topic_dir).iterdir()
            if p.is_file() and p.suffix.lower() in EXT
        )
        rank = siblings.index(img.name) if img.name in siblings else 0
        digest_ctx = placeholders[rank] if rank < len(placeholders) else ""

        if embeds:
            priority = "P1"
        elif placeholders:
            priority = "P2"
        else:
            priority = "P3"

        context = alt or digest_ctx
        if img.suffix.lower() == ".gif":
            context = (context + " [GIF]").strip()
        elif img.suffix.lower() == ".webp":
            context = (context + " [WEBP]").strip()

        rows.append(
            {
                "path": rel,
                "slug": slug,
                "topic": topic,
                "source_url": f"https://www.kaggle.com/competitions/{slug}/discussion/{topic}",
                "format": img.suffix.lower().lstrip("."),
                "bytes": str(img.stat().st_size),
                "priority": priority,
                "context": re.sub(r"\s+", " ", context)[:300],
                "embedded_in": embedded_in,
            }
        )

    out = ROOT / "analysis" / "images_index.csv"
    with out.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    p1 = sum(1 for r in rows if r["priority"] == "P1")
    p2 = sum(1 for r in rows if r["priority"] == "P2")
    p3 = sum(1 for r in rows if r["priority"] == "P3")
    print(f"images_index.csv: {len(rows)} rows (P1={p1}, P2={p2}, P3={p3}) -> {out}")


if __name__ == "__main__":
    main()
