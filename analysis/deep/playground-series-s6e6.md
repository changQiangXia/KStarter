# Playground Series S6E6 轻量深读（Tier B）

> 赛事：Playground ｜ 主题 tabular（天文三分类，合成数据）｜ 2816 队 ｜ 标准赛 ｜ 指标：Balanced Accuracy（BA）
> 材料基础：`digests/playground-series-s6e6.md`（6 篇正文：1st 717510 / 6th 716945 / 8th 716756 / 25th 716748 / 派生特征公式 703535 / TabPFN-3 基线 703686；78 条主题索引）+ 0 张归档图
> 轻读时间：2026-10（Tier B B05）

## 1. 一句话重述与数字账

天体（恒星/星系/类星体）三分类，BA 指标 + 合成数据。真正的考点是**对抗公开榜污染（盲 blend/LB probing）的 CV 纪律 + 用合适的替代指标（加权 log-loss）替代高噪声的 BA + 集成规模甜点区**；本场 1st 从公开榜第 344 逆转到私榜第 1。

| 关键数字 | 值 | 来源 |
| --- | --- | --- |
| 1st（717510，31 票） | 中途最好 CV 0.970506 / LB 0.97171（49 模型）；判断"CV 框架天花板 ≈ LB 0.97200"，超过者基本是盲 blend/probing；**模型数涨到 100+ 后性能反而下降**，回退到 ~49/~78 版本再往上加；集成器以 **LR-Logits 与 MLP 最好**（AutoGluon/XGB/CatBoost 次之）；LR-Logits 两版公开均 0.97179；**MLP 版 CV 最高 0.970598（89 模型）但公开仅 0.97172 → 按 CV 选它，夺冠**；单模最强是 CatBoost（cdeotte CAT-v3 + 自研 FE/HP）；覆盖 XGB/LGBM/CatBoost/RealMLP/TabM/ET/HGB/RF/YDF/FT-Transformer/TabNet + AutoGluon/LightAutoML/FLAML/PyTabKit；FE 200–400 列 | 1st |
| 6th（716945，17 票） | **92 模型 OOF 概率栈**：OOF 0.970718 / pub 0.97130 / priv 0.97054；池内最强单成员是公开 OOF stacker（0.970350）→ 堆叠增益真实但很小；家族构成：RealMLP 24、XGB 19、CatBoost 12、LGBM 5、公开 artifact 17+、FM/FT/TabM/TabPFN 若干；工作流 = "公开 notebook/想法 → 本地 OOF 复现 → 注册预测 → 测增益 → 保留或记录死因"（Codex 承担编码/检索循环） | 6th |
| 8th（716756） | **用加权 log-loss 取代 BA 做 CV**：证明加权 log-loss 的最优解 argmax 与 BA 最优决策一致（`argmax_c η_c(x)/π_c`），且是严格 proper scoring rule、可微、低方差；对不支持样本权重的模型（RealMLP/TabPFN）用**预测除以先验**（[0.653818, 0.202899, 0.143283]）做后验校正；判断"公榜前 100 全在过拟合"，整场只看 CV | 8th |
| 25th（716748，26 票） | 公开起步 notebook（19 模型：XGB/RealMLP/TabM/CatBoost/TabICLv2/LGBM/logreg/FT-Transformer/DCN）CV 0.97028 / pub 0.97101 / priv 0.97024（rank 45）；**Codex 建议并实现两处升级**（TabICLv2 改为微调 + 新增 OVR CatBoost）→ 20 模型 CV 0.97045 / pub 0.97094 / priv 0.97033（rank 25） | 25th |
| 派生特征 | `spectral_type = cut(r−g, [−∞,−1,−0.5,0,∞])`、`galaxy_population = cut(u−r, [−∞,2.2,∞])`——还原公式后原数据才能与合成数据对齐合并 | 703535 |
| 其他 | TabPFN-3 基线 LB 0.964（21 票）；GPU LR stacker 模板（35 票）；"单模型 or 集成"讨论（33 票） | 社区 |

## 2. 逐方案对照矩阵

| 维度 | 1st | 6th | 8th | 25th |
| --- | --- | --- | --- | --- |
| 规模 | 49/78/89 模型两版决赛 | 92 模型 OOF 栈 | 未强调规模（重指标设计） | 19→20 模型 |
| CV 指标 | BA（+CV-LB 一致性判断） | BA/OOF 平台 | **加权 log-loss** | BA |
| 集成器 | LR-Logits / MLP | 概率栈（OOF 特征） | — | notebook 集成 |
| 关键纪律 | 拒盲 blend、集成甜点区、按 CV 定稿 | 平台即止、死因留档 | 只看 CV、先验校正 | 复用公开起点 + 定点升级 |
| 结果 | priv #1（pub 344） | priv 0.97054 | 8th | priv 0.97033（rank 25） |

