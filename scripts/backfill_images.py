#!/usr/bin/env python3
"""为跳过图片的已采集比赛补下图片（第二阶段补采）。

背景：批量采集时使用 --skip-images 提速，DONE 标记里会写 images_skipped=true。
本脚本直接读取已落盘的 bodies/*.html 提取图片 URL，无需重新访问 Kaggle API，
因此不会受账号限流影响（图片来自 Google 存储，与 Kaggle API 配额无关）。

用法：
    python backfill_images.py                # 报告待补数量并处理全部
    python backfill_images.py --slugs a,b    # 只处理指定比赛
    python backfill_images.py --report       # 只报告不下载
    python backfill_images.py --limit 5      # 最多处理 5 场
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import pathlib
import time

HERE = pathlib.Path(__file__).resolve().parent
INTEL = HERE.parent / "intel"


def load_intel_module():
    spec = importlib.util.spec_from_file_location("intel", HERE / "fetch_competition_intel.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


intel = load_intel_module()


def needs_backfill(comp_dir: pathlib.Path) -> bool:
    marker = comp_dir / "DONE"
    if not marker.exists():
        return False
    try:
        record = json.loads(marker.read_text())
    except json.JSONDecodeError:
        return False
    return bool(record.get("images_skipped"))


def backfill_one(comp_dir: pathlib.Path) -> tuple[int, int]:
    """返回 (下载成功数, 涉及到的图片总数)。"""
    ok = total = 0
    for html_file in sorted((comp_dir / "bodies").glob("*.html")):
        image_dir = comp_dir / "bodies" / f"{html_file.stem}_img"
        if image_dir.exists() and any(image_dir.iterdir()):
            continue  # 已有图片，跳过
        got, count = intel.download_images(int(html_file.stem), html_file.read_text(), comp_dir / "bodies")
        ok += got
        total += count
        time.sleep(0.2)
    return ok, total


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--slugs", default="")
    parser.add_argument("--report", action="store_true")
    parser.add_argument("--limit", type=int, default=0)
    args = parser.parse_args()

    wanted = {s.strip() for s in args.slugs.split(",") if s.strip()}
    targets = [
        d for d in sorted(INTEL.iterdir())
        if d.is_dir() and needs_backfill(d) and (not wanted or d.name in wanted)
    ]
    print(f"待补图片的比赛：{len(targets)} 场")
    for directory in targets[:10]:
        print("  -", directory.name)
    if len(targets) > 10:
        print(f"  …… 其余 {len(targets) - 10} 场")
    if args.report or not targets:
        return

    if args.limit:
        targets = targets[: args.limit]
    done_ok = done_total = 0
    for index, directory in enumerate(targets, 1):
        ok, total = backfill_one(directory)
        done_ok += ok
        done_total += total
        print(f"[{index}/{len(targets)}] {directory.name}：图片 {ok}/{total}")
        if ok == 0 and total > 0:
            print("    （连续失败，可能是网络不可达，稍后再试或减少并发）")
    print(f"完成：成功下载 {done_ok} / 共 {done_total} 张")


if __name__ == "__main__":
    main()
