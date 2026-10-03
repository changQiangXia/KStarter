# AI Village CTF（DEF CON 30）深读：黑箱 oracle 探测 × 暴力优先 × 饱和分数竞速

> 赛事：Research（AI Village @ DEF CON 30）｜ 主题 sim-agent（ML 安全夺旗）｜ 668 队 ｜ 标准赛 ｜ 指标：Nvidia Defcon（flag 加权分）
> 材料基础：`digests/ai-village-ctf.md`（6 篇正文：HOTTERDOG 52 / 48 小时 39 / 7th 33 / 1st 24 / 21 解法摘要 11 / 分享禁令 13；80 条主题索引）+ 2 张图
> 深读时间：2026-10（Tier A #59）；同系列 2023 届（DEF CON 31）在仓库中另有归档（1344 队、25 flags），可作品系对照

## 0. 一句话重述：这道题真正在考什么

题面是"在 22 道 ML 攻击/逆向题（hotdog、math、WAF、token、sloth…）上拿 flag 换分"——真正的考题是**在分数会饱和的竞速赛里，用最廉价的探测/暴力手段最快拿分**：

1. **分数饱和 → 名次由时间决定**：最高分 0.894（21/22）被 **34 位选手同时达到**；1st 与 7th 同为 0.894，7th 的 Chris Deotte 自述"一周没睡好"。在这种结构下，"解得好"不如"解得快"。
2. **黑箱 oracle + 暴力优先**：1st 的明牌策略是"**把工作尽量交给不优雅/暴力的解法，以腾出时间做下一题**"——math 从 100 递增暴力；inference 用手写字符探测 server 预测再对 top-5 候选暴力；WAF 用"固定 4 字符块 + 变最后一个字符直到触发检测"的 oracle 边界搜索逐字符反推恶意串；sloth 直接对词典暴力（答案是一个单词）。
3. **对抗攻击的经济学**：给模型的题（Salt/Theft）用白盒梯度攻击（ART 库）；黑盒（Hotterdog）只能代理模型集合 + 对抗攻击 + 热狗图噪声叠加；而检查器薄弱的题（Honor Student 的篡改检测、Deepfake 的视频轨检查、Bad-to-Good 的学生模型）用**画图/换视频轨/改输入值**这类非 ML 手段直接击穿——攻击的是**整条判定管线的最弱环**。
4. **元层反向工程**：1st 发现每题 `genChallengeFlag()` 的固定字符集是挑战相关的变位词（hotdog→HOTDOGFORDAYSS、wifi→TURNED、murderbots→IWasNotMurdebotted、inference→D3FCON…），把 CTF 本身当成一道 meta 谜题来校验解法。

一句话：**这是一场"oracle 探测 + 暴力搜索 + 对抗迁移 + 时间管理"的马拉松**——正规方法的价值只在它比暴力更快时存在。

## 1. 材料与角色

