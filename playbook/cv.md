# Playbook：计算机视觉

> 版本：v1.2（定稿）｜ 依据：`notes/cv/` 全部 49 篇摘要（该主题 49/49 已完成）
> 覆盖：RSNA 系列（2022/2023/2024/乳腺/颅内动脉瘤/MICCAI）、HuBMAP 系列、Vesuvius 系列（墨迹/表面）、IMC 系列（2022–2025）、
> FGVC 系列（Herbarium/Sorghum/Hotel-ID/iWildCam）、病理（UBC-OCEAN/Mayo）、细粒度与检索（Happywhale/Google UIE）、
> 视频与追踪（DFL/NFL/TensorFlow GBR）、数字化（ECG/Benetech）、生成（SD→Prompts）、合成检测等
> 已含入门/研究型条目（gan-getting-started、wikipedia-image-caption）与 NFL 头盔分配

## 1. 分型：先判断任务骨架

| 子类型 | 代表 | 关键约束 |
| --- | --- | --- |
| 整图分类/回归 | PetFinder、ISIC 2024、PlantTraits | 增强配方 + 预训练骨干 |
| 检测 / 分割 | Sartorius、Blood Vessel、RSNA 2022 | 分辨率、后处理、细结构损失 |
| 超高分辨率医学（WSI/CT/MRI） | RSNA 乳腺、UBC-OCEAN、Mayo、HuBMAP | 分块/降采样、多视角聚合、极低阳性率 |
| 3D / 科学体数据 | Vesuvius、CZII、BYU Motors、Biohub | 各向异性、显存、检测→关联 |
| 检索 / 匹配 / 重建 | IMC 系列、Google UIE、Hotel-ID | 嵌入、几何验证、跨域 |
| 视频 / 事件 / 追踪 | DFL、iWildCam、TensorFlow GBR | 相机运动、跨帧关联、序列验证 |
| 生成 / 数字化 | SD→Prompts、ECG 数字化、Benetech | 输出表示设计、合成数据规模 |
| 开放集 / 异常 | FathomNet OOD、伪造检测 | 异常分数、校准 |

## 2. 跨比赛的第一性结论

1. **两阶段范式（定位 → 分类）** 是多部位/细粒度任务的默认骨架：RSNA 2022/2023/2024、颅内动脉瘤、Happywhale、Benetech、DFL 均如此；单阶段端到端在定位错误时会污染全流程。
2. **分辨率与聚合方式决定上限**：分块推理 + 拼接（3D 检测、WSI）、低→高分阶段训练（RSNA 乳腺）、单视角建模再按患者聚合、多中心稳健性评估。
3. **按实体分组验证是底线**：患者（RSNA 全系列）、视频序列（GBR）、扫描/样本（CZII）、多中心（HuBMAP）——随机切分 = 自欺。
4. **领域预训练/基础模型优先**：病理用领域骨干（UBC-OCEAN）、显微用 LiveCell（Sartorius）、医学用 HAI-DEF/MedGemma 类；从零训 patch 编码器不划算。
5. **标注噪声/歧义是常态**：软标签与一致性过滤（HuBMAP 血管）、几何一致性约束（Contrails 禁翻转/旋转）、部分标注用 masked loss（UWMGI）。
6. **输出表示比 backbone 更重要**：SDF 回归替代二值分割（Vesuvius 表面）、热图回归替代坐标回归（BYU Motors）、边界型损失（血管）、直接回归嵌入而非生成文本（SD→Prompts）。
7. **检测 + 关联 + 计数**是视频/生物追踪的通用骨架：iWildCam、Biohub、DFL 三段式。
8. **指标特殊性必须显式处理**：pAUC（ISIC 2024 只优化决策区间）、概率任务的校准与阈值（乳腺、Vesuvius）、开放集要设计异常分数（FathomNet）。

## 3. 工具箱

### 3.1 分类 / 细粒度

