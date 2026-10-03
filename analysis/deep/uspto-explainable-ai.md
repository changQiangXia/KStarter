# USPTO Explainable AI 轻量深读（Tier B）

> 赛事：Featured ｜ 主题 nlp（检索 + 查询合成）｜ 571 队 ｜ 代码赛 ｜ 指标：`USPTO 59575`（AP@50 变体）
> 材料基础：`digests/uspto-explainable-ai.md`（6 篇正文：1st 522233 / 2nd 522258 / 4th 522200 / 6th 522202 / 7th"Magic" 522199 / 5th 522201；80 条主题索引）+ 6 张图
> 轻读时间：2026-10（Tier B B06）

## 1. 一句话重述与数字账

给 50 个目标专利，构造一个 Whoosh 查询（token 数受限）把它们检出来——本质是**在检索语法与计分规则的缝隙里做"查询合成"**。本场的头号变量不是模型，而是一个**计数与解析不一致的规则漏洞（"Magic"）**：用它能把 0.90 直接抬到 0.998。

| 关键数字 | 值 | 来源 |
| --- | --- | --- |
| 2nd（522258） | **使用 Magic：CV 0.99934 / pub 0.99849 / priv 0.99872；不用 Magic：0.89992/0.90295/0.90427**；两种 Magic：① 无空格的 AND（`ti:"abcd"ab:"efgh"clm:"ijkl"`）② 无空格 n-gram（`ti:"abcd/efgh/ijkl"`）；最终查询 = `(sub1 OR sub2 …) NOT (neg1 OR neg2 …)`（负子查询 +0.0002 CV）；自研 C++ 检索器（比 Python 快 5×、省内存 3×）；自建 CV：1975 年后随机 2500 行、且查询限定"不含非目标" | 522258 |
| 7th"Magic"帖（522199） | 披露机制：`count_query_tokens` 用空格切分统计，而 Whoosh 预处理会把 `~` 之类字符替换成空白 → **一个标题只花 1 个 token**；"用 25 个精确标题"即可 LB ≈0.8；配 cuDF 全 GPU 处理，notebook 1 分钟跑完 | 522199 |
| 1st（522233） | **纯模拟退火**：查询只用 AND/OR；用 `-` 省略 AND token；cpc 必须放最后（cpc 不能用 `-`）；候选子查询生成 = 单词集合按出现次数升序 + 集合交集逐步加入，直到只含目标；**用 cuPy `intersect1d` 求交集比 Python set 快 2–3× → 最后一天得以用满全部 cpc/title/abstract，名次从第 3 升到第 1**；内存只保留 test.csv 相关专利（2500×50） | 522233 |
| 4th（522200） | 双版本：**带 Magic LB 0.98**（把目标两两配对、用最多 25 个公共 token 的 AND 串连接，贪心只留"命中的恰是目标"的组合，词频低者优先，控制 10000 字符上限）；**不带 Magic LB 0.91**（对 `cpc:CPC(token OR …)` 形式做模拟退火，评估函数是 mAP 的期望近似）；预处理工程经验：预分词、bz2、leveldb（key→range→bz2）、哈希分库、断点 flag | 522200 |
| 6th（522202） | 自研 **C++ 检索器 + 替代指标**做验证（13M 专利建索引不可行）；分析 AP'@50 的实现缺陷与 padding 机制：`score1(25,0)=0.842`、`score1(50,50)=0.500` → **"结果里没有非目标"的期望分远高于混合**，因此解法应追求"零非目标"；用受限假设（无 proximity/权重/通配符）近似打分 | 522202 |
| 事件 | "Test set is public?"（21 票）、"Sharing my mistakes and learnings"（20 票）、Whoosh 高级用法帖（44 票）；多队承认 Magic 改变了整场策略（4th 说"很遗憾有这些 magic，我 10 天前才知道"） | 社区 |

## 2. 逐方案对照矩阵

| 维度 | 1st | 2nd | 4th | 6th |
| --- | --- | --- | --- | --- |
| Magic | 用（`-` 省略 AND） | **两种全用** | 带/不带双版本 | 不用（自建检索器） |
| 搜索 | 自研 + cuPy | 自研 C++ | Whoosh 测试 + 自研预处理 | 自研 C++ |
| 查询形态 | sub-query OR 组合 | OR + **NOT 负子查询** | 目标配对 + 公共 token AND 串 / SA | 子查询 OR |
| 优化法 | 模拟退火 | 贪心 + 候选筛选 | 贪心 / SA（期望 mAP 近似） | 约束下的近似评分 |
| priv | 1st | 0.99872（Magic） | 0.98（Magic）/0.91 | — |

