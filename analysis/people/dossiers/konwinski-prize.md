# Konwinski Prize

> `konwinski-prize` ｜ Featured ｜ 指标 K Prize Metric ｜ 617 队 ｜ 截止 2025-07-23

本页汇总该场 **1 条 ≥50 票 GM 主题帖**、**5 条断言**、**0 条高票评论**。

## GM 主题帖

| 票 | 选手 | 日期 | 主题 |
| --- | --- | --- | --- |
| 75 | [@arc144](https://www.kaggle.com/arc144) | 2025-03-18 | [1st Place Solution Write Up](https://www.kaggle.com/competitions/konwinski-prize/discussion/568884) |

## 断言（条件→动作→机制→结果）

| 选手 | 等级 | 阶段 | 动作（节选） | 出处 |
| --- | --- | --- | --- | --- |
| @arc144 | A | 特征与数据工程 | 两阶段检索：先让模型找相关单测文件，再给这些文件的函数/类骨架，让它挑要看的类/函数/方法；同时提取 imports；5 个候选中 1 个给全 context、1 个只给 impo | [konwinski-prize#568884-02](https://www.kaggle.com/competitions/konwinski-prize/discussion/568884) |
| @arc144 | A | 验证设计 | 5 个 F2P 候选只保留能复现 issue 且无其他问题的；全失败则高温度再生成 5 个；8 个修复候选（4 定位 × 2 采样）先 git apply dry-run，再用 F | [konwinski-prize#568884-03](https://www.kaggle.com/competitions/konwinski-prize/discussion/568884) |
| @arc144 | A | 工程/流程 | repo 结构只生成一次（原 Agentless 每步重新生成，每次 5 到 20 秒）；全局超过 20 小时跳过剩余样本、单样本超过 12 分钟跳过；最佳提交 5 到 7 小时（ | [konwinski-prize#568884-04](https://www.kaggle.com/competitions/konwinski-prize/discussion/568884) |
| @arc144 | A | 复盘与流程 | 赛后披露 private 结果 9 对、2 错、109 跳过；作者认为即使前沿模型也离 90% 很远（错误惩罚重）；本地验证花一周只跑通少量 Django 样本，最终放弃改作调试用 | [konwinski-prize#568884-05](https://www.kaggle.com/competitions/konwinski-prize/discussion/568884) |
| @arc144 | B | 建模与训练 | 关键点：为生成 F2P 测试改 context 检索；F2P 与 P2P 双重 patch 拒绝；用 Qwen2.5-Coder-32B；用 search/replace diff | [konwinski-prize#568884-01](https://www.kaggle.com/competitions/konwinski-prize/discussion/568884) |

## 高票评论

_无 ≥10 票评论_

## 关联资产

- 深读：`analysis/deep/konwinski-prize.md`
- 结构化摘要：`notes/nlp/konwinski-prize.md`
- 归档讨论区：`intel/konwinski-prize/`（主题 1 条有 ≥50 票帖，图证 1 个）
