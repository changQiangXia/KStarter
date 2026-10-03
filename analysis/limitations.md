# KStarter 局限与批判（Limitations）

> 定位：对本次"深读升级"材料、方法、证据与四件套自身边界的系统批判。写作依据：264 篇深读（Tier A 60 + Tier B 204）、`analysis/THEORY.md`（L1–L113 + T1–T27）、`analysis/images_index.csv`（1666 行）、`analysis/claims.csv`（1850 行）与 `analysis/lineage.md`（52 节点）。
> 快照时间：2026-10；数据源为仓库内 `intel/` + `digests/` 的归档材料。

## 1. 范围与快照

- 本研究**不扩采**：所有结论来自已归档的 6–8 篇正文/场与讨论区索引；未归档的获奖方案、被删帖、私有 notebook、站外图床都不在证据范围内。
- 材料是 2026-10 的快照；Kaggle 讨论区、平台规则、比赛数据版本此后可能变化。
- "深读/轻读"是分析产物，不是官方结论；`claims.csv` 的 evidence_type 与 `lineage.md` 的传播链都是编辑归纳。

## 2. 材料层的局限

| 局限 | 具体表现 | 影响 |
| --- | --- | --- |
| Digest 是压缩件 | `digests/*.md` 对正文做过截断/去代码/术语压缩，部分帖子只有标题级信息 | 细节（超参、消融、失败对照）可能缺失 |
| 获奖方案常缺正文 | openai-gpt-oss、gemma-language-tuning、pokemon-strategy、bigquery 等场次只有名单/公告 | 只能转引官方评语，无法独立复核 |
| 0 图场次 | 多场 0 张归档图（iwildcam、nfl-2025、wids 等） | 图证缺口只能登记，不能补造 |
| 装饰图/梗图 | 部分归档图为毛衣、梗图、风景照（wids、makersuite 等） | 不内嵌，分析价值为零 |
| 站外图床 | imgur 等图未下载（BlendFlip、Lux Eye、ExamplePlay.gif 等） | 关键管线图缺失，只有文字描述 |
| GIF/BMP 不内嵌 | GAN Lab GIF（2.5MB）、GIF 动图等按规则不内嵌 | 图表证据节只能登记"未内嵌" |
| 私有/删除内容 | 私有 notebook、被删的 draft、未提交作品 | 成功与失败样本都不完整 |

## 3. 证据层的局限

### 3.1 自述与不可核实

多数方案帖的分数、增益、消融均为作者自述；我们没有运行任何比赛代码。`claims.csv` 中"可复算-原文数字"只表示**数字在原文中明确写出**，不等于我们独立复算过。真正可复核的是少数官方帖（评审流程、规则、时间线）与图表截图。

### 3.2 幸存者偏差

- 归档材料偏向高票帖与获奖方案；失败方案只在少数"what did not work"段落出现。
- 讨论区的沉默大多数（未发帖、未公开 notebook）完全没有进入样本。
- 平台机制（点赞/热度排序）会放大"会讲故事"的方案，压低"有效但不善表达"的方案。

### 3.3 数字口径不一致

- CV/LB 的样本量、折数、随机种子、早停规则常常不明；
- 同一队在不同帖子里的分数可能对应不同提交（如 s3e22 的选中/未选中版本）；
- 单位/量纲错误（s5e9 的 fold RMSE 3.1 vs LB 26.4）；
- 平均方式不同（s3e18 的逐列 AUC vs 堆叠 GINI）；
- 这些差异在 `claims.csv` 中以"矛盾"或备注形式登记，但无法自动调和。

### 3.4 公开榜污染与博弈

- 探榜/探测公开榜（s3e22 用一次提交反推目标分布）会改变"榜单作为证据"的含义；
- 公开 notebook 复制、sample_submission 套利（planttraits2024 导致换测试集+重置 LB）；
- 社区投票进入评分（kaggle-measuring-agi 的 15%）会引入曝光/互赞偏差；
- 提交策略本身是分数（fallback 套利、select_submission、阈值/裁剪），使"模型能力"与"平台规则理解"难以分离。