## 3. 共识、分歧与裁决

### 共识一：能把 50 个目标"精确打包"就赢（2nd/4th/6th/7th）

6th 的数学分析给出根本原因：结果里混入非目标会大幅拉低期望分（25 目标+0 非目标 = 0.842，25+25 = 0.500）；Magic 让"一个标题=1 token"，于是 25 个精确标题几乎白送 0.8。**裁决**：本赛的最优策略是"**零非目标的精确检索**"，而不是"高召回 + 排序"；任何能压缩 token 成本的语法技巧都直接换算成分数。置信度：高（多队 + 数学/实证）。

### 共识二：Whoosh 的语法缝隙是本场的"元问题"（2nd/4th/7th）

无空格 AND、无空格 n-gram、`~` 当空白——三个变体都源于同一类"计数与解析不一致"。4th 明确"没有 Magic 上限 0.91，有 Magic 0.98+";2nd 差距 0.094。**裁决**：代码赛要优先审计"计分/预算统计代码 vs 实际执行引擎"的不一致；发现后应立即重排整场策略。置信度：高。

### 共识三：自研检索器是必须的工程（1st/2nd/6th）

Whoosh 无法承载 13M 专利全量索引；1st/2nd/6th 都写了自研（C++/cuPy）检索器，2nd 报"比 Python 快 5×、内存省 3×"；1st 最后一天靠 cuPy 交集提速 2–3× 才敢用满全字段（3rd→1st）。**裁决**：检索赛的胜负常在"能不能在时限内把全量数据用起来"。置信度：高。

### 分歧一：优化器选择（模拟退火 vs 贪心）

1st 用 SA（不含 Magic 也拿第 1）；2nd/4th 的 Magic 版用"目标配对 + 公共 token 贪心"；4th 的不含 Magic 版用 SA。**裁决**：如果 Magic 已把问题变成"打包目标"，贪心足够；没有 Magic 时，查询组合空间需要 SA/期望 mAP 近似来搜索。置信度：中高。

### 事件：评测实现缺陷与验证口径（6th）

6th 指出 AP'@50 的实现缺陷（padding 参与排序）并自建替代指标；2nd 也自建 CV（限定零非目标查询）以消除 CV-LB 差。**裁决**：当官方指标实现有缺陷时，自建"与榜一致"的近似指标是可行且必要的工程。置信度：中高。

## 4. 证据分级

| 断言 | 等级 | 说明 |
| --- | --- | --- |
| Magic 的机制与 0.8 效果 | 自述 + 可复现 notebook + 多队复现 | 高 |
| 2nd 的 0.99872/0.90427 对照 | 自述 + 表 | 高 |
| 6th 的 score1(n,m) 分析 | 自述 + 图 + 数学 | 中高 |
| 1st 的 SA + cuPy 提速（3rd→1st） | 自述 + 公开代码 | 中高 |
| 4th 的双版本与工程经验 | 自述 + 公开 notebook | 中高 |

## 5. 悬案与缺口（登记）

- 3rd/5th/11th 的方案未细读；"Whoosh 高级用法"（44 票）、"Test set is public?"（21 票）未细读；
- host 是否知晓 Magic、是否修正指标，材料无结论；
- 1st 未给 SA 的逐项消融（Magic 与 cuPy 各自的贡献）；
- 归档 6 图中 2nd 的三步流程图（图 1）为关键证据。

## 6. 图表证据

![2nd 的三步查询合成流程](../../intel/uspto-explainable-ai/bodies/522258_img/01.png)

**图 1**（topic 522258）：2nd 的管线——① 建 `patent_to_word`/`word_to_patent` 索引；② 对目标对生成候选子查询（取公共词、按出现数升序、逐步求交，**一旦剩余非目标无法用负子查询抵消就放弃**）；③ 按"能新增覆盖的目标数"贪心选子查询。图中同时给出打分示例（命中新目标数越多的候选越优）。

## 7. 出处

- 1st（39 票）：https://www.kaggle.com/competitions/uspto-explainable-ai/discussion/522233
- 2nd（29 票）：https://www.kaggle.com/competitions/uspto-explainable-ai/discussion/522258
- 4th（44 票）：https://www.kaggle.com/competitions/uspto-explainable-ai/discussion/522200
- 6th（24 票）：https://www.kaggle.com/competitions/uspto-explainable-ai/discussion/522202
- 7th"Magic"（522199）：https://www.kaggle.com/competitions/uspto-explainable-ai/discussion/522199
- Whoosh 技巧（44 票）：https://www.kaggle.com/competitions/uspto-explainable-ai/discussion/516104
