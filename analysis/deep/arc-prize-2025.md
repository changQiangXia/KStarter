# ARC Prize 2025 轻量深读（Tier B）

> 赛事：Featured ｜ 主题 nlp（抽象推理，代码赛）｜ 1455 队 ｜ 12 小时 / 4×L4 / 30GB ｜ 指标：ARC-AGI-2 准确率（公开 120 题 + 私有 120 题）
> 材料基础：`digests/arc-prize-2025.md`（6 篇正文：NVARC 651671 / 3rd MindsAI&Tufa 629790 / 5th 617939 / ARChitects 656966 / 2024 复盘 575595 / 公榜第一自述 614436；80 条主题索引）+ 4 张归档图（2 张有信息量）
> 轻读时间：2026-10（Tier B B11）

## 1. 一句话重述与数字账

ARC-AGI-2 抽象推理：给几对输入/输出网格、推出变换并预测测试输出，**一个像素错就整题失败**。本届的核心结论是"**预训练规模 + 测试时自适应 + 候选重打分**"三件套——NVARC 用 LLM 生成 10 万+ 合成谜题（320 万增强样本）并做逐题 LoRA + 批量 DFS，赛内公榜最好 27.64%；MindsAI&Tufa（私榜 3rd，15.42%）用 660M CodeT5 自训 1 亿+ 推理样本，靠 TTT+AIRV 拿到 8–12× 增益；ARChitects 从自回归转向**掩码扩散递归精化**（已知形状 ~30.5%±1%），却因 shape predictor 与提交选择失误只落在公 21.67 / 私 16.53。

| 关键数字 | 值 | 来源 |
| --- | --- | --- |
| NVARC（651671） | 合成管线：716 个真实谜题描述（H-ARC 1700 人 + BARC 160）→ 266,593 混合摘要 → 126,901 输入格程序 → 103,253 完整谜题；gpt-oss-120b + NeMo-Skills（8×H100 = 15k tokens/s）；3.2M 增强样本（MINI-ARC 147 / ConceptARC 160 / RE-ARC 400 / ARC-AGI-2 609 / NVARC 47,337–55,886）；4B 全参微调 4 节点×8×H100×27h；逐题 LoRA r=256/α=32、bf16；批量 DFS（确定性版慢 17% 未用）；重打分 = 候选出现频次 × 多增强 log-prob 几何平均；最佳模型公榜 **27.64%**；TRM：24h/8×H100 复现 → Kaggle 2h 内 2.08% → 选点技巧 7.5% → 赛后 4k epochs **10.0%**；TRM+Qwen3 2B 21.53→22.50，与 4B 组合 27.22→27.22 | 651671 |
| 3rd MindsAI&Tufa（629790） | 私榜 **15.42%**；660M CodeT5-Large（encoder 24 / decoder 16）+ 1 亿+ 推理样本（~70M ARC 风格），TPU 累计至 2.5 年；TTT ~45k 步 + AIRV 每题 10k 增强 → 相比零样本 **8–12×**（两者近似可加）；自集成两 checkpoint 优于 2× 采样（+6.2%）；mixup/combine 增强 +6.3% top-2（ARC 1.5）；决赛 4×L4 约 11 小时；简化版 77M 单 P100 10–60 分钟可达 90–95% 相对增益 | 629790 |
| ARChitects（656966） | 掩码扩散 LLaDA-8B：soft-masking + 递归潜变量采样（token algebra）、2D 位置编码（Golden Gate RoPE）；预训练 ~175k 步（bs 8、8×H100）；每题 TTT 128 步（L4）；独立 shape predictor 85%±2%；已知形状 **30.5%±1%**（102 步 = 2×51 冷重启）；预期 ~26%，实际公 **21.67** / 私 **16.53**；未选提交 19.17/19.17；早期 AR 路线（Mistral-NeMo-Minitron-8B）公榜上限 16.94% | 656966 |
| 5th（617939） | fork 2024 ARChitects 冠军方案（Nemo Mini + LoRA r=32、仅前 32 层、4 GPU、seq 4224/8192、4 epoch×240 步、lr 1e-4/1e-5）；唯一关键改动 = 随机种子 **19920627**；公榜 4.17%（344 名）→ 私榜 **第 5**；种子间分数 3.33–6.67%（±4 题 / 120） | 617939 |
| 2024 复盘（575595） | 2nd Omni-ARC TTT（Qwen-0.5B 逐题 TTT + AIRV + C++ DSL 回退 +14 分）；3rd Guided Brute-Force（120 个手工函数、700 行 Python 40 分）；4th DSL/DAG 深搜 + CNN/决策树；5th 六求解器 mega-ensemble + 自动修复 + 二分猜题序；13th 19-token 自训 Transformer（reverse 增强 +27、投票 31 分）；21st 颜色重映射预处理（+2 分到 28%）；34th LLaMA 3.1 8B + 2020 求解器混合 | 575595 |
| 公榜第一自述（614436） | 团队 sorokin + Ivan 末周冲上公榜第一；因排队 10 小时，只能提交"约 5% 题会超时"且方差大的版本；作者自述预期私榜回落 | 614436 |
| 赛事治理 | "Deadline and the queue"（21 票 / 23 评论）、"队列突然变糟"（14 票）、"隐藏测试可能只有 1 个训练样本"（32 票）、"测试集编辑"（20 票） | 614325 等 |

