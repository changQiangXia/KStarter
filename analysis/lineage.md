# KStarter 方法谱系（Method Lineage）

> 定位：基于 264 篇深读（Tier A 60 + Tier B 204）与 `analysis/THEORY.md`（L1–L113 + T1–T27）的**编辑归纳**，抽取跨场技法传播链，共 52 个节点（≥40）。节点是"技法流传路径"的重构，不是文献计量结论；证据以归档材料为准，引用场次可用 `analysis/deep/<slug>.md` 与 `analysis/claims.csv` 复核。
> 生成：2026-10（Tier B 收官后）。

## 0. 总览图

```text
A GBDT/表格基线 ─┬─ N01 XGB/LGBM ─ N02 CatBoost 原生类别 ─ N03 异质集成 ─┬─ N04 爬山
                │                                                        ├─ N05 OOF 权重/栈
                │                                                        ├─ N06 AutoML 栈
                │                                                        └─ N07 伪标签迭代
                └─ N08 log 变换 / 后处理截断
B 度量学习/检索 ─ N09 ArcFace ─ N10 subcenter+动态 margin ─ N11 分类+度量混合头
                └─ N12 嵌入 PCA+kNN ─ N13 双塔/DOLG ─ N14 遮挡/掩码增强（BlendFlip）─ N15 DeepMAC chip
C 多模态融合 ─── N16 CNN+表格 concat ─ N17 结构化自注意力 ─ N18 三头（回归+硬分类+软分类）
                └─ N19 物种身份辅助任务 ─ N20 Transformer 融合 ─ N21 大模型 embedding+GBDT
D 时序/生存/物理 ─ N22 ARIMA ─ N23 GAM/EP ─ N24 Cox ─ N25 事件概率→期望→差分（EPA/WPA）
                └─ N26 "截至当前"滚动聚合
E 验证与选择 ─── N27 KFold ─ N28 分层多标签 ─ N29 GroupKFold 实体隔离 ─ N30 对抗验证（合并原数据）
                └─ N31 CV/LB 样本量（测量 vs 随机变量）─ N32 随机目标 z 检验 ─ N33 OOF 选模/融合判据
F 后处理/校准 ── N34 clip/分位裁剪 ─ N35 isotonic ─ N36 单参数 logit 平移
                └─ N37 分组合法性裁剪 ─ N38 指标形态整形（MedAE/档位/样本权重）
G RL/自对弈 ──── N39 PPO ─ N40 课程学习（地图/场景缩放）─ N41 JAX 向量化环境
                └─ N42 行为克隆 bootstrap ─ N43 自对弈对手多样性
H Agent/LLM ──── N44 RAG 数据助手 ─ N45 长上下文多模态应用 ─ N46 工具/通道安全
                └─ N47 Agent-Config 元竞赛 ─ N48 LLM 辅助环境移植
I 平台/工程 ──── N49 URL→feather/datatable/LMDB/HDF5 ─ N50 JPEG 压缩（71GB→14GB）
                └─ N51 提交沙箱与 schema ─ N52 云额度/计费管理
```

## 1. GBDT / 表格基线链（N01–N08）

| 节点 | 技法 | 传播路径 | 证据场次 | 边界/失败条件 |
| --- | --- | --- | --- | --- |
| N01 | XGB/LGBM 单模基线 | Playground 全系默认起点 | s3e9/s3e23/s3e25 等 | 单模封顶后需要多样性 |
| N02 | CatBoost 原生类别 | 高基数类别不 one-hot | s3e23（7 模型配方） | 类别极多时训练变慢 |
| N03 | 异质集成（6 树+1 非树） | 胜利说明书 445245 → #2 八模型 450315 | s3e23 | 非树成员增益极小（+3e-4） |
| N04 | 爬山权重搜索（允许负权重） | 444784 → 450315 | s3e23 | 折间不稳时权重过拟合 |
| N05 | OOF 权重/二级栈 | Stacking 常规 | s3e9/s3e23 | 需无泄漏 OOF |
| N06 | AutoML 栈（LAML/AutoGluon） | Nov2022 3rd → planttraits 6th | tps-nov-2022 / planttraits2024 | 定制受限、调参不透明 |
| N07 | 伪标签迭代 | 多处独立出现 | s5e9（26th）/sorghum（2nd/1st） | 低信号场次无对照不可信 |
| N08 | log 变换/后处理截断 | s3e23 提示 → s3e25/s3e8 | 多处 | 与目标分布形状绑定 |

## 2. 度量学习与检索链（N09–N15）

