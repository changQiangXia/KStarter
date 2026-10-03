#!/usr/bin/env python3
"""把近 5 年比赛按主题分类（第二阶段基础设施）。

输出：
    ../data/themes.csv        每场比赛的主题、领域与判定依据
    ../data/themes_summary.md 主题分布概览

主题（方法维度，用于后续 playbook）：
    sim-agent  优化博弈 / agent / 模拟对战
    cv         计算机视觉
    nlp        NLP / LLM
    science    科学计算（生物、化学、医学、物理等）
    tabular    表格 / 时序
    audio      音频（BirdCLEF 一类，方法接近 CV 但不属于原六类）
    other      其他 / 多模态 / 非建模类

subtheme 记录更细的家族（reasoning、recsys、meta、tracking 等），
不改变六大主题的 playbook 划分。

领域（应用维度）单独记录，便于"按领域找参考"。
规则优先级：sim-agent > cv > nlp > science > tabular > other，
主题与领域冲突时（如医学影像）方法维度优先归入 cv，领域标记为医疗。
"""

from __future__ import annotations

import collections
import csv
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "data"

TAG_THEME = {
    "sim-agent": {
        # 注意：'games' / 'video games' 标签存在错标（如 RNA 折叠被打上 video games），
        # 因此只保留强信号标签，具体对战类比赛靠关键词命中。
        "simulations", "reinforcement learning", "optimization", "multi-agent",
    },
    "cv": {
        "image", "computer vision", "video", "segmentation", "object detection",
        "image classification", "image segmentation", "image text recognition",
    },
    "nlp": {
        "nlp", "text", "text generation", "text classification", "translation",
        "large language model", "llm", "natural language processing",
    },
    "science": {
        "biology", "chemistry", "physics", "medicine", "health", "healthcare",
        "biotechnology", "genetics", "astronomy", "materials", "neuroscience",
        "medical", "drug discovery",
    },
    "tabular": {
        "tabular", "time series analysis", "regression", "classification",
        "binary classification", "multiclass classification", "auc",
        "roc auc score", "mean squared error", "rmse", "forecasting",
    },
    "audio": {"audio", "speech", "music", "sound", "acoustic"},
}

KEYWORD_THEME = {
    "sim-agent": [
        r"battle", r"code[\s-]?golf", r"santa", r"maze", r"orbit[\s-]?wars",
        r"connectx", r"halite", r"game[\s-]?arena", r"ptcg", r"kaggriculture",
        r"agent(ic)?[\s-](battle|arena|challenge)", r"simulation",
    ],
    # "detection" 单独出现太宽（如 PII detection 是 NLP），必须是"目标检测"或配合视觉词
    "cv": [r"\bimage\b", r"segmentation", r"object detection", r"\bvideo\b", r"photo", r"vision"],
    "nlp": [r"\bllm\b", r"language model", r"translation", r"text", r"prompt", r"chat", r"gpt", r"gemma", r"gemini"],
    "science": [
        # 短词必须加词边界，否则会误命中（例如 rna 命中 "touRNAments"）
        r"protein", r"molecul", r"\bchem\w*", r"\bbio\w*", r"\bcell\w*", r"genom",
        r"\brna\b", r"\bdna\b", r"\bmedic\w*", r"\bhealth\w*", r"\becg\b", r"\beeg\b",
        r"physics", r"astronom", r"wellbore", r"geolog", r"climate", r"weather",
        r"seismic", r"cancer",
    ],
    "audio": [r"birdclef", r"speech", r"audio", r"acoustic", r"music"],
}

SUBTHEME_RULES = [
    ("reasoning", r"arc-prize|measuring-agi|konwinski|nemotron|mathematical-olympiad|ai-mathematical"),
    ("meta", r"kaggle-survey|ai-report|vibecoding|intensive-course"),
    ("recsys", r"recommender|recommendation|personalized-fashion"),
    ("tracking", r"nfl-big-data-bowl"),
    ("agent-safety", r"ai-agent-security|red-teaming"),
    ("tabular-ts", r"commodity|trading|forecast|sales|store|energy"),
]

