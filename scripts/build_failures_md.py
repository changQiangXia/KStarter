#!/usr/bin/env python3
"""由 analysis/failures.csv 生成 analysis/failures.md（失败学手册）。

上半部分为人工归纳的"十二大失败模式"（机制/典型证据/预防/关联 L-T），
下半部分为按分类自动展开的条目表（每类最多 24 条，按 topic id 是否可得与信息量排序）。
"""

from __future__ import annotations

import csv
import pathlib
import re
from collections import Counter, defaultdict

ROOT = pathlib.Path(__file__).resolve().parent.parent
CSV = ROOT / "analysis" / "failures.csv"
OUT = ROOT / "analysis" / "failures.md"

PATTERNS = [
    (
        "F1 验证口径与榜单不一致",
        "CV 与 LB 的样本量/分布/泄漏方向不同，公开榜噪声或分布红利把选模带偏；小测试集上排名接近随机变量。",
        "先量 CV/LB 样本量比与相关性；实体/时间泄漏先排除；LB 只验证绝对水平；保留 OOF 证据。",
        "L4/L6/L31/L116/T3/T31/T37",
        [
            ("s3e9", "CV 5407 样本 vs 公榜 721 样本：测量 vs 随机变量；公开 notebook 无 CV 不抄"),
            ("s5e9", "榜首分带仅 26.38–26.41；未选用提交反而更高（609999）"),
            ("planttraits2024", "列顺序不一致导致 CV/LB 大幅偏离（487985）"),
        ],
    ),
    (
        "F2 实体/重复/泄漏",
        "同一实体（玩家、马、酒店、图）跨 train/test 或重复出现，历史统计与目标形成泄漏；GroupKFold 分数更低但更真实。",
        "先做实体键审计与重复检测；用 GroupKFold/时间切分；对重复行/近重复图登记处理规则。",
        "L2/L116/T31",
        [
            ("scrabble-player-rating", "同一玩家历史整体落在 train 或 test；GroupKFold 分数显著变差（372554）"),
            ("s3e22", "同一 hospital_number 的马会死多次（441284/438825）"),
            ("herbarium-2022-fgvc9", "图像重复/数据泄漏报告（323906）"),
        ],
    ),
    (
        "F3 数据缺失、坏值与口径漂移",
        "错误哨兵值（-666）、缺失编码不一致、test 端 OOD 类别、tracking 错位、语义口径不清，会让派生特征与结论同时失真。",
        "逐列 train/test diff、哨兵值扫描、事件对齐与可视化抽检；先写口径表再建模。",
        "L19/L21/T7/T10",
        [
            ("s3e18", "FpDensityMorgan1=-666；fr_COO/fr_COO2 出现 test 有 train 无的取值（419692/419651）"),
            ("nfl-big-data-bowl-2024", "位置滞后、缺失 tracking/ball_snap/passresult、plays 与 tracking 矛盾（448035/451985/452944）"),
            ("nfl-big-data-bowl-2025", "球轨迹不准、输入数据互相矛盾（551782/543709）"),
        ],
    ),
    (
        "F4 长尾与不平衡处理失效",
        "长尾下重采样/加权并不总有效；测试同样长尾时「均衡化」反而伤 top-K 指标；类别层级错误与无图类别让训练目标本身失真。",
        "先确认评测集分布；能归并的稀有类归并 unknown；用度量损失/多级监督替代盲目重采样。",
        "L130/L121",
        [
            ("herbarium-2022-fgvc9", "class-aware sampling 与 data cleaning 均无效；靠 subcenter-ArcFace/多级 CE（329299）"),
            ("geolifeclef-2022", "长尾「什么都不做」最好；多标签聚合失败（328637/327055）"),
            ("fathomnet-out-of-sample-detection", "290 类中 157 类无图；<10 图类别归 unknown（398752/413092）"),
        ],
    ),
    (
        "F5 指标结构/评测实现误读",
        "按指标名字猜测行为；未读官方 metric 实现（AUC 部分 bug、MAP@20 与评分代码不一致、逐列 AUC vs 堆叠 GINI），导致选模与提交策略错误。",
        "下载官方 metric 实现做单元校验；把指标数学结构写成实验（中位数型/排序型/阈值型/容差型）。",
        "L30/L114/L52",
        [
            ("fathomnet-out-of-sample-detection", "metric 的 AUC 部分有 bug，官方修复重算；MAP@20 与评分代码不一致（404769/410140）"),
            ("s3e18", "逐列 AUC 平均 vs 堆叠 GINI 口径不同（421149）"),
            ("s3e25", "MedAE 只取决于中位误差样本（455888）"),
        ],
    ),
    (
        "F6 无效的新增技巧与过拟合公榜",
        "公开 notebook/热门技巧在无 CV 证明时复制；Optuna 参数不经种子检验；PCA/t-SNE/聚类在结构化特征上无效；集成在低信号目标上过拟合。",
        "任何技巧必须过「同折 CV 对照」；Optuna 换种子复跑；低信号目标设预算上限。",
        "L41/L113/L125",
        [
            ("s3e9", "Optuna 参数换 KFold 种子后不存活（394592）"),
            ("s3e23", "PCA/t-SNE/聚类均无提升（450315）"),
            ("s5e9", "伪标签/残差无 CV 对照；低信号场次集成收益不可证（610264/610016）"),
        ],
    ),
    (
        "F7 伪标签/外部数据/合成数据反噬",
        "把检测器/教师输出当训练数据会误差传播；外部数据未做类别映射/对抗验证会引入分布错配；低质合成数据毒害训练。",
        "外部数据先做映射与对抗验证；伪标签只在同折 CV 对照下启用；教师输出先过滤置信度。",
        "L17/L31/T6/T8/T21/T30",
        [
            ("iwildcam2022", "用检测器结果训练会误差传播；1st 选择不训练只过滤（328965）"),
            ("hotel-id", "2nd 的 FGVC8 伪标签与 Hotel50K 均失败（328345）"),
            ("planttraits2024", "sample_submission 刷榜导致换测试集+重置 LB（486503）"),
        ],
    ),
    (
        "F8 提交/平台/预算工程事故",
        "提交按钮失效、schema/zip 结构错误、PENDING、模型挂载方式、地区限制、API 预算/额度、TPU 排队——工程事故直接淘汰或压缩实验次数。",
        "提前 48h 提交、本地 validate、保留截图凭证；赛前做成本模型与额度申领；准备自部署 fallback。",
        "L122/L123/T35",
        [
            ("bigquery-ai-hackathon", "提交按钮失效/保存锁定多帖（608992/608986/609004）"),
            ("autonomous-agent-prediction-beta", "agent schema 校验失败、$2 预算、工具兼容问题（737407/723907/723806）"),
            ("gemini-long-context", "必须 Save&Run All 才挂载模型；当时全站仅 4 用户（541420）"),
        ],
    ),
    (
        "F9 评审/材料不可复核",
        "获奖方案未归档、个人评分不公开、正文被压缩、0 图场次、站外图床不可达——大量结论只能停留在「自述/转引」层级。",
        "把评审材料当二手证据，标注置信度；引用前回原文 topic；把缺口写进悬案而不是补造结论。",
        "L117/L118/T36",
        [
            ("openai-gpt-oss-20b-red-teaming", "20 篇获奖 write-up 正文均未归档，仅官方评语（608537）"),
            ("med-gemma-impact-challenge", "落选者请求分项评分/rubric 未获承诺（685138）"),
            ("pokemon-tcg-strategy", "官方明确不公开个人评分与分项明细（742692）"),
        ],
    ),
    (
        "F10 RL/Agent 训练失败",
        "RL 在复杂环境里常打不过规则/示例微调；自对弈同质化导致策略偏科；延迟奖励与思考死循环烧光预算；训练收益在 20–30M 步后枯竭。",
        "先规则基线；RL 配课程+快模拟器+对手多样性；用 KL/产量/胜率曲线早停；agent 赛先过 schema。",
        "L124/L125/L126/L127/T32/T33",
        [
            ("kore-2022-beta", "1st 规则七模块；社区 Q-learning 打不过官方示例微调（317737/317955）"),
            ("maze-crawler", "1st 评分函数 BFS；3rd JAX+BC+PPO 自述自对弈池同质→战斗弱（717120/718158）"),
            ("lux-ai-season-2-neurips-stage-2", "32×32 KL>0.02、金属产量跌破 100 后收益枯竭（459891）"),
        ],
    ),
    (
        "F11 时间/成本/复现边界",
        "算力/显存/内存/时长限制、随机种子、私有数据、版本依赖与平台环境差异，使历史分数与方案不可完全复现。",
        "记录版本与种子；优先低成本可复现基线；把不可复现部分显式声明；用提前量对冲排队与超时。",
        "L28/L21",
        [
            ("sorghum-id-fgvc-9", "71GB PNG → 14GB JPEG；测试图缺失/API 拉取问题（313266/313438/313691）"),
            ("geolifeclef-2024", "Seafile 栅格下载脚本报错、GLC 模块不可用（481283）"),
            ("wikipedia-image-caption", "URL 图片下载/内存/TSV 读取问题（272204/287955）"),
        ],
    ),
    (
        "F12 社区与规则风险",
        "抄袭/引用缺失、upvote 影响评分、外部数据合规、规则中途变更、late submission 被拒——社区与规则风险会造成不公平或直接判负。",
        "注明来源并给增量；规则含社区分则提前发布维护；外部数据/影片合规先问；beta 规则变化用版本开关。",
        "L133/L118/T17",
        [
            ("s3e25", "基线被大量复制且不注明来源（458154）"),
            ("kaggle-measuring-agi", "rubric 含 15% 社区投票引发 upvote farming 争议（683674）"),
            ("planttraits2024", "sample_submission 套利导致测试集更换与 LB 重置（486503）"),
        ],
    ),
]


