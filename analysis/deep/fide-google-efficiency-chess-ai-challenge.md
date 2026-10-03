# FIDE & Google Efficient Chess AI Challenge 轻量深读（Tier B）

> 赛事：Featured ｜ 主题 sim-agent（国际象棋引擎，代码赛）｜ 1120 队 ｜ 约束：单核、**二进制 ≤64 KiB**、**内存 ≤5 MiB** ｜ 指标：对局胜率/排行榜（Chess）
> 材料基础：`digests/fide-google-efficiency-chess-ai-challenge.md`（6 篇正文：1st 571023 / 4th 563173 / 9th 567106 / Niboshi 563866 / GitHub 汇总 562764 / Tiny Chess Bot 548062；80 条主题索引）+ 5 张归档图
> 轻读时间：2026-10（Tier B B14）

## 1. 一句话重述与数字账

在 **64 KiB 二进制 + 5 MiB 内存 + 单核**的嵌入式式约束下造一个国际象棋引擎。本场的结论是**"数据与压缩工程 > 搜索花活"**：1st 把 NNUE 压到约 20kb（tiny 网络），靠 Leela T77/T79 数据 + 两阶段训练 + 数据过滤（piece-count 平坦化、跳前 28 步、弃子局面）与"16-bit 权重无损压到 8-bit"的技巧夺冠；4th 用 Stockfish 16 的 HCE + 2,489 参数的小 MLP 拿第 4；9th 纯 HCE + SPSA 调参也进前十。

| 关键数字 | 值 | 来源 |
| --- | --- | --- |
| 1st（571023，"minifish"） | Cfish 底座；768 输入、双视角、水平镜像国王、单隐藏层 NNUE；**两阶段训练**：①100 superbatches（100 亿局面、Stockfish 数据、5k 节点搜索分数）②120 superbatches（120 亿局面、lc0 T77/T79 数据、Q+WDL）；数据过滤：piece-count 分布平坦化（随机跳过）、跳前 28 步、保留"弃子是最好着法"的局面、WDL 与分数不匹配时跳过；**压缩**：16-bit 权重中 98% 落在 8-bit 范围（QA=101/QB=160），按棋子类型分组后多数组≤256 个唯一值 → 用未使用的 8-bit 码映射回 16-bit 权重；权重转置提高压缩率；7z 压缩 + 运行时解压 + zopfli 外层 tar.gz；最终网络 ~20kb，显著强于 HCE；因 RAM 限制是"渐变墙"用了 896kb 哈希（冒险） | 571023 |
| 4th（563173） | Stockfish 16（最后的 HCE 版本）+ 小 MLP（非 NNUE）：内存拆分 = pawn hash 640KiB、continuation history 512KiB、TT 1MiB、去掉大页、用 Classical bitboard 替魔术位板、重写以去掉 libstdc++ 依赖；NN = 99 输入 → 14 个 16-bit 值（256-bit 寄存器）→ ClippedReLU → 32×32 → 32×1，共 **2,489 参数**；用 kaggle-environments 跑 7 万局自对弈采样训练（目标 = NNUE 评估 − HCE 评估）；**加半个 NN 输出** +30 Elo（全量 <10）；最终同时提交 HCE-only 与 NN 增强两份 | 563173 |
| 9th（567106） | Cfish + 纯 HCE：内存压到 ~4MB（删 NNUE、1MB TT、Counter Move History 合并索引等）；`-O3` + strip + **upx --lzma** 保持 <64KB；把 Cfish 搜索参数移植到 Stockfish 16 的 HCE 版本（+30 Elo）；自写 ~400 行 SPSA（cutechess-cli、2000 开局书、10s）再 +30 Elo；因排行榜噪声大，**提交两份相同二进制** | 567106 |
| Niboshi（563866） | NNUE 但用 CNN 特征变换器（12→13 通道 15×15 + 共享权重的 96 输入 dense）；TT 512KiB、continuation history 128KiB；自述计算代价太重（等效 L1=896），是最大失误 | 563866 |
| 工具与生态 | 前 8 名 GitHub 仓库汇总（Approvers / KaggleFish / minifish / Noggenfogger / nagiss / Niboshi / SSE / Cfish_kaggle）；Tiny Chess Bot 挑战与讲解视频（46 票） | 562764 / 548062 |
| 社区与治理 | "Increment is superior to Simple Delay"（35 票）；"必须改 ELO 计分"（34 票 / 14 评论）；"连 numpy 都 import 不了"（28 票 / 49 评论）；"Kaggle 悄悄改了环境？"（25 票 / 22 评论）；64KiB 限制未在 notebook 提交时强制（22 票）；开源引擎移植记录（25 票 / 49 评论） | 索引 |

## 2. 逐方案对照矩阵

| 维度 | 1st | 4th | 9th | Niboshi |
| --- | --- | --- | --- | --- |
| 底座 | Cfish | Stockfish 16（HCE） | Cfish（HCE） | Cfish/Stockfish |
| 评估 | **NNUE（~20kb）** | HCE + 2,489 参数 MLP | HCE + SPSA 参数 | NNUE（CNN 特征变换器） |
| 数据 | lc0 T77/T79 + 两阶段 + 过滤 | 7 万局自对弈采样 | 2000 开局书（SPSA） | lc0 + Stockfish 混合 |
| 压缩 | 8-bit 码表映射 + 转置 + 7z | 去 libstdc++、Classical bitboard | upx --lzma、-O3 | 删未用特性 |
| 结果 | 1st | 4th | 9th（双份相同提交） | 前列 |