# 规则无法覆盖时的人工判定（少量特例，附理由）
OVERRIDES = {
    "ai-agent-security-multi-step-tool-attacks": ("nlp", "agent-safety", "LLM 工具调用安全"),
    "autonomous-agent-prediction-beta": ("sim-agent", "agent", "自主 agent 行为预测"),
    "5-day-ai-agents-intensive-vibecoding-course-with-google": ("other", "meta", "课程活动"),
    "mitsui-commodity-prediction-challenge": ("tabular", "tabular-ts", "商品价格时序"),
    "make-data-count-finding-data-references": ("nlp", "document-ai", "学术文档信息抽取"),
    "neurips-2023-machine-unlearning": ("cv", "unlearning", "图像分类模型遗忘"),
    "predict-ai-model-runtime": ("other", "systems", "编译器/运行时性能预测"),
    "asl-fingerspelling": ("cv", "sign-language", "手语视频识别"),
    "kore-2022-beta": ("sim-agent", "agent-game", "对战 agent"),
    "2023-kaggle-ai-report": ("other", "meta", "调查报告"),
    "kaggle-survey-2022": ("other", "meta", "调查报告"),
    "kaggle-survey-2021": ("other", "meta", "调查报告"),
    "google-tunix-hackathon": ("other", "hackathon", "Tunix 微调黑客松（评审制）"),
    "ai-village-ctf": ("sim-agent", "agent-game", "AI agent 对抗（CTF）"),
    "ai-village-capture-the-flag-defcon31": ("sim-agent", "agent-game", "AI agent 对抗（夺旗）"),
    "gemini-3": ("other", "hackathon", "黑客松（评审制，非预测任务）"),
    "kaggle-measuring-agi": ("other", "hackathon", "基准设计黑客松（评审制）"),
    "openai-to-z-challenge": ("other", "hackathon", "黑客松（Kaggle 首届，评审制）"),
    "med-gemma-impact-challenge": ("other", "hackathon", "医疗 AI 应用黑客松（评审制）"),
    "openai-gpt-oss-20b-red-teaming": ("other", "hackathon", "红队挑战赛（评审制）"),
    "dfl-bundesliga-data-shootout": ("cv", "video-events", "视频事件识别（足球转播）"),
    "nfl-big-data-bowl-2026-analytics": ("other", "analytics", "分析赛道（评审制，非预测任务）"),
    "bigquery-ai-hackathon": ("other", "hackathon", "数据分析应用黑客松（评审制）"),
    "meta-kaggle-hackathon": ("other", "hackathon", "Meta Kaggle 数据洞察黑客松（评审制）"),
    "gemini-long-context": ("other", "hackathon", "Gemini 长上下文应用赛（评审制）"),
    "data-assistants-with-gemma": ("other", "hackathon", "Gemma 数据助手应用赛（评审制）"),
    "gemma-language-tuning": ("other", "hackathon", "Gemma 微调社区活动（非竞态）"),
    "google-gemma-3n-hackathon": ("other", "hackathon", "开源模型应用黑客松（评审制）"),
    "nfl-big-data-bowl-2024": ("other", "analytics", "评审制分析赛（擒抱主题报告，非预测任务）"),
    "nfl-big-data-bowl-2023": ("other", "analytics", "评审制分析赛（锋线球员评估，非预测任务）"),
    "nfl-big-data-bowl-2022": ("other", "analytics", "评审制分析赛（特勤组主题，非预测任务）"),
    "big-data-derby-2022": ("other", "analytics", "赛马分析赛（评审制，非预测任务）"),
    "llm-prompting-with-makersuite": ("other", "hackathon", "提示词工程设计赛（评审制）"),
}

DOMAIN_TAGS = {
    "医疗": {"medicine", "health", "healthcare", "medical", "biology"},
    "科学": {"chemistry", "physics", "astronomy", "materials", "biotechnology", "genetics"},
    "金融": {"finance", "economics"},
    "体育": {"sports", "football", "basketball", "soccer", "baseball", "cricket"},
    "教育": {"education", "primary and secondary schools"},
    "游戏": {"games", "video games", "artificial intelligence"},
}