def clip(text: str, n: int = 160) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    return text if len(text) <= n else text[: n - 1] + "…"


def main() -> None:
    rows = list(csv.DictReader(CSV.open(encoding="utf-8")))
    by_cat: dict[str, list[dict[str, str]]] = defaultdict(list)
    for r in rows:
        by_cat[r["category"]].append(r)
    counts = Counter(r["category"] for r in rows)

    lines: list[str] = []
    lines.append("# KStarter 失败学手册（Failures & Open Problems）")
    lines.append("")
    lines.append(
        f"> 由 `scripts/build_failures.py` 扫描 264 篇深读生成（原始条目 {len(rows)} 条，覆盖 {len({r['slug'] for r in rows})} 场）；"
        "上半部分为人工归纳的十二大失败模式，下半部分按分类展开代表性条目；完整机器可读版见 `analysis/failures.csv`。"
    )
    lines.append("> 用法：开赛/复盘时把失败模式当检查清单；引用某条时回 `analysis/deep/<slug>.md` 与原文 topic 核对。")
    lines.append("")
    lines.append("## 0. 分类统计")
    lines.append("")
    lines.append("| 分类 | 条目数 |")
    lines.append("| --- | --- |")
    for cat, n in counts.most_common():
        lines.append(f"| {cat} | {n} |")
    lines.append("")
    lines.append("## 1. 十二大失败模式")
    lines.append("")
    for name, mech, prevent, refs, examples in PATTERNS:
        lines.append(f"### {name}")
        lines.append(f"- **机制**：{mech}")
        lines.append(f"- **预防**：{prevent}")
        lines.append(f"- **关联规律/张力**：{refs}")
        lines.append("- **典型证据**：")
        for slug, statement in examples:
            lines.append(f"  - `{slug}`：{statement}")
        lines.append("")

    lines.append("## 2. 分类明细（每类代表性条目）")
    lines.append("")
    for cat, _ in counts.most_common():
        entries = sorted(
            by_cat[cat],
            key=lambda r: (bool(r["topic_ids"]), len(r["statement"])),
            reverse=True,
        )
        seen = set()
        picked = []
        for r in entries:
            key = clip(r["statement"], 80)
            if key in seen:
                continue
            seen.add(key)
            picked.append(r)
            if len(picked) >= 24:
                break
        lines.append(f"### {cat}（{counts[cat]} 条，展示 {len(picked)} 条）")
        lines.append("")
        lines.append("| slug | 条目 | topic |")
        lines.append("| --- | --- | --- |")
        for r in picked:
            topic = r["topic_ids"].split()[0] if r["topic_ids"] else ""
            lines.append(f"| `{r['slug']}` | {clip(r['statement'])} | {topic} |")
        lines.append("")

    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"failures.md: {len(lines)} lines -> {OUT}")


if __name__ == "__main__":
    main()
