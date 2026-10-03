# Drawing with LLMs

> `drawing-with-llms` ｜ Featured ｜ 指标 SVG Image Fidelity ｜ 1309 队 ｜ 截止 2025-05-27

本页汇总该场 **2 条 ≥50 票 GM 主题帖**、**8 条断言**、**0 条高票评论**。

## GM 主题帖

| 票 | 选手 | 日期 | 主题 |
| --- | --- | --- | --- |
| 98 | [@cnumber](https://www.kaggle.com/cnumber) | 2025-05-28 | [3rd place solution: VQA/AES=0.81/0.64 Diffusion model + differentiable](https://www.kaggle.com/competitions/drawing-with-llms/discussion/581024) |
| 79 | [@tatamikenn](https://www.kaggle.com/tatamikenn) | 2025-02-28 | [Text Rendering: OCR-Exploit [LB=0.305]](https://www.kaggle.com/competitions/drawing-with-llms/discussion/565396) |

## 断言（条件→动作→机制→结果）

| 选手 | 等级 | 阶段 | 动作（节选） | 出处 |
| --- | --- | --- | --- | --- |
| @cnumber | A | 建模与训练 | FLUX.1-schnell 按 4 个 prompt 模板各生成 2 张位图（共 8 候选）→ vtracer 转 SVG（二分搜索 PNG 分辨率满足大小限制）→ SigLIP | [drawing-with-llms#581024-01](https://www.kaggle.com/competitions/drawing-with-llms/discussion/581024) |
| @tatamikenn | A | 报告结果 | local CLIP 0.285 / LB 0.305；提交耗时 2527 秒（约 5.0 秒/实例） | [drawing-with-llms#565396-03](https://www.kaggle.com/competitions/drawing-with-llms/discussion/565396) |
| @cnumber | B | 建模与训练 | 总损失为三项加权和：Aesthetic Predictor 负分（最大化美观）+ SigLIP 余弦相似度（渲染 SVG 与目标位图）+ MSE（与初始位图）；Adam + cos | [drawing-with-llms#581024-02](https://www.kaggle.com/competitions/drawing-with-llms/discussion/581024) |
| @cnumber | B | 工程/流程 | 实现 ImageProcessorTorch：随机裁剪缩放、diff_jpeg、中值滤波、FFT 低通、双边滤波；不可微处用 straight-through estimator； | [drawing-with-llms#581024-03](https://www.kaggle.com/competitions/drawing-with-llms/discussion/581024) |
| @cnumber | B | 后处理 | 后处理：去 opacity、RGB 转 hex、数值取整、同色路径合并、路径命令优化（相对命令与 H/V 线）、二分搜索渲染尺寸、必要时激进剪枝 | [drawing-with-llms#581024-04](https://www.kaggle.com/competitions/drawing-with-llms/discussion/581024) |
| @tatamikenn | B | 建模与训练 | 把描述文本直接画进 SVG 可提高与输入文本的相似度；因禁止直接文本渲染，用字体 glyph 转 SVG path 实现文本可视化 | [drawing-with-llms#565396-01](https://www.kaggle.com/competitions/drawing-with-llms/discussion/565396) |
| @tatamikenn | B | 工程/流程 | 在 10,000 字节限制内搜索最大有效文本长度；搜索 24 种背景色 | [drawing-with-llms#565396-02](https://www.kaggle.com/competitions/drawing-with-llms/discussion/565396) |
| @cnumber | C | 复盘与流程 | 作者明确声明方案没有用文本 embedding 去 hack VQA 评测器，而是走图像生成加矢量优化 | [drawing-with-llms#581024-05](https://www.kaggle.com/competitions/drawing-with-llms/discussion/581024) |

## 高票评论

_无 ≥10 票评论_

## 关联资产

- 深读：`analysis/deep/drawing-with-llms.md`
- 结构化摘要：`notes/nlp/drawing-with-llms.md`
- 归档讨论区：`intel/drawing-with-llms/`（主题 2 条有 ≥50 票帖，图证 5 个）
