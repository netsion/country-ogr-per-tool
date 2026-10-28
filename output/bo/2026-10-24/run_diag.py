# -*- coding: utf-8 -*-
"""Diagnostic: discover P31 class distribution for Bolivia orgs, then targeted follow-ups."""
import json
import os
import subprocess
import sys
import time

PROXY = "http://127.0.0.1:7890"
ENDPOINT = "https://query.wikidata.org/sparql"
OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sparql")
os.makedirs(OUT_DIR, exist_ok=True)
SLEEP_BETWEEN = 14

DIAG = """SELECT ?type ?typeLabel (COUNT(?org) AS ?cnt) WHERE {
  ?org wdt:P17 wd:Q750 .
  ?org wdt:P31 ?type .
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en,zh". }
} GROUP BY ?type ?typeLabel ORDER BY DESC(?cnt) LIMIT 120"""

# To be filled after diagnostic: targeted queries by discovered classes
TARGET_TMPL = """SELECT ?org ?nameEs ?orgLabel ?orgDescription ?typeLabel ?hqLabel ?inception ?website WHERE {{
  ?org wdt:P17 wd:Q750 .
  ?org wdt:P31 ?type .
  VALUES ?type {{ {types} }}
  OPTIONAL {{ ?org rdfs:label ?nameEs . FILTER(LANG(?nameEs) = "es") }}
  OPTIONAL {{ ?org wdt:P159 ?hq . }}
  OPTIONAL {{ ?org wdt:P571 ?inception . }}
  OPTIONAL {{ ?org wdt:P856 ?website . }}
  SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en,zh". }}
}} LIMIT 400"""


def run_query(name: str, query: str) -> str:
    out_path = os.path.join(OUT_DIR, f"{name}.json")
    cmd = [
        "curl", "--proxy", PROXY, "-s", "-L",
        "-H", "User-Agent: ApecOsintResearch/1.0 (contact: research@example.org)",
        "-H", "Accept: application/sparql-results+json",
        "-G", "--data-urlencode", f"query={query}",
        "--data-urlencode", "format=json",
        ENDPOINT, "-o", out_path, "--max-time", "120",
    ]
    subprocess.run(cmd, check=True, timeout=150)
    with open(out_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    n = len(data.get("results", {}).get("bindings", []))
    print(f"[OK] {name}: {n} bindings", flush=True)
    return out_path


def main() -> None:
    p = run_query("diag_p31", DIAG)
    with open(p, "r", encoding="utf-8") as f:
        data = json.load(f)
    rows = []
    for b in data["results"]["bindings"]:
        qid = b["type"]["value"].rsplit("/", 1)[-1]
        label = b.get("typeLabel", {}).get("value", "")
        cnt = b["cnt"]["value"]
        rows.append((int(cnt), qid, label))
        print(cnt, qid, label)


if __name__ == "__main__":
    main()
