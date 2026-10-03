# AI Mathematical Olympiad Progress Prize 2 轻量深读（Tier B）

> 赛事：Featured ｜ 主题 nlp（数学推理/LLM）｜ 2212 队 ｜ 代码赛（离线 Notebook，L4x4）｜ 指标：Accuracy（50 题，1 提交/天）
> 材料基础：`digests/ai-mathematical-olympiad-progress-prize-2.md`（digest 收 2 篇；`intel/.../bodies/` 已有 **14 篇**本地归档 write-up——1st/2nd/3rd/4th/5th/7th/8th/11th/17th/20th/21st 等，按"≤3 篇才补采"规则直接使用）+ 8 张图
> 轻读时间：2026-10（Tier B B04）

## 1. 一句话重述与数字账

在 Kaggle Notebook（L4x4、严格时限）里离线跑 LLM 解 50 道 AIME/HMMT 级数学题。真正的考点是**"推理能力 × 推理效率 × 测试时策略"三角**：模型几乎全是 DeepSeek-R1-Distill-Qwen-14B 系，胜负在量化/加速/早停/采样预算。

| 关键数字 | 值 | 来源 |
| --- | --- | --- |
| 1st（NemoSkills，147 票） | 数据：540K AoPS 题 → 3.2M CoT（R1/QwQ-32B 多候选+答案校验）；TIR：LIMO 冷启 → 迭代生成/过滤（1.7M→15K）；训练：Qwen2.5-14B SFT 2.2M CoT 8 epochs（RoPE 500k，**512×H100 48h**，20% 算力可得大部分强度）+ TIR 400 步；**线性 merge CoT×0.3+TIR×0.7**：maj@16 62.9/66.8→**69.1**，长度 15834→12489，代码执行 2.73→0.85；推理：TensorRT-LLM + FP8 + **ReDrafter 投机解码（1.8×，65% 接受）**，bf16 210→f8+redrafter 554 tok/s；12 路异步 + 流式早停（5 中 4 同/10/12 完成）+ 时间缓冲（350s+210s） | 1st |
| 2nd（imagination-research，111 票） | R1-Distill-Qwen-14B；SFT 8 epochs（Light-R1 stage2+LIMO；8×A800 11h）→ **DPO 压长度**（正确性/长度比/最短/相似度四准则；4 epochs 40h）；lmdeploy TurboMind + **AWQ4 + KV8**（W4KV8 比 FP16 快 55%、样本精度 -5~10%）；15 样本（7 CoT+8 code）+ 样本级/题级早停 + 按剩余时间调超参；公 34/50（第 1）→ 私 31/50（第 2） | 2nd |
| 3rd（58 票） | **零训练**：R1-Distill-Qwen-14B AWQ；核心是**分支复用推理**：5 分支×4096 token → 复制到 10 → 若 ≥6 完成且某答案 >70% 即停；否则复制 7 条未完成到 14 分支×4096；vLLM `enable_prefix_caching` 复用 KV；私 30/50 | 3rd |
| 8th（65 票） | 单模型（自量化 R1-14B AWQ-4bit GEMM）+ 单 prompt + vLLM V1；**Attempts=5**（时间/稳定性折中）；私 28/50；观察到模型"我 Google 过类似的题"式幻觉 | 8th |
| 其他 | 4th/5th/7th/11th/17th/20th/21st 本地均有 write-up（大量代码题路线） | 本地 bodies |

## 2. 逐方案对照矩阵

| 维度 | 1st | 2nd | 3rd | 8th |
| --- | --- | --- | --- | --- |
| 训练 | 2.2M CoT SFT + 15K TIR + merge | SFT + DPO（压长度） | **无** | **无** |
| 基座 | Qwen2.5-14B→自训 | R1-Distill-14B | R1-Distill-14B AWQ | R1-Distill-14B AWQ4 GEMM |
| 引擎/量化 | TensorRT-LLM FP8 + ReDrafter | lmdeploy AWQ4 + KV8 | vLLM + prefix caching | vLLM V1 |
| 测试时策略 | 12 路 + 流式早停 + 时间缓冲 | 15 样本（CoT+code）+ 双层早停 | **分支复制 + 70% 共识早停** | 5 attempts |
| 私榜 | 1st（CV 与私榜更一致） | 31/50（2nd） | 30/50（3rd） | 28/50（8th） |

## 3. 共识、分歧与裁决

### 共识一：基座几乎是唯一的——R1-Distill-Qwen-14B 系（4/4）

1st 自训也从 Qwen2.5-14B；2nd/3rd/8th 直接用 R1-Distill-14B（AWQ/自量化）。**裁决**：本赛在算力/时限约束下，14B 蒸馏模型是能力/速度的最优点；训练是"锦上添花"而非必需。置信度：高。