def classify(competition: dict) -> tuple[str, str, str, str]:
    tags = {t.get("name", "").lower() for t in (competition.get("categories") or [])}
    text = " ".join(
        [
            competition.get("competitionName", ""),
            competition.get("title", ""),
            competition.get("briefDescription", "") or "",
        ]
    ).lower()
    slug = competition.get("competitionName", "")

    subtheme = next((name for name, pattern in SUBTHEME_RULES if re.search(pattern, slug)), "")

    if slug in OVERRIDES:
        theme, subtheme, reason = OVERRIDES[slug]
        return theme, "", subtheme, reason
    # NFL 数据碗 / 头盔识别 / 球员接触检测都是视频或图像任务，必须排在通用体育规则之前
    if re.search(r"nfl-big-data-bowl|helmet|player-contact", slug):
        return "cv", "体育", "tracking", "球员追踪（视频/图像）"
    if tags & {"sports", "basketball", "football", "soccer", "baseball", "cricket", "hockey", "tennis"}:
        return "tabular", "体育", "sports", "赛事结果预测（结构化数据）"
    if re.search(r"recommender|personalized-fashion", slug):
        return "tabular", "", "recsys", "推荐系统（结构化 + 嵌入）"

    def matched(theme: str) -> list[str]:
        hits = sorted(tags & TAG_THEME[theme])
        hits += [kw for kw in KEYWORD_THEME.get(theme, []) if re.search(kw, text)]
        return hits

    if subtheme == "meta":
        return "other", "meta", "", "非建模类（调查报告 / 课程）"
    if subtheme == "reasoning" and not matched("sim-agent"):
        return "nlp", "reasoning", "reasoning", "AI 推理类（LLM / 程序合成）"

    # 注意：audio 必须排在 science 之前——否则 "bioacoustics" 之类描述会命中 science 关键词
    for theme in ("sim-agent", "cv", "nlp", "audio", "science", "tabular"):
        hits = matched(theme)
        if hits:
            # 医疗/健康类的表格赛按方法归入 tabular，避免"科学计算"吸走过多的
            # 标准 GBDT/MLP 比赛；蛋白/化学/物理等结构类仍留在 science。
            if theme == "science":
                science_tags = tags & TAG_THEME["science"]
                tabular_tags = tags & TAG_THEME["tabular"]
                soft = {"health", "medicine", "healthcare", "medical"}
                if tabular_tags and science_tags and science_tags <= soft:
                    continue
                if tabular_tags and slug.startswith("playground-series"):
                    continue
            domain = next(
                (name for name, keys in DOMAIN_TAGS.items() if tags & keys), ""
            )
            return theme, domain, subtheme, ",".join(hits[:4])
    return "other", "", subtheme, ""


def main() -> None:
    competitions = {c["competitionName"]: c for c in json.loads((DATA / "competitions_all.json").read_text())}
    rows = list(csv.DictReader((DATA / "competitions_last5y.csv").open()))

    out = []
    for row in rows:
        competition = competitions.get(row["name"], {})
        theme, domain, subtheme, evidence = classify(competition)
        out.append(
            {
                "slug": row["name"],
                "title": row["title"],
                "category": row["category"],
                "theme": theme,
                "subtheme": subtheme,
                "domain": domain,
                "evidence": evidence,
                "teams": row["teams"],
                "deadline": row["deadline"],
                "metric": row["metric"],
                "code_only": row["code_only"],
                "reward_usd": row["reward_usd"],
            }
        )

    with (DATA / "themes.csv").open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(out[0].keys()))
        writer.writeheader()
        writer.writerows(out)

    by_theme = collections.Counter(r["theme"] for r in out)
    lines = ["# 近 5 年比赛主题分布", "", "| 主题 | 数量 | 代表比赛 |", "| --- | --- | --- |"]
    for theme, count in by_theme.most_common():
        examples = [r["slug"] for r in out if r["theme"] == theme][:3]
        lines.append(f"| {theme} | {count} | {', '.join(f'`{e}`' for e in examples)} |")
    lines += ["", "## 未归类（other）", ""]
    for r in out:
        if r["theme"] == "other":
            lines.append(f"- `{r['slug']}`（{r['category']}）")
    (DATA / "themes_summary.md").write_text("\n".join(lines) + "\n")

    print("主题分布:", dict(by_theme.most_common()))
    print("已写入 data/themes.csv 与 data/themes_summary.md")


if __name__ == "__main__":
    main()