| 帖子 | 作者 | 票数 | 角色与独有信息 |
| --- | --- | --- | --- |
| [344336](https://www.kaggle.com/competitions/ai-village-ctf/discussion/344336) HOTTERDOG 求助（梗图） | Edward Crookenden | 52 | 全场最高票：一张"狗夹在热狗面包里"的图 + "为什么这都不行"；评论区藏着真实方法论——"从简单实验开始、证伪假设"（一位选手 ~5 小时解出） |
| [344396](https://www.kaggle.com/competitions/ai-village-ctf/discussion/344396) 48 小时把我变成了什么 | Rob Mulla | 39 | 社区文化证据：梗图"It's all connected——Chester 和 sloth 合谋偷走我们的 WiFi 去喂 murderbots"；CTF 的沉浸式节奏（48 小时） |
| [351800](https://www.kaggle.com/competitions/ai-village-ctf/discussion/351800) 7th：21 个解法 | Chris Deotte | 33 | 赛后公开 21 题完整 notebook；**34 位选手同时达到 0.894**；自述一周后才睡好——竞速赛的真实成本 |
| [353536](https://www.kaggle.com/competitions/ai-village-ctf/discussion/353536) 1st | IsaiahP | 24 | 唯一完整"策略层"叙述：暴力优先以腾时间；逐题解法（含 WAF 逐字符反推、Crop1 任意分辨率、sloth 词典暴力、Crop_2 未解）；**proto-flag 元谜题表**；代码 GitHub |
| [351804](https://www.kaggle.com/competitions/ai-village-ctf/discussion/351804) 21 解法摘要 | Vasilis Konstantakos | 11 | 逐题方法学：math=DBSCAN/PCA、hotdog=贴图、hotterdog=代理模型梯度攻击、theft/salt=ART、token=tokenizer 失同步词、waf=exploit 库、inference=Kaggle 手写集、crop1=Optuna/GA、crop2 失败、sloth"不想谈" |
| [344845](https://www.kaggle.com/competitions/ai-village-ctf/discussion/344845) 分享禁令 | — | 13 | 官方提醒：比赛期间分享答案/解法代码将被取消评奖资格；赛后（9-12 后）欢迎分享 |

**材料缺口（受"仅 ≤3 篇场次定点补采"约束，登记备查）**：无任何**题面/挑战代码/逐题细节**入库；关键讨论未收录——[351806](https://www.kaggle.com/competitions/ai-village-ctf/discussion/351806) Solve sloth with abs()（30 票）、[351801](https://www.kaggle.com/competitions/ai-village-ctf/discussion/351801) Competition End（26）、[343582](https://www.kaggle.com/competitions/ai-village-ctf/discussion/343582) 欢迎帖（23）、[347149](https://www.kaggle.com/competitions/ai-village-ctf/discussion/347149) secret-sloth 提示（21）、[346451](https://www.kaggle.com/competitions/ai-village-ctf/discussion/346451) CTF Feedback（19）、[343964](https://www.kaggle.com/competitions/ai-village-ctf/discussion/343964) 公开分享是否允许（18）、[352068](https://www.kaggle.com/competitions/ai-village-ctf/discussion/352068) sloth 致敬（13）、[343947](https://www.kaggle.com/competitions/ai-village-ctf/discussion/343947) No Medals & No Teaming?（12）、[343654](https://www.kaggle.com/competitions/ai-village-ctf/discussion/343654) Release Notes（11）。

## 2. 逐方案对照矩阵

| 维度 | 1st（IsaiahP） | 7th（Chris Deotte） | Vasilis（21 解摘要） |
| --- | --- | --- | --- |
| 总体策略 | **暴力优先，腾时间** | 系统化、逐题写清 notebook | 工具箱化：聚类/优化/对抗库 |
| math_1-4 | 从 100 递增暴力 | 系统性解法（notebook） | DBSCAN + PCA 找簇与维度 |
| hotdog/hotterdog | 贴热狗图；跨开源模型暴力+热狗噪声 | / | 贴图；代理模型（InceptionV3/MobileNet）梯度攻击 |
| theft/salt | 对抗样例（模型给定时较易） | / | Art 库梯度攻击 |
| bad/to/good | 手动调参（负 demerit 是关键） | / | 人工+DBSCAN 引导；评论区补充 **-100** 极值 |
| baseball | 正态均值网格搜索 + 置信度排序 | / | 分布边界实验 + 手动模仿 |
| deepfake | 用静态图替换视频轨 | / | First Order Motion Model |
| honor student | 画 A + 在线压缩规避篡改检测 | / | 直接改 F 为 A |
| token | Excel 找 BLANK/SECRETKEY 重复行 | / | 关键词失同步（SECRET/BLANK 词干） |
| WAF | **逐字符 oracle 反推 + 加空格/变量绕过** | / | 从 exploit 库试到成功 |
| inference | 手写字符集探测 + top-5 候选暴力 | / | Kaggle 手写数据集 + 循环组合 |
| forensics / leakage | model.summary()；用户名喂 LSTM 还原密码 | / | 同左（摘要级） |
| murderbot | 逻辑回归挑 10 个"最像人"的 | / | 多分类器加权平均 |
| wifi | LLE 2D→1D 投影找路径 | / | 嵌入空间可视化路径 |
| crop1 | 发现可提交任意分辨率 → 3×3 平铺 | / | Optuna 贝叶斯优化（GA 亦可） |
| crop2 | ✗ 未解 | ✗（21/22 上限） | ✗（反转/投毒尝试失败） |
| sloth | 词典暴力（答案是单词） | 解出（21 题之一） | "不想谈"（最大痛点） |

## 3. 共识、分歧与裁决

### 共识一：这是一场"分数饱和 + 按时间排名"的竞速（2/2 顶级队 + 官方统计）

0.894 = 21/22，被 34 人同时达到；1st/7th/Vasilis 都是 0.894 层级；1st 反复强调"fast puzzle-solving""腾时间解下一题"。**裁决**：当分数上限被多数强队触达时，排名的唯一自由度是**时间**；策略目标从"求最优解"变成"求最快可提交解"。置信度：高。

### 共识二：黑箱 oracle 探测是第一通用武器（3/3 有细节的队）

WAF（逐字符触发检测边界）、Inference（手写字符 → server 预测 → top-5 暴力）、Crop1（试探任意分辨率）、Math（从 100 递增）、Token（文件末尾重复词）——本质都是"用最便宜的探测换结构性信息，再对剩余小空间暴力"。**裁决**：CTF 里**评分接口本身就是题目的一部分**；先设计探测实验，再选算法。置信度：高。

### 共识三：攻击要打在判定管线的最弱环（3/3）

有模型 → 白盒梯度攻击（ART）；无模型 → 代理模型迁移 + 噪声叠加（Hotterdog）；检查器薄弱 → 贴图/画图/换视频轨/填负值。**裁决**：ML 安全检查的鲁棒性取决于整条管线（预处理、篡改检测、分辨率假设、正则化），而不是模型本身；"绕过检测"经常比"骗过模型"更便宜。置信度：高。

### 共识四：真正卡住所有人的是同一道题（Crop_2，2/2 顶级队未解）

1st 未解 Crop_2；Vasilis 的模型反转/投毒逆推失败；21/22 成为事实上的共享上限。**裁决**：CTF 的名次结构由"最难题"决定上限、由"速度"决定分布——难题不解（或不快解）时，其余 21 题的完成时间就是全部竞争空间。置信度：高。

### 分歧一：优雅解法 vs 暴力优先

1st 明牌"把工作交给不优雅/暴力解法"（math 暴力、sloth 词典、baseball 网格）；Vasilis/Chris 更偏向成体系的方法（DBSCAN/PCA、Optuna、完整 notebook）。**裁决**：两者都到 0.894；在时间压力下，**暴力是理性默认，成体系方法是加速器**（当它能节省试错时）。置信度：高。

### 分歧二：分享的时机与边界

官方禁令（比赛期间分享=取消资格）与社区困惑（"Is Public Sharing Allowed?" 18 票）并存；赛后 Chris 公开 21 解 notebook、1st 放 GitHub、Vasilis 发摘要——赛前赛后的文化切换是 CTF 传统（通常赛后大量 writeup）。**裁决**：这类比赛的"知识资产"在赛后一次性释放；参赛期应把沟通限制在方法论层面。置信度：高。

### 事实：Crop1 的"意外解"是 reward hacking 还是正解？

1st 发现"可提交任意分辨率图像"后用 3×3 平铺绕过裁剪逻辑；社区称其 tricky。**裁决**：CTF 中"检查器实现边界"就是攻击面的一部分；这类发现与 ML 对抗攻击同族（利用实现假设），应记录为"读检查器代码/试探接口约束"的标准动作。置信度：中高。

## 4. 增量数字账

| 动作 | 数字 | 来源 |
| --- | --- | --- |
| 赛事规模 | 668 队 / 80 帖 / 22 挑战；2022-08-11 开赛、09-12 结束（DEF CON 30 周末开幕） | 元数据+帖子日期 |
| 分数上限 | 最高 **0.894**（21/22）；**34 人**同时达到；1st 与 7th 并列该分 | 7th 帖 |
| 时间成本 | 7th："一周后才睡好"；社区梗图："48 小时把我变成了…"；HOTTERDOG 有人 ~5 小时解出 | 7th/344396/344336 |
| 1st 关键动作 | math 从 100 递增；inference top-5 候选暴力；crop1 3×3 平铺；WAF 固定 4 字符块逐位反推；sloth 词典暴力 | 1st 帖 |
| Vasilis 工具链 | DBSCAN/PCA（math）、ART（theft/salt）、Optuna+GA（crop1）、FOM（deepfake） | 摘要帖 |
| Bad-to-Good 极值技巧 | 把 demerit/absences 改为 **-100**（评论区） | 摘要帖评论 |
| 元谜题 | 每题 `genChallengeFlag()` 固定字符集=变位词；示例：hotdog→HOTDOGFORDAYSS、wifi→TURNED、murderbots→IWasNotMurdebotted、inference→D3FCON、sloth→SPECTRAL | 1st 帖 |
| 分享规则 | 赛期分享答案/解法=取消资格；赛后可分享 | 344845/351800 |
| 系列 | 2022：668 队 22 题 → 2023（DEF CON 31）：1344 队 25 flags | 仓库对照 digest |

**结构校验（2 处吻合）**

1. "34 人 0.894"与"1st/7th/Vasilis 均 21/22"自洽：上限由 Crop_2 锁死，达标者并列 ✓；
2. 1st 的暴力清单与 Vasilis 的"crop2 失败/ sloth 痛点"互相印证：暴力在 oracle 便宜时有效、在 oracle 不可用（crop2 无廉价反馈）时失效 ✓。

## 5. 机制推演

**M1｜饱和竞速的博弈结构**：当多数强队都能到达分数上限，边际"解题质量"不再影响名次，名次取决于"第 k 题的正确提交时间"。于是最优策略是把每题的成本压到最低（暴力/贴图/编辑）并按期望时间排序求解——这正是 1st 的显式策略。副作用：睡眠剥夺成为真实资源约束（7th 一周不眠）。

**M2｜oracle 探测的三种模式**：(a) **增量暴力**（math：从 100 递增；成本=调用次数）；(b) **边界二分**（WAF：固定前 4 字符变最后一位，逐步发现触发点，再向前推进——本质是 oracle 引导的串构造）；(c) **查表 + 小空间穷举**（inference：先把 62 个手写字符喂 server 得到映射，再对每位 top-5 组合暴力）。共同点：先花少量调用学结构，再花大量调用做小空间搜索。

**M3｜对抗迁移的经济学**：白盒（模型给定）→ 直接梯度攻击，成本低；黑盒 → 代理模型集成 + 迁移 + 噪声叠加（1st 对 Hotterdog 的做法）；检查器弱 → 绕过管线（压缩图规避篡改检测、静态图替换视频轨、负值输入）。**推论**：安全题的难度 ≈ min(模型鲁棒性, 管线假设强度)；攻方永远打更便宜的一侧。

**M4｜检查器的"实现边界"= 攻击面**：Crop1 的分辨率假设、Honor Student 的篡改启发式、Token 的分词器特殊串——都是实现细节泄漏出的自由度。与对抗样本同源：**任何"近似判定"都有可利用的维度**。

**M5｜元层反向工程的杠杆**：`genChallengeFlag()` 的固定字符集把 22 题的 flag 生成逻辑连成一个家族；识别变位词既提示挑战语义，又能验证解法方向（例如 wifi→TURNED 提示"路径/转向"）。在 CTF 中，"题目工厂"本身也是逆向对象。

**M6｜CTF 社区文化作为生产力/阻力**：最高票帖子是梗图（52/39）；求解经验藏在玩笑评论区（5 小时解 HOTTERDOG 的方法论）；但赛期分享禁令防止答案扩散。社区氛围提供了"情绪韧性"（长赛程的关键资源），同时要求参赛者自律。

**M7｜该系列的方法谱系**：2023 届（DEF CON 31，1344 队、25 flags）的 writeup 大量出现"25 flags 全解/最后到 24"的竞争结构，说明同类"饱和竞速 + 少数难题卡上限"的拓扑在续作中延续（本仓库另有归档）。

## 6. 证据分级

| 断言 | 等级 | 说明 |
| --- | --- | --- |
| 34 人 0.894 / 21/22 上限 | 7th 帖明确统计 | 中高 |
| 1st 的逐题解法与 proto-flag 表 | 自述 + GitHub 代码 | 中高 |
| Vasilis 的逐题方法 | 自述 + notebook 链接 | 中 |
| 分享禁令与取消资格 | 官方帖 | 高 |
| HOTTERDOG 5 小时/证伪假设建议 | 评论区自述 | 中 |
| 比赛规模/日期/系列沿革 | 元数据 + 仓库对照 | 高 |
| 每题分值权重/0.894 的确切算法 | 未收录 | 低（缺口） |
| Challenge 规格/代码 | 未收录 | —（缺口） |

## 7. 边界条件与反事实

- **反事实 1（若分数不饱和）**：名次由解题深度决定，暴力优先不再最优，Optuna/系统化方法价值上升。
- **反事实 2（若 oracle 调用昂贵/限次）**：WAF 逐字符探测、math 递增暴力、inference 查表都不成立；必须先建本地模型模拟判定。
- **反事实 3（若检查器更严）**：Honor Student（禁止压缩图）、Crop1（强制 5×5）、Deepfake（校验运动一致性）会同时失效——题目难度对"实现严格度"极其敏感。
- **反事实 4（若允许组队）**：并行解多题会显著压缩时间；本场"无奖牌、禁止组队"的规则让个人策略（排序+暴力）成为关键。
- **边界**：全部结论属于"flag 加权分 + 赛期长 + 后期饱和 + 检查器含实现缝隙"的 CTF 生态；不适用于深度优化型 Kaggle 赛。

## 8. 悬案与失败学

**悬案**

1. **Crop_2 的解法**：1st/Vasilis 均未解；模型反转与投毒逆推失败；是否有队伍/官方解法未在材料中。
2. **"Solve sloth with abs()"（30 票）**：sloth 的另一条解法路径未收录——它与词典暴力是否等价？
3. **0.894 的计算方式与逐题权重**：Nvidia Defcon 指标的精确公式缺失。
4. **题目规格与代码（22 题）**：未归档；本深读的"攻击面"结论只能靠解法反推。
5. **分享规则与组队规则的执行情况**：是否有人被取消资格/特例（No Medals & No Teaming）。
6. **math_3 描述错误**（12 票）对解题公平性的影响。

**失败学（跨队合集）**

- 1st：Crop_2 未解；Hotterdog 需要跨开源模型暴力+噪声，说明纯迁移攻击不稳定。
- Vasilis：Bad-to-Good 无好自动解（靠人工+聚类）；Crop_2 的模型反转/投毒反推全部失败；sloth 自述"不想谈"。
- Chris Deotte：无失败项记录（但一周不眠暗示时间/心理成本）。
- 社区：HOTTERDOG 线程显示"直觉贴图"普遍失败——检测模型对真实热狗+"更热"的梗图并不买账（对抗鲁棒性）。

## 9. 图表证据

> 路径相对本文件（`analysis/deep/`）：`../../intel/ai-village-ctf/bodies/<topic>_img/NN.ext`

![HOTTERDOG 梗图](../../intel/ai-village-ctf/bodies/344336_img/01.png)

**图 1：HOTTERDOG 求助帖的配图**（topic 344336，52 票）——把狗夹进热狗面包、画上芥末酱的图配上"为什么这都不行 :)"; 评论区给出真实方法论："从简单实验开始，证伪假设"。**一图代表本场的"直觉对抗"失败学与社区幽默**。

![It's all connected 梗图](../../intel/ai-village-ctf/bodies/344396_img/01.jpg)

**图 2：Rob Mulla 的 48 小时梗图**（topic 344396，39 票）——"IT'S ALL CONNECTED：Chester 和 sloth 合谋偷走我们的 WiFi 去喂 murderbots"，把 hotdog（Chester）、sloth、wifi、murderbots 四道题串成一个阴谋论。**赛程强度与社区文化的直接证据**，也说明四道题是全场讨论焦点。

## 10. 对既有笔记/playbook 的修订点

1. `notes/sim-agent/ai-village-ctf.md` 升级：从"精简版"扩为 9 节结构；补 6 篇角色表、1st/7th/Vasilis 三队对照、数字账（668 队/0.894/34 人/22 题）、机制 M1–M7、2 张图证与失败清单。
2. `playbook/sim-agent.md`（CTF/黑箱节）增补：
   - **饱和竞速策略**：先评估"分数是否饱和"；若饱和，按预期耗时排序题目，暴力优先、快速提交；
   - **oracle 探测三模式**：增量暴力 / 边界二分（逐字符构造）/ 查表+小空间穷举；
   - **对抗迁移经济学**：白盒用梯度、黑盒用代理+噪声、检查器弱就绕过管线（篡改检测/分辨率/输入域）；
   - **实现缝隙清单**：分辨率假设、特殊 token、极值（负数）、文件尾注释、model.summary()；
   - **时间与心理管理**：长赛程的睡眠/交接安排；把"下一题"当默认状态；
   - **分享纪律**：赛期只谈方法，赛后统一释放 writeup。
3. `playbook/00-通用方法论.md` 增补：**"先判断赛制的排名结构（质量型 vs 速度型），再决定投入策略"**；**"判定管线的最弱环决定安全赛题的难度"**。
4. `analysis/THEORY.md`（Batch 6 末汇总 v0.6）候选：
   - **L107｜饱和分数→速度排名律**（上限被多数触达时，时间成为唯一自由度；证据 = 34 人 0.894 + 1st 的暴力优先策略）；
   - **L108｜黑箱 oracle 探测律**（先花少量调用学结构、再暴力小空间；证据 = WAF/inference/crop1/math）；
   - **L109｜安全判定最弱环律**（攻击成本 ≈ min(模型鲁棒性, 管线假设强度)；证据 = hotdog/honor/deepfake/bad-to-good 的非 ML 击穿）。

## 11. 出处

- HOTTERDOG 梗图与讨论（52 票）：https://www.kaggle.com/competitions/ai-village-ctf/discussion/344336
- 48 小时梗图（39 票）：https://www.kaggle.com/competitions/ai-village-ctf/discussion/344396
- 7th：21 solutions（33 票）：https://www.kaggle.com/competitions/ai-village-ctf/discussion/351800
- 1st（24 票）：https://www.kaggle.com/competitions/ai-village-ctf/discussion/353536
- 21 解法摘要（11 票）：https://www.kaggle.com/competitions/ai-village-ctf/discussion/351804
- 分享禁令（13 票）：https://www.kaggle.com/competitions/ai-village-ctf/discussion/344845
- 同系列对照：`digests/ai-village-capture-the-flag-defcon31.md`（2023，1344 队、25 flags）
- 未收录正文的关键讨论（真实 topic id，供后续定点补采/图片层参考）：351806、351801、343582、347149、346451、343964、352068、343947、343654、352466
