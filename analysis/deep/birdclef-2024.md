# BirdCLEF 2024 轻量深读（Tier B）

> 赛事：Research ｜ 主题 audio（声景物种识别）｜ 974 队 ｜ 代码赛（CPU 推理约束）｜ 指标：Birdclef ROC AUC
> 材料基础：`digests/birdclef-2024.md`（6 篇正文：4th Cerberus 511845 / 2nd 512340 / 1st 512197 / 3rd 511905 / 5th 511535 / Xeno 补充数据 491687；80 条主题索引）+ 6 张图
> 轻读时间：2026-10（Tier B B04）

## 1. 一句话重述与数字账

声景中的鸟类/两栖类识别（ROC AUC）。真正的考点是**简单 log-mel CNN + 伪标 soundscape + CPU 推理约束下的后处理**；"额外数据是否使用"与"CE vs BCE"在本场出现明显分歧。

| 关键数字 | 值 | 来源 |
| --- | --- | --- |
| 1st（107 票） | 仅 2024 数据（**额外数据最好不用**）；发现**fold0 的信号统计（std+var+rms+pwr）更低→更好**，改用 fold0 + 0.8 分位构造集成分折；Google 分类器清洗/重标/PL（0.05）；10 秒输入=两个 5 秒平均标签；EfficientNet-B0 + RegNetY-008（SED/ViT 更差）；**CE 损失（BCE 显著更差）**、bs96、7–12 epochs、2h/模型 P100；推理：sigmoid + 相邻 chunk 均值 + **min() reduction**（图 1）；OpenVINO+joblib+RAM 缓存 → 18 分钟/模型（CPU）；183 类 nocall 对公榜无益但私榜 0.655→**0.671** | 1st |
| 3rd（NVBird，78 票） | 额外数据（Xeno+往年同物种，按物种封顶 500 取最近）+ 低频类上采样；5 秒随机裁剪/填充；additive mixup；log-mel 图像模型（224/288）；**两级伪标 + 蒸馏**（第一级可用大模型，第二级受 CPU 限制）；AVES 波形模型微调 | 3rd |
| 4th Cerberus（511845） | melspec 模型（rexnet/seresnext/inception-next）+ **raw signal 模型**（tf_efficientnet_b0_ns）集成 + TTA + OpenVINO；加权平均公 0.731/私 0.667 | 4th |
| 2nd/5th | 512340 / 511535 | 材料 |

## 2. 逐方案对照矩阵

| 维度 | 1st | 3rd | 4th |
| --- | --- | --- | --- |
| 额外数据 | **不用**（明确最优） | Xeno+往年（封顶 500/物种） | 未强调 |
| 损失 | **CE** | BCE/SED 系 | — |
| 主干 | EffNet-B0/RegNetY-008 | EfficientViT/CNNs/SED/AVES | melspec+raw signal |
| 伪标 | 分类器 PL 0.05 | 两级 PL + 蒸馏 | — |
| 后处理 | 邻居均值+**min reduction** | — | TTA+加权平均 |
| 推理 | OpenVINO CPU（18 分钟/模型） | CPU 约束 | OpenVINO |
| 私榜 | 1st | 3rd | 0.667（4th） |

## 3. 共识、分歧与裁决

### 共识一：log-mel 图像 CNN + 声景伪标是标准骨架（3/3）

1st 用分类器清洗+PL；3rd 两级伪标+蒸馏；4th melspec/raw 集成。**裁决**：unlabeled soundscapes 的伪标是核心数据杠杆；第一级可以用大模型，部署级要精简。置信度：高。

### 共识二：CPU 推理约束是隐藏设计维度（1st/3rd/4th）

提交只能用 CPU：1st 用 OpenVINO+缓存把单模型压到 18 分钟；3rd 明确"第一级可用大模型、第二级必须小"；4th 用 OpenVINO+TTA。**裁决**：模型选型先过 CPU 预算，再谈精度。置信度：高。

### 共识三：类不平衡/低频类要专门处理（3rd/1st）

3rd：封顶 500/物种 + 低频上采样 ≥10；1st：183 nocall 类（私榜 +0.016）。**裁决**：长尾声景赛中，采样策略与 nocall 类是独立增益模块。置信度：中高。

### 分歧一：额外数据是否使用

1st："最佳方案是不用额外数据"（尝试过过滤/分位筛选均无效）；3rd 用 Xeno+往年数据并封顶/取最近；社区还有专门的"Additional Xeno samples"帖（85 票）。**裁决**：额外数据的价值取决于清洗与配比；不受控地加入会伤害（1st 实证），受控封顶+最近优先可行（3rd）。置信度：中高。

### 分歧二：CE vs BCE

1st：CE 明显更好（182 类几乎单标签 → 多分类问题；推理再 sigmoid）；3rd/4th 系多标签 BCE/SED。**裁决**：标签结构与训练配比决定损失选择；1st 的"CE 训练 + sigmoid 推理 + min()"是自洽的降噪组合。置信度：中高。

### 共识四/事件：CV-LB gap（52 票帖）

1st 的 fold 统计发现（fold0 更"安静"）说明 CV 划分与音频响度相关；社区专门讨论 CV-LB gap。**裁决**：声景赛要按"响度/站点/记录者"审计折划分，不能只随机分。置信度：中高。

## 4. 证据分级

| 断言 | 等级 | 说明 |
| --- | --- | --- |
| 1st 的数据清洗/折设计/推理链 | 自述 + 图 + 公开代码 | 中高 |
| 3rd 的两级伪标/蒸馏/封顶 | 自述 + 代码 | 中高 |
| 4th 的 melspec+raw 集成与 TTA 分数 | 自述 + 表格 + 代码 | 中高 |
| fold0 统计异常 | 自述 + 图 | 中 |
| 183 nocall 私榜增益 | 自述（0.655→0.671） | 中高 |

## 5. 悬案与缺口（登记）

- 2nd/5th 未细读；"Compare BirdCLEF 2023 vs 2024"（67 票）与内存优化帖（58 票）未入库。
- 1st 的 min() reduction 机制只有直觉解释（降低不确定预测），缺消融数字。
- 额外数据的"清洗到什么程度才安全"无统一定论。

## 6. 图表证据

![1st 的集成推理流程](../../intel/birdclef-2024/bodies/512197_img/03.png)

**图 1**（topic 512197）：EffNet_b0×3 与 RegNetY_008×3 各自对 5 个相邻 chunk（n−2..n+2）sigmoid 后取 mean，再跨模型 **min()**，最后 mean() 输出。**"邻居平均 + 最小值降噪"的后处理设计**。

## 7. 出处

- 4th Cerberus（511845）：https://www.kaggle.com/competitions/birdclef-2024/discussion/511845
- 2nd（512340）：https://www.kaggle.com/competitions/birdclef-2024/discussion/512340
- 1st（107 票）：https://www.kaggle.com/competitions/birdclef-2024/discussion/512197
- 3rd（78 票）：https://www.kaggle.com/competitions/birdclef-2024/discussion/511905
- 5th（57 票）：https://www.kaggle.com/competitions/birdclef-2024/discussion/511535
- Xeno 补充数据（85 票）：https://www.kaggle.com/competitions/birdclef-2024/discussion/491687
