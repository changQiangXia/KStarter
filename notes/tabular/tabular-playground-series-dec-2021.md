# Tabular Playground Series - Dec 2021（森林覆盖类型，Accuracy，特征修复与软投票）

> 主题：tabular ｜ 子类：— ｜ 领域：地理/林业（合成数据） ｜ 类别：Playground
> 截止：2021-12-31 ｜ 队伍数：1188 ｜ 机制：标准赛 ｜ 指标：Categorization Accuracy
> 数据来源：`intel/tabular-playground-series-dec-2021/`（80 条主题索引 + 6 篇 write-up 正文）

## 1. 任务与数据

- 预测目标：森林覆盖类型（多分类 Accuracy）；字段为地形/土壤/光照类地理特征。
- **数据修复机会**（社区爆款帖）：`Aspect`（方位角）出现 <0 或 >359 的越界值（应为 0–359 循环量）→ 加减 360 修正；三个 `Hillshade`（山体阴影灰度）出现越界值 → 按物理含义截断到 [0, 255]。**仅修复这四列即显著提分**。
- 其它领域约束：某些树种不可能长在某些土壤上（土壤掩码的动机），但社区实测"硬靠拢原数据"反而过拟合。

## 2. 验证方案

- 2nd 的复盘：把竞赛数据"改得更像原数据"的尝试在 CV 上极好但测试失败（过拟合原数据）；最终只有欧氏/曼哈顿距离特征与 Aspect 修复幸存。
- 软投票（10 个最优模型）+ 同架构不同 batch_size 再投票是两次突破点。

## 3. 模型家族

| 方案 | 使用者层次 | 关键点 | 出处 |
| --- | --- | --- | --- |
| 特征修复 + 距离特征 + 同架构多 batch 软投票 | 2nd | 伪标签实测无效 | topic 298304 |
| 四列越界值修复 | 社区 | 最大单点增益 | topic 293373 |
| 2021 年 TPS 教训合集 / focal loss | 社区 | 经验与不平衡处理 | topic 296842、293072 |

## 4. 关键技巧

- **越界值修复 = 最便宜的提分**：先核对每列的物理范围（角度 0–359、灰度 0–255），修正循环量与截断异常——无需建模改动。
- 软投票 + 同架构扰动（batch_size 等）制造多样性；SeLU 网络在作者手中意外地强。
- 2nd 的真实叙事：公开 notebook 被大量复制的"马戏团"现象 → 最终选择"融合自己最优 + 他人已验证结果"的务实路线（并剔除其中的伪标签成分）。

## 5. 可迁移性评估

- **可直接迁移**：字段物理范围核对与修复清单；距离类特征（对地理数据）；同架构扰动软投票；"CV 极好但 LB 崩"作为过拟合原数据的警报。
- **需要前提**：领域字段有明确的物理范围；多模型存档。
- **不建议照搬**：把"改得像原数据"当目标（本场实测失败）；对伪标签的盲目跟风（2nd 实测无效）。

## 6. 对新手的关键启示

- 建模前先做"物理范围审计"：角度、灰度、比例类字段的越界值修一修就可能白捡分数。
- 领域约束（土壤-树种）要用在**模型/验证设计**里，而不是硬改数据去迎合原分布。
- 公开 notebook 泛滥时，把精力放在"自己最优 + 已验证成果的稳健融合"。

## 7. 出处

- 2nd：特征修复、距离与软投票全记录：https://www.kaggle.com/competitions/tabular-playground-series-dec-2021/discussion/298304
- 修复四列特征的爆款帖：https://www.kaggle.com/competitions/tabular-playground-series-dec-2021/discussion/293373
- 2021 TPS 教训合集：https://www.kaggle.com/competitions/tabular-playground-series-dec-2021/discussion/296842
- Focal loss 处理不平衡：https://www.kaggle.com/competitions/tabular-playground-series-dec-2021/discussion/293072
