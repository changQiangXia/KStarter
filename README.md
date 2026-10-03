# Kaggle 近 5 年 write-up 采集与主题化分析（2021-10 ~ 2026-10）

对 **264 场已结束比赛**的全量 write-up 采集、逐场结构化摘要与主题化方法论提炼。

## 目录结构

| 路径 | 内容 |
| --- | --- |
| `data/` | 比赛清单（`competitions_ended.csv` 735 场 / `competitions_last5y.csv` 264 场）、主题分类（`themes.csv`）、分布摘要 |
| `intel/<slug>/` | 每场原始材料：`topics.json`（讨论区索引）、`topics.md`、`bodies/*.html`（正文 HTML + 内嵌图片 URL）、`bodies/*.txt`（正文 + 全部评论纯文本）、`bodies/*_img/`（内嵌图片）、`DONE`（断点标记） |
| `digests/<slug>.md` | 索引 + 正文纯文本汇总（写摘要的输入） |
| `notes/<主题>/<slug>.md` | **逐场结构化摘要**（任务/数据、验证、模型家族、关键技巧、可迁移性、新手启示、出处） |
| `notes/INDEX.md` | 全量索引（264 场） |
| `playbook/` | **七册方法论**：通用方法论、表格/时序、CV、NLP/LLM、科学计算、优化博弈/Agent、多模态/音频/元类 |
| `LEARNING_PATH.md` | 面向新手的分阶段学习路径（含跨领域迁移清单、黑箱迭代搜索、提交与定稿） |
| `scripts/` | 采集/摘要/校验工具链（可断点续跑、限流退避、链接与引用校验） |
| `templates/` | 摘要撰写模板（完整版/精简版） |

## 统计（最终）

- 比赛：**264/264**（tabular 106、cv 49、nlp 35、science 23、other 23、sim-agent 22、audio 6）
- 摘要：**264/264**；playbook：**7/7**；学习路径：成文
- 链接校验：933 条讨论链接 + 241 条明文 topic 引用，全部通过
- 图片：内嵌图片经域名改写（`storage.googleapis.com`）回填，无 Kaggle API 消耗；223 场有图、33 场原帖无内嵌图、8 场仅存站外图床（imgur/twitter 等，本机网络不可达，URL 保留在 HTML 中）

## 常用命令

```bash
PY=/root/miniconda3/envs/kaggle/bin/python
$PY scripts/notes_status.py                 # 进度
$PY scripts/build_index.py                  # 重建 notes/INDEX.md
$PY scripts/verify_links.py                 # 校验讨论链接
$PY scripts/build_digest.py <slug>          # 生成某场 digest
$PY scripts/batch_collect.py --slugs a,b    # 定向采集
$PY scripts/backfill_images.py              # 图片回填（报告/下载）
$PY scripts/repair_missing_top.py [--fix]   # 缺陷检查/补采
```

## 说明

- 不下载站外超链接内容；仅抓取 write-up 正文中的**内嵌图片**（属原帖内容）。
- 摘要保留原文链接与名次信息，不复制代码原文。
- 采集可断点续跑：`DONE` 标记为合法 JSON 即视为完成。
