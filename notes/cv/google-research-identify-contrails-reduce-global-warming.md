# Google Research - Identify Contrails to Reduce Global Warming

> 主题：cv ｜ 子类：— ｜ 领域：气候/遥感 ｜ 类别：Research
> 截止：2023-08-09 ｜ 队伍数：954 ｜ 机制：代码赛 ｜ 指标：Dice（凝结尾迹分割）
> 数据来源：`intel/google-research-identify-contrails-reduce-global-warming/`（80 条主题索引 + 6 篇 write-up 正文）

## 1. 任务与数据

- 预测目标：由卫星图像序列分割**飞机凝结尾迹（contrails）**，用于减少航空对气候的影响。
- 数据形态：**多通道卫星图像序列**（时间维度）+ 掩码。
- 构造陷阱：
  - **几何增强会破坏标签**（掩码有方向性偏移）→ 2nd 明确**禁用翻转与 90° 旋转增强与 TTA**；
  - 序列信息重要（凝结尾迹随时间演化）；
  - 像素级精度决定得分。

## 2. 方案谱系

| 方案 | 名次 | 关键点 |
| --- | --- | --- |
| **定制 U 形网络 + 多骨干**（CoaT / NeXtViT / SAM-B / EfficientNetV2-S）+ 时序混合（LSTM/Transformer/卷积） | 2nd | 上采样×2/×4 提升像素精度；**禁用翻转/旋转增强与 TTA**（因为掩码有方向偏移）；**软标签训练**（多标注平均） |

## 3. 关键技巧

- **几何增强要检查标签一致性**（本场直接禁用——这是"增强策略按任务定制"的又一例证）。
- **时序建模**（LSTM/Transformer/卷积混合）捕捉凝结尾迹演化。
- **软标签**（多标注者平均）缓解边界噪声。
- **像素级精度**通过上采样策略优化。

## 4. 可迁移性评估

- **可直接迁移**：
  - **增强前先验证标签的几何一致性**（本场禁用翻转/旋转是正确决策）；
  - 多骨干 U 形网络 + 时序模块；
  - 软标签处理标注歧义。
- 需要前提：遥感/序列分割能力。
- 不建议照搬：默认使用全套几何增强。

## 5. 对新手的关键启示

1. **"标准增强"可能有害**——先验证标签在几何变换下是否仍成立。
2. 遥感/气候类任务是 Kaggle 的稳定方向（Google Research 系列）。
3. 与 HuBMAP/HMS 对照：**软标签是处理标注歧义的通用手段**。

## 6. 轻读结论（2026-10 补）

**一句话**：本场的"元问题"是**标签相对影像偏移 0.5 像素**——识别它的队伍解锁 flip/rot90 增强与 TTA（+0.005~0.01），没识别的被锁死；其余是细线分割的分辨率与阈值工程。

- 1st（430618）：用"180° 旋转后蓝图-绿-红条纹"诊断出右下 0.5px 偏移；y_sym 训练 + 小卷积映射回原标签 + 8 模式 TTA；4 帧拼图（1024²）替代训不起来的 3D/ConvLSTM；集成 priv 0.724。
- 2nd（111 票）：软标签 + 输入 ×2/×4 上采样 + pixel shuffle；时序只在 res/32、res/16 混合（LSTM 最佳，+0.01）；CoaT 最佳单模 0.71790 priv；dice-Lovasz 拓宽阈值最优区间；指出标准 K 折因瓦片重叠高估 CV。
- 3rd（430685）：2.5D U-Net 把 3D 卷积插到 skip 各层（+0.02）；百分位阈值（≈0.16% 正像素比）；最终因加入全量 flip/TTA 版本，与第 2 名只差 0.00001。
- 5th/9th：分别独立标定出偏移量（x=0.408/y=0.453）与成因（多边形转掩码左右边界规则）。

**裁决**：先做"几何一致性审计"再谈增强；细结构任务用分辨率/解码上采样换精度；阈值要抗漂移（百分位/宽最优区间）；伪标签提升单模但常被集成同质化抵消。

**悬案**：4th/6th–8th 方案缺失；3rd 最后一天掉分只有一句解释；CV-LB 线程未细读。

## 7. 图表证据

![1st 的错位诊断](../../intel/google-research-identify-contrails-reduce-global-warming/bodies/430618_img/01.png)

**图 1**（topic 430618）：旋转 180° 输入的预测 vs 原标签出现"蓝-绿-红"条纹，证明标签相对影像向下偏移——本场所有"增强失效"现象的根源。

## 8. 出处

- 讨论区索引：`intel/google-research-identify-contrails-reduce-global-warming/topics.md`（80 条）
- 已收录 write-up（6 篇）：
  - 1st（164 票）：https://www.kaggle.com/competitions/google-research-identify-contrails-reduce-global-warming/discussion/430618
  - 2nd 定制 U 形网络（111 票）：https://www.kaggle.com/competitions/google-research-identify-contrails-reduce-global-warming/discussion/430491
  - 9th（76 票）：https://www.kaggle.com/competitions/google-research-identify-contrails-reduce-global-warming/discussion/430479
  - 3rd（48 票，2.5D U-Net）：https://www.kaggle.com/competitions/google-research-identify-contrails-reduce-global-warming/discussion/430685
  - 5th（41 票，最佳单模）：https://www.kaggle.com/competitions/google-research-identify-contrails-reduce-global-warming/discussion/430549
- 轻读全本：`analysis/deep/google-research-identify-contrails-reduce-global-warming.md`（Tier B 轻读：对照矩阵/裁决/证据分级/悬案 + 3 图证）
