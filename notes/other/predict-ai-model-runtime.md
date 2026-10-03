# Google - Fast or Slow? Predict AI Model Runtime（精简）

> 主题：other ｜ 子类：systems ｜ 领域：编译器/系统性能 ｜ 类别：Research ｜ 截止：2023-11-17 ｜ 队伍数：616 ｜ 指标：运行时预测误差
> 出处：`intel/predict-ai-model-runtime/`（80 条主题索引 + 6 篇 write-up 正文）

## 任务

预测 **Triton 编译器配置在 GPU 上的执行时间**（由编译器中间表示 + 硬件参数预测性能），目标是加速自动调优（autotuning）。

## 关键要点

- 1st 的方法核心是"**剪枝 + 组合**"：先剪掉不可能的配置，再对候选建模——**先缩小搜索空间再预测**的经典系统优化思路。
- 输入是图/代码表示（Triton IR）+ 配置参数 → 本质是**结构化数据回归**（与图神经网络、序列建模相关）。
- 该主题属于"**ML for Systems**"：既不是纯 ML 比赛，也不是纯系统比赛。

## 可迁移要点

- **先剪枝再预测**：在组合空间巨大时，分类筛选往往比直接回归更有效（与 USPTO 的"候选生成 + 求解器选择"同构）。
- 结构化输入（图/IR）需要匹配的编码方式（GNN/序列模型）。
- 性能预测类任务对**特征工程（硬件参数 + 程序特征）**依赖很重。

## 出处

- 讨论区索引：`intel/predict-ai-model-runtime/topics.md`
- 1st（68 票）：https://www.kaggle.com/competitions/predict-ai-model-runtime/discussion/456343
- 10th 图 Transformer（25 票）：https://www.kaggle.com/competitions/predict-ai-model-runtime/discussion/456129
- 11th LightGBM（27 票）：https://www.kaggle.com/competitions/predict-ai-model-runtime/discussion/456092
