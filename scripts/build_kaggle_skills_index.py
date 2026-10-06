#!/usr/bin/env python3
"""索引外部技能仓库 kei-kochiya/kaggle-skills（MIT）。

输入：data/cache/kaggle-skills（本地 clone，不入库）
输出：analysis/external/kaggle_skills_index.csv
  逐文件索引：路径 / 类别 / 标题 / 行数 / 主要小节 / 本仓库映射 / 处置状态

用法：
  git clone --depth 1 https://github.com/kei-kochiya/kaggle-skills.git data/cache/kaggle-skills
  python scripts/build_kaggle_skills_index.py
"""

from __future__ import annotations

import argparse
import csv
import pathlib
import subprocess
import time

SKILL_REPO = "https://github.com/kei-kochiya/kaggle-skills"

# 外部文件 -> 本仓库去向（已蒸馏/交叉引用）
MAPPING = [
    ("Handbook/workflows/llm-agentic-kaggle-workflow.md", "KExperienceSkill references/agent-kaggle-playbook.md", "已蒸馏（角色矩阵/7 阶段/护栏/审计）"),
    (".agent/skills/kaggle-tabular-playbook/references/", "KExperienceSkill references/tabular-advanced-recipes.md", "已蒸馏（CIR/FFT-AUC/base_margin/Fréchet/lexrank…）"),
    (".agent/skills/kaggle-rl-simulation/references/", "KExperienceSkill references/sim-engineering.md", "已蒸馏（加速/架构/联赛/量化部署）"),
    (".agent/skills/kaggle-tabular-playbook/SKILL.md", "KExperienceSkill references/tabular-advanced-recipes.md", "已蒸馏（总览）"),
    (".agent/skills/kaggle-rl-simulation/SKILL.md", "KExperienceSkill references/sim-engineering.md", "已蒸馏（总览）"),
    (".agent/skills/kaggle-competition-distiller/SKILL.md", "KStarter analysis/SOP.md §9", "参考（蒸馏流程对照）"),
    ("Handbook/reinforcement-learning/simulation-competition-starter.md", "KExperienceSkill references/sim-engineering.md", "已蒸馏（选型表 + 开赛清单）"),
]
SLUG_MAP = {
    "playground-s6e1-exam-score": "playground-series-s6e1",
    "playground-s6e2-heart-disease": "playground-series-s6e2",
    "playground-s6e3-customer-churn": "playground-series-s6e3",
    "playground-s6e5-f1-pit-stops": "playground-series-s6e5",
    "playground-s6e9-will-buy-ev": "playground-series-s6e9",
    "playground-s6e10-airline-satisfaction": "",
    "orbit-wars": "orbit-wars",
    "maze-crawler": "maze-crawler",
    "kaggriculture": "",
}
FIELDS = ["path", "track", "kind", "title", "lines", "top_headings", "our_mapping", "status"]


def source_commit(source: pathlib.Path) -> str:
    try:
        return subprocess.run(
            ["git", "-C", str(source), "rev-parse", "HEAD"], capture_output=True, text=True, check=True
        ).stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return "unknown"


def classify(rel: str) -> tuple[str, str]:
    if rel.startswith(".agent/skills/"):
        parts = rel.split("/")
        return "agent-skill", parts[2] if len(parts) > 2 else ""
    if rel.startswith("Handbook/workflows/"):
        return "workflow", "workflows"
    if rel.startswith("Handbook/tabular/"):
        return "handbook", "tabular"
    if rel.startswith("Handbook/reinforcement-learning/"):
        return "handbook", "reinforcement-learning"
    if rel in ("README.md", "Handbook/README.md"):
        return "catalog", ""
    return "other", ""


def mapping_for(rel: str) -> tuple[str, str]:
    for prefix, target, status in MAPPING:
        if rel.startswith(prefix):
            return target, status
    name = pathlib.Path(rel).stem
    if rel.startswith("Handbook/tabular/"):
        slug = SLUG_MAP.get(name, "")
        return (f"KStarter notes/<theme>/{slug}.md" if slug else "—（不在 264 场内）"), ("已覆盖" if slug else "未覆盖")
    if rel.startswith("Handbook/reinforcement-learning/"):
        slug = SLUG_MAP.get(name, "")
        return (f"KStarter notes/sim-agent/{slug}.md" if slug else "—"), ("已覆盖" if slug else "未覆盖")
    return "—", "参考"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=str(pathlib.Path(__file__).resolve().parent.parent))
    parser.add_argument("--source", default="", help="默认 <root>/data/cache/kaggle-skills")
    args = parser.parse_args()

    root = pathlib.Path(args.root)
    source = pathlib.Path(args.source) if args.source else root / "data/cache/kaggle-skills"
    if not source.exists():
        print(f"ERROR: 缺少 {source}；先 git clone --depth 1 {SKILL_REPO}.git {source}")
        return 1

    rows = []
    for path in sorted(source.rglob("*.md")):
        rel = path.relative_to(source).as_posix()
        if rel.startswith(".git/"):
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        lines = text.splitlines()
        title = next((l[2:].strip() for l in lines if l.startswith("# ")), path.stem)
        headings = [l.lstrip("# ").strip() for l in lines if l.startswith(("## ", "### "))]
        kind, track = classify(rel)
        target, status = mapping_for(rel)
        rows.append({
            "path": rel,
            "track": track,
            "kind": kind,
            "title": title[:120],
            "lines": str(len(lines)),
            "top_headings": " | ".join(headings[:4])[:200],
            "our_mapping": target,
            "status": status,
        })

    out_dir = root / "analysis/external"
    out_dir.mkdir(parents=True, exist_ok=True)
    with (out_dir / "kaggle_skills_index.csv").open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    print(f"index: {len(rows)} files -> analysis/external/kaggle_skills_index.csv")
    print(f"source commit: {source_commit(source)[:12]} | snapshot {time.strftime('%Y-%m-%d')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
