#!/usr/bin/env python3
"""校验 notes/ 与 analysis/ 中 Markdown 图证相对路径是否存在（GitHub 可渲染性）。

- 只校验相对路径（外链 http(s) 一律跳过，符合"站外图床不下载"约束）。
- 相对路径以引用文件所在目录为基准解析。
"""

from __future__ import annotations

import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
IMG = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")


def main() -> None:
    checked = 0
    problems: list[str] = []
    for folder in ("notes", "analysis"):
        for md in sorted((ROOT / folder).rglob("*.md")):
            for target in IMG.findall(md.read_text()):
                if target.startswith(("http://", "https://")):
                    continue
                if "<" in target or ">" in target:  # 模板占位符（如 <slug>）跳过
                    continue
                checked += 1
                resolved = (md.parent / target.split("#")[0]).resolve()
                if not resolved.exists():
                    problems.append(f"{md.relative_to(ROOT)} -> {target}")
    print(f"检查相对图片路径 {checked} 条")
    if problems:
        print(f"发现 {len(problems)} 条无效：")
        for item in problems:
            print("  -", item)
        sys.exit(1)
    print("全部有效 ✅（GitHub 可渲染）")


if __name__ == "__main__":
    main()
