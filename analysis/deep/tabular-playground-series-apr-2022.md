# Tabular Playground Series Apr 2022（传感器序列分类）轻量深读（Tier B）

> 赛事：Playground ｜ 主题 tabular（13 路传感器 × 60 步序列，二分类）｜ 816 队 ｜ 标准赛 ｜ 指标：ROC AUC
> 材料基础：`digests/tabular-playground-series-apr-2022.md`（6 篇正文：1st 322259 / 2nd 322257 / 3rd 322269 / 5th 322277 / 6th 322622 / 特征工程六坑 318527；68 条主题索引）+ 0 张可读归档图（318527_img 目录为空）
> 轻读时间：2026-10（Tier B B13）

## 1. 一句话重述与数字账

每个 subject 有 13 路传感器 × 60 步的序列，预测二分类（AUC），train/test 的 subject 完全不相交。本场是"**序列深度学习 vs 特征工程 GBDT**"的分水岭：1st 用 **LSTM 去噪自编码器（DAE）+ 预测网络 + 大混合** 拿到私榜 0.99249；2nd 的单个 4×2D-CNN+GRU 模型就有私榜 0.989（单独可排第 6）；而 5th 用 tsfresh ~9000 特征 + RFE 的 LGBM 也能进前 5。共同的硬约束是：**CV 必须按 subject 分组**，否则就是泄漏。

| 关键数字 | 值 | 来源 |
| --- | --- | --- |
| 1st（322259） | DAE（2 层 LSTM）在 train+test 上做 swap-noise 自监督（样本间 / 时间步间互换；噪声 <30% 最好）；把 DAE 各层输出当特征喂第二个预测网络（同时给原始 scaled 序列）；预测网络用**高比例 spatial dropout（>0.35）**更稳；最终混合（4 个 PyTorch DAE 跑 + 2 个 TF/TPU 模型 + LGBM）用 ElasticNet 定权；**最佳单 DAE 模型 CV 0.98999 / 私榜 0.99134；最佳总混合 CV 0.9918 / 私榜 0.99249**；10 折 GroupKFold（subject 不跨折）；最佳 DAE 训练约 8h + 预测模型 5.5h | 322259 |
| 2nd（322257） | 40 个模型的 stacking；最佳单模 = **4×2D-CNN + GRU + GlobalMaxPooling**：公 0.987 / 私 **0.989** / CV 0.963（单独即可第 6）；每折跑 3 次取最好，其余 2 次当 meta 特征；把数据 reshape 成 (-1,60,13) 后**按标签做 StratifiedKFold**（每个 index 即一个完整 subject，规避分组问题）；LGBM 元学习器 +0.00130；DAE 的 Conv2D 版本与 Transformer 都没跑通 | 322257 |
| 3rd（322269） | VD Brothers 队：10 折 GroupKFold（按 subject）；**shapelets**（tslearn 的 Keras 实现移植到 torch，加入 lr 调度/早停/条件特征，在已有特征之后挖掘互补形状）；单模 公 0.98052 / 私 0.97706；stacking（CatBoost 元学习器）→ 公 0.99037；**把预测按 subject 聚合（mean/min/max/std）再入模型：+0.002**；伪标签、同 subject 序列建模、HMM、拼接序列均失败；powershap 做特征筛选 | 322269 |
| 5th（322277） | tsfresh 生成 ~9000 个特征 + **按 subject 归一化**的镜像特征，RFE 精简；LGBM 私 0.97816 / 公 0.98248；再与 LSTM（私 0.98259）及 6 个公开 notebook 以 ~0.4/0.2/0.4 权重混合 | 322277 |
| 6th（322622） | RNN 变体：先把每条序列投影到 16 维，再对 **13 路序列分别用 4 层 GRU**（避免跨序列噪声）→ 私 0.9839 / 公 0.985；与 XGB、1D-CNN、公开 LSTM 集成 → 私 0.98797 | 322622 |
| 六坑帖（318527） | 185 票：①聚合不够有创意（sensor_04 的**峰度**是单特征最重要）；②重复聚合（sum≈mean、std≈var）；③不做特征选择；④漏掉"每 subject 的序列数"（第二重要特征）；⑤**CV 泄漏——必须 GroupKFold(subject)，不能 KFold/StratifiedKFold**；⑥RandomForest 在本场不如 GBDT | 318527 |
| 社区 | "无变化时 target=0"（14 票）；"概率比标签得分更高"（12 票）；协变量偏移（10 票）；"公榜骗人"（9 票）；NN 为何远好于 ML（10 票） | 索引 |

## 2. 逐方案对照矩阵

