# 外部技能库索引（kei-kochiya/kaggle-skills）

> 来源：[kei-kochiya/kaggle-skills](https://github.com/kei-kochiya/kaggle-skills)（MIT License），
> commit `821fa0fdbb81`，抓取 2026-10-06；本地 clone 在 `data/cache/kaggle-skills`（不入库）。
> 本目录派生索引：`kaggle_skills_index.csv`（30 个文件逐条映射到本仓库去向）。
> 与另一外部源（kaggle-solutions 链接库）并列：链接索引见 `EXTERNAL.md`，本文件是**方法/配方**索引。

## 规模

- 3 个 agent skills（tabular / RL-simulation / competition-distiller）+ 16 篇 references + 1 篇多 LLM 工作流 + 10 篇 handbook。
- 内容形态：数学配方与实现（CIR、FFT-AUC、base_margin、Fréchet、NF4 量化）、KGMON 7 阶段流水线、
  RL 工程（模拟器加速/联赛/部署）、以及蒸馏 SOP。

## 已蒸馏进 KExperienceSkill（本仓库仅登记来源，正文在 skill 仓库）

| 外部内容 | 去向（KExperienceSkill） | 蒸馏要点 |
| --- | --- | --- |
| `Handbook/workflows/llm-agentic-kaggle-workflow.md`（526 行） | `references/agent-kaggle-playbook.md` §2.5/3.5/3.7 | 多 LLM 角色矩阵、KGMON 7 阶段、5×5 嵌套护栏、双 agent 审计 + 8 门 + 两段漏斗 |
| `kaggle-tabular-playbook/references/*`（9 篇） | `references/tabular-advanced-recipes.md` | 生成器取证、嵌套 OOF TE、CIR+Ridge、logit 堆叠+秩平均、FFT-AUC、base_margin、Fréchet+lexrank、软伪标签、公榜拟合代价法则 |
| `kaggle-rl-simulation/references/*`（5 篇）+ starter | `references/sim-engineering.md` | 加速层级与 parity、多实体架构、PPO/联赛、NF4 量化与部署兜底、选型与 48h 清单 |
| 提示词模板（工作流 §5） | `assets/agent_prompt_templates.md` | 生成器逆向 / PyTorch 合成 / 爬山堆叠 / 独立审计 / 两段漏斗 |

## 与本仓库 264 场的关系（覆盖核对）

| 外部场次 | 本仓库 | 状态 |
| --- | --- | --- |
| playground-s6e1 / s6e2 / s6e3 / s6e5 / s6e9 | `notes/tabular/playground-series-s6e{1,2,3,5,9}.md` + `analysis/deep/` | 已覆盖（外部可作交叉佐证） |
| orbit-wars / maze-crawler | `notes/sim-agent/` | 已覆盖 |
| kaggriculture / s6e10 | — | 未覆盖（本仓库 264 场边界之外；如扩场可优先） |

### 逐场增量（外部有、我们 notes 尚未覆盖或较浅的点）

| 场次 | 外部增量 | 我们已有（避免重复引用） |
| --- | --- | --- |
| s6e1 | 模 10 位分解与谐振周期（p=12/14/20）特征；Centered Isotonic（CIR）+ Ridge 的配对细节 | 190 模型 Ridge + 等距回归后处理、线性残差建模范式 |
| s6e3 | KGMON 7 阶段流水线 + 多 LLM 角色矩阵 + 5×5 嵌套/维度断言/求解器兜底护栏（工程方法论） | 60 万行代码、850 模型、Radix、Benford |
| s6e9 | 公榜拟合代价法则（`ΔPrivate ≈ 16.7u − 0.88×ΔPublic`，r=−0.97）；GLM `base_margin` 残差提升；lexrank 零平局；超球 Fréchet 集成；TabPFN 全上下文缩放律与"OOF 喂邻居模型"泄漏警告 | FFT AUC-direct 三层融合（+1.62u）、嵌套 CV 对私榜 Spearman 0.991 |
| s6e2 | 多尺度分箱与 PLR embedding 的工程细节 | ~150 OOF + Optuna 2500 trials + Ridge |
| s6e5 | 去 Driver 双流分支与同步折对齐原数据增广的完整参数（权重 0.5–1.0） | Driver 对抗漂移、186 OOF、AutoGluon+LR 混合 |
| 通用 | 双 agent 跨家族审计（8 门）+ Fold0→Fold1 两段漏斗；RL 工程（加速层级/联赛/NF4 量化部署） | 实验协议、提交组合对冲 |

## 可引用的外部数字（证据等级：外部自述，未独立复算）

- S6E3 冠军战役：30 天、60 万行代码、50 个 EDA 脚本、850 模型 → 154 模型集成（4×A100；GPT-5.4/Gemini 3.1/Claude Opus 4.6 分工）。
- S6E9 公榜拟合法则：`ΔPrivate ≈ +16.7u − 0.88 × ΔPublic`（r=−0.97）；嵌套 CV 对私榜 Spearman 0.991 vs 公榜 0.793。
- S6E9 单模：TabPFN-3.5 全上下文 668,665 行 → pooled AUC 0.946485（缩放律 ≈ +18.6e-5 / 上下文翻倍）。
- Orbit Wars 部署：NF4-LSQ(128) 800MiB → 90.7MiB + 5M fallback 10.1MiB（<100MiB）；动态 int8 单步 2500ms → 450ms。
- 模拟器加速：官方 Python ~50–200 steps/sec 基线；Rust PyO3/Rayon 融合循环 + AABB + pinned 内存；parity harness 必须逐 bit 对齐官方 replay。

> 引用规则：以上数字进入方案时必须标注"外部自述"并按 `analysis/SOP.md` 的同折对照纪律验证；
> 不得直接写成本仓库 claims 的已验证结论。

## 复现

```bash
git clone --depth 1 https://github.com/kei-kochiya/kaggle-skills.git data/cache/kaggle-skills
python scripts/build_kaggle_skills_index.py     # -> analysis/external/kaggle_skills_index.csv
```

> 许可：MIT License（上游 README 声明）；本目录与 KExperienceSkill 的蒸馏文档均保留来源署名。
