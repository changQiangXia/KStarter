# Playground Series S6E6 - 天体分类（Balanced Accuracy，私榜大逆转）

> 主题：tabular ｜ 子类：— ｜ 领域：天文（合成数据） ｜ 类别：Playground
> 截止：2026-06-30 ｜ 队伍数：2816 ｜ 机制：标准赛 ｜ 指标：Balanced Accuracy
> 数据来源：`intel/playground-series-s6e6/`（78 条主题索引 + 6 篇 write-up 正文）

## 1. 任务与数据

- 预测目标：天体三分类（恒星/星系/类星体等），Balanced Accuracy；合成数据 + 原数据。
- 数据特性：原数据被删除了部分特征，而竞赛数据**额外增加了合成后的派生特征** `spectral_type` 与 `galaxy_population`——社区发现它们是简单阈值化的结果：`spectral_type = cut(r−g, [−∞,−1,−0.5,0,∞])`、`galaxy_population = cut(u−r, [−∞,2.2,∞])`。还原公式后即可对原数据套用同样变换再合并。
- 赛道生态：本场公开榜被"盲目 blender"大量污染——**公开榜 0.97200 是 CV 框架的天花板，超过它基本只有探榜/拟合公开榜**。

## 2. 验证方案

- 1st 的策略宣言：两周后当盲 blender 开始冲榜，他给自己定的目标不是追榜，而是**守 CV 与 CV–LB 一致性**，接受公开榜下滑；最终从公开第 344 名逆转到私榜第 1。
- 6th（参赛第二场）：92 模型 OOF 概率栈爬到"OOF 平台"后**只做实验不做更换**——"trusting the OOF plateau"；OOF 0.970718 对应私榜 0.97054。
- 1st 的集成规模纪律：模型数涨到 100+ 后性能反而下降，回退到 ~49 与 ~78 两个版本；两版 LR-Logits 公开 0.97179，MLP 版 CV 最高（0.970598）但公开只有 0.97172——**最终靠 CV 选了 MLP，正是它夺冠**。

## 3. 模型家族

| 方案 | 使用者层次 | 关键点 | 出处 |
| --- | --- | --- | --- |
| 49/78 模型 LR-Logits + 89 模型 MLP，按 CV 定稿 | 1st | 拒接盲 blend；344→1 | topic 717510 |
| 92 模型 OOF 概率栈（含 24 个 RealMLP 系） | 6th | OOF 平台即停止堆叠 | topic 716945 |
| 8th / 25th 公开起点 | 社区 | 快速复用往届三分类代码 | topic 716756 |

## 4. 关键技巧

- **派生特征公式逆向**：`spectral_type`/`galaxy_population` 是对 (r−g)/(u−r) 的阈值切分——还原后原数据才能与竞赛数据对齐合并（否则两套特征不一致无法拼行）。
- **AUC/BA 类指标的集成器选型**：本场 LR-Logits 与 MLP 集成器最好（AutoGluon/XGB 等次之）；且 MLP 集成器 CV 更高、LB 更低——最终证明 CV 判断正确。
- **集成规模存在甜点区**（约 49–90 个），超过后性能退化；"回退到较早版本再向前加"是有效策略。
- 对盲 blend 的免疫：公开榜 >0.97200 的分数与 CV 框架不符时，直接无视，不进入候选池。

## 5. 可迁移性评估

- **可直接迁移**：派生特征阈值公式还原（任何"原数据缺特征/竞赛数据多特征"的合成赛）；集成器选型对照（LR-Logits/MLP）；集成规模甜点区探测；公开榜异常检测（CV 框架上限之外的分数视为污染）。
- **需要前提**：有 CV–LB 一致性的度量习惯；能抵抗追榜冲动。
- **不建议照搬**：盲 blend 高分 notebook（本场大清洗）；无限扩池。

## 6. 对新手的关键启示

- "公开榜 344 → 私榜 1"不是运气：它是**守住 CV 纪律**的直接结果——本场对"要不要追榜"给出了最贵的学费样本。
- 集成不是越多越好：找到自己的甜点区，超过就回退。
- 合成数据的"多出来的列"往往是可逆向的：先验证是不是对已有列的确定性变换。

## 7. 出处

- 1st：Mission 300+（344→1 的纪律复盘）：https://www.kaggle.com/competitions/playground-series-s6e6/discussion/717510
- 6th：Trusting The OOF Plateau：https://www.kaggle.com/competitions/playground-series-s6e6/discussion/716945
- 派生特征公式（spectral_type / galaxy_population）：https://www.kaggle.com/competitions/playground-series-s6e6/discussion/703535
