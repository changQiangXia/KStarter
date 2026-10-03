#!/usr/bin/env python3
"""把单场比赛的采集结果整理成便于分析的 digest（第二阶段输入）。

用法：
    /root/miniconda3/envs/kaggle/bin/python build_digest.py <slug> [<slug> ...]
    /root/miniconda3/envs/kaggle/bin/python build_digest.py --all-collected

输出：../digests/<slug>.md
    包含：比赛元信息、主题分类、讨论区索引、每篇 write-up 的正文纯文本
    （图片以 [图 N: 文件名] 占位，代码块保留为文本）
"""

from __future__ import annotations

import argparse
import csv
import html
import json
import pathlib
import re
from html.parser import HTMLParser

ROOT = pathlib.Path(__file__).resolve().parent.parent
INTEL = ROOT / "intel"
DIGESTS = ROOT / "digests"

SKIP_TAGS = {"script", "style"}
BLOCK_TAGS = {
    "p", "div", "br", "li", "tr", "h1", "h2", "h3", "h4", "h5", "h6",
    "pre", "blockquote", "table", "ul", "ol",
}


class HtmlToText(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []
        self.skip_depth = 0
        self.in_pre = False
        self.image_index = 0

    def handle_starttag(self, tag: str, attrs) -> None:
        if tag in SKIP_TAGS:
            self.skip_depth += 1
            return
        if tag == "img":
            self.image_index += 1
            src = dict(attrs).get("src", "")
            name = pathlib.Path(src.split("?")[0]).name or "image"
            self.parts.append(f"[图 {self.image_index}: {name}]")
            return
        if tag in BLOCK_TAGS:
            self.parts.append("\n")
        if tag == "pre":
            self.in_pre = True

    def handle_endtag(self, tag: str) -> None:
        if tag in SKIP_TAGS and self.skip_depth:
            self.skip_depth -= 1
            return
        if tag in BLOCK_TAGS:
            self.parts.append("\n")
        if tag == "pre":
            self.in_pre = False

    def handle_data(self, data: str) -> None:
        if self.skip_depth:
            return
        self.parts.append(data if self.in_pre else data)

    def text(self) -> str:
        raw = "".join(self.parts)
        raw = re.sub(r"[ \t]+", " ", raw)
        raw = re.sub(r"\n{3,}", "\n\n", raw)
        return raw.strip()


def html_to_text(source: str) -> str:
    parser = HtmlToText()
    parser.feed(source)
    return html.unescape(parser.text())


def load_metadata() -> dict[str, dict]:
    meta = {}
    for name in ("themes.csv", "competitions_last5y.csv"):
        path = ROOT / "data" / name
        for row in csv.DictReader(path.open()):
            key = row.get("slug") or row.get("name")
            meta.setdefault(key, {}).update(row)
    return meta


def build(slug: str, meta: dict) -> pathlib.Path:
    src = INTEL / slug
    topics = json.loads((src / "topics.json").read_text())
    info = meta.get(slug, {})

    lines = [f"# {slug}", ""]
    if info:
        lines += [
            f"- 类别：{info.get('category', '?')} ｜ 主题：{info.get('theme', '?')}"
            f" ｜ 子类：{info.get('subtheme') or '—'} ｜ 领域：{info.get('domain') or '—'}",
            f"- 截止：{info.get('deadline', '?')} ｜ 队伍数：{info.get('teams', '?')}"
            f" ｜ 机制：{'代码赛' if info.get('code_only') == 'True' else '标准赛'}",
            f"- 评估指标：{info.get('metric', '?')}",
            f"- 讨论区：{len(topics)} 条主题",
            "",
        ]

    lines += ["## 讨论区索引（按票数排序）", ""]
    for topic in topics:
        flag = "「write-up」" if topic.get("looks_like_writeup") else ""
        lines.append(
            f"- {topic['votes']} 票 / {topic['commentCount']} 评论 | {topic['title']} {flag}"
            f"\n  https://www.kaggle.com/competitions/{slug}/discussion/{topic['id']}"
        )
    lines.append("")

    bodies_dir = src / "bodies"
    html_files = sorted(
        bodies_dir.glob("*.html"), key=lambda p: p.stat().st_size, reverse=True
    )
    lines += [f"## write-up 正文（{len(html_files)} 篇）", ""]
    for path in html_files:
        title = next(
            (t["title"] for t in topics if str(t["id"]) == path.stem), path.stem
        )
        text = html_to_text(path.read_text())
        lines += [f"### {title}", "", f"来源：https://www.kaggle.com/competitions/{slug}/discussion/{path.stem}", "", text, "", "---", ""]

    DIGESTS.mkdir(exist_ok=True)
    target = DIGESTS / f"{slug}.md"
    target.write_text("\n".join(lines))
    return target


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("slugs", nargs="*")
    parser.add_argument("--all-collected", action="store_true")
    args = parser.parse_args()

    meta = load_metadata()
    slugs = args.slugs
    if args.all_collected:
        slugs = sorted(p.name for p in INTEL.iterdir() if (p / "DONE").exists())

    for slug in slugs:
        try:
            target = build(slug, meta)
            print(f"{slug} -> {target.relative_to(ROOT)} ({target.stat().st_size // 1024} KB)")
        except Exception as exc:
            print(f"{slug} 失败：{type(exc).__name__}: {exc}")


if __name__ == "__main__":
    main()
