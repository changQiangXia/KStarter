#!/usr/bin/env python3
"""P3：按比赛领域生成 playbook 增量（条件→动作→机制→结果 + 复现证据）。

输出：analysis/people/playbooks/<domain>.md、analysis/people/PLAYBOOK_DOMAINS.md
"""

from __future__ import annotations

import argparse
import csv
import pathlib
import re
from collections import Counter, defaultdict

ROOT = pathlib.Path(__file__).resolve().parents[2]

PLAYBOOK_OF = {
    "视觉 CV": "playbook/cv.md",
    "文本 NLP": "playbook/nlp.md",
    "表格/结构化": "playbook/tabular.md",
    "科学研究": "playbook/science.md",
    "语音/音频": "playbook/multimodal-audio-other.md",
    "强化学习/博弈": "playbook/sim-agent.md",
}


def units_of(claims_rows):
    """证据单位：team_evidence 按（slug, team）合并。"""
    comps = ROOT / "people" / "competitions" / "gm_competitions.csv"
    team_of = {}
    if comps.exists():
        for row in csv.DictReader(comps.open(encoding="utf-8")):
            team_of[(row["handle"], row["slug"])] = row["team_name"] or ""
    units = {}
    for c in claims_rows:
        team = team_of.get((c["person"], c["slug"]), "")
        units[c["claim_id"]] = (
            f"team:{c['slug']}:{team}" if "team_evidence" in c["flags"] and team else f"person:{c['person']}"
        )
    return units


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--claims", default=str(ROOT / "people" / "claims" / "gm_claims.csv"))
    parser.add_argument("--tags", default=str(ROOT / "people" / "claims" / "gm_claim_tags.csv"))
    parser.add_argument("--out-dir", default=str(ROOT / "analysis" / "people" / "playbooks"))
    args = parser.parse_args()

    claims = list(csv.DictReader(open(args.claims, encoding="utf-8")))
    tags = {}
    for t in csv.DictReader(open(args.tags, encoding="utf-8")):
        tags[t["claim_id"]] = [x for x in t["tags"].split(";") if x]
    units = units_of(claims)

    domains = ["视觉 CV", "文本 NLP", "表格/结构化", "时间序列", "语音/音频", "生物/医疗", "强化学习/博弈", "科学研究"]
    out_dir = pathlib.Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    index = []

    for domain in domains:
        pool = [c for c in claims if domain in c["domain"]]
        tag_groups = defaultdict(list)
        for c in pool:
            for t in tags.get(c["claim_id"], []):
                tag_groups[t].append(c)

        lines = [
            f"# {domain}：前 50 选手决策增量（P3）",
            "",
            f"> 来源：`people/claims/gm_claims.csv` 中该领域的 {len(pool)} 条断言，按受控标签聚合；"
            "每条断言可经 `scripts/people/verify_claims.py` 回链原文。",
        ]
        if domain in PLAYBOOK_OF:
            lines.append(f"> 系统方法论见 `{PLAYBOOK_OF[domain]}`；本页只保留有跨人/跨队复现证据的决策项。")
        lines.append("")

        kept = []
        for tag, items in tag_groups.items():
            unit_count = len({units[i["claim_id"]] for i in items})
            ab = [i for i in items if i["evidence_level"] in ("A", "B")]
            if unit_count < 2 or not ab:
                continue
            kept.append((tag, unit_count, items, ab))
        kept.sort(key=lambda x: (-x[1], -len(x[2])))

        for tag, unit_count, items, ab in kept:
            best = sorted(ab, key=lambda c: ("A" != c["evidence_level"], -int(c["votes"])))[0]
            lines.append(f"## {tag}（证据单位 {unit_count}）")
            lines.append("")
            lines.append(
                f"- **条件**：{best['condition']}  \n"
                f"- **动作**：{best['action']}  \n"
                f"- **机制**：{best['mechanism']}  \n"
                f"- **结果**：{best['result']}  \n"
                f"- **证据**：[{best['claim_id']}]({best['source_url']})（@{best['person']}｜{best['evidence_level']}）"
            )
            others = [c for c in ab if c["claim_id"] != best["claim_id"]][:4]
            if others:
                lines.append(
                    "- 其他案例：" + "、".join(f"[@{c['person']}]({c['source_url']})" for c in others)
                )
            lines.append("")

        out = out_dir / f"{domain.replace('/', '_')}.md"
        out.write_text("\n".join(lines) + "\n", encoding="utf-8")
        index.append((domain, len(pool), len(kept)))

    idx = [
        "# 领域 playbook 增量索引（P3）",
        "",
        "> 每个领域页只保留跨 ≥2 证据单位、且含 A/B 级证据的决策项；系统方法论仍在 `playbook/`。",
        "",
        "| 领域 | 领域断言数 | 复现决策项 |",
        "| --- | --- | --- |",
    ]
    for domain, n_pool, n_kept in index:
        idx.append(f"| [{domain}](playbooks/{domain.replace('/', '_')}.md) | {n_pool} | {n_kept} |")
    (ROOT / "analysis" / "people" / "PLAYBOOK_DOMAINS.md").write_text("\n".join(idx) + "\n", encoding="utf-8")

    print("domain playbooks:")
    for domain, n_pool, n_kept in index:
        print(f"  {domain}: claims {n_pool} | replicated decision items {n_kept}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
