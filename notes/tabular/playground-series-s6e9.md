# Playground Series S6E9 - 电动车购买预测（AI 接力赛）

> 主题：tabular ｜ 子类：— ｜ 领域：汽车消费（合成数据） ｜ 类别：Playground
> 截止：2026-09-30 ｜ 队伍数：3575 ｜ 机制：标准赛 ｜ 指标：ROC AUC
> 数据来源：`intel/playground-series-s6e9/`（79 条主题索引 + 6 篇 write-up 正文）

## 1. 任务与数据

- 预测目标：预测是否购买电动车（AUC）；66.9 万训练行 / 28.7 万测试行、13 个特征、阳性率 17.46%。
- 数据来源：由 Omkar Kadam 的 1 万行原始数据合成；**原始购买公式被社区逆向**：`1.2·income/100k + 0.6·concern + 2·subsidy − [Medium] − 3·[High] + noise > 5.5` 单条规则 AUC≈0.9377。
- 生成器痕迹：行由 LLM 以 token 形式生成 → **GPT-2 BPE token 特征（收入/通勤距离的 CSV 字符串分词）** 成为多数最强一级模型的核心输入。

## 2. 验证方案（本场的技术巅峰：团队级验证工程）

2nd（Team Alicia）把验证做成了准科研流程：

- **封存 holdout**：53.5 万 dev 行做 5 折，13.4 万行封存从不参与选择；另设 5 万行筛查子集且只使用一次。
- **预注册**：所有候选实验在出结果前登记（54 条）；门控 = ≥+1.0u、≥2 fold-SE、≥4/5 折为正、权重全正；最终轮收紧到 +1.5u / 2.5 SE。
- **安慰剂对照**：新特征必须战胜同宽度的行置换安慰剂（稀释代价 −3~−8u）。
- **公开榜有害实验**：故意拟合公开榜的文件冲上 0.94945 公开第 1，但私榜仅 0.94313——用实验量化"追榜的代价"。
- 1u = 1e-5 AUC；嵌套增益对私榜的 Spearman 0.991，公开分只有 0.793。

## 3. 模型家族

| 方案 | 使用者层次 | 关键点 | 出处 |
| --- | --- | --- | --- |
| AI 接力：3 代 5 个 agent + 人类教练，60 模型 logit 堆叠 | 1st | 共享 folds.npy 公平比较；私榜 1st（0.94602） | topic 745013 |
| 嵌套 CV + TabPFN-3.5（42.8 万上下文）+ AUC-direct 三层融合 | 2nd | 标签无关代理特征（distilgpt2 LLR）；FFT 精确成对 AUC | topic 744815 |
| 115 列 logistic 回归堆叠 + 收入多级取整 TE | 3rd | 软伪标签；token 分组与语言模型特征 | topic 744848 |

## 4. 关键技巧

- **AI 接力（1st 的范式）**：baton = 代码 + 笔记（plan/progress/discoveries/黑名单/cookbook 五件套）；新 agent 上岗第一天派 13 个助手分头读历史、6 个审代码；"agents forget, notes remember"。
- **反内卷技巧**：用 `1−p` 倒置提交把真实分数藏成 0.053，避免给对手公开榜激励（平台只显示每队最佳分）。
- **多样性规则**（可当操作标准）：>0.94 AUC 且与现有模型相关性 <0.99 才值得入库；让 agent 互相代码审查（新眼睛抓泄漏）。
- **标签无关代理特征**：只在原始 1 万行微调 distilgpt2，取 Yes/No 对数似然比作为 TabPFN 输入。
- **AUC-direct 融合**：对约 2.6e10 对样本用直方图+FFT 精确计算成对 AUC 代理，比 logloss 栈再涨 1.62u。
- 无伪标签、统一折文件是 1st 的纪律；3rd 则用软伪标签+多级收入 TE——两条路线都进前三。

## 5. 可迁移性评估

