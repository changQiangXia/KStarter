#!/usr/bin/env python3
"""P2：跨人/跨赛复现判定与张力扫描。

输入：people/claims/gm_claims.csv、people/competitions/gm_competitions.csv
输出：
  - people/claims/gm_claim_tags.csv   每条断言的标签（可多条）
  - analysis/people/REPLICATION.md    按标签的复现报告与领域门禁
  - analysis/people/TENSIONS.md       张力条目（人工裁决 + 证据链接）

证据单位：solo 断言按人计算；team_evidence 断言按（比赛 + 队名）计算，
使同一队的多人发言只贡献一个证据单位。
"""

from __future__ import annotations

import csv
import json
import pathlib
import re
import sys
from collections import Counter, defaultdict

ROOT = pathlib.Path(__file__).resolve().parents[2]

# 标签 -> 正则（作用于 condition/action/mechanism/result/quote 的合并文本）
TAG_RULES: dict[str, str] = {
    "验证设计": r"验证|validation|cross.?valid|kfold|k 折|折|holdout|cv\b",
    "时间/分组切分": r"时间 cv|time[- ]?cv|按时间|滑窗|group.?kfold|groupkfold|subjectid|prompt_id|按 prompt|按 signer|按文件|按视频|时间切分|last k|嵌套",
    "泄漏检测/探针": r"leak|泄漏|探针|probe|对抗验证|adversarial validation|重复|overlap|探",
    "公开榜策略": r"public lb|公开榜|lb 选模|public score|leaderboard|lb\b",
    "多种子平均": r"seed|种子",
    "伪标签/自训练": r"pseudo|伪标签|self.?train|noisy student|自训练",
    "知识蒸馏": r"distill|蒸馏|teacher|kd\b",
    "规模/Scaling": r"scal|更大|bigger|large model|模型规模|参数|bitter lesson",
    "长序列/上下文": r"max_len|max_length|context length|seq_len|sequence length|2048|4096|5120|长文本|长序列|长上下文|window",
    "混合精度/量化": r"fp16|bf16|fp32|int8|int4|quant|量化|awq|gptq|fp8|mixed precision|2x t4|混合精度",
    "数据增广": r"augment|增广|mixup|cutmix|flip|rotate|rot90|cutout|masking",
    "预训练/域适应": r"pretrain|pre-train|预训练|mlm|domain adapt|域适应|fine.?tune|微调",
    "类别不平衡": r"imbalan|不平衡|class weight|resampl|downsampl|focal|权重",
    "损失设计": r"loss|损失|dice|bce|ce\b|cross.?entropy|focal|mae|rmse loss|gaussiannll",
    "度量学习/ArcFace": r"arcface|metric learning|triplet|embedding",
    "Transformer/注意力": r"transformer|attention|self.?attention|vit\b|rope",
    "CNN/视觉架构": r"cnn|conv|resnet|efficientnet|unet|u-net|convnext|backbone",
    "序列模型": r"gru|lstm|rnn|wavenet|squeezeformer|seq2seq",
    "GBDT 家族": r"xgb|lgbm|lightgbm|catboost|gbdt|gbm|lightautoml",
    "线性/简单模型": r"linear|ridge|lasso|svr|logistic|linear model|简单模型|朴素",
    "集成/融合": r"stack|blend|ensembl|融合|hill.?climb|wbf|加权平均|rank|投票|平均",
    "残差提升": r"residual|残差|base_margin",
    "目标编码/类别特征": r"target encod|target encoding|te\b|类别|categorical|one.?hot|label encod|bins|分箱",
    "分组聚合特征": r"groupby|聚合|agg\b|统计特征|count encod|分组",
    "特征选择": r"feature selection|特征选择|importance|permutation|前向|重要性",
    "外部数据": r"external data|外部数据|additional data|supplemental|额外数据|原始数据|persuade|旧赛|去年",
    "合成/生成数据": r"synthetic|合成|generat|生成数据|llm-generated|t5|flux|合成数据",
    "数据清洗/去噪": r"clean|清洗|noise|噪声|outlier|离群|dedup|去重|inpainting|热像素|hot pixel|纠正|修正",
    "dtype/内存优化": r"dtype|内存|memory|quantile.?matrix|vram|ram|压缩|compress|int32|float32|字节",
    "缺失值/NAN": r"nan|missing|缺失|impute|插补|mask 掉|置零|zero.?(fill|ing)",
    "检索/RAG": r"\brag\b|retriev|faiss|余弦|cosine|top.?k|rerank|bi.?encoder|相似度|检索",
    "信号/频谱处理": r"spectrogram|mel|fft|filter|信号|eeg|audio|音频|频域|波",
    "图结构/GNN": r"graph|gnn|sageconv|conv.*graph",
    "优化器": r"muon|adamw|optimizer|优化器|sgd\b",
    "学习率调度": r"scheduler|cosine|warmup|schedule|调度|学习率|lr\b",
    "TTA": r"tta|test.?time augment|permute|翻转|reflection|rot90|多视图",
    "后处理/校准": r"post.?process|后处理|threshold|阈值|校准|calibrat|clip|nms|剪枝|均值|平滑",
    "提交/推理工程": r"submission|提交|kernel|inference|推理|时间限制|timeout|runtime|cpu|打包|docker|量化推理|onnx",
    "Agent/LLM 工具": r"codex|agent|chatgpt|claude|llm studio|vllm|copilot|prompt|llm",
    "贝叶斯/概率模型": r"bayesian|posterior|prior|gaussian process|\bgp\b|hmm|particle filter|贝叶斯|卡尔曼",
    "集成权重选择": r"weight|权重|voting|投票|median|中位数|hill",
}