| 节点 | 技法 | 传播路径 | 证据场次 | 边界/失败条件 |
| --- | --- | --- | --- | --- |
| N09 | ArcFace 度量损失 | 细粒度检索标配 | hotel-id 1st/2nd、sorghum 3rd | 需稳定大类数 |
| N10 | subcenter-ArcFace + 动态 margin | hotel-id 2nd → herbarium 1st | hotel-id / herbarium-2022 | 类别 <10 图时无意义 |
| N11 | 分类 + 度量混合头 | herbarium 1st（CE 头并入 arcface 输出） | herbarium-2022 | 权重需调 |
| N12 | 嵌入 PCA + kNN 检索 | hotel-id 1st（1536D→PCA 3072D→KNN） | hotel-id | logits 路线可替代 |
| N13 | 双塔/DOLG 检索 | hotel-id 3rd；wikipedia 双塔 | hotel-id / wikipedia-image-caption | 域差大时退化 |
| N14 | 遮挡/掩码专用增强（BlendFlip） | hotel-id 1st 自研 | hotel-id | 提升约 0.03–0.04 mAP（自述） |
| N15 | DeepMAC 掩码 chip | iwildcam 9th（掩码质心自编码器） | iwildcam2022 | 全集上跟踪未兑现 |

## 3. 多模态融合链（N16–N21）

| 节点 | 技法 | 传播路径 | 证据场次 | 边界/失败条件 |
| --- | --- | --- | --- | --- |
| N16 | CNN + 表格 concat/dropout | 遥感 + 协变量标配 | geolifeclef 1st/2nd、planttraits | 协变量塞进 CNN 常失败 |
| N17 | 结构化自注意力（元数据） | planttraits 1st（PCA 失败后） | planttraits2024 | 需要元数据变量分组 |
| N18 | 三头：回归+硬分类+软分类 | PlantHydra | planttraits2024 | 依赖物种聚类质量 |
| N19 | 物种/聚类身份辅助任务 | 1st 三头；6th 标签链 | planttraits2024 | 聚类数由性状唯一组合决定 |
| N20 | Transformer 融合 | AutoGluon 多模态略胜 MLP | planttraits2024 | 超参/框架黑箱 |
| N21 | 大模型 embedding + GBDT | DINOv2+CatBoost 9th；EVA 系列 | planttraits2024 | 不同 embedding 融合无效 |

## 4. 时序/生存/物理链（N22–N26）

| 节点 | 技法 | 传播路径 | 证据场次 | 边界/失败条件 |
| --- | --- | --- | --- | --- |
| N22 | ARIMA 基线 | WiDS 资源推荐的时序起点 | phase-ii-widsdatathon2022 | 非线性/多变量受限 |
| N23 | GAM / 期望点（EP） | nflWAR：EP 作为 WP 输入 | nfl-bdb-2023/2024 | 需事件概率模型 |
| N24 | Cox 生存模型 | 马疝痛文献基线 | s3e22 | 比例风险假设 |
| N25 | 事件概率→期望→差分（EPA/WPA） | nflWAR 链 | nfl-bdb-2023/2024 | 需要可解释状态定义 |
| N26 | "截至当前"滚动聚合 | scrabble 历史 min/max/mean | scrabble-player-rating | 必须严格排除当前局 |

## 5. 验证与选择链（N27–N33）

| 节点 | 技法 | 传播路径 | 证据场次 | 边界/失败条件 |
| --- | --- | --- | --- | --- |
| N27 | 普通 KFold | 默认口径 | 全系 | 实体重复/时序泄漏时偏乐观 |
| N28 | 分层多标签 CV | MultilabelStratifiedKFold | s3e18（11th） | 标签极稀时分层退化 |
| N29 | GroupKFold 实体隔离 | scrabble 按 nickname；s3e22 按 hospital_number | scrabble / s3e22 | 分组后分数更低≠错（可能更真实） |
| N30 | 对抗验证 | 原数据可否并入 | s3e18（419685）、原数据族 | 只证明分布一致 |
| N31 | CV/LB 样本量：测量 vs 随机变量 | S3E9 ambrosm（5407 vs 721） | s3e9 | 依赖样本量差 |
| N32 | 随机目标 z 检验 | S5E9（100 次打乱，z=-0.83） | s5e9 | 只判原数据信号 |
| N33 | OOF 选模 / 融合判据 | autonomous-agent 3rd；大量赛后复盘 | autonomous-agent / 多处 | P2 选择噪声存在 +0.0005/−0.0166 |

## 6. 后处理 / 校准链（N34–N38）

| 节点 | 技法 | 传播路径 | 证据场次 | 边界/失败条件 |
| --- | --- | --- | --- | --- |
| N34 | clip / 分位裁剪 | 常规 | 多处 | 阈值经验化 |
| N35 | isotonic 校准 | Nov2022 3rd 拿第 3 | tps-nov-2022 | 小数据易过拟合阶梯 |
| N36 | 单参数 logit 平移（−1.17） | Nov2022 overlooked 机制帖 | tps-nov-2022 | 只在已知偏差方向有效 |
| N37 | 分组合法性裁剪 | S3E8 8th（Q3+1.5IQR 上界/下界 +1.1） | s3e8 | 依赖分组样本量 |
| N38 | 指标形态整形（档位/样本权重） | MedAE 权重（0.01）+9 档分箱 | s3e25 | 需测试同分布 |

## 7. RL / 自对弈链（N39–N43）

