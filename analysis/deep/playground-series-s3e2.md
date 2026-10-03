# Playground Series S3E2（中风预测）轻量深读（Tier B）

> 赛事：Playground ｜ 主题 tabular（医疗二分类，AUC，强不平衡）｜ 770 队 ｜ 标准赛 ｜ 指标：ROC AUC
> 材料基础：`digests/playground-series-s3e2.md`（6 篇正文：1st 378795 / 5th 378780 / 88th 378879 / "Never get married!" 377253 / 8th 381377 / 6th 378866；67 条主题索引）+ 1 张归档图
> 轻读时间：2026-10（Tier B B15）

## 1. 一句话重述与数字账

从不平衡的医疗表格数据预测中风（AUC）。本场方法朴素但两个教训锋利：①**原数据（中风病例）加入训练、CV 只算合成数据**，是全场共识做法；②**线性模型异常强**（社区帖"Lasso 效果很好"39 票；1st 的 LogisticRegression 私榜 0.89209，与 XGBoost 的差距很小），而 1st 的夺冠模型只是**调参 500 次的单 XGBoost + 5 模型平均**。此外，"已婚更危险"的 EDA 结论被**年龄混杂**推翻——是很好的因果推理教学案例。

| 关键数字 | 值 | 来源 |
| --- | --- | --- |
| 1st（378795） | 合成数据 + 原数据中风病例（**训练并入、CV 只用合成**，10 折 StratifiedKFold）；one-hot（稀疏/k−1）；**KNN 回归插补 BMI**；风险因子计数（比逻辑回归基线 +0.0008）；中心化/缩放；500 次随机超参搜索 ×10 折；最终 = **5 个最佳模型的全部折测试预测平均（共 50 份）**；其他模型：LR 私 0.89209、CatBoost 0.89799、NN 0.89423；"四类模型全混合"（200 份预测）私 0.89879 也能进前 10；TPOT 总是选 XGBoost | 378795 |
| 5th（378780） | 缺失填充：`smoking_status=Unknown → never smoked`、`gender=Other → Male`；**梯度下降 + 排名**融合；原数据拼接、验证只用合成数据；RFE 特征选择；自造比值/交互（age/bmi、age×bmi、glucose×bmi/…、hypertension×heart_disease）；失败：前向选择（集成只剩 XGB）、Mean/WoE/频率编码器 | 378780 |
| 88th（378879） | CatBoost/XGB/LGBM/Lasso 各 5 个（5 折）；**等权最好**；最佳混合给 CatBoost 双倍权重；风险因子计数无增益；smoking_status 序数编码略优于 one-hot；逐折小网格扰动参数只 +0.0002 | 378879 |
| 因果教训（377253） | 49 票 / 62 评论的 EDA 帖先得出"已婚风险更高"，随后被指出**年龄混杂**——控制年龄后结论反转（未婚者风险略高）；更新中致谢 paddykb/bcruise/behroozsohrabi | 377253 |
| 其他资源 | "Lasso 效果很好"（39 票 / 31 评论）；风险因子特征（28 票）；血糖/年龄/BMI 分组（27 票 / 15 评论）；"正确排名"（23 票）；"新工具不一定更好"（22 票 / 18 评论）；6th 用 Optuna 搜融合权重 | 索引 |

## 2. 逐方案对照矩阵

| 维度 | 1st | 5th | 88th |
| --- | --- | --- | --- |
| 模型 | 单 XGB + 5 模型平均 | LR/LGBM/CatBoost/XGB 异质集成 | 4 类模型 ×5 等权混合 |
| 原数据 | 训练并入、CV 排除 | 同 | 同 |
| 编码 | one-hot（稀疏/k−1） | RFE + 填充 | smoking 序数化 |
| 融合 | 简单平均 | 梯度下降 + 排名 | 等权（CatBoost 加倍更佳） |
| 关键点 | BMI KNN 插补、风险因子 | 缺失填充直觉 | 等权优于调权 |