## 2. 逐方案对照矩阵

| 维度 | NVARC | MindsAI&Tufa（3rd） | ARChitects | 5th（私榜） |
| --- | --- | --- | --- | --- |
| 基础模型 | Qwen3 4B（全参微调）+ TRM 7M 集成 | CodeT5-Large 660M（encoder-decoder，自训） | LLaDA-8B（掩码扩散） | Nemo Mini（2024 冠军底座） |
| 训练数据 | 10 万+ 合成谜题、3.2M 增强样本 | 1 亿+ 推理样本（含 ~70M ARC 风格） | ReARC / ARC-GEN-100K / ARC1&2 / Arc-Heavy / ConceptARC | ARC 2024 数据 |
| 测试时自适应 | 逐题 LoRA（r=256）+ DFS + 重打分 | TTT（4.5 万步）+ AIRV（1 万增强） | 逐题 TTT 128 步 + 递归精化 | 逐题 priming + Turbo DFS |
| 解码/选择 | 批量 DFS + 频次×几何平均 | AIRV 投票 + 双 checkpoint 集成 | 软掩码递归采样（2×51 步） | 束搜索 + 多增强打分 |
| 关键弱点 | 确定性 batch DFS 慢 17% 未用上 | ARC-AGI-2 对 TTT/AIRV 部分对抗 | shape 预测误差 + 选错提交 | 依赖种子运气（小样本方差） |
| 结果 | 公榜 27.64%（赛内报道最好） | 私榜 3rd（15.42%） | 公 21.67 / 私 16.53（未选 19.17） | 私榜 5th |

## 3. 共识、分歧与裁决

### 共识一：测试时自适应（TTT / 逐题微调 + 增强推理）已是顶级方案必备件（NVARC、MindsAI、5th、2024 多队；置信度高）

NVARC 每题单独 LoRA 微调；MindsAI 的 TTT+AIRV 合计给出 8–12× 增益；5th 全盘继承 2024 ARChitects 的逐题 priming/打分框架；2024 的 2nd、13th 也都以逐题训练 + 反向增强为核心。**裁决**：ARC 上"预训练 + 测试时自适应"是标准范式，固定权重的零样本方案很难竞争。置信度：高。

### 共识二：合成数据的规模与质量决定预训练上限（NVARC、MindsAI、575595；置信度中高）

NVARC 的 loss 曲线显示"去掉 BARC、加更多 NVARC 合成数据"可从 12.92% 提升到 27.64% 公榜；MindsAI 训练 1 亿+ 样本；2024 各队也普遍生成合成训练格。**裁决**：ARC 监督极稀疏，"描述 → 程序/谜题"的生成式数据管线是当前最有效的规模化手段。置信度：中高（loss↔公榜相关来自自述图）。

### 共识三：小样本（120 题）上，"重打分/超参/种子"与模型能力同量级（5th、ARChitects、614436；置信度高）

5th 只改种子就从公榜 344 名到私榜第 5（种子间波动 3.33–6.67%）；ARChitects 因选了公榜更高的提交少拿 2.6 分（16.53 vs 19.17）；614436 因队列被迫提交了方差大的版本。**裁决**：小样本赛必须把选择策略（重打分、模型选择、提交选择）当一等公民，并显式接受高方差。置信度：高。

### 分歧一：自回归 vs 掩码扩散（ARChitects 转向 vs NVARC 押注 AR；置信度中高）

