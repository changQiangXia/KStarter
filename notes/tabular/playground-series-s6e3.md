# Playground Series S6E3 - 客户流失预测

> 主题：tabular ｜ 子类：— ｜ 领域：电信（合成数据） ｜ 类别：Playground
> 截止：2026-03-31 ｜ 队伍数：4142 ｜ 机制：标准赛 ｜ 指标：ROC AUC
> 数据来源：`intel/playground-series-s6e3/`（80 条主题索引 + 6 篇 write-up 正文）

## 1. 任务与数据

- 预测目标：用户流失概率（二分类 AUC）；60 万行合成数据 + 7,032 行原始 IBM Telco 数据集。
- 数据特性：原数据最优 XGB `max_depth=1` → **特征间几乎没有交互**（EDA 帖的关键结论）——逻辑回归类线性模型强，交互挖掘收益低；信号主要藏在合成器留下的"指纹"里。
- 与本系列其他场的关系：本场是 S6E4（灌溉）亚军作者"从 3 月迁移到 4 月"的源比赛，也是本月两条主线（KGMON 深度栈 / 百模型集成）的试验场。

## 2. 验证方案

- 全体统一 5 折 StratifiedKFold + 固定 seed；所有 OOF/test 按命名规范存档（`oof_*_v*.npy`）。
- **嵌套（无泄漏）目标编码**：外层 CV 折内再套内层 5 折算 TE；原数据的先验统计无合成标签 → 可放心使用。
- 公开 notebook 生态警示：blender 农场与多账号作弊被社区点名；讨论区（如 ID/depth 类分析帖）才是信号源。

## 3. 模型家族

| 方案 | 使用者层次 | 关键点 | 出处 |
| --- | --- | --- | --- |
| KGMON Playbook：4 层堆叠（特征提取层→GBDT/NN×2→logit LR） | 1st | 850 模型筛 150；25 种 DL 架构；600k 行代码由 LLM 写 | topic 686686 |
| 100 OOF 混合集成（自有 + 公开 kernel） | 3rd | 简单 LinearRegression 反而最好；逐模型加、盯 CV–LB | topic 686834 |
| 149 模型 → 6 元模型 → 3 blend | 5th | BayesianRidge/Ridge/HC 几乎同分；选交存在遗憾 | topic 686871 |
| 高级 EDA：用 max_depth 探测交互结构 | 社区 | 原数据 depth=1 最优 → 转向线性模型 | topic 680290 |

## 4. 关键技巧

- **把合成过程当信号源**（1st 的核心思想）：`snap` 特征（合成值 → 原数据最近值 + 差值）恢复"真值"并编码噪声幅度；**小数位数字特征**（各十进制位的 digit/round 标记）；`radix` 交互（数值×类别的联合整数编码）；KDTree 最近邻原客户标签；频率编码；TF-IDF 字符 n-gram 与 Benford 偏差检测生成器指纹。
- **四级堆叠**：L1 特征提取模型（KNN/DAE/PCA/TE）→ L2、L3 嵌套 OOF 训练 GBDT/NN → L4 cuML LogReg（logit stacking, L2 惩罚）；多样性来自 4 个 GBDT 库 + 25 个 NN 架构 + 12+ 特征管线。
- **LLM 工程化**：GPT5.4/Gemini3.1/ClaudeOpus4.6 编写全部代码（60 万行），4×A100 上训 850 模型、跑 50 个 EDA 脚本——顶级方案的组织形态已是"人类定 playbook + agent 执行"。
- **选择与提交**：3rd 的"每天加一个模型看 CV–LB"流程；5th 的教训——最后交了 Ridge，而 BayesianRidge 其实最优（选择纪律与记录同等重要）。

## 5. 可迁移性评估

- **可直接迁移**：嵌套 TE 写法；OOF 命名/存档规范；logit stacking；snap/数字位类"生成器指纹"特征（任何合成数据赛）；用 depth 扫描探测交互结构；LLM 批量建模的工程流程。
- **需要前提**：原数据可得（snap/KDTree 依赖）；大规模算力（4×A100 级）或按比例缩小；LLM 工具链。
- **不建议照搬**：无 CV 纪律的盲目 blender；指望 agent 无人监督完成路线决策。

## 6. 对新手的关键启示

- 先问"原数据在哪、合成器改了什么"：snap + 小数位特征是本届最便宜的高收益技巧。
- 交互结构决定模型选择：depth=1 最优时别再堆深树与特征交叉，转向线性/简单模型。
- 学 3rd 的日常节奏：收集 OOF → 逐个加入 → 观察 CV 与 LB 的背离，而不是一次性糊一个大 blend。

## 7. 出处

- 1st：KGMON Playbook（四级堆叠 + 合成指纹特征）：https://www.kaggle.com/competitions/playground-series-s6e3/discussion/686686
- 3rd：100 OOF 集成：https://www.kaggle.com/competitions/playground-series-s6e3/discussion/686834
- 5th：149 模型 → 6 元模型 → 3 blend：https://www.kaggle.com/competitions/playground-series-s6e3/discussion/686871
- 高级 EDA（depth 扫描揭示无交互）：https://www.kaggle.com/competitions/playground-series-s6e3/discussion/680290