# 张力条目：人工裁决；证据为 gm_claims.csv 的 claim_id（脚本会校验存在性）
TENSIONS: list[dict] = [
    {
        "title": "公开榜 vs 私有榜选模",
        "verdict": "按公私有划分与样本量决定：随机划分且 public 占比大时可参考 public；小样本/时间漂移/已知泄漏时只信 CV，并接受 public 排名下滑。",
        "evidence": [
            "foursquare-location-matching#338112-03",
            "tlvmc-parkinsons-freezing-gait-prediction#416057-04",
            "petfinder-pawpularity-score#301015-01",
            "novozymes-enzyme-stability-prediction#376116-04",
            "amex-default-prediction#348014-05",
            "icr-identify-age-related-conditions#431067-04",
        ],
    },
    {
        "title": "伪标签/自训练：有效 vs 有害",
        "verdict": "有效但有条件：需控制伪标签噪声与标签和上限（birdclef 的两个 enabler），并保证 CV 与 LB 同向；用测试集自训练属灰区，风险与收益都大。",
        "evidence": [
            "amex-default-prediction#347641-01",
            "birdclef-2026#704752-05",
            "tlvmc-parkinsons-freezing-gait-prediction#416057-03",
            "happy-whale-and-dolphin#320298-03",
            "feedback-prize-english-language-learning#369609-04",
            "birdclef-2026#704752-04",
            "llm-detect-ai-generated-text#470148-04",
        ],
    },
    {
        "title": "规模（Scaling）vs 小模型/正则",
        "verdict": "由数据量与信噪比决定：大数据/高信息量支持放大（icecube/lux-3/LLM 赛），小数据或噪声大时更小的模型与更强正则更稳（polymer/DFL/playground）。",
        "evidence": [
            "icecube-neutrinos-in-deep-ice#402888-02",
            "map-charting-student-math-misunderstandings#612268-04",
            "playground-series-s5e3#568268-01",
            "neurips-open-polymer-prediction-2025#607947-05",
            "dfl-bundesliga-data-shootout#359932-02",
            "playground-series-s5e1#560549-02",
        ],
    },
    {
        "title": "长序列/长上下文 vs 短训长推",
        "verdict": "训练长度与推理长度可解耦：文本/文档任务倾向更长上下文（max_len 1024-5120），时序事件任务用短序列训练 + 长序列推理并只取中段更优。",
        "evidence": [
            "learning-agency-lab-automated-essay-scoring-2#497832-02",
            "feedback-prize-2021#313389-04",
            "AI4Code#360501-04",
            "tlvmc-parkinsons-freezing-gait-prediction#416057-01",
            "birdclef-2026#704752-01",
        ],
    },
    {
        "title": "大集成 vs 单模/蒸馏单模",
        "verdict": "预算与推理约束决定：候选异构且时间充足时大集成/多层 stack 仍是最稳上限；推理受限或候选同质时，单模 + 蒸馏/伪标签可接近甚至超过集成。",
        "evidence": [
            "playground-series-s5e6#587393-04",
            "playground-series-s5e10#614079-01",
            "amex-default-prediction#348014-03",
            "feedback-prize-effectiveness#347537-01",
            "playground-series-s6e8#738592-02",
            "stanford-rna-3d-folding#609774-03",
        ],
    },
    {
        "title": "线性融合 vs 非线性 stack",
        "verdict": "线性融合（hill climbing/加权平均）是默认安全解；当存在场景切换、特征缺失导致的条件分支时，非线性 stack 明显更优（playground-s5e4）。",
        "evidence": [
            "petfinder-pawpularity-score#301015-04",
            "playground-series-s5e5#582611-01",
            "playground-series-s5e4#575784-02",
            "playground-series-s5e6#587393-04",
        ],
    },
    {
        "title": "泄漏利用：红利 vs 反噬",
        "verdict": "可利用但必须把 private 风险计入：重复行/切分探测能大幅提分（foursquare/novozymes），但用公开榜探针制造训练目标会伤 private（ICR），且公开榜小比例时排名不可信（jigsaw）。",
        "evidence": [
            "foursquare-location-matching#336055-02",
            "novozymes-enzyme-stability-prediction#376116-02",
            "jigsaw-toxic-severity-rating#306074-01",
            "icr-identify-age-related-conditions#431067-04",
            "feedback-prize-english-language-learning#369609-04",
        ],
    },
    {
        "title": "数据增广：高影响 vs 无用",
        "verdict": "按模态与数据量：视觉/序列任务增广常是首要杠杆（ASL/Rogii/Petfinder），回归与文本小数据增广往往无效甚至有害（反馈英语/amex 清单）。",
        "evidence": [
            "asl-fingerspelling#434485-03",
            "rogii-wellbore-geology-prediction#733220-05",
            "petfinder-pawpularity-score#301015-02",
            "feedback-prize-english-language-learning#369578-05",
            "amex-default-prediction#348014-04",
        ],
    },
    {
        "title": "蒸馏/teacher-student：提速与掉分",
        "verdict": "蒸馏在推理受限时性价比最高，但教师噪声会传导：需限制伪标签权重、保持真实标签监督；学生有可能超过教师（jsday96），教师选择错误会拖后腿（Mamba）。",
        "evidence": [
            "amex-default-prediction#347641-01",
            "llm-detect-ai-generated-text#470093-02",
            "feedback-prize-effectiveness#347537-01",
            "birdclef-2026#704752-01",
            "birdclef-2026#704752-04",
            "llm-detect-ai-generated-text#470093-05",
        ],
    },
    {
        "title": "时间/分组 CV 的必要性",
        "verdict": "存在时间漂移、会话/用户泄漏或域偏移时必须用时间切分或分组折（ICR/Otto/Eedi/写作）；否则随机折会系统性高估。",
        "evidence": [
            "icr-identify-age-related-conditions#431067-01",
            "otto-recommender-system#370210-02",
            "eedi-mining-misconceptions-in-mathematics#551391-01",
            "linking-writing-processes-to-writing-quality#466906-02",
            "MABe-mouse-behavior-detection#663029-01",
        ],
    },
    {
        "title": "使用测试数据：特征适配 vs 标签窥探",
        "verdict": "用测试特征做域适应/伪标签通常可接受且有收益；用测试标签或探针反推标签风险高，且可能违反赛制精神；需在规则边界内选择。",
        "evidence": [
            "llm-detect-ai-generated-text#470148-04",
            "novozymes-enzyme-stability-prediction#376116-01",
            "icr-identify-age-related-conditions#431067-04",
            "foursquare-location-matching#338112-04",
        ],
    },
    {
        "title": "Agent 自动化：生产力 vs 新意边界",
        "verdict": "工程实现、实验循环、看板与打包可高度自动化（s6e8/rogii/neurogolf），但问题重构、新意与关键假设仍需人类判断（pressman1 明言不能替代思考）。",
        "evidence": [
            "playground-series-s6e8#738592-01",
            "playground-series-s6e8#738592-02",
            "rogii-wellbore-geology-prediction#733181-01",
            "neurogolf-2026#726653-01",
            "orbit-wars#714324-02",
        ],
    },
]


