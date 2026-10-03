# 面向新手的 Kaggle 学习路径

> 版本：v1.1 ｜ 依据：`playbook/` 六册（通用/NLP/科学/CV/音频元类/sim-agent 均已升级）+ `notes/` 已完成的 195 篇比赛摘要
> 使用方式：**按能力顺序推进，不要按比赛年份或奖金大小选比赛**。

## 阶段 0：平台与工具（1–2 天）

**目标**：能独立完成"找到比赛 → 下载数据 → 提交 → 看分"的闭环。

1. 读 `notes/other/gemini-3.md`，理解"非建模类比赛"长什么样（避免一开始就选错赛道）。
2. 用 `playbook/tabular.md` 第 2 节的 8 步工作流过一次流程。
3. 本机环境：`/root/miniconda3/envs/kaggle`（CLI 2.2.4 + kagglehub，账号已认证）。

## 阶段 1：验证设计（最重要的地基，1–2 周）

**为什么先学这个**：ICR 那场比赛的 1st → 私榜 967 名，全部差异来自验证。

| 学习材料 | 你要掌握的 |
| --- | --- |
| `notes/tabular/icr-identify-age-related-conditions.md` | 时间漂移下如何设计滑动窗口 CV；公开榜何时是陷阱 |
| `notes/tabular/amex-default-prediction.md` | 分组验证 + 数据清洗优先 |
| `notes/nlp/jigsaw-toxic-severity-rating.md` | Union-Find 防文本泄漏 |
| `notes/nlp/commonlit-evaluate-student-summaries.md` | 按"来源"分组（4 个题目 vs 122 个题目） |

**练习**：拿任一表格赛数据，分别用随机 K 折与分组/时间切分跑同一模型，记录两者与 LB 的差距。

## 阶段 2：数据质量与特征工程（2–3 周）

| 学习材料 | 你要掌握的 |
| --- | --- |
| `notes/tabular/ubiquant-market-prediction.md` | 缺失即信息（停牌特征）；时间衰减加权 |
| `notes/tabular/home-credit-credit-risk-model-stability.md` | 关系型多表聚合；指标理解 |
| `notes/tabular/godaddy-microbusiness-density-forecasting.md` | 倍率建模；先做基线校准 |
| `notes/nlp/deep-past-initiative-machine-translation.md` | 语料工程（对齐/OCR/归一）压倒模型结构 |

**练习**：任选一表格赛，只用线性模型 + 特征工程，目标进入前 50%。

## 阶段 3：模型与集成（2–3 周）

| 学习材料 | 你要掌握的 |
| --- | --- |
| `notes/tabular/optiver-realized-volatility-prediction.md` | **消融思维**：单模型 vs 集成到底差多少（本场只差 0.0002） |
| `notes/nlp/feedback-prize-english-language-learning.md` | 多模型多池化 + 爬山法加权 |
| `notes/tabular/optiver-trading-at-the-close.md` | 树模型 + 序列模型融合、权重搜索 |

**练习**：对同一个任务，先跑单模型，再跑集成，量化集成收益；写一段结论说明"值不值得"。

## 阶段 4：机制与策略（1–2 周）

| 学习材料 | 你要掌握的 |
| --- | --- |
| `notes/tabular/predict-energy-behavior-of-prosumers.md` | 在线学习（能更新就更新） |
| `notes/tabular/march-machine-learning-mania-2026.md` | 概率校准；小样本下的提交策略 |
| `notes/tabular/hull-tactical-market-prediction.md` | 指标是 Sharpe 时，组合构建比预测更重要 |
| `notes/nlp/llm-prompt-recovery.md` | 指标套利的边界（知道但别依赖） |

**练习**：读完一场比赛的 metric 定义后，先写出"这个指标奖励什么行为、惩罚什么行为"，再开始建模。

## 阶段 5：分主题深入（按兴趣选 1–2 个）

| 主题 | 入口 playbook | 首个推荐比赛 |
| --- | --- | --- |
| 表格/时序 | `playbook/tabular.md` | ICR → Amex → Enefit |
| 计算机视觉 | `playbook/cv.md` | Petfinder → RSNA 2022 → Vesuvius 墨迹 |
| NLP/LLM | `playbook/nlp.md` | Jigsaw Toxic → Deep Past → LLM Science Exam → AIMO |
| 科学计算 | `playbook/science.md` | ROGII → Novozymes → Polymer |
| 优化博弈 / agent | `playbook/sim-agent.md` | Kore 2022 → Santa 2024 → Lux S3 |
| 多模态 / 音频 | `playbook/multimodal-audio-other.md` | CMI 传感器 → BirdCLEF 2025 |

**另一条赛道（非建模）**：如果你更擅长写作、产品与叙事，走 `multimodal-audio-other.md` §2 的路线——黑客松（零算力起步）→ Kaggle Survey 分析赛 → NFL BDB 类评审制分析赛。这类比赛不拼 GPU，拼领域定义与表达能力，且官方明言是"简历加速器"。

