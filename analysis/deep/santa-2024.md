# Santa 2024 深读：困惑度置换 × 受限 k-opt/ILS × 批量并行 SA

> 赛事：Featured（Santa 年度赛）｜ 主题 sim-agent（黑箱组合优化）｜ 1514 队 ｜ 标准赛（无运行时间限制）｜ 指标：官方 metric.py 的语言模型困惑度（越低越好）
> 材料基础：`digests/santa-2024.md`（6 篇正文：批量困惑度 92 / 1st 85 / 2nd@zaburo 43 / 5th CPMP 43 / sample5 41 / SA 总论 59；80 条主题索引）+ 6 张图；**1st 正文仅有 repo 链接（398B 存根）**
> 深读时间：2026-10（Tier A #57）

## 0. 一句话重述：这道题真正在考什么

题面是"把每个样例的词序重排，使一个语言模型对整段文本的困惑度最低"——真正的考题是**在黑箱、昂贵、非局部的评分函数上跑启发式搜索**。四件事：

1. **先对齐评分函数**：官方 `metric.py`（v29、float16）必须本地精确复现；batch_size>1 时要 `padding_side="right"` + 屏蔽 pad token + 按有效 token 求平均（Chris Deotte，92 票）。批量与逐行评分还有 cuBLAS kernel 带来的微小差异——搜索算法必须在"有噪声的靶子"上爬山。
2. **把 TSP/ATSP 启发式搬过来，但按目标函数改造**：2nd 用受限 k-opt（禁止翻转、限制移动子序列长度）+ 自定义 kick 的 ILS；5th 用全局上界接受准则的 SA 变体 + multi-point 并行 + ATSP 的 double root-and-stem 移动；社区总论帖用标准 SA。
3. **非局部目标 → 必须砍搜索空间**：移动一个词会改变其后所有词的上下文，无法像 TSP 那样 O(1) 增量算分；2nd 把移动限制为 (k=3, max_moving=5) 与 (k=4, max_moving=1)，才把 Problem 5 的全部候补移动压到 4090 上 ~18 分钟；5th 用分数字典缓存 + 批量 104 + 98% GPU 利用率。
4. **用问题结构压缩解空间**：sample 5 的 100! 空间可用"停用词/字母块"排序先验压缩（44.0 起点 → 顶尖队伍做到 28.5）；2nd 的 28.5 来自**打破块结构**的定制 kick：(停用词)(优化非停用词)(其他停用词)(近排序非停用词)；多起点（multi-start）是标准配置。

一句话：**这是一场"评分函数工程 + 邻域设计 + GPU 预算管理"的比赛**——算法家族（SA/ILS/k-opt）是公共知识，胜负在候选移动的取舍与结构先验。

## 1. 材料与角色

