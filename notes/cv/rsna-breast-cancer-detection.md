# RSNA - Screening Mammography Breast Cancer Detection

> 主题：cv ｜ 子类：— ｜ 领域：医疗影像 ｜ 类别：Featured
> 截止：2023-02-27 ｜ 队伍数：1687 ｜ 机制：代码赛 ｜ 指标：Probabilistic F-Score Beta (micro)
> 数据来源：`intel/rsna-breast-cancer-detection/`（120 条主题索引 + 8 篇 write-up 正文）

## 1. 任务与数据

- **预测目标**：由乳腺 X 光（mammography）图像预测是否患癌（按患者聚合，多视角多侧位）。
- **数据形态**：**超高分辨率医学影像**（原始约 3000×5000 像素）+ DICOM 元数据 + 患者级标签；阳性率极低（典型医学影像赛）。
- **构造陷阱**：
  - 高分辨率必须降采样或分块，**分辨率选择直接影响成绩**。
  - 每患者有多个视角（CC/MLO × 左右），需要**多视角聚合**。
  - 指标是概率化的 F-beta，**阈值与概率校准影响大**。
  - 阳性样本稀少 → 外部正样本数据价值高。

## 2. 验证方案

| 方案 | 使用者 | 说明 |
| --- | --- | --- |
| 按患者分组 CV | 多数 | 避免同一患者多视角跨折泄漏 |
| 消融验证外部数据收益 | 1st | 同一流水线、同一超参，仅切换外部数据，量化 +0.02 F1 |
| 公开榜与 OOF 双轨对照 | 1st | 消融表同时给出 OOF / 公开 / 私榜 |

## 3. 方案谱系

| 方案 | 名次 | 关键点 |
| --- | --- | --- |
| 分阶段训练（低分辨率预训练 → 高分辨率微调 → 多视角） | 2nd | 1280×1280 带外部数据预训练，1536×1536 不带外部数据微调，再做多视角融合 |
| 外部数据 + 标签平滑 | 1st | 消融显示**外部数据带来约 +0.02 F1**（OOF 与私榜一致）；soft positive label 与 label smoothing 效果相当 |
| 多视角多侧位建模 | 6th | 显式建模不同视角/侧位之间的关系 |
| 广泛技术试验 | 9th | 在医学影像上系统性试错 |

## 4. 关键技巧

- **分阶段分辨率训练**：低分辨率预训练（省算力、学通用特征）→ 高分辨率微调（学细节）。
- **多视角聚合**：先单视角建模，再按患者聚合（max/mean/注意力）。
- **外部正样本数据**：阳性率极低时，外部数据的边际收益最直接。
- **标签处理**：label smoothing 与软正标签作用相近，不必过度设计。
- **概率化指标的阈值/校准**：F-beta 需要单独优化决策阈值。
- **域内先验**：社区有专门的乳腺影像入门帖；同类 RSNA 系列赛的历史方案被系统整理。

## 5. 可迁移性评估

- **可直接迁移**：
  - **按实体（患者/病例）分组切分**是医学影像的底线要求。
  - 分阶段分辨率训练（低 → 高）在超高分辨率影像任务中通用。
  - 先单视角再聚合的结构。
  - 概率化指标必须单独做阈值/校准。
- **需要前提**：
  - 高分辨率训练需要大显存或分块推理（DALI 等加速工具很关键）。
  - 外部医学数据的获取与合规。
- **不建议照搬**：
  - 直接全分辨率端到端训练（算力代价过高）。

## 6. 对新手的关键启示

1. **医学影像先解决三件事**：分辨率策略、多视角聚合、按患者分组验证。
2. **外部数据的价值可以被量化**（+0.02 F1），值得花时间找。
3. **标签技巧的收益常被高估**（1st 的消融显示两种标签技巧差别不大）。
4. **概率化指标 = 模型 + 阈值**，二者都要调。

## 7. 出处

- 讨论区索引：`intel/rsna-breast-cancer-detection/topics.md`（120 条）
- 已收录 write-up（8 篇）：
  - 1st（178 票）：https://www.kaggle.com/competitions/rsna-breast-cancer-detection/discussion/392449
  - 6th（101 票）：https://www.kaggle.com/competitions/rsna-breast-cancer-detection/discussion/390974
  - 9th（89 票）：https://www.kaggle.com/competitions/rsna-breast-cancer-detection/discussion/390966
  - 乳腺影像入门（253 票）：https://www.kaggle.com/competitions/rsna-breast-cancer-detection/discussion/369262
  - 往届 RSNA 获奖方案汇总（120 票）：https://www.kaggle.com/competitions/rsna-breast-cancer-detection/discussion/369103
