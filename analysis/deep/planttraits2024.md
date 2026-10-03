# PlantTraits2024（植物性状多目标回归）轻量深读（Tier B）

> 赛事：Research（标准赛）｜ 主题 cv（多模态：图像 + 表格 → 6 个性状）｜ 398 队 ｜ 指标 R² ｜ 截止 2024-06-02
> 材料基础：`digests/planttraits2024.md`（6 篇正文：植物表型综述 473745 / 1st PlantHydra 510393 / 6th AutoGluon 510143 / 9th DINOv2+CatBoost 510188 / 测试集更新与重算 486503 / 提交列顺序 487985；58 条主题索引）+ 3 张归档图
> 轻读时间：2026-10（Tier B B19）

## 1. 一句话重述与数字账

从植物照片 + 气候/土壤元数据预测 **6 个性状均值**（R²）。三条获奖路线共同指向一句话：**"物种身份"是隐藏变量**——1st 把训练集按性状聚成 **17,396 个"物种"**，用回归 + 硬分类 + 软分类三个头融合；6th 用 AutoGluon 的多模态栈 + 标签链；9th 用 DINOv2 embedding + CatBoost。本场还有一次重大赛事事故：有选手利用 `sample_submission.csv` 刷榜，官方**更换测试集并重置排行榜**；另有"提交列顺序必须与 sample_submission 一致"这个致命细节。

| 关键数字 | 值 | 来源 |
| --- | --- | --- |
| 规模与目标 | **398 队**；6 个目标列 `X4_mean/X11_mean/X18_mean/X50_mean/X26_mean/X3112_mean`；R²（官方只计 >0 的值） | 索引 / 481308 |
| 1st（PlantHydra） | 三头：回归头（归一化性状）+ 分类头（**17,396 个"物种"**）+ 软分类头（按 softmax 权重对物种性状加权求和），三头权重可训练；DINOv2 ViT-b/l + **PlantCLEF 2024 西南欧植物预训练**；元数据用 **Structured Self-Attention**（PCA 失败）；损失 = 回归 R²+cosine、分类 focal、最终未归一化 R²；骨干与头用不同 LR schedule；MoE 混合不同风味模型 | 510393 |
| 9th（DINOv2+CatBoost） | DINOv2 [giant] embedding + 表格 → **CatBoost 原生处理 embedding**（含降维）；public **0.51162** / private **0.51238**；2 阶多项式特征小增益；**不同 embedding 的模型融合无效** | 510188 |
| 6th（AutoGluon） | TIMM 图像特征 + 表格特征 → Transformer 融合（略优于 MLP）；**标签链**（按论文 R² 顺序逐个预测）；EVA 系列最强：`eva_large_patch14_336` private **0.483**、`eva02_large_patch14_448` **0.486**、vit_large_384 0.43、swin_large 0.419；再 stacking → **0.526（第 6）** | 510143 |
| 公开基线进展 | 纯表格 +0.02486（480563）；表格 + ImageNet 特征 ≈0.22（489515）；EfficientNetB0 仅正分 +0.08921（486973）；sample_submission + 表格 = 0.3584（483574，后因测试集更换失效） | 索引 |
| 赛事事故 | 有选手用 `sample_submission.csv` 提分 → 官方**更新测试集（图片+test.csv）并重置 LB**；`sample_submission.csv` 在新测试集上从正分变成 **-33.38** | 486503 / 483518 |
| 提交细节 | **列顺序必须与 sample_submission 一致**（不是表头匹配就行）：`['X4_mean','X11_mean','X18_mean','X50_mean','X26_mean','X3112_mean']` | 487985 |
| 数据质量争议 | 极端标签值处理（9 票 / 10 评论）；"Poor labeling"（7 票）；为何不给物种（7 票）；性状数 6 vs 聚合数据 33（5 票）；单位为题；负 X4；R² 只计正值的规则被质疑 | 索引 |

## 2. 逐方案对照矩阵

| 维度 | 1st PlantHydra | 6th AutoGluon | 9th DINOv2+CatBoost |
| --- | --- | --- | --- |
| 核心 | 回归+硬分类+软分类三头 | 多模态 AutoML + 标签链 + stacking | 大模型 embedding + GBDT |
| 图像侧 | DINOv2 ViT-b/l + 植物域预训练 | TIMM（EVA 最强） | DINOv2 giant |
| 表格侧 | Structured Self-Attention | FT-Transformer/MLP | 原样拼接 |
| 后处理 | 三头可训练权重融合 | 模型 soup + stack | 2 阶多项式 |
| 私榜 | 冠军（未报分数） | 0.526 | 0.51238 |

## 3. 共识、分歧与裁决

### 共识一：把"物种识别"显式建模是最大杠杆（510393 / 510143；置信度中高）

