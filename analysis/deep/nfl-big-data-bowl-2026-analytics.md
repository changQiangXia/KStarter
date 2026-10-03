# NFL Big Data Bowl 2026 – Analytics Track 轻量深读（Tier B）

> 赛事：Featured（评审制 analytics）｜ 主题 cv/tracking（NFL 传球在空中阶段的球员移动）｜ 277 队 ｜ 截止 2025-12-17
> 材料基础：`digests/nfl-big-data-bowl-2026-analytics.md`（6 篇正文：起步与 Discord 609278 / 2025 冠军 AMA 与补充数据 614950 / 官方欢迎 609370 / 结果延期询问 670213 / 编辑已提交 writeup 663242 / 获奖公布 670745；41 条主题索引）+ 0 张归档图
> 轻读时间：2026-10（Tier B B20）

## 1. 一句话重述与数字账

第八届 BDB 的 Analytics 赛道：主题是**球在空中这段时间里球员怎么移动**（从 snap 到出手决策的传球进攻演化），官方希望产出新的进攻/防守球员指标。系列赛的"就业管线"在本场被再次验证：2025 冠军 Vishakh Sandwar 借比赛进入 SumerSports，并**开源生产数据补充（帧级防守覆盖 + 球员级覆盖细节）与 man/zone 分类的 Transformer 代码**，成为本届最热的社区资源。与此同时，讨论区显示数据口径问题（ball_land、player_to_predict、frame、朝向、加速度）与提交流程（"evaluation system not configured"、编辑 writeup）是主要摩擦点。

| 关键数字 | 值 | 来源 |
| --- | --- | --- |
| 规模与机制 | **277 队**；Analytics 赛道（评审制，另有 Broadcast Visualization 赛道）；截止 2025-12-17；原定 2026-01-20 出结果，1/26 仍在等（16 票帖） | 609370 / 670213 / 索引 |
| 主题 | 球在空中阶段的球员移动；官方希望形成新的进攻/防守球员统计，理解"从 snap 到出手决策"的传球演化；强调 BDB→体育分析就业管线 | 609370 |
| 冠军生态资源 | 2025 冠军 @VishakhSandwar 的开源补充：**帧级 coverage scheme + 球员级 coverage 细节**数据集；基于 Udit Ranasaria & Pavel Vabishchevich 的 Transformer 改造成 **man vs zone** 分类 notebook；SumerSports 博客；作者在讨论区持续 AMA | 614950 |
| 社区选题讨论 | "novel data analytics you can do"（4 票）；"Describe a Play. Find Similar Ones."（4 票）；Safety Range Visualizer（2 票）；Broadcast Visualization 提交讨论；用 Gemini 3 做可视化（1 帖） | 索引 |
| 数据口径问题 | `ball_land` 不一致（4 评论）；`player_to_predict` 澄清；每 play 球员数；`frame_id`；朝向；加速度值；字段名；dropback 距离；球落点数据；team coverage type；data subset/requirements/outside data | 610834 / 613454 / 612717 / 614459 / 613468 / 657011 / 610026 / 639412 / 656536 / 656945 / 651738 |
| 提交/资格摩擦 | "Cannot submit – evaluation system has not been configured"（3 评论）；编辑已提交 writeup（663242）；notebook 提交与上传问题；非美学生资格；2027 预告 | 663170 / 663242 / 索引 |

## 2. 逐方案对照矩阵

| 维度 | 官方期待 | 社区提供 | 风险 |
| --- | --- | --- | --- |
| 选题 | 空中阶段的新球员指标 | 相似 play 检索、安全范围可视化、覆盖分类 | 与 2024/2025 主题重复 |
| 数据 | NFL 追踪/事件数据 | 2025 冠军的 coverage 补充数据 | 字段口径不一致 |
| 交付 | Analytics writeup + 图表 | 开源 notebook/Transformer 基线 | 提交系统与资格问题 |
| 回报 | 奖项 + 就业管线 | AMA + 博客 + 开源 | 结果周期长 |