| 帖子 | 作者 | 票数 | 角色与独有信息 |
| --- | --- | --- | --- |
| [548249](https://www.kaggle.com/competitions/santa-2024/discussion/548249) 批量困惑度正确算法 | Chris Deotte | 92 | `padding_side="right"`、pad token 屏蔽、按有效长度平均；batch=64 在 2×T4 上暴力搜 sample#0；评论区记录批量 vs 逐行的 cuBLAS 微小差异 |
| [560560](https://www.kaggle.com/competitions/santa-2024/discussion/560560) 1st | — | 85 | **正文缺失**：仅感谢 + repo 链接（github.com/Lgeu/santa2024，en/ja 说明）——本场最大的材料缺口 |
| [548476](https://www.kaggle.com/competitions/santa-2024/discussion/548476) 255.9 通用解（SA 总论） | ONODERA | 59 | SA 为什么适用（逃局部最优/模块化/历史成功 TSP 类比）；greedy vs SA 接受率热力图（图 1/2）；评论区：前 6 名有 5 个日本队、SA 是 AtCoder Heuristic 的主流 |
| [560533](https://www.kaggle.com/competitions/santa-2024/discussion/560533) 2nd（@zaburo 部分） | KaizaburoChubachi | 43 | **受限 k-opt + 自定义 kick 的 ILS**：禁止翻转、(k=3,max_move=5)/(k=4,max_move=1)、全移动测试 ~18 分钟/4090、Problem 5 的 28.5 与 Problem 3 的 191.x、多起点、结构分解 kick；明确不用 SA/GA |
| [560597](https://www.kaggle.com/competitions/santa-2024/discussion/560597) 5th（CPMP 部分） | CPMP | 43 | SA 变体（全局上界接受）；multi-point 并行（N=最大 batch，A100 上 104）；k-opt（分段随机洗牌，k≤10）+ remove-insert + ATSP double root-and-stem；**位置折扣困惑度**与前缀限制；98% GPU 利用率 + 分数缓存；失败清单（Sinkhorn/KL、logits→ATSP、MCTS/RL） |
| [559339](https://www.kaggle.com/competitions/santa-2024/discussion/559339) sample 5 团队解 | WOOSUNG YOON | 41 | 字母序排序 44.0 → 按字母块 sharding（100! → 块内排列）；SA 在块间搬词；**赛期内发布**引发"gold zone 会被同分填满"的争议与公平性讨论（图 5/6） |

**材料缺口（受"仅 ≤3 篇场次定点补采"约束，登记备查）**：本场收录 6 篇但 1st 正文为空（仅 repo 链接）；主题索引中还有 2nd 另两位队友 [560540](https://www.kaggle.com/competitions/santa-2024/discussion/560540)（27 票）/ [560565](https://www.kaggle.com/competitions/santa-2024/discussion/560565)（26 票）、[3rd 560620](https://www.kaggle.com/competitions/santa-2024/discussion/560620)（30）、[4th 560536](https://www.kaggle.com/competitions/santa-2024/discussion/560536)（32）、[10th 560531](https://www.kaggle.com/competitions/santa-2024/discussion/560531)（32）、[11th 560542](https://www.kaggle.com/competitions/santa-2024/discussion/560542)（33）、[13th](https://www.kaggle.com/competitions/santa-2024/discussion/560531) 等 write-up 未收录；机制/事件帖 [551818](https://www.kaggle.com/competitions/santa-2024/discussion/551818)（248.5 搜索方向，59 票）、[556784](https://www.kaggle.com/competitions/santa-2024/discussion/556784)（各 sample 最优分揭示，36）、[551902](https://www.kaggle.com/competitions/santa-2024/discussion/551902)（256.6 教程，60）、[555881](https://www.kaggle.com/competitions/santa-2024/discussion/555881)（公开顶级解危险，26）、[547676](https://www.kaggle.com/competitions/santa-2024/discussion/547676)（指标修订与重打分，27）、[547505](https://www.kaggle.com/competitions/santa-2024/discussion/547505)（LB hack 被修复，25）、[557817](https://www.kaggle.com/competitions/santa-2024/discussion/557817)（300 词加赛，25）、[555545](https://www.kaggle.com/competitions/santa-2024/discussion/555545)（困惑度进度图，25）、[550287](https://www.kaggle.com/competitions/santa-2024/discussion/550287)/[550429](https://www.kaggle.com/competitions/santa-2024/discussion/550429)（sample 6 排序 53.46/48.69）未收录。

## 2. 逐方案对照矩阵

| 维度 | 2nd @zaburo | 5th CPMP | sample 5 团队 | 社区 SA 总论 | 1st |
| --- | --- | --- | --- | --- | --- |
| 算法家族 | ILS + 受限 k-opt + 自定义 kick | SA 变体 + multi-point 并行 | 块 sharding + SA | 标准 SA | 未知（repo 链接） |
| 邻域移动 | k-opt（禁翻转、限移动子序列长） | k-opt 分段洗牌；remove-insert；ATSP double root-and-stem | 块间搬词/块内排列 | 未展开 | 未知 |
| 逃逸机制 | 相邻子序列随机洗牌 kick（+样例专用转移/交换 kick） | 上界接受 + 保留 best+M + 与最优交叉 | 温度退火 | Metropolis 接受 | 未知 |
| 并行/预算 | 4090；全移动一轮 ~18 分钟 | A100；batch 104；98% GPU；分数缓存 | Kaggle Notebook 受限环境 | — | 未知 |
| 结构先验 | P5 从（停用词)(非停用词)分解到四段结构；P3 固定末词穷举 | 前缀限制 / 位置折扣 | （停用词)(字母块 A)(字母块 B) | 无 | 未知 |
| 关键数字 | P5=28.5；P3=191.x；32.xx 壁垒 | 随机起点半数以上找到最优；sample 3 依赖队友分组 | 字母序 44.0 起点 | 热力图 | 未知 |
| 明确失败 | beam search（评价函数短视）；不用 SA/GA | Sinkhorn+KL；logits→ATSP；EMA+Sinkhorn；MCTS/RL | 自述"未验证的测试代码" | — | — |

## 3. 共识、分歧与裁决

### 共识一：评分函数工程先于算法（全社区）

92 票的批量帖把 `padding_side`、pad 屏蔽、有效长度平均讲透；评论区确认批量/逐行存在 cuBLAS 级别差异（搜索噪声）；metric 还有过一次"修订与重打分"事件（547676）。**裁决**：黑箱评分任务的第一个交付物是"与官方逐位一致的本地评分器 + 批量化"；批量既是加速手段也是正确性风险点。置信度：高。

### 共识二：TSP/ATSP 启发式可直接迁移，但必须按目标函数改造（2/2 有方法的队）

2nd 迁移 k-opt + double-bridge kick 后改造（禁翻转、限移动长度）；5th 迁移 k-opt/remove-insert/double root-and-stem。**裁决**：组合优化的算法骨架（邻域 + 扰动 + 接受）是通用语言；不可迁移的是 TSP 的假设（无向边、局部增量、对称性）——在困惑度目标下它们全部失效，需要重新推导。置信度：高。

### 共识三：非局部目标 → 候选移动必须激进剪枝，评分开销必须摊薄（2/2）

2nd：(k=3,max_move=5)+(k=4,max_move=1)，P5 全移动 ~18 分钟；5th：分数缓存字典 + batch 104 + 98% 利用率。**裁决**：这类任务的瓶颈是"每次移动的评分成本 × 候选数量"；两队的两种极端——"少候选 × 精确评分"（ILS）与"全候选 × 批量近似评分"（SA）——都能赢，但都离不开剪枝与批量化。置信度：高。

### 共识四：结构先验价值巨大（sample 5 全社区 + 2nd 的 P5 kick）

字母序排序 44.0 → 块结构把 100! 压成块内排列 → 2nd 用四段结构 + 定制 kick 拿到 28.5；sample 6 也有"排序/停用词优先"的社区分数链（53.46→48.69）。**裁决**：黑箱优化里"从数据里读出的结构"等价于免费的白箱信息；但结构一旦固化也会锁死上限（32.xx 壁垒只能靠打破结构的 kick 突破）。置信度：高。

### 分歧一：SA vs ILS/k-opt

2nd 明确不用 SA（"温度控制不适合这种长期、间断的计算"）也不用 GA（缺乏 TSP 式的有效交叉）；5th 用 SA 变体并发扬光大；ONODERA 用标准 SA 并给出接受率热力图。**裁决**：两者都是"邻域 + 逃逸"的实现差异——ILS 适合长周期人工干预、确定性复现；SA 适合批量并行、连续算力（尤其 GPU 批评分）。选型应匹配算力形态而非信仰。置信度：中高。

### 分歧二：接受准则（Metropolis vs 全局上界）

5th 用"新解 < 全局上界即接受，上界定期下调"替代 `exp(−Δ/T)`，自称同等有效且更高效。**裁决**：在评分昂贵、只关心 best-so-far 的场景，接受准则只需保证"探索 + 单调收紧"；上界式接受把温度调度换成阈值调度，减少一次指数运算与温度调参。置信度：中（单队自述，无消融数字）。

### 分歧三：位置偏差怎么修

5th 观察到**序列前部的修改影响更大**：(a) 队友方案：把移动限制在前缀；(b) 自研：维护每个位置的平均 logit，用"折扣困惑度"（logits 按位置均值归一）作为接受判据。**裁决**：LM 困惑度天然带位置难度差异，不归一化会让搜索偏向尾部；两种修法等价于"把目标变成位置可比的量"。置信度：中高（机制清晰，但缺量化消融）。

### 分歧四：赛期内公开解的方法论（伦理争议）

sample 5 团队在赛期发布思路，评论区出现"会把 gold zone 填满同分"（24 票帖《Publishing top solution is dangerous》同题）与"为公平性而发"的对抗评价。**裁决**：在"每样例单一答案 + 同分并列"的启发式比赛里，公开解把金牌竞争变成"复现速度 + 提交时机"的彩票——这是社区规范问题，不是技术问题。置信度：高（事件本身）。

## 4. 增量数字账

| 动作 | 数字 | 来源 |
| --- | --- | --- |
| 批量困惑度 | batch=64 可在 Kaggle 2×T4 上暴力搜 sample#0 的全部排列；批量与逐行有 cuBLAS 级微小差异 | 548249 |
| 2nd 邻域参数 | (k=3, max_moving=5) 与 (k=4, max_moving=1)；P5 全部候选移动一轮 ~18 分钟（4090） | 560533 |
| 2nd 最好成绩 | P5 **28.5**；P3 **191.x**；四段结构突破 32.xx 壁垒 | 560533 |
| 5th 并行度 | A100 上 batch 104 = 104 条 SA 轨迹同时评分；GPU 利用率 98%；随机起点**半数以上**找到各样例最优 | 560597 |
| 5th 移动规模 | 分段洗牌 k 随机 ≤10；remove-insert 取子序列比随机子集更有效 | 560597 |
| sample 5 压缩 | 字母序（含停用词）**44.0**；100! → 块内排列；块结构 + SA 搬词 | 559339 |
| sample 6 社区分 | 排序 53.46；停用词优先排序 48.69 | 主题索引 550287/550429 |
| 榜单参照 | 社区讨论"如何突破 LB=248.5"；通用教程 256.6；255.9 总论帖 | 主题索引 551818/551902/548476 |
| 赛事 | 1514 队；80 帖；指标经历 "Metric Revision and Rescore"；LB hack 被修复 | 元数据 + 547676/547505 |

**结构校验（2 处吻合 + 1 处口径受限）**

1. 2nd 的"限制移动长度"与其图（图 3）一致：Allowed=小段交换/长段保持，Restricted=长段移动被禁 ✓；
2. sample 5 的"44.0 起点 → 社区最优 28.5"与 2nd 的 28.5 相互印证 ✓；
3. ⚠ 1st 的算法/数字完全未知（仅 repo 链接），本场"最优方法的完整证据链"缺失；5th 的接受准则优势仅有自述，无消融数字。

## 5. 机制推演

**M1｜为什么 TSP 技巧能迁移但必须改造**：k-opt/ILS/SA 的抽象结构是"邻域 + 扰动 + 接受"，与目标函数无关；但 TSP 的三个前提在困惑度下全部失效——(a) 边无向（翻转不变）→ 这里翻转会破坏语序、必须禁止；(b) 增量可局部计算 → 这里移动一个词改变其后全部上下文，只能整体重算；(c) 对称/度量结构 → 这里分数依赖顺序且高度非凸。改造的核心就是"在非局部目标上找回局部性"：限制移动子序列长度、批量化整体评分、缓存重复文本。

**M2｜受限 k-opt 的信息论解释**：移动长段 = 同时改变大量词的上下文，单次评分的信息量虽大但接受率极低（几乎必然变差）；移动短段 = 单位评分的接受概率较高。2nd 的实验设计正是"允许大段静止、只交换小段"，把算力花在高接受率的移动上。P5 18 分钟/轮说明即使如此剪枝，搜索空间仍大——所以还需要 ILS 的 kick 与多起点。

**M3｜kick 为什么要"洗牌相邻子序列"**：普通 double-bridge 在 TSP 里有效是因为它能重构长程路径而不破坏局部；在词序问题里，score 的局部性意味着"相邻词的分离/重聚"才是关键的势垒。随机选 n=5/10 的相邻块洗牌，等于一次性重排一个局部语境，是专门针对该势垒设计的扰动。

**M4｜SA 的并行化优势**：SA 的每次迭代只需"修改 + 评分 + 接受判定"，天然适合把 N 条链打包成一个 batch 送 GPU；Metropolis 或上界准则都是逐元素的。5th 的 multi-point + 交叉（对最优解做 crossover）在保留多样性的同时利用 batch——这是"用 GPU 宽度换搜索深度"。

**M5｜位置折扣的必要性**：因果 LM 的下一 token 损失随上下文增长而变化；序列前部的错误会污染其后所有 token 的损失，因此同等"视觉上"的移动在前部造成的 Δ 更大。搜索若直接比较 Δ，会系统性地偏好尾部移动（前部 Δ 太大、接受率低），导致前部冻结。折扣分数/前缀限制都是把 Δ 标准化到位置可比的尺度。

**M6｜结构压缩的双刃剑**：把解空间限制到"字母块内排列"是巨大的先验红利（44→28 量级），但也把搜索限制在块结构的流形上；突破 32.xx 需要"块间搬词/交换"的定制 kick。**一般规律：结构先验给你起点，打破结构的算子给你上限。**

**M7｜评分函数的"观测误差"会影响爬山**：批量评分的 cuBLAS 差异、float16/8bit 精度、padding/掩码错误都会引入 ~1e-2 级别的分数噪声；局部搜索在噪声尺度内无法区分优劣，可能锁死在伪局部最优。所以"精确复现 + 固定精度 + 可复算"是优化正确性的前提，而非工程细节。

## 6. 证据分级

| 断言 | 等级 | 说明 |
| --- | --- | --- |
| 批量困惑度正确实现（padding/mask/平均） | 作者公开代码 + 官方 metric 差分验证 | 高 |
| 批量 vs 逐行的 cuBLAS 差异 | 多队复现（评论区） | 中高 |
| 2nd 的 28.5/191.x、k-opt 参数、18 分钟 | 自述 + 赛后公开 notebook | 中高 |
| 5th 的 batch 104/98%/半数次找到最优 | 自述 | 中（无公开消融） |
| 位置折扣/前缀限制有效 | 自述（机制清晰） | 中 |
| sample 5 字母序 44.0、块 sharding | 自述（自称未验证测试代码） | 中低（仅为思路，社区质疑） |
| 社区分数链（53.46/48.69/248.5/255.9/256.6） | 主题索引（标题+票数） | 中 |
| 1st 方法 | 仅 repo 链接（未下载） | 低（缺口） |
| 赛事/事件（重打分、hack 修复、公开解争议） | 主题索引 | 高 |

## 7. 边界条件与反事实

- **反事实 1（不做批量评分）**：Chris Deotte 的 batch=64 说明 GPU 一次可评 64 条——单条评估下采样效率降两个数量级；5th 的 104 条并行 SA 直接不可行。
- **反事实 2（不限制 k-opt 候选）**：k-opt 组合随 k 指数增长；P5 全移动一轮从 18 分钟变成不可承受，搜索轮数大幅缩水。
- **反事实 3（无结构先验）**：sample 5 从随机排列出发，多数队伍停在 40+；块结构把起点拉到 44.0 并让 28.5 成为可能；但完全固守块结构则卡在 32.xx。
- **反事实 4（用 Metropolis 而非上界接受）**：5th 判断两者等效；差别在超参（温度调度 vs 上界下调）与计算开销——在长周期搜索里后者的调参负担更低。
- **反事实 5（赛期不公开 sample 5 思路）**：社区分数分布会保留更多差异性；公开后"同分填满 gold zone"的担忧成真概率上升（道德/策略双输）。
- **边界**：全部结论依赖"评分函数可本地复现 + 可批量 + 目标对顺序敏感 + 存在可利用的语言学结构"；非因果 LM 或不可批量评分的黑箱优化不适用。

## 8. 悬案与失败学

**悬案**

1. **1st 方案完全缺失**（仅 repo 链接）：本场最重要的方法论空缺——无法验证"最优解法是否也是 ILS/SA 家族的变体"。
2. **"Metric Revision and Rescore" 细节未收录**：指标改了什么、分数怎么变、是否影响最终名次（547676，27 票，55 评论）。
3. **"Each Optimal(?) Score has been revealed!"**：社区是否真的证明了各 sample 最优？28.5 / 191.x 与最优的差距（556784）。
4. **LB hack 被修复**（547505）的技术细节与影响面。
5. **3rd/4th/10th/11th/13th 方案未收录**：无法构建完整的算法谱系（尤其 3rd 的 30 票、4th 的 32 票）。
6. **sample 6/其他样例的分数链**（53.46→48.69→?）与 sample 5 的最优差距。

**失败学（跨队合集）**

- 2nd：beam search（难以设计非短视的评价函数）；明确不用 SA（温度控制不适合间断计算）与 GA（缺有效交叉）。
- 5th：置换矩阵 + Sinkhorn + KL（能跑但远不如局部搜索）；logits 直接解 ATSP（完全失败）；logits 的 EMA + Sinkhorn（较好但仍不及）；MCTS/RL 训练预测序列（失败）。
- sample 5 团队：自述方案未验证、环境受限，发布时仅为测试代码。
- 社区：批量评分未对齐导致分数错误（548249 之前的大量困惑）；cuBLAS 差异（GPUs 非确定性的经典坑）。

## 9. 图表证据

> 路径相对本文件（`analysis/deep/`）：`../../intel/santa-2024/bodies/<topic>_img/NN.ext`

![Greedy 接受率热力图](../../intel/santa-2024/bodies/548476_img/01.png)

**图 1：Greedy 的接受率面**（topic 548476）——Δ>0 全接受、Δ<0 全拒绝，与温度无关。作为 SA 的对照基线：无逃逸能力。

![SA 接受率热力图](../../intel/santa-2024/bodies/548476_img/02.png)

**图 2：SA 的接受率面**（topic 548476）——Δ<0 时接受率随温度升高、随 |Δ| 减小而上升（Metropolis 形式）。**一图说明"温度控制探索—利用"的机制**。

![受限 k-opt：允许 vs 禁止](../../intel/santa-2024/bodies/560533_img/01.png)

**图 3：k-opt 移动剪枝**（topic 560533）——Allowed：小段交换、长段保持；Restricted：长移动子序列被禁。对应 (k=3,max_moving=5)/(k=4,max_moving=1) 的参数化。

![ATSP double root-and-stem 结构](../../intel/santa-2024/bodies/560597_img/01.png)

**图 4：double root-and-stem 移动**（topic 560597）——(a) bicycle 结构上的试探移动；(b)(c) tricycle 结构（r1/r2 root、t1 stem）。5th 把词序映射成双环+路径图结构后做专门的图移动。**这是"从 ATSP 文献直接借算子"的实证。**

![sample 5 的块 sharding](../../intel/santa-2024/bodies/559339_img/01.png)

**图 5：sample 5 的结构分解**（topic 559339）——"Has Limitation?" → Stopwords / Alphabet Block A / Alphabet Block B，以及 "Just Extend It!" 的分块扩展。**100! → 块内排列的空间压缩示意**。

![sample 5 的块内示例](../../intel/santa-2024/bodies/559339_img/02.png)

**图 6：块结构与块内有序示例**（topic 559339）——Stopwords → Block A（Apple/Apricot/Banana）→ Block B（Blueberry/Cherry…）；块内近似有序、块间由 SA 搬词。**结构性先验的具体形态**。

## 10. 对既有笔记/playbook 的修订点

1. `notes/sim-agent/santa-2024.md` 升级：补 6 篇角色表、5 队 × 8 维对照、数字账（batch 64/104、18 分钟、28.5/191.x/44.0/32.xx 壁垒）、机制 M1–M7、6 张图证与失败清单；修正"1st/3rd 见讨论区"的占位符（1st 正文确认为空）。
2. `playbook/sim-agent.md`（启发式优化节）增补：
   - **黑箱评分三件套**：官方 metric 逐位复现 → 批量化 → 固定精度/可复算（含 padding 方向这种陷阱）；
   - **非局部目标邻域设计**：禁翻转、限制移动子序列长度、长段静止、整体重评 + 分数缓存；
   - **逃逸算子**：随机相邻子序列洗牌 kick；结构专用 kick（块间搬词/交换）；
   - **接受准则**：Metropolis vs 全局上界（阈值调度，减少指数运算与调参）；
   - **位置归一**：前缀限制或按位置平均 logit 折扣，消除尾部偏好；
   - **GPU 并行的 SA 轨迹**（batch=轨迹数，98% 利用率）+ multi-start + 结构先验；
   - **分享时机**：单一答案的启发式赛，赛期公开顶级解 = 把金牌竞争变成复现速度竞赛。
3. `playbook/00-通用方法论.md` 增补：**"评分器对齐先于一切优化"**（与 LLM Prompt Recovery 结论同族）；**"结构先验给你起点、打破结构的算子给你上限"**。
4. `analysis/THEORY.md`（Batch 6 末汇总 v0.6）候选：
   - **L97｜黑箱评分器对齐律**（先精确复现+批量化+固定精度，再谈搜索；反例=批量与逐行 cuBLAS 差异污染爬山；证据 = 548249 + 本场全社区）；
   - **L98｜非局部目标的邻域剪枝律**（限制移动长度/禁翻转/缓存重评；证据 = 2nd 18 分钟一轮、5th 98% 利用率）；
   - **L99｜位置归一化律**（昂贵因果评分下，接受判据需按位置难度归一；证据 = 5th 的前缀/折扣困惑度）；
   - **L100｜结构压缩双刃剑律**（块 sharding 把 44→28 量级，但打破块结构的 kick 才能越过 32.xx 壁垒；证据 = 559339+560533）；
   - **L101｜启发式赛分享时机定律**（单一答案 + 同分并列 = 赛期公开顶级解改变竞争性质；证据 = 559339 争议与 555881）。

## 11. 出处

- 批量困惑度（92 票）：https://www.kaggle.com/competitions/santa-2024/discussion/548249
- 1st（85 票，正文仅 repo 链接）：https://www.kaggle.com/competitions/santa-2024/discussion/560560
- SA 总论 255.9（59 票）：https://www.kaggle.com/competitions/santa-2024/discussion/548476
- 2nd @zaburo（43 票）：https://www.kaggle.com/competitions/santa-2024/discussion/560533
- 5th CPMP（43 票）：https://www.kaggle.com/competitions/santa-2024/discussion/560597
- sample 5 团队解（41 票）：https://www.kaggle.com/competitions/santa-2024/discussion/559339
- 未收录正文的关键讨论（真实 topic id，供后续定点补采/图片层参考）：560540、560565、560620、560536、560531、560542、551818、556784、551902、555881、547676、547505、557817、555545、550287、550429