| 节点 | 技法 | 传播路径 | 证据场次 | 边界/失败条件 |
| --- | --- | --- | --- | --- |
| N39 | PPO 基线 | Parametrix 基线 → Lux S2 | lux-ai-s2 系 | 需要 shaped reward 起训 |
| N40 | 课程学习（16→32→64 地图） | PPO+Jux 逐步热启动 | lux-ai-s2-neurips | 小图难度未必随尺寸下降 |
| N41 | JAX 向量化环境 | Jux fork；maze-crawler 3rd 自研移植 | lux / maze-crawler | 移植成本高 |
| N42 | 行为克隆 bootstrap | maze 3rd（每日 episodes 数据） | maze-crawler | 依赖高质量示范 |
| N43 | 自对弈对手多样性 | maze 3rd 反思（AlphaStar 式） | maze-crawler | 同质池→策略短板 |

## 8. Agent / LLM 链（N44–N48）

| 节点 | 技法 | 传播路径 | 证据场次 | 边界/失败条件 |
| --- | --- | --- | --- | --- |
| N44 | RAG 数据助手 | Gemma 系列（从零 RAG/多实现） | data-assistants-with-gemma | 小模型需精调补格式 |
| N45 | 长上下文多模态应用 | Gemini 1.5 四冠军全视频类 | gemini-long-context | 配额/限流/挂载配置 |
| N46 | 工具/通道安全 | gpt-oss 红队：工具通道、CoT 伪造、reasoning_effort | openai-gpt-oss-20b-red-teaming | low/high 复现差异 |
| N47 | Agent-Config 元竞赛 | 提交会自己建模的 agent | autonomous-agent-prediction-beta | schema/工具兼容/预算 |
| N48 | LLM 辅助环境移植 | maze 3rd 用 LLM 写 JAX 端口 | maze-crawler | 需人工验证语义 |

## 9. 平台 / 工程链（N49–N52）

| 节点 | 技法 | 传播路径 | 证据场次 | 边界/失败条件 |
| --- | --- | --- | --- | --- |
| N49 | URL→feather/datatable/LMDB/HDF5 | wikipedia 图像 I/O 帖 | wikipedia-image-caption | 内存/并发瓶颈 |
| N50 | JPEG 压缩（71GB→14GB） | sorghum 社区数据集 | sorghum-id-fgvc-9 | 有损但任务容忍 |
| N51 | 提交沙箱与 schema | BigQuery 复现评审；zip/PostProcessorKernel；agent schema | bigquery / gan / autonomous-agent | 格式错误直接淘汰 |
| N52 | 云额度/计费管理 | BigQuery $300+$50+$5；OpenAI API 成本 | bigquery-ai-hackathon / openai-to-z | 项目暂停/账单风险 |

## 10. 传播链示例（跨节点路径）

1. **度量学习链**：Hotel-ID 2021（Swin+ArcFace+DBA）→ Hotel-ID 2022 1st（BlendFlip+5 模型，N09/N12/N14）→ Hotel-ID 2022 2nd（subcenter 动态 margin，N10）→ Herbarium 2022 1st（多级 CE+subcenter，N10/N11）→ Sorghum 3rd（ArcFace+域适应，N09）。
2. **表格配方链**：Playground 单模基线（N01）→ S3E23 七模型配方（N02/N03）→ S3E23 #2 八模型 + 爬山（N04）→ AutoGluon/LAML 自动栈（N06）→ 元 agent 的 OOF 选模（N33）。
3. **校准链**：Nov2022 的单参数平移（N36）与 isotonic（N35）→ MedAE 的样本权重/档位整形（N38）→ Hotel/Herbarium 的后处理（N34）。
4. **验证链**：KFold（N27）→ 分层多标签（N28）→ 实体分组（N29）→ 对抗验证（N30）→ "测量 vs 随机变量"的 CV/LB 论（N31）→ 随机目标检验（N32）→ OOF 选择纪律（N33）。
5. **RL 链**：PPO（N39）→ 课程学习（N40）→ JAX 向量化（N41）→ 行为克隆 bootstrap（N42）→ 对手多样性反思（N43）。

## 11. 失败传播链（未被继承的技法）

| 失败技法 | 场次 | 失败方式 |
| --- | --- | --- |
| class-aware sampling | herbarium-2022 1st | 长尾重采样无效（度量损失更有效） |
| data cleaning | herbarium-2022 1st | 对最终分数无贡献 |
| Optuna 无种子稳定性检验 | s3e9 1st/12th | 换 KFold 种子后最优参数消失 |
| PCA 降维 | s3e23 #2 | >99% 方差但掉分 |
| 帧间跟踪（全集） | iwildcam 9th | 小范围有效，全量不兑现 |
| 端到端 RL（Kore beta） | kore-2022-beta | 打不过规则型/示例微调 |
| 多标签聚合 | geolifeclef 1st | 未能优于单标签 + 邻域松弛 |

## 12. 使用与维护

- 引用某节点时，请回到对应 `analysis/deep/<slug>.md` 与 `analysis/claims.csv` 的数字行核对；
- 节点表示"在该比赛语境下被验证过/被证伪过"，不等于通用最优；
- 新增场次时按同一模板追加节点，并同步更新 `analysis/limitations.md` 的证据边界。
