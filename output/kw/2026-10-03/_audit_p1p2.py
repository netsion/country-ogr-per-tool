# -*- coding: utf-8 -*-
"""P1/P2 data audit for output/kw/2026-10-03."""
import json
import os
import glob
import re
from collections import Counter

BASE = os.path.dirname(os.path.abspath(__file__))
issues = []

# ---------- load everything ----------
orgs = {}
for f in glob.glob(os.path.join(BASE, "orgs", "KW-*.json")):
    with open(f, encoding="utf-8") as fh:
        d = json.load(fh)
    orgs[d["org_id"]] = d

reg = json.load(open(os.path.join(BASE, "id_registry.json"), encoding="utf-8"))
targets = json.load(open(os.path.join(BASE, "_target_orgs.json"), encoding="utf-8"))
torgs = targets["organizations"] if isinstance(targets, dict) else targets
cache_files = glob.glob(os.path.join(BASE, "_cache", "*.json"))

print(f"org files: {len(orgs)} | registry orgs: {len(reg['registry'])} | targets: {len(torgs)} | cache: {len(cache_files)}")

# ---------- 1. registry <-> files bidirectional ----------
reg_ids = {r["org_id"] for r in reg["registry"]}
file_ids = set(orgs)
if reg_ids - file_ids:
    issues.append(f"registry has {len(reg_ids-file_ids)} ids without files: {sorted(reg_ids-file_ids)[:5]}")
if file_ids - reg_ids:
    issues.append(f"{len(file_ids-reg_ids)} files not in registry: {sorted(file_ids-reg_ids)[:5]}")

# registry name <-> file name_en consistency
for r in reg["registry"]:
    oid = r["org_id"]
    if oid in orgs:
        fen = orgs[oid].get("basic_info", {}).get("name_en")
        rname = r.get("name") or ""
        # registry name format: 中文 (English) or plain English
        en_part = rname[rname.rfind("(")+1:-1] if "(" in rname else rname
        if fen and en_part and en_part.strip() != fen.strip():
            issues.append(f"registry/file name mismatch {oid}: registry='{en_part}' file='{fen}'")

# targets <-> files count per category
tcat = Counter(t["category"] for t in torgs)
fcat = Counter(o["basic_info"]["org_type"] for o in orgs.values())
if tcat != fcat:
    diff = {k: (tcat.get(k, 0), fcat.get(k, 0)) for k in set(tcat) | set(fcat) if tcat.get(k, 0) != fcat.get(k, 0)}
    issues.append(f"category count mismatch targets vs files: {diff}")

# ---------- 2. QID checks ----------
qid_map = {}
for oid, o in orgs.items():
    q = o.get("basic_info", {}).get("wikidata_qid")
    if q:
        if q in qid_map:
            issues.append(f"DUPLICATE QID {q}: {qid_map[q]} vs {oid}")
        qid_map[q] = oid
no_qid = [oid for oid, o in orgs.items() if not o.get("basic_info", {}).get("wikidata_qid")]
print(f"orgs with QID: {len(qid_map)} | without: {len(no_qid)} -> {no_qid}")

# ---------- 3. name duplicates ----------
en_names = Counter()
for oid, o in orgs.items():
    n = (o.get("basic_info", {}).get("name_en") or "").lower().strip()
    if n:
        en_names[n] += 1
dups = [n for n, c in en_names.items() if c > 1]
if dups:
    issues.append(f"duplicate name_en: {dups}")

# ---------- 4. basic_info field quality ----------
missing_en, missing_orig, missing_zh, missing_country = [], [], [], []
for oid, o in orgs.items():
    bi = o.get("basic_info", {})
    if not bi.get("name_en"):
        missing_en.append(oid)
    if not bi.get("name_original"):
        missing_orig.append(oid)
    if not bi.get("name_zh"):
        missing_zh.append(oid)
    if not bi.get("country_iso3"):
        missing_country.append(oid)
print(f"field gaps -> name_en missing:{len(missing_en)} name_original missing:{len(missing_orig)} name_zh missing:{len(missing_zh)} country_iso3 missing:{len(missing_country)}")

# ---------- 5. date format sanity ----------
bad_dates = []
for oid, o in orgs.items():
    fd = o.get("basic_info", {}).get("founded_date")
    if fd and not re.match(r"^\d{4}-\d{2}-\d{2}$", str(fd)):
        bad_dates.append((oid, fd))
if bad_dates:
    issues.append(f"founded_date not strict YYYY-MM-DD: {bad_dates[:8]}")

# ---------- 6. key_people bindings ----------
kp_total, kp_missing_person, kp_eng_names = 0, [], []
person_reg = {p["person_id"] for p in reg.get("person_registry", [])}
for oid, o in orgs.items():
    for kp in o.get("key_people") or []:
        kp_total += 1
        pid = kp.get("person_id")
        if pid and pid not in person_reg:
            kp_missing_person.append((oid, pid))
        name = kp.get("name") or ""
        # expected 中文(本国官方语言); flag pure-Latin names (skeleton-stage known gap)
        if re.match(r"^[A-Za-z .'\-]+$", name):
            kp_eng_names.append((oid, name))
orphan_persons = []
for p in reg.get("person_registry", []):
    pid = p["person_id"]
    referenced = any(
        any(kp.get("person_id") == pid for kp in (o.get("key_people") or []))
        for o in orgs.values()
    )
    if not referenced:
        orphan_persons.append(pid)
print(f"key_people total: {kp_total} | unbound person_ids: {kp_missing_person} | pure-EN names: {len(kp_eng_names)}")
print(f"person_registry orphans (in registry, referenced by no org): {orphan_persons}")

# ---------- 7. related_entities sanity ----------
rel_bad = []
for oid, o in orgs.items():
    for r in o.get("related_entities") or []:
        if not r.get("org_name"):
            rel_bad.append(oid)
if rel_bad:
    issues.append(f"related_entities missing org_name: {sorted(set(rel_bad))}")

# ---------- 8. social/website stats + cache coverage ----------
with_cache = 0
for oid, o in orgs.items():
    q = o.get("basic_info", {}).get("wikidata_qid")
    if q and os.path.exists(os.path.join(BASE, "_cache", f"{q}.json")):
        with_cache += 1
print(f"orgs with cache file: {with_cache}/{len(qid_map)} (QID-having)")

# ---------- 9. key_people -> which orgs (for trim impact) ----------
kp_by_org = {oid: [kp.get("name") for kp in (o.get("key_people") or [])] for oid, o in orgs.items() if o.get("key_people")}
print("\norgs with key_people (trim impact map):")
for oid, names in sorted(kp_by_org.items()):
    bi = orgs[oid]["basic_info"]
    print(f"  {oid} [{bi['org_type']}] {bi.get('name_en')}: {names}")

print("\n" + "=" * 60)
if issues:
    print(f"AUDIT ISSUES ({len(issues)}):")
    for i in issues:
        print(" !", i)
else:
    print("AUDIT: no structural issues found")