- 增强配方（长宽比裁剪 + 面积采样 + HSV 抖动，Petfinder）几乎可通用；但与任务几何冲突时禁用（Contrails）。
- 细粒度：类间相似度分析找易混对（Sorghum）、局部特征/注意力/多尺度（Herbarium）、遮挡专用增强（Hotel-ID）、长尾重采样/损失重加权。
- 元数据：强相关时当辅助任务标签（PetFinder），弱相关但有效时双线融合（ISIC 2024）。

### 3.2 检测 / 分割

- 工具链：nnU-Net 系、Mask R-CNN/Detectron2/Cellpose（按数据选）；2.5D 折中；检测器集成的元分类器融合（颅内动脉瘤）。
- 结构：分块推理 + 合并；辅助分割任务提升主任务（RSNA 2022）；瓶颈分析决定投入（Sartorius：检测 vs 分割 vs 后处理）。
- 细结构：专用损失 + 连通性后处理（血管、裂缝、道路通用）。

### 3.3 超高分辨率医学 / 病理

- WSI：patch 特征 + MIL 聚合、染色归一化（跨中心必备）、openslide；先单视角/单切片再聚合。
- 工程：分阶段分辨率（低→高）、DALI 等加速、大显存或分块推理。
- 稳定性：多中心稳健评估（UBC-OCEAN）；建立自己的"任务检查清单"（Mayo STRIP 的做法）。

### 3.4 视频 / 追踪

- 先做相机运动补偿再谈识别（DFL）；跨帧平滑/投票后处理（GBR）；轨迹级优化替代逐帧独立预测。
- 追踪任务用向量场/中心回归分离接触实例（Biohub）。

### 3.5 匹配 / 检索 / 重建

- 现代 SfM 标准件：学习型特征 + 匹配器 + **几何验证**；先 kNN 检索缩规模再精细匹配（IMC 2024）。
- 两级范式：先聚类分组、再组内精细对齐（IMC 2025，顺序不能反）。
- 跨域检索：均衡训练 + 难负样本 + 半监督自训练（Google UIE）；嵌入 PCA 降维去噪（Hotel-ID）。

### 3.6 生成 / 数字化

- 指标是嵌入相似度 → 直接回归嵌入（SD→Prompts）；合成数据规模 = 竞争上限。
- 图像→数值信号：分阶段（分割→标定→提取）+ 几何约束，忌端到端回归（ECG 数字化）。
- 图表理解：先分类再按类型条件化解码（Benetech）。

## 4. 年度演进

- **2021–2022**：CNN/骨干迁移 + 检测分割框架成熟；FGVC9、RSNA 2022、HuBMAP、Petfinder、GBR——分组验证与增强配方成为常识。
- **2023**：3D 医学与体数据兴起（Vesuvius 墨迹、Biohub、CZII 前奏）；IMC 转向学习型匹配；软标签/噪声处理（HuBMAP、Contrails）。
- **2024**：RSNA 2024 腰椎确立"定位→分类"定式；IMC 工具链化（LoFTR/ALIKED 系）；pAUC 等特殊指标优化（ISIC）。
- **2025–2026**：领域基础模型普及（UBC-OCEAN、NFL 2026）；开放集检测（FathomNet）；Vesuvius 表面用 SDF 回归；对称性增强 + 多智能体建模（NFL 2025/2026）；生成式与数字化任务增多。

## 5. 常见坑

| 坑 | 证据 |
| --- | --- |
| 随机分帧/切片（视频、WSI、体数据） | TensorFlow GBR、UWMGI、CZII |
| 默认全套几何增强破坏标签一致性 | Contrails（禁翻转/旋转是正确决策） |
| 假设标注完美 | HuBMAP（软标签/一致性过滤） |
| 跳过几何验证 | IMC 2024（误匹配毁掉重建） |
| 各向同性假设处理各向异性体数据 | CZII |
| 小样本堆大模型/复杂集成 | RSNA-MICCAI（已证否） |
| 忽视方向/层面定位直接分类 | RSNA 2024（定位错误污染全流程） |
| 用常规 AUC 思路优化 pAUC | ISIC 2024 |

## 6. 新手学习路径