def norm(text: str) -> str:
    return re.sub(r"\s+", " ", (text or "").lower())


def main() -> int:
    claims_path = ROOT / "people" / "claims" / "gm_claims.csv"
    comps_path = ROOT / "people" / "competitions" / "gm_competitions.csv"
    claims = list(csv.DictReader(claims_path.open(encoding="utf-8")))

    # 证据单位：team_evidence 按（slug, 队名）合并；solo 按人
    team_of: dict[tuple[str, str], str] = {}
    if comps_path.exists():
        for row in csv.DictReader(comps_path.open(encoding="utf-8")):
            team_of[(row["handle"], row["slug"])] = row["team_name"] or ""

    rows = []
    unit_people = defaultdict(set)
    for c in claims:
        text = " ".join(c[k] for k in ("domain", "stage", "action_class", "condition", "action", "mechanism", "result", "quote"))
        tags = sorted({tag for tag, pattern in TAG_RULES.items() if re.search(pattern, text)})
        team = team_of.get((c["person"], c["slug"]), "")
        if "team_evidence" in c["flags"] and team:
            unit = f"team:{c['slug']}:{team}"
        else:
            unit = f"person:{c['person']}"
        unit_people[unit].add(c["person"])
        rows.append({"claim_id": c["claim_id"], "person": c["person"], "slug": c["slug"], "level": c["evidence_level"], "domain": c["domain"], "unit": unit, "tags": ";".join(tags)})

    out_tags = ROOT / "people" / "claims" / "gm_claim_tags.csv"
    with out_tags.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=["claim_id", "person", "slug", "level", "domain", "unit", "tags"])
        writer.writeheader()
        writer.writerows(rows)

    # 标签级复现
    tag_rows = defaultdict(list)
    for r in rows:
        for tag in filter(None, r["tags"].split(";")):
            tag_rows[tag].append(r)

    replicated = {}
    for tag, items in tag_rows.items():
        units = {i["unit"] for i in items}
        comps = {i["slug"] for i in items}
        ab = [i for i in items if i["level"] in ("A", "B")]
        replicated[tag] = {
            "units": len(units),
            "people": len({i["person"] for i in items}),
            "comps": len(comps),
            "ab": len(ab),
            "claims": items,
        }

    # 领域门禁：A/B 断言中该 tag 跨 ≥2 证据单位
    DOMAINS = ["视觉 CV", "文本 NLP", "表格/结构化", "时间序列", "语音/音频", "生物/医疗", "强化学习/博弈", "科学研究"]
    gate = {}
    for domain in DOMAINS:
        hit: set[str] = set()
        for tag, info in replicated.items():
            if info["units"] < 2:
                continue
            for i in info["claims"]:
                if i["level"] in ("A", "B") and domain in i["domain"]:
                    hit.add(i["claim_id"])
        gate[domain] = len(hit)

    lines = [
        "# 前 50 选手断言复现报告（P2）",
        "",
        "> 证据单位：solo 按人；`team_evidence` 按（比赛 + 队名）合并，同队多人发言只算一个单位。",
        "> 标签由 `scripts/people/build_claim_analysis.py` 的受控词表自动匹配，完整标签见 `people/claims/gm_claim_tags.csv`。",
        "",
        "## 领域门禁（跨 ≥2 证据单位的 A/B 断言数，目标每领域 ≥5）",
        "",
        "| 领域 | 复现 A/B 断言 | 达标 |",
        "| --- | --- | --- |",
    ]
    for domain, n in gate.items():
        lines.append(f"| {domain} | {n} | {'✅' if n >= 5 else '❌'} |")

    lines += ["", "## 标签复现榜（按证据单位数排序）", "", "| 标签 | 证据单位 | 作者数 | 比赛数 | A/B 断言 |", "| --- | --- | --- | --- | --- |"]
    for tag, info in sorted(replicated.items(), key=lambda kv: (-kv[1]["units"], -kv[1]["ab"]))[:40]:
        lines.append(f"| {tag} | {info['units']} | {info['people']} | {info['comps']} | {info['ab']} |")

    out_rep = ROOT / "analysis" / "people" / "REPLICATION.md"
    out_rep.write_text("\n".join(lines) + "\n", encoding="utf-8")

    # 张力文档
    by_id = {c["claim_id"]: c for c in claims}
    t_lines = [
        "# 前 50 选手经验张力（P2）",
        "",
        "> 写法：张力 → 当前裁决 → 证据。证据为 `people/claims/gm_claims.csv` 中的断言，可经 `verify_claims.py` 回链原文。",
        "",
    ]
    missing = []
    for i, t in enumerate(TENSIONS, 1):
        t_lines.append(f"## T{i}｜{t['title']}")
        t_lines.append("")
        t_lines.append(f"**当前裁决**：{t['verdict']}")
        t_lines.append("")
        t_lines.append("**证据**：")
        for cid in t["evidence"]:
            c = by_id.get(cid)
            if not c:
                missing.append(cid)
                continue
            link = c["source_url"]
            t_lines.append(f"- [{cid}]({link})（{c['person']}｜{c['evidence_level']}｜{c['action'][:70]}）")
        t_lines.append("")
    out_ten = ROOT / "analysis" / "people" / "TENSIONS.md"
    out_ten.write_text("\n".join(t_lines) + "\n", encoding="utf-8")

    print(f"claims: {len(claims)} | tagged: {sum(1 for r in rows if r['tags'])} | tags: {len(tag_rows)}")
    print("gate:", json.dumps(gate, ensure_ascii=False))
    fails = [d for d, n in gate.items() if n < 5]
    print("gate PASS" if not fails else f"gate below target: {fails}")
    print(f"tensions: {len(TENSIONS)}" + (f" | missing evidence: {missing}" if missing else ""))
    print(f"tags -> {out_tags}")
    print(f"report -> {out_rep}")
    print(f"tensions -> {out_ten}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
