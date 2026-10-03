# 按赛型上分打法

> 每类给"优先级最高的 5 个动作 + 2 个致命坑"。赛前先归类，再按对应打法执行。

## 1. Playground / 表格回归与分类

**优先动作**：① 指标结构后处理（中位数/分位/阈值）；② 主体 CV 纪律（实体/时间）；③ 合成赛随机目标检验；④ 清洗三件套（坏值/重复/近常数）；⑤ 异质集成（6 树 + 1 非树）或 AutoML 栈。
**致命坑**：LB 微差选模；低信号场堆大集成。
**证据**：s3e25、s5e9、s3e18、s3e23、s3e9。

## 2. CV / 视觉比赛

**优先动作**：① 分辨率与域适应（IBN/直方图）组合；② 度量损失 + 分类头；③ 掩码/遮挡按测试分布增强；④ 多尺度 TTA/多骨干融合；⑤ 提交格式与列顺序保护。
**致命坑**：忽略 train/test 域差直接调骨干；长尾归并不慎伤 top-K。
**证据**：sorghum、hotel-id、planttraits、herbarium、fathomnet、iwildcam。

## 3. NLP / LLM 比赛

**优先动作**：① 先判题型（理解/生成/检索/安全/Agent）；② 输出可机读 + 评分口径进 prompt；③ few-shot 稳定性测试；④ 大数据 I/O 与检索骨架复用；⑤ LLM 引用/语义核验。
**致命坑**：无 CV 的公开 prompt/方案照抄；把 LLM 输出当事实。
**证据**：makersuite、wikipedia-image-caption、gpt-oss、autonomous-agent。

## 4. 时序 / 金融

**优先动作**：① 时间切分 + purge/embargo；② 截止当前滚动特征；③ 指标口径（预测期/单位）核对；④ 稳健损失与分布整形；⑤ 在线重训 vs 集成宽度的预算取舍。
**致命坑**：随机 KFold 造成时间穿越；用未来信息构造特征。
**证据**：tps-nov-2022、scrabble、amex、predict-energy。

## 5. 模拟对战 / RL Agent

**优先动作**：① 规则基线（评分函数/兵力计算）先行；② 快模拟器/向量化环境；③ 课程学习 + 最佳 checkpoint 热启动；④ 对手多样性与镜像鲁棒性；⑤ 监控 KL/资源/胜率拐点早停。
**致命坑**：端到端 RL 无课程直接上大场景；自对弈池同质导致偏科。
**证据**：kore-2022-beta、maze-crawler、lux-ai-s2-neurips。

## 6. 评审制 / 分析 / 研究赛

**优先动作**：① 按"观察→改动→验证"闭环写交付；② 消融 + 失败路径 + 少而精图表；③ 可复现（公开 notebook/模型/数据链接）；④ 规则与字数/图表限制合规；⑤ working note/论文按时提交。
**致命坑**：只报最终结果；依赖私有依赖导致评审无法复现。
**证据**：pokemon-strategy、nfl-bdb、bigquery、geolifeclef、med-gemma。

## 7. Getting Started / 学习型

**优先动作**：① 先跑通官方教程与提交链路；② 复现一个经典方案；③ 建立自己的实验模板；④ 记录可迁移技巧；⑤ 控制算力成本。
**致命坑**：追求排名而跳过基础；在无评测的场次过度优化。
**证据**：gan-getting-started。

## 8. Agent-Config / LLM 应用赛

**优先动作**：① schema 本地校验；② 预算感知工作流（锚点→迭代）；③ 模型-工具兼容适配；④ 思考死循环/超时保护；⑤ 交付自包含（自包含 notebook/视频/数据集）。
**致命坑**：未本地校验就消耗提交；预算烧在探索。
**证据**：autonomous-agent-prediction-beta、gemini-long-context、data-assistants-with-gemma。
