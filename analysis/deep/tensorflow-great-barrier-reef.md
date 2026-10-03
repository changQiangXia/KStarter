# TensorFlow Great Barrier Reef 轻量深读（Tier B）

> 赛事：Research ｜ 主题 cv（视频目标检测）｜ 2025 队 ｜ 代码赛 ｜ 指标：CSIROObjectDetectionFBeta（F2@IoU0.8 类）
> 材料基础：`digests/tensorflow-great-barrier-reef.md`（6 篇正文：往届检测冠军汇总 289999 / 3rd Hydrogen 307707 / Kaggle 教训 297863 / 1st "Trust CV" 307878 / 5th Poisson 308007 / YOLOv5 高分辨率 300638；80 条主题索引）+ 0 张归档图
> 轻读时间：2026-10（Tier B B02）

## 1. 一句话重述与数字账

水下视频中的海星（COTS）检测（F2，IoU 0.8 阈值对**框的松紧**极敏感）。真正考的是：**检测集成 + 二阶段重打分/多家族融合 + 跟踪/后处理**；而本场最著名的教训是**"训练框松、公榜框紧、私榜又不同"的标注松紧域偏移**。

| 关键数字 | 值 | 来源 |
| --- | --- | --- |
| 1st "Trust CV" | 6×YOLOv5 集成 CV 0.716 → 分类重打分 0.727 → 分类集成 0.73+ → 注意力后处理 **0.74+**；3 折按 video_id；跟踪 +0.002 但弃用（多两个超参） | 1st |
| 1st 的 F2 事故 | 同一份 OOF：三名队员算出 F2=**0.62 / 0.66 / 0.68**；最终选用最低分实现评估全部模型 | 1st |
| 3rd（Hydrogen） | 5 种检测器（CenterNet+HRNet、FasterRCNN+NFNet、FCOS、EfficientDet、YOLOv5l-6 直优 F2）；WBF；轨迹置信度提升 +0.01；光流 +0.001 | 3rd |
| 3rd 的标注松紧 | 高分辨率推理→框更紧→公榜大涨；手动把框缩小 ~**3px**（训练框平均大 3px）；手标小样本微调也涨公榜；但**私榜全部失效** | 3rd |
| 5th | cut&paste + Poisson 融合 + 真假分类器；多模型多尺寸（YOLOv5 S/M/L6、YOLOX-L、YOLOR-P6、HRNet）；SuperPoint/SuperGlue 单应 + DeepSort；WBF 前丢弃 maxIoU<0.55 的框 | 5th |
| 公榜玄学 | "[LB 0.579] YOLOv5 高分辨率 is all you need"（300638） | 材料 |

## 2. 逐方案对照矩阵

| 维度 | 1st | 3rd | 5th |
| --- | --- | --- | --- |
| 路线 | 2 阶段：检测→分类重打分→后处理 | 5 家族检测集成 + 轨迹置信提升 | 检测多模型 + Poisson 合成 + 跟踪 |
| 检测 | YOLOv5×6（全图 3648 / patch 1536） | CenterNet/FRCNN/FCOS/EffDet/YOLOv5 | YOLOv5/YOLOX/YOLOR/HRNet |
| 分类/重打分 | 7 个 IoU bin 的分类头（dropout 0.7/drop_path 0.5），均值当分数 | 无（直接融合） | 真假分类器筛合成样本 |
| 跟踪 | 注意力区域跨帧加分（+0.01 级）；tracking 方法 +0.002 弃用 | 中心距离轨迹 + 低置信框提到轨迹最大置信（**+0.01**）；光流 +0.001 | SuperPoint/SuperGlue 单应 + DeepSort |
| 验证 | 3 折视频；**只优化 CV** | 视频折+子序列折（公榜相关好，私榜失败） | 5 折按序列 |
| 关键姿态 | Trust CV | 追公榜的"框紧度"漏洞 → 私榜反噬 | 合成数据 + 跟踪 |

## 3. 共识、分歧与裁决

### 共识一：检测集成 + WBF/跟踪是基础盘（3/3）

