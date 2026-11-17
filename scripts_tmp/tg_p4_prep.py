# -*- coding: utf-8 -*-
"""P4 启动准备：
1. 执行已确认的 ID 合并（000337/000340 -> 000331；000006 -> 000001）：
   orgs/*.json 中 person_id 引用改指 + person_list/registry 标记 merged
2. 应用用户确认的裁剪：_p4_trim_plan.json 118 人 + 全部剩余 low -> status=excluded
3. 生成 P4 执行清单 _p4_queue.json（按 high->medium 排序）+ _p4_progress.json
"""
import json
import os
import sys, io
import glob
from collections import defaultdict
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

BASE = r"D:\ai-workspace\apec-osint-tool\output\tg\2026-11-16"

MERGE = {"TG-PERSON-000337": "TG-PERSON-000331",
         "TG-PERSON-000340": "TG-PERSON-000331",
         "TG-PERSON-000006": "TG-PERSON-000001"}

# ── 1. orgs 引用改指 ──
refs_changed = defaultdict(int)
for p in glob.glob(os.path.join(BASE, "orgs", "*.json")):
    raw = open(p, encoding="utf-8").read()
    hit = False
    for old, new in MERGE.items():
        if old in raw:
            raw = raw.replace(f'"{old}"', f'"{new}"')
            hit = True
            refs_changed[old] += raw.count(f'"{new}"')
    if hit:
        json.loads(raw)  # 验证合法
        open(p, "w", encoding="utf-8").write(raw)
print("orgs 引用改指:", dict(refs_changed) or "无匹配")

# ── 2. person_list 标记 ──
pl = json.load(open(os.path.join(BASE, "person_list.json"), encoding="utf-8"))
persons = pl["persons"] if isinstance(pl, dict) and "persons" in pl else pl
trim = json.load(open(os.path.join(BASE, "_p4_trim_plan.json"), encoding="utf-8"))
trim_ids = set()
for cat in trim["trim_candidates"].values():
    trim_ids.update(cat["person_ids"])

queue = []
stats = defaultdict(int)
for p in persons:
    pid = p["person_id"]
    if pid in MERGE:
        p["status"] = "merged"
        p["merged_into"] = MERGE[pid]
        stats["merged"] += 1
        continue
    if pid in trim_ids:
        p["status"] = "excluded"
        p["exclude_note"] = "user-approved trim (_p4_trim_plan.json 2026-11-17)"
        stats["excluded_trim"] += 1
        continue
    if p.get("importance_level") == "low":
        p["status"] = "excluded"
        p["exclude_note"] = "user decision: all low excluded (2026-11-17)"
        stats["excluded_low"] += 1
        continue
    p["status"] = "queued"
    queue.append(p)

json.dump(pl, open(os.path.join(BASE, "person_list.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("person_list 标记:", dict(stats), "| queue:", len(queue))

# ── 3. P4 执行清单（high 优先）+ 进度文件 ──
queue.sort(key=lambda x: (0 if x["importance_level"] == "high" else 1, x["person_id"]))
json.dump(queue, open(os.path.join(BASE, "_p4_queue.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

prog = {"phase": "P4_person_enrichment", "started_at": "2026-11-17T00:00:00",
        "last_updated": "2026-11-17T00:00:00", "completed": [], "remaining": [p["person_id"] for p in queue],
        "current": [], "failed": [], "concurrency": 6}
json.dump(prog, open(os.path.join(BASE, "_p4_progress.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

hi = sum(1 for p in queue if p["importance_level"] == "high")
print(f"P4 队列: {len(queue)} 人（high {hi} / medium {len(queue)-hi}）")

# 抽查验证合并
m331 = [p for p in persons if p["person_id"] == "TG-PERSON-000331"][0]
print("000331 保留 OK:", m331.get("name_zh"), "| status:", m331.get("status"))
for pid in ("TG-PERSON-000337", "TG-PERSON-000340", "TG-PERSON-000006"):
    e = [p for p in persons if p["person_id"] == pid][0]
    print(pid, "status:", e.get("status"), "->", e.get("merged_into"))
