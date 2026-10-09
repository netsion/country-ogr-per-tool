"""P1/P2 data audit: consistency, duplicates, registry cross-refs, cache coverage."""
import json
import glob
import os
import re
from collections import Counter, defaultdict

BASE = "output/ci/2026-10-06"
issues = []
info = []

# ---------- Load all artifacts ----------
with open(f"{BASE}/_target_orgs.json", encoding="utf-8") as f:
    targets = json.load(f)

org_files = {}
for fp in glob.glob(f"{BASE}/orgs/*.json"):
    with open(fp, encoding="utf-8") as f:
        d = json.load(f)
    org_files[d["org_id"]] = d

with open(f"{BASE}/id_registry.json", encoding="utf-8") as f:
    reg = json.load(f)

cache_files = set()
for fp in glob.glob(f"{BASE}/_cache/*.json"):
    qid = os.path.splitext(os.path.basename(fp))[0]
    try:
        with open(fp, encoding="utf-8") as f:
            json.load(f)
        cache_files.add(qid)
    except Exception as e:
        issues.append(f"CACHE: corrupt JSON {fp}: {e}")

with open(f"{BASE}/_name_index.json", encoding="utf-8") as f:
    name_index = json.load(f)

info.append(f"targets={len(targets)} org_files={len(org_files)} cache={len(cache_files)} "
            f"registry_orgs={len(reg.get('registry', []))} registry_persons={len(reg.get('person_registry', []))}")

# ---------- 1. Target list checks ----------
t_ids = [t["id"] for t in targets]
dup_t_ids = [i for i, n in Counter(t_ids).items() if n > 1]
if dup_t_ids:
    issues.append(f"TARGET: duplicate ids {dup_t_ids}")

id_pat = re.compile(r"^CI-(GOV|SOE|CORP|NGO|ACAD|MEDIA|FIN|INTL|PARTY|MIL)-\d{3}$")
for t in targets:
    if not id_pat.match(t["id"]):
        issues.append(f"TARGET: bad id format {t['id']}")
    if t.get("country") != "CI":
        issues.append(f"TARGET: country != CI: {t['id']} = {t.get('country')}")
    qid = t.get("qid") or t.get("wikidata_qid")
    if qid and not re.match(r"^Q\d+$", qid):
        issues.append(f"TARGET: bad qid format {t['id']}: {qid}")

# sequence continuity per type
seqs = defaultdict(list)
for t in targets:
    m = id_pat.match(t["id"])
    if m:
        seqs[t["id"].split("-")[1]].append(int(t["id"].split("-")[2]))
for typ, lst in seqs.items():
    lst.sort()
    expect = list(range(1, len(lst) + 1))
    if lst != expect:
        gaps = sorted(set(range(1, max(lst) + 1)) - set(lst))
        info.append(f"TARGET: {typ} seq has gaps {gaps} (count={len(lst)})")

# ---------- 2. Duplicate org names (fuzzy: normalized) ----------
def norm(s):
    s = (s or "").lower()
    s = re.sub(r"[^a-z0-9\u4e00-\u9fff\u0600-\u06ff\u00c0-\u024f]", "", s)
    return s

seen_names = defaultdict(list)
for t in targets:
    key = norm(t.get("name", ""))
    if key:
        seen_names[key].append(t["id"])
for k, ids in seen_names.items():
    if len(ids) > 1:
        issues.append(f"TARGET: exact duplicate name -> {ids}")

# token-overlap fuzzy dup detection (Jaccard on tokens > 0.7)
entries = [(t["id"], set(norm(t.get("name", ""))).union(set(norm(t.get("name", "").replace(" ", ""))))) for t in targets]
names_toks = [(t["id"], set(re.findall(r"[a-z\u00e0-\u024f]+", (t.get("name") or "").lower()))) for t in targets]
fuzzy_reported = set()
for i in range(len(names_toks)):
    for j in range(i + 1, len(names_toks)):
        a, b = names_toks[i], names_toks[j]
        if not a[1] or not b[1]:
            continue
        stop = {"de", "du", "la", "le", "des", "cote", "divoire", "ivory", "coast", "national", "nationale", "banque"}
        aa, bb = a[1] - stop, b[1] - stop
        if not aa or not bb:
            continue
        jac = len(aa & bb) / len(aa | bb)
        if jac > 0.7 and (a[0], b[0]) not in fuzzy_reported:
            fuzzy_reported.add((a[0], b[0]))
            issues.append(f"TARGET: possible near-duplicate (jac={jac:.2f}): {a[0]} vs {b[0]}")

# ---------- 3. QID collisions across orgs ----------
qid_owner = defaultdict(list)
for t in targets:
    qid = t.get("qid") or t.get("wikidata_qid")
    if qid:
        qid_owner[qid].append(t["id"])
for qid, ids in qid_owner.items():
    if len(ids) > 1:
        issues.append(f"TARGET: QID {qid} shared by {ids}")

