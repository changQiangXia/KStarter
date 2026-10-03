# MAP - Charting Student Math Misunderstandings

> `map-charting-student-math-misunderstandings` ｜ Featured ｜ 指标 MAP@{K} ｜ 1857 队 ｜ 截止 2025-10-15

本页汇总该场 **3 条 ≥50 票 GM 主题帖**、**13 条断言**、**1 条高票评论**。

## GM 主题帖

| 票 | 选手 | 日期 | 主题 |
| --- | --- | --- | --- |
| 191 | [@tascj0](https://www.kaggle.com/tascj0) | 2025-10-18 | [1st Place Solution](https://www.kaggle.com/competitions/map-charting-student-math-misunderstandings/discussion/612268) |
| 98 | [@cdeotte](https://www.kaggle.com/cdeotte) | 2025-07-12 | [Does Test Data Have Questions Different Than Train Data?](https://www.kaggle.com/competitions/map-charting-student-math-misunderstandings/discussion/589400) |
| 81 | [@cdeotte](https://www.kaggle.com/cdeotte) | 2025-10-16 | [18th Place - Pyramid Ensemble](https://www.kaggle.com/competitions/map-charting-student-math-misunderstandings/discussion/612096) |

## 断言（条件→动作→机制→结果）

| 选手 | 等级 | 阶段 | 动作（节选） | 出处 |
| --- | --- | --- | --- | --- |
| @tascj0 | A | 验证设计 | 先用 3 seeds 集成稳住验证（5 折 x 5 seeds 实验），再用最难 fold 加 3 runs 做后续实验；最终用 32B/GLM 全量数据 3 seeds | [map-charting-student-math-misunderstandings#612268-03](https://www.kaggle.com/competitions/map-charting-student-math-misunderstandings/discussion/612268) |
| @tascj0 | A | 建模与训练 | 对照 7B/8B/9B/14B/32B：loss 从 0.2716 降到 0.2589，MAP@3 从 0.9444 升到 0.9484；32B 加 32B 双模型集成 loss  | [map-charting-student-math-misunderstandings#612268-04](https://www.kaggle.com/competitions/map-charting-student-math-misunderstandings/discussion/612268) |
| @tascj0 | A | 工程/流程 | W8A8 INT8（LMDeploy 加 SmoothQuant alpha=0.75）替代 FP16：T4 实测约 20 TFLOPS 不稳定，INT8 稳定 40+；层次化推理 | [map-charting-student-math-misunderstandings#612268-05](https://www.kaggle.com/competitions/map-charting-student-math-misunderstandings/discussion/612268) |
| @cdeotte | A | 特征与数据工程 | 新增 is_correct 特征：对每个 QuestionId 找 Category 为 True 的正确选项，标记每题答案是否正确；该特征提升当前最好公开 notebook 的  | [map-charting-student-math-misunderstandings#589400-01](https://www.kaggle.com/competitions/map-charting-student-math-misunderstandings/discussion/589400) |
| @cdeotte | A | 集成与融合 | 先全量小模型推理 → 估不确定性 → 最不确定 top 50% 用中模型（2 倍权重）→ top 10% 用大模型（4 倍）→ top 6% 用超大模型（8 倍）；最终 5 折 C | [map-charting-student-math-misunderstandings#612096-01](https://www.kaggle.com/competitions/map-charting-student-math-misunderstandings/discussion/612096) |
| @cdeotte | A | 工程/流程 | 训练 1000+ LLM 模型，覆盖 backbone、范式（分类、生成、多选、多头）、prompt、合成数据、训练配置、推理配置 | [map-charting-student-math-misunderstandings#612096-02](https://www.kaggle.com/competitions/map-charting-student-math-misunderstandings/discussion/612096) |
| @cdeotte | A | 建模与训练 | 序列分类 65 类或去 True/False 的 37 类；CausalLM 生成单 token 取 logits；多选题（每题至多 6 个候选类别、随机打乱选项、预测后映射回 6 | [map-charting-student-math-misunderstandings#612096-03](https://www.kaggle.com/competitions/map-charting-student-math-misunderstandings/discussion/612096) |
| @cdeotte | A | 特征与数据工程 | 最佳单模 prompt：加 system 指令、列出 MC_Answer 选项、列出该 QuestionId 与 MC_Answer 的候选 target 类、澄清 Correct | [map-charting-student-math-misunderstandings#612096-04](https://www.kaggle.com/competitions/map-charting-student-math-misunderstandings/discussion/612096) |
| @cdeotte | A | 建模与训练 | 14B 及以下多为全参；14B 以上用 LoRA 或 QLoRA（r=32、a=64、dropout 0.05 到 0.1、7 个 target modules、梯度检查点、bat | [map-charting-student-math-misunderstandings#612096-05](https://www.kaggle.com/competitions/map-charting-student-math-misunderstandings/discussion/612096) |
| @tascj0 | B | 工程/流程 | 实现 offload_adam（优化器状态卸载）支持 32B 单卡全参训练；实验统一 epoch=1、bs=32、lr=1e-5 | [map-charting-student-math-misunderstandings#612268-02](https://www.kaggle.com/competitions/map-charting-student-math-misunderstandings/discussion/612268) |
| @tascj0 | C | 建模与训练 | 把任务建成 suffix 分类：prefix 共享输入加 FlexAttention 自定义 mask，取 last-token 特征过线性头，交叉熵训练 | [map-charting-student-math-misunderstandings#612268-01](https://www.kaggle.com/competitions/map-charting-student-math-misunderstandings/discussion/612268) |
| @tascj0 | C | 工程/流程 | 三个挂载点语义不同：/kaggle/input 非本地且慢；/tmp 是 Copy-on-Write 有容量限制且不能真正删除；/kaggle/working 可删除释放空间；作者 | [map-charting-student-math-misunderstandings#612268-06](https://www.kaggle.com/competitions/map-charting-student-math-misunderstandings/discussion/612268) |
| @cdeotte | C | 数据理解 | 若完整 test 不含新题，可硬编码每题正确答案，从而始终知道 label 是否以 True 或 False 开头 | [map-charting-student-math-misunderstandings#589400-02](https://www.kaggle.com/competitions/map-charting-student-math-misunderstandings/discussion/589400) |

## 高票评论

| 票 | 选手 | 日期 | 摘录 | 出处 |
| --- | --- | --- | --- | --- |
| 11 | @cdeotte | 2025-07-30 | To my understanding, the private leaderboard will use a separate hidden test set, so it can't be probed direct | [589400](https://www.kaggle.com/competitions/map-charting-student-math-misunderstandings/discussion/589400) |

## 关联资产

- 深读：`analysis/deep/map-charting-student-math-misunderstandings.md`
- 结构化摘要：`notes/nlp/map-charting-student-math-misunderstandings.md`
- 归档讨论区：`intel/map-charting-student-math-misunderstandings/`（主题 3 条有 ≥50 票帖，图证 1 个）