## 阶段 6：参赛与复盘（持续）

1. 选一场**正在开放**的比赛（Playground 系列最适合第一个正式成绩）。
2. 全程按 `playbook/tabular.md` 的 8 步工作流执行，并把每一步的决策写进实验日志。
3. 赛后写自己的 write-up（对照 `notes/` 里的高分方案找差距）。

## 三条贯穿始终的原则

1. **先读指标与赛制，再碰数据**——它决定一切后续选择。
2. **验证设计优先于模型**——本地不可信时，任何提升都是幻觉。
3. **量化每个决策的收益**（消融），别凭感觉堆组件。

## 附三：提交与定稿（分数管理，第五项基本功）

近 40 篇摘要反复证明：**最后 0.001 的分数往往来自"怎么选提交"，而不是"再训一个模型"**。定稿前过一遍清单：

| 动作 | 依据 |
| --- | --- |
| 画出自己的 CV–LB 轨迹，找"可信区间"，不选孤立最高 CV | S6E2（CV>0.95578 后不再兑现）、S5E12（gap 监控） |
| 相关性嘈杂时多份对冲提交（互补结构 > 同质高分） | S6E4（High 类敏感）、S5E5（74 模型 vs 11 模型两路） |
| 用秩平均替代概率平均，抗校准漂移与私榜抖动 | S6E2、S6E3 的 rank blend |
| 无选择的全量平均会伤分：先选子集（Optuna/HC）再 Ridge | S6E2、S6E1 |
| 不追公开榜；大洗牌场次（S5E3/S5E7/S5E12）以 CV + 结构稳健为准 | 多场 |
| 保留全部候选与 OOF 档案，最后统一选择 | Playground 系列通用教训 |

**口诀**：验证决定你能否得分，特征决定你能得多少分，**提交选择决定你最终交出哪一份分**。

## 附：跨领域方法迁移清单（读得越多越值钱）

以下技术在 **多个不同主题**的比赛里被反复验证，属于"学一次、到处能用"的资产：

| 技术 | 原始领域 | 迁移到的场景 | 证据 |
| --- | --- | --- | --- |
| 框融合（Weighted Box Fusion） | 目标检测 | 文本跨度抽取、生理事件检测 | Feedback 2021、CMI Sleep States |
| k-opt / 迭代局部搜索 | 旅行商问题（TSP） | LLM 困惑度优化 | Santa 2024 2nd |
| BM25 / TF-IDF / LSI | 信息检索 | 单细胞多组学稀疏计数矩阵 | Open Problems Multimodal 2nd/3rd |
| 偏差特征（减组中位数） | 结构化特征工程 | 金融时序、传感器 | Optiver Close、Optiver Vol |
| 事件合并 + 容差后处理 | 检测/检索评测 | 事件级 F1 任务 | CMI Sleep States |
| 辅助任务（把弱相关模态当标签） | 多任务学习 | 图像 + 元数据 | Petfinder 6th |
| 物理对称性增强 | 物理学/几何先验 | 多智能体轨迹预测 | NFL Big Data Bowl 2026 |
| 测试时训练（TTT） | 在线学习 | 规则在测试期才可见的分类 | Jigsaw Agile Rules 3rd |
| 自洽投票 + 熵加权 | 推理工程 | 无需训练拉高准确率 | AIMO 3 1st/2nd |
| 合成数据"难度阶梯" | 数据增强 | 训练样本极少的推理任务 | ARC Prize 2025 NVARC |

**使用方法**：进入一个新比赛时，先问"这个问题在别的领域里解决过吗"，再到本清单里找对应技术——比从零设计快得多。

## 附二：黑箱评分下的迭代搜索（另一条高频规律）

当**评分函数可以反复查询**（排行榜、本地可调用的评测器、平台配对），"用反馈做迭代搜索"往往比"一次性训练好模型"更有效。已在至少四类比赛里验证：

| 场景 | 做法 | 证据 |
| --- | --- | --- |
| 安全 CTF | 对着 ID 列表做爬山，直到分数足够拿 flag | AI Village CTF 6th |
| 组合优化 | 局部搜索/模拟退火（每步都能精确评估） | Santa 2024/2025 |
| 黑箱评分器 | 探针 + 后处理对齐隐藏护栏 | AI Agent Security 11th |
| 可操纵指标 | 识别指标漏洞并谨慎下注 | Home Credit 1st（"下注策略"） |

**前提与风险**：

1. 先确认规则允许（探针/爬榜在部分比赛被禁止或惩罚）。
2. 若公开榜与私榜脱节（ICR、Novozymes、ARC），**迭代到公开榜高分可能适得其反**——先量化 CV-LB 一致性。
3. 迭代搜索的收益会快速递减，注意设置停止条件与时间预算。

> 本路径会随笔记增加持续修订；当前已完成 195/264 场摘要，后续补充会让各阶段材料更完整。
