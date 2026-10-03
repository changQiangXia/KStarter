#!/usr/bin/env python3
"""由 analysis/claims.csv 生成 analysis/evidence_map.md：
把 THEORY 的 Tier B 新规律（L114–L133）与新张力（T28–T37）映射到具体数字证据，
并给七册 playbook 提供"数字锚点"表。
"""

from __future__ import annotations

import csv
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
CLAIMS = ROOT / "analysis" / "claims.csv"
OUT = ROOT / "analysis" / "evidence_map.md"

EVIDENCE_RANK = {
    "可复算-官方": 5,
    "可复算-图证": 4,
    "可复算-原文数字": 3,
    "自述": 2,
    "矛盾": 1,
    "未分级": 0,
}

L_RULES = {
    "L114 指标结构套利": (["MedAE", "中位", "样本权重", "档位", "0.25"], ["playground-series-s3e25", "playground-series-s3e8"]),
    "L115 目标随机性检验": (["随机目标", "打乱", "z", "随机数", "合成"], ["playground-series-s5e9", "playground-series-s5e2", "playground-series-s4e12"]),
    "L116 实体块切分/分组 CV": (["GroupKFold", "分组", "昵称", "hospital_number", "实体", "玩家历史"], ["scrabble-player-rating", "playground-series-s3e22", "playground-series-s3e9"]),
    "L117 评审闭环": (["闭环", "消融", "失败路径", "牌组", "write-up", "观察"], ["pokemon-tcg-ai-battle-challenge-strategy", "nfl-big-data-bowl-2023", "nfl-big-data-bowl-2024"]),
    "L118 评审可信度工程": (["盲样", "复现", "评委", "召回", "145", "artifact"], ["openai-gpt-oss-20b-red-teaming", "bigquery-ai-hackathon", "pokemon-tcg-ai-battle-challenge-strategy"]),
    "L119 危害增量判定": (["reasoning_effort", "CoT", "工具", "通道", "越狱", "危害"], ["openai-gpt-oss-20b-red-teaming"]),
    "L120 分层学习率": (["学习率", "scheduler", "warmup", "LayerNorm", "微调"], ["planttraits2024"]),
    "L121 身份辅助任务": (["物种", "三头", "软分类", "17,396", "标签链", "身份"], ["planttraits2024"]),
    "L122 提交契约": (["列顺序", "images.zip", "validate_submission", "agent.yaml", "提交按钮", "schema"], ["planttraits2024", "gan-getting-started", "autonomous-agent-prediction-beta", "bigquery-ai-hackathon"]),
    "L123 平台能力配给": (["预算", "额度", "$2", "$300", "配额", "地区", "Save", "TPU"], ["bigquery-ai-hackathon", "gemini-long-context", "autonomous-agent-prediction-beta", "llm-prompting-with-makersuite", "openai-to-z-challenge"]),
    "L124 RL 课程+热启动": (["16x16", "32x32", "64x64", "80m", "80M", "课程", "checkpoint"], ["lux-ai-season-2-neurips-stage-2"]),
    "L125 RL 收益拐点": (["KL", "金属", "metal", "拐点", "早停", "产量"], ["lux-ai-season-2-neurips-stage-2"]),
    "L126 规则优先/RL 局部化": (["规则", "Q-learning", "DQN", "PPO", "BC", "行为克隆"], ["kore-2022-beta", "maze-crawler", "lux-ai-season-2-neurips-stage-2"]),
    "L127 近镜像鲁棒性": (["镜像", "bunterrrr", "53/47", "rating", "对手"], ["maze-crawler"]),
    "L128 密度分层后处理": (["密度", "8", "NMS", "阈值", "计数", "MAP"], ["iwildcam2022-fgvc9"]),
    "L129 域适应组合": (["IBN", "直方图", "1024", "960", "ArcFace", "TTA", "遮挡"], ["sorghum-id-fgvc-9", "hotel-id-to-combat-human-trafficking-2022-fgvc9"]),
    "L130 标签病态松弛": (["block-label", "邻域", "presence", "长尾", "换标", "多标签"], ["geolifeclef-2022-lifeclef-2022-fgvc9", "geolifeclef-2024"]),
    "L131 原数据先对抗验证": (["对抗验证", "原数据", "adversarial", "分布一致"], ["playground-series-s3e18"]),
    "L132 LLM 验证义务": (["幻觉", "核验", "引用", "LLM 辅助", "JAX", "RAG"], ["openai-to-z-challenge", "maze-crawler", "data-assistants-with-gemma"]),
    "L133 评审赛激励设计": (["中期奖", "swag", "开源", "补充数据", "AMA", "引用"], ["data-assistants-with-gemma", "nfl-big-data-bowl-2026-analytics", "playground-series-s3e25"]),
}

