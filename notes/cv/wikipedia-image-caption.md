# Wikipedia - Image/Caption Matching（多语言图文匹配，精选）

> 主题：cv ｜ 子类：— ｜ 领域：多模态百科 ｜ 类别：Playground/研究型 ｜ 截止：2021-12-09 ｜ 队伍数：105 ｜ 指标：NDCG@K
> 出处：`intel/wikipedia-image-caption/`（32 条主题索引 + 6 篇正文）

## 任务

维基百科的**多语言图文匹配**：给定图片与候选说明/文章，检索匹配（NDCG@K）；数据为"图片 URL + 标题/描述"的百科规模多模态集合，属研究型低竞争场。

## 关键要点

- **数据工程第一课：URL 化的图片数据集**（社区帖的教训）：图片不在本地而是 URL 列表 → 需 `urlretrieve`/流式读取、nrows 抽样、缓存与容错；本场大量时间花在"怎么把图片喂进模型"。
- 资源型讨论区：相似竞赛 Mega Thread（Shopee 检索赛等）、图片描述论文清单（含 code）、入门 notebook 汇编——研究型比赛的资产以文献与流程为主。
- 低参赛量（105 队）说明：多语言/多模态规模门槛劝退了多数人——**数据搬运与 I/O 优化本身是主要竞争力**。

## 可迁移要点

- URL 数据集处理范式：抽样检查 → 流式下载 → 本地缓存 → 容错重试（与 `intel` 归档脚本同源思想）。
- 图文检索的指标（NDCG@K）需要按 k 截断评估与候选排序设计。
- 同类任务（Shopee、Flickr、COCO 系）的公开方案可横向复用。

## 出处

- 官方欢迎帖：https://www.kaggle.com/competitions/wikipedia-image-caption/discussion/272023
- 大尺寸 URL 图片数据处理经验：https://www.kaggle.com/competitions/wikipedia-image-caption/discussion/272204
- 相似竞赛方案汇总（Shopee Mega Thread）：https://www.kaggle.com/competitions/wikipedia-image-caption/discussion/283917
