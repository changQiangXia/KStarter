#!/usr/bin/env python3
"""抓取单个 Kaggle 比赛的讨论区情报与公开 notebook 排名。

用法：
    /root/miniconda3/envs/kaggle/bin/python fetch_competition_intel.py <competition-slug> [选项]

选项：
    --pages N      讨论区翻页数（每页 20 条，默认 5，0 = 翻到没有为止）
    --bodies K     为前 K 个疑似 write-up 的主题抓正文（默认 3，0 = 不抓）
    --notebooks N  列出前 N 个按分数排序的公开 notebook（默认 10，0 = 不抓）

输出目录：../intel/<slug>/
    topics.json        讨论区主题索引（标题/票数/评论数/日期/链接）
    topics.md          可读的讨论区清单，标注疑似 write-up
    bodies/<id>.html   主题正文原始 HTML（含图片/代码块，内容完整）
    bodies/<id>.txt    正文 + 全部评论的纯文本版
    bodies/<id>_img/   正文内嵌图片（自动改写被墙的下载域名）
    notebooks.md       按票数排序的公开 notebook 列表

背景：Kaggle 讨论区 API 对比赛级论坛返回 403，但 CLI 自带的
`kaggle competitions topics` 子命令可以正常读取，本脚本基于它实现。
正文若用 CLI 的表格输出会丢失约一半内容（图片、代码块被压平），
因此正文改用 /api/v1/discussions/{id}/get 取原始 HTML。
"""

from __future__ import annotations

import argparse
import json
import pathlib
import re
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

KAGGLE = "/root/miniconda3/envs/kaggle/bin/kaggle"
OUT_ROOT = pathlib.Path(__file__).resolve().parent.parent / "intel"
TOKEN_PATH = pathlib.Path.home() / ".kaggle" / "access_token"
TOPIC_API = "https://www.kaggle.com/api/v1/discussions/{id}/get"

WRITEUP_PATTERN = re.compile(
    r"write[\s-]?up|solution|\d+(st|nd|rd|th)\s+place|first place|"
    r"winning|our approach|how we|gold medal|silver medal|bronze medal|working note",
    re.IGNORECASE,
)


def with_retry(func, *args, attempts: int = 4, base_delay: float = 2.0, **kwargs):
    """网络调用重试：指数退避，遇到 429/5xx 或超时不直接放弃。"""
    last_error = None
    for attempt in range(1, attempts + 1):
        try:
            return func(*args, **kwargs)
        except RateLimited as exc:
            last_error = exc
            if attempt < attempts:
                # 429 频繁出现时，长退避会浪费大量时间；改为较短的递进退避
                time.sleep(12 * attempt)
        except Exception as exc:  # noqa: BLE001 - 需要覆盖 urllib 与 subprocess 的各种异常
            last_error = exc
            if attempt < attempts:
                time.sleep(base_delay * attempt)
    raise last_error


class RateLimited(RuntimeError):
    """被 Kaggle 限流（HTTP 429）。"""


def run_cli(args: list[str]) -> str:
    result = subprocess.run([KAGGLE, *args], capture_output=True, text=True)
    if result.returncode != 0:
        # 抛异常而不是 sys.exit，好让上层重试；429 用更长的退避
        message = result.stderr.strip() or result.stdout.strip()
        if "429" in message or "Too Many Requests" in message:
            raise RateLimited(f"限流：kaggle {' '.join(args[:6])}")
        raise RuntimeError(f"命令失败：kaggle {' '.join(args[:6])}\n{message}")
    return result.stdout


def parse_json_output(text: str):
    """CLI 的 JSON 输出会在末尾附一行 'Next Page Token = N'，需要剥掉。"""
    end = text.rfind("]")
    if end == -1:
        return []
    return json.loads(text[: end + 1])


def fetch_topics(slug: str, pages: int) -> list[dict]:
    topics: list[dict] = []
    token = None
    page = 0
    while pages == 0 or page < pages:
        page += 1
        args = ["competitions", "topics", "list", "-c", slug, "-s", "top", "--format", "json"]
        if token:
            args += ["--page-token", token]
        text = with_retry(run_cli, args)
        topics += parse_json_output(text)
        match = re.search(r"Next Page Token\s*=\s*(\S+)", text)
        if not match:
            break
        token = match.group(1)
    # 接口按页返回局部排序，需要本地按票数全局排序
    topics.sort(key=lambda t: t["votes"], reverse=True)
    return topics


def fetch_body(slug: str, topic_id: int) -> str:
    return with_retry(run_cli, ["competitions", "topics", "show", str(topic_id)])


def fetch_topic_html(topic_id: int) -> dict:
    """取主题的原始 HTML，比 CLI 表格输出多出图片与代码块。"""
    token = TOKEN_PATH.read_text().strip()
    request = urllib.request.Request(
        TOPIC_API.format(id=topic_id),
        headers={"Authorization": f"Bearer {token}", "User-Agent": "Mozilla/5.0"},
    )
    def _get():
        try:
            with urllib.request.urlopen(request, timeout=40) as response:
                return json.load(response)["topic"]
        except urllib.error.HTTPError as exc:
            if exc.code == 429:
                raise RateLimited(f"限流：topic {topic_id}") from exc
            raise

    return with_retry(_get)


