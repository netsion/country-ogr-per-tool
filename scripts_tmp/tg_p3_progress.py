# -*- coding: utf-8 -*-
"""P3 进度管理（主会话串行调用，单写者无冲突）
用法:
  python tg_p3_progress.py current <org_id...>      # 标记派发中
  python tg_p3_progress.py done <org_id...>         # 完成 -> completed
  python tg_p3_progress.py fail <org_id...>         # 失败 -> failed
  python tg_p3_progress.py next <N>                 # 列出下 N 个待派发
  python tg_p3_progress.py status                   # 汇总
"""
import json
import os
import sys
import tempfile
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

BASE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                    "output", "tg", "2026-11-16")
PF = os.path.join(BASE, "_phase_progress.json")

def save(p):
    fd, tmp = tempfile.mkstemp(dir=BASE, suffix=".tmp")
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        json.dump(p, f, ensure_ascii=False, indent=1)
    os.replace(tmp, PF)

p = json.load(open(PF, encoding="utf-8"))
cmd = sys.argv[1] if len(sys.argv) > 1 else "status"
ids = [a for a in sys.argv[2:] if not a.startswith("-")]

if cmd == "current":
    for i in ids:
        if i in p["remaining"]:
            p["remaining"].remove(i)
        if i not in p["current"]:
            p["current"].append(i)
elif cmd == "done":
    for i in ids:
        if i in p["current"]:
            p["current"].remove(i)
        if i in p["remaining"] and i not in p["completed"]:
            p["remaining"].remove(i)
        if i not in p["completed"]:
            p["completed"].append(i)
elif cmd == "fail":
    for i in ids:
        if i in p["current"]:
            p["current"].remove(i)
        if i in p["remaining"]:
            p["remaining"].remove(i)
        if i not in p["failed"]:
            p["failed"].append(i)
elif cmd == "next":
    n = int(ids[0]) if ids else 4
    for i in p["remaining"][:n]:
        print(i)
    sys.exit(0)
elif cmd == "status":
    print(f"completed={len(p['completed'])} current={len(p['current'])} "
          f"remaining={len(p['remaining'])} failed={len(p['failed'])}")
    if p["current"]:
        print("in-flight:", ",".join(p["current"]))
    if p["failed"]:
        print("failed:", ",".join(p["failed"]))
    sys.exit(0)

from datetime import datetime
p["last_updated"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
save(p)
print(f"completed={len(p['completed'])} current={len(p['current'])} "
      f"remaining={len(p['remaining'])} failed={len(p['failed'])}")
