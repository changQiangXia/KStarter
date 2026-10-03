#!/usr/bin/env python3
"""抓取 Kaggle 竞赛榜前 N 名（默认 50）Grandmaster 名单快照。

数据源：Kaggle 内部接口 users.RankingService/GetUserRankingsV2（用 ~/.kaggle/access_token 认证）。
输出：people/roster/gm_top<N>_<YYYY-MM-DD>.csv + manifest.json（含 latest 指针）。
"""

from __future__ import annotations

import argparse
import csv
import json
import pathlib
import sys
import urllib.request
from datetime import date

ROOT = pathlib.Path(__file__).resolve().parents[2]
TOKEN_PATH = pathlib.Path.home() / ".kaggle" / "access_token"
URL = "https://www.kaggle.com/api/i/users.RankingService/GetUserRankingsV2"


def fetch(count: int) -> list[dict]:
    token = TOKEN_PATH.read_text().strip()
    payload = json.dumps({"type": "competitions", "pageSize": count, "page": 1}).encode()
    req = urllib.request.Request(
        URL,
        data=payload,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        data = json.loads(resp.read())
    return data.get("userRankings", [])


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--count", type=int, default=50)
    parser.add_argument("--out-dir", default=str(ROOT / "people" / "roster"))
    parser.add_argument("--date", default=date.today().isoformat())
    args = parser.parse_args()

    rows = fetch(args.count)
    if not rows:
        print("ERROR: 接口返回空名单", file=sys.stderr)
        return 1

    outdir = pathlib.Path(args.out_dir)
    outdir.mkdir(parents=True, exist_ok=True)
    snapshot = outdir / f"gm_top{args.count}_{args.date}.csv"
    fields = [
        "rank", "display_name", "handle", "user_id", "tier", "points",
        "gold", "silver", "bronze", "join_time", "user_url",
    ]
    with snapshot.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields)
        writer.writeheader()
        for r in rows:
            handle = (r.get("userUrl") or "").strip("/").split("/")[-1]
            writer.writerow(
                {
                    "rank": r.get("currentRanking"),
                    "display_name": r.get("displayName", ""),
                    "handle": handle,
                    "user_id": r.get("userId"),
                    "tier": r.get("tier", ""),
                    "points": r.get("points", ""),
                    "gold": r.get("totalGoldMedals", ""),
                    "silver": r.get("totalSilverMedals", ""),
                    "bronze": r.get("totalBronzeMedals", ""),
                    "join_time": r.get("joinTime", ""),
                    "user_url": "https://www.kaggle.com" + (r.get("userUrl") or ""),
                }
            )

    manifest_path = outdir / "manifest.json"
    manifest = {"latest": snapshot.name, "snapshots": []}
    if manifest_path.exists():
        manifest = json.loads(manifest_path.read_text())
    if snapshot.name not in manifest["snapshots"]:
        manifest["snapshots"].append(snapshot.name)
    manifest["latest"] = snapshot.name
    manifest["count"] = args.count
    manifest["updated"] = args.date
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"roster: {len(rows)} users -> {snapshot}")
    print(f"latest -> {manifest['latest']}")
    print("sample:", ", ".join(r.get("displayName", "") for r in rows[:5]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
