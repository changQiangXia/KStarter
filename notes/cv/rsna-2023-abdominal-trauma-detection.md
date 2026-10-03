# RSNA 2023 - Abdominal Trauma Detection

> 主题：cv ｜ 子类：— ｜ 领域：医疗影像 ｜ 类别：Featured
> 截止：2023-10-XX ｜ 队伍数：2000+ ｜ 机制：代码赛 ｜ 指标：多器官多标签（患者级 + 器官级）
> 数据来源：`intel/rsna-2023-abdominal-trauma-detection/`（80 条主题索引 + 6 篇 write-up 正文）

## 1. 任务与数据

- 预测目标：由腹部 CT 检测并分类多个器官的损伤（肝/脾/肾/肠等），含患者级"是否存在任何损伤"与器官级多标签。
- 数据形态：3D CT 序列 + 器官分割掩码；标注稀疏（损伤是少数切片）。
- 构造陷阱：**患者级与器官级指标混合**；不同器官的可见性与尺度差异大；正样本极不平衡。

## 2. 方案谱系

| 方案 | 名次 | 关键点 |
| --- | --- | --- |
| 两阶段（定位器官 → 器官级分类） | 1st | **4 折 GroupKFold（按患者分组）**；完整预处理与训练代码开源 |
| 复用往届 RSNA 经验 | 2nd | 作者明确说"结合了此前 RSNA 比赛中获得的知识"，投入远超本场的一个月 |
| 多方案 | 其他 | 见讨论区 |

## 3. 关键技巧

- **按患者分组验证**（RSNA 系列的统一要求）。
- **两阶段结构**：先用分割定位器官，再在器官 ROI 上分类。
- **系列经验复用**：同一系列（RSNA）比赛的方案可以跨年迁移。
- **注意到赛制变动**：2nd 明确抱怨"无理由延长截止时间"对参赛者的伤害——**规则变动会直接改变策略价值**，这类信息值得记录。

## 4. 可迁移性评估

- **可直接迁移**：
  - 多器官/多部位任务用"**定位 → 分类**"两阶段（与 RSNA 2024 腰椎、颅内动脉瘤同源）；
  - 患者级分组验证；
  - 系列赛事经验迁移。
- 需要前提：3D CT 处理与分割工具链。
- 不建议照搬：忽视赛制变动（截止延长会改变"何时定稿"的最优决策）。

## 5. 对新手的关键启示

1. **RSNA 系列的方法论高度一致**：患者级分组 + 器官定位 + 器官级分类。
2. **系列赛事是复用的富矿**（同一批人、相似数据、可迁移的流程）。
3. 关注赛制公告——规则变化会影响策略。

## 6. 出处

- 讨论区索引：`intel/rsna-2023-abdominal-trauma-detection/topics.md`（80 条）
- 已收录 write-up（6 篇）：
  - 1st Team Oxygen（133 票，完整代码已发布）：https://www.kaggle.com/competitions/rsna-2023-abdominal-trauma-detection/discussion/447449
  - 2nd（105 票）：https://www.kaggle.com/competitions/rsna-2023-abdominal-trauma-detection/discussion/447453
  - 3rd（53 票）：https://www.kaggle.com/competitions/rsna-2023-abdominal-trauma-detection/discussion/447464
  - 10th（38 票）：https://www.kaggle.com/competitions/rsna-2023-abdominal-trauma-detection/discussion/447450
