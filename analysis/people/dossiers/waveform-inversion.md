#  Yale/UNC-CH - Geophysical Waveform Inversion

> `waveform-inversion` ｜ Research ｜ 指标 Mean Absolute Error ｜ 1365 队 ｜ 截止 2025-06-30

本页汇总该场 **3 条 ≥50 票 GM 主题帖**、**14 条断言**、**0 条高票评论**。

## GM 主题帖

| 票 | 选手 | 日期 | 主题 |
| --- | --- | --- | --- |
| 194 | [@harshitsheoran](https://www.kaggle.com/harshitsheoran) | 2025-07-01 | [1st Place Solution](https://www.kaggle.com/competitions/waveform-inversion/discussion/587388) |
| 60 | [@tascj0](https://www.kaggle.com/tascj0) | 2025-07-01 | [3rd place solution](https://www.kaggle.com/competitions/waveform-inversion/discussion/587419) |
| 59 | [@christofhenkel](https://www.kaggle.com/christofhenkel) | 2025-07-01 | [9th place - Custom CUDA kernel for wave propagation](https://www.kaggle.com/competitions/waveform-inversion/discussion/587498) |

## 断言（条件→动作→机制→结果）

| 选手 | 等级 | 阶段 | 动作（节选） | 出处 |
| --- | --- | --- | --- | --- |
| @harshitsheoran | A | 数据理解 | 不做分割：把输入从 (5,1000,70) reshape 成 (1,350,350)，把通道铺成空间布局 | [waveform-inversion#587388-01](https://www.kaggle.com/competitions/waveform-inversion/discussion/587388) |
| @harshitsheoran | A | 建模与训练 | 用无解码器 ViT 直接回归；对比 EVA02 与 ViT 后定位到 RoPE 是主要增益来源；最终 backbone 为 vit_small_patch14_reg4_dinov | [waveform-inversion#587388-02](https://www.kaggle.com/competitions/waveform-inversion/discussion/587388) |
| @harshitsheoran | A | 特征与数据工程 | 用 FiveCrop/5xRandomAffine 在已有速度模型上生成 10 倍数据（4.7M seismic 样本）做预训练；迭代伪标签：每 epoch 预测验证与测试约 95 | [waveform-inversion#587388-03](https://www.kaggle.com/competitions/waveform-inversion/discussion/587388) |
| @harshitsheoran | A | 特征与数据工程 | 只保留 CurveFault_B/CurveVel_B/Style_A/Style_B 数据训练（移除过半数据、加速训练），推理时用该模型替换这 4 类预测；最后用 896x896 | [waveform-inversion#587388-04](https://www.kaggle.com/competitions/waveform-inversion/discussion/587388) |
| @tascj0 | A | 特征与数据工程 | 从 manatoyo 实现改进：float64 改 float32（OpenFWI 本身是 float32）；生成 6 通道 isx 取值 120、137、154、155、172、 | [waveform-inversion#587419-01](https://www.kaggle.com/competitions/waveform-inversion/discussion/587419) |
| @tascj0 | A | 数据工程 | 生成 6 通道 Full OpenFWI；同 fold 同 vel-type 的两个 vel 随机混合（alpha 0.3 到 0.7）并重复 8 个种子；同 fold 不同 ve | [waveform-inversion#587419-02](https://www.kaggle.com/competitions/waveform-inversion/discussion/587419) |
| @tascj0 | A | 建模与训练 | 输入重排为 (N,5,250,280) 再插值到 patch×18 网格；输出 16 维像素重排到 (N,1,72,72) 再裁到 70×70；logits sigmoid 乘 6 | [waveform-inversion#587419-03](https://www.kaggle.com/competitions/waveform-inversion/discussion/587419) |
| @tascj0 | A | 建模与训练 | AdamW 换 MuonWithAuxAdam 大幅提升（9.x 到 7.x）；Muon 只用于除 patch embedding 外的 Linear 权重，其余参数仍用 Adam | [waveform-inversion#587419-04](https://www.kaggle.com/competitions/waveform-inversion/discussion/587419) |
| @tascj0 | A | 工程/流程 | stage1：14×18 网格 4x 上采样、10 epochs、MAE 8.1；stage2：14×35 网格 2x 上采样、1 epoch、7.6；stage3：在验证数据上  | [waveform-inversion#587419-05](https://www.kaggle.com/competitions/waveform-inversion/discussion/587419) |
| @christofhenkel | A | 验证设计 | 按文件划 8 折；第一周只在 CurveFault_B 上训评（最难且代表性强的类） | [waveform-inversion#587498-02](https://www.kaggle.com/competitions/waveform-inversion/discussion/587498) |
| @christofhenkel | A | 工程/流程 | LR 恒 0.0005 便于在最好实验上继续跑；最后 2 天对 checkpoint 加 150 epochs cosine 并给难类更高权重；每 3 epochs 保存测试预测， | [waveform-inversion#587498-03](https://www.kaggle.com/competitions/waveform-inversion/discussion/587498) |
| @christofhenkel | A | 工程/流程 | 把波传播移植到 PyTorch GPU 并用 torch.compile；实现批量化；最后写自定义 CUDA kernel；提速约 100x，可直接在训练中按增广后的目标重算 se | [waveform-inversion#587498-04](https://www.kaggle.com/competitions/waveform-inversion/discussion/587498) |
| @christofhenkel | B | 建模与训练 | 沿用 brendanartley 的两个模型与超参（caformer_b36、convnextv2_huge），重点放在长时间训练下的高效实验与单人下注 | [waveform-inversion#587498-01](https://www.kaggle.com/competitions/waveform-inversion/discussion/587498) |
| @christofhenkel | B | 复盘与流程 | 管理训练时长并对冲平台风险（compute、数据 host、Kaggle），赛前 2 天备好 CSV 兜底；单提交导致更差分数（最后 2 天才意识到只需预测每 2 个像素，可快一倍 | [waveform-inversion#587498-05](https://www.kaggle.com/competitions/waveform-inversion/discussion/587498) |

## 高票评论

_无 ≥10 票评论_

## 关联资产

- 深读：`analysis/deep/waveform-inversion.md`
- 结构化摘要：`notes/science/waveform-inversion.md`
- 归档讨论区：`intel/waveform-inversion/`（主题 3 条有 ≥50 票帖，图证 8 个）
