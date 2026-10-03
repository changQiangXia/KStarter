# Biohub - Cell Tracking During Development

> `biohub-cell-tracking-during-development` ｜ Research ｜ 指标 CZI Biohub Zebrafish 133605 ｜ 3947 队 ｜ 截止 2026-09-29

本页汇总该场 **2 条 ≥50 票 GM 主题帖**、**11 条断言**、**0 条高票评论**。

## GM 主题帖

| 票 | 选手 | 日期 | 主题 |
| --- | --- | --- | --- |
| 95 | [@ren4yu](https://www.kaggle.com/ren4yu) | 2026-09-30 | [3rd Place Solution](https://www.kaggle.com/competitions/biohub-cell-tracking-during-development/discussion/744484) |
| 76 | [@sersasj](https://www.kaggle.com/sersasj) | 2026-10-01 | [1st Place Solution](https://www.kaggle.com/competitions/biohub-cell-tracking-during-development/discussion/744801) |

## 断言（条件→动作→机制→结果）

| 选手 | 等级 | 阶段 | 动作（节选） | 出处 |
| --- | --- | --- | --- | --- |
| @ren4yu | A | 建模与训练 | 六阶段：检测（2.5D U-Net 集成加 3D SegResNet 热图）→ 稠密流 → 匹配 → 分裂识别 → 谱系图联合优化 → 后处理；检测占最终运行时间 55% | [biohub-cell-tracking-during-development#744484-01](https://www.kaggle.com/competitions/biohub-cell-tracking-during-development/discussion/744484) |
| @ren4yu | A | 复盘与流程 | A0→A7 消融链：检测加 Hungarian 0.890211；加稠密流 0.901919；加匹配 0.901953；加分裂与联合优化 0.964493；加 gap closin | [biohub-cell-tracking-during-development#744484-05](https://www.kaggle.com/competitions/biohub-cell-tracking-during-development/discussion/744484) |
| @ren4yu | A | 数据理解 | 官方分数 = 节点数调整后的 edge Jaccard + 0.1 × Division Jaccard；未标注区域的链接不自动算 FP；只有与标注连接竞争的错链才被罚；检测精度或 | [biohub-cell-tracking-during-development#744484-06](https://www.kaggle.com/competitions/biohub-cell-tracking-during-development/discussion/744484) |
| @sersasj | A | 建模与训练 | 三阶段加解码：检测（3D U-Net 加 Cellpose 风格头）→ Soon Net（看每细胞 3 帧预测分裂状态与走向）→ learned linker（transforme | [biohub-cell-tracking-during-development#744801-01](https://www.kaggle.com/competitions/biohub-cell-tracking-during-development/discussion/744801) |
| @sersasj | A | 建模与训练 | 3.1M 参数 3D U-Net，crop 128×128×64，3 次下采样（24/48/96 到 192），各向异性 pooling (1,2,2)、(1,2,2)、(2,2, | [biohub-cell-tracking-during-development#744801-02](https://www.kaggle.com/competitions/biohub-cell-tracking-during-development/discussion/744801) |
| @sersasj | A | 工程/流程 | 第一轮用手绘约 1800 细胞加 133k GT 的 4.305 µm stamps 微调；再用 5-fold 平均加 4x flip TTA 给 195 部电影与 150 外部  | [biohub-cell-tracking-during-development#744801-04](https://www.kaggle.com/competitions/biohub-cell-tracking-during-development/discussion/744801) |
| @sersasj | A | 建模与训练 | Soon Net = 236K CNN encoder 加 508K transformer，看 3 帧预测 interphase / soon to divide / just  | [biohub-cell-tracking-during-development#744801-05](https://www.kaggle.com/competitions/biohub-cell-tracking-during-development/discussion/744801) |
| @ren4yu | B | 建模与训练 | 用低阈值 DoG 找候选中心；排除距未匹配候选 6 µm 内的区域（不产生损失）；正样本与背景 MSE 分开平均、背景权重 0.5；强度用每视频 0.1 与 99.9 分位归一化； | [biohub-cell-tracking-during-development#744484-02](https://www.kaggle.com/competitions/biohub-cell-tracking-during-development/discussion/744484) |
| @ren4yu | B | 建模与训练 | 下采样 (1,4,4) 得到各向同性 1.625 µm 网格；3D encoder-decoder 用局部相关加 soft-argmax 出初位移再残差精修；真图对用 warp 一 | [biohub-cell-tracking-during-development#744484-03](https://www.kaggle.com/competitions/biohub-cell-tracking-during-development/discussion/744484) |
| @sersasj | B | 建模与训练 | 掩掉 50% 体积但只用 2×4×4 小块（约 3.25 µm，约三分之一细胞核）；数据 180 部电影 18000 帧加 1500 外部帧；30 epochs | [biohub-cell-tracking-during-development#744801-03](https://www.kaggle.com/competitions/biohub-cell-tracking-during-development/discussion/744801) |
| @ren4yu | C | 集成与融合 | 把保留哪些节点、选哪些普通链接、选哪些女儿对一起做优化；约束：每细胞至多一个 parent、至多一个 outgoing（普通或分裂）、分裂必须同时选两女儿、分裂 parent 必须 | [biohub-cell-tracking-during-development#744484-04](https://www.kaggle.com/competitions/biohub-cell-tracking-during-development/discussion/744484) |

## 高票评论

_无 ≥10 票评论_

## 关联资产

- 深读：`analysis/deep/biohub-cell-tracking-during-development.md`
- 结构化摘要：`notes/cv/biohub-cell-tracking-during-development.md`
- 归档讨论区：`intel/biohub-cell-tracking-during-development/`（主题 2 条有 ≥50 票帖，图证 11 个）
