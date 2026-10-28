# -*- coding: utf-8 -*-
"""Run Wikidata SPARQL queries for Bolivia (Q750) with rate limiting.
Usage: python run_sparql.py <batch: 1|2>
"""
import json
import os
import subprocess
import sys
import time

PROXY = "http://127.0.0.1:7890"
ENDPOINT = "https://query.wikidata.org/sparql"
OUT_DIR = os.path.dirname(os.path.abspath(__file__))
SPARQL_DIR = os.path.join(OUT_DIR, "sparql")
os.makedirs(SPARQL_DIR, exist_ok=True)
SLEEP_BETWEEN = 14  # seconds, >=12s rate limit

COUNTRY = "wd:Q750"
LABEL_ES = 'OPTIONAL { ?org rdfs:label ?nameEs . FILTER(LANG(?nameEs) = "es") }'
LBL = 'SERVICE wikibase:label { bd:serviceParam wikibase:language "en,zh". }'

QUERIES = {}

# Template H: state organs (priority)
QUERIES["H_state_organs"] = f"""SELECT ?org ?nameEs ?orgLabel ?orgDescription ?typeLabel ?parentLabel ?headLabel ?website WHERE {{
  ?org wdt:P17 {COUNTRY} .
  ?org wdt:P31 ?type .
  VALUES ?type {{ wd:Q648294 wd:Q4164870 wd:Q11204 wd:Q190752 wd:Q41487 wd:Q845161 wd:Q12106 wd:Q193505 }}
  {LABEL_ES}
  OPTIONAL {{ ?org wdt:P749 ?parent . }}
  OPTIONAL {{ ?org wdt:P1308 ?head . }}
  OPTIONAL {{ ?org wdt:P856 ?website . }}
  {LBL}
}} LIMIT 300"""

# Template A: general orgs
QUERIES["A_general"] = f"""SELECT ?org ?nameEs ?orgLabel ?orgDescription ?typeLabel ?hqLabel ?inception ?website WHERE {{
  ?org wdt:P17 {COUNTRY} .
  ?org wdt:P31 ?type .
  VALUES ?type {{ wd:Q43229 wd:Q4830453 wd:Q783794 wd:Q327333 wd:Q648294 wd:Q3918 wd:Q7278 wd:Q22687 wd:Q163740 wd:Q192621 wd:Q15416 wd:Q3230 wd:Q176742 wd:Q484652 }}
  {LABEL_ES}
  OPTIONAL {{ ?org wdt:P159 ?hq . }}
  OPTIONAL {{ ?org wdt:P571 ?inception . }}
  OPTIONAL {{ ?org wdt:P856 ?website . }}
  {LBL}
}} LIMIT 600"""

# Template B: companies (CORP)
QUERIES["B_corp"] = f"""SELECT ?org ?nameEs ?orgLabel ?orgDescription ?industryLabel ?employees ?revenue ?hqLabel ?website WHERE {{
  ?org wdt:P17 {COUNTRY} .
  ?org wdt:P31 ?type .
  VALUES ?type {{ wd:Q4830453 wd:Q783794 }}
  {LABEL_ES}
  OPTIONAL {{ ?org wdt:P452 ?industry . }}
  OPTIONAL {{ ?org wdt:P1128 ?employees . }}
  OPTIONAL {{ ?org wdt:P2139 ?revenue . }}
  OPTIONAL {{ ?org wdt:P159 ?hq . }}
  OPTIONAL {{ ?org wdt:P856 ?website . }}
  {LBL}
}} LIMIT 300"""

# Template C: academic (ACAD)
QUERIES["C_acad"] = f"""SELECT ?org ?nameEs ?orgLabel ?orgDescription ?typeLabel ?established ?website WHERE {{
  ?org wdt:P17 {COUNTRY} .
  ?org wdt:P31 ?type .
  VALUES ?type {{ wd:Q3918 wd:Q31855 wd:Q15978631 }}
  {LABEL_ES}
  OPTIONAL {{ ?org wdt:P571 ?established . }}
  OPTIONAL {{ ?org wdt:P856 ?website . }}
  {LBL}
}} LIMIT 200"""

# Template D: political parties (PARTY)
QUERIES["D_party"] = f"""SELECT ?org ?nameEs ?orgLabel ?orgDescription ?ideologyLabel ?chairLabel ?founded ?website WHERE {{
  ?org wdt:P17 {COUNTRY} .
  ?org wdt:P31 wd:Q7278 .
  {LABEL_ES}
  OPTIONAL {{ ?org wdt:P1142 ?ideology . }}
  OPTIONAL {{ ?org wdt:P488 ?chair . }}
  OPTIONAL {{ ?org wdt:P571 ?founded . }}
  OPTIONAL {{ ?org wdt:P856 ?website . }}
  {LBL}
}} LIMIT 150"""

