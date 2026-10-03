# Playground Series S6E4 - 灌溉需求预测

> 主题：tabular ｜ 子类：— ｜ 领域：农业（合成数据） ｜ 类别：Playground
> 截止：2026-04-30 ｜ 队伍数：4315 ｜ 机制：标准赛 ｜ 指标：Balanced Accuracy
> 数据来源：`intel/playground-series-s6e4/`（55 条主题索引 + 6 篇 write-up 正文）

## 1. 任务与数据

- 预测目标：三分类灌溉需求（Low / Medium / High），指标为 Balanced Accuracy。
- 数据特性：High 类仅约 3.3%，但三类在指标中等权 → 分数对 High 的预测极其敏感，出现大量"彩票式"名次波动；原数据约 1 万行且被社区**逆向了完全分离的生成公式**（规则版：土壤湿度<25、降雨<300 等四因子打分决定类别，原数据上 Balanced Accuracy=1）。
- 关键观察（1st 所引）：模型几乎从不混淆 Low 与 High 两类 → 允许 One-vs-Rest 分解。

## 2. 验证方案

- 主流 5 折固定 OOF；本场 CV–Private LB 相关性弱（2nd：CV 0.98175 的多个提交私榜 0.98130–0.98170）+ 领奖台拥挤 → 用"多提交对冲 + 阈值搜索"代替单一选择。
- Balanced Accuracy 需要显式阈值/类权重处理：1st 用两个贪心阈值搜索；2nd 用带类权重的多项逻辑回归。
- 自造公式可直接当验证工具：规则公式在原始数据上完全分离，是分布理解的"金标准"。

## 3. 模型家族

| 方案 | 使用者层次 | 关键点 | 出处 |
| --- | --- | --- | --- |
| 两个二分类器 OVR（Low vs Rest、Medium vs High）+ logits LR 融合 | 1st | 概率换算闭式；61 个 OOF；贪心阈值搜索 | topic 696040 |
| Claude/Codex 迁移 150+ 脚本 + GPU 多项 LogReg 堆叠 | 2nd | 模型迁移自动化；PyTorch 实现加权多项 LR | topic 696169 |
| 200+ 模型误差多样性堆叠（LightGBM 元模型） | 高分帖 | 203 模型谱系；单堆叠器 > 双堆叠混合 | topic 696104 |
| 166 OOF + 神经元模型 | 24th | 重堆叠路线 | topic 696016 |
| 多层集成器（11 L1 + 4 L2，含投票/差分进化/爬山） | 4th | "集成器比模型多"；彩票敏感性 | topic 696054 |

## 4. 关键技巧

- **OVR 分解**：利用"Low vs High 从不混淆"的结构，两个二分类器相乘得三类概率；P(Medium)=(1−P1)(1−P2)、P(High)=(1−P1)P2——比直接多分类更稳。
- **堆叠器选择**：logits 变换 + 逻辑回归（带类权重）在 Balanced Accuracy 下优于普通 Ridge；GPU 版多项 LogReg = 去掉隐层的 NN，用 weight_decay 模拟 L2（2nd）。
- **LLM 工程化**：2nd 用 Claude Code 第一天批量迁移上月（churn）比赛的全部脚本 → 第 3 天即私榜第一；Codex 再迁一版做双保险——"跨届代码资产 + LLM 迁移"成为新范式。
- **彩票防御**：High 类敏感 → 多份互补提交、L2 平均、不盲信单次 CV 提升（4th 的复盘：未选提交里有多份更优）。
- 原数据公式 = 规则基线：任何模型都应先对照规则公式的表现，理解"还剩多少噪声"。

## 5. 可迁移性评估

- **可直接迁移**：OVR 分解（当个别类间从不混淆时）；带类权重的 logits 逻辑回归堆叠；阈值搜索适配 Balanced Accuracy；LLM 批量迁移往届代码。
- **需要前提**：类别不均衡 + 指标均衡敏感的赛制；能拿到原始数据的合成赛；GPU 与大量 OOF 的算力。
- **不建议照搬**：在 CV–LB 弱相关时用单一 CV 峰值定稿；对稀缺类敏感场景押注单提交。

## 6. 对新手的关键启示

- 先问"哪些类之间会混淆"：混淆结构直接决定该用 OVR、分层模型还是直接多分类。
- 均衡指标（Balanced Accuracy/QWK）必须配阈值搜索或类权重，默认 argmax 会吃亏。
- 若能拿到原数据，先逆向/拟合它的生成规则——既是特征工程金矿，也是理解噪声上限的标尺。
- 本届最醒目的信号：**LLM Agent 把往届方案迁移到新赛的速度已成为竞争力本身**。

## 7. 出处

- 1st：OVR + 多分类模型的概率分解：https://www.kaggle.com/competitions/playground-series-s6e4/discussion/696040
- 2nd：Claude Code/Codex 迁移 + GPU 逻辑回归堆叠：https://www.kaggle.com/competitions/playground-series-s6e4/discussion/696169
- 4th：集成器比模型多：https://www.kaggle.com/competitions/playground-series-s6e4/discussion/696054
- 误差多样性：200 模型堆叠：https://www.kaggle.com/competitions/playground-series-s6e4/discussion/696104
- 24th：166 OOF 重堆叠：https://www.kaggle.com/competitions/playground-series-s6e4/discussion/696016
- 原数据精确公式：https://www.kaggle.com/competitions/playground-series-s6e4/discussion/687460
