# Google Code Golf Championship 2025

> 主题：sim-agent（优化/代码压缩）｜ 子类：— ｜ 领域：编程竞赛 ｜ 类别：Research
> 截止：2025-10-30 ｜ 队伍数：1142 ｜ 机制：标准赛 ｜ 指标：代码字节数（越少越好，且须通过测试）
> 数据来源：`intel/google-code-golf-2025/`（80 条主题索引 + 6 篇 write-up 正文）

## 1. 任务与数据

- 任务形式：给定编程题，用**最短的代码**通过全部测试（code golf），按字节计分。
- 数据形态：题目 + 测试用例；无训练数据。
- 构造陷阱：
  - 既要正确又要极短（**双约束优化**）；
  - 语言特性、内建库、编码技巧都能压字节；
- 参赛者多为竞赛编程/CTF 背景（5th 指出"许多队伍也是 Kaggle 新手"）。

## 2. 方案谱系

| 方案 | 名次 | 关键点 |
| --- | --- | --- |
| 更好的压缩算法 | 5th | 团队背景是竞赛编程与 CTF；核心贡献在**压缩/编码策略**而非模型 |
| 其他方案 | 见讨论区 | |

## 3. 关键技巧

- **压缩与编码技巧**（把程序文本本身压缩后再解压执行）。
- **利用语言内建特性**（隐式转换、位运算、库函数）。
- **自动化搜索**（对短代码变体做批量验证，与 NeuroGolf 的 agent 流水线同源）。

## 4. 可迁移性评估

- **可直接迁移**：
  - **压缩 + 解压执行**的思路（在模型压缩、序列化、prompt 压缩中也有用）；
  - 自动化代码搜索与验证回路；
  - 双约束（正确性 + 长度）下的工程取舍。
- 需要前提：编程语言熟练度与测试自动化。
- 不建议照搬：只做手工缩短（规模上不去）。

## 5. 对新手的关键启示

1. **code golf 是"提示词/代码压缩"能力的极端形式**，与 NeuroGolf（ONNX 模型高尔夫）同源。
2. **这类比赛对 Kaggle 新人也友好**（5th 指出许多队伍都是首次参加 Kaggle）——**技能可跨平台迁移**。
3. 自动化验证回路是任何"生成-筛选"任务的必要条件。

## 6. 轻读结论（2026-10 补）

**一句话**：短代码竞赛的两条主线——**agent 流水线（并行采样 + 机械验证 + 最短选择）** 与 **压缩/编码套利（自研 >Zopfli 的压缩器 + 语言特性）**；两者叠加才是顶区解法。

- 4th（614124）：98% LLM 生成；每轮 N=4 并行 → 验证 → 取最短；**AST 规则化提示**（无 regex 提示用 `re`、循环提示改递归、`def` 提示改 `lambda`）；空沙箱重启逃离局部最优；最后两周让 LLM 优化"压缩友好代码"（+钻石级 Task 324）；用 Codex Cloud（15 会话并行）。
- 5th（614225）：自研压缩器比 Zopfli 强（相对 zlib +700 分）；`#coding:L1` latin-1 载荷 + `zlib.decompress(...,-15)`；deflate/Huffman RLE 认知直接指导写法（少大写、tab、单引号）；task111 62B / task270 115B。
- 8th（615039）：全手工；递归模板 `-i*g or p(...,i-1)`、`pop()` 变异遍历、`a*0==0` 类型判别、4 层循环位运算压成 1 层。
- 交叉引用：NeuroGolf 2026 的 9th 调度器灵感来自本场 4th（`analysis/deep/neurogolf-2026.md`）。

**裁决**：LLM 负责吞吐、人类负责"改变搜索空间"；计分含代码体积时压缩器是独立赛道；这类赛制的漏洞披露与共享规则需要社区治理。

**悬案**：**1st/2nd 方案未入库**（本场最高名次细节缺失）；seed cracking 机制未展开。

## 7. 图表证据

![4th 的并行采样与规则化提示循环](../../intel/google-code-golf-2025/bodies/614124_img/01.png)

**图 1**（topic 614124）：每轮 4 份并行生成 → 取最短有效（71B）→ AST 规则化跟进提示 → 下一轮的闭环。

## 8. 出处

- 讨论区索引：`intel/google-code-golf-2025/topics.md`（80 条）
- 已收录 write-up（6 篇）：
  - 并行采样 + 规则化提示生成（52 票）：https://www.kaggle.com/competitions/google-code-golf-2025/discussion/614124
  - 5th 压缩算法（27 票）：https://www.kaggle.com/competitions/google-code-golf-2025/discussion/614225
  - 8th 技巧（36 票）：https://www.kaggle.com/competitions/google-code-golf-2025/discussion/615039
  - 解决方案链接（41 票）：https://www.kaggle.com/competitions/google-code-golf-2025/discussion/613968
  - 单题分数共享（44 票）：https://www.kaggle.com/competitions/google-code-golf-2025/discussion/596679
- 跨项对照：`analysis/deep/neurogolf-2026.md`（9th 的调度器即源自本场 4th 的流水线）
- 轻读全本：`analysis/deep/google-code-golf-2025.md`（Tier B 轻读：对照矩阵/裁决/证据分级/悬案 + 1 图证）
