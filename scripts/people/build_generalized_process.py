#!/usr/bin/env python3
"""从 551 条 GM 断言里归纳"可泛化流程"。

输入：people/claims/gm_claims.csv、people/claims/gm_claim_tags.csv
输出：analysis/people/GENERALIZED_PROCESS.md
  - 通用 7 阶段主循环（每阶段配额 + 代表断言）
  - 8 领域变体（阶段侧重 + 跨人复现标签）
  - 选手原型（按阶段签名分型，≥5 条 A/B 才入榜）
  - solo vs team 差异

用法：python scripts/people/build_generalized_process.py
"""

from __future__ import annotations

import collections
import csv
import pathlib
import re
import time

ROOT = pathlib.Path(__file__).resolve().parents[2]
CLAIMS = ROOT / "people" / "claims" / "gm_claims.csv"
TAGS = ROOT / "people" / "claims" / "gm_claim_tags.csv"
OUT = ROOT / "analysis" / "people" / "GENERALIZED_PROCESS.md"

PHASES = [
    ("数据理解", ["数据理解"]),
    ("验证与数据工程", ["验证设计", "数据工程"]),
    ("特征与数据工程", ["特征与数据工程"]),
    ("建模与训练", ["建模与训练"]),
    ("集成与融合", ["集成与融合"]),
    ("提交/推理工程", ["工程/流程", "后处理", "后处理/校准", "后处理与选模", "报告结果", "工程/提交"]),
    ("复盘与流程", ["复盘与流程"]),
]
PHASE_OF = {s: name for name, members in PHASES for s in members}
CANON_DOMAINS = ["视觉 CV", "文本 NLP", "表格/结构化", "时间序列", "语音/音频", "生物/医疗", "强化学习/博弈", "科学研究"]

ARCHETYPES = [
    ("数据取证型", lambda sh: sh.get("数据理解", 0) + sh.get("特征与数据工程", 0) >= 0.40),
    ("验证纪律型", lambda sh: sh.get("验证设计", 0) >= 0.18),
    ("集成工程型", lambda sh: sh.get("集成与融合", 0) >= 0.18),
    ("工程/Agent 型", lambda sh: sh.get("工程/流程", 0) >= 0.25),
    ("复盘流程型", lambda sh: sh.get("复盘与流程", 0) >= 0.18),
    ("单模深磨型", lambda sh: sh.get("建模与训练", 0) >= 0.60),
]