# conflicting qid vs wikidata_qid
conflicts = []
for t in targets:
    q1, q2 = t.get("qid"), t.get("wikidata_qid")
    if q1 and q2 and q1 != q2:
        conflicts.append((t["id"], q1, q2))
if conflicts:
    issues.append(f"TARGET: qid vs wikidata_qid conflict (qid wins): {conflicts}")

# ---------- 4. Cache coverage ----------
org_qids = {}
for t in targets:
    qid = t.get("qid") or t.get("wikidata_qid")
    if qid:
        org_qids[t["id"]] = qid
missing_cache = [oid for oid, q in org_qids.items() if q not in cache_files]
orphan_cache = [q for q in cache_files if q not in set(org_qids.values())]
if missing_cache:
    issues.append(f"CACHE: orgs with QID but no cache: {missing_cache}")
if orphan_cache:
    issues.append(f"CACHE: cache files not referenced by any org: {orphan_cache}")

# cache content sanity: wikidata + wikipedia blocks
thin = []
for fp in glob.glob(f"{BASE}/_cache/*.json"):
    with open(fp, encoding="utf-8") as f:
        c = json.load(f)
    wd = c.get("wikidata") or {}
    labels = wd.get("labels") or {}
    if not labels and not (c.get("wikipedia") or {}).get("extract"):
        thin.append(os.path.basename(fp))
if thin:
    issues.append(f"CACHE: {len(thin)} thin caches (no labels & no extract): {thin[:5]}...")

# ---------- 5. Org files vs registry ----------
reg_org_ids = {r.get("org_id") for r in reg.get("registry", [])}
for oid in org_files:
    if oid not in reg_org_ids:
        issues.append(f"REGISTRY: org file {oid} not in registry")
for oid in reg_org_ids:
    if oid and not oid.startswith("Q") and oid not in org_files and not oid.startswith("CI-PERSON"):
        # registry entries may include related entities not yet profiled (ok) — only flag if marked profiled
        entry = next((r for r in reg["registry"] if r.get("org_id") == oid), {})
        if entry.get("status") == "profiled":
            issues.append(f"REGISTRY: {oid} marked profiled but no file")

# org file basic sanity
for oid, d in org_files.items():
    if d["basic_info"].get("hq_country_iso3") != "CIV":
        issues.append(f"ORG: {oid} hq_country_iso3={d['basic_info'].get('hq_country_iso3')}")
    kp = d.get("key_people") or []
    for p in kp:
        if p.get("person_id") and not p.get("person_id").startswith("CI-PERSON"):
            issues.append(f"ORG: {oid} key_people person_id format: {p.get('person_id')}")
    # leftover Inter Milan contamination check
    blob = json.dumps(d, ensure_ascii=False)
    for tok in ["Moratti", "Masseroni", "Facchetti", "Thohir", "Kangyang", "Paramithiotti", "Inter Milan", "国际米兰"]:
        if tok in blob:
            issues.append(f"ORG: {oid} leftover contamination token: {tok}")

# ---------- 6. person_registry sanity ----------
p_ids = [p.get("person_id") for p in reg.get("person_registry", [])]
dup_p = [i for i, n in Counter(p_ids).items() if n > 1]
if dup_p:
    issues.append(f"REGISTRY: duplicate person_ids {dup_p}")
for p in reg.get("person_registry", []):
    for so in p.get("source_orgs", []):
        if so not in org_files:
            issues.append(f"REGISTRY: person {p['person_id']} references missing org {so}")

# person name sanity: Inter Milan-like leftovers
for p in reg.get("person_registry", []):
    if "CI-MEDIA-006" in (p.get("source_orgs") or []):
        issues.append(f"REGISTRY: person {p['person_id']} still references CI-MEDIA-006")

# ---------- 7. APEC compliance scan ----------
for t in targets:
    blob = json.dumps(t, ensure_ascii=False).lower()
    if "apec" in blob:
        issues.append(f"TARGET: mentions APEC: {t['id']}")
for oid, d in org_files.items():
    if d.get("apec_stance"):
        s = d["apec_stance"].lower()
        if ("member" in s or "加入" in s or "成员" in s) and "不是apec" not in s and "非apec" not in s and "未加入" not in s:
            issues.append(f"ORG: {oid} apec_stance may falsely claim membership: {d['apec_stance'][:80]}")

# ---------- 8. name_index validity ----------
n_entries = 0
if isinstance(name_index, dict):
    for k, v in name_index.items():
        if isinstance(v, list):
            n_entries += len(v)
info.append(f"name_index: {len(name_index)} top keys, ~{n_entries} entries")

print("=== INFO ===")
for i in info:
    print(" ", i)
print()
print("=== ISSUES ===")
if issues:
    for x in issues:
        print(" !", x)
else:
    print("  none")
print(f"\nTotal issues: {len(issues)}")