- **可直接迁移**：共享折文件（任何多人/多 agent 协作的第一基建）；预注册+门控+安慰剂的实验管理学；1e-5 级增益的显著性检验；notes-as-baton 的 agent 协作协议；token 特征（LLM 生成的合成数据）。
- **需要前提**：多 agent 工具链与算力；TabPFN 类大上下文模型；团队协作。
- **不建议照搬**：拟合公开榜（本场实验证明 −0.006 私榜代价）；无尺度感地追逐 1e-5 级"提升"（它们常是噪声）。

## 6. 对新手的关键启示

- 本场是"agent 时代竞赛组织学"的活教材：人会从选手变成教练/裁判；**笔记质量 = 下一代 agent 的起点**。
- 学 Team Alicia 的验证门控思想：即使不做全套，也要"先登记假设、再跑实验、用多种子与外折复核"。
- 公开榜适合做"噪声守卫"，不适合做目标函数——0.949 的公开第 1 最终私榜 0.943。

## 7. 轻读结论（2026-10 补）

**一句话**：两层看点——技术上，"原始 1 万行小数据是生成器钥匙"（复原购买公式单独 AUC 0.9377、合成行带 LLM token 痕迹→GPT-2 BPE 特征有效）；协作上，冠军是**"1 个教练 + 5 个 AI agent、三代接力"**，靠笔记与代码库继承上下文。

- 1st（745013，私榜 0.94602）：GPT-5.6 Sol+Fable5 → GPT-6-Astra+Fable5.1 → Opus 5.5；每腿 CV 0.94637→0.94656→0.94683→0.94697；**接力棒=笔记**（plan.md / progress.md / discoveries.md / **closed ideas** / cookbook）；Opus 5.5 首日派 **13 个 helper agent 读历史 + 6 个审代码**；**隐藏分数用 p→1−p（AUC 变 1−AUC）**。
- 2nd（744815，私榜 0.94588）：**嵌套 CV + 13.4 万密封 holdout + 预注册 + 双门槛**（常规 ≥1.0u/2SE，决赛 ≥1.5u/2.5SE）；嵌套增益与私榜 **Spearman 0.991**（公榜仅 0.793）；**TabPFN-3.5 全上下文（42.8 万行/折）**、distilgpt2 的 label-free LLR 特征、**AUC-direct 融合（~2.6e10 对，直方图+FFT，+1.62u）**；反面教材：拟合公榜的文件公榜第 1（0.94945）私榜仅 0.94313。
- 3rd（744848）：115 列 logistic 堆叠（clip→logit→L2 LR）；**income 多级取整目标编码** + 折外编码，0.9431→0.9458。
- 社区：辛普森悖论（31 票）、诚实模型目录/OOF Hub（17 票）、"逻辑回归在原始数据上击败高级模型"（16 票）。

**裁决**：合成赛先吃透原始数据与生成伪影；折外监督编码 + LR 堆叠是稳健骨架；选择提交靠嵌套验证与预注册而非公榜；agent 团队的关键是上下文继承机制。

**悬案**：4th–7th/9th 方案缺失；1st 的模型细节散落在其笔记体系中；2nd 的 Final B 风险未复盘。

## 8. 图表证据

![2nd 的最终管线与权重](../../intel/playground-series-s6e9/bodies/744815_img/02.png)

**图 1**（topic 744815）：三级管线与两份提交的权重（AUC-direct 融合含 FFT 精确成对 AUC）+1.62u。

## 9. 出处

- 1st：The AI Relay（5 agents / 3 generations / 1 codebase）：https://www.kaggle.com/competitions/playground-series-s6e9/discussion/745013
- 2nd：嵌套 CV、预注册与公开榜有害实验：https://www.kaggle.com/competitions/playground-series-s6e9/discussion/744815
  - 3rd：FE 与 logistic 回归堆叠（115 列）：https://www.kaggle.com/competitions/playground-series-s6e9/discussion/744848
  - 8th：https://www.kaggle.com/competitions/playground-series-s6e9/discussion/744923
  - 10th：https://www.kaggle.com/competitions/playground-series-s6e9/discussion/744826
  - 辛普森悖论（31 票）：https://www.kaggle.com/competitions/playground-series-s6e9/discussion/738991
- 轻读全本：`analysis/deep/playground-series-s6e9.md`（Tier B 轻读：对照矩阵/裁决/证据分级/悬案 + 2 图证）
