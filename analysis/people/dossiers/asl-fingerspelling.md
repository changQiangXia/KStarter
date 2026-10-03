# Google - American Sign Language Fingerspelling Recognition

> `asl-fingerspelling` ｜ Research ｜ 指标 PostProcessorKernelDesc ｜ 1314 队 ｜ 截止 2023-08-24

本页汇总该场 **1 条 ≥50 票 GM 主题帖**、**6 条断言**、**1 条高票评论**。

## GM 主题帖

| 票 | 选手 | 日期 | 主题 |
| --- | --- | --- | --- |
| 242 | [@christofhenkel](https://www.kaggle.com/christofhenkel) | 2023-08-25 | [[1st place solution] Improved Squeezeformer + TransformerDecoder + Cle](https://www.kaggle.com/competitions/asl-fingerspelling/discussion/434485) |

## 断言（条件→动作→机制→结果）

| 选手 | 等级 | 阶段 | 动作（节选） | 出处 |
| --- | --- | --- | --- | --- |
| @christofhenkel | A | 建模与训练 | 用 Llama rotary embedding 替换相对位置编码；旋转嵌入缓存一次并在各层共享 | [asl-fingerspelling#434485-02](https://www.kaggle.com/competitions/asl-fingerspelling/discussion/434485) |
| @christofhenkel | A | 建模与训练 | 组合增广：时间缩放/平移、左右翻转、同签名者内 CutMix、手指/面部/姿态 dropout、时间与空间 masking；多数增广作用 50% 样本，resize/affine  | [asl-fingerspelling#434485-03](https://www.kaggle.com/competitions/asl-fingerspelling/discussion/434485) |
| @christofhenkel | A | 后处理 | 额外预测 confidence（目标为历史 OOF 预测的归一化 Levenshtein 距离）；confidence<0.15 或序列<15 帧时替换为 dummy phrase | [asl-fingerspelling#434485-04](https://www.kaggle.com/competitions/asl-fingerspelling/discussion/434485) |
| @christofhenkel | A | 建模与训练 | 用 mixed precision 训练（cosine 400 epochs、peak LR 0.0045、weight decay 0.08、10 epochs warmup、e | [asl-fingerspelling#434485-05](https://www.kaggle.com/competitions/asl-fingerspelling/discussion/434485) |
| @christofhenkel | B | 复盘与流程 | 记录无效尝试：全量使用补充数据、edit distance loss、CTC（含辅助损失）、label smoothing、AWP（fp16 下 nan）、TTA、hidden-l | [asl-fingerspelling#434485-06](https://www.kaggle.com/competitions/asl-fingerspelling/discussion/434485) |
| @christofhenkel | C | 建模与训练 | 单 encoder-decoder：encoder 为适配关键点的改进 Squeezeformer，decoder 为 2 层 Transformer；另加线性头预测 confid | [asl-fingerspelling#434485-01](https://www.kaggle.com/competitions/asl-fingerspelling/discussion/434485) |

## 高票评论

| 票 | 选手 | 日期 | 摘录 | 出处 |
| --- | --- | --- | --- | --- |
| 12 | @christofhenkel | 2023-08-25 | Let me comment on a few of your point. Wont go into details, just give some of my thoughts Well, I entered thi | [434485](https://www.kaggle.com/competitions/asl-fingerspelling/discussion/434485) |

## 关联资产

- 深读：`analysis/deep/asl-fingerspelling.md`
- 结构化摘要：`notes/cv/asl-fingerspelling.md`
- 归档讨论区：`intel/asl-fingerspelling/`（主题 1 条有 ≥50 票帖，图证 2 个）
