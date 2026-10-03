# Playbook：表格 / 时序

> 版本：v1.1（定稿）｜ 依据：`notes/tabular/` 全部 106 篇摘要（该主题 106/106 已完成；含 2021–2022 月度系列全量）
> 定位：近 5 年最大主题（106/264，40%）。"表格"只是数据形态，真正的分野见 §1。

## 1. 主题地图：先判断你属于哪个族群

| 族群 | 代表 | 纲 |
| --- | --- | --- |
| **真实业务 Featured/Research** | Amex、Home Credit、Optiver、H&M、JPX、ICR | 验证设计 + 领域建模 + 机制理解 |
| **Playground 合成系列** | S4E1–S6E9 全系 | 生成痕迹挖掘 + 集成科学 |
| **多表关系型** | Home Credit Stability、Learning Equality | 聚合策略 + 指标拆解 |
| **用户-物品序列** | Otto、H&M、四方形匹配 | 召回 → 排序 |
| **时序面板 / 金融** | Jane Street、Mitsui、Ubiquant、GoDaddy、Enefit | walk-forward + 在线更新 |
| **传感器 / 生理序列** | CMI 系列、TLVMC、HMS | 序列建模 + 事件级后处理 |
| **体育概率** | March Mania 系列 | 校准 + 稳健提交 |

**指标族群速查**：概率类（AUC/LogLoss/Brier）｜ 回归类（RMSE/MSLE/RMSLE）｜ 标签类（Accuracy/Balanced Accuracy/QWK）｜ 复合/自定义（Sharpe、稳定性、事件级 F1）。

## 2. 验证设计（第一地基，永远先做）

1. **按实体分组**：患者/用户/球队/地点（`StratifiedGroupKFold`，Home Credit Stability）。
2. **时间结构**：walk-forward（Hull）、按年/时间段分组（S5E3 按年 GroupKFold）、CombinatorialPurgedGroupKFold（Mitsui）、滑动窗口（ICR 的时间漂移）；
   验证规模与评测对齐（Jane Street 用 200 天 = 公开集窗口）。
3. **CV–LB 关系量化**，然后决定信谁：
   - 一致性高 → 简化验证，预算投给特征/融合（Optiver Close 的元决策）；
   - 公开榜小样本/被污染 → 只信 CV（ICR、Playground 洗牌场）。
4. **Playground 专属**：train/test 同分布（对抗验证 AUC≈0.5）→ 可以信 CV；但公开 notebook 的"高分 blender"是毒药，**超出 CV 框架上限的公开分视为污染**（S6E6）。
5. **高级形态**：密封 holdout + 预注册 + 安慰剂（S6E9）；把 CV 噪声量化为特征准入阈值（Student Performance）。

## 3. 特征工程工具箱

### 3.1 通用（跨族群 80% 场景）

- **groupby(COL1)[COL2].agg(STAT)**：mean/std/min/max/count/nunique/skew……；进阶：**直方图分桶计数**、分位数、分组 z-score（S5E2/S5E5）。
- **偏差特征**：值减组中位数（Optiver Close、Optiver Vol）。
- 频率编码、NAN 合成单一列、类别两两组合、数值分箱、**小数位/round 特征**（S5E11）。
- 比值/倍率目标（Godaddy：预测"相对变化"而非绝对值）。
- **锚数据**：原数据/参照表当"建议零售价"（S5E2）。

### 3.2 时序 / 金融

- 滞后/滚动统计、时间衰减加权、按时间步标准化（Ubiquant）；
- **缺失即信息**（停牌指示特征，Ubiquant）；
- 天气预报类特征的**预报间差分**（Enefit）；分组偏差特征。

### 3.3 推荐 / 排序

- **召回 → 排序**两阶段（Otto、H&M）；共现矩阵当候选生成器；热门度基线先量化；用户自身历史回填候选；层级/图结构传播（Learning Equality）。

### 3.4 合成数据指纹（Playground 专章，本系列最独特的积累）