## 3. 共识、分歧与裁决

### 共识一：NNUE 是最大杠杆，但非唯一路径（1st、Niboshi vs 4th、9th；置信度中高）

1st 明确"~20kb 的网络比几十年人类评估知识更快更强"；Niboshi/Approvers 也押 NNUE。但 4th（HCE+小 MLP +30 Elo）与 9th（纯 HCE+SPSA +30 Elo）同样进前列。**裁决**：NNUE 上限更高，但 HCE 路线在工程优化到位时仍有奖牌竞争力。置信度：中高。

### 共识二：数据选择/过滤比网络架构更重要（1st、4th；置信度中高）

1st 的增益主要来自 lc0 小网络数据、两阶段课程与过滤策略；4th 用 7 万局自对弈 + "只用半个 NN 输出"的调参发现 +30 Elo。**裁决**：小模型场景下先优化数据分布与目标定义。置信度：中高。

### 共识三：压缩/内存工程是硬门槛（1st、4th、9th、Niboshi；置信度中高）

删模块、替数据结构、避免 libstdc++、选压缩器（7z/upx）、8-bit 码表映射、TT 大小权衡——每一条都直接决定是否达标。**裁决**：这类"嵌入式约束"比赛，系统工程量与算法同等重要。置信度：中高。

### 事件一：环境与规则变化带来运气成分（1st、556777、548945、550339；置信度中高）

官方在截止后调整环境使全体错误损失上升（1st 的 896kb 哈希冒险被"运气"救回）；simple delay 的随机性与 increment 的未落地引发争论；ELO 计分方式被质疑。**裁决**：约束型比赛要留安全边际，规则/环境变化是主要外生风险。置信度：中高。

### 事件二：开源与社区工具是公共底座（562764、548062、553936；置信度中高）

前 8 名全部开源仓库；Tiny Chess Bot 挑战与视频、移植记录帖降低了入门门槛。**裁决**：先复现社区引擎骨架，再攻自己的差异化（NNUE/压缩/调参）。置信度：中高。

## 4. 证据分级

| 断言 | 等级 | 说明 |
| --- | --- | --- |
| 1st 的 NNUE 训练/压缩全流程 | 自述（极详细）+ 权重可视化 | 高 |
| 4th 的内存拆分与 MLP 细节 | 自述 + 全部 notebook 链接 | 高 |
| 9th 的 SPSA 与压缩命令 | 自述 + 开源代码 | 中高 |
| Niboshi 的 CNN 特征变换器 | 自述 | 中 |
| 环境变化/规则争议 | 多帖（高评论） | 中高 |

## 5. 悬案与缺口（登记）

- 2nd/3rd、5th–8th 方案未收录（仅 GitHub 链接）；
- ELO 计分争议的最终处理未跟进；
- 64KiB 未强制执行的 bug 影响范围未知；
- **图证缺口**：无（5 张图，本深读内嵌 2 张）。

## 6. 图表证据

![NNUE 特征变换器权重](../../intel/fide-google-efficiency-chess-ai-challenge/bodies/571023_img/02.png)

**图 1**（topic 571023，1st）：特征变换器权重按棋子类型与视角分组（左=我方、右=对方；每行依次为兵/马/象/车/后/王）——可以看到国王水平镜像带来的零条纹，以及量化后的结构。

![16-bit 权重的直方图](../../intel/fide-google-efficiency-chess-ai-challenge/bodies/571023_img/04.png)

**图 2**（topic 571023，1st）：49,152 个 16-bit 特征权重中只有 288 个唯一值、绝大多数落在 ±50 内——这是"8-bit 码表无损映射"压缩策略的依据。

## 7. 出处

- 1st Cfish + NNUE + 数据（22 票）：https://www.kaggle.com/competitions/fide-google-efficiency-chess-ai-challenge/discussion/571023
- 4th HCE + 小 MLP（39 票 / 5 评论）：https://www.kaggle.com/competitions/fide-google-efficiency-chess-ai-challenge/discussion/563173
- 9th Cfish + SPSA（18 票）：https://www.kaggle.com/competitions/fide-google-efficiency-chess-ai-challenge/discussion/567106
- Niboshi 方案（21 票 / 2 评论）：https://www.kaggle.com/competitions/fide-google-efficiency-chess-ai-challenge/discussion/563866
- 前 8 名 GitHub 汇总（24 票 / 17 评论）：https://www.kaggle.com/competitions/fide-google-efficiency-chess-ai-challenge/discussion/562764
- Tiny Chess Bot 挑战（46 票 / 12 评论）：https://www.kaggle.com/competitions/fide-google-efficiency-chess-ai-challenge/discussion/548062
- Increment vs Simple Delay（35 票）：https://www.kaggle.com/competitions/fide-google-efficiency-chess-ai-challenge/discussion/548945
- ELO 计分质疑（34 票 / 14 评论）：https://www.kaggle.com/competitions/fide-google-efficiency-chess-ai-challenge/discussion/550339
- 环境变更质疑（25 票 / 22 评论）：https://www.kaggle.com/competitions/fide-google-efficiency-chess-ai-challenge/discussion/556777
- 64KiB 未强制 bug（22 票）：https://www.kaggle.com/competitions/fide-google-efficiency-chess-ai-challenge/discussion/558075
