#!/usr/bin/env python3
"""生成人档：people/profiles/<handle>.md + analysis/people/OVERVIEW.md。

输入：people/roster 最新快照、people/competitions/gm_competitions.csv、people/posts/gm_posts.jsonl、
      data/competitions_last5y.csv（赛事元信息）
"""

from __future__ import annotations

import argparse
import csv
import json
import pathlib
import re
from collections import Counter, defaultdict

ROOT = pathlib.Path(__file__).resolve().parents[2]

KEYWORDS = {
    "GBDT 调参": r"xgboost|xgb|lgbm|lightgbm|catboost|gbdt|gradient boost",
    "神经网络": r"neural|nn\b|mlp|transformer|cnn|lstm|gru|attention|bert|deberta|vit",
    "集成/融合": r"ensembl|stack|blend|hill.?climb|加权|融合",
    "伪标签/蒸馏": r"pseudo.?label|distill|自训练|self.?train",
    "AutoML": r"automl|autogluon|flaml|auto.?sklearn",
    "特征工程": r"feature engineering|fe\b|target encod|embedding|tf.?idf|统计特征",
    "验证/CV": r"cross.?valid|cv\b|kfold|group.?kfold|holdout|leak|泄漏",
    "检索/度量": r"retriev|knn|arcface|metric learning|similarity|nearest",
    "LLM/提示": r"llm|prompt|gpt|gemma|gemini|lora|finetun|rag",
    "RL/搜索": r"reinforcement|ppo|self.?play|mcts|search|优化|heuristic",
    "后处理/校准": r"post.?process|calibrat|clip|threshold|isotonic|裁剪|校准",
}

# 比赛标签 -> 宽领域（一场比赛可命中多个领域，取并集后按场计数）
DOMAINS = {
    "视觉 CV": r"computer vision|image|video|object detection|segmentation",
    "文本 NLP": r"\bnlp\b|text|language|llm|sentiment|translation|question answering",
    "表格/结构化": r"tabular|binary classification|multiclass classification|regression|"
    r"roc auc|auc\b|rmse|mean squared error|accuracy score|classification",
    "时间序列": r"time series|forecast",
    "语音/音频": r"audio|speech|music",
    "生物/医疗": r"biology|health|medicine|medical|biotech|protein|genomic",
    "强化学习/博弈": r"reinforcement learning|games|video games|simulations|optimization",
    "科学研究": r"chemistry|physics|astronomy|research|science|climate|earth",
}


def domains_of(tags: str) -> set[str]:
    hits = set()
    for tag in (tags or "").split("|"):
        tag = tag.strip().lower()
        for name, pattern in DOMAINS.items():
            if re.search(pattern, tag):
                hits.add(name)
    return hits