# Template E: media (MEDIA)
QUERIES["E_media"] = f"""SELECT ?org ?nameEs ?orgLabel ?orgDescription ?typeLabel ?hqLabel ?founded ?website WHERE {{
  ?org wdt:P17 {COUNTRY} .
  ?org wdt:P31 ?type .
  VALUES ?type {{ wd:Q192621 wd:Q15416 wd:Q2085381 wd:Q1153192 }}
  {LABEL_ES}
  OPTIONAL {{ ?org wdt:P159 ?hq . }}
  OPTIONAL {{ ?org wdt:P571 ?founded . }}
  OPTIONAL {{ ?org wdt:P856 ?website . }}
  {LBL}
}} LIMIT 200"""

# Template F: financial institutions (FIN)
QUERIES["F_fin"] = f"""SELECT ?org ?nameEs ?orgLabel ?orgDescription ?typeLabel ?hqLabel ?founded ?website WHERE {{
  ?org wdt:P17 {COUNTRY} .
  ?org wdt:P31 ?type .
  VALUES ?type {{ wd:Q22687 wd:Q1290325 }}
  {LABEL_ES}
  OPTIONAL {{ ?org wdt:P159 ?hq . }}
  OPTIONAL {{ ?org wdt:P571 ?founded . }}
  OPTIONAL {{ ?org wdt:P856 ?website . }}
  {LBL}
}} LIMIT 200"""

# Extra: state-owned enterprises (SOE)
QUERIES["SOE"] = f"""SELECT ?org ?nameEs ?orgLabel ?orgDescription ?industryLabel ?hqLabel ?founded ?website WHERE {{
  ?org wdt:P17 {COUNTRY} .
  ?org wdt:P31 ?type .
  VALUES ?type {{ wd:Q3230 wd:Q582058 }}
  {LABEL_ES}
  OPTIONAL {{ ?org wdt:P452 ?industry . }}
  OPTIONAL {{ ?org wdt:P159 ?hq . }}
  OPTIONAL {{ ?org wdt:P571 ?founded . }}
  OPTIONAL {{ ?org wdt:P856 ?website . }}
  {LBL}
}} LIMIT 200"""

# Extra: NGO / nonprofit
QUERIES["NGO"] = f"""SELECT ?org ?nameEs ?orgLabel ?orgDescription ?typeLabel ?hqLabel ?founded ?website WHERE {{
  ?org wdt:P17 {COUNTRY} .
  ?org wdt:P31 ?type .
  VALUES ?type {{ wd:Q163740 wd:Q43229 wd:Q104932 }}
  {LABEL_ES}
  OPTIONAL {{ ?org wdt:P159 ?hq . }}
  OPTIONAL {{ ?org wdt:P571 ?founded . }}
  OPTIONAL {{ ?org wdt:P856 ?website . }}
  {LBL}
}} LIMIT 300"""

# Extra: military / security
QUERIES["MIL"] = f"""SELECT ?org ?nameEs ?orgLabel ?orgDescription ?typeLabel ?hqLabel ?founded ?website WHERE {{
  ?org wdt:P17 {COUNTRY} .
  ?org wdt:P31 ?type .
  VALUES ?type {{ wd:Q176742 wd:Q1138001 }}
  {LABEL_ES}
  OPTIONAL {{ ?org wdt:P159 ?hq . }}
  OPTIONAL {{ ?org wdt:P571 ?founded . }}
  OPTIONAL {{ ?org wdt:P856 ?website . }}
  {LBL}
}} LIMIT 100"""

BATCHES = {
    "1": ["H_state_organs", "SOE", "B_corp", "C_acad"],
    "2": ["D_party", "E_media", "F_fin", "A_general", "NGO", "MIL"],
}


def run_query(name: str, query: str) -> None:
    out_path = os.path.join(SPARQL_DIR, f"{name}.json")
    cmd = [
        "curl", "--proxy", PROXY, "-s", "-L",
        "-H", "User-Agent: ApecOsintResearch/1.0 (contact: research@example.org)",
        "-H", "Accept: application/sparql-results+json",
        "-G", "--data-urlencode", f"query={query}",
        "--data-urlencode", "format=json",
        ENDPOINT,
        "-o", out_path,
        "--max-time", "120",
    ]
    t0 = time.time()
    try:
        subprocess.run(cmd, check=True, timeout=150)
        size = os.path.getsize(out_path)
        with open(out_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        n = len(data.get("results", {}).get("bindings", []))
        print(f"[OK] {name}: {n} bindings, {size} bytes, {time.time()-t0:.1f}s")
    except Exception as exc:  # noqa: BLE001
        print(f"[FAIL] {name}: {exc}", flush=True)


def main() -> None:
    batch = sys.argv[1]
    names = BATCHES[batch]
    for i, name in enumerate(names):
        if i > 0:
            time.sleep(SLEEP_BETWEEN)
        print(f"Running {name} ...", flush=True)
        run_query(name, QUERIES[name])
    print("Batch done.")


if __name__ == "__main__":
    main()