## 3. 共识、分歧与裁决

### 共识一：系列主题逐年收窄，复用公开生态是最快起手（609370 / 614950 / 609278；置信度中高）

2024 擒抱 → 2025 pre-snap → 2026 球在空中；冠军补充数据与开源模型直接可用。**裁决**：先读近三届主题与往届方案，再决定"新指标/新可视化"切口；优先复用公开 coverage/Transformer 基线。置信度：中高。

### 事件一：数据字段口径要在建模前锁死（610834 / 613454 / 614459 / 613468；置信度中高）

ball_land 不一致、player_to_predict/frame/orientation/acceleration 等被逐条提问。**裁决**：开赛先做字段字典与异常抽检（尤其球落点与帧对齐），把口径写进 notebook。置信度：中高。

### 事件二：提交流程与赛道规则要先验证（663170 / 663242 / 662658；置信度中高）

有人遇到"未配置评测系统"、writeup 编辑方式不明。**裁决**：提前用草稿跑通提交链路，确认赛道（Analytics vs Broadcast Visualization）与编辑规则；留出结果延迟的预期。置信度：中高。

### 事件三：就业与传播价值是这类赛的重要回报（609370 / 614950；置信度中高）

官方直言"简历管道很深"，2025 冠军进入 SumerSports 并反哺社区。**裁决**：把 writeup 当作品集（可公开、可复现、有业务结论），赛后继续运营开源产物。置信度：中高。

### 事件四：结果公布经常延期（670213 / 670745；置信度中）

原定 1/20，1/26 仍在询问，最终获奖以附件公布。**裁决**：不要把结果时间写进求职/发表计划；提交后保持 notebook 可访问。置信度：中。

## 4. 证据分级

| 断言 | 等级 | 说明 |
| --- | --- | --- |
| 主题、赛道与就业定位 | 官方帖（609370） | 高 |
| 冠军补充数据与开源模型 | 冠军自述 + 链接（614950） | 高（资源可查） |
| 结果延期 | 讨论帖（670213） | 中高 |
| 数据口径问题 | 多帖（610834 等） | 中高 |
| 提交系统问题 | 个案帖（663170） | 中低 |
| 获奖名单 | 附件公告（670745） | 中（无正文） |

## 5. 悬案与缺口（登记）

- 获奖 writeup 正文与评审细节未归档；
- Analytics 与 Broadcast Visualization 两赛道的评分权重未公开；
- ball_land 等数据不一致的官方结论未归档；
- 2027 预告内容未归档；
- **图证缺口**：本场 0 张归档图，已登记。

## 6. 图表证据

本场 0/0 张归档图，**图证缺口已登记**。

## 7. 出处

- 官方欢迎（8 票 / 12 评论）：https://www.kaggle.com/competitions/nfl-big-data-bowl-2026-analytics/discussion/609370
- 2025 冠军 AMA 与补充数据（5 票 / 1 评论）：https://www.kaggle.com/competitions/nfl-big-data-bowl-2026-analytics/discussion/614950
- 结果延期询问（16 票 / 0 评论）：https://www.kaggle.com/competitions/nfl-big-data-bowl-2026-analytics/discussion/670213
- 获奖公布（8 票 / 2 评论）：https://www.kaggle.com/competitions/nfl-big-data-bowl-2026-analytics/discussion/670745
- 编辑已提交 writeup（0 票 / 1 评论）：https://www.kaggle.com/competitions/nfl-big-data-bowl-2026-analytics/discussion/663242
- ball_land 不一致（1 票 / 4 评论）：https://www.kaggle.com/competitions/nfl-big-data-bowl-2026-analytics/discussion/610834
- 提交系统未配置（0 票 / 3 评论）：https://www.kaggle.com/competitions/nfl-big-data-bowl-2026-analytics/discussion/663170