## 3. 共识、分歧与裁决

### 共识一：公开榜被盲 blend/LB probing 污染，必须锚定 CV（1st/6th/8th）

1st 观察到公榜分数快速越过其 CV 框架上限（0.97200），据此判定高分多为拟合公榜；8th 直接判定"公榜前 100 全过拟合"；6th 全程以本地 OOF 为筛选器。**裁决**：当"CV 上限"与"公榜高分"系统性冲突时，采用 CV/一致性纪律的队伍会在私榜收获（本场 344→1、以及 25th 的 pub 降而 priv 升）。置信度：高（多队 + 榜面后果）。

### 共识二：BA 是高噪声指标，需要降噪替代（8th 的贡献）

8th 给出推导：加权 log-loss 的总体最优解与 BA 最优决策同一点（除先验），且 BA 只依赖 argmax、分段常数、对近界样本极敏感。**裁决**：分类赛若指标是 accuracy/BA/F1 类，用对应的 proper scoring rule（加权 log-loss）做模型选择，最后一步再取 argmax。置信度：高（有数学证明 + 全部队伍都受榜面噪声影响的事实）。

### 共识三：集成存在甜点区（1st/6th）

1st：模型数 100+ 后性能退化，回退再增；6th：92 模型栈相对最强单成员仅 +0.00037 OOF。**裁决**：堆叠的边际收益很小且会转负，纪律（何时停）比继续加模型更值钱。置信度：中高。

### 分歧一：CV 用什么指标

1st/6th 直接用 BA 相关的 OOF 分数；8th 改用加权 log-loss。**裁决**：两者在本场结论一致（都靠 CV 赢），但加权 log-loss 提供更细的梯度信号与更低的估计方差——样本少/近界多时优先。置信度：中高。

### 分歧二：公开 artifact 用不用

6th/25th 大量使用公开 notebook 的预测与配方（但都过本地 OOF 检验）；1st 明确拒绝"盲 blend 公开高分"进入候选池。**裁决**：区分"公开方法/配方"（可复用）与"公开高分概率面"（可能是 probing 产物，须经 CV 验证）。置信度：高。

### 事件：合成数据的可逆特征

社区逆出两个阈值公式（r−g 与 u−r 的分箱），使原始 SDSS 数据能与合成数据对齐合并——25th 的多个模型都利用了"附加原始行 + 低权重"。**裁决**：合成赛先检查"多出来的列"是否为确定性变换，可逆则直接还原并对齐原数据。置信度：高。

## 4. 证据分级

| 断言 | 等级 | 说明 |
| --- | --- | --- |
| 1st 的 344→1、集成甜点区、CV 定稿 | 自述 + 完整分数 | 高（结果可查） |
| 8th 的加权 log-loss 等价性推导 | 数学证明（自洽，可独立复核） | 高（理论）/中（实践增益未单独量化） |
| 6th 的 92 模型构成与 OOF 0.970718 | 自述 + 家族表 | 中高 |
| 25th 的 Codex 两处升级 +0.00009 priv | 自述 + 前后对比 | 中 |
| 派生特征公式 | 社区帖 + 众队复现 | 高 |

## 5. 悬案与缺口（登记）

- 2nd–5th 与 7th 的方案未入库；"Single Model or Ensemble?"（33 票）与"Blending Topic"（27 票）未细读；
- 1st 的 78 模型版 CV 数字在原文写作中疑似笔误（0.97573），无法据以复算；
- **图证缺口**：本场 0 张归档图（原帖无内嵌图或未归档），按规则不内嵌。

## 6. 图表证据

无可用图证（本场归档 0 图）。核心证据为分数表与数学推导，已在正文引用。

## 7. 出处

- 1st（31 票）：https://www.kaggle.com/competitions/playground-series-s6e6/discussion/717510
- 6th（17 票）：https://www.kaggle.com/competitions/playground-series-s6e6/discussion/716945
- 8th（28 票）：https://www.kaggle.com/competitions/playground-series-s6e6/discussion/716756
- 25th（26 票）：https://www.kaggle.com/competitions/playground-series-s6e6/discussion/716748
- 派生特征公式（47 票）：https://www.kaggle.com/competitions/playground-series-s6e6/discussion/703535
- GPU LR stacker 模板（35 票）：https://www.kaggle.com/competitions/playground-series-s6e6/discussion/704014
- TabPFN-3 基线（21 票）：https://www.kaggle.com/competitions/playground-series-s6e6/discussion/703686
