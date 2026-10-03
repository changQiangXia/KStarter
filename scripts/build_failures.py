#!/usr/bin/env python3
"""扫描 264 篇深读，抽取"失败学"与"悬案"条目 → analysis/failures.csv。

来源：
- 含"悬案/缺口/失败/无效/反例/不奏效"的小节全文；
- 全文中的负结果句子（含"无效/失败/未兑现/掉分/退化/没有提升"等关键词）。

分类：数据/标签、验证/CV、模型/训练、特征/后处理、平台/提交、评审/材料、复现/规模、其他。
"""

from __future__ import annotations

import csv
import json
import pathlib
import re
from collections import Counter

ROOT = pathlib.Path(__file__).resolve().parent.parent
DEEP = ROOT / "analysis" / "deep"

HEADING = re.compile(r"^(#{1,4})\s+(.*)$")
TOPIC_ID = re.compile(r"(?<![\d.])(\d{5,7})(?![\d.])")
SECTION_HINT = ("悬案", "缺口", "失败", "无效", "反例", "不奏效")
NEGATIVE = re.compile(
    r"无效|失败|未兑现|掉分|退化|没有提升|无提升|没提升|没有奏效|不予采用|被放弃|"
    r"did not work|didn't work|not work|没有收益|无收益|不奏效|反例|陷阱"
)
GENERIC = re.compile(r"^图证缺口|^凭证缺口|^本场 0/0|^本场 0 张|图片未内嵌|装饰")

CATEGORY_RULES = [
    ("数据/标签", r"数据|标签|重复|缺失|泄漏|偏移|分布|实体|ID|清洗|噪声|标注|口径|OOD|异常"),
    ("验证/CV", r"CV|交叉验证|验证|分组|GroupKFold|KFold|holdout|公榜|私榜|LB|leaderboard|线下"),
    ("模型/训练", r"模型|训练|RL|PPO|折叠|集成|骨干|损失|过拟合|欠拟合|学习率|蒸馏|伪标签"),
    ("特征/后处理", r"特征|后处理|校准|裁剪|阈值|融合|嵌入|PCA|编码|增强"),
    ("平台/提交", r"提交|平台|Kaggle|notebook|schema|API|额度|配额|超时|失败|deadline|截止"),
    ("评审/材料", r"评审|评委|write-?up|公告|评分|奖项|方案未|正文|归档|索引"),
    ("复现/规模", r"复现|算力|显存|内存|时间|规模|样本量|随机|种子|不可复现"),
]


def categorize(text: str) -> str:
    for cat, pattern in CATEGORY_RULES:
        if re.search(pattern, text, re.I):
            return cat
    return "其他"


def valid_ids(slug: str, text: str) -> list[str]:
    ids = sorted(set(TOPIC_ID.findall(text)))
    f = ROOT / "intel" / slug / "topics.json"
    if not f.exists():
        return ids
    try:
        valid = {str(t["id"]) for t in json.loads(f.read_text())}
    except Exception:
        return ids
    return [i for i in ids if i in valid]


def clean(line: str) -> str:
    text = line.strip()
    text = re.sub(r"^[-*+]\s+", "", text)
    text = re.sub(r"^\d+[.)]\s+", "", text)
    text = re.sub(r"^\|\s*", "", text)
    text = re.sub(r"\s*\|$", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def main() -> None:
    rows: list[dict[str, str]] = []
    for md in sorted(DEEP.glob("*.md")):
        slug = md.stem
        section = ""
        for raw in md.read_text(encoding="utf-8", errors="ignore").splitlines():
            m = HEADING.match(raw.strip())
            if m:
                section = m.group(2)
                continue
            line = raw.strip()
            if not line:
                continue
            in_gap = any(h in section for h in SECTION_HINT)
            if not (in_gap or NEGATIVE.search(line)):
                continue
            text = clean(line)
            if len(text) < 12 or GENERIC.search(text):
                continue
            if text.startswith("#") or re.fullmatch(r"[-|:\s]+", text):
                continue
            # 排除"证据分级"表里泛泛的"低/中"行
            if not in_gap and not NEGATIVE.search(text):
                continue
            ids = valid_ids(slug, text)
            rows.append(
                {
                    "slug": slug,
                    "category": categorize(text),
                    "statement": text[:400],
                    "section": section[:80],
                    "topic_ids": " ".join(ids),
                }
            )

    # 去重（同场 + 文本）
    seen = set()
    deduped = []
    for r in rows:
        key = (r["slug"], r["statement"])
        if key in seen:
            continue
        seen.add(key)
        deduped.append(r)

    out = ROOT / "analysis" / "failures.csv"
    with out.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(deduped[0].keys()))
        writer.writeheader()
        writer.writerows(deduped)

    print(f"failures.csv: {len(deduped)} rows -> {out}")
    print("category:", dict(Counter(r["category"] for r in deduped)))
    print("slugs:", len({r["slug"] for r in deduped}))


if __name__ == "__main__":
    main()