T_TENSIONS = {
    "T28 随机目标 vs 合成痕迹": (["随机目标", "z=-0.83", "合成", "彩票", "生成痕迹"], ["playground-series-s5e9", "playground-series-s5e2"]),
    "T29 多目标拆 vs 合": (["EC1", "EC2", "多输出", "MultiOutput", "两场比赛", "Bagged KNN"], ["playground-series-s3e18"]),
    "T30 伪标签增益 vs 不可证": (["伪标签", "残差", "CV 对照", "几何平均"], ["playground-series-s5e9", "sorghum-id-fgvc-9", "geolifeclef-2022-lifeclef-2022-fgvc9"]),
    "T31 分组 CV vs LB": (["GroupKFold", "分组", "CV", "5407", "721", "随机变量"], ["scrabble-player-rating", "playground-series-s3e9", "playground-series-s3e22"]),
    "T32 主动终局 vs 被动 tiebreak": (["tiebreak", "碰撞", "能量", "矿工", "工厂"], ["maze-crawler"]),
    "T33 规则型 vs RL": (["规则", "RL", "PPO", "Q-learning", "自对弈"], ["kore-2022-beta", "maze-crawler", "lux-ai-season-2-neurips-stage-2"]),
    "T34 LLM 加速器 vs 风险源": (["幻觉", "核验", "工具", "通道", "信任", "引用"], ["openai-to-z-challenge", "openai-gpt-oss-20b-red-teaming", "maze-crawler"]),
    "T35 API 成本 vs 额度/自部署": (["API", "预算", "额度", "$2", "$300", "地区", "自部署"], ["openai-to-z-challenge", "bigquery-ai-hackathon", "llm-prompting-with-makersuite", "autonomous-agent-prediction-beta"]),
    "T36 评审透明度 vs 自包含": (["评分", "rubric", "分项", "复现", "自包含", "不公开"], ["med-gemma-impact-challenge", "pokemon-tcg-ai-battle-challenge-strategy", "bigquery-ai-hackathon"]),
    "T37 窄分带 vs 噪声": (["26.38", "26.40", "0.25", "分带", "窄", "噪声"], ["playground-series-s5e9", "playground-series-s3e25"]),
}

PLAYBOOKS = {
    "tabular": ["playground-series-s3e25", "playground-series-s5e9", "playground-series-s3e18", "playground-series-s3e9", "playground-series-s3e22", "playground-series-s3e23", "playground-series-s3e8", "scrabble-player-rating", "amex-default-prediction"],
    "cv": ["sorghum-id-fgvc-9", "hotel-id-to-combat-human-trafficking-2022-fgvc9", "planttraits2024", "herbarium-2022-fgvc9", "iwildcam2022-fgvc9", "fathomnet-out-of-sample-detection", "geolifeclef-2022-lifeclef-2022-fgvc9"],
    "nlp": ["llm-prompting-with-makersuite", "gemma-language-tuning", "wikipedia-image-caption", "openai-gpt-oss-20b-red-teaming", "autonomous-agent-prediction-beta", "kaggle-measuring-agi", "gemini-long-context"],
    "science": ["geolifeclef-2024", "geolifeclef-2022-lifeclef-2022-fgvc9", "med-gemma-impact-challenge", "phase-ii-widsdatathon2022", "planttraits2024"],
    "sim-agent": ["maze-crawler", "lux-ai-season-2-neurips-stage-2", "kore-2022-beta", "lux-ai-2022-beta", "autonomous-agent-prediction-beta", "pokemon-tcg-ai-battle-challenge-strategy"],
    "multimodal": ["planttraits2024", "med-gemma-impact-challenge", "gemini-long-context", "data-assistants-with-gemma", "geolifeclef-2024", "openai-gpt-oss-20b-red-teaming"],
}


