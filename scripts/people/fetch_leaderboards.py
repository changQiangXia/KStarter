#!/usr/bin/env python3
"""按"人"批量抓取公开榜：把前 N GM 在近 5 年比赛中的名次/分数/提交映射出来。

- 原始 zip/CSV 只进缓存：data/cache/people_lb/（gitignore，不入库）
- 派生结果入库：people/competitions/gm_competitions.csv + summary.csv
"""

from __future__ import annotations

import argparse
import csv
import json
import pathlib
import re
import subprocess
import sys
import time
import zipfile
from collections import Counter

ROOT = pathlib.Path(__file__).resolve().parents[2]
KAGGLE = "/root/miniconda3/envs/kaggle/bin/kaggle"


def normalize(name: str) -> str:
    return re.sub(r"[^a-z0-9]", "", (name or "").lower())


def load_roster(path: pathlib.Path) -> tuple[dict[str, dict], list[dict]]:
    rows = list(csv.DictReader(path.open(encoding="utf-8")))
    index = {}
    for row in rows:
        for key in {normalize(row["handle"]), normalize(row["display_name"])}:
            if key:
                index[key] = row
    return index, rows


def latest_roster(roster_dir: pathlib.Path) -> pathlib.Path | None:
    manifest = roster_dir / "manifest.json"
    if manifest.exists():
        latest = json.loads(manifest.read_text()).get("latest")
        if latest and (roster_dir / latest).exists():
            return roster_dir / latest
    snaps = sorted(roster_dir.glob("gm_top*.csv"))
    return snaps[-1] if snaps else None


def download(slug: str, cache_dir: pathlib.Path, retries: int) -> tuple[str, pathlib.Path | None]:
    target = cache_dir / slug
    target.mkdir(parents=True, exist_ok=True)
    zips = sorted(target.glob("*.zip"))
    if not zips:
        for attempt in range(1, retries + 1):
            proc = subprocess.run(
                [KAGGLE, "competitions", "leaderboard", slug, "--download", "-p", str(target)],
                capture_output=True,
                text=True,
                timeout=180,
            )
            zips = sorted(target.glob("*.zip"))
            if zips and proc.returncode == 0:
                break
            time.sleep(2 * attempt)
    if not zips:
        return "no_zip", None
    zpath = zips[0]
    csvs = sorted(target.glob("*publicleaderboard*.csv"))
    if not csvs:
        try:
            with zipfile.ZipFile(zpath) as zf:
                zf.extractall(target)
        except zipfile.BadZipFile:
            return "bad_zip", None
        csvs = sorted(target.glob("*publicleaderboard*.csv"))
    if not csvs:
        return "no_csv", None
    return "ok", csvs[0]


