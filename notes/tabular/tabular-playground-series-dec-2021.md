# Tabular Playground Series - Dec 2021（森林覆盖类型）

> 主题：tabular ｜ 子类：— ｜ 领域：地理/林业（CTGAN 合成数据）｜ 类别：Playground
> 截止：2021-12-31 ｜ 队伍数：1188 ｜ 机制：标准赛 ｜ 指标：Categorization Accuracy（7 类）
> 数据来源：`intel/tabular-playground-series-dec-2021/`（80 条主题索引 + 6 篇正文；深读升级 2026-10，Tier A #60；本场无可用归档图）

## 1. 任务与数据

- 预测目标：森林覆盖类型（多分类 Accuracy）；字段为地形/土壤/光照类地理特征（**非匿名化**，有物理含义）。
- **合成数据伪影**（全场核心）：`Aspect`（角度）出现 (-360,720) 越界值；三个 `Hillshade`（灰度）越界；距离字段出现负值——生成器（CTGAN 类）按边缘分布采样，未表达约束语义（bounds 被设为 None）。
- 社区爆款修复：**Aspect ±360 循环修正 + 三 Hillshade 截断到 [0,255]**（同网络 0.95631→0.95656→0.95673）；负距离置 0（+0.0053）。

## 2. 验证方案

| 方案 | 使用者 | 说明 |
| --- | --- | --- |
| CV-LB 一致性检验（修复 vs 还原） | 2nd | 向原始 Covertype 靠拢的改法 CV 极好但测试崩；只有局部修复（Aspect）+ 距离特征幸存 |
| 软投票（10 模型） | 2nd | 单模几乎收敛一致 → 平均概率突破 |
| 同架构不同 batch_size 再投票 | 2nd | 第二个突破：训练扰动制造多样性 |
| 伪标签消融 | 2nd / kaaveland | 结论分歧（2nd 变差；kaaveland 早期版本受益）——缺同代际 A/B |
| 类级诊断 | 社区（ambrosm） | "Eliminate cover type 4!" 类级模型进入 2nd 终版 blend |

## 3. 模型家族与方案谱系

| 方案 | 名次（票数） | 关键点与数字 |
| --- | --- | --- |
| 物理修复 + 距离特征 + 双软投票 + 公共 blend 策展 | 2nd（54） | 数十次"向原数据靠拢"失败；唯一幸存=欧氏/曼哈顿距离+Aspect；单模 0.9707；10 模型 soft voting；batch_size 扰动再投票；终版=自己×3 + mlanhenke×1 + kaaveland×3 + ambrosm×2（去伪标签） |
| 四列修复（Aspect+Hillshade） | Gulshan（62） | 同 NN 0.95631→0.95656→0.95673；评论区扩展负距离→0（+0.0053）；引发 CTGAN bounds 成因讨论 |
| Focal loss 处理不平衡 | Luca Massaron（23） | 改 loss 而非重采样/加权；gamma 强调难样本；多分类 TF/Keras 实现 |
| 2021 TPS 解法索引 | Vadim Irtlach（51） | Jan–Nov 全量前排解法链接——跨场谱系素材 |
| TPS 年度教训 | Remek Kinas（116） | 90% 数据/9% 模型/1% 调参；先有模型再调参；EDA 要 so what；看 fork 数；聚焦 |
| 收官现场 | Luca Massaron（13） | "巨大 shake-up"；伪标签分歧；Aspect 离散化+Top10 线性特征=999/1200 |

## 4. 关键技巧

- **物理范围审计清单**：角度是 0–359 循环量（±360）；灰度有界 [0,255]（截断）；距离非负（置 0）；比例字段 [0,1]。
- **修复 vs 还原**：局部去伪影（修不可能值）稳定正收益；全局向原始分布靠拢（土壤掩码、额外裁剪）CV 好但 LB 崩。
- **同质化对策**：soft voting + 同架构 batch_size/seed 扰动（比继续堆特征更有效）。
- **公共代码策展**：把已验证公共模型去掉伪标签后与私有强单模混合（2nd 的"打不过就改进它"）。
- **不平衡处理**：focal loss / 类级模型（cover type 4 专门化）。
- **实验管理**：Graphviz 实验树 + 电子表格记录（2nd）；看 fork 数而非票数（教训帖）。

## 5. 深读结论（2026-10 补）