def rewrite_gcs_url(url: str) -> str:
    """www.googleapis.com 在部分网络不可达，改写到同源可用的 storage.googleapis.com。"""
    match = re.match(
        r"https://www\.googleapis\.com/download/storage/v1/b/([^/]+)/o/([^?]+)", url
    )
    if not match:
        return url
    bucket, obj = match.group(1), urllib.parse.unquote(match.group(2))
    return f"https://storage.googleapis.com/{bucket}/{urllib.parse.quote(obj)}"


def download_images(topic_id: int, html: str, out_dir: pathlib.Path) -> tuple[int, int]:
    urls = re.findall(r'<img[^>]+src="([^"]+)"', html)
    if not urls:
        return 0, 0
    image_dir = out_dir / f"{topic_id}_img"
    image_dir.mkdir(exist_ok=True)
    ok = 0
    consecutive_failures = 0
    for index, url in enumerate(urls, 1):
        # 熔断：本机网络对 Google 存储间歇不可达，连续失败时放弃其余图片，
        # 否则每张图最多等 40s 超时，图多的比赛会被拖到十几分钟。
        if consecutive_failures >= 3:
            print(f"    图片下载连续失败 {consecutive_failures} 次，跳过剩余 {len(urls) - index + 1} 张")
            break
        suffix = pathlib.Path(urllib.parse.urlparse(url).path).suffix or ".png"
        target = image_dir / f"{index:02d}{suffix}"
        try:
            request = urllib.request.Request(
                rewrite_gcs_url(url), headers={"User-Agent": "Mozilla/5.0"}
            )

            def _get():
                with urllib.request.urlopen(request, timeout=12) as response:
                    return response.read()

            target.write_bytes(with_retry(_get, attempts=2, base_delay=1.0))
            ok += 1
            consecutive_failures = 0
        except Exception as exc:  # noqa: BLE001 - 单张图片失败不应中断整篇
            consecutive_failures += 1
            print(f"    图片 {index} 下载失败：{type(exc).__name__}: {exc}")
    return ok, len(urls)


def fetch_notebooks(slug: str, limit: int, sort_by: str = "voteCount") -> list[dict]:
    text = run_cli(
        [
            "kernels",
            "list",
            "--competition",
            slug,
            "--sort-by",
            sort_by,
            "--page-size",
            str(max(20, limit)),
            "--format",
            "json",
        ]
    )
    return parse_json_output(text)[:limit]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("slug", help="比赛 slug，例如 rogii-wellbore-geology-prediction")
    parser.add_argument("--pages", type=int, default=3)
    parser.add_argument("--bodies", type=int, default=3)
    parser.add_argument("--notebooks", type=int, default=10)
    parser.add_argument("--notebook-sort", default="voteCount", choices=["voteCount", "scoreDescending", "hotness"])
    args = parser.parse_args()

    out_dir = OUT_ROOT / args.slug
    (out_dir / "bodies").mkdir(parents=True, exist_ok=True)

    print(f"抓取讨论区（最多 {args.pages} 页）……")
    topics = fetch_topics(args.slug, args.pages)
    for topic in topics:
        topic["url"] = f"https://www.kaggle.com/competitions/{args.slug}/discussion/{topic['id']}"
        topic["looks_like_writeup"] = bool(WRITEUP_PATTERN.search(topic["title"]))
    json.dump(topics, (out_dir / "topics.json").open("w"), ensure_ascii=False, indent=2)

    lines = [f"# {args.slug} 讨论区（按票数排序，共 {len(topics)} 条）", ""]
    for topic in topics:
        flag = "**write-up?**" if topic["looks_like_writeup"] else ""
        lines.append(
            f"- [{topic['title']}]({topic['url']}) — {topic['votes']} 票 / "
            f"{topic['commentCount']} 评论 / {topic['postDate'][:10]} {flag}"
        )
    (out_dir / "topics.md").write_text("\n".join(lines) + "\n")

    candidates = [t for t in topics if t["looks_like_writeup"]][: args.bodies]
    for topic in candidates:
        print(f"  抓正文：{topic['title'][:60]}")
        topic_id = topic["id"]
        detail = fetch_topic_html(topic_id)
        html = detail.get("content") or ""
        (out_dir / "bodies" / f"{topic_id}.html").write_text(html)
        # 正文 + 评论（评论树只在 CLI 输出里完整）
        comments = fetch_body(args.slug, topic_id)
        (out_dir / "bodies" / f"{topic_id}.txt").write_text(f"# {topic['url']}\n\n{comments}")
        if html:
            ok, total = download_images(topic_id, html, out_dir / "bodies")
            if total:
                print(f"    图片 {ok}/{total} 张")

    if args.notebooks:
        print("抓取公开 notebook 排名……")
        notebooks = fetch_notebooks(args.slug, args.notebooks, args.notebook_sort)
        lines = [f"# {args.slug} 公开 notebook（按 {args.notebook_sort}，前 {len(notebooks)} 个）", ""]
        for index, kernel in enumerate(notebooks, 1):
            lines.append(
                f"{index}. [{kernel['title']}](https://www.kaggle.com/code/{kernel['ref']}) — "
                f"{kernel['totalVotes']} 票 / 最后运行 {kernel['lastRunTime'][:10]}"
            )
        (out_dir / "notebooks.md").write_text("\n".join(lines) + "\n")

    print(f"完成，输出目录：{out_dir}")


if __name__ == "__main__":
    main()
