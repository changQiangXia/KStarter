# 第二阶段摘要说明

## 目录结构

```
notes/<主题>/<slug>.md     每场比赛一份结构化摘要
notes/README.md            本文件
```

主题目录：`tabular` `cv` `nlp` `science` `sim-agent` `audio` `other`

## 两种模板

| 模板 | 适用 | 结构 |
| --- | --- | --- |
| 完整版 `templates/competition_summary.md` | Featured / Research，且有 3 篇以上实质 write-up | 任务与数据、验证方案、模型家族、关键技巧、可迁移性评估、新手启示、出处 |
| 精简版 `templates/competition_summary_compact.md` | Playground / Community，或 write-up 稀少 | 任务、关键技巧、可迁移要点、出处 |

## 写作要求

1. **出处链接必须来自 `intel/<slug>/topics.json` 的真实 topic id**，不得凭记忆填写。
2. 保留公开链接与名次信息；不复制代码原文，不做超出摘要需要的长段引用。
3. 「可迁移性评估」分三档：可直接迁移 / 需要前提 / 不建议照搬——这是对新手最有价值的部分。
4. 涉及参赛者身份时按名次表述（如"1st place"），不突出个人 handle。

## 进度核对

```bash
/root/miniconda3/envs/kaggle/bin/python scripts/notes_status.py
```
