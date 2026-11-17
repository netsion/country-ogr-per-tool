# -*- coding: utf-8 -*-
"""EG P1/P2 comprehensive audit."""
import json, glob, os, re, time, urllib.request, urllib.parse, sys
sys.path.insert(0, r"D:\ai-workspace\apec-osint-tool\.agents\skills\country-org-collector\scripts")
from atomic_write import setup_proxy, load_json
setup_proxy()

BASE = r"D:\ai-workspace\apec-osint-tool\output\eg\2026-11-16"
TMP = f"{BASE}/_tmp"

targets = load_json(f"{BASE}/_target_orgs.json")["organizations"]
orgs = {}
for p in glob.glob(f"{BASE}/orgs/*.json"):
    d = load_json(p)
    orgs[d["org_id"]] = d
reg = load_json(f"{BASE}/id_registry.json")

lines = []
def out(s=""):
    lines.append(s)

# --- 1. QID duplicates across org entries ---
qid_map = {}
for o in targets:
    q = o.get("wikidata_qid")
    if q:
        qid_map.setdefault(q, []).append(o["id"])
out("### 1. QID duplicates (target file)")
dups = {q: ids for q, ids in qid_map.items() if len(ids) > 1}
out(f"  dup QIDs: {len(dups)}")
for q, ids in dups.items():
    out(f"  !! {q}: {ids}")

# --- 2. name duplicates (normalized) ---
def norm_name(s):
    s = re.sub(r"\(.*?\)", "", s or "").lower()
    return re.sub(r"[^a-z0-9]+", " ", s).strip()
name_map = {}
for o in targets:
    k = norm_name(o.get("name"))
    if k:
        name_map.setdefault(k, []).append((o["id"], o.get("name")))
out()
out("### 2. name_en duplicates")
ndups = {k: v for k, v in name_map.items() if len(v) > 1}
out(f"  dup names: {len(ndups)}")
for k, v in ndups.items():
    out(f"  !! {k}: {v}")

# --- 3. skeleton vs target QID consistency ---
out()
out("### 3. skeleton/target QID consistency")
tq = {o["id"]: o.get("wikidata_qid") for o in targets}
mism = 0
for oid, d in orgs.items():
    sq = d["basic_info"].get("wikidata_qid")
    if sq != tq.get(oid):
        out(f"  !! {oid}: target={tq.get(oid)} skeleton={sq}")
        mism += 1
out(f"  mismatches: {mism}")

# --- 4. extract P31 / P17 per org from cache; collect distinct QIDs ---
out()
out("### 4. P31 (instance-of) / P17 (country) extraction")
p31_map, p17_map = {}, {}   # org_id -> [QIDs]
for o in targets:
    q = o.get("wikidata_qid")
    if not q:
        continue
    cache = load_json(f"{BASE}/_cache/{q}.json")
    wd = (cache or {}).get("wikidata") or {}
    claims = wd.get("claims", {})
    for prop, dst in (("P31", p31_map), ("P17", p17_map)):
        vals = []
        for c in claims.get(prop, []):
            try:
                vals.append(c["mainsnak"]["datavalue"]["value"]["id"])
            except (KeyError, TypeError):
                pass
        dst[o["id"]] = vals

_lab_cache = {}
def fetch_labels(qids):
    qids = [q for q in qids if q not in _lab_cache]
    for i in range(0, len(qids), 50):
        batch = qids[i:i+50]
        url = ("https://www.wikidata.org/w/api.php?action=wbgetentities&ids="
               + urllib.parse.quote("|".join(batch)) + "&props=labels&languages=en&format=json")
        req = urllib.request.Request(url, headers={"User-Agent": "ApecOsintTool/1.0"})
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                ents = json.loads(r.read().decode()).get("entities", {})
            for q, e in ents.items():
                _lab_cache[q] = e.get("labels", {}).get("en", {}).get("value") or "(no en label)"
        except Exception as e:
            for q in batch:
                _lab_cache[q] = f"(fetch error: {e})"
        time.sleep(1.5)

all_p31 = sorted({v for vs in p31_map.values() for v in vs})
fetch_labels(all_p31)
out(f"  distinct P31 values: {len(all_p31)}")
p31_count = {}
for vs in p31_map.values():
    for v in vs:
        p31_count[v] = p31_count.get(v, 0) + 1
for q in sorted(p31_count, key=lambda x: -p31_count[x]):
    out(f"    P31 {q} x{p31_count[q]}: {_lab_cache.get(q)}")

BAD_P31_HINT = ["human", "article", "album", "film", "song", "book", "television series", "video game", "football", "association football club"]
suspects = []
for oid, vs in p31_map.items():
    labels = [_lab_cache.get(v, "") or "" for v in vs]
    for lab in labels:
        if any(h in lab.lower() for h in BAD_P31_HINT):
            suspects.append((oid, lab))
            break
out(f"  P31-suspect orgs: {len(suspects)}")
for oid, lab in suspects:
    out(f"  !! {oid}: P31={lab}")