def parse_leaderboard(path: pathlib.Path, slug: str, roster: dict[str, dict]):
    records = []
    with path.open(encoding="utf-8-sig", newline="") as fh:
        for row in csv.DictReader(fh):
            members = [m.strip() for m in (row.get("TeamMemberUserNames") or "").split(",") if m.strip()]
            for member in members:
                person = roster.get(normalize(member))
                if not person:
                    continue
                records.append(
                    {
                        "handle": person["handle"],
                        "display_name": person["display_name"],
                        "slug": slug,
                        "rank": row.get("Rank", ""),
                        "team_name": row.get("TeamName", ""),
                        "score": row.get("Score", ""),
                        "submission_count": row.get("SubmissionCount", ""),
                        "last_submission": row.get("LastSubmissionDate", ""),
                        "team_members": ",".join(members),
                    }
                )
    return records


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--roster", default="")
    parser.add_argument("--roster-dir", default=str(ROOT / "people" / "roster"))
    parser.add_argument("--competitions", default=str(ROOT / "data" / "competitions_last5y.csv"))
    parser.add_argument("--cache", default=str(ROOT / "data" / "cache" / "people_lb"))
    parser.add_argument("--out", default=str(ROOT / "people" / "competitions" / "gm_competitions.csv"))
    parser.add_argument("--summary", default=str(ROOT / "people" / "competitions" / "summary.csv"))
    parser.add_argument("--coverage", default=str(ROOT / "people" / "competitions" / "coverage.csv"))
    parser.add_argument("--slugs", default="")
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--sleep", type=float, default=0.7)
    parser.add_argument("--retries", type=int, default=2)
    parser.add_argument("--force", action="store_true", help="忽略缓存状态，重新下载")
    parser.add_argument("--rebuild-only", action="store_true", help="不下载，仅从缓存状态重建派生结果")
    args = parser.parse_args()

    roster_path = pathlib.Path(args.roster) if args.roster else latest_roster(pathlib.Path(args.roster_dir))
    if not roster_path or not roster_path.exists():
        print("ERROR: 找不到 roster，先运行 scripts/people/fetch_gm_roster.py", file=sys.stderr)
        return 1
    roster, roster_rows = load_roster(roster_path)

    if args.slugs:
        slugs = [s.strip() for s in args.slugs.split(",") if s.strip()]
    else:
        slugs = [r["name"] for r in csv.DictReader(open(args.competitions, encoding="utf-8"))]
    if args.limit:
        slugs = slugs[: args.limit]

    cache = pathlib.Path(args.cache)
    cache.mkdir(parents=True, exist_ok=True)
    state_path = cache / "_state.json"
    state = json.loads(state_path.read_text()) if state_path.exists() else {}

    status_counter = Counter()
    for i, slug in enumerate(slugs, 1):
        if args.rebuild_only:
            status_counter[state.get(slug, {}).get("status", "missing")] += 1
            continue
        if state.get(slug, {}).get("status") == "ok" and not args.force:
            status_counter["cached"] += 1
            continue
        status, csv_path = download(slug, cache, args.retries)
        if status == "ok" and csv_path:
            records = parse_leaderboard(csv_path, slug, roster)
            state[slug] = {"status": "ok", "csv": csv_path.name, "matched": len(records)}
            status_counter["ok"] += 1
        else:
            state[slug] = {"status": status}
            status_counter[status] += 1
        if i % 20 == 0 or i == len(slugs):
            state_path.write_text(json.dumps(state, ensure_ascii=False, indent=1), encoding="utf-8")
            print(f"[{i}/{len(slugs)}] {slug}: {state[slug]}")
        time.sleep(args.sleep)
    state_path.write_text(json.dumps(state, ensure_ascii=False, indent=1), encoding="utf-8")

    # 从缓存重建派生结果（确定性）
    all_records = []
    for slug, info in sorted(state.items()):
        if info.get("status") != "ok":
            continue
        csv_path = cache / slug / info["csv"]
        if csv_path.exists():
            all_records.extend(parse_leaderboard(csv_path, slug, roster))

    out_path = pathlib.Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fields = ["handle", "display_name", "slug", "rank", "team_name", "score", "submission_count", "last_submission", "team_members"]
    with out_path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields)
        writer.writeheader()
        writer.writerows(all_records)

    per_person = Counter(r["handle"] for r in all_records)
    per_slug = Counter(r["slug"] for r in all_records)

    coverage_path = pathlib.Path(args.coverage)
    with coverage_path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh)
        writer.writerow(["slug", "status", "matched_people", "matched_records"])
        for slug in slugs:
            info = state.get(slug, {})
            matched_people = len({r["handle"] for r in all_records if r["slug"] == slug})
            writer.writerow([slug, info.get("status", "missing"), matched_people, per_slug.get(slug, 0)])

    summary_path = pathlib.Path(args.summary)
    with summary_path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh)
        writer.writerow(["handle", "display_name", "competitions", "best_rank"])
        display = {r["handle"]: r["display_name"] for r in roster_rows}
        for handle, n in per_person.most_common():
            ranks = [int(r["rank"]) for r in all_records if r["handle"] == handle and str(r["rank"]).isdigit()]
            writer.writerow([handle, display.get(handle, ""), n, min(ranks) if ranks else ""])

    print(f"roster: {roster_path.name} ({len(roster_rows)} people)")
    print(f"slugs: {len(slugs)} | status: {dict(status_counter)}")
    print(f"matched records: {len(all_records)} | people: {len(per_person)} | competitions: {len(per_slug)}")
    print(f"coverage -> {coverage_path}")
    for handle, n in per_person.most_common(10):
        print(f"  {handle}: {n} competitions")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
