# -*- coding: utf-8 -*-
"""P4 data quality audit: Chinese convention checks + avatar link classification."""
import json
import os
import re
import sys
from collections import Counter

sys.stdout.reconfigure(encoding="utf-8")
BASE = "output/ci/2026-10-06"
PERSONS = os.path.join(BASE, "persons")

def cn_ratio(s):
    s = s or ""
    if not s.strip():
        return 0.0
    cn = len(re.findall(r"[\u4e00-\u9fff]", s))
    return cn / max(len(s.strip()), 1)

def is_mostly_cn(s, th=0.5):
    return cn_ratio(s) > th

issues = Counter()
detail = {"name_cn": [], "name_zh_bad": [], "bio_short": [], "bio_en": [],
          "org_no_cn": [], "pos_en": [], "currpos_en": [], "inst_no_cn": [],
          "relname_no_cn": [], "famname_no_cn": [], "achv_en": [], "ascii_quote": [],
          "topic_en": []}

files = sorted(f for f in os.listdir(PERSONS) if f.endswith(".json") and f != "_index.json")
all_persons = []
for fn in files:
    with open(os.path.join(PERSONS, fn), encoding="utf-8") as f:
        d = json.load(f)
    all_persons.append(d)
    pid = d.get("person_id", fn[:-5])

    # 1. name: official language (French) — should not be Chinese-dominant
    if d.get("name") and cn_ratio(d["name"]) > 0.3:
        issues["name_is_chinese"] += 1
        detail["name_cn"].append(pid)

    # 2. name_zh: pure Chinese
    nz = d.get("name_zh") or ""
    if not nz.strip():
        issues["name_zh_empty"] += 1
        detail["name_zh_bad"].append(pid + "(empty)")
    elif not is_mostly_cn(nz, 0.4):
        issues["name_zh_not_chinese"] += 1
        detail["name_zh_bad"].append(pid + "(" + nz[:20] + ")")

    # 3. biography_summary: Chinese >= 100 chars
    bio = d.get("biography_summary") or ""
    if len(bio.strip()) < 100:
        issues["bio_too_short"] += 1
        detail["bio_short"].append(pid)
    elif not is_mostly_cn(bio, 0.4):
        issues["bio_not_chinese"] += 1
        detail["bio_en"].append(pid)

    # 4. work_experience: organization must contain Chinese; position must be Chinese
    for i, w in enumerate(d.get("work_experience", []) or []):
        org = w.get("organization") or ""
        if org and not re.search(r"[\u4e00-\u9fff]", org):
            issues["org_no_chinese"] += 1
            detail["org_no_cn"].append(f"{pid}[{i}]{org[:25]}")
        pos = w.get("position") or ""
        if pos and not is_mostly_cn(pos, 0.3):
            issues["position_not_cn"] += 1
            detail["pos_en"].append(f"{pid}[{i}]{pos[:25]}")

    # 5. current_positions: pure Chinese
    for i, cp in enumerate(d.get("current_positions", []) or []):
        if isinstance(cp, str) and cp.strip() and not is_mostly_cn(cp, 0.3):
            issues["currpos_not_cn"] += 1
            detail["currpos_en"].append(f"{pid}[{i}]{cp[:25]}")

    # 6. education: institution contains Chinese; field Chinese
    for i, e in enumerate(d.get("education", []) or []):
        inst = e.get("institution") or ""
        if inst and not re.search(r"[\u4e00-\u9fff]", inst):
            issues["institution_no_chinese"] += 1
            detail["inst_no_cn"].append(f"{pid}[{i}]{inst[:25]}")
        fld = e.get("field") or ""
        if fld and not is_mostly_cn(fld, 0.3):
            issues["field_not_cn"] += 1

    # 7. relationships / family names: 中文(原文)
    for r in d.get("person_relationships", []) or []:
        pn = r.get("person_name") or ""
        if pn and not re.search(r"[\u4e00-\u9fff]", pn):
            issues["relname_no_chinese"] += 1
            detail["relname_no_cn"].append(f"{pid}{pn[:25]}")
    for r in d.get("family_members", []) or []:
        nm = r.get("name") or ""
        if nm and not re.search(r"[\u4e00-\u9fff]", nm):
            issues["famname_no_chinese"] += 1
            detail["famname_no_cn"].append(f"{pid}{nm[:25]}")

    # 8. achievements / stances in Chinese
    for a in d.get("major_achievements", []) or []:
        ach = a.get("achievement") or ""
        if ach and not is_mostly_cn(ach, 0.3):
            issues["achievement_not_cn"] += 1
            detail["achv_en"].append(f"{pid}{ach[:25]}")
    for s in d.get("political_stances", []) or []:
        topic = s.get("topic") or ""
        if topic and not is_mostly_cn(topic, 0.3):
            issues["topic_not_cn"] += 1
            detail["topic_en"].append(f"{pid}{topic[:25]}")

    # 9. ASCII double quotes inside Chinese strings (should use 「」)
    raw = json.dumps(d, ensure_ascii=False)
    for m in re.findall(r":\s*\"([^\"]*[\u4e00-\u9fff][^\"]*)\"", raw):
        if '"' in m:
            issues["ascii_quote_in_cn"] += 1
            detail["ascii_quote"].append(pid)
            break

