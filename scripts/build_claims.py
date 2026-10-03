#!/usr/bin/env python3
"""生成 analysis/claims.csv：从 264 篇深读的"数字账"层抽取可量化断言。

覆盖范围（与 DEPTH_PLAN 的"全量可量化断言"对齐到可机械抽取的层）：
- Tier B：`## 1. 一句话重述与数字账` 下的"关键数字"表；
- Tier A：`## 4. 增量数字账` / "制胜增量识别（数字账）"等含"数字"小节里的表。

每行标注 evidence_type：
- 可复算-官方：来源/断言含"官方"
- 可复算-图证：来源含 _img / 图
- 自述：含"自述/作者称/估计"等
- 矛盾：含"矛盾/口径不一致/量纲"
- 可复算-原文数字：显式数字但来源为社区帖
- 未分级：其余
"""

from __future__ import annotations

import csv
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
DEEP = ROOT / "analysis" / "deep"
HEADING = re.compile(r"^(#{1,4})\s+(.*)$")
TOPIC_ID = re.compile(r"(?<![\d.])(\d{5,7})(?![\d.])")


def valid_topic_ids(slug: str, text: str) -> list[str]:
    """只接受 topics.json 中真实存在的 topic id，避免把分数误当 topic。"""
    import json

    ids = sorted(set(TOPIC_ID.findall(text)))
    topics_file = ROOT / "intel" / slug / "topics.json"
    if not topics_file.exists():
        return ids
    try:
        valid = {str(t["id"]) for t in json.loads(topics_file.read_text())}
    except Exception:
        return ids
    return [i for i in ids if i in valid]


def parse_tables(lines: list[str]):
    """yield (header_cells, row_cells) for consecutive |...| blocks."""
    block: list[list[str]] = []
    for line in lines + [""]:
        stripped = line.strip()
        if stripped.startswith("|") and stripped.endswith("|"):
            cells = [c.strip() for c in stripped.strip("|").split("|")]
            block.append(cells)
            continue
        if block:
            if len(block) >= 2:
                header = block[0]
                if not all(re.fullmatch(r":?-{2,}:?", c or "-") for c in block[1]):
                    for row in block[2:]:
                        yield header, row
                else:
                    for row in block[2:]:
                        yield header, row
            block = []


def index_of(cells: list[str], needles: tuple[str, ...]) -> int | None:
    for i, cell in enumerate(cells):
        if any(n in cell for n in needles):
            return i
    return None


def value_index(header: list[str]) -> int | None:
    """优先精确匹配"值/数字/变化"，避免把"关键数字"列误判为值列。"""
    for i, cell in enumerate(header):
        if cell in ("值", "数字", "变化", "数值", "数字/值", "增量", "指标值"):
            return i
    for i, cell in enumerate(header):
        if "关键数字" in cell:
            continue
        if "值" in cell or "数字" in cell:
            return i
    return None


def classify(claim: str, value: str, source: str) -> str:
    blob = f"{claim} {value} {source}"
    if re.search(r"矛盾|口径不一致|量纲|互相冲突|互斥", blob):
        return "矛盾"
    if "官方" in blob or "主办方" in blob or "host" in blob.lower():
        return "可复算-官方"
    if re.search(r"_img|图\s*\d|见.*图", blob):
        return "可复算-图证"
    if re.search(r"自述|作者称|作者估计|估计|猜测|推测", blob):
        return "自述"
    if re.search(r"\d", value):
        return "可复算-原文数字"
    return "未分级"


def main() -> None:
    rows: list[dict[str, str]] = []
    for md in sorted(DEEP.glob("*.md")):
        text = md.read_text(encoding="utf-8", errors="ignore")
        lines = text.splitlines()
        tier = "B" if any("Tier B" in l for l in lines[:4]) else "A"
        slug = md.stem
        section = ""
        buffer: list[str] = []
        sections: list[tuple[str, list[str]]] = []
        for line in lines:
            m = HEADING.match(line.strip())
            if m:
                if buffer:
                    sections.append((section, buffer))
                section = m.group(2)
                buffer = []
            else:
                buffer.append(line)
        if buffer:
            sections.append((section, buffer))

        for heading, body in sections:
            if "数字" not in heading and "增量" not in heading:
                continue
            for header, row in parse_tables(body):
                if len(row) < 2:
                    continue
                value_idx = value_index(header)
                source_idx = index_of(header, ("来源", "备注", "说明"))
                if value_idx is None:
                    value_idx = 1
                claim_idx = next(
                    (i for i in range(len(header)) if i not in {value_idx, source_idx}),
                    0,
                )
                cells = (row + [""] * len(header))[: len(header)]
                claim = cells[claim_idx]
                value = cells[value_idx]
                source = cells[source_idx] if source_idx is not None else ""
                blob = " ".join(cells)
                if not claim or not re.search(r"\d", blob):
                    continue
                ids = valid_topic_ids(slug, source)
                if not ids:
                    ids = valid_topic_ids(slug, claim)
                urls = " ".join(
                    f"https://www.kaggle.com/competitions/{slug}/discussion/{t}"
                    for t in ids
                )
                rows.append(
                    {
                        "slug": slug,
                        "tier": tier,
                        "claim": re.sub(r"\s+", " ", claim)[:300],
                        "value": re.sub(r"\s+", " ", value)[:300],
                        "source": re.sub(r"\s+", " ", source)[:200],
                        "evidence_type": classify(claim, value, source),
                        "topic_ids": " ".join(ids),
                        "source_urls": urls,
                    }
                )

    # 去重（同一场次 + 断言 + 值）
    seen = set()
    deduped = []
    for r in rows:
        key = (r["slug"], r["claim"], r["value"])
        if key in seen:
            continue
        seen.add(key)
        deduped.append(r)

    out = ROOT / "analysis" / "claims.csv"
    with out.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(deduped[0].keys()))
        writer.writeheader()
        writer.writerows(deduped)

    from collections import Counter

    print(f"claims.csv: {len(deduped)} rows -> {out}")
    print("evidence_type:", dict(Counter(r["evidence_type"] for r in deduped)))
    print("tier:", dict(Counter(r["tier"] for r in deduped)))


if __name__ == "__main__":
    main()
