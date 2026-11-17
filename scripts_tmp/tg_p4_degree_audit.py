# -*- coding: utf-8 -*-
"""TG P4 输出 degree 枚举合规审计（对照 2026-11-17 v2 docs/degree-enum.md）
检查：persons/*.json education[].degree 是否全部落在 8 值枚举+null；
同时检查 note 中的归一痕迹与「中文学位值」残留。
"""
import json, os, sys, io, glob, re
from collections import Counter
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

BASE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                    "output", "tg", "2026-11-16")
ENUM = {"primary", "high_school", "associate", "bachelor", "master",
        "doctorate", "professional", "other", None}

dist = Counter()
bad = []          # (pid, institution, degree)
null_str = []     # 字符串 "null"
zh_degree = []    # 中文/本地语言学位值
note_norm = 0     # 已有归一 note 痕迹
files = sorted(glob.glob(os.path.join(BASE, "persons", "*.json")))
n_edu = 0
for fp in files:
    pid = os.path.basename(fp).replace(".json", "")
    d = json.load(open(fp, encoding="utf-8"))
    for e in d.get("education") or []:
        n_edu += 1
        deg = e.get("degree")
        dist[deg if deg is None else deg] += 1
        if isinstance(deg, str) and deg.lower() == "null":
            null_str.append((pid, e.get("institution"), deg))
        if deg not in ENUM:
            bad.append((pid, e.get("institution"), deg))
            if isinstance(deg, str) and re.search(r'[\u4e00-\u9fff]', deg):
                zh_degree.append((pid, deg))
        note = (e.get("note") or "")
        if "已归一" in note:
            note_norm += 1

print(f"文件数: {len(files)} | education 条目: {n_edu}")
print("degree 分布:")
for k, v in sorted(dist.items(), key=lambda x: -x[1]):
    print(f"  {k}: {v}")
print()
print(f"非枚举脏值: {len(bad)}")
for pid, inst, deg in bad[:40]:
    print(f"  {pid} | {deg} | {inst}")
print(f"其中含中文的脏值: {len(zh_degree)}")
print(f"字符串'null': {len(null_str)} -> {null_str[:10]}")
print(f"已有归一 note 条目: {note_norm}")
