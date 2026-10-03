# 推送到 GitHub 的安排（方案与执行清单）

> 适用对象：本目录（`/root/autodl-tmp/kaggle`，264 场全量分析与归档）

## 1. 现状盘点（实测）

| 内容 | 体积 | 文件数 | 备注 |
| --- | --- | --- | --- |
| `intel/`（原始归档） | **695 MB** | 4,885 | 其中**图片 649 MB / 1,689 个**；HTML 9.4 MB；正文+评论 txt 12.1 MB |
| `digests/`（索引+正文纯文本） | 12 MB | 264 | 原文文本副本 |
| `data/`（清单与分类） | 2 MB | ~10 | CSV/JSON/MD |
| `notes/`（264 篇摘要） | 1.3 MB | 264 | 二次创作，出处齐全 |
| `playbook/` + `LEARNING_PATH.md` + `README.md` | ~0.2 MB | 10 | 方法论与学习路径 |
| `scripts/` + `templates/` | ~0.2 MB | ~20 | 工具链 |
| **合计** | **710 MB** | **6,314** | 最大单文件 12.9 MB（`kore-2022` 的 GIF） |

其他实测：仓库内**无凭证/密钥**（脚本只引用 `~/.kaggle` 路径）；>5 MB 文件仅 5 个；GIF 合计 92 MB。

## 2. 三个可选方案

| 方案 | 结构 | 体积 | 优点 | 风险/缺点 |
| --- | --- | --- | --- | --- |
| **A. 单仓全量（public）** | 一个公开仓库 = 全部 710 MB | 710 MB | 最"完整"，一次到位 | 国内网络推 710 MB 易反复失败；公开再分发论坛全文与代码片段有版权/ToS 顾虑 |
| **B. 分层双仓（推荐）** | 公开"分析仓"（~6 MB）+ 私有"归档仓"（~707 MB） | 6 MB + 707 MB | 公开部分干净可分享；原文归档留私有自用，合规风险最小 | 需要管两个仓库 |
| **C. 单仓 + Release 归档** | 公开轻仓 + 把 `intel+digests` 打包成分卷 release 附件 | 6 MB + 700 MB | 一个仓库搞定；下载走 Release CDN | Release 附件是**公开可下载**的，版权暴露与 A 相同 |

> 说明：GitHub 单文件上限 100 MB（我们最大 12.9 MB，未触限）；仓库建议 <1 GB（710 MB 在范围内，**无需 Git LFS**，也避免免费 LFS 1 GB 流量很快用尽的坑）。

## 3. 推荐执行（方案 B）

### 3.1 公开仓 `kaggle-writeup-analysis`（~6 MB）

包含：`README.md`、`NOTICE.md`、`LEARNING_PATH.md`、`data/`、`scripts/`、`templates/`、`notes/`、`playbook/`、`.gitignore`、`.gitattributes`

不包含：`intel/`、`digests/`（原文全量归档），README 中说明其存在与获取方式。

```bash
cd /root/autodl-tmp/kaggle
git init
git add .gitignore .gitattributes NOTICE.md README.md LEARNING_PATH.md \
        data scripts templates notes playbook docs
git commit -m "Kaggle 近5年 264 场 write-up 分析：摘要/playbook/学习路径"
git branch -M main
git remote add origin git@github.com:<you>/kaggle-writeup-analysis.git
git push -u origin main
```

### 3.2 私有归档仓 `kaggle-writeup-archive`（~707 MB）

包含：`intel/`、`digests/`、数据清单（可选）。

```bash
cd /root/autodl-tmp/kaggle
git init
git add .gitignore .gitattributes intel digests
git commit -m "原始归档：264 场索引/正文/评论/图片（仅供个人学习）"
git branch -M main
git remote add origin git@github.com:<you>/kaggle-writeup-archive.git   # 建为 Private
git push -u origin main
```

## 4. 大仓库 + 网络加速（AutoDL 实测）

### 4.1 机器自带加速：`source /etc/network_turbo`

AutoDL 的"学术资源加速"脚本（内部代理 `http://172.29.51.4:12798`），专为 github / huggingface 设计：

```bash
source /etc/network_turbo     # 开启（当前 shell 生效，设 http_proxy/https_proxy）
unset http_proxy https_proxy  # 关闭（或直接新开 shell）
```

注意脚本自带提示：**仅限学术用途、不承诺稳定性；开启后访问 pip 等其它资源会更慢**。

### 4.2 本机实测（2026-10-03）

| 目标 | 直连 | 代理（network_turbo） |
| --- | --- | --- |
| github.com | ✅ 200 / 0.54s | ✅ 200 / **6.4s（更慢）** |
| 下载测速（git 归档 ~11MB） | ✅ **3.0 MB/s** | ✅ 1.1 MB/s |
| raw.githubusercontent.com | ❌ 超时 | ✅ 301 可达 |
| huggingface.co | ❌ 失败 | ✅ 200 / 2.1s |
| git ls-remote | ✅ | ✅ |

**结论**：本机对 github.com **直连比代理快约 3 倍** → 推送优先直连；代理用于两类场景：① 直连推送中途失败/被重置时兜底；② 需要 raw.githubusercontent / HuggingFace 资源时。

### 4.3 推送配置与流程

```bash
git config http.postBuffer 524288000
git config http.version HTTP/1.1

# 1) 先推公开轻仓（秒级）
# 2) 再推私有归档仓（~707 MB）。直连失败时：
source /etc/network_turbo
git push -u origin main        # 走代理重试（git 自动读取 http(s)_proxy）
unset http_proxy https_proxy   # 推完关闭，避免拖慢 pip 等
```

- 若 HTTPS 整体受限：SSH 走 443——`~/.ssh/config` 写 `Host github.com` / `Hostname ssh.github.com` / `Port 443`。
- 重试代价小：git 按对象续传，中断后重复 `git push` 即可。
- 备选：`tar -czf intel.tar.gz intel`（图片已压缩，预计 ~600 MB）经网盘/中转上传。
- HTTPS + token：`git remote set-url origin https://<token>@github.com/<you>/<repo>.git`（token 不要提交进仓库）。

## 5. 合规清单（推送前逐条确认）

- [ ] `NOTICE.md` 已包含（来源、版权归属、删除请求通道）。
- [ ] 公开仓不含原始全文归档（或你明确接受公开再分发）。
- [ ] 仓库内无 `.kaggle/`、token、代理配置等敏感文件（`.gitignore` 已兜底）。
- [ ] 每篇摘要的出处链接均来自真实 topic id（已由 `verify_links.py` 校验：937 条全过）。

## 6. 一键自检

```bash
PY=/root/miniconda3/envs/kaggle/bin/python
$PY scripts/verify_links.py          # 讨论链接
$PY scripts/notes_status.py          # 264/264
git status --short | head            # 确认无敏感文件被跟踪
```