1. **分类/回归基本功**：PetFinder（增强配方 + 辅助任务）→ PlantTraits（多任务/综述）。
2. **检测与分割**：Sartorius（瓶颈分析）→ RSNA 2022（两阶段 + 辅助分割）。
3. **超高分辨率医学**：RSNA 乳腺（分组 + 分阶段分辨率）→ Mayo STRIP（任务清单方法）。
4. **3D / 科学影像**：Vesuvius 墨迹（大切块 + 上下文）→ Vesuvius 表面（SDF 回归）。
5. **检索 / 匹配 / 重建**：IMC 2024 → IMC 2025（聚类 + 对齐）。
6. **视频 / 追踪**：DFL（相机补偿 + 轨迹优化）→ iWildCam（检测+关联+计数）。

> 提示：每进入一个新子领域，先找该场的"任务检查清单/综述帖"（Mayo、PlantTraits），再进代码。

## 7. v2 增补（Tier B 204 场，2026-10）

1. **域适应组合拳**：多来源采集的细粒度分类 = 高分辨率 + IBN/直方图均衡 + 度量损失 + 外部数据/伪标签 + 集成/TTA。sorghum 3rd 的单项增益：直方图均衡 +0.03、IBN +0.05、ArcFace +0.015、512→1024 +0.04、FGVC8 +0.03、TTA +0.02（L129）。
2. **无 GT 的检测/计数**：不训练也能靠过滤进前列——按"每图 >8 框"分密度切换阈值/NMS（1st public MAE 0.247 vs 9th 的跟踪 0.265/0.275）（L128，iwildcam）。
3. **未知类检测（OSD）**：`1 − max(class prob)` + 集成标准差是强基线；<10 图类别并入 unknown + label smoothing 0.1（fathomnet 4th）。
4. **标签病态松弛**：presence-only 单标签用同网格邻域换标（10%）+2%；长尾按测试分布决定是否处理（L130，geolifeclef-2022）。
5. **长尾 + 层级错误**：先统计类别样本数与层级一致性，157/290 类无图时要归并 unknown，而不是硬训（fathomnet）。
6. **身份辅助任务**：目标与"物种/群体身份"强相关时，硬分类 + 软分类 + 回归三头融合优于纯回归（L121，planttraits 1st）。
7. **分层学习率**：头/融合权重高 LR 早 warmup，骨干按层组递减（L120，PlantHydra 调度图）。
8. **提交契约**：列顺序必须与 sample_submission 完全一致；zip/images.zip 结构与 PostProcessorKernel 先跑通最小提交（L122，planttraits/gan）。
9. **研究型 CV 赛**：GeoLifeCLEF 的 working note 是第二交付物（6/7→7/8，CEUR-WS/LNCS），数据获取（Seafile/ClimateClef）常比建模更耗时（geolifeclef-2022/2024）。

## 8. 检查清单（v2，可打印）

- [ ] 分辨率上限实验（512 vs 960/1024）（L129）
- [ ] 域适应方案：IBN / 直方图均衡 / 颜色归一化，先用分布可视化选（L129）
- [ ] 度量损失（ArcFace/subcenter/动态 margin）与分类头组合（L129）
- [ ] 遮挡/掩码增强与测试分布对齐（hotel-id BlendFlip）
- [ ] 无 GT 检测/计数：密度分层 + NMS + 阈值分桶（L128）
- [ ] 未知类检测：1−max(prob) + 集成标准差 + 阈值校准（fathomnet）
- [ ] 长尾：<N 图类别归 unknown + label smoothing；先确认测试分布（L130/F4）
- [ ] 身份辅助任务（物种/聚类/软分类头）（L121）
- [ ] 分层学习率与冻结/解冻计划（L120）
- [ ] 外部数据先映射/对抗验证；伪标签同折对照（L131/T6）
- [ ] TTA / 多尺度 / 多骨干融合（L129）
- [ ] 提交契约：列顺序、zip、PostProcessorKernel（L122）
- [ ] 架构/分数表/校准图截图入库 `images_index.csv`
