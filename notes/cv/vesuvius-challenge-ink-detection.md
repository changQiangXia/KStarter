# Vesuvius Challenge - Ink Detection

> 主题：cv ｜ 子类：— ｜ 领域：文化遗产/3D 成像 ｜ 类别：Featured
> 截止：2023-06-14 ｜ 队伍数：1249 ｜ 机制：代码赛 ｜ 指标：F0.5（像素级）
> 数据来源：`intel/vesuvius-challenge-ink-detection/`（80 条主题索引 + 6 篇 write-up 正文）

## 1. 任务与数据

- 预测目标：在**碳化卷轴的 3D X 射线 CT 扫描**中检测墨迹（像素级分割）。
- 数据形态：大体积 3D 体数据 + 表面纹理；正样本极稀疏。
- 构造陷阱：
  - 数据量大、显存受限 → 必须切块（crop）训练；
  - **测试集存在旋转等几何差异**（6th 明确提到），需要对应增强；
  - 公开榜样本少 → 榜分波动大，1st 明确表示"全程打得很保守，避免过拟合榜单"。

## 2. 方案谱系

| 方案 | 名次 | 关键点 |
| --- | --- | --- |
| 大尺寸切块 + **深度不变（depth-invariant）模型** + 多模型平均 + 验证后全量训练 | 1st | 把成功主要归因于这四点；强调多模型平均带来的**校准改善** |
| EfficientNet + SegFormer 集成 + 旋转增强 | 6th | 观察到测试数据被旋转，据此做图像旋转处理；首次尝试分割任务即拿 solo 金 |
| 其他方案 | 2nd | 见讨论区 |

## 3. 关键技巧

- **大 crop 训练**：上下文越大，墨迹判别越稳（切块尺寸是主要超参）。
- **深度不变性**：3D 体数据中沿深度方向的纹理变化需要被显式处理。
- **多模型平均改善校准**：不只是提分，还降低阈值敏感性。
- **几何增强对齐测试条件**（旋转）。
- **验证后再全量训练**：稳健的常规收尾动作。

## 4. 可迁移性评估

- **可直接迁移**：
  - 大体积数据用**大切块 + 充分上下文**；
  - 几何增强要与测试集的形变对齐（旋转/翻转）；
  - 多模型平均的价值之一是**校准**（对稀疏正样本的阈值任务尤其重要）；
  - "验证通过后全量重训"是标准收尾。
- 需要前提：3D 数据处理与显存管理能力。
- 不建议照搬：直接整卷训练（显存不够）。

## 5. 对新手的关键启示

1. **切块尺寸是被低估的超参**。
2. **测试集有几何差异时，先做几何增强**。
3. 稀疏任务里，**校准比排序更重要**。

## 6. 出处

- 讨论区索引：`intel/vesuvius-challenge-ink-detection/topics.md`（80 条）
- 已收录 write-up（6 篇）：
  - 1st（112 票）：https://www.kaggle.com/competitions/vesuvius-challenge-ink-detection/discussion/417496
  - 2nd（76 票）：https://www.kaggle.com/competitions/vesuvius-challenge-ink-detection/discussion/417255
  - 6th（84 票）：https://www.kaggle.com/competitions/vesuvius-challenge-ink-detection/discussion/417274
