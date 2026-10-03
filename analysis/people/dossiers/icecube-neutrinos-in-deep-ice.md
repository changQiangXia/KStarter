# IceCube - Neutrinos in Deep Ice

> `icecube-neutrinos-in-deep-ice` ｜ Research ｜ 指标 MeanAngularError ｜ 812 队 ｜ 截止 2023-04-19

本页汇总该场 **1 条 ≥50 票 GM 主题帖**、**5 条断言**、**0 条高票评论**。

## GM 主题帖

| 票 | 选手 | 日期 | 主题 |
| --- | --- | --- | --- |
| 56 | [@dipamc77](https://www.kaggle.com/dipamc77) | 2023-04-20 | [3rd Place - Attention + XGBoost Ensembler](https://www.kaggle.com/competitions/icecube-neutrinos-in-deep-ice/discussion/402888) |

## 断言（条件→动作→机制→结果）

| 选手 | 等级 | 阶段 | 动作（节选） | 出处 |
| --- | --- | --- | --- | --- |
| @dipamc77 | A | 建模与训练 | 基础模型用自注意力（NanoGPT 风格）：输入为归一化 pulse 与 transparency，序列最多 256，优先采样 aux=False 的 pulse；输出两个 128 | [icecube-neutrinos-in-deep-ice#402888-01](https://www.kaggle.com/competitions/icecube-neutrinos-in-deep-ice/discussion/402888) |
| @dipamc77 | A | 建模与训练 | 小模型有效的增广、监督对比、多池化、球面单分类器在大模型上被洗掉；真正提升来自 scaling：128 维 9 层 200 batch 约 1.001、256/12/400 约 0 | [icecube-neutrinos-in-deep-ice#402888-02](https://www.kaggle.com/competitions/icecube-neutrinos-in-deep-ice/discussion/402888) |
| @dipamc77 | A | 工程/流程 | FP16 加 FlashAttention 训练快，但 score 到 0.990 后不稳定 → 切 FP32（仅大模型出现）；按事件长度分组 batch 减少 padding：比 | [icecube-neutrinos-in-deep-ice#402888-03](https://www.kaggle.com/competitions/icecube-neutrinos-in-deep-ice/discussion/402888) |
| @dipamc77 | A | 集成与融合 | base 分类器与 vMF 栈模型输出：简单投票（差太远不平均）0.976 到 0.973，加置信度/长度/z 阈值到 0.9715；再用 XGBoost 融合两模型输出一次到 0 | [icecube-neutrinos-in-deep-ice#402888-04](https://www.kaggle.com/competitions/icecube-neutrinos-in-deep-ice/discussion/402888) |
| @dipamc77 | B | 复盘与流程 | 先测 scaling（尤其欠拟合时）再做特征工程；先把 pipeline 工程做好以便快速试想法；模型分歧大且未接近上限时训练分类器做 ensemble；不要放弃；后悔没试 GNN | [icecube-neutrinos-in-deep-ice#402888-05](https://www.kaggle.com/competitions/icecube-neutrinos-in-deep-ice/discussion/402888) |

## 高票评论

_无 ≥10 票评论_

## 关联资产

- 深读：`analysis/deep/icecube-neutrinos-in-deep-ice.md`
- 结构化摘要：`notes/science/icecube-neutrinos-in-deep-ice.md`
- 归档讨论区：`intel/icecube-neutrinos-in-deep-ice/`（主题 1 条有 ≥50 票帖，图证 1 个）