print("=" * 60)
print("P4 QUALITY AUDIT — %d person files" % len(all_persons))
print("=" * 60)
print("\n[Language convention issues]")
for k, v in sorted(issues.items()):
    print(f"  {k}: {v}")
if not issues:
    print("  (none)")

print("\n[Details (first 5 each)]")
for k, items in detail.items():
    if items:
        for it in items[:5]:
            print(f"  {k}: {it}")

# ============ Avatar audit ============
print("\n" + "=" * 60)
print("AVATAR AUDIT")
print("=" * 60)
IMG_EXT = re.compile(r"\.(jpe?g|png|webp|gif|svg)(\?|$)", re.I)
QID_LINK = re.compile(r"wikidata\.org/wiki/Q\d+", re.I)
WIKI_PAGE = re.compile(r"(wikipedia|wikimedia)\.org/(wiki|wikipedia/(en|fr|commons))/", re.I)

stats = Counter()
bad_links = {"qid": [], "nonimage": [], "nourl": []}
local_missing = []
have_local = 0
for d in all_persons:
    pid = d.get("person_id", "?")
    prof = d.get("profile") or {}
    url = (prof.get("source_url") or "").strip()
    lp = (prof.get("local_path") or "").strip()
    if url:
        if QID_LINK.search(url):
            stats["qid_link"] += 1
            bad_links["qid"].append(pid + " " + url[:70])
        elif IMG_EXT.search(url) or "upload.wikimedia.org" in url:
            stats["direct_image"] += 1
        elif WIKI_PAGE.search(url) or True:
            stats["non_image_url"] += 1
            bad_links["nonimage"].append(pid + " " + url[:70])
    else:
        stats["no_source_url"] += 1
        bad_links["nourl"].append(pid)
    if lp:
        cand1 = os.path.join(BASE, lp)
        cand2 = os.path.join(BASE, "persons", lp)
        if os.path.exists(cand1) or os.path.exists(cand2):
            have_local += 1
        else:
            stats["local_missing"] += 1
            local_missing.append(pid + " " + lp)
    else:
        stats["no_local_path"] += 1

for k, v in sorted(stats.items()):
    print(f"  {k}: {v}")
print(f"  local files verified: {have_local}")
print("\n[QID links as photo] first 5:")
for x in bad_links["qid"][:5]: print("   ", x)
print("[Non-image URLs] first 8:")
for x in bad_links["nonimage"][:8]: print("   ", x)
print("[local_path missing on disk] count:", len(local_missing), "first 5:")
for x in local_missing[:5]: print("   ", x)

# ============ Social accounts ============
print("\n" + "=" * 60)
print("SOCIAL ACCOUNTS")
print("=" * 60)
sc = Counter()
for d in all_persons:
    accs = d.get("social_accounts") or []
    if not accs:
        sc["no_accounts"] += 1
    else:
        sc["has_accounts"] += 1
        for a in accs:
            sc["plat:" + str(a.get("platform"))] += 1
print("  persons with accounts: %d | without: %d" % (sc["has_accounts"], sc["no_accounts"]))
for k, v in sorted(sc.items()):
    if k.startswith("plat:"):
        print(f"    {k[5:]}: {v}")