1st/3rd/5th 都做多检测器集成与跨帧信息；3rd 的 WBF 自动投票、5th 先丢孤立框再 WBF、1st 用跨帧注意力加分。**裁决**：视频检测的稳定增益来自"多模型 + 跨帧一致性"，而非单模调参。置信度：高。

### 共识二：F2@IoU0.8 让"框的松紧"成为一等变量

3rd 的证据链：高分辨率推理→框更紧→公榜大涨；手动缩小 3px 同样涨；训练框平均大 3px；手标小样本微调也涨。**裁决**：指标对框尺寸敏感时，**标注松紧是可测量、可利用、也可被私榜反噬的域变量**。置信度：高（多证据链，但私榜结论未明）。

### 共识三：CV 必须按视频/序列分组，并统一实现（1st 的 F2 事故）

1st 用 3 折按 video_id；3rd 用视频折+子序列折；5th 5 折按序列。1st 还发现同一 OOF 的 F2 在三人实现下差 0.06。**裁决**：分组 CV + **共享同一评测实现**是团队协作的硬要求；否则模型选择都在噪声上。置信度：高。

### 分歧一：Trust CV 还是追公榜漏洞

1st（冠军）"没有新东西，只从第一天到最后一天优化 CV"；3rd 发现并重仓公榜的"框紧度"调整，私榜失效。**裁决**：对"疑似测试集标注差异"的漏洞要**先对冲**（保留无漏洞版本），不能把提交全押在公榜反馈上。置信度：高。

### 分歧二：跟踪是否值得

1st：tracking +0.002 但引入两个超参 → 弃用；注意力后处理（无超参化）替代；3rd：轨迹置信提升 +0.01；5th：单应+DeepSort。**裁决**：跟踪有效但超参敏感；用"无额外超参"的跨帧后处理（注意力/轨迹置信提升）性价比最高。置信度：中高。

### 分歧三：合成数据

5th：Poisson 融合+真假分类器有效；GAN 生成逼真但不涨分（受限于独特海星数量）；其他人未用。**裁决**：合成数据的瓶颈是"目标多样性"而非真实感；copy-paste 需解决光照边界与位置合理性。置信度：中。

## 4. 证据分级

| 断言 | 等级 | 说明 |
| --- | --- | --- |
| 1st 的 CV 提升链（0.716→0.74+） | 自述 | 中高 |
| F2 实现差异 0.62/0.66/0.68 | 自述（真实协作事故） | 高（事实性） |
| 3rd 的框紧度证据链 | 自述（公榜 A/B + 训练集统计） | 中高（公榜部分）；私榜结论开放 |
| 3rd 的轨迹置信 +0.01 | 自述 | 中 |
| 5th 的 Poisson/真假分类器 | 自述 | 中 |
| 指标实现细节（F2@IoU 0.8） | 1st 帖给出实现链接 | 中高 |

## 5. 悬案与缺口（登记）

- 2nd/4th 方案未收录；私榜为何与公榜标注不一致没有官方解释（3rd 的开放问题）。
- "框紧度"调整的私榜失效说明公榜反馈不可外推，但材料未给出各队最终分数明细。
- F2 的精确实现（1st 提供了自己的版本）与官方差异未核。
- 5th 的 GAN 受限于 unique 海星数量的假设未做受控实验。

## 6. 图表证据

**本场无归档图片**（`intel/tensorflow-great-barrier-reef/bodies/` 无 `*_img`；digest 中 5th 的三张图未落盘），无法内嵌图证。

## 7. 出处

- 往届检测冠军汇总（289999）：https://www.kaggle.com/competitions/tensorflow-great-barrier-reef/discussion/289999
- 3rd Team Hydrogen（307707）：https://www.kaggle.com/competitions/tensorflow-great-barrier-reef/discussion/307707
- Kaggle 教训（297863）：https://www.kaggle.com/competitions/tensorflow-great-barrier-reef/discussion/297863
- 1st Trust CV（307878）：https://www.kaggle.com/competitions/tensorflow-great-barrier-reef/discussion/307878
- 5th Poisson（308007）：https://www.kaggle.com/competitions/tensorflow-great-barrier-reef/discussion/308007
- YOLOv5 高分辨率（300638）：https://www.kaggle.com/competitions/tensorflow-great-barrier-reef/discussion/300638
