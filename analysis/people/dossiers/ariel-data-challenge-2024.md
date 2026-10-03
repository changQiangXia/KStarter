# NeurIPS - Ariel Data Challenge 2024

> `ariel-data-challenge-2024` ｜ Featured ｜ 指标 Ariel Gaussian Log Likelihood ｜ 1151 队 ｜ 截止 2024-10-31

本页汇总该场 **2 条 ≥50 票 GM 主题帖**、**10 条断言**、**1 条高票评论**。

## GM 主题帖

| 票 | 选手 | 日期 | 主题 |
| --- | --- | --- | --- |
| 125 | [@jeroencottaar](https://www.kaggle.com/jeroencottaar) | 2024-11-01 | [2nd place solution - pure Bayesian Inference, no deep learning](https://www.kaggle.com/competitions/ariel-data-challenge-2024/discussion/543853) |
| 51 | [@daiwakun](https://www.kaggle.com/daiwakun) | 2024-11-04 | [1st Place Solution](https://www.kaggle.com/competitions/ariel-data-challenge-2024/discussion/544317) |

## 断言（条件→动作→机制→结果）

| 选手 | 等级 | 阶段 | 动作（节选） | 出处 |
| --- | --- | --- | --- | --- |
| @jeroencottaar | A | 建模与训练 | 用多个 squared-exponential kernel 组合的 GP（按长度尺度调 sigma）；光谱漂移用 KISS-GP 稀疏化（否则 100k × 100k 稠密矩阵） | [ariel-data-challenge-2024#543853-02](https://www.kaggle.com/competitions/ariel-data-challenge-2024/discussion/543853) |
| @jeroencottaar | A | 建模与训练 | 迭代 7 次：初始猜测、在当前点线性化、标准 GP 求解、用后验均值作下一轮起点；推理期唯一调的超参（transit depth 幅度）用对数似然梯度下降，并设最小值防止 MLE  | [ariel-data-challenge-2024#543853-03](https://www.kaggle.com/competitions/ariel-data-challenge-2024/discussion/543853) |
| @jeroencottaar | A | 特征与数据工程 | 不能对训练标签做 PCA（测试分布不同）；先用全模型粗拟合 800 个行星，对结果做无中心 PCA（1 到 2 个形状，final 用 1 个），再带形状重拟合 | [ariel-data-challenge-2024#543853-04](https://www.kaggle.com/competitions/ariel-data-challenge-2024/discussion/543853) |
| @jeroencottaar | A | 复盘与流程 | 训练集上利用该共享加 0.005，但测试灾难（0.110）；另有 fudge：均值乘 1.0064（关键但作者不明原因），后经 cnumber 指出是漏了常数背景，开启 inclu | [ariel-data-challenge-2024#543853-05](https://www.kaggle.com/competitions/ariel-data-challenge-2024/discussion/543853) |
| @daiwakun | A | 数据工程 | 只用 AIRS-CH0（依赖相邻波长相关）；关闭 hot pixel 处理带来最大跳跃（热像素处理丢失中间像素、时变 PSF 噪声无法校正）；用 [0:8] 与 [24:32] 估 | [ariel-data-challenge-2024#544317-01](https://www.kaggle.com/competitions/ariel-data-challenge-2024/discussion/544317) |
| @daiwakun | A | 特征与数据工程 | 从 ExoSim2 代码得知 gain drift 形式为 (1 + f(t)×g(λ))，f 与 g 各 5 个参数多项式；直接拟合 y = I(λ)×Box(λ)×(1+f(t | [ariel-data-challenge-2024#544317-02](https://www.kaggle.com/competitions/ariel-data-challenge-2024/discussion/544317) |
| @daiwakun | A | 集成与融合 | GP 回归（RBF+Matérn 核、bootstrap 误差传入 sklearn GPR）、AutoEncoder（非线性、每行星归一化、移动中值平滑、隐藏 4 节点）与 NMF | [ariel-data-challenge-2024#544317-03](https://www.kaggle.com/competitions/ariel-data-challenge-2024/discussion/544317) |
| @daiwakun | A | 复盘与流程 | 最终 public 0.7330321 / private 0.7420624；仅 GP 0.7221480/0.7343485（-0.0108841/-0.0077139）；仅  | [ariel-data-challenge-2024#544317-04](https://www.kaggle.com/competitions/ariel-data-challenge-2024/discussion/544317) |
| @daiwakun | A | 复盘与流程 | 用 TauREx3 拟合已知气体吸收谱在训练集好但 LB 很差（大气组成漂移）；ML 去噪输入未能超过简单 [8:24] 求和；作者承认方案利用了模拟器细节；认为赛期短一天或长一天 | [ariel-data-challenge-2024#544317-05](https://www.kaggle.com/competitions/ariel-data-challenge-2024/discussion/544317) |
| @jeroencottaar | C | 建模与训练 | 用贝叶斯推断分层：prior=物理（噪声、漂移、transit 等分布），观测=测量，posterior=分解；从 posterior 采样得到 transit depth 与置信 | [ariel-data-challenge-2024#543853-01](https://www.kaggle.com/competitions/ariel-data-challenge-2024/discussion/543853) |

## 高票评论

| 票 | 选手 | 日期 | 摘录 | 出处 |
| --- | --- | --- | --- | --- |
| 12 | @jeroencottaar | 2024-11-02 | For Bayesian Inference, I only really have a reference if you want to learn it properly: Bayesian Data Analysi | [543853](https://www.kaggle.com/competitions/ariel-data-challenge-2024/discussion/543853) |

## 关联资产

- 深读：`analysis/deep/ariel-data-challenge-2024.md`
- 结构化摘要：`notes/science/ariel-data-challenge-2024.md`
- 归档讨论区：`intel/ariel-data-challenge-2024/`（主题 2 条有 ≥50 票帖，图证 7 个）