def main() -> int:
    claims = {r["claim_id"]: r for r in csv.DictReader(CLAIMS.open(encoding="utf-8"))}
    tag_rows = list(csv.DictReader(TAGS.open(encoding="utf-8")))
    # 用有序列表保证生成结果可复现（集合迭代顺序受 PYTHONHASHSEED 影响）
    ab = [cid for cid, r in claims.items() if r["evidence_level"] in ("A", "B")]
    ab_set = set(ab)

    def phase(cid: str) -> str:
        return PHASE_OF.get(claims[cid]["stage"].strip(), "其他")

    # 阶段配额
    phase_counts = collections.defaultdict(collections.Counter)
    for cid in ab:
        phase_counts[phase(cid)][claims[cid]["role"]] += 1
    total_ab = sum(sum(c.values()) for c in phase_counts.values())

    # 每阶段代表断言：票数最高的 A 级
    reps = {}
    for cid in ab:
        p = phase(cid)
        r = claims[cid]
        if r["evidence_level"] != "A" or not any(p == name for name, _ in PHASES):
            continue
        key = (int(r["votes"] or 0), cid)
        if p not in reps or key > reps[p][0]:
            reps[p] = (key, r)

    # 领域 × 阶段 + 跨人标签
    dom_phase = collections.defaultdict(collections.Counter)
    dom_tag = collections.defaultdict(list)
    tag_dom = {t["claim_id"]: t for t in tag_rows}
    for cid in ab:
        r = claims[cid]
        for d in r["domain"].split(";"):
            if d in CANON_DOMAINS:
                dom_phase[d][phase(cid)] += 1
        tr = tag_dom.get(cid)
        if not tr:
            continue
        for d in tr["domain"].split(";"):
            if d not in CANON_DOMAINS:
                continue
            for tag in tr["tags"].split(";"):
                if tag:
                    dom_tag[d].append((tag, cid))

    def top_tags(domain: str, limit: int = 4):
        grouped = collections.defaultdict(list)
        for tag, cid in dom_tag[domain]:
            grouped[tag].append(cid)
        out = []
        for tag, cids in grouped.items():
            persons = {claims[c]["person"] for c in cids}
            if len(persons) >= 2 and len(cids) >= 3:
                a_count = sum(1 for c in cids if claims[c]["evidence_level"] == "A")
                out.append((tag, len(cids), len(persons), a_count))
        out.sort(key=lambda x: (-x[2], -x[1], x[0]))
        return out[:limit]

    # 选手原型（≥5 条 A/B）
    per_stage = collections.defaultdict(collections.Counter)
    for cid in ab:
        per_stage[claims[cid]["person"]][claims[cid]["stage"].strip()] += 1
    archetype_pool = {}
    for person, st in per_stage.items():
        n = sum(st.values())
        if n < 5:
            continue
        share = {k: v / n for k, v in st.items()}
        labels = [name for name, rule in ARCHETYPES if rule(share)]
        archetype_pool[person] = (n, labels, st.most_common(3))

    # solo vs team
    role_stage = collections.defaultdict(collections.Counter)
    for cid in ab:
        role_stage[claims[cid]["role"]][phase(cid)] += 1

    lines = [
        "# 前 50 选手的可泛化流程（从 551 条断言归纳；有公开言论的 35 位入样）",
        "",
        f"> 数据：{len(claims)} 条断言（A/B {total_ab} 条，{len({r['person'] for r in claims.values()})} 位 GM），"
        f"由脚本从 stage/标签/复现度聚合生成；生成时间 {time.strftime('%Y-%m-%d')}。",
        "> 用法：这是「流程骨架」，具体决策项回 `PLAYBOOK_DOMAINS.md` 与各领域 playbook；冲突裁决见 `TENSIONS.md`。",
        "> 复现：`python scripts/people/build_generalized_process.py`",
        "",
        "## 1. 通用主循环（7 阶段）",
        "",
        "| 阶段 | 目的 | A/B 断言 | 占比 | 代表断言（票数最高 A 级） |",
        "| --- | --- | --- | --- | --- |",
    ]
    purpose = {
        "数据理解": "先搞清数据怎么来的：分布/泄漏/生成器痕迹/原数据匹配",
        "验证与数据工程": "把测量修好：折设计、分组/时间切分、泄漏审计",
        "特征与数据工程": "制造可复现的信息差：取证特征、TE、增广、外部数据",
        "建模与训练": "强单模与训练细节：损失/架构/课程/伪标签",
        "集成与融合": "多样性与低自由度融合：权重选择、秩/概率融合、堆叠",
        "提交/推理工程": "把分数交付出来：推理工程、后处理/校准、提交格式与预算",
        "复盘与流程": "把胜负写成资产：赛后复盘、负结果、跨届迁移",
    }
    for name, _ in PHASES:
        c = phase_counts[name]
        n = sum(c.values())
        rep = reps.get(name)
        rep_text = ""
        if rep:
            r = rep[1]
            action = re.sub(r"\s+", " ", r["action"])[:56]
            rep_text = (
                f"@{r['person']}｜{action}…（{r['votes']} 票｜"
                f"[{r['claim_id'].split('#')[-1][:6]}]({r['source_url']})）"
            )
        lines.append(f"| {name} | {purpose[name]} | {n} | {n / max(total_ab,1):.0%} | {rep_text} |")

    lines += [
        "",
        "**读数**：建模与训练是最大头，但「建模之外」（验证 + 特征 + 集成 + 提交 + 复盘）合计超过一半——"
        "榜单差距往往不在模型本身，而在测量、数据信息差与交付工程。",
        "",
        "## 2. 8 领域变体",
        "",
        "| 领域 | 阶段侧重（A/B） | 跨人复现标签（≥2 人） |",
        "| --- | --- | --- |",
    ]
    for d in CANON_DOMAINS:
        staged = sorted(dom_phase[d].items(), key=lambda kv: (-kv[1], kv[0]))[:3]
        stages = "、".join(f"{k}({v})" for k, v in staged)
        tags = "、".join(f"{t}({c}条/{p}人/A{a})" for t, c, p, a in top_tags(d))
        lines.append(f"| {d} | {stages} | {tags} |")

    lines += [
        "",
        "**领域读法**：NLP/表格看「集成 + 提交 + 验证」；CV 看「损失 + 验证 + 规模」；"
        "时间序列先修「验证 + 提交」；语音/信号先做「频谱/信号处理」；生物医疗重「损失 + 后处理 + 集成权重」；"
        "RL 看「提交/推理 + 规模 + Agent 工具」；科学研究重「清洗 + 谱系 + 提交」。",
        "",
        "## 3. 选手原型（按阶段签名，≥5 条 A/B 入榜）",
        "",
        "| 原型 | 判据（阶段占比） | 代表选手（n=断言数） |",
        "| --- | --- | --- |",
    ]
    rule_text = {
        "数据取证型": "数据理解 + 特征工程 ≥ 40%",
        "验证纪律型": "验证设计 ≥ 18%",
        "集成工程型": "集成与融合 ≥ 18%",
        "工程/Agent 型": "工程/流程 ≥ 25%",
        "复盘流程型": "复盘与流程 ≥ 18%",
        "单模深磨型": "建模与训练 ≥ 60%",
    }
    for name, _ in ARCHETYPES:
        members = [(p, n) for p, (n, labels, _) in archetype_pool.items() if name in labels]
        members.sort(key=lambda x: (-x[1], x[0]))
        exemplars = "、".join(f"@{p}({n})" for p, n in members[:6]) or "—"
        lines.append(f"| {name} | {rule_text[name]} | {exemplars} |")

    lines += [
        "",
        "> 一人可属多型；原型是「看哪一段最重」的启发，不是能力评级。找同型选手参考其赛内决策顺序，"
        "找异型选手补自己的短板环节。",
        "",
        "## 4. solo vs team（阶段占比差异）",
        "",
        "| 阶段 | solo | team | 差异 |",
        "| --- | --- | --- | --- |",
    ]
    solo_total = sum(role_stage["solo"].values())
    team_total = sum(role_stage["team"].values())
    for name, _ in PHASES:
        s, t = role_stage["solo"][name], role_stage["team"][name]
        ss, ts = s / max(solo_total, 1), t / max(team_total, 1)
        diff = ss - ts
        mark = "solo 更重" if diff > 0.03 else ("team 更重" if diff < -0.03 else "相近")
        lines.append(f"| {name} | {s}（{ss:.0%}） | {t}（{ts:.0%}） | {mark} |")

    lines += [
        "",
        f"- solo 断言 {solo_total} 条 / team {team_total} 条；数据理解几乎只在 solo 断言里出现——"
        "团队方案的公开复盘更偏向工程与集成，个人选手更愿意讲「怎么把数据看懂」。",
        "",
        "## 5. 套用到新比赛的顺序",
        "",
        "1. **P0 数据理解**：先做泄漏/分布/生成器取证（对应 `playbook/` 与 `idea-playbook` 的 S5/S25 类症状）。",
        "2. **P1 验证**：折设计 + 分组/时间切分 + 对抗验证；测量不可信就不进入建模。",
        "3. **P2 特征**：按领域变体选 2–3 个跨人复现标签先做（如 NLP 的目标编码/域适应，CV 的增广/损失）。",
        "4. **P3 建模**：先强单模，再谈多样性；训练细节与负结果优先于堆模型数。",
        "5. **P4 集成**：只在 OOF 有增量时上；权重选择优先（榜单显示这是最常见的最后一截）。",
        "6. **P5 交付**：推理工程 + 后处理/校准 + 提交组合（时间序列/NLP 的跨人复现证据最集中在提交环节）。",
        "7. **P6 复盘**：把死因、负结果、跨届资产写回笔记——复盘类断言在头部选手里有稳定占比。",
        "",
        "## 6. 反例与张力",
        "",
        "- 12 组选手间冲突（如公开榜 vs 私榜、单模 vs 集成、伪标签强度）见 `TENSIONS.md`；"
        "本页给的是「多数人怎么做」，不替代条件化裁决。",
        "- 复现度门槛：本页标签默认「≥2 人 + ≥3 条断言」；更严格口径（≥2 个相同具体技法）见"
        "KExperienceSkill `references/people-evidence.md`。",
        "",
    ]
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"generalized process -> {OUT.relative_to(ROOT)}")
    print(f"claims A/B {total_ab} | phases {len(PHASES)} | archetype pool {len(archetype_pool)} persons")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
