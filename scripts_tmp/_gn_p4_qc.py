# -*- coding: utf-8 -*-
"""P4 data quality round: language norms + profile-image link audit + weak-field stats."""
import glob
import json
import os
import re
import collections
from urllib.parse import urlparse

BASE = "output/gn/2026-11-10"
CJK = r"\u4e00-\u9fff"
FMT_OK = re.compile(rf"^[{CJK}][^()]*\([^()]*[A-Za-z][^()]*\)$")      # 中文(拉丁)
FMT_REV = re.compile(rf"^[A-Za-z][^()]*\([^()]*[{CJK}][^()]*\)$")     # 拉丁(中文) reversed
TRAD = set("內國黨聯幾會學廳員權區發動農點後處線戰師東兩無應陽隱職機構監審環境讓責權亞華貝裡盧喬納薩爾蘇丹幾亞")

viol = collections.defaultdict(list)

def is_image_url(url):
    if not url or not str(url).startswith("http"):
        return "not-http"
    u = str(url).lower()
    path = urlparse(u).path
    if re.search(r"\.(jpg|jpeg|png|gif|webp)$", path):
        return "image-ext"
    if "upload.wikimedia.org" in u:
        return "wikimedia-direct"
    # lookaside/og endpoints may still be images but unverifiable statically
    return "no-ext"  # potentially weak

# ---- profile source audit + language norms ----
weak_profile = collections.Counter()
files = sorted(glob.glob(f"{BASE}/persons/GN-*.json"))
n_files = 0
for f in files:
    oid = os.path.basename(f)[:-5]
    try:
        d = json.load(open(f, encoding="utf-8"))
    except Exception as e:
        viol["json_invalid"].append(f"{oid}:{e}")
        continue
    n_files += 1
    bi = d  # person file is flat
    # 1. name language norms
    name = bi.get("name") or ""
    if FMT_REV.match(name):
        viol["name_reversed"].append(f"{oid}:{name[:40]}")
    if re.search(rf"[{CJK}]", name):
        viol["name_has_cjk"].append(f"{oid}:{name[:40]}")  # name should be local language only
    name_zh = bi.get("name_zh") or ""
    if name_zh and not re.search(rf"^[{CJK}]+$", name_zh):
        viol["name_zh_not_pure_cjk"].append(f"{oid}:{name_zh[:30]}")
    bad_tr = [c for c in name_zh if c in TRAD]
    if bad_tr:
        viol["name_zh_traditional"].append(f"{oid}:{name_zh[:20]}({','.join(bad_tr)})")
    # org/institution format: 中文(拉丁) required when CJK present
    for i, w in enumerate(bi.get("work_experience") or []):
        org = w.get("organization") or ""
        if org and re.search(rf"[{CJK}]", org) and not FMT_OK.match(org):
            viol["work_org_fmt"].append(f"{oid}[{i}]:{org[:40]}")
        if w.get("org_id") == "":
            viol["empty_org_id"].append(f"{oid}[{i}]")
    for i, e in enumerate(bi.get("education") or []):
        inst = e.get("institution") or ""
        if inst and re.search(rf"[{CJK}]", inst) and not FMT_OK.match(inst):
            viol["edu_inst_fmt"].append(f"{oid}[{i}]:{inst[:40]}")
    # relationships / family name format
    for i, r in enumerate(bi.get("person_relationships") or []):
        nm = r.get("person_name") or ""
        if nm and re.search(rf"[{CJK}]", nm) and not FMT_OK.match(nm):
            viol["rel_name_fmt"].append(f"{oid}[{i}]:{nm[:40]}")
        if r.get("person_id") == "":
            viol["empty_pid"].append(f"{oid}[{i}]")
    for i, fm in enumerate(bi.get("family_members") or []):
        nm = fm.get("name") or ""
        if nm and re.search(rf"[{CJK}]", nm) and not FMT_OK.match(nm):
            viol["family_name_fmt"].append(f"{oid}[{i}]:{nm[:40]}")
    # 2. profile image link audit
    prof = bi.get("profile")
    if prof is None:
        weak_profile["profile_null"] += 1
        viol["profile_null"].append(oid)
    elif isinstance(prof, dict):
        src = prof.get("source_url")
        if not src:
            weak_profile["source_url_null"] += 1
            viol["profile_src_null"].append(oid)
        else:
            kind = is_image_url(src)
            weak_profile[kind] += 1
            if kind in ("not-http", "no-ext"):
                viol["profile_link_weak"].append(f"{oid}:{str(src)[:80]}")
            if "wikimedia" in str(src).lower() and "_tmp_" not in str(src):
                weak_profile["wikimedia_link"] += 1
            # QID link check: link pointing to wikidata.org entity page (not an image host)
            if re.search(r"wikidata\.org/wiki/Q\d+", str(src)):
                viol["profile_qid_link"].append(f"{oid}:{str(src)[:80]}")
    elif isinstance(prof, str):
        kind = is_image_url(prof)
        weak_profile["str_profile_" + kind] += 1
        viol["profile_is_string"].append(f"{oid}:{prof[:60]}")
    # 3. date norms
    bd = bi.get("birth_date")
    if bd and not re.match(r"^\d{4}-\d{2}-\d{2}$", str(bd)):
        viol["birth_date_fmt"].append(f"{oid}:{bd}")
    # 4. forbidden top-level extras (schema whitelist, *_note allowed by prior practice? — strict list check)
    ALLOWED = {"person_id","wikidata_qid","name","name_zh","name_en","aliases","nationality","gender",
               "birth_date","birth_place","contacts","current_positions","education","work_experience",
               "person_relationships","social_accounts","family_members","political_stances",
               "major_achievements","biography_summary","profile","collection_meta",
               "rank","honors","works","public_activities","languages","is_deceased",
               "death_date","dissolved_date","religion",
               "birth_date_note","birth_place_note","family_note","education_note","profile_note",
               "work_note","position_note","death_note","social_accounts_note","identity_note",
               "children_note","birth_note","religion_note","family_members_note","status_note",
               "name_spelling_note","family_members_note","collection_meta"}
    extra = set(bi.keys()) - ALLOWED
    if extra:
        viol["extra_top_fields"].append(f"{oid}:{sorted(extra)}")
    # 5. social platform enum
    PLAT = {"twitter_x","facebook","linkedin","youtube","instagram","telegram","tiktok","threads",
            "mastodon","wechat","weibo","github","gitlab","medium","substack","other"}
    for sa in bi.get("social_accounts") or []:
        if sa.get("platform") not in PLAT:
            viol["platform_enum"].append(f"{oid}:{sa.get('platform')}")

print("=" * 66)
print(f"P4 QC — {n_files} person files")
print("=" * 66)
total = 0
for k in sorted(viol):
    items = viol[k]
    total += len(items)
    print(f"[{len(items):3d}] {k}")
    for it in items[:5]:
        print(f"       - {it}")
    if len(items) > 5:
        print(f"       ... +{len(items)-5} more")
if not viol:
    print("ALL CHECKS PASSED")
print(f"total issues: {total}")
print()
print("=== profile.source_url distribution ===")
for k, v in weak_profile.most_common():
    print(f"  {v:3d}  {k}")