def latest_roster(roster_dir: pathlib.Path) -> pathlib.Path:
    manifest = roster_dir / "manifest.json"
    if manifest.exists():
        latest = json.loads(manifest.read_text()).get("latest")
        if latest:
            return roster_dir / latest
    return sorted(roster_dir.glob("gm_top*.csv"))[-1]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--roster-dir", default=str(ROOT / "people" / "roster"))
    parser.add_argument("--competitions", default=str(ROOT / "people" / "competitions" / "gm_competitions.csv"))
    parser.add_argument("--posts", default=str(ROOT / "people" / "posts" / "gm_posts.jsonl"))
    parser.add_argument("--meta", default=str(ROOT / "data" / "competitions_last5y.csv"))
    parser.add_argument("--out-profiles", default=str(ROOT / "people" / "profiles"))
    parser.add_argument("--out-overview", default=str(ROOT / "analysis" / "people" / "OVERVIEW.md"))
    args = parser.parse_args()

    roster = list(csv.DictReader(latest_roster(pathlib.Path(args.roster_dir)).open(encoding="utf-8")))
    meta = {r["name"]: r for r in csv.DictReader(open(args.meta, encoding="utf-8"))}

    coverage_path = ROOT / "people" / "competitions" / "coverage.csv"
    cov_ok = cov_total = 0
    if coverage_path.exists():
        cov_rows = list(csv.DictReader(coverage_path.open(encoding="utf-8")))
        cov_total = len(cov_rows)
        cov_ok = sum(1 for r in cov_rows if r["status"] == "ok")

    comps = defaultdict(list)
    if pathlib.Path(args.competitions).exists():
        for r in csv.DictReader(open(args.competitions, encoding="utf-8")):
            comps[r["handle"]].append(r)
    posts = defaultdict(list)
    if pathlib.Path(args.posts).exists():
        for line in open(args.posts, encoding="utf-8"):
            if line.strip():
                rec = json.loads(line)
                posts[rec["person"]].append(rec)

    outdir = pathlib.Path(args.out_profiles)
    outdir.mkdir(parents=True, exist_ok=True)
    overview_rows = []

    for person in roster:
        handle = person["handle"]
        my_comps = sorted(comps.get(handle, []), key=lambda r: int(r["rank"]) if str(r["rank"]).isdigit() else 10**9)
        my_posts = sorted(posts.get(handle, []), key=lambda r: r.get("date", ""))

        kw_counts = Counter()
        for rec in my_posts:
            text = rec.get("text", "").lower()
            for name, pattern in KEYWORDS.items():
                if re.search(pattern, text):
                    kw_counts[name] += 1

        domain_counts = Counter()
        for r in my_comps:
            for d in domains_of(meta.get(r["slug"], {}).get("tags", "")):
                domain_counts[d] += 1

        lines = [f"# {person['display_name']}（@{handle}）", ""]
        lines.append(
            f"> 当前竞赛榜第 {person['rank']} 名 ｜ {person['tier']} ｜ 积分 {person['points']} ｜ "
            f"金/银/铜 {person['gold'] or 0}/{person['silver'] or 0}/{person['bronze'] or 0} ｜ "
            f"加入 {person['join_time'][:10]} ｜ [Kaggle 主页]({person['user_url']})"
        )
        lines.append("")
        lines.append("## 近 5 年归档战绩（公开榜匹配）")
        lines.append("")
        if my_comps:
            lines.append("| 比赛 | 类别 | 指标 | 名次 | 队伍数 | 分数 | 提交数 | 最后提交 |")
            lines.append("| --- | --- | --- | --- | --- | --- | --- | --- |")
            flagged = 0
            for r in my_comps:
                m = meta.get(r["slug"], {})
                valid = r.get("lb_quality", "ok") == "ok"
                if not valid:
                    flagged += 1
                lines.append(
                    f"| `{r['slug']}` | {m.get('category','')} | {m.get('metric','')} | "
                    f"{r['rank']}{'' if valid else ' ⚠'} | {m.get('teams','')} | {r['score']} | "
                    f"{r['submission_count']} | {r['last_submission']} |"
                )
            cats = Counter(meta.get(r["slug"], {}).get("category", "?") for r in my_comps)
            lines.append("")
            lines.append(
                f"共匹配 **{len(my_comps)}** 场；类别分布 " + "、".join(f"{k} {v}" for k, v in cats.most_common()) + "。"
            )
            if flagged:
                lines.append("")
                lines.append(
                    f"> ⚠ {flagged} 场公开榜分数全为 0（Kaggle 冻结榜），名次不可信、不计入统计。"
                )
            if domain_counts:
                lines.append("")
                lines.append(
                    "领域分布（按赛事标签）"
                    + "、".join(f"{k} {v}" for k, v in domain_counts.most_common(5))
                    + "。"
                )
        else:
            lines.append("_在归档的 264 场公开榜中没有匹配记录（可能未参加、使用团队账号或榜单不可下载）。_")
        lines.append("")

        lines.append("## 公开区言论（归档讨论区）")
        lines.append("")
        lines.append(
            f"共 **{len(my_posts)}** 条（主题 {sum(1 for r in my_posts if r['kind']=='topic')} / "
            f"评论 {sum(1 for r in my_posts if r['kind']=='comment')}）"
            + (f"，时间跨度 {my_posts[0]['date'][:10]} ~ {my_posts[-1]['date'][:10]}。" if my_posts else "。")
        )
        lines.append("")
        top_posts = sorted(my_posts, key=lambda r: r.get("votes", 0), reverse=True)[:8]
        if top_posts:
            lines.append("| 日期 | 类型 | 比赛 | 主题 | 票 | 摘录 |")
            lines.append("| --- | --- | --- | --- | --- | --- |")
            for r in top_posts:
                url = f"https://www.kaggle.com/competitions/{r['slug']}/discussion/{r['topic_id']}"
                excerpt = re.sub(r"\s+", " ", r.get("text", ""))[:130].replace("|", "/")
                title = r.get("topic_title", "").replace("|", "/")[:40]
                lines.append(
                    f"| {r.get('date','')[:10]} | {r['kind']} | `{r['slug']}` | [{title}]({url}) | "
                    f"{r.get('votes',0)} | {excerpt} |"
                )
            lines.append("")

        lines.append("## 方法关键词（公开言论）")
        lines.append("")
        if kw_counts:
            lines.append("、".join(f"**{k}** {v}" for k, v in kw_counts.most_common(10)))
        else:
            lines.append("_无公开言论可供关键词统计。_")
        lines.append("")
        lines.append(
            "> 自动生成；匹配规则：公开榜 `TeamMemberUserNames` 与讨论区作者名按 handle/显示名归一化匹配，"
            "仅覆盖 KStarter 归档的 264 场近 5 年比赛。"
        )
        (outdir / f"{handle}.md").write_text("\n".join(lines), encoding="utf-8")

        overview_rows.append(
            {
                "rank": int(person["rank"]),
                "handle": handle,
                "display_name": person["display_name"],
                "points": person["points"],
                "comps": len(my_comps),
                "best_rank": min(
                    (
                        int(r["rank"])
                        for r in my_comps
                        if r.get("lb_quality", "ok") == "ok" and str(r["rank"]).isdigit()
                    ),
                    default="",
                ),
                "posts": len(my_posts),
                "topics": sum(1 for r in my_posts if r["kind"] == "topic"),
                "top_kw": ", ".join(k for k, _ in kw_counts.most_common(3)),
                "domains": ", ".join(k for k, _ in domain_counts.most_common(3)),
            }
        )

    overview = [
        "# Kaggle 竞赛榜前 50：人档总览（2026-10 快照）",
        "",
        f"> 数据：竞赛榜前 50 名单 + 近 5 年 {cov_ok}/{cov_total} 场可下载公开榜匹配 + 归档讨论区公开发言。",
        "> 每个人的详细档案见 `people/profiles/<handle>.md`；抓取与生成脚本见 `scripts/people/`。",
        "",
        "| # | 选手 | 积分 | 匹配场次 | 最佳名次 | 领域 | 发言 | 主题 | 高频方法词 |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for r in sorted(overview_rows, key=lambda x: x["rank"]):
        overview.append(
            f"| {r['rank']} | [@{r['handle']}]({next(p['user_url'] for p in roster if p['handle']==r['handle'])}) "
            f"| {r['points']} | {r['comps']} | {r['best_rank']} | {r['domains']} | {r['posts']} | {r['topics']} | {r['top_kw']} |"
        )
    overview.append("")
    out = pathlib.Path(args.out_overview)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(overview), encoding="utf-8")
    print(f"profiles: {len(roster)} -> {outdir}")
    print(f"overview -> {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