ARChitects 发现 AR 顺序生成不可回改、难处理全局重构，转向掩码扩散 + 递归精化；NVARC 则继续改进 ARChitects 的 AR 线并报道了赛内最高公榜分。**裁决**：两条路线在 ARC-AGI-2 上都有效，但失效模式不同——扩散擅长"整体重写"，AR+DFS 擅长局部可验证搜索；把 TRM 等异质候选并入 AR 候选池（NVARC 已试）是自然的融合方向。置信度：中高。

### 事件：排队/超时/提交选择是最大的非技术风险（614325、611119、614436、573301；置信度中高）

"Deadline and the queue"与"队列突然变糟"集中反映排队问题；614436 因 10 小时排队只能提交会超时的版本；另有"测试集编辑"与"隐藏测试可能只有一个训练样本"的规则风险帖。**裁决**：代码赛应给运行/排队留足冗余，并让"最佳提交"与"最稳提交"分离。置信度：中高。

## 4. 证据分级

| 断言 | 等级 | 说明 |
| --- | --- | --- |
| MindsAI 的 TTT/AIRV 消融与增益 | 自述 + 官方 PDF + 开源代码/数据 | 高 |
| NVARC 的数据管线、训练配置与分数 | 自述 + 2 张图（管线/曲线） | 中高 |
| ARChitects 的公私榜数字、shape 准确率与两版提交 | 自述 + 技术报告 | 中高 |
| 5th 的种子方差（3.33–6.67%）与名次跃迁 | 自述 | 中 |
| 2024 各名次方案细节 | 二次汇编帖 | 中 |
| 排队/截止/测试集编辑 | 多帖互证 | 中高 |

## 5. 悬案与缺口（登记）

- 最终私榜完整名次（除 3rd MindsAI、5th 作者外）未在归档正文确认；NVARC 最终名次与 TRM 融合结果未更新；
- 614436 团队最终成绩、"Post comp update"（652927）与 615018（29.72 分帖）未细读；
- 2024 方案细节（如 Omni-ARC 论文）未展开；
- 归档 4 图中仅 2 张可用（NVARC 管线图 + loss 曲线）；ARChitects 两张为版画/封面图，无信息量；
- **图证缺口**：无排行榜/提交界面类证据图。

## 6. 图表证据

![NVARC 总体流程](../../intel/arc-prize-2025/bodies/651671_img/01.png)

**图 1**（topic 651671，NVARC）：三段式流程——合成数据生成（~5k 人类描述 → ~267k 混合摘要 → ~127k 输入程序 → ~103k 谜题）→ 离线训练（Qwen3 4B 3.2M 样本 / 32×H100 27h；TRM 7M 1M 样本 / 8×H100 24h）→ Kaggle 在线（12 小时、4×L4：逐题 LoRA → DFS 生成 → 重打分 → TTFT）。

![合成数据规模与验证 loss](../../intel/arc-prize-2025/bodies/651671_img/02.png)

**图 2**（topic 651671，NVARC）：验证 loss 随训练步数下降；标注显示"去掉 BARC、增加 NVARC 合成数据"的配置达到最佳公榜 27.64%，而含 BARC 的配置停在 12.92–17.50%。

## 7. 出处

- NVARC 方案（123 票）：https://www.kaggle.com/competitions/arc-prize-2025/discussion/651671
- MindsAI & Tufa Labs 3rd（16 票）：https://www.kaggle.com/competitions/arc-prize-2025/discussion/629790
- ARChitects 方案（15 票）：https://www.kaggle.com/competitions/arc-prize-2025/discussion/656966
- 5th Place（13 票）：https://www.kaggle.com/competitions/arc-prize-2025/discussion/617939
- ARC 2024 复盘（49 票）：https://www.kaggle.com/competitions/arc-prize-2025/discussion/575595
- 公榜第一自述（152 票 / 106 评论）：https://www.kaggle.com/competitions/arc-prize-2025/discussion/614436
- Deadline and the queue（21 票）：https://www.kaggle.com/competitions/arc-prize-2025/discussion/614325
- 队列突然变糟（14 票）：https://www.kaggle.com/competitions/arc-prize-2025/discussion/611119
- 隐藏测试可能只有 1 个训练样本（32 票）：https://www.kaggle.com/competitions/arc-prize-2025/discussion/578736
- 测试集编辑（20 票）：https://www.kaggle.com/competitions/arc-prize-2025/discussion/573301
- Post comp update（20 票）：https://www.kaggle.com/competitions/arc-prize-2025/discussion/652927
