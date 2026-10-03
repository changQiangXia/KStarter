# Lux AI Season 2

> `lux-ai-season-2` ｜ Featured ｜ 指标 lux_ai_s2 ｜ 646 队 ｜ 截止 2023-05-08

本页汇总该场 **1 条 ≥50 票 GM 主题帖**、**6 条断言**、**0 条高票评论**。

## GM 主题帖

| 票 | 选手 | 日期 | 主题 |
| --- | --- | --- | --- |
| 51 | [@ferdinandlimburg](https://www.kaggle.com/ferdinandlimburg) | 2023-05-03 | [FLG's Approach - Deep Reinforcement Learning with a Focus on Performan](https://www.kaggle.com/competitions/lux-ai-season-2/discussion/406702) |

## 断言（条件→动作→机制→结果）

| 选手 | 等级 | 阶段 | 动作（节选） | 出处 |
| --- | --- | --- | --- | --- |
| @ferdinandlimburg | A | 建模与训练 | 动作空间分 7 类 actor：bid 10 档、spawn 位置 48×48、water/metal 各 7 档、工厂 Grid(4)、轻/重单位 Grid(23)；观测 54  | [lux-ai-season-2#406702-01](https://www.kaggle.com/competitions/lux-ai-season-2/discussion/406702) |
| @ferdinandlimburg | A | 建模与训练 | 早期 RL 随机探索导致大量自碰撞，agent 学会避免相邻作业与少造单位 → 直接取消所有会导致自碰撞的移动（改为 noop） | [lux-ai-season-2#406702-02](https://www.kaggle.com/competitions/lux-ai-season-2/discussion/406702) |
| @ferdinandlimburg | A | 工程/流程 | 推理用前向预测填队列（同时预测自己与对手再步进环境）；训练不建队列，但用期望通信成本：以 p=0.2 随机施加通信代价，模拟平均约 5 步队列；实测至少需 4-6 步预测，单步严重 | [lux-ai-season-2#406702-03](https://www.kaggle.com/competitions/lux-ai-season-2/discussion/406702) |
| @ferdinandlimburg | A | 建模与训练 | 用约 2000 场顶级 agent 对局（MetaKaggle）做模仿学习数据集（约 300GB HDF5，快速随机访问），以单位动作准确率评估架构；最佳为 DoubleCone( | [lux-ai-season-2#406702-04](https://www.kaggle.com/competitions/lux-ai-season-2/discussion/406702) |
| @ferdinandlimburg | A | 工程/流程 | ONNX runtime/OpenVino 打包失败（错误日志 404），被迫取消正在训练的 DoubleCone(6,8,6)；静态/动态量化、压缩、jit 都因 setup 时 | [lux-ai-season-2#406702-05](https://www.kaggle.com/competitions/lux-ai-season-2/discussion/406702) |
| @ferdinandlimburg | A | 建模与训练 | 两阶段奖励：先约 65M 步 shaped 资源奖励（自私、非零和），后转零和（游戏结果 ±1、终局地衣优势、工厂 ±0.3、单位优势 ±0.8、地衣发电 ±0.1），且只在变化时 | [lux-ai-season-2#406702-06](https://www.kaggle.com/competitions/lux-ai-season-2/discussion/406702) |

## 高票评论

_无 ≥10 票评论_

## 关联资产

- 深读：`analysis/deep/lux-ai-season-2.md`
- 结构化摘要：`notes/sim-agent/lux-ai-season-2.md`
- 归档讨论区：`intel/lux-ai-season-2/`（主题 1 条有 ≥50 票帖，图证 7 个）
