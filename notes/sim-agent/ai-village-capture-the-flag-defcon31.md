# AI Village Capture the Flag @ DEF CON 31

> 主题：sim-agent ｜ 子类：agent-game / 安全 ｜ 领域：AI 安全 ｜ 类别：Featured
> 截止：2023-11-09 ｜ 队伍数：1344 ｜ 机制：标准赛 ｜ 指标：Flag 得分（多关卡，按解出数计）
> 数据来源：`intel/ai-village-capture-the-flag-defcon31/`（80 条主题索引 + 6 篇 write-up 正文）

## 1. 任务与数据

- **任务形式**：AI/ML 主题的夺旗赛（CTF）——每关是一道针对机器学习系统的攻击/逆向题目（模型逆向、数据探测、对抗样本等），解出即得 flag。
- **数据形态**：每关给出独立的数据/接口；**评分是离散的 flag 计数**。
- **构造陷阱**：题目是"对抗性"的，需要主动探测模型/接口行为；部分关卡依赖排行榜反馈（可迭代逼近）。

## 2. 方案特征

| 方案 | 名次 | 关键点 |
| --- | --- | --- |
| 25 个 flag 的高层总结 | 高票 | 承认 **ChatGPT 是极有价值的助手**（讨论思路、翻译密文、写代码）；多数关卡在比赛初期集中解决 |
| 24 分方案 | 6th | 例：把数据跑过模型筛出被预测为 ">50K" 的条目，发现 "Tech-support" 职业过度代表，再**用爬山法对着 ID 列表迭代**直到分数足够拿 flag |
| "Aha moments" 复盘 | 11th | 记录关键突破点 |
| 参考资料帖 | 社区 | 汇总 AI 安全相关的公开资料 |

## 3. 关键技巧

- **把排行榜当作可探测的 oracle**：用爬山/迭代逼近答案（6th 的典型做法）。
- **观察模型的"过度代表"现象**（某类别异常集中）→ 是定位答案的强线索。
- **LLM 作为助手**：翻译、解释密文、生成脚本（本场高票方案明确致谢 ChatGPT）。
- **领域资料先行**：AI 安全（模型逆向、成员推断、对抗攻击）的公开资料是解题地图。

## 4. 可迁移性评估

- **可直接迁移**：
  - **"用排行榜反馈做迭代搜索"**（在黑箱评分场景通用，与 Santa 2024、AI Agent Security 一致）。
  - 观察分布异常（过度代表/缺失）来定位隐藏结构。
  - 把 LLM 当编程与思路助手。
- 需要前提：AI 安全基础知识（攻击/逆向方向）。
- 不建议照搬：无。

## 5. 对新手的关键启示

1. **CTF 类比赛比的是"探测与推理"，不是训练模型**——先改变心智模型。
2. **排行榜反馈可以被主动利用**（前提是规则允许）。
3. **AI 安全是一个独立且实用的技能方向**，值得单独学习。

## 6. 出处

- 讨论区索引：`intel/ai-village-capture-the-flag-defcon31/topics.md`（80 条）
- 已收录 write-up（6 篇）：
  - 25 flags 总结（49 票）：https://www.kaggle.com/competitions/ai-village-capture-the-flag-defcon31/discussion/454403
  - 9th（43 票）：https://www.kaggle.com/competitions/ai-village-capture-the-flag-defcon31/discussion/454364
  - 另一份 25 flags（37 票）：https://www.kaggle.com/competitions/ai-village-capture-the-flag-defcon31/discussion/454545
  - 11th "Aha moments"（22 票）：https://www.kaggle.com/competitions/ai-village-capture-the-flag-defcon31/discussion/454579
  - 参考资料（46 票）：https://www.kaggle.com/competitions/ai-village-capture-the-flag-defcon31/discussion/446004
