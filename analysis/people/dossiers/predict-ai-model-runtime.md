# Google - Fast or Slow? Predict AI Model Runtime

> `predict-ai-model-runtime` ｜ Research ｜ 指标 58266_TpuGraphsEval ｜ 616 队 ｜ 截止 2023-11-17

本页汇总该场 **1 条 ≥50 票 GM 主题帖**、**5 条断言**、**0 条高票评论**。

## GM 主题帖

| 票 | 选手 | 日期 | 主题 |
| --- | --- | --- | --- |
| 68 | [@arc144](https://www.kaggle.com/arc144) | 2023-11-19 | [1st Place Solution for the Google - Fast or Slow? Predict AI Model Run](https://www.kaggle.com/competitions/predict-ai-model-runtime/discussion/456343) |

## 断言（条件→动作→机制→结果）

| 选手 | 等级 | 阶段 | 动作（节选） | 出处 |
| --- | --- | --- | --- | --- |
| @arc144 | A | 特征与数据工程 | 每图只保留可配置节点（Conv、Dot、Reshape）及其输入输出邻居，把大图拆成多个可能不连通的子图，最后靠全局图池化融合；vRAM 减 4 倍、训练最多快 5 倍 | [predict-ai-model-runtime#456343-01](https://www.kaggle.com/competitions/predict-ai-model-runtime/discussion/456343) |
| @arc144 | A | 特征与数据工程 | 删除 layout 全部重复配置；node_config_feat 每个 6 维向量只有 7 种取值（-1 到 5），用 base-7 整数压缩、dataloader 即时解压，使 | [predict-ai-model-runtime#456343-02](https://www.kaggle.com/competitions/predict-ai-model-runtime/discussion/456343) |
| @arc144 | A | 特征与数据工程 | 重新生成 node_feat 使 padding 为 -1，从而与 node_config_feat 共用一个 4 通道 embedding；node_feat[:134] 用 S | [predict-ai-model-runtime#456343-03](https://www.kaggle.com/competitions/predict-ai-model-runtime/discussion/456343) |
| @arc144 | A | 建模与训练 | 架构：Linear 到 256 维 + 2 个图卷积块（InstanceNorm、SAGEConv、SelfChannelAttention、CrossConfigAttentio | [predict-ai-model-runtime#456343-04](https://www.kaggle.com/competitions/predict-ai-model-runtime/discussion/456343) |
| @arc144 | A | 复盘与流程 | 最佳单模 private 0.714 / public 0.748；每 collection 用 5 到 10 个模型简单平均达到 0.736/0.757（但最终没选该提交）；负结 | [predict-ai-model-runtime#456343-05](https://www.kaggle.com/competitions/predict-ai-model-runtime/discussion/456343) |

## 高票评论

_无 ≥10 票评论_

## 关联资产

- 深读：`analysis/deep/predict-ai-model-runtime.md`
- 结构化摘要：`notes/other/predict-ai-model-runtime.md`
- 归档讨论区：`intel/predict-ai-model-runtime/`（主题 1 条有 ≥50 票帖，图证 1 个）
