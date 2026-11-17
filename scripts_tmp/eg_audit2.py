# -*- coding: utf-8 -*-
"""EG audit follow-up: suspicious P31 -> org mapping; shared person_id check; entity desc fetch."""
import json, glob, re, time, urllib.request, urllib.parse, sys
sys.path.insert(0, r"D:\ai-workspace\apec-osint-tool\.agents\skills\country-org-collector\scripts")
from atomic_write import setup_proxy, load_json
setup_proxy()

BASE = r"D:\ai-workspace\apec-osint-tool\output\eg\2026-11-16"
targets = load_json(f"{BASE}/_target_orgs.json")["organizations"]
tmap = {o["id"]: o for o in targets}

SUS = {
    "Q4167410": "Wikimedia disambiguation page",
    "Q79007": "street",
    "Q721329": "direct-broadcast satellite",
    "Q12832168": "artificial satellite",
    "Q620615": "mobile app",
    "Q13499": "debit card",
    "Q35127": "website",
    "Q45400320": "open-access publisher",
    "Q18127": "record label",
}

lines = []
def out(s=""):
    lines.append(s)

out("### A. suspicious P31 -> org mapping")
sus_orgs = set()
for o in targets:
    q = o.get("wikidata_qid")
    if not q:
        continue
    cache = load_json(f"{BASE}/_cache/{q}.json")
    claims = ((cache or {}).get("wikidata") or {}).get("claims", {})
    p31 = []
    for c in claims.get("P31", []):
        try:
            p31.append(c["mainsnak"]["datavalue"]["value"]["id"])
        except (KeyError, TypeError):
            pass
    hit = [f"{v}({SUS[v]})" for v in p31 if v in SUS]
    if hit:
        sus_orgs.add(q)
        out(f"  {o['id']} {o['name']} qid={q} P31-hit={hit} fullP31={p31}")

out()
out("### B. shared person_id across orgs (name consistency)")
orgs = {}
for p in glob.glob(f"{BASE}/orgs/*.json"):
    d = load_json(p)
    orgs[d["org_id"]] = d
reg = load_json(f"{BASE}/id_registry.json")
preg = {e["person_id"]: e for e in reg.get("person_registry", [])}
pid_usage = {}
for oid, d in orgs.items():
    for kp in d.get("key_people", []) or []:
        pid = kp.get("person_id")
        if pid:
            pid_usage.setdefault(pid, []).append((oid, kp.get("name"), kp.get("title")))
for pid, uses in sorted(pid_usage.items()):
    if len(uses) > 1:
        out(f"  {pid} | registry: {preg.get(pid, {}).get('name')} | qid={preg.get(pid, {}).get('wikidata_qid')}")
        for oid, nm, ti in uses:
            out(f"    - {oid}: name='{nm}' title='{ti}'")

out()
out("### C. person_registry sample (first 12 + those shared)")
for pid, e in list(sorted(preg.items()))[:12]:
    out(f"  {pid}: {e.get('name')} | qid={e.get('wikidata_qid')} | org={e.get('org_id') or e.get('source_org_id') or e.get('orgs')}")
for pid in [p for p, u in pid_usage.items() if len(u) > 1]:
    e = preg.get(pid, {})
    out(f"  shared {pid}: {e}")

out()
out("### D. fetch en/ar label+desc for suspicious & trim-candidate QIDs")
FETCH = sorted(sus_orgs) + ["Q1998063"]
out(f"  qids to fetch: {FETCH}")
for i in range(0, len(FETCH), 40):
    batch = FETCH[i:i+40]
    url = ("https://www.wikidata.org/w/api.php?action=wbgetentities&ids="
           + urllib.parse.quote("|".join(batch)) + "&props=labels|descriptions|claims&languages=en|ar&format=json")
    req = urllib.request.Request(url, headers={"User-Agent": "ApecOsintTool/1.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        ents = json.loads(r.read().decode()).get("entities", {})
    for q, e in ents.items():
        lab = e.get("labels", {})
        desc = e.get("descriptions", {})
        nclaims = len(e.get("claims", {}))
        out(f"  {q}: en={lab.get('en',{}).get('value')} | ar={lab.get('ar',{}).get('value')} | desc={desc.get('en',{}).get('value')} | claims={nclaims}")
    time.sleep(2)

with open(f"{BASE}/_tmp/audit_followup.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(lines))
print("written")