def score(row: dict[str, str], keywords: list[str], slugs: list[str]) -> int:
    blob = f"{row['claim']} {row['value']} {row['source']}"
    s = EVIDENCE_RANK.get(row["evidence_type"], 0)
    if row["slug"] in slugs:
        s += 6
    s += sum(2 for k in keywords if k.lower() in blob.lower())
    if row["topic_ids"]:
        s += 1
    # 优先信息量大的数字行，压低"规模/体量"类泛泛行
    s += min(len(row["value"]) // 40, 4)
    if re.search(r"增益|提升|降低|分数|阈值|样本|CV|LB|排名|私榜|公榜|分数|±|\+0\.|-0\.", row["claim"]):
        s += 3
    if re.search(r"规模与|讨论区体量|赛制|队伍数", row["claim"]):
        s -= 3
    return s


def pick(rows: list[dict[str, str]], keywords: list[str], slugs: list[str], n: int = 5):
    if slugs:
        candidates = [r for r in rows if r["slug"] in slugs]
    else:
        candidates = [
            r
            for r in rows
            if any(k.lower() in f"{r['claim']} {r['value']}".lower() for k in keywords)
        ]
    ranked = sorted(candidates, key=lambda r: score(r, keywords, slugs), reverse=True)
    out, seen = [], set()
    for r in ranked:
        key = (r["slug"], re.sub(r"\s+", "", r["claim"])[:60], r["value"][:40])
        if key in seen:
            continue
        seen.add(key)
        out.append(r)
        if len(out) >= n:
            break
    return out


def table(rows: list[dict[str, str]]) -> list[str]:
    lines = ["| 场次 | 断言 | 数字 | 证据类型 |", "| --- | --- | --- | --- |"]
    for r in rows:
        claim = re.sub(r"\s+", " ", r["claim"])[:90]
        value = re.sub(r"\s+", " ", r["value"])[:120]
        lines.append(f"| `{r['slug']}` | {claim} | {value} | {r['evidence_type']} |")
    return lines


def main() -> None:
    rows = list(csv.DictReader(CLAIMS.open(encoding="utf-8")))
    lines: list[str] = []
    lines.append("# 规律 × 数字证据映射（Evidence Map）")
    lines.append("")
    lines.append(
        f"> 由 `scripts/build_evidence_map.py` 从 `analysis/claims.csv`（{len(rows)} 行）生成；"
        "每条规律给出最多 5 条最相关数字证据，按「官方 > 图证 > 原文数字 > 自述」与场次匹配排序。"
    )
    lines.append("> 用途：写方案/做复盘时直接引用；引用前回 `analysis/deep/<slug>.md` 核对上下文。")
    lines.append("")
    lines.append("## 1. L114–L133：Tier B 新规律的证据台账")
    lines.append("")
    for rule, (kw, slugs) in L_RULES.items():
        lines.append(f"### {rule}")
        picked = pick(rows, kw, slugs, n=5)
        lines.extend(table(picked) if picked else ["（未匹配到数字证据，回深读文档核对）"])
        lines.append("")
    lines.append("## 2. T28–T37：新张力的证据台账")
    lines.append("")
    for rule, (kw, slugs) in T_TENSIONS.items():
        lines.append(f"### {rule}")
        picked = pick(rows, kw, slugs, n=5)
        lines.extend(table(picked) if picked else ["（未匹配到数字证据，回深读文档核对）"])
        lines.append("")
    lines.append("## 3. Playbook 数字锚点")
    lines.append("")
    for name, slugs in PLAYBOOKS.items():
        lines.append(f"### {name}")
        picked = pick(rows, [], slugs, n=15)
        lines.extend(table(picked))
        lines.append("")
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"evidence_map.md: {len(lines)} lines -> {OUT}")


if __name__ == "__main__":
    main()