1st 的三头里分类/软分类贡献核心；6th 的标签链也依赖性状相关性。**裁决**：多性状回归先做"物种/聚类身份"辅助任务（硬标签 + 软权重两条支路），再与直接回归融合；聚类数按性状唯一组合确定。置信度：中高。

### 共识二：大模型 embedding + 轻量头部/GBDT 是性价比最高的起手式（510188 / 510143；置信度中高）

9th 用 DINOv2+CatBoost 进前 10；6th 用 AutoGluon 多模态进前 6；两者都避免端到端大模型训练。**裁决**：算力有限时先冻结大骨干提 embedding，再上 CatBoost/stacking；端到端微调留给最后冲榜。置信度：中高。

### 事件一：域内预训练模型显著加分（510393；置信度中）

PlantCLEF 2024（Pl@ntNet 西南欧植物）预训练"显著提升"性状识别。**裁决**：生物/农业赛道优先找领域预训练权重，再考虑通用 ImageNet 权重。置信度：中（冠军自述）。

### 事件二：分层学习率调度是微调成败关键（510393；置信度中）

1st 用不同的 scheduler：头与融合权重高 LR + 早 warmup，backbone block 逐层降 LR，tokens 最低（图见下）。**裁决**：微调大骨干时按层组设置 LR/冻结解冻顺序，不要全网络单一 LR。置信度：中。

### 事件三：赛事公平性与提交规范被两次事故教育（486503 / 487985；置信度高）

sample_submission 刷榜导致换测试集+重置 LB；列顺序错位造成 CV/LB 大幅不一致。**裁决**：提交前核对列顺序与行数；发现"利用样例文件"的机会先报告而不是利用；本地 CV 与 LB 不一致时先查提交格式。置信度：高。

### 分歧：多图/多模态增强是否值得（510143 vs 510393；置信度低）

6th 用 5 张图/物种未提升；1st 靠元数据自注意力拿到核心增益。**裁决**：优先元数据融合与物种建模，多图策略在大规模算力下再试。置信度：低。

## 4. 证据分级

| 断言 | 等级 | 说明 |
| --- | --- | --- |
| 1st 三头架构与损失设计 | 冠军自述 + 调度图（510393） | 中高（无分数表） |
| 9th 的 0.51238 与 DINOv2+CatBoost | 自述 + notebook（510188） | 中高 |
| 6th 的分模型分数与 0.526 | 自述（510143） | 中（AutoML 细节依赖框架） |
| 测试集更换与 LB 重置 | 官方帖（486503） | 高 |
| 列顺序问题 | 官方样例 + 作者复盘（487985） | 高 |
| 数据质量争议 | 多帖（481726 / 478549 等） | 中 |

## 5. 悬案与缺口（登记）

- 1st 未公开私榜分数与完整消融；"三头权重"具体数值未给；
- 官方为何选 6 个性状、R² 只计 >0 的规则依据未归档；
- 换测试集后旧提交的最终处理细节未归档；
- 多图/物种分类路线未充分验证；
- **图证缺口**：无（3 张图，本深读内嵌 1 张调度图；PlantHydra 的 DALL-E 蛇图与植物插画无分析价值，未内嵌）。

## 6. 图表证据

![PlantHydra 分层学习率调度](../../intel/planttraits2024/bodies/510393_img/02.png)

**图**（topic 510393，1st）：多 scheduler 学习率曲线——head（蓝）峰值 1e-4 且最早 warmup；blend weights（橙）次之；backbone block7–12（绿→黑）峰值逐层降低（8e-5 → 2e-5）；tokens（黄）最低（2e-5）。直接支撑"头高 LR、骨干低 LR"的微调裁决。

## 7. 出处

- 1st PlantHydra（29 票 / 13 评论）：https://www.kaggle.com/competitions/planttraits2024/discussion/510393
- 6th AutoGluon（9 票 / 4 评论）：https://www.kaggle.com/competitions/planttraits2024/discussion/510143
- 9th DINOv2+CatBoost（9 票 / 1 评论）：https://www.kaggle.com/competitions/planttraits2024/discussion/510188
- 测试集更新与重算（13 票 / 13 评论）：https://www.kaggle.com/competitions/planttraits2024/discussion/486503
- 提交列顺序（13 票 / 3 评论）：https://www.kaggle.com/competitions/planttraits2024/discussion/487985
- 植物表型综述（37 票 / 13 评论）：https://www.kaggle.com/competitions/planttraits2024/discussion/473745
- R² 只计正值规则（3 票 / 1 评论）：https://www.kaggle.com/competitions/planttraits2024/discussion/481308
- 极端标签值处理（9 票 / 10 评论）：https://www.kaggle.com/competitions/planttraits2024/discussion/478549