**一句话**：这是一场"物理审计 + 抗同质化 blend + 公开代码策展"的比赛——特征修复决定入场，差异化与伪标签判断决定名次。

- 三处独立验证物理修复的稳定正收益；"向原始数据还原"被 2nd 的数十次失败证伪。
- 单模收敛一致 → 唯二突破口都是训练扰动软投票；最终名次由"私有强单模 + 去伪标签公共 blend"取得。
- 公开 notebook 经济让分数饱和（0.9709–0.9711 复制党）；差异化 = 公共品策展 × 私有强单模。
- 伪标签在合成数据上高风险（2nd 变差、前排疑似不用；kaaveland 的早期成功不可跨代际引用）。
- accuracy 指标对不平衡不友好（社区批评）；类级模型（cover type 4）是实际对策。

**数字账精选**：0.95631→0.95673（四列修复）；负距离 +0.0053；单模 0.9707、复制 blend 0.9709–0.9711；终版 3+1+3+2 模型；90-9-1 数据/模型/调参。

**失败学**：2nd 的原始数据靠拢/土壤掩码/额外裁剪/伪标签（一度想放弃）；社区的大面积特征工程无效；SeLU 之外的模型无差异化；复制党导致的名次饱和。

**悬案**：1st/3rd 方案未收录；"train/test 不重叠"帖（292381）上下文缺失；"不该用 accuracy"（293362）论证缺失；shake-up 成因未量化；**图证缺失**（293072_img 为空目录）。

## 6. 图表证据

**本场无可用归档图片**：`intel/tabular-playground-series-dec-2021/bodies/293072_img/` 为空目录（293072.html 内有 1 个 `<img>` 标签但未落盘）；其余 HTML 无 `<img>`。按"只用仓库内已归档图片"约束，无法内嵌图证，缺口已登记（阶段二图片层可复核）。

## 7. 可迁移性评估

- **可直接迁移**：
  - 字段物理范围审计（角度/灰度/距离/比例）作为建模前第一步；
  - "修复 vs 还原"判据与 CV 好/LB 崩的警报解释；
  - 同质化环境的训练扰动软投票；
  - 公开代码饱和下的策展公式（去伪标签 + 私有强单模）；
  - 伪标签的同代际消融纪律；不平衡的 focal loss / 类级处理。
- **需要前提**：字段非匿名化、有明确物理含义；数据为生成器合成（有伪影结构）；公开 notebook 生态存在。
- **不建议照搬**：把"改得像原始数据"当目标；跨代际引用伪标签成功案例；在匿名化比赛做物理审计（无从下手）。

## 8. 对新手的关键启示

1. **建模前先做物理范围审计**：角度、灰度、距离修一修就可能白捡分数。
2. **领域约束用在模型/验证设计里，不要硬改数据迎合原始分布**（本场实测失败）。
3. **公开 notebook 泛滥时，把精力放在"私有强单模 + 已验证成果的稳健策展"**，而不是参与复制。
4. **特征工程枯竭后，训练扰动（batch/seed）软投票是最后一块稳定增量**。
5. **伪标签要用同代际消融验证**；合成数据上默认保守。

## 9. 出处

- 讨论区索引：`intel/tabular-playground-series-dec-2021/topics.md`（80 条）
- 已收录正文（6 篇）：
  - TPS 2021 教训（116 票）：https://www.kaggle.com/competitions/tabular-playground-series-dec-2021/discussion/296842
  - 修复四列特征（62 票）：https://www.kaggle.com/competitions/tabular-playground-series-dec-2021/discussion/293373
  - 2nd 方案（54 票）：https://www.kaggle.com/competitions/tabular-playground-series-dec-2021/discussion/298304
  - 2021 Tabular 解法索引（51 票）：https://www.kaggle.com/competitions/tabular-playground-series-dec-2021/discussion/294062
  - Focal loss（23 票）：https://www.kaggle.com/competitions/tabular-playground-series-dec-2021/discussion/293072
  - 收官祝贺（13 票）：https://www.kaggle.com/competitions/tabular-playground-series-dec-2021/discussion/298131
- 深读全本：`analysis/deep/tabular-playground-series-dec-2021.md`（11 组件 + 机制推演 M1–M7）
- 缺口登记（未收录正文/图缺失）：293768、291844、293612、292823、291871、291832、293362、292381、292839、295617；293072_img 为空
