#!/usr/bin/env python3
"""批量采集近 5 年 Kaggle 比赛的 write-up 材料（第一阶段）。

对每场比赛：
  1. 抓讨论区索引（本地按票数全局排序）
  2. 识别疑似 write-up（标题关键词 + 票数阈值）
  3. 抓正文 HTML、全部评论、内嵌图片
  4. 写 <out>/DONE 标记，支持断点续跑

用法：
    /root/miniconda3/envs/kaggle/bin/python batch_collect.py [选项]

选项：
    --max-bodies N   每场最多抓多少篇正文（默认 8）
    --pages N        讨论区索引翻页上限，0 = 翻到底（默认 0）
    --limit N        本次最多处理多少场（默认全部）
    --sleep S        每场之间的间隔秒数（默认 2）
    --order MODE     value = Featured/Research 优先（默认），date = 按截止日期倒序
    --slugs A,B,C    只处理指定比赛（逗号分隔），用于补采
    --force          忽略已存在的 DONE 标记，重新采集
    --shard I/N      分片：只处理编号 % N == I 的比赛（I 从 1 开始），用于并行加速
    --threads K      场内并发线程数（同时抓多篇正文，默认 3）
    --skip-images    跳过图片下载（图片慢且本机网络不稳，可留到后续补采）

进度日志：../intel/_batch_progress.log 与 ../intel/_batch_status.jsonl
产出目录：../intel/<slug>/
"""

from __future__ import annotations

import argparse
import concurrent.futures
import csv
import importlib.util
import json
import pathlib
import time
import traceback

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
INTEL = ROOT / "intel"


def _load_intel_module():
    spec = importlib.util.spec_from_file_location(
        "intel", HERE / "fetch_competition_intel.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


intel = _load_intel_module()


def log(message: str) -> None:
    stamp = time.strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{stamp}] {message}"
    print(line, flush=True)
    with (INTEL / "_batch_progress.log").open("a") as handle:
        handle.write(line + "\n")


def load_targets(order: str) -> list[dict]:
    rows = list(csv.DictReader((ROOT / "data" / "competitions_last5y.csv").open()))
    if order == "value":
        priority = {"Featured": 0, "Research": 1, "Community": 2, "Playground": 3, "Getting Started": 4}
        rows.sort(key=lambda r: (priority.get(r["category"], 9), -int(r["teams"] or 0)))
    else:
        rows.sort(key=lambda r: r["deadline"], reverse=True)
    return rows


def shard_targets(rows: list[dict], shard: str) -> list[dict]:
    index, total = shard.split("/")
    index, total = int(index), int(total)
    if not 1 <= index <= total:
        raise SystemExit("--shard 参数格式应为 I/N，且 1 <= I <= N")
    return [row for position, row in enumerate(rows, 1) if position % total == index % total]


