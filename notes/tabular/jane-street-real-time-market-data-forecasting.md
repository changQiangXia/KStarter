# Jane Street - Real-Time Market Data Forecasting

> 主题：tabular ｜ 子类：tabular-ts ｜ 领域：金融 ｜ 类别：Featured
> 截止：2025-07-12 ｜ 队伍数：3757 ｜ 机制：代码赛 ｜ 指标：Zero-Mean R²
> 数据来源：`intel/jane-street-real-time-market-data-forecasting/`（120 条主题索引 + 8 篇 write-up 正文）

## 1. 任务与数据

- **任务形式**：在隐藏测试期**实时预测**金融标的收益，提交的是能在评测时自行训练与推理的 notebook——**必须支持在线/自适应学习**。
- **数据形态**：匿名化的 79 个特征 + "responder" 标签，按日期与标的组织；数据经过混淆但保留可分析结构。
- **关键特性**：非平稳（non-stationary）——静态模型会随时间失效，这是本场与普通离线比赛的根本区别。

## 2. 验证方案

| 方案 | 使用者 | 说明 |
| --- | --- | --- |
| 时间序列 CV（2 折，验证窗口 200 天） | 私榜第 8 | 验证窗口刻意与公开数据集大小一致，与 LB 相关性良好 |
| 分标的建模 | 多数 | 每个 symbol 单独训练/预测 |
| 线上滚动评估 | 社区 | 模拟"边训边测"的真实条件 |

## 3. 方案谱系

| 方案 | 名次 | 关键点 |
| --- | --- | --- |
| 在线学习 TabM 神经网络（70%）+ 静态 LightGBM 集成（30%） | 私榜 162 | **自适应模型 + 静态模型混合**，并对预测做 clip |
| 3 层 Transformer 编码器为主的 50/50 集成 | 公开 17 | 与 GBDT 组合 |
| 时间序列 CV + 集成 | 私榜 8 | 强调验证窗口要与公开集规模对齐 |
| 简单 3 层 MLP（无在线学习、无集成） | 社区提问帖 | 作者用"极度小心的训练与泛化设计"拿到 0.0064——说明**谨慎的基础方案仍有价值** |

## 4. 关键技巧

- **在线/自适应学习**：本场最大的结构性杠杆；静态模型 + 动态模型的加权组合是主流。
- **预测后 clip**：金融收益分布长尾，裁剪极值能稳定指标。
- **验证窗口对齐**：私榜第 8 明确把验证集设为 200 天以匹配公开集规模，保证 CV 与 LB 可比。
- **混淆数据的结构分析**：社区对 responder 与标签结构做了深入逆向分析（本场高票讨论帖）。
- **历史赛事复用**：上一届 Jane Street 比赛（2021）的获奖方案被系统整理成参考帖。

## 5. 可迁移性评估

- **可直接迁移**：
  - **非平稳场景下"自适应 + 静态"混合建模**的范式。
  - 预测裁剪（clip）作为稳定化手段。
  - 让验证集规模与公开评测集**规模对齐**，提高 CV-LB 可比性。
- **需要前提**：
  - 在线学习要求评测环境允许"边训边测"（代码赛特有）。
  - 金融数据的严谨性要求（避免未来函数、泄漏）。
- **不建议照搬**：
  - 直接复用上一届的特征与模型（市场结构会变）。
  - 忽略非平稳性只做静态训练。

## 6. 对新手的关键启示

1. **先判断数据是否非平稳**：决定要不要引入在线学习。
2. **验证集设计要与评测条件对齐**（规模、时间跨度、切分方式）。
3. **简单模型 + 严谨训练也能有竞争力**（社区里 3 层 MLP 的案例），但前提是把泛化想清楚。
4. **善用历史赛事资料**：同类比赛的历史 write-up 是最快的入门材料。

## 7. 出处

- 讨论区索引：`intel/jane-street-real-time-market-data-forecasting/topics.md`（120 条）
- 已收录 write-up（8 篇）：
  - 私榜 8（295 票）：https://www.kaggle.com/competitions/jane-street-real-time-market-data-forecasting/discussion/556542
  - 公开 17（57 票）：https://www.kaggle.com/competitions/jane-street-real-time-market-data-forecasting/discussion/556541
  - 私榜 162（11 票）：https://www.kaggle.com/competitions/jane-street-real-time-market-data-forecasting/discussion/589829
  - 简单方案能到什么水平（32 票）：https://www.kaggle.com/competitions/jane-street-real-time-market-data-forecasting/discussion/550849
  - 参考资料与入门材料（172 票）：https://www.kaggle.com/competitions/jane-street-real-time-market-data-forecasting/discussion/540437
  - 往届金融赛获奖方案汇总（48 票）：https://www.kaggle.com/competitions/jane-street-real-time-market-data-forecasting/discussion/541003
