"""Scan ALL orgs: cached Wikidata identity vs target-list name, flag cross-country mismatches."""
import json
import glob
import re

BASE = "output/ci/2026-10-06"

with open(f"{BASE}/_target_orgs.json", encoding="utf-8") as f:
    targets = {t["id"]: t for t in json.load(f)}

GENERIC = {
    "ministry", "ministere", "ministère", "of", "the", "de", "du", "la", "le", "les", "des",
    "national", "nationale", "cote", "divoire", "ivory", "coast", "ivorian", "ivoirien",
    "ivoirienne", "republic", "republique", "general", "generale", "and", "et", "for",
    "center", "centre", "agency", "agence", "office", "bureau", "company", "societe",
    "international", "internationale", "banque", "bank", "group", "groupe", "council",
    "conseil", "authority", "autonomous", "port", "autonome", "institute", "institut",
    "university", "universite", "school", "ecole", "chamber", "chambre", "fund", "fonds",
    "association", "foundation", "fondation", "party", "parti", "politique", "political",
    "union", "africa", "afrique", "african", "africain", "west", "ouest", "organisation",
    "organization", "organisation", "regionale", "regional", "states", "etats", "economique",
    "economic", "monetary", "monetaire", "central", "development", "developpement",
}

def toks(s):
    return {t for t in re.findall(r"[a-zà-ÿ]+", (s or "").lower()) if len(t) > 2} - GENERIC

def cache_label(qid):
    try:
        with open(f"{BASE}/_cache/{qid}.json", encoding="utf-8") as f:
            c = json.load(f)
    except FileNotFoundError:
        return None, None, None, None
    wd = c.get("wikidata") or {}
    labels = wd.get("labels") or {}
    descs = wd.get("descriptions") or {}
    en = labels.get("en", {}).get("value")
    fr = labels.get("fr", {}).get("value")
    desc = (descs.get("en") or descs.get("fr") or {}).get("value")
    return en, fr, desc, c

suspicious = []
for oid, t in sorted(targets.items()):
    qid = t.get("qid") or t.get("wikidata_qid")
    if not qid:
        continue
    en, fr, desc, c = cache_label(qid)
    if en is None and fr is None:
        suspicious.append((oid, t["name"][:40], qid, "NO CACHE", "", ""))
        continue
    t_tok = toks(t["name"])
    l_tok = toks(en) | toks(fr)
    # distinctive target tokens not present in label
    missing = t_tok - l_tok
    overlap = len(t_tok & l_tok) / max(1, len(t_tok | l_tok))
    # country indicators in label/desc that contradict CI
    blob = f"{en} {fr} {desc}".lower()
    wrong_country = [x for x in ["senegal", "greece", "turkey", "turkish", "mali", "burkina",
                                 "guinea", "nigeria", "ghana", "france", "belgium", "switzerland",
                                 "morocco", "tunisia", "algeria", "cameroon", "benin", "togo", "niger"] if x in blob]
    if overlap < 0.34 or (missing and len(missing) >= 2) or wrong_country:
        suspicious.append((oid, t["name"][:40], qid, f"{en} | {fr}"[:60], f"ov={overlap:.2f} miss={sorted(missing)[:4]}", f"country?={wrong_country}"))

print(f"Suspicious: {len(suspicious)}")
for s in suspicious:
    print(" ", s)
