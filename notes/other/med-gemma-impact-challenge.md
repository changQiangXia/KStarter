# The MedGemma Impact Challenge（精简）

> 主题：other ｜ 子类：hackathon ｜ 类别：Featured ｜ 截止：2026-02-24 ｜ 队伍数：872 ｜ 指标：评审制
> 出处：`intel/med-gemma-impact-challenge/`（80 条主题索引 + 6 篇正文）

## 任务

用 MedGemma 与 Google 健康 AI 开放模型（HAI-DEF：CXR Foundation、Path Foundation、Derm Foundation 等）构建**以人为中心的医疗 AI 应用**，评审制。已从 nlp 归入 `other/hackathon`。

## 关键要点

- 官方在讨论区发布了 **HAI-DEF 基础模型清单与用法**（胸部 X 光 / 病理 / 皮肤等专用基础模型）——这类比赛的"起点"是学会用官方基座。
- 医疗 AI 应用的评审维度通常包含临床价值、可用性与合规性，而不只是模型指标。
- 与前几场黑客松（Gemini 3、Gemma 4、OpenAI to Z）合并观察：**Kaggle 的"应用型赛道"正在增多**。

## 可迁移要点

- **专用基础模型（domain foundation models）正在成为医疗 AI 的默认起点**——先摸清官方基座能力，再决定自研范围。
- 评审制比赛：把"临床价值 + 可复现性"写清楚，和技术实现同等重要。

## 轻读结论（2026-10 补）

- **规模**：872 队 / **879 份提交**；HAI-DEF 五族模型：CXR Foundation（EfficientNet-L2×3，图像+报告）、Path Foundation（病理 ViT 自监督）、Derm Foundation（BiT ResNet-101x3，16K+ 图像）、HeAR（音频 MAE）、CT Foundation（VideoCoCa）；官方局限：**分类优先、暂不支持分割/生成、端侧需蒸馏**（667677）。
- **部署是最大技术门槛**：MedGemma 27B 部署难、VertexAI 被报故障、4B 微调塌缩成单 token 重复、量化限制（673091 / 668731 / 673582）。
- **提交物流事故密集**：提交显示成功却错过、视频格式失败、晚 1 分钟关闭、迟到窗口请求（678790–678915 一串）→ 提前 48h 提交 + 留凭证。
- **评审透明度**：落选者请求分项评分/rubric 未获承诺（685138）；交付物要自包含、可独立复现。
- **合规**：外部非商用数据 + 获奖者 CC BY 4.0、HAI-DEF 监管语境等被追问（671596 / 668280）。

## 图表证据

本场 0 张归档图（0/0），**图证缺口已登记**。

## 出处

- 讨论区索引：`intel/med-gemma-impact-challenge/topics.md`
- 官方 HAI-DEF 模型说明：https://www.kaggle.com/competitions/med-gemma-impact-challenge/discussion/667677
- 评分透明性请求：https://www.kaggle.com/competitions/med-gemma-impact-challenge/discussion/685138
- 获奖延期：https://www.kaggle.com/competitions/med-gemma-impact-challenge/discussion/684112
- 获奖公布：https://www.kaggle.com/competitions/med-gemma-impact-challenge/discussion/685002
- MedGemma 27B 部署挑战：https://www.kaggle.com/competitions/med-gemma-impact-challenge/discussion/673091