| 技术 | 说明 | 来源 |
| --- | --- | --- |
| 原数据接法对照 | 拼行（concat）vs 拼列（merge）vs 仅统计 | S5E3、S6E2 |
| 生成公式逆向 | GP 逼近（S6E1）或精确还原（S6E4 完全分离公式） | S6E1/S6E4 |
| snap 特征 | 合成值 → 原数据最近值 + 差值 | S6E3 |
| 子集匹配 | 枚举基特征子集是否原样出现在原数据 | S4E1 |
| token 特征 | CSV 字符串的 GPT-2 BPE 分词特征 | S6E9 |
| 孪生行挖掘 | KNN/groupby 找复制行的"兄弟姐妹" | S5E2 |
| 派生列反推 | 多出来的列多为已有列的确定性变换 | S6E6 |
| 频率比 | train 频率 / 原数据频率（过采样程度） | S5E11 |
| 噪声上限量化 | 找出不可预测样本，解释名次波动 | S5E7 |

## 4. 建模与集成科学

### 4.1 单模优先

- **先压满单模再谈集成**：S5E2 单模夺冠、S5E11 单模亚军、S6E8 单模型 18 个月来首次登顶——特征工程到位时集成不是必需品。
- GBDT 三件套 + 现代 DL：**RealMLP / TabM / TabPFN**（小数据强）、FT-Transformer（大样本多分类）。
- 交互结构探测：用 max_depth 扫描判断"有没有交互"（S6E3/S6E4 原数据 depth=1 最优 → 转向线性模型）。

### 4.2 集成器选型（按任务特性）

| 集成器 | 适用 | 备注 |
| --- | --- | --- |
| logit + LR | AUC/概率类首选 | class_weight=None、不校准（S6E5）；L2、C=0.03–1.0 |
| Ridge / rank 平均 | 回归与稳健场景 | 对相关预测与校准漂移更稳 |
| Hill Climbing | 快速选模 | **容差必须按指标量级设定**（S4E9 的 5→81 教训） |
| 非线性栈 | 情景差异存在时 | "有/无主特征"双情景（S5E4）；缺失主特征是最强信号 |
| NN 集成器 | 追求上限 | 1.5 小时 > AutoGluon 12 小时（S5E8） |
| AutoGluon | 多样性机器/基线 | 强，但需与其它集成器对照 |
| baseline 参数式二次学习 | 通用增益 | CatBoost/LGBM/XGB 均可（S4E10/S5E8/S5E10） |

### 4.3 选择与多样性

- 子集选择：Optuna（S6E2，仅 1/10 被稳定选中）；分歧度最大优先（S6E1 13th）。
- 多样性判断：**>0.94 分且与现有池相关性 <0.99**（S6E9）；秩平均抗校准漂移。
- 集成规模有**甜点区**（约 50–100），超过后退化回退（S6E6）。
- 残差栈、OVR 分解、等距回归后处理等按场景选用。

### 4.4 工程与工具链

- GPU：RAPIDS cuDF/cuML、**QuantileDMatrix + 降精度**（显存 ×4–8，S5E8）。
- 存档规范：统一折文件 + `oof_*/pred_*` 命名（S6E3）；OOF 共享池需完整性检查（S6E8 14th）。
- Agent 工程化：local_leaderboard.md（S6E5 2nd）、notes-as-baton 五件套（S6E9）、分工竞赛协议（S6E8）。

## 5. 决策规则与指标适配（最"便宜"的分数）

| 指标 | 决策要点 | 证据 |
| --- | --- | --- |
| Balanced Accuracy | `argmax(p/prior)` 或类乘子优化（一行代码 +0.06） | S6E7 4th/2nd |
| Accuracy | 概率 → 阈值/权重优化，别直接 argmax | S4E2 |
| QWK | 显式优化阈值 | Essay 2.0 等 |
| RMSLE | 在 log1p 空间集成再用 expm1 还原 | S5E5 |
| AUC | 只关心排序：不校准、不做类别权重 | S6E5 5th |
| Brier / LogLoss | 概率校准（裁剪、isotonic、LR 融合） | March Mania 系列 |
| 自定义复合指标 | 先拆解"奖励什么行为" | Home Credit Stability |
| 边界/截断目标 | 门控、区间加权、clip | S6E1/S6E2 |

## 6. 机制与策略

- **在线学习**：评测期若揭示新标签，能更新就更新（Enefit、Optiver 系、Mitsui、Jane Street 四场独立验证）。
- **提交管理**：按 CV–LB 轨迹选稿、互补对冲、不追公开榜（详见 `LEARNING_PATH.md` 附三）。
- **目标可被公开信息直接构造**的赛事（JPX）要自检"分数是否来自外部信息"。
- 时间预算：新手路线图——前 2–3 天探索、编号实验、保存 OOF（S5E12）。

