# Learning Agency Lab - PII Data Detection

> 主题：nlp ｜ 子类：— ｜ 领域：教育/隐私 ｜ 类别：Featured
> 截止：2024-04-23 ｜ 队伍数：2048 ｜ 机制：代码赛 ｜ 指标：PII 检出（token 级）
> 数据来源：`intel/pii-detection-removal-from-educational-data/`（120 条主题索引 + 8 篇 write-up 正文）

## 1. 任务与数据

- **预测目标**：在教育文本中检出并移除个人身份信息（PII），属于**长文本 token 分类**任务。
- **数据形态**：学生作文 + 逐 token 标注；文本长、类别多、样本有限。
- **构造陷阱**：长文本需要滑窗 + stride 切分；类别不平衡；对齐/边界错误直接损失分数。

## 2. 验证方案

| 方案 | 使用者 | 说明 |
| --- | --- | --- |
| 5 折 CV + 多模型集成 | 4th | 2×DeBERTa-v3-large × 5 折 = 10 个模型 |
| CV 与榜分对齐 | 5th | 表格中同时给出 CV/公开/私榜（如 0.979/0.973/0.960） |
| 社区数据集交叉验证 | 多队 | 公开数据集对本场贡献极大 |

## 3. 方案谱系

| 方案 | 名次 | 关键点 |
| --- | --- | --- |
| 多样 DeBERTa 架构集成 + 后处理 | 1st | 架构多样性 + 边界/规则后处理 |
| DeBERTa-v3-large + **Llama-3-70B 生成训练数据** | 4th | 标题即"Llama3 70B is all you need"；maxlen 4000 / stride 1024，推理 < 7 小时 |
| 不同 max_length（128 vs 512）模型集成 | 5th | 序列长度差异带来互补，权重按 CV 分配 |
| 多模型方案 | 2nd / 3rd | 见讨论区 |

## 4. 关键技巧

- **长文本切分策略**（maxlen/stride）是核心超参，不同切分方式本身就是集成多样性来源。
- **LLM 生成训练数据**：用 Llama-3-70B 合成标注数据扩充训练集。
- **架构多样性**：同一基座的不同变体 + 不同长度 + 后处理规则。
- **后处理**：PII 类别的格式规则（邮箱、电话）可硬编码校验。
- **推理时间预算**：长文本推理耗时，需要在时限内完成集成。

## 5. 可迁移性评估

- **可直接迁移**：
  - 长文本的 **maxlen/stride 组合**是超参也是集成维度。
  - LLM 合成标注数据扩充小样本任务。
  - 规则后处理与模型互补（结构化格式用规则最可靠）。
- **需要前提**：
  - 长文本训练需要大显存；推理需要时间预算管理。
- **不建议照搬**：无。

## 6. 对新手的关键启示

1. **长文本任务先调切分**（长度与重叠），它比换模型更影响结果。
2. **不同切分/长度可以当集成成员**，成本低。
3. **规则 + 模型**组合在结构化实体（邮箱/电话/ID）上最稳。

## 7. 出处

- 讨论区索引：`intel/pii-detection-removal-from-educational-data/topics.md`（120 条）
- 已收录 write-up（8 篇）：
  - 1st（99 票）：https://www.kaggle.com/competitions/pii-detection-removal-from-educational-data/discussion/497374
  - 2nd（57 票）：https://www.kaggle.com/competitions/pii-detection-removal-from-educational-data/discussion/497352
  - 3rd（26 票）：https://www.kaggle.com/competitions/pii-detection-removal-from-educational-data/discussion/497482
  - 4th（43 票）：https://www.kaggle.com/competitions/pii-detection-removal-from-educational-data/discussion/497367
  - 5th（45 票）：https://www.kaggle.com/competitions/pii-detection-removal-from-educational-data/discussion/497306
