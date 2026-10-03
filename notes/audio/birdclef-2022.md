# BirdCLEF 2022（精简）

> 主题：audio ｜ 子类：— ｜ 领域：生物声学 ｜ 类别：Research ｜ 截止：2022-05-24 ｜ 队伍数：801 ｜ 指标：物种识别
> 出处：`intel/birdclef-2022/`（80 条主题索引 + 6 篇 write-up 正文）

## 任务

由野外录音识别鸟种（多标签、弱标签、长尾），该系列的早期届次（数据规模较后续小）。

## 关键要点

- 3rd 由两人团队完成，强调"双方贡献想法的协作"。
- 方法沿用系列主线：**频谱图 + 切窗 + 多实例 + 伪标签**（2022 起步 → 2023 数据为王 → 2024 常规化 → 2025 多轮 Noisy Student → 2026 Noisy Student + 蒸馏）。
- 该系列的主办方为康奈尔鸟类学实验室（Cornell Lab of Ornithology），数据与评估逐年改进（2026 届首次引入独立验证集）。

## 可迁移要点

- 弱标签音频的通用配方在本系列五年中保持一致：**切窗 → 多实例 → 伪标签 → 多轮迭代**。
- 早期届次的价值在于"看方法如何起步"。

## 出处

- 讨论区索引：`intel/birdclef-2022/topics.md`
- 1st（63 票）：https://www.kaggle.com/competitions/birdclef-2022/discussion/327047
- 3rd（56 票）：https://www.kaggle.com/competitions/birdclef-2022/discussion/327193
- 7th（45 票）：https://www.kaggle.com/competitions/birdclef-2022/discussion/326973
