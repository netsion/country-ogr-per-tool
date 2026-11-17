# -*- coding: utf-8 -*-
import json, re

BASE = r"D:\ai-workspace\apec-osint-tool\output\eg\2026-11-16"
with open(f"{BASE}/_target_orgs.json", encoding="utf-8") as f:
    targets = json.load(f)["organizations"]
with open(f"{BASE}/_tmp/qid_labels.json", encoding="utf-8") as f:
    labels = json.load(f)

def norm(s):
    s = s.lower()
    s = re.sub(r"[^a-z0-9\u0600-\u06ff\s]", " ", s)
    return set(s.split())

def sim(a, b):
    A, B = norm(a), norm(b)
    if not A or not B:
        return 0.0
    return len(A & B) / len(A | B)

rows = []
for o in targets:
    q = o.get("wikidata_qid") or o.get("qid")
    if not q:
        continue
    lab = labels.get(q, {})
    en = lab.get("en") or ""
    name = o.get("name", "")
    s = max(sim(name, en), sim(name.split("(")[0], en))
    rows.append((s, o["id"], name, q, en, (lab.get("desc") or "")[:70], lab.get("ar") or ""))

rows.sort()
lines = ["=== LOW (<0.35, review) ==="]
for s, oid, name, q, en, desc, ar in rows:
    if s < 0.35:
        lines.append(f"sim={s:.2f} {oid} | {name} | {q} -> {en} | {desc} | ar:{ar[:40]}")
lines.append("")
lines.append("=== MEDIUM (0.35-0.55) ===")
for s, oid, name, q, en, desc, ar in rows:
    if 0.35 <= s < 0.55:
        lines.append(f"sim={s:.2f} {oid} | {name} | {q} -> {en} | {desc} | ar:{ar[:40]}")
n_ok = sum(1 for r in rows if r[0] >= 0.55)
lines.append(f"\nOK(sim>=0.55): {n_ok} / {len(rows)}")

with open(f"{BASE}/_tmp/qid_compare_report.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(lines))
print("report written,", len(rows), "checked,", n_ok, "ok")
