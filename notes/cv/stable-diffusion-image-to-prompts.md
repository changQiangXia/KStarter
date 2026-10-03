# Stable Diffusion - Image to Prompts

> 主题：cv ｜ 子类：— ｜ 领域：生成式 AI ｜ 类别：Featured
> 截止：2023-XX-XX ｜ 队伍数：1200+ ｜ 机制：代码赛 ｜ 指标：CLIP 嵌入相似度
> 数据来源：`intel/stable-diffusion-image-to-prompts/`（80 条主题索引 + 6 篇 write-up 正文）

## 1. 任务与数据

- 预测目标：给定由 Stable Diffusion 生成的图像，**反推其提示词**（按 CLIP 句向量相似度评分）。
- 数据形态：官方训练集很小；**社区大量自建合成数据**——这是本场的主要竞争点。
- 构造陷阱：指标是嵌入相似度（对目标文本的"语义方向"敏感，而非逐词匹配）。

## 2. 方案谱系

| 方案 | 名次 | 关键点 |
| --- | --- | --- |
| 自建 **1060 万图像 / 860 万提示词**数据集 + ViT 回归 CLIP 嵌入 | 1st | 用多种加速手段批量生成；再做消融验证各机制贡献 |
| 自建数据集 + 监督学习预测句向量 | 2nd | 明确"与公开 notebook 的 ViT 方法基本一致"，差异在数据规模与训练细节 |
| 其他方案 | 3rd / 11th | 见讨论区 |

## 3. 关键技巧

- **数据规模是主要杠杆**：千万级自生成图像-提示词对，其它技巧都是次要的。
- **回归到嵌入空间**（而非生成文本）：直接把指标空间当作学习目标。
- **生成加速**：批量推理/并行生成决定你能造多大的数据集。
- **消融验证**：冠军专门做消融说明各机制的贡献（可复用的工程纪律）。

## 4. 可迁移性评估

- **可直接迁移**：
  - **当指标是嵌入相似度时，直接回归嵌入**而不是生成文本。
  - 自建合成数据集（用生成模型造训练数据）——与 LLM Prompt Recovery、Deep Past、ARC Prize 的结论一致。
  - 生成吞吐 = 数据规模 = 竞争上限。
- 需要前提：GPU 资源用于批量生成；CLIP 类模型可离线使用。
- 不建议照搬：只在小数据集上调模型结构。

## 5. 对新手的关键启示

1. **能造数据就造数据**：本场冠亚军都把预算花在造数据上。
2. **对齐指标空间**（回归嵌入）比"看起来自然"的输出更有效。
3. **算力换数据规模**是本类比赛的通用公式。

## 6. 出处

- 讨论区索引：`intel/stable-diffusion-image-to-prompts/topics.md`（80 条）
- 已收录 write-up（6 篇）：
  - 1st（121 票）：https://www.kaggle.com/competitions/stable-diffusion-image-to-prompts/discussion/411237
  - 2nd（96 票）：https://www.kaggle.com/competitions/stable-diffusion-image-to-prompts/discussion/410606
  - 3rd（38 票）：https://www.kaggle.com/competitions/stable-diffusion-image-to-prompts/discussion/410686
  - 11th（33 票）：https://www.kaggle.com/competitions/stable-diffusion-image-to-prompts/discussion/410611
