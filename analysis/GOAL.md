# KStarter 深读升级 · Goal 文本（v3，指针式）

> 本文件是 goal 的**权威版本**：新会话只需读本文件 + `analysis/TIER_A.md` 即可获得全部上下文。
> 方案细节见 `analysis/DEPTH_PLAN.md`；进度以 `analysis/TIER_A.md` 为准。
> 更新：2026-10-03（Tier A 8/60 完成时固化）。

## 目标

对已归档的 264 场 Kaggle write-up 做"深读层"再分析：不扩采（仅对正文 ≤3 篇的缺口场次定点补采），
把速览式摘要升级为对照式深读；所有图表证据以仓库相对路径内嵌，GitHub 上直接呈现"文字分析 + 图片作证"。

## 阶段与交付

1. **深读层**：Tier A 约 60 场完整深读（11 组件模板）+ Tier B 约 204 场轻量深读（对照矩阵/分歧裁决/证据分级/悬案）；
   每篇完成后回写升级原 `notes/` 笔记（保留原结构、内嵌关键图）。
2. **图像层**：`analysis/images_index.csv`（每图：相对路径/来源帖/上下文/优先级）；截图与分数表批量 OCR
   （sidecar 存 `*_img/<file>.ocr.txt`，数字并入 claims.csv）；Tier A 候选图逐张视觉精读；
   不可达图床（imgur 等）保留 URL+alt 并登记缺口清单。
3. **综合层**：`analysis/THEORY.md`（≥25 条可证伪规律：命题→机制→适用范围→反例→带数字证据场次，重点收录张力）；
   `analysis/claims.csv`（全量可量化断言台账：可复算/自述/矛盾）；`analysis/lineage.md`（方法谱系 ≥40 节点）；
   `analysis/limitations.md`（批判与局限）；对应修订各主题 playbook。

## 完成标准

- Tier A 60 篇 + Tier B 204 篇深读全部完成并通过校验：讨论链接与明文 topic id 全部真实；
  图证相对路径在仓库中可渲染；每篇含证据分级与数字账。
- 原 notes 全部完成回写升级；THEORY / claims / lineage / limitations 四件套成文。
- 全部产物分批推送至 GitHub `changQiangXia/KStarter`，每批 `verify_links.py` 与 `verify_images.py` 全绿。

## 约束

- 不新扩采（仅正文 ≤3 篇场次定点补采，如 lux-ai-season-2、AIMO-2 已完成）；
- 图片只用仓库内已归档文件、相对路径内嵌（从 `notes/<theme>/` 或 `analysis/deep/` 出发为 `../../intel/<slug>/bodies/<topic>_img/NN.png`）；
  站外图床不下载（保留链接与 alt）；`.bmp` 不内嵌并注明原因；
- 引用必须来自 `topics.json` 真实 topic id；不复制代码原文；
- 推送沿用容器低内存/代理环境下的分批策略（token 临时文件 + `source /etc/network_turbo` + `pack.threads=1`）；
- 所有工作可断点续跑（每场独立文件 + TIER_A.md 状态表）。

## 断点续跑指引

- 进度看 `analysis/TIER_A.md`（⬜ 未开始 / 🔄 进行中 / ✅ 完成）；已完成深读在 `analysis/deep/<slug>.md`；
  计分在 `analysis/_tier_a_scored.csv`。
- 单场节奏：读 digest/原帖 → 写 `analysis/deep/<slug>.md`（11 组件）→ 回写 `notes/<theme>/<slug>.md`（新增"深读结论""图表证据"节）→
  更新 `TIER_A.md` → 校验 → commit（格式：`Tier A 深读 N/60：<slug>（要点）`）→ 分批推送。
- 汇报口径：Tier A N/60、本场关键数字账、推送哈希。
