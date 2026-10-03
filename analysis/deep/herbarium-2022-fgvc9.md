# Herbarium 2022（FGVC9 植物标本细粒度分类）轻量深读（Tier B）

> 赛事：Research（标准赛）｜ 主题 cv（植物标本细粒度分类）｜ 134 队 ｜ 指标 Macro F-Score ｜ 截止 2022-05-30
> 材料基础：`digests/herbarium-2022-fgvc9.md`（6 篇正文：上手 notebook 合集 323794 / 可解释细粒度与 machine teaching 308406 / 1st 329299 / 往届 notebook 307745 / JSON→Pandas 307804 / 往届获奖 307624；39 条主题索引）+ 0 张归档图
> 轻读时间：2026-10（Tier B B19）

## 1. 一句话重述与数字账

**83.9 万张**植物标本图的超细粒度分类（Macro F1，长尾极重）。1st 方案把增益拆得非常干净：**多级分类损失（family/genus/species）→ 更高学习率 → 5-crop 多尺度 → subcenter-ArcFace 动态 margin → 额外 CE 头 → Swin 增强 → 384 分辨率 → 冻结层渐进解冻 → SwinV2**，单模 private 从 0.78442 一路推到 **0.86282**，再用 8 个骨干按公榜分数融合到 **0.87662**。值得注意的负结果：**class-aware sampling 与 data cleaning 都没用**——长尾问题靠损失/度量学习解决，而不是重采样。

| 关键数字 | 值 | 来源 |
| --- | --- | --- |
| 规模 | **839,772 张**训练图；134 队；Macro F-Score；长尾分布；CVPR FGVC9 workshop | 307615 / 索引 |
| 1st 单模消融（private） | Swin-B224 基线 **0.78442** → +多级 CE（family/genus/species）**0.79544** → LR 2e-4→5e-4 **0.80501** → +5crop **0.80981** → subcenter-ArcFace 动态 margin **0.82267** → +额外 CE 头 **0.82929** → +Swin 式增强 **0.83554** → SwinB384 **0.85245** → +5crop（384）**0.85654** → 冻结层 100→0 **0.86055** → square resize **0.86201** → SwinV2 **0.86282** | 329299 |
| 骨干对比（private） | swinv2-B 0.86282 > swin-B 0.86055 > convnext-B 0.85956 > swin-L 0.85607 > cswin-L 0.8501 > deit-iii B 0.8495 > efficient-B6 0.84321 > resnest-101 0.83838 | 329299 |
| 融合 | 用**公榜分数**做权重：3 模型 0.8679 → 5 模型 0.87185 → 8 模型 **0.87662**（private） | 329299 |
| 训练设置 | batch 512（大模型 256）、100 epoch、torch.amp；ImageNet22k 预训练；先冻结部分层放大 batch 再全参训练；后处理 +0.001 | 329299 |
| 无效项 | **class-aware sampling、data cleaning 均无效**；另有帖子报告图像重复（数据泄漏）问题 | 329299 / 323906 |
| 社区设施 | 往届 notebook 合集 38 票；JSON→Pandas 数据框 18 票；往届获奖 18 票；可解释细粒度 + machine teaching 综述 16 票 | 307745 / 307804 / 307624 / 308406 |

## 2. 逐方案对照矩阵

| 维度 | 1st（损失/分辨率/融合） | 社区起步线 |
| --- | --- | --- |
| 骨干 | SwinV2-B 主 + 8 骨干融合 | ResNet50 / EfficientNet / TresNet / Flax-Jax KFold |
| 损失 | 多级 CE + subcenter-ArcFace（动态 margin）+ CE 头 | 单 CE |
| 分辨率 | 224 → 384（+5crop、square resize） | 224 |
| 长尾 | 损失与度量学习 | WeightedRandomSampler（讨论） |
| 融合 | 按公榜分数加权 | 单模/简单平均 |

## 3. 共识、分歧与裁决

### 共识一：长尾细粒度分类用"度量损失 + 多级监督"而非重采样（329299；置信度中高）