### 共识二：效率工程是半壁江山（4/4）

量化（FP8/AWQ4）、KV 量化、投机解码（ReDrafter 1.8×）、前缀缓存（3rd）、in-flight batching、流式早停、时间缓冲。**裁决**：在固定 5 小时/50 题的预算里，推理吞吐直接换成尝试次数/更长的思考；不做效率工程等于自愿砍分。置信度：高。

### 共识三：测试时用"多样本 + 多数投票 + 早停"（4/4）

maj@12/16（1st）、15 样本（2nd）、14 分支（3rd）、5 attempts（8th）；都有题目级/样本级早停与时间自适应。**裁决**：测试时扩展的收益取决于"样本多样性×共识速度"；早停规则（如 5 中 4 同、70% 共识）是效率核心。置信度：高。

### 共识四：长度控制直接决定可行性（1st/2nd）

1st 的 merge 把平均长度从 15834 降到 12489（代码执行 2.73→0.85）；2nd 用 DPO 压长度；1st 更指出"更强的模型因 token 太多会超时未答完"。**裁决**：在时限赛里，"解得更长"可能等于"解不完"；长度是目标函数的一部分。置信度：高。

### 分歧：训练 vs 零训练

1st/2nd 投入大训练（512×H100 / 8×A800），3rd/8th 零训练仍获第 3/第 8。**裁决**：训练提升 CV 但引入 token/超时风险；零训练+优秀推理策略可以进前 3（3rd 连续两届如此）。**本场最大启示：推理工程的上限被严重低估**。置信度：高。

### 分歧：推理引擎与量化路线

TensorRT-LLM+FP8（1st）vs lmdeploy+AWQ4+KV8（2nd）vs vLLM V1（3rd/8th）。**裁决**：都能做到高吞吐；选型取决于实现熟悉度与投机解码/缓存支持；FP8 精度损失最小（1st 表：f8a16 精度与 bf16 持平）。置信度：中高。

### 事件：开源合规争议

评论区质疑"冠军未按规则开源最终提交 notebook"（3rd 帖下 32+ 小时无回应等），涉及赛事规则执行。**裁决**：登记为治理事件；材料不足以判定事实。置信度：低（单方面评论）。

### CV-LB 方差

50 题、1 提交/天、公开榜波动大（1st 不同设置 23–29）；1st 最终"私榜更接近 CV"。**裁决**：小评测集下公榜噪声极大，模型选择应以自建验证（AIME/HMMT 24-25）为主。置信度：高。

## 4. 证据分级

| 断言 | 等级 | 说明 |
| --- | --- | --- |
| 1st 的数据/训练/merge/推理表 | 自述 + 论文 + 图 + 代码 | 高（有量化表与消融） |
| 2nd 的 SFT/DPO/量化数据 | 自述 + 模型开源 | 中高 |
| 3rd 的分支复用策略 | 自述 + notebook | 中高 |
| 8th 的单模 5 attempts | 自述 + 公开模型 | 中 |
| 开源合规争议 | 评论（单方） | 低 |

## 5. 悬案与缺口（登记）

- digest 只整理了 2 篇，其余 12 篇本地 write-up 未纳入本轻读的细节对照（4th/5th/7th/11th/17th/20th/21st）——后续可按需细读。
- 官方对"开源要求"争议的处置未收录；赛事规则执行情况不明。
- 3rd 的"共享前缀相关性"缺陷未量化；分支复用的最优参数（4096/70%）只单队经验。

## 6. 图表证据

![1st 的推理流程](../../intel/ai-mathematical-olympiad-progress-prize-2/bodies/574765_img/04.png)

**图 1**（topic 574765）：Question → 批量 n 样本（maj@）→ TensorRT-LLM 异步多线程生成（流式 + 本地代码停止准则 + Flask 代码沙箱/sympy）→ 全局停止（时间或 maj@ 达成）→ 取消生成并清缓存。**"测试时扩展 + 工具集成 + 时间预算"的完整工程图**。

## 7. 出处

- 2nd（111 票）：https://www.kaggle.com/competitions/ai-mathematical-olympiad-progress-prize-2/discussion/572948
- 1st（147 票）：https://www.kaggle.com/competitions/ai-mathematical-olympiad-progress-prize-2/discussion/574765
- 3rd（58 票）：https://www.kaggle.com/competitions/ai-mathematical-olympiad-progress-prize-2/discussion/573314
- 4th（573671）：https://www.kaggle.com/competitions/ai-mathematical-olympiad-progress-prize-2/discussion/573671
- 8th（65 票）：https://www.kaggle.com/competitions/ai-mathematical-olympiad-progress-prize-2/discussion/571356
- 本地其他 write-up：5th 574262、7th 572760、11th 573086、17th 573071、20th 575172、21st 571289
