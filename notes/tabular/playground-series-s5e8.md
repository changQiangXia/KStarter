# Playground Series S5E8 - 燃油效率预测（AUC）

> 主题：tabular ｜ 子类：— ｜ 领域：汽车（合成数据） ｜ 类别：Playground
> 截止：2025-08-31 ｜ 队伍数：3365 ｜ 机制：标准赛 ｜ 指标：ROC AUC
> 数据来源：`intel/playground-series-s5e8/`（80 条主题索引 + 6 篇 write-up 正文）

## 1. 任务与数据

- 预测目标：二分类 AUC；数据规模较大（本场对显存管理提出了实战要求）。
- 竞争形态：分数带极密（1st 公开 0.97844、私榜 0.97801），平台期长达一周以上——"谁的档案库更厚、定稿更稳"决定名次。

## 2. 验证方案

- 1st：CV–LB 对应关系良好 → 后段决策主要信 CV；但在最后期限前没有提交机会验证的新技巧（CatBoost baseline）仍靠 CV 下注。
- 2nd：与 S5E6 相同的流程——生成大量**异质** OOF（不同模型 > 同模型不同超参），缓慢入池。
- 3rd：OOF 堆叠 + AutoGluon。

## 3. 模型家族

| 方案 | 使用者层次 | 关键点 | 出处 |
| --- | --- | --- | --- |
| 136 个 OOF 的大杂烩 + AutoGluon 集成 | 1st | 弱模型（RF/KNN/GOSS/DART）贡献多样性；平台期后靠"新表示"破局 | topic 603210 |
| 异质 OOF 池 + 简单加权 | 2nd | 复用 S5E6 流程 | topic 603297 |
| OOF 堆叠 + AutoGluon | 3rd | 社区标准配方 | topic 603198 |

## 4. 关键技巧

- **XGBoost QuantileDMatrix 显存技巧**（可复用的工程资产）：按批压缩为直方图（默认 256 bin → 1 字节/值），配合 float32/int32 降精度 + 磁盘数据加载器，可在 16GB 显存训练 15GB+ 数据（约 4–8 倍容量）。pandas/cuDF 默认 int64/float64 是浪费。
- **CatBoost/LGBM/XGB 的 baseline 参数**（1st 最后一天才用上）：把另一模型的预测当初始 margin 再学残差——低分模型也能被提升；与 S4E10/S5E10 的结论互相印证。
- **NNE（神经网络集成器）**（1st 赛后复盘）：用 5 折 NN 当 L3 集成器 + 爬山，效果超过跑了 12 小时的 AutoGluon，且耗时约 1/8——"AG 很强但并非不可战胜"。
- 翻转小技巧（quirk）：概率取 `1−p` 提交可带来 ~1e-5 的"免费"提升——本场可用，属数据/指标特性，注意甄别适用性。
- 平台期突破的两种正确姿势：补充**新特征工程的模型重跑**（1st 的 136 OOF）、换集成器结构（NNE）。

## 5. 可迁移性评估

- **可直接迁移**：QuantileDMatrix + 降精度 + 磁盘批加载；baseline 参数式二次学习；NN 集成器；"异质 OOF 缓慢入池"的档案管理。
- **需要前提**：大量 OOF 存档与算力；显存受限时尤其值钱。
- **不建议照搬**：把翻转技巧当通用手段（依赖特定数据分布）；死守单一集成器（1st 的 AG 教训）。

## 6. 对新手的关键启示

- 学会两个"显存翻倍术"：降精度 + QuantileDMatrix——很多"跑不动"其实是数据格式问题。
- 集成器也要选型：AutoGluon 12 小时不一定赢过一个 1.5 小时的 NN 集成器。
- 平台期不要只会加模型：换表示（新 FE 重跑）或换集成结构，往往更快。

## 7. 轻读结论（2026-10 补）

**一句话**：本场把"OOF 收藏馆 + 集成器选型"推到极限：**成员多样性 > 单模强度，集成器本身是一等模型**——1st 的赛后实验甚至推翻了自己整月依赖的 AutoGluon。

- 1st（JAPE）：136 OOF 大集成；AG 跑满 12h；flip +0.00001~0.00003；100 OOF 遇墙、136 OOF 破墙（0.97844 pub），私榜 0.97801 第 1；**赛后：NN 集成器 1.5h 达到同等水平，配 LGBM+LR 爬山后 0.97805 私榜，优于所有 AG 结果且省 8 倍时间**。
- 2nd：59 模型 + CatBoost 集成器；最好单模 TabM 0.97750 priv；"不同模型 > 同模型调参"。
- 3rd：迭代 OOF 堆叠（收集 OOF → AG 训练 → 按重要性筛 → 循环），先过滤泄漏与虚高 CV。
- 15th：单模最佳 CatBoost Optuna 0.97732 priv、xLearn FFM 0.97708；遗传编程特征在原数据上 +0.003、加统计/TE 后仅 +0.0001。
- QuantileDMatrix（69 票）：分批建直方图 + 降 dtype，最多支持 8× 数据；进阶用"落盘→分块读"省显存。

**裁决**：二分类 Playground 的通用配方 = 多样 OOF（含弱模型）+ 多集成器对照 + flip；扩池优先加"机制不同"的成员。

**悬案**：baseline 接力技巧细节缺失；反盲混争议结论未细读；本场 0 归档图。

## 8. 图表证据

无可用图证（本场归档 0 图）。

## 9. 出处

- 1st：JAPE 大集成全记录（含 NN 集成器复盘）：https://www.kaggle.com/competitions/playground-series-s5e8/discussion/603210
- XGBoost QuantileDMatrix 与降精度技巧：https://www.kaggle.com/competitions/playground-series-s5e8/discussion/600048
- 2nd：异质 OOF 流程：https://www.kaggle.com/competitions/playground-series-s5e8/discussion/603297
- 3rd：迭代 OOF 堆叠 + AutoGluon：https://www.kaggle.com/competitions/playground-series-s5e8/discussion/603198
- 15th：遗传编程特征：https://www.kaggle.com/competitions/playground-series-s5e8/discussion/603179
- 轻读全本：`analysis/deep/playground-series-s5e8.md`（Tier B 轻读：对照矩阵/裁决/证据分级/悬案；图证缺口已登记）
