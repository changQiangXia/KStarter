# PetFinder.my - Pawpularity Contest

> 主题：cv ｜ 子类：— ｜ 领域：动物图像 ｜ 类别：Research
> 截止：2022-01-14 ｜ 队伍数：3537 ｜ 机制：代码赛 ｜ 指标：RMSE（回归 1–100 分）
> 数据来源：`intel/petfinder-pawpularity-score/`（120 条主题索引 + 8 篇 write-up 正文）

## 1. 任务与数据

- **预测目标**：由宠物照片（+ 少量元数据）回归预测"可爱度/Pawpularity"分数。
- **先立锚**：训练目标均值 38.04、标准差 20.59——**全预测 38.04 的 RMSE=20.59**，任何低于它的模型才算有预测力；前排模型在 16.9–17.9 之间。
- **数据形态**：9912 张训练图 + 约 6800 张测试图；目标由官方"cuteness meter"生成，机制未公开 → 存在**标注噪声上限**。
- **构造陷阱**：目标主观、元数据弱、RMSE 对离群样本敏感（少数"rare object"样本可毁掉一个提交）。

## 2. 验证方案

| 方案 | 使用者 | 说明 |
| --- | --- | --- |
| K 折 + 多模型平均 | 多数 | 数据量小，折数不宜过多 |
| **重复图分组** | Public1st/5th | 同图/近图分到同一折（GroupKFold 加重复组 id；或先删重复再分层） |
| CV 口径 | 18th | **用 OOF 的 RMSE**，而非各折 RMSE 的均值（后者偏乐观） |
| 最佳 CV vs 最佳 LB 双轨 | 6th | 两个集成分别维护；最佳 CV 提交公开仅第 120 名、私榜第 6 |

## 3. 方案谱系

| 方案 | 名次 | 关键点 |
| --- | --- | --- |
| SVR 特征堆叠（575 预训练模型 → 爬山前向选择）+ 5×DL 集成 | 1st | **完全弃用元数据**；三套 SVR 特征集 A/B/C（CV 16.997–17.148），集成私榜 **16.95**；top-1k 分类头特征优于内部嵌入；目标 clip@85 小增益 |
| 多任务学习（猫/狗标签当辅助输出） | 6th | **自带元数据输入无效、当辅助输出也无效（12 列）；猫/狗标签辅助有效**；等权爬山日均加一模；最佳 CV 集成私榜 **16.90** |
| 14 单模 + 近重复检测 + 往届元数据后处理 | Public1st/Private5th | EffNetB0 嵌入 + 余弦相似度找同图；对阈值以上用往届比赛元数据，按 AdoptionSpeed 分组建后处理模型 |
| 单 Swin-Large 10 折 + 序数回归头 | 18th | CV 17.25（OOF 口径）；往届伪标签仅微弱改善 |
| 纯图像回归（丢弃元数据） | — | 1st 的结论被多队复现：图像信号 >> 元数据 |
| 图像训练技巧汇总（293 票） | 通用 | 增强/初始化/调度/label smoothing/MixUp/KD 清单 |

## 4. 关键技巧

- **图像增强完整配方**（293 票帖）：随机长宽比裁剪（3/4–4/3）→ 随机面积采样（8%–100%）→ 缩放；水平翻转；HSV 抖动；测试时保持长宽比、短边缩放后中心裁剪。
- **元数据三态**：输入（本场最弱）→ 辅助输出（取决于标签质量：猫/狗 ✅、自带 12 列 ❌）→ 后处理（仅对近重复样本用往届元数据 ✅）。
- **分类头当特征提取器**：timm 的 ImageNet-1k **头部输出**（1000 维）优于内部嵌入——细粒度（猫狗品种类目）与任务对齐。
- **BCE 当回归损失**：社区主流（1st/6th 均用）；与"目标有界 + 抗离群"的直觉一致；18th 用序数头同样进前列 → 损失与模型家族耦合。
- **近重复检测**：EffNetB0 嵌入 + 余弦相似度找完全/近似重复图；既是验证分组依据，也是跨届元数据利用的入口。
- **小信号回归的评估纪律**：先算均值锚；CV 写清口径；RMSE 尾部样本单独关注；名次带宽大（CV 最佳 vs LB 最佳可差百余位）。
- **负结果**：伪标签外部图像（6th ❌）；往届数据全量预训练/特征（6th ❌）；自带元数据多任务（6th ❌）。

