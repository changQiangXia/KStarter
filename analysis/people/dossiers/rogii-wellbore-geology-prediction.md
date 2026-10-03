# ROGII - Wellbore Geology Prediction

> `rogii-wellbore-geology-prediction` ｜ Featured ｜ 指标 Mean Squared Error ｜ 6125 队 ｜ 截止 2026-08-05

本页汇总该场 **2 条 ≥50 票 GM 主题帖**、**10 条断言**、**0 条高票评论**。

## GM 主题帖

| 票 | 选手 | 日期 | 主题 |
| --- | --- | --- | --- |
| 184 | [@w5833946](https://www.kaggle.com/w5833946) | 2026-08-06 | [1st Place Solution](https://www.kaggle.com/competitions/rogii-wellbore-geology-prediction/discussion/733220) |
| 53 | [@cdeotte](https://www.kaggle.com/cdeotte) | 2026-08-06 | [36th Place - GPT5.6 Sol - Yolo](https://www.kaggle.com/competitions/rogii-wellbore-geology-prediction/discussion/733181) |

## 断言（条件→动作→机制→结果）

| 选手 | 等级 | 阶段 | 动作（节选） | 出处 |
| --- | --- | --- | --- | --- |
| @cdeotte | A | 工程/流程 | codex --yolo 连续两周 + 2×L4 跑实验；GPT5.6 Sol 读讨论/notebook/搜网页理解科学；每晚与 Codex 简短对话给次日方向；得到单模 CV 5 | [rogii-wellbore-geology-prediction#733181-01](https://www.kaggle.com/competitions/rogii-wellbore-geology-prediction/discussion/733181) |
| @cdeotte | A | 建模与训练 | 建 parent TVT（已知 TVT、未来 XYZ、水平 GR、typewell、fold-pure canonical GR、粒子跟踪与残差修正、几何/层面约束）；每位置试 - | [rogii-wellbore-geology-prediction#733181-02](https://www.kaggle.com/competitions/rogii-wellbore-geology-prediction/discussion/733181) |
| @cdeotte | A | 报告结果 | 单模五折 OOF RMSE 5.706354；最后真实 GR 全局 shift 把 OOF 从 5.758806 降到 5.706354（约 0.052）；最终与另一变体平均 pr | [rogii-wellbore-geology-prediction#733181-03](https://www.kaggle.com/competitions/rogii-wellbore-geology-prediction/discussion/733181) |
| @cdeotte | A | 复盘与流程 | 软平均不同地质层产生物理不可能的中间层；HMM 神经分支概率过度自信，独立真实 GR 对齐更可靠；中值滤波在部分折有效但冻结后变差（5.709434 对 5.706354）；更复杂 | [rogii-wellbore-geology-prediction#733181-04](https://www.kaggle.com/competitions/rogii-wellbore-geology-prediction/discussion/733181) |
| @w5833946 | B | 建模与训练 | 把问题建成 2D 对齐：水平井 345 个位置（下采样 32；1024 可见 + 10000 目标区）、typewell 400 个位置（±100 ft，0.5 ft 分辨率）；主 | [rogii-wellbore-geology-prediction#733220-01](https://www.kaggle.com/competitions/rogii-wellbore-geology-prediction/discussion/733220) |
| @w5833946 | B | 建模与训练 | 2D U-Net + ConvNeXt（convnext_small.in12k_ft_in1k_384）；把 ConvNeXt 的 LayerNorm 换成 BatchNorm（ | [rogii-wellbore-geology-prediction#733220-02](https://www.kaggle.com/competitions/rogii-wellbore-geology-prediction/discussion/733220) |
| @w5833946 | B | 验证设计 | 加入 XY 邻域信息提升 local CV 约 0.3 RMSE 但公开榜变差；做了多项邻域质量分析后归因于标签不一致，选择相信 local CV | [rogii-wellbore-geology-prediction#733220-03](https://www.kaggle.com/competitions/rogii-wellbore-geology-prediction/discussion/733220) |
| @w5833946 | B | 特征与数据工程 | 粒子滤波独立 CV 约 7.4 RMSE；关键改进：允许低概率大跳变、typewell GR 校准、FFBSi 平滑、混合多种配置、按 64 样本分箱更新粒子 | [rogii-wellbore-geology-prediction#733220-04](https://www.kaggle.com/competitions/rogii-wellbore-geology-prediction/discussion/733220) |
| @w5833946 | B | 特征与数据工程 | 两个核心增广：Z-shift（块 bootstrap 生成 TVT 路径并保持 TVT+Z 不变，用 typewell 重建 GR，另模拟罕见断层跳变）与 GR transform | [rogii-wellbore-geology-prediction#733220-05](https://www.kaggle.com/competitions/rogii-wellbore-geology-prediction/discussion/733220) |
| @w5833946 | B | 集成与融合 | 无可靠 XY 的井改用不含 XY 通道、含 z_diff 的模型；不同模型在增广与训练配置上也有差异；最终加权集成 | [rogii-wellbore-geology-prediction#733220-06](https://www.kaggle.com/competitions/rogii-wellbore-geology-prediction/discussion/733220) |

## 高票评论

_无 ≥10 票评论_

## 关联资产

- 深读：`analysis/deep/rogii-wellbore-geology-prediction.md`
- 结构化摘要：`notes/science/rogii-wellbore-geology-prediction.md`
- 归档讨论区：`intel/rogii-wellbore-geology-prediction/`（主题 2 条有 ≥50 票帖，图证 0 个）