### 3.5 规则变化导致的伪趋势

beta/预览赛（kore-2022-beta 的 4p→2p、lux-ai-2022-beta 的 breaking change、agent beta 的预算/工具调整）在赛程中变更规则；跨版本比较方法优劣会产生伪趋势。

### 3.6 因果缺位

我们的"裁决"是观察性归纳：例如"GroupKFold 更诚实"基于数据切分逻辑与单个选手实验，并非随机对照；"多级 CE/ArcFace 有效"主要来自冠军自述的消融表。引用时应视为**待检验假设**，不是已证证明的因果结论。

## 4. 四件套自身的局限

### 4.1 images_index.csv（1666 行）

- 覆盖 `intel/<slug>/bodies/<topic>_img/` 下全部归档图片；P1（已内嵌作证）= 502，P2（digest 有占位符但未内嵌）= 1164，P3 = 0。
- P2 的上下文是**按文件序号 ↔ digest 中 `[图 N]` 占位符顺序**的近似映射；若 crawl 顺序与正文顺序不一致会错位。
- 未批量生成 OCR sidecar（DEPTH_PLAN 的可选项），图内文字只覆盖到我们人工精读的图片。
- 路径为仓库根相对路径；从 `notes/` 或 `analysis/deep/` 嵌入时需加 `../../` 前缀。
- 站外图床与私有 notebook 图不在索引中，缺口只在各深读的"图表证据/悬案"节登记。

### 4.2 claims.csv（1850 行）

- 覆盖 264 篇深读的"数字账"层：Tier B 1149 行、Tier A 701 行；不覆盖正文中的每一句量化描述。
- evidence_type 是关键词启发式分类：可复算-原文数字 1523、可复算-官方 78、自述 92、未分级 81、可复算-图证 73、矛盾 3。
- "可复算-图证"表示来源指向归档图，不代表图内数字已 OCR 校对。
- topic_ids 已用 `intel/<slug>/topics.json` 过滤为真实 id；无 topic id 的断言 source_urls 为空。
- 跨场断言的去重只按（slug, claim, value），同一断言在不同表述下可能重复。

### 4.3 lineage.md（52 节点）

- 谱系是编辑重构：节点依据"技法在该场被验证/证伪"编排，不是引用关系或时间先后；
- 传播路径（如 ArcFace 从 Hotel-ID 到 Herbarium）是方法相似性推断，缺少作者间的直接引用证据；
- 未做系统文献计量，"起源/首创"归属不可靠。

### 4.4 limitations.md（本文）

- 批判本身也基于同一批材料，受同样的幸存者偏差影响；
- 未做外部对照（官方赛后报告、论文、其他综述）。

## 5. 可复现性边界

- 比赛数据/私有数据集/平台环境（GPU/TPU、Kaggle 版本）不可完全复现；
- 深度学习随机性、早停、集成种子使数字可重复性有限；
- 部分方案依赖站外仓库与 notebook，链接失效即不可复现；
- 评测口径变更（metric bug 修复、换测试集、重置 LB）会让历史分数不可比。

## 6. 验证状态说明

- `scripts/verify_links.py`（运行时扫描 `notes/`）与 `scripts/verify_images.py`（扫描 `notes/` + `analysis/` 的 Markdown 图片路径）是当前仓库的自动门禁；
- `analysis/claims.csv` 与 `analysis/images_index.csv` 的 URL 另行用 `topics.json` 全量校验（claims 1177 条、images_index 1666 条，均 0 错）；
- 自动校验只证明"链接/路径真实"，不证明"结论正确"。

## 7. 使用建议

1. 把 `THEORY.md` 的 L/T 条目当**待检验假设**，在自己的数据上做最小对照实验；
2. 引用具体数字前，回到 `analysis/deep/<slug>.md` 的"证据分级"与原文 topic；
3. 用 `claims.csv` 做检索与横向比较，但先看 evidence_type 与 source；
4. 用 `lineage.md` 找方法灵感，用 `limitations.md` 评估适用边界；
5. 新归档场次时按同一模板追加，并保留"悬案与缺口"节——失败与未知同样是资产。
