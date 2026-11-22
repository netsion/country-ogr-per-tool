# -*- coding: utf-8 -*-
"""P5 批量修复 strict 错误：
①org key_people[] 内非法 source/sources 字段 → 内容并入 collection_meta.notes 后删除
②person work_experience[] 内非法 org_id_note 字段 → 内容并入 collection_meta.notes 后删除
不改任何其他字段；id_registry.json 不动。"""
import json, glob, os, sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
BASE = r"D:\claude-workspace\country-ogr-per-tool\output\gh\2026-11-17"

def load(p):
    return json.load(open(p, encoding="utf-8"))

def save(p, d):
    json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=2)

n_fix_org = n_fix_person = 0

# ① org: key_people source/sources → notes
for f in glob.glob(os.path.join(BASE, "orgs", "*.json")) + glob.glob(os.path.join(BASE, "orgs_trimmed_skeletons", "*.json")):
    d = load(f)
    changed = False
    moves = []
    for i, kp in enumerate(d.get("key_people") or []):
        for bad in ("source", "sources"):
            if bad in kp:
                v = kp.pop(bad)
                if v:
                    moves.append("key_people[%d] %s %s: %s" % (i, bad, kp.get("name", "?"), v))
                changed = True
    if changed:
        cm = d.setdefault("collection_meta", {})
        notes = cm.get("notes") or ""
        add = "；key_people 来源补记：" + " | ".join(moves) if moves else ""
        cm["notes"] = (notes + add) if notes else ("key_people 来源补记：" + " | ".join(moves))
        save(f, d)
        n_fix_org += 1

# ② person: work_experience org_id_note → notes
for f in glob.glob(os.path.join(BASE, "persons", "*.json")):
    d = load(f)
    changed = False
    moves = []
    for i, w in enumerate(d.get("work_experience") or []):
        if "org_id_note" in w:
            v = w.pop("org_id_note")
            if v:
                moves.append("work_experience[%d]（%s）org_id_note: %s" % (i, w.get("organization", "?"), v))
            changed = True
    if changed:
        cm = d.setdefault("collection_meta", {})
        notes = cm.get("notes") or ""
        add = "；org_id_note 补记：" + " | ".join(moves) if moves else ""
        cm["notes"] = (notes + add) if notes else ("org_id_note 补记：" + " | ".join(moves))
        save(f, d)
        n_fix_person += 1

print("org files fixed:", n_fix_org, "| person files fixed:", n_fix_person)
