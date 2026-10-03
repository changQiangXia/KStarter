#!/usr/bin/env python3
"""检查已采集比赛的"最高票主题"是否遗漏，必要时补采。

背景：早期版本按标题关键词选正文，会漏掉标题不含关键词的冠军帖
（例如 "How on Earth did I win this competition?"）。脚本对比 topics.json
中票数最高的 2 条主题与 bodies/ 里的文件，列出需要补采的比赛。

用法：
    python repair_missing_top.py            # 只报告
    python repair_missing_top.py --fix      # 调 batch_collect 补采（--force）
"""

from __future__ import annotations

import argparse
import json
import pathlib
import subprocess

HERE = pathlib.Path(__file__).resolve().parent
INTEL = HERE.parent / "intel"
PYTHON = "/root/miniconda3/envs/kaggle/bin/python"


def affected() -> list[str]:
    slugs = []
    for directory in sorted(INTEL.iterdir()):
        if not (directory / "DONE").exists():
            continue
        # 情况 0：整场没有任何正文（限流导致的"假成功"）
        if not list((directory / "bodies").glob("*.html")):
            slugs.append(directory.name)
            continue
        topics_file = directory / "topics.json"
        if not topics_file.exists():
            continue
        topics = json.loads(topics_file.read_text())
        if not topics:
            continue
        top = sorted(topics, key=lambda t: -t["votes"])[:2]
        bodies = directory / "bodies"
        missing = [t for t in top if not (bodies / f"{t['id']}.html").exists()]
        if missing:
            slugs.append(directory.name)
    return slugs


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--fix", action="store_true")
    args = parser.parse_args()

    slugs = affected()
    print(f"需要补采：{len(slugs)} 场")
    for slug in slugs[:20]:
        print("  -", slug)
    if len(slugs) > 20:
        print(f"  …… 其余 {len(slugs) - 20} 场省略")

    if args.fix and slugs:
        subprocess.run(
            [PYTHON, str(HERE / "batch_collect.py"), "--slugs", ",".join(slugs),
             "--force", "--max-bodies", "8", "--pages", "6"],
            check=False,
        )


if __name__ == "__main__":
    main()
