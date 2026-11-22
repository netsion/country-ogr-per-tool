# -*- coding: utf-8 -*-
"""P4 进度收账：python gh_p4_progress_update.py <pid_tail> [<pid_tail> ...]
输入 6 位尾号（如 000092），校验文件存在→移入 completed→打印 next 派发名单。"""
import json, os, sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
BASE = r"D:\claude-workspace\country-ogr-per-tool\output\gh\2026-11-17"
PGF = os.path.join(BASE, "_phase_progress.json")

pg = json.load(open(PGF, encoding="utf-8"))
for tail in sys.argv[1:]:
    pid = "GH-PERSON-" + tail
    f = os.path.join(BASE, "persons", pid + ".json")
    if not os.path.exists(f):
        print("!! 文件缺失: %s —— 不收账" % pid)
        continue
    for lst in (pg["current"], pg["remaining"]):
        if pid in lst:
            lst.remove(pid)
    if pid not in pg["completed"]:
        pg["completed"].append(pid)
    print("OK 收账 %s (文件 %d bytes)" % (pid, os.path.getsize(f)))

pg["last_updated"] = "2026-11-20"
pg["current"] = [p for p in pg["current"] if os.path.exists(os.path.join(BASE, "persons", p + ".json")) is False or True]
json.dump(pg, open(PGF, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("completed=%d remaining=%d current=%s" % (
    len(pg["completed"]), len(pg["remaining"]), [p[-6:] for p in pg["current"]]))
print("NEXT10:", " ".join(p[-6:] for p in pg["remaining"][:10]))
