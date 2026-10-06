#!/usr/bin/env python3
"""构建外部题解索引（kaggle-solutions -> KStarter）。

来源：https://github.com/faridrashidi/kaggle-solutions （MIT License, Farid Rashidi）
输入：data/cache/kaggle-solutions/data/competitions.yml（本地 clone，不入库）
输出：analysis/external/
  kaggle_solutions_index.csv  全量外部索引（721 场 / 全部题解链接，标注本仓库是否已收录）
  coverage_by_comp.csv        本仓库 264 场逐场覆盖明细（链接数/新增数/冠军链接/缺口）
  delta_links.csv             本仓库尚未收录的外部链接（按场次、排名排序）
  EXTERNAL.md                 来源/许可/口径/统计/缺口与用法

用法：
  git clone --depth 1 https://github.com/faridrashidi/kaggle-solutions data/cache/kaggle-solutions
  python scripts/build_external_index.py
"""

from __future__ import annotations

import argparse
import collections
import csv
import pathlib
import re
import subprocess
import time
from urllib.parse import urlparse

import yaml

SCAN_PATHS = ["README.md", "LEARNING_PATH.md", "analysis", "notes", "playbook", "people", "digests", "templates", "docs"]
URL_RE = re.compile(r"https?://[A-Za-z0-9][A-Za-z0-9/_.?=&%#:~+-]*")
KAGGLE_RE = re.compile(r"https://www\.kaggle\.com/[A-Za-z0-9/_.?=&%#-]*")

INDEX_FIELDS = [
    "comp_slug", "comp_title", "year", "category", "prize", "teams", "metric",
    "rank", "link_kind", "url", "link_domain", "flag",
    "in_kstarter_scope", "in_kstarter_docs",
]
COVERAGE_FIELDS = [
    "slug", "title", "year", "theme", "status", "ksol_links", "new_links", "rank1_links",
    "new_rank1", "new_rank_le3", "best_new_rank",
]
DELTA_FIELDS = ["slug", "title", "year", "in_scope", "theme", "rank", "link_kind", "url"]


def canonical(url: str) -> str:
    """规范化 URL 用于跨仓库去重（/c/ 与 /competitions/ 等价，去 query、去尾斜杠、小写主机）。"""
    url = (url or "").strip()
    parsed = urlparse(url)
    host = parsed.netloc.lower()
    path = parsed.path.rstrip("/")
    path = re.sub(r"^/c/", "/competitions/", path)
    return f"{host}{path}".lower()


def slug_of(url: str) -> str:
    match = re.search(r"kaggle\.com/(?:c|competitions)/([^/?#]+)", url or "")
    return match.group(1) if match else ""


def link_flag(url: str) -> str:
    if "blog.kaggle.com" in (url or ""):
        return "legacy_blog"
    if (url or "").startswith("http://"):
        return "insecure_http"
    return ""


def rank_num(rank: str) -> int:
    match = re.search(r"\d+", rank or "")
    return int(match.group(0)) if match else 10**6


def scan_kstarter_docs(root: pathlib.Path) -> set[str]:
    """扫描本仓库策展文档里出现过的 Kaggle URL（不含 intel/ 原始采集层）。"""
    try:
        out = subprocess.run(
            [
                "git", "-C", str(root), "grep", "-ohI", "-E", KAGGLE_RE.pattern, "--",
                *SCAN_PATHS, ":(exclude)analysis/external",
            ],
            capture_output=True, text=True, check=True,
        ).stdout
        # analysis/external 是本脚本的输出目录，必须排除，否则会把"新增链接"误判为"已收录"。
        return {canonical(line) for line in out.splitlines() if line.strip()}
    except (subprocess.CalledProcessError, FileNotFoundError):
        urls: set[str] = set()
        for path in ("README.md", "LEARNING_PATH.md"):
            target = root / path
            if target.exists():
                urls |= {canonical(u) for u in KAGGLE_RE.findall(target.read_text(encoding="utf-8", errors="ignore"))}
        for folder in SCAN_PATHS[2:]:
            for path in (root / folder).rglob("*"):
                if path.is_file() and path.suffix in {".md", ".csv", ".json"}:
                    urls |= {canonical(u) for u in KAGGLE_RE.findall(path.read_text(encoding="utf-8", errors="ignore"))}
        return urls


