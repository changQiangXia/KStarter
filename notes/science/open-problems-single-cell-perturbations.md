# Open Problems - Single-Cell Perturbations

> 主题：science ｜ 子类：— ｜ 领域：生物信息 ｜ 类别：Research
> 截止：2023-XX-XX ｜ 队伍数：1000+ ｜ 机制：代码赛 ｜ 指标：扰动响应预测（多组学误差）
> 数据来源：`intel/open-problems-single-cell-perturbations/`（80 条主题索引 + 6 篇 write-up 正文）

## 1. 任务与数据

- 预测目标：预测**小分子扰动后单细胞的基因表达响应**（细胞类型 × 化合物的组合）。
- 数据形态：输入特征只有"细胞类型 + 小分子名"这样的**短关键词对**，输出是高维表达谱。
- 构造陷阱（本场核心）：
  - 特征信息极少（两个关键词），必须**外部注入生物学知识**；
  - 高维输出、强噪声；
  - 训练/测试的化合物或细胞类型存在未见组合（泛化要求高）。

## 2. 方案谱系

| 方案 | 名次 | 关键点 |
| --- | --- | --- |
| **整合生物学知识**（把领域先验注入特征/表示） | 1st | 明确记录：因为输入只有关键词对，必须引入外部生物知识才能有效建模；还包含赛后的"late findings" |
| PyBoost 方案 | 13th | 见讨论区（强调某个 boosting 变体的效果） |
| 其他 | 见讨论区 | |

## 3. 关键技巧

- **特征信息不足时，用领域知识补足**（基因/通路/化合物结构等外部表示）。
- **高维输出目标**需要合适的变换与损失（表达谱常用对数变换）。
- **未见组合的泛化**：按化合物/细胞类型分组验证。

## 4. 可迁移性评估

- **可直接迁移**：
  - **输入特征太弱时，外部知识注入是唯一出路**（与 Deep Past 的语料工程、Leash-BELKA 的构建块结构同源）；
  - 高维输出目标的变换与损失选择；
  - 按组合维度分组验证。
- 需要前提：生物学数据库与工具链。
- 不建议照搬：只用原始关键词特征硬拟合。

## 5. 对新手的关键启示

1. **先判断"输入信息是否足够"**：不够就必须注入外部知识，而不是换模型。
2. 该系列（Open Problems）的两场（Multimodal / Perturbations）都说明：**生物信息赛的胜负在数据与知识整合**。

## 6. 出处

- 讨论区索引：`intel/open-problems-single-cell-perturbations/topics.md`（80 条）
- 已收录 write-up（6 篇）：
  - 1st（50 票，含 late findings）：https://www.kaggle.com/competitions/open-problems-single-cell-perturbations/discussion/459258
  - 2nd（49 票）：https://www.kaggle.com/competitions/open-problems-single-cell-perturbations/discussion/458738
  - 3rd（33 票）：https://www.kaggle.com/competitions/open-problems-single-cell-perturbations/discussion/458750
  - 13th U900 / PyBoost（65 票）：https://www.kaggle.com/competitions/open-problems-single-cell-perturbations/discussion/460858