## 5. 深读结论（2026-10 补）

- 本场是"**冻结特征 + 线性头**"的胜利：SVR-on-头部特征（16.9 级）胜过纯端到端 DL（17.38–17.75）；在提交 9h 限制下，SVR 部分占 ~4h，融合规模被推理时限硬约束。
- 元数据三态裁决：**输入 < 辅助输出 < 后处理（仅近重复）**；辅助输出的增益由标签质量决定。
- 名次噪声：最佳 CV 提交（私榜 6）公开仅 120 名——小信号任务里"信 CV"要配合对噪声带宽的清醒认识。

## 6. 图表证据

**图 1：多任务两种用法（元数据当输入 vs 当辅助输出）**（6th，topic 301015）——`intel/petfinder-pawpularity-score/bodies/301015_img/04.png`

![multitask](../../intel/petfinder-pawpularity-score/bodies/301015_img/04.png)

**图 2：Squish vs Crop 预处理对照**（6th，topic 301015）——`.../301015_img/02.png`

![preprocess](../../intel/petfinder-pawpularity-score/bodies/301015_img/02.png)

*读图*：Squish 扭曲长宽比；Crop 保持自然比例且训练期随机裁剪自带增强（6th 实测 Crop 提升 CV/LB）。

## 7. 可迁移性评估

- **可直接迁移**：
  - 图像增强配方（长宽比裁剪 + 面积采样 + HSV 抖动）几乎适用于所有视觉任务。
  - "先立均值锚"与"CV 口径写清楚"适用于一切回归任务。
  - "冻结特征 + 线性头"（SVR/Ridge）在小数据视觉任务上常常打败端到端微调。
  - 元数据三态决策顺序（先试后处理、再辅助输出、最后输入）。
- **需要前提**：
  - 预训练视觉骨干（timm/CLIP）；cuML 等加速件（SVR 爬山搜索需要数千次拟合）。
  - 跨届重叠是"往届元数据后处理"的前提。
- **不建议照搬**：
  - 直接把元数据拼进特征；在无重叠时混训往届数据（6th 实测无益）。

## 8. 对新手的关键启示

1. **先算"什么都不做的分数"**：本场 20.59 的均值锚告诉你 17 分的意义与噪声带宽。
2. **多余的特征不一定有用**：冠军主动删掉全部元数据；要做多任务，就选强语义标签（猫/狗）。
3. **增强策略值得单独学习**（293 票帖可当视觉任务清单）。
4. **CV 与名次都带噪声**：最佳 CV 提交可能公开排 120、私榜第 6——别被单次榜单位次带偏。

## 9. 出处

- 讨论区索引：`intel/petfinder-pawpularity-score/topics.md`（120 条）
- 已收录 write-up（8 篇）：
  - 1st 全文（329 票）：https://www.kaggle.com/competitions/petfinder-pawpularity-score/discussion/301686
  - 1st 占位帖（274 票）：https://www.kaggle.com/competitions/petfinder-pawpularity-score/discussion/300938
  - 图像技巧汇总（293 票）：https://www.kaggle.com/competitions/petfinder-pawpularity-score/discussion/288896
  - 6th 多任务（164 票）：https://www.kaggle.com/competitions/petfinder-pawpularity-score/discussion/301015
  - Public1st/Private5th：https://www.kaggle.com/competitions/petfinder-pawpularity-score/discussion/300928
  - 18th 单 Swin（91 票）：https://www.kaggle.com/competitions/petfinder-pawpularity-score/discussion/300942