| 维度 | 1st | 2nd | 3rd | 5th | 6th |
| --- | --- | --- | --- | --- | --- |
| 核心 | LSTM DAE 自监督 + 预测网 | 2D-CNN+GRU + 40 模型 stacking | shapelets + stacking | tsfresh 9000 特征 + LGBM | 每路独立 GRU |
| CV | 10 折 GroupKFold(subject) | reshape 后按标签 Stratified | 10 折 GroupKFold(subject) | GroupKFold | GroupKFold |
| 自监督/外部 | DAE（train+test 无标签） | 无 | shapelet 挖掘 | 无 | 无 |
| 集成 | ElasticNet 大混合 | LGBM 元学习器 | CatBoost stacking | 加权混合 | 加权混合 |
| 私榜 | 0.99249 | 0.989（单模） | 0.97706（单模） | 0.97816 | 0.98797 |

## 3. 共识、分歧与裁决

### 共识一：CV 必须按 subject 分组（1st、3rd、六坑帖、5th；置信度高）

test 的 subject 与 train 不相交；六坑帖把"KFold/StratifiedKFold"直接列为错误，3rd 用 10 折 GroupKFold 后 CV-LB 高度吻合。**裁决**：分组结构（subject/用户/病人）就是验证边界；忽略它必然高估。置信度：高。

### 共识二：序列深度模型是本届的主线，特征工程 GBDT 是有效补充（1st、2nd、6th vs 5th；置信度中高）

1st 的 DAE 混合 0.99249、2nd 单模 CNN+GRU 0.989、6th 的独立 GRU 0.98797；5th 的 tsfresh+LGBM 也有 0.97816 并作为混合成分。**裁决**：有序列结构时优先 RNN/CNN/自监督表示，GBDT+统计特征用于补足与集成。置信度：中高。

### 共识三：FE 要"有创造力 + 会筛"（六坑帖、5th、3rd；置信度中高）

峰度、subject 序列计数、按 subject 归一化、shapelets 等被反复验证；powershap/RFE 用于裁剪。**裁决**：聚合统计不够，要针对数据生成机制（传感器/主体）设计特征并严格选择。置信度：中高。

### 技巧：按 subject 聚合预测（3rd；置信度中）

3rd 报告把每个 subject 的模型预测做 mean/min/max/std 聚合后再入模型 +0.002。**裁决**：当样本以组出现时，组级聚合是廉价的后处理增益；建议在 CV 中验证。置信度：中（单队证据）。

### 事件：概率 vs 标签与公榜噪声（321000、318963；置信度中）

社区帖"概率比标签得分高"（AUC 对排序敏感、阈值化损失信息）与"公榜骗人"提醒：提交概率而非硬标签。**裁决**：AUC 赛一律提交校准后的概率。置信度：中。

## 4. 证据分级

| 断言 | 等级 | 说明 |
| --- | --- | --- |
| 1st 的 DAE 设计与全部分数 | 自述（含训练时长/噪声比例） | 中高 |
| 2nd 的单模 0.989 与 stacking | 自述（含 notebook） | 中高 |
| 3rd 的 shapelets 与 +0.002 聚合技巧 | 自述（含开源工具） | 中高 |
| 5th/6th 的特征与集成 | 自述 | 中 |
| 六坑帖的六条结论 | 高票帖（185 票）+ 可验证 | 中高 |
| 概率 vs 标签 | 社区帖 | 中 |

## 5. 悬案与缺口（登记）

- 4th、7th–10th 方案未收录；
- 318527 的配图未归档（目录为空）；其余帖子无图；
- HMM/序列顺序性（3rd 的失败探索）没有结论；
- **图证缺口**：本场 0 张可读归档图。

## 6. 图表证据

无可用图证（本场归档 0 张可读图，图证缺口已登记）。

## 7. 出处

- 1st DAE 方案（40 票 / 8 评论）：https://www.kaggle.com/competitions/tabular-playground-series-apr-2022/discussion/322259
- 2nd Place（25 票 / 7 评论）：https://www.kaggle.com/competitions/tabular-playground-series-apr-2022/discussion/322257
- 3rd Place（17 票 / 9 评论）：https://www.kaggle.com/competitions/tabular-playground-series-apr-2022/discussion/322269
- 5th Place（17 票 / 7 评论）：https://www.kaggle.com/competitions/tabular-playground-series-apr-2022/discussion/322277
- 6th Place（22 票 / 5 评论）：https://www.kaggle.com/competitions/tabular-playground-series-apr-2022/discussion/322622
- 特征工程六大坑（185 票 / 86 评论）：https://www.kaggle.com/competitions/tabular-playground-series-apr-2022/discussion/318527
- 无变化则 target=0（14 票）：https://www.kaggle.com/competitions/tabular-playground-series-apr-2022/discussion/316383
- 概率 vs 标签（12 票）：https://www.kaggle.com/competitions/tabular-playground-series-apr-2022/discussion/321000
- 协变量偏移（10 票）：https://www.kaggle.com/competitions/tabular-playground-series-apr-2022/discussion/317778
