#!/usr/bin/env bash
# 关机/重启后恢复采集。用法：bash scripts/resume_collection.sh
#
# 做了什么：
#   1. 校验 intel/*/DONE 标记是否为合法 JSON（关机可能截断写入），非法则删除以便重采
#   2. 打印当前进度
#   3. 以 2 分片 × 1 线程、sleep 10（跳图片）启动后台采集
#
# 该配置在 2 核 / 无 GPU 环境下同样适用——瓶颈是 Kaggle 账号限流，不是本地算力。
# 实测 3 分片 × 2 线程 + sleep 1 会触发限流风暴，吞吐反而暴跌，故保持保守配置。

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PY=/root/miniconda3/envs/kaggle/bin/python
cd "$ROOT"

echo "== 1. 校验 DONE 标记 =="
"$PY" - <<'EOF'
import json, pathlib
bad = []
for marker in pathlib.Path("intel").glob("*/DONE"):
    try:
        json.loads(marker.read_text())
    except Exception:
        bad.append(marker)
for marker in bad:
    print("  删除损坏标记：", marker)
    marker.unlink()
print(f"  损坏标记 {len(bad)} 个" if bad else "  全部合法")
EOF

echo "== 2. 当前进度 =="
"$PY" scripts/notes_status.py | tail -3

echo "== 3. 启动采集（2 分片 × 1 线程，sleep 10，跳过图片）=="
for i in 1 2; do
  setsid nohup "$PY" scripts/batch_collect.py \
    --max-bodies 6 --pages 4 --sleep 10 --threads 1 --skip-images --shard "$i/2" \
    > "intel/_batch_r$i.log" 2>&1 < /dev/null &
  disown
done
sleep 5
echo "运行中的采集进程：$(pgrep -fc 'batch_collect.py --max-bodies' || echo 0)"
echo
echo "查看进度：$PY scripts/notes_status.py"
echo "采集日志：intel/_batch_r1.log / _r2.log"
echo "完成后的补采（可选）："
echo "  $PY scripts/backfill_images.py    # 补图片（依赖 Google 存储可达）"
echo "  $PY scripts/repair_missing_top.py --fix   # 补最高票主题"