## 3. 共识、分歧与裁决

### 共识一：原数据并入训练、CV 只算合成数据（1st/5th/88th；置信度高）

与 S3E3/S4E1/S3E11/S4E10 完全同型；1st 明确说这样避免对原数据过拟合。**裁决**：不平衡医疗赛的标准协议。置信度：高。

### 共识二：线性模型在本场与 GBDT 差距极小（1st/88th/社区帖；置信度中高）

1st 的 LogisticRegression 私 0.89209、Lasso 被社区称为"效果很好"（39 票）；88th 的四类混合里也有 Lasso。**裁决**：特征已高度线性/低秩时，先跑线性基线再决定是否上 GBDT。置信度：中高。

### 共识三：类别编码与缺失填充有稳定小增益（1st/5th/88th；置信度中高）

one-hot（或稀疏 k−1）够用，Mean/WoE/频率编码没有超过它；`Unknown→never smoked` 与 BMI 的 KNN 插补有效。**裁决**：先做语义化填充 + 简单编码，再尝试复杂编码。置信度：中高。

### 事件：因果混杂的教学案例（377253 的更新；置信度中高）

"已婚更危险"被年龄混杂推翻；社区在评论中完成了纠正。**裁决**：EDA 的组间差异必须做分层/回归控制后再下结论（此帖可作为负面案例归档）。置信度：中高。

### 事件：洗牌与集成深度（1st、5th、378754；置信度中）

数据高度不平衡 → AUC 方差大、洗牌明显（"Now that's a shake up!!" 24 票 / 19 评论）；1st 的简单平均与 5th 的梯度下降融合都能站住。**裁决**：不平衡场景下简单稳健的融合优于复杂权重。置信度：中。

## 4. 证据分级

| 断言 | 等级 | 说明 |
| --- | --- | --- |
| 1st 的 CV 协议与 50 份预测平均 | 自述 + notebook | 高 |
| 5th 的填充/特征/失败清单 | 自述 | 中高 |
| 88th 的等权结论 | 自述 | 中 |
| "已婚风险"因果反转 | 高票帖 + 更新 + 图 | 中高 |
| Lasso 的强度 | 39 票帖 + 多方案采用 | 中高 |

## 5. 悬案与缺口（登记）

- 2nd–4th、7th、9th–10th 方案未收录；
- 风险因子的临床定义清单未逐条核对；
- 洗牌幅度的量化未给出；
- **图证缺口**：无（1 张图，本深读内嵌 1 张）。

## 6. 图表证据

![控制年龄后的婚姻风险](../../intel/playground-series-s3e2/bodies/377253_img/01.png)

**图 1**（topic 377253）：按年龄分层的婚姻状态-中风概率曲线——控制年龄后，"已婚更危险"的结论反转（未婚者在高龄段略高），是混杂因素修正的直观证据。

## 7. 出处

- 1st（35 票 / 14 评论）：https://www.kaggle.com/competitions/playground-series-s3e2/discussion/378795
- 5th（46 票 / 22 评论）：https://www.kaggle.com/competitions/playground-series-s3e2/discussion/378780
- 88th 四模型混合（4 票）：https://www.kaggle.com/competitions/playground-series-s3e2/discussion/378879
- Never get married!（49 票 / 62 评论）：https://www.kaggle.com/competitions/playground-series-s3e2/discussion/377253
- 8th（5 票）：https://www.kaggle.com/competitions/playground-series-s3e2/discussion/381377
- 6th Optuna 权重（5 票）：https://www.kaggle.com/competitions/playground-series-s3e2/discussion/378866
- Lasso 效果很好（39 票 / 31 评论）：https://www.kaggle.com/competitions/playground-series-s3e2/discussion/377377
- 风险因子特征（28 票）：https://www.kaggle.com/competitions/playground-series-s3e2/discussion/377370
- 血糖/年龄/BMI 分组（27 票 / 15 评论）：https://www.kaggle.com/competitions/playground-series-s3e2/discussion/377135