all_p17 = sorted({v for vs in p17_map.values() for v in vs})
fetch_labels(all_p17)
out(f"  distinct P17 values: {len(all_p17)}")
for oid, vs in sorted(p17_map.items()):
    labs = [_lab_cache.get(v, "?") for v in vs]
    if labs and not any("Egypt" in l for l in labs):
        out(f"  !! non-Egypt P17: {oid} -> {labs}")
n_no_p17 = sum(1 for vs in p17_map.values() if not vs)
out(f"  orgs with no P17 claim: {n_no_p17} (info only)")

# --- 5. person_id reference integrity ---
out()
out("### 5. person_id integrity (org key_people -> person_registry)")
preg = {e["person_id"]: e for e in reg.get("person_registry", [])}
n_refs, n_bad = 0, 0
for oid, d in sorted(orgs.items()):
    for kp in d.get("key_people", []) or []:
        pid = kp.get("person_id")
        if pid is None:
            continue
        n_refs += 1
        if pid not in preg:
            out(f"  !! {oid}: key_people '{kp.get('name')}' person_id={pid} NOT in registry")
            n_bad += 1
out(f"  person refs: {n_refs}, dangling: {n_bad}")
nmap = {}
for oid, d in orgs.items():
    for kp in d.get("key_people", []) or []:
        nmap.setdefault(norm_name(kp.get("name")), []).append((oid, kp.get("person_id")))
nname_dups = {k: v for k, v in nmap.items() if len(v) > 1}
out(f"  same key_people name in multiple orgs: {len(nname_dups)}")
for k, v in nname_dups.items():
    pids = set(x[1] for x in v)
    flag = "  !!" if len(pids) > 1 else "   (same pid, ok)"
    out(f"  {flag} '{k}': {v}")

# --- 6. key_people name format: Chinese (Arabic) ---
out()
out("### 6. key_people name format")
AR = re.compile(r"[\u0600-\u06ff]")
fmt_ok = fmt_no_ar = 0
for oid, d in orgs.items():
    for kp in d.get("key_people", []) or []:
        nm = kp.get("name") or ""
        if "(" in nm and AR.search(nm.split("(")[-1]):
            fmt_ok += 1
        else:
            fmt_no_ar += 1
out(f"  with Arabic in parens: {fmt_ok}, without: {fmt_no_ar} (skeleton uses en labels; P3 fixes)")

# --- 7. founded_date format ---
out()
out("### 7. founded_date format")
bad_dates = []
for oid, d in orgs.items():
    fd = d["basic_info"].get("founded_date")
    if fd and not re.fullmatch(r"\d{4}-\d{2}-\d{2}", fd):
        bad_dates.append((oid, fd))
out(f"  non-strict founded_date: {len(bad_dates)}")
for oid, fd in bad_dates:
    out(f"  !! {oid}: {fd}")

# --- 8. name_zh fill rate ---
out()
out("### 8. name_zh fill")
n_zh = sum(1 for d in orgs.values() if d["basic_info"].get("name_zh"))
out(f"  name_zh filled: {n_zh}/190")

# --- 9. cache integrity ---
out()
out("### 9. cache integrity")
cfiles = set(os.path.basename(p)[:-5] for p in glob.glob(f"{BASE}/_cache/*.json"))
out(f"  cache files: {len(cfiles)} (target QIDs: {len(qid_map)})")
no_cache = [o["id"] for o in targets if o.get("wikidata_qid") and o["wikidata_qid"] not in cfiles]
out(f"  QID orgs missing cache: {len(no_cache)} {no_cache[:10]}")
no_wp = [q for q in cfiles if not ((load_json(f'{BASE}/_cache/{q}.json') or {}).get('wikipedia'))]
out(f"  caches without wikipedia: {len(no_wp)}")

# --- 10. registry counters vs files ---
out()
out("### 10. registry vs files")
from collections import Counter
fc = Counter(d["basic_info"]["org_type"] for d in orgs.values())
rc = reg["counters"]["EG"]
out(f"  files: {dict(sorted(fc.items()))}")
out(f"  counters: {rc}")
for t in set(list(fc) + list(rc)):
    if fc.get(t, 0) != rc.get(t, 0):
        out(f"  !! type {t}: files={fc.get(t,0)} counters={rc.get(t,0)}")

# --- 11. full org table for trim review ---
out()
out("### 11. full org list (for trim review)")
for o in targets:
    oid = o["id"]
    d = orgs.get(oid, {})
    q = "Y" if o.get("wikidata_qid") else "N"
    kp = len(d.get("key_people") or [])
    soc = len(d.get("social_accounts") or [])
    sc = d.get("collection_meta", {}).get("completeness_score", "?")
    vs = o.get("verification_status", "?")
    out(f"  {oid} | {o.get('category')} | qid:{q} | kp:{kp} soc:{soc} sc:{sc} | {vs} | {o.get('name')} | sub:{o.get('subcategory')}")

with open(f"{TMP}/audit_report.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(lines))
print("audit written:", len(lines), "lines")