## 7. 常见坑

| 坑 | 证据 |
| --- | --- |
| 随机切分用于分组/时间结构数据 | ICR、Home Credit、S5E3 |
| 追公开榜 blender（多账号/盲目混合） | S6E6、S5E8、多场社区批评 |
| 搜索容差不按指标量级设定 | S4E9（tol=1e-5 → 第 5 掉到 81） |
| 无选择平均全部 OOF | S6E2 |
| 目标编码未嵌套折内 | S4E2 69th（移除后私榜反升） |
| 小数据盲目 AutoML/伪标签 | S4E2 反例 |
| 默认原数据拼行有效 | S5E11/S6E2（视场次而定） |
| 公开榜微差动摇 OOF 判断 | S6E7（414→4）、S6E6（344→1） |

## 8. 年度演进

- **2021–2022**：GBDT + 特征工程 + 简单集成；金融时序与体育概率成熟（Optiver、March Mania、Amex、Ubiquant）。
- **2023**：关系型多表与自定义指标（Home Credit Stability）；召回排序普及（Otto、H&M）。
- **2024**：Playground 转向"生成痕迹挖掘"（S4E1 子集匹配、S4E9 离群分类器）；GNN/多模态开始渗透表格。
- **2025**：RMSLE/log 空间、S5E2 孪生行、S5E11 指纹特征矩阵、深栈（S5E4）；单模价值回归。
- **2026**：**agent 化生产**（S6E5 Codex YOLO、S6E8 蜂群、S6E9 接力）；先验校正等"决策层技巧"常态化；社区 OOF 图书馆与密封折协作。

## 9. 新手学习路径

1. **验证与 CV–LB**：ICR（滑动窗口）→ Optiver Close（元决策）→ S5E12（ID 位移）。
2. **特征基本功**：Ubiquant（缺失即信息）→ Godaddy（倍率）→ S5E2（groupby/直方图）。
3. **集成科学**：S6E2（Optuna+Ridge）→ S5E5（RMSLE/残差）→ S6E9（验证工程）。
4. **指标适配**：S6E7（先验校正）→ S4E2（Accuracy 阈值）→ March Mania（校准）。
5. **合成数据专题**：S4E1 → S6E3 → S6E9（由浅入深）。
6. **Agent 时代工作流**：S6E5（local leaderboard）→ S6E8 → S6E9（接力协议）。

> 修订说明：剩余 Playground 场次收齐后将补一次"年度演进"与案例索引；本册方法论部分已稳定。

## 10. v2 增补（Tier B 204 场，2026-10）

1. **中位数型指标的结构套利**：MedAE 只取决于中位误差样本；对 AE≤0.06 或 ≥0.7 的样本给 0.01 权重（LGBM CV +0.03），并把预测向 9 档硬度值整形（±0.25 覆盖 89.5%，约 56% 命中即 0.25）（L114，s3e25）。
2. **随机目标检验**：100 次打乱目标对照，z 在 ±2 内即原数据无信号；S5E9 z=-0.83，近 6 场回归 3/6 随机。此后转向生成痕迹与稳健集成（L115，s5e9）。
3. **多目标先做"拆合实验"**：EC1/EC2 上模型排序完全反转（EC1 树模型、EC2 Bagged KNN），11th 拆开进前 11；1st 用多输出+重 FE 也能赢（T29，s3e18）。
4. **实体块切分**：玩家历史整体落在 train 或 test → 按 nickname GroupKFold；分组后分数更低 ≠ 错，需与 LB 绝对值对照（L116/T31，scrabble-player-rating）。
5. **清洗三件套**：`-666` 错误值、重复行、近常数冗余列（fr_COO2）；test 端 OOD 类别值用频率编码而不是硬编码（s3e18）。
6. **原数据合并先对抗验证**：确认分布一致后再并入，并用 CV 证明增益（L131，s3e18 419685）。
7. **指标实现口径**：逐列 AUC 平均 vs 堆叠 GINI 会给出不同乐观度；以官方定义为唯一口径（s3e18 421149）。
8. **窄分带不要读 LB**：26.38–26.41、大量 0.25 聚集时，LB 微差无信息，按 CV/分布整形决策（T37，s5e9/s3e25）。
9. **引用纪律**：Playground 无奖牌，抄公开 notebook 不注明来源会引发社区反弹（L133，s3e25 458154）。
