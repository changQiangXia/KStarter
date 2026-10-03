#!/usr/bin/env python3
"""抓取 Kaggle 全站比赛清单，输出全量与已结束两份数据文件。

用法：
    /root/miniconda3/envs/kaggle/bin/python fetch_competitions.py

输出：
    ../data/competitions_all.json   全站比赛（含进行中）
    ../data/competitions_ended.csv  仅已结束比赛，按截止日期倒序

凭证从 ~/.kaggle/access_token 读取，脚本不会打印 token。
注意：公开的 /api/v1 列表接口每页硬上限 20 条且翻页失效，
这里用的是 Kaggle 网站自身的分页接口（支持 pageToken）。
"""

from __future__ import annotations

import csv
import datetime as dt
import json
import pathlib
import time
import urllib.request

API = "https://www.kaggle.com/api/i/competitions.CompetitionService/ListCompetitions"
TOKEN_PATH = pathlib.Path.home() / ".kaggle" / "access_token"
OUT_DIR = pathlib.Path(__file__).resolve().parent.parent / "data"

SEGMENT = {
    1: "Featured",
    2: "Research",
    3: "Recruitment",
    5: "Getting Started",
    6: "Masters",
    8: "Playground",
    11: "Community",
}


def fetch_page(token: str, page_token: str | None, page_size: int = 200) -> dict:
    body: dict = {"pageSize": page_size}
    if page_token:
        body["pageToken"] = page_token
    request = urllib.request.Request(
        API,
        data=json.dumps(body).encode(),
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0",
        },
    )
    with urllib.request.urlopen(request, timeout=40) as response:
        return json.load(response)


def fetch_all(token: str) -> list[dict]:
    competitions: list[dict] = []
    page_token = None
    while True:
        payload = fetch_page(token, page_token)
        batch = payload.get("competitions", [])
        competitions.extend(batch)
        page_token = payload.get("nextPageToken")
        print(f"  累计 {len(competitions)}/{payload.get('totalResults')}")
        if not page_token or not batch:
            return competitions
        time.sleep(0.2)


def parse_date(value: str | None) -> dt.datetime | None:
    if not value:
        return None
    return dt.datetime.fromisoformat(value.replace("Z", "+00:00")).replace(tzinfo=None)


def to_rows(competitions: list[dict], now: dt.datetime) -> list[dict]:
    rows = []
    for comp in competitions:
        deadline = parse_date(comp.get("deadline"))
        if not deadline or deadline >= now:
            continue
        reward = comp.get("reward") or {}
        tags = [tag.get("name", "") for tag in (comp.get("categories") or [])]
        rows.append(
            {
                "name": comp["competitionName"],
                "title": comp["title"],
                "category": SEGMENT.get(comp["competitionHostSegmentId"], "?"),
                "deadline": deadline.strftime("%Y-%m-%d"),
                "year": deadline.year,
                "teams": comp.get("totalTeams") or 0,
                "reward_id": reward.get("id", ""),
                "reward_usd": reward.get("quantity") if reward.get("id") == "USD" else "",
                "metric": (comp.get("evaluationAlgorithm") or {}).get("name", ""),
                # fileBasedSubmissions 为空 + 有 notebook 提交 = 代码赛
                "code_only": (not comp.get("fileBasedSubmissions")) and bool(comp.get("hasScripts")),
                "has_solution": bool(comp.get("hasSolution")),
                "medals": bool(comp.get("medalsAllowed")),
                "max_team": comp.get("maxTeamSize"),
                "daily_subs": comp.get("maxDailySubmissions"),
                "host": comp.get("hostName", ""),
                "tags": "|".join(tags),
            }
        )
    rows.sort(key=lambda row: row["deadline"], reverse=True)
    return rows


def main() -> None:
    token = TOKEN_PATH.read_text().strip()
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    print("抓取全站比赛清单……")
    competitions = fetch_all(token)
    json.dump(competitions, (OUT_DIR / "competitions_all.json").open("w"), ensure_ascii=False)

    rows = to_rows(competitions, dt.datetime.now())
    with (OUT_DIR / "competitions_ended.csv").open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    print(f"全站 {len(competitions)} 场，已结束 {len(rows)} 场")
    print(f"已写入 {OUT_DIR}")


if __name__ == "__main__":
    main()