subcenter-ArcFace 动态 margin 一步 +0.0172（private），多级 CE +0.011；class-aware sampling 无效。**裁决**：先上 ArcFace/子中心等度量损失与层级标签监督，再把重采样作为备选而非常规动作。置信度：中高（单一冠军自述，但消融链完整）。

### 共识二：分辨率与多尺度测试是稳定的第二杠杆（329299；置信度中高）

224→384 单项 +0.03；两次 5crop 各 +0.005–0.007。**裁决**：细粒度植物/标本数据在显存允许时直接冲 384+，并用多尺度 crop 做 TTA。置信度：中高。

### 事件一：多骨干融合按公榜加权有效但过拟合公榜（329299；置信度中）

8 模型融合 private 0.87662（+1.4），但权重来自公榜分数。**裁决**：融合权重用 OOF/公榜各做一版对比；公榜加权需要留出私榜验证空间，别把权重搜到公榜最优。置信度：中。

### 事件二：数据重复/泄漏是这类大型标本库的隐性风险（323906；置信度中低）

有帖报告 image duplicates，直接影响 CV 可信度。**裁决**：先做近重复检测（embedding/pHash）与分组 CV；至少确认 val/test 无重复泄漏。置信度：中低（单帖，未见官方结论）。

### 事件三：领域侧关注"人机协作与可解释"（308406 / 307851 / 308258；置信度中）

FGVC workshop 的主题包含 human-in-the-loop、machine teaching 与可解释模型；社区给了系统综述。**裁决**：评审制/workshop 赛道把"可解释性/人机协作"写进叙事是加分项，但本场实际排名仍由分类精度主导。置信度：中。

## 4. 证据分级

| 断言 | 等级 | 说明 |
| --- | --- | --- |
| 1st 的逐项消融与骨干/融合表 | 自述 + 三张表（329299） | 高（本场最可复算的收益分解） |
| 839,772 张训练图 | 社区统计帖（307615） | 中高 |
| 无效尝试（重采样/清洗） | 1st 自述 | 中 |
| 数据重复/泄漏 | 个案帖（323906） | 低—中 |
| 可解释/machine teaching 主题 | 文献综述（308406） | 中高（文献可查） |
| 往届获奖与 notebook | 社区合集（307745 / 307624） | 中高（链接可查） |

## 5. 悬案与缺口（登记）

- 除 1st 外的前排方案未归档（2nd/3rd 无正文）；
- 数据重复问题的规模与官方处理未归档；
- 融合权重按公榜搜索的过拟合风险未量化；
- Competitive wrap-up（329802）没有正文；
- **图证缺口**：本场 0 张归档图，已登记。

## 6. 图表证据

本场 0/0 张归档图，**图证缺口已登记**；1st 的消融与骨干对比均为表格，无图片证据。

## 7. 出处

- 1st 方案（5 票 / 1 评论）：https://www.kaggle.com/competitions/herbarium-2022-fgvc9/discussion/329299
- 上手 notebook 合集（15 票 / 7 评论）：https://www.kaggle.com/competitions/herbarium-2022-fgvc9/discussion/323794
- 往届 notebook（38 票 / 18 评论）：https://www.kaggle.com/competitions/herbarium-2022-fgvc9/discussion/307745
- 往届获奖方案（18 票 / 9 评论）：https://www.kaggle.com/competitions/herbarium-2022-fgvc9/discussion/307624
- JSON→Pandas（18 票 / 8 评论）：https://www.kaggle.com/competitions/herbarium-2022-fgvc9/discussion/307804
- 可解释细粒度与 machine teaching（16 票 / 2 评论）：https://www.kaggle.com/competitions/herbarium-2022-fgvc9/discussion/308406
- 训练图规模（11 票 / 17 评论）：https://www.kaggle.com/competitions/herbarium-2022-fgvc9/discussion/307615
- 数据重复/泄漏（0 票 / 7 评论）：https://www.kaggle.com/competitions/herbarium-2022-fgvc9/discussion/323906
