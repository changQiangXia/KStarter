# NeurIPS 2024 - Lux AI Season 3

> `lux-ai-season-3` ｜ Featured ｜ 指标 Lux AI Season 3 ｜ 701 队 ｜ 截止 2025-03-24

本页汇总该场 **1 条 ≥50 票 GM 主题帖**、**5 条断言**、**0 条高票评论**。

## GM 主题帖

| 票 | 选手 | 日期 | 主题 |
| --- | --- | --- | --- |
| 53 | [@pressman1](https://www.kaggle.com/pressman1) | 2025-03-17 | [Frog Parade's Solution](https://www.kaggle.com/competitions/lux-ai-season-3/discussion/568621) |

## 断言（条件→动作→机制→结果）

| 选手 | 等级 | 阶段 | 动作（节选） | 出处 |
| --- | --- | --- | --- | --- |
| @pressman1 | A | 工程/流程 | 用 Rust 重写规则引擎与全部特征工程；用严格 TDD：小组件单测 + 与真实引擎跨 seed 的集成测试；规则中途大改时测试能及时报警，作者称几乎不花时间 debug 模拟器， | [lux-ai-season-3#568621-01](https://www.kaggle.com/competitions/lux-ai-season-3/discussion/568621) |
| @pressman1 | A | 特征与数据工程 | 特征按 global/spatial × temporal/nontemporal 四类；temporal 保留最近 10 帧；约 80 global + 100 spatial； | [lux-ai-season-3#568621-02](https://www.kaggle.com/competitions/lux-ai-season-3/discussion/568621) |
| @pressman1 | A | 建模与训练 | 残差 CNN + squeeze-excitation（也试过 RoPE ViT 但训练不稳）；spatial 输入 10 帧堆叠 + nontemporal 经 2 层 CNN  | [lux-ai-season-3#568621-04](https://www.kaggle.com/competitions/lux-ai-season-3/discussion/568621) |
| @pressman1 | A | 工程/流程 | PPO + clipping + 非法动作掩码 + 熵与 teacher-KL 项；GAE-Lambda、gamma 0.9999 到 1.0；求和各单位的联合 log-prob； | [lux-ai-season-3#568621-05](https://www.kaggle.com/competitions/lux-ai-season-3/discussion/568621) |
| @pressman1 | B | 建模与训练 | 禁止出界、撞小行星、能量不足的动作；还禁止对非已知点位及邻格的盲 sap；作者事后认为该限制可能错误（对手 Flat Neurons 善用盲 sap），下次只禁必然无意义的动作 | [lux-ai-season-3#568621-03](https://www.kaggle.com/competitions/lux-ai-season-3/discussion/568621) |

## 高票评论

_无 ≥10 票评论_

## 关联资产

- 深读：`analysis/deep/lux-ai-season-3.md`
- 结构化摘要：`notes/sim-agent/lux-ai-season-3.md`
- 归档讨论区：`intel/lux-ai-season-3/`（主题 1 条有 ≥50 票帖，图证 1 个）
