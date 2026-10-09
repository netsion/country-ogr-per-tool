"""P3 enriched-profile deep audit: coverage, dates, language conventions, sources, duplicates."""
import json
import glob
import re
from collections import Counter, defaultdict

BASE = "output/ci/2026-10-06"
trimmed = {t["org_id"] for t in json.load(open(f"{BASE}/_p3_trim_plan.json", encoding="utf-8"))["trim"]}
issues = []
warn = []
stats = defaultdict(int)

DATE_FULL = re.compile(r"^\d{4}-\d{2}-\d{2}$")
CJK = re.compile(r"[\u4e00-\u9fff]")
person_names = defaultdict(list)  # normalized name -> [(org, name)]
event_years = Counter()

files = []
for fp in sorted(glob.glob(f"{BASE}/orgs/*.json")):
    d = json.load(open(fp, encoding="utf-8"))
    if d.get("collection_meta", {}).get("phase") != "phase3_enriched":
        continue
    files.append(d)

for d in files:
    oid = d["org_id"]
    bi = d.get("basic_info", {})
    kp = d.get("key_people") or []
    ev = d.get("recent_events") or []
    ra = d.get("related_entities") or []
    sa = d.get("social_accounts") or []
    da = d.get("digital_assets") or []
    cm = d.get("collection_meta", {})
    quotes = cm.get("quotes") or []

    stats["orgs"] += 1
    for field, lst in [("key_people", kp), ("recent_events", ev), ("related_entities", ra),
                       ("social_accounts", sa), ("digital_assets", da)]:
        stats[f"has_{field}"] += bool(lst)
        stats[f"total_{field}"] += len(lst)

    # core_business length
    cb = d.get("core_business") or ""
    stats["core_business_200plus"] += len(cb) >= 200
    if not cb:
        issues.append(f"{oid}: core_business empty")
    # apec_stance
    ap = d.get("apec_stance") or ""
    stats["apec_stance_ok"] += ("不是APEC" in ap or "非APEC" in ap or "未加入" in ap)
    if ap and not ("不是APEC" in ap or "非APEC" in ap or "未加入" in ap):
        issues.append(f"{oid}: apec_stance missing non-member declaration")
    # quotes
    if not quotes or not isinstance(quotes, list) or not isinstance(quotes[0], dict):
        issues.append(f"{oid}: quotes missing or not object array")
    else:
        stats["quotes_3plus"] += len(quotes) >= 3

    # dates & event sources
    for i, e in enumerate(ev):
        dt = e.get("date") or ""
        if not DATE_FULL.match(dt):
            issues.append(f"{oid}: recent_events[{i}] date not YYYY-MM-DD: {dt}")
        else:
            event_years[dt[:4]] += 1
        if not e.get("source"):
            issues.append(f"{oid}: recent_events[{i}] missing source")
        if not e.get("title"):
            issues.append(f"{oid}: recent_events[{i}] missing title")
    # founded_date format
    fd = bi.get("founded_date")
    if fd and not (DATE_FULL.match(fd) or re.match(r"^\d{4}-\d{2}$", fd) or re.match(r"^\d{4}$", fd)):
        issues.append(f"{oid}: founded_date bad format {fd}")

    # language conventions: key_people name 中文(法语)
    for p in kp:
        nm = p.get("name") or ""
        if CJK.search(nm) and "(" in nm:
            # chinese first: char before "(" must contain CJK
            head = nm.split("(")[0]
            if not CJK.search(head):
                issues.append(f"{oid}: key_people name not 中文(法语) order: {nm}")
        elif nm and not CJK.search(nm):
            issues.append(f"{oid}: key_people name lacks Chinese: {nm}")
        # title
        ti = p.get("title") or ""
        if ti and not CJK.search(ti):
            issues.append(f"{oid}: key_people title lacks Chinese: {ti}")
        # duplicate person tracking
        key = re.sub(r"\s*\(.*?\)\s*", "", nm).strip().lower()
        if key:
            person_names[key].append((oid, nm))

    # social platform enum
    for s in sa:
        pl = (s.get("platform") or "").lower()
        if pl not in {"facebook", "x_twitter", "twitter", "instagram", "youtube", "linkedin", "tiktok", "website", "other", "whatsapp", "telegram", "flickr"}:
            warn.append(f"{oid}: unusual social platform '{s.get('platform')}'")
        if not s.get("url"):
            issues.append(f"{oid}: social_account {pl} missing url")

# duplicate person names across orgs (possible dedup candidates for P4)
dups = {k: v for k, v in person_names.items() if len(v) > 1}

print(f"Enriched profiles audited: {len(files)}")
print()
print("=== FIELD COVERAGE ===")
n = stats["orgs"]
for f in ["key_people", "recent_events", "related_entities", "social_accounts", "digital_assets"]:
    print(f"  {f}: {stats['has_'+f]}/{n} orgs have, total {stats['total_'+f]} items")
print(f"  core_business >=200 chars: {stats['core_business_200plus']}/{n}")
print(f"  apec_stance with non-member declaration: {stats['apec_stance_ok']}/{n}")
print(f"  quotes >=3 (object array): {stats['quotes_3plus']}/{n}")
print()
print("=== EVENT YEAR DISTRIBUTION ===")
for y in sorted(event_years):
    print(f"  {y}: {event_years[y]}")
print()
print("=== CROSS-ORG DUPLICATE PERSON NAMES (P4 dedup candidates) ===")
for k, v in sorted(dups.items(), key=lambda x: -len(x[1])):
    print(f"  {v[0][1]}  ->  {sorted(set(o for o, _ in v))}")
print()
print(f"=== ISSUES: {len(issues)} ===")
for x in issues[:40]:
    print(" !", x)
print(f"=== WARNINGS: {len(warn)} ===")
for x in warn[:10]:
    print(" ~", x)
