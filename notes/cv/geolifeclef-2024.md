# GeoLifeCLEF 2024（精简）

> 主题：cv ｜ 子类：— ｜ 领域：生态/地理 ｜ 类别：Research ｜ 截止：2024-05-24 ｜ 队伍数：51 ｜ 指标：物种分布预测
> 出处：`intel/geolifeclef-2024/`（80 条主题索引 + 6 篇 write-up 正文）

## 任务

由**地理位置 + 遥感影像 + 环境变量**预测物种分布（生态学基准，LifeCLEF 系列）。

## 关键要点

- 该系列是**研究基准型比赛**（与 GeoLifeCLEF/CLEF 社区绑定），讨论区以"Working Notes 征稿"等学术事项为主。
- 输入是**多模态：卫星影像 + 地理坐标 + 气候/地形栅格**。
- 主办方提到"榜分超过 0.4 已是显著成就"——说明任务本身难度高、上限受限（生态数据噪声大）。

## 可迁移要点

- **地理空间任务 = 影像 + 坐标 + 环境栅格的融合**（与本系列其他届次、ARIEL 遥感类一致）。
- 研究基准型比赛的价值在于方法可发表，评估也更严格。
- 与 PlantTraits、Herbarium、BirdCLEF 并列：**生物多样性/生态是 Kaggle 的稳定赛道**。

## 轻读结论（2026-10 补）

- **研究赛交付**：working note 时间线 5/24 竞赛截止 → **6/7 论文截稿** → 6/21 通知 → 7/8 camera-ready；CEUR-WS 出版、择优进 Springer LNCS，最佳论文获 CLEF 注册费；官方称 LB >0.4 已显著（506431）。
- **数据门槛**：PA 在 Kaggle、原始栅格在 Seafile，官方 `download.py` 让新手报错（找不到文件）、`GLC.plotting` 在 Kaggle 不可用、首次加载 10 分钟；社区自行打包 **ClimateClef** 气候栅格到 Kaggle（481283 / 481485）。
- **方法线索**：卫星图像分类综述、湿地物种多样性遥感论文；Transformer 融合多模态；Landsat 时序/卫星 patch/PA-PO 关系等答疑（480732 / 500432 / 497807 / 482176）。
- 51 队、FGVC11 + LifeCLEF 研究赛；结果/作者归属需赛前确认（507399 / 486171）。

## 图表证据

![download.py 报错](../../intel/geolifeclef-2024/bodies/481283_img/01.png)

**图**（topic 481283）：`can't open file '/kaggle/working/download.py'`——数据下载脚本是本届最典型卡点。

## 出处

- 讨论区索引：`intel/geolifeclef-2024/topics.md`
- 官方征稿与说明（8 票）：https://www.kaggle.com/competitions/geolifeclef-2024/discussion/506431
- 新手门槛吐槽（20 票）：https://www.kaggle.com/competitions/geolifeclef-2024/discussion/481283
- ClimateClef 数据集（20 票）：https://www.kaggle.com/competitions/geolifeclef-2024/discussion/481485
- 论文推荐：https://www.kaggle.com/competitions/geolifeclef-2024/discussion/480732
- 报告与排名问题：https://www.kaggle.com/competitions/geolifeclef-2024/discussion/507399