def collect_one(row: dict, args) -> dict:
    slug = row["name"]
    out_dir = INTEL / slug
    done_marker = out_dir / "DONE"
    if done_marker.exists() and not args.force:
        return {"slug": slug, "status": "skipped"}

    started = time.time()
    topics = intel.fetch_topics(slug, args.pages)
    stats = {"slug": slug, "category": row["category"], "topics": len(topics), "bodies": 0, "images": 0}
    if not topics:
        stats["status"] = "no_topics"
        return stats

    for topic in topics:
        topic["url"] = f"https://www.kaggle.com/competitions/{slug}/discussion/{topic['id']}"
        topic["looks_like_writeup"] = bool(intel.WRITEUP_PATTERN.search(topic["title"]))
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "topics.json").write_text(json.dumps(topics, ensure_ascii=False, indent=2))

    lines = [f"# {slug} 讨论区（按票数排序，共 {len(topics)} 条）", ""]
    for topic in topics:
        flag = "**write-up?**" if topic["looks_like_writeup"] else ""
        lines.append(
            f"- [{topic['title']}]({topic['url']}) — {topic['votes']} 票 / "
            f"{topic['commentCount']} 评论 / {topic['postDate'][:10]} {flag}"
        )
    (out_dir / "topics.md").write_text("\n".join(lines) + "\n")

    # 候选选择：高票主题（通常是冠军帖）+ 标题命中 write-up 的主题，合并后按票数取前 N。
    # 只靠标题会漏掉标题不含关键词的冠军帖（例如 "How on Earth did I win this competition?"）。
    by_votes = sorted(topics, key=lambda t: -t["votes"])
    mandatory = by_votes[:2]
    writeup_like = [t for t in by_votes if t["looks_like_writeup"]]
    combined, seen_ids = [], set()
    for topic in mandatory + writeup_like + by_votes:
        if topic["id"] in seen_ids:
            continue
        seen_ids.add(topic["id"])
        combined.append(topic)
        if len(combined) >= args.max_bodies:
            break
    candidates = combined

    bodies_dir = out_dir / "bodies"
    bodies_dir.mkdir(exist_ok=True)

    def fetch_candidate(topic: dict) -> tuple[int, int]:
        """抓单篇正文（HTML + 评论 + 图片），返回 (正文数, 图片数)。"""
        topic_id = topic["id"]
        if (bodies_dir / f"{topic_id}.html").exists():
            return 1, 0
        try:
            detail = intel.fetch_topic_html(topic_id)
            html = detail.get("content") or ""
            (bodies_dir / f"{topic_id}.html").write_text(html)
            comments = intel.fetch_body(slug, topic_id)
            (bodies_dir / f"{topic_id}.txt").write_text(f"# {topic['url']}\n\n{comments}")
            images = 0
            if html and not args.skip_images:
                ok, _total = intel.download_images(topic_id, html, bodies_dir)
                images = ok
            return 1, images
        except Exception as exc:  # 单篇失败不影响整场
            log(f"    ! {slug} topic {topic_id} 失败: {type(exc).__name__}: {exc}")
            return -1, 0  # -1 表示失败，稍后统一重试

    def run_pool(items: list[dict]) -> list[dict]:
        """跑一轮抓取，返回仍然失败的主题列表。"""
        failed: list[dict] = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=args.threads) as pool:
            for topic, (body_count, image_count) in zip(items, pool.map(fetch_candidate, items)):
                if body_count < 0:
                    failed.append(topic)
                    continue
                stats["bodies"] += body_count
                stats["images"] += image_count
        return failed

    failed = run_pool(candidates)
    if failed:
        log(f"    {slug}: {len(failed)} 篇失败，等待 30s 后重试")
        time.sleep(30)
        failed = run_pool(failed)
        if failed:
            log(f"    ! {slug}: 仍有 {len(failed)} 篇失败：{[t['id'] for t in failed]}")

    stats["status"] = "ok"
    stats["seconds"] = round(time.time() - started, 1)
    stats["images_skipped"] = bool(args.skip_images)
    done_marker.write_text(json.dumps(stats, ensure_ascii=False))
    return stats


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--max-bodies", type=int, default=8)
    parser.add_argument("--pages", type=int, default=0)
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--sleep", type=float, default=2.0)
    parser.add_argument("--order", choices=["value", "date"], default="value")
    parser.add_argument("--slugs", default="")
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--shard", default="")
    parser.add_argument("--threads", type=int, default=3)
    parser.add_argument("--skip-images", action="store_true")
    args = parser.parse_args()

    INTEL.mkdir(exist_ok=True)
    targets = load_targets(args.order)
    if args.shard:
        targets = shard_targets(targets, args.shard)
    if args.slugs:
        wanted = {s.strip() for s in args.slugs.split(",") if s.strip()}
        targets = [t for t in targets if t["name"] in wanted]
    if args.limit:
        targets = targets[: args.limit]

    log(
        f"开始批量采集：{len(targets)} 场，order={args.order}，"
        f"max_bodies={args.max_bodies}{'，force=True' if args.force else ''}"
        f"{'，shard=' + args.shard if args.shard else ''}，threads={args.threads}"
    )
    ok = failed = skipped = 0
    for index, row in enumerate(targets, 1):
        slug = row["name"]
        try:
            stats = collect_one(row, args)
        except Exception as exc:
            failed += 1
            log(f"[{index}/{len(targets)}] {slug} 异常: {type(exc).__name__}: {exc}")
            log(traceback.format_exc(limit=3))
            continue
        with (INTEL / "_batch_status.jsonl").open("a") as handle:
            handle.write(json.dumps(stats, ensure_ascii=False) + "\n")
        if stats["status"] == "skipped":
            skipped += 1
            continue
        ok += 1
        log(
            f"[{index}/{len(targets)}] {slug} — 主题 {stats.get('topics', 0)} / "
            f"正文 {stats.get('bodies', 0)} / 图片 {stats.get('images', 0)} / "
            f"{stats.get('seconds', '?')}s"
        )
        time.sleep(args.sleep)

    log(f"批次完成：成功 {ok}，跳过 {skipped}，失败 {failed}")


if __name__ == "__main__":
    main()