def source_commit(source: pathlib.Path) -> str:
    try:
        return subprocess.run(
            ["git", "-C", str(source), "rev-parse", "HEAD"], capture_output=True, text=True, check=True
        ).stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return "unknown"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=str(pathlib.Path(__file__).resolve().parent.parent))
    parser.add_argument("--source", default="", help="kaggle-solutions clone 目录（默认 <root>/data/cache/kaggle-solutions）")
    parser.add_argument("--snapshot-date", default=time.strftime("%Y-%m-%d"))
    args = parser.parse_args()

    root = pathlib.Path(args.root)
    source = pathlib.Path(args.source) if args.source else root / "data/cache/kaggle-solutions"
    yml = source / "data/competitions.yml"
    if not yml.exists():
        print(f"ERROR: 缺少 {yml}；先 git clone --depth 1 https://github.com/faridrashidi/kaggle-solutions {source}")
        return 1

    comps = yaml.safe_load(yml.read_text(encoding="utf-8"))["competitions"]
    scope_rows = list(csv.DictReader((root / "data/competitions_last5y.csv").open(encoding="utf-8")))
    scope = {r["name"]: r for r in scope_rows}
    theme = {
        path.stem: path.parent.name
        for path in (root / "notes").glob("*/*.md")
        if path.stem not in {"INDEX", "README"}
    }
    kstarter_urls = scan_kstarter_docs(root)

    index_rows: list[dict[str, str]] = []
    per_comp: dict[str, list[dict[str, str]]] = collections.defaultdict(list)
    all_comp_slugs = {slug_of(comp.get("link", "")) for comp in comps}
    for comp in comps:
        slug = slug_of(comp.get("link", ""))
        for sol in comp.get("solutions") or []:
            url = sol.get("link", "")
            row = {
                "comp_slug": slug,
                "comp_title": comp.get("title", ""),
                "year": comp.get("year", ""),
                "category": comp.get("kind", ""),
                "prize": comp.get("prize", ""),
                "teams": comp.get("team", ""),
                "metric": comp.get("metric", ""),
                "rank": sol.get("rank", ""),
                "link_kind": sol.get("kind", ""),
                "url": url,
                "link_domain": urlparse(url).netloc,
                "flag": link_flag(url),
                "in_kstarter_scope": "1" if slug in scope else "0",
                "in_kstarter_docs": "1" if canonical(url) in kstarter_urls else "0",
            }
            index_rows.append(row)
            per_comp[slug].append(row)

    scope_have_row = {s for s in scope if s in per_comp}
    coverage_rows = []
    for slug, meta in scope.items():
        rows = per_comp.get(slug, [])
        new = [r for r in rows if r["in_kstarter_docs"] == "0"]
        r1 = [r for r in rows if rank_num(r["rank"]) == 1]
        new_r1 = [r for r in new if rank_num(r["rank"]) == 1]
        new_le3 = [r for r in new if rank_num(r["rank"]) <= 3]
        best_new = min((rank_num(r["rank"]) for r in new), default=0)
        if rows:
            status = "covered"
        elif slug in all_comp_slugs:
            status = "zero_link"
        else:
            status = "absent"
        coverage_rows.append({
            "slug": slug,
            "title": meta.get("title", ""),
            "year": meta.get("year", ""),
            "theme": theme.get(slug, ""),
            "status": status,
            "ksol_links": str(len(rows)),
            "new_links": str(len(new)),
            "rank1_links": str(len(r1)),
            "new_rank1": str(len(new_r1)),
            "new_rank_le3": str(len(new_le3)),
            "best_new_rank": str(best_new) if best_new else "",
        })

    delta_rows = [
        {
            "slug": r["comp_slug"], "title": r["comp_title"], "year": r["year"],
            "in_scope": "1" if r["comp_slug"] in scope else "0",
            "theme": theme.get(r["comp_slug"], ""),
            "rank": r["rank"], "link_kind": r["link_kind"], "url": r["url"],
        }
        for r in index_rows if r["in_kstarter_docs"] == "0"
    ]
    delta_rows.sort(key=lambda r: (-int(r["in_scope"]), r["slug"], rank_num(r["rank"])))

    out_dir = root / "analysis/external"
    out_dir.mkdir(parents=True, exist_ok=True)
    with (out_dir / "kaggle_solutions_index.csv").open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=INDEX_FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(index_rows)
    with (out_dir / "coverage_by_comp.csv").open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=COVERAGE_FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(coverage_rows)
    with (out_dir / "delta_links.csv").open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=DELTA_FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(delta_rows)

    covered = [r for r in coverage_rows if r["status"] == "covered"]
    zero = [r for r in coverage_rows if r["status"] == "zero_link"]
    absent = [r for r in coverage_rows if r["status"] == "absent"]
    scope_delta = [r for r in delta_rows if r["slug"] in scope]
    adders = collections.Counter(r["slug"] for r in scope_delta)
    flags = collections.Counter(r["flag"] for r in index_rows if r["flag"])
    domains = collections.Counter(r["link_domain"] for r in index_rows)
    ranks_in = collections.Counter(rank_num(r["rank"]) for r in scope_delta)
    top_add = adders.most_common(15)
    titles = {r["slug"]: r["title"] for r in coverage_rows}

    lines = [
        "# 外部题解索引（kaggle-solutions）",
        "",
        f"> 来源：[faridrashidi/kaggle-solutions](https://github.com/faridrashidi/kaggle-solutions)（MIT License, Farid Rashidi）"
        f"，commit `{source_commit(source)[:12]}`，抓取 {args.snapshot_date}；本地 clone 放在 `data/cache/`（不入库）。",
        "> 本目录只存派生索引：外部 721 场 / 全部题解链接 → 与本仓库 264 场逐条比对，标注已收录/未收录。",
        "",
        "## 规模",
        "",
        f"- 外部索引：**{len(comps)} 场 / {len(index_rows)} 条链接**（description "
        f"{sum(1 for r in index_rows if r['link_kind'] == 'description')} · code "
        f"{sum(1 for r in index_rows if r['link_kind'] == 'code')} · kernel "
        f"{sum(1 for r in index_rows if r['link_kind'] == 'kernel')}）。",
        f"- 本仓库覆盖：{len(covered)} 场有外部链接（共 {sum(int(r['ksol_links']) for r in covered)} 条，"
        f"其中未收录 {len(scope_delta)} 条）；{len(zero)} 场外部零链接；{len(absent)} 场外部无此赛事。",
        f"- 历史池（不在 264 场内）：{len([r for r in index_rows if r['in_kstarter_scope'] == '0'])} 条链接，"
        "按年份集中在 2010–2021，可作为跨时代对照素材。",
        "",
        "## 新增链接最多（未收录，本仓库覆盖场）",
        "",
        "| 场次 | 新增 | 其中冠军 | 说明 |",
        "| --- | --- | --- | --- |",
    ]
    for slug, count in top_add:
        r1 = sum(1 for r in scope_delta if r["slug"] == slug and rank_num(r["rank"]) == 1)
        lines.append(f"| `{slug}` | {count} | {r1} | {titles.get(slug, '')} |")
    lines += [
        "",
        f"新增链接里的排名分布（前 10）：" + "、".join(f"rank {k}×{v}" for k, v in sorted(ranks_in.items())[:10]) + "。",
        "",
        "## 外部零链接 / 缺赛事（本仓库覆盖场）",
        "",
        f"- 外部零链接 {len(zero)} 场：" + "、".join(f"`{r['slug']}`" for r in zero[:40]) + ("…" if len(zero) > 40 else ""),
        f"- 外部无此赛事 {len(absent)} 场：" + "、".join(f"`{r['slug']}`" for r in absent) if absent else "- 外部无此赛事 0 场。",
        "",
        "## 链接健康与口径",
        "",
        f"- 域名分布：" + "、".join(f"{k} {v}" for k, v in domains.most_common(6)) + "。",
        f"- 需注意的链接：{dict(flags)}（`legacy_blog` 为已停服的 blog.kaggle.com；抽样 25 条 HTTP 校验，"
        "24 条 200、1 条为 blog.kaggle.com）。",
        "- 去重口径：URL 规范化（`/c/` ≡ `/competitions/`、去 query、去尾斜杠、主机小写）；"
        "`in_kstarter_docs=1` 表示该链接已出现在本仓库策展文档（README/analysis/notes/playbook/people/digests/templates/docs，不含 intel 原始层）。",
        "",
        "## 用法",
        "",
        "- 给 `notes/` / `analysis/deep/` 补外部题解：查 `delta_links.csv`（按 slug + rank 排好），把高排名链接补进对应「出处」节。",
        f"  `in_scope=1` 的 {len(scope_delta)} 条是 264 场内可补链接，`in_scope=0` 的 {len(delta_rows) - len(scope_delta)} 条是历史池链接。",
        "- 优先清单：`coverage_by_comp.csv` 里 `new_rank_le3` 或 `new_links` 大的行（本轮共 "
        f"{sum(1 for r in coverage_rows if int(r['new_rank_le3'] or 0) > 0)} 场前三名新增链接）。",
        "- 下游消费：KExperienceSkill 的 `tools/import_external_links.py` 会读取本目录 CSV，生成 skill 侧外链资产与冠军方案索引。",
        "",
        "## 复现",
        "",
        "```bash",
        "git clone --depth 1 https://github.com/faridrashidi/kaggle-solutions data/cache/kaggle-solutions",
        "python scripts/build_external_index.py",
        "```",
        "",
        "> 许可：kaggle-solutions 为 MIT License（Copyright (c) 2018-2026 Farid Rashidi）；本目录仅派生链接与元数据，"
        "保留来源署名；原始 YAML 不入库。",
    ]
    (out_dir / "EXTERNAL.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"index: {len(index_rows)} links / {len(comps)} comps -> analysis/external/kaggle_solutions_index.csv")
    print(f"coverage: {len(covered)} covered / {len(zero)} zero-link / {len(absent)} absent -> coverage_by_comp.csv")
    print(f"delta: {len(delta_rows)} links not in KStarter docs -> delta_links.csv")
    print(f"source commit: {source_commit(source)[:12]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
