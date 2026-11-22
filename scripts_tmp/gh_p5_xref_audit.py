# -*- coding: utf-8 -*-
"""P5 交叉引用错绑审计：对所有带 ID 的引用做宽松匹配，
区分「同一实体的写法差异」与「真实错绑」。"""
import json, os, re, sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
BASE = r"D:\claude-workspace\country-ogr-per-tool\output\gh\2026-11-17"

def load(p):
    return json.load(open(p, encoding="utf-8"))

def norm_lat(s):
    s = s.lower()
    s = re.sub(r"[^a-z0-9\u00c0-\u024f ]", " ", s)
    return [t for t in s.split() if len(t) >= 3]

def cjk_chars(s):
    return set(ch for ch in s if "\u4e00" <= ch <= "\u9fff")

def loose_match(ref, targets):
    """targets: list of candidate names. Return True if plausibly same entity."""
    ref_lat = set(norm_lat(ref))
    ref_cjk = cjk_chars(ref)
    for t in targets:
        if not t:
            continue
        t_lat = set(norm_lat(t))
        t_cjk = cjk_chars(t)
        if ref_lat and t_lat and (ref_lat & t_lat):
            return True
        if ref_cjk and t_cjk and len(ref_cjk & t_cjk) >= 2:
            return True
    return False

# build maps
person_names, org_names = {}, {}
for f in os.listdir(os.path.join(BASE, "persons")):
    if f.startswith("_") or not f.endswith(".json"):
        continue
    d = load(os.path.join(BASE, "persons", f))
    pid = d.get("person_id")
    if pid:
        person_names[pid] = [d.get("name"), d.get("name_en"), d.get("name_zh")] + (d.get("aliases") or [])
for f in os.listdir(os.path.join(BASE, "orgs")):
    if f.startswith("_") or not f.endswith(".json"):
        continue
    d = load(os.path.join(BASE, "orgs", f))
    oid = d.get("org_id")
    if oid:
        bi = d.get("basic_info") or {}
        org_names[oid] = [bi.get("name_zh"), bi.get("name_en"), bi.get("name_original")] + (bi.get("aliases") or [])

stylistic, suspicious = [], []

for f in sorted(os.listdir(os.path.join(BASE, "persons"))):
    if f.startswith("_") or not f.endswith(".json"):
        continue
    d = load(os.path.join(BASE, "persons", f))
    for i, rel in enumerate(d.get("person_relationships") or []):
        pid = rel.get("person_id")
        ref = rel.get("person_name") or ""
        if pid and pid in person_names and ref and not loose_match(ref, person_names[pid]):
            suspicious.append((f, "person_relationships[%d]" % i, ref, pid, person_names[pid][:3]))
    for i, we in enumerate(d.get("work_experience") or []):
        oid = we.get("org_id")
        ref = we.get("organization") or ""
        if oid and oid in org_names and ref and not loose_match(ref, org_names[oid]):
            suspicious.append((f, "work_experience[%d]" % i, ref, oid, org_names[oid][:3]))

for f in sorted(os.listdir(os.path.join(BASE, "orgs"))):
    if f.startswith("_") or not f.endswith(".json"):
        continue
    d = load(os.path.join(BASE, "orgs", f))
    for i, re_ in enumerate(d.get("related_entities") or []):
        oid = re_.get("org_id")
        ref = re_.get("org_name") or re_.get("name") or ""
        if oid and oid in org_names and ref and not loose_match(ref, org_names[oid]):
            suspicious.append((f, "related_entities[%d]" % i, ref, oid, org_names[oid][:3]))

print("SUSPICIOUS (loose-match failed):", len(suspicious))
for row in suspicious[:40]:
    print(" %s %s\n   ref=%r -> %s = %r" % row)
