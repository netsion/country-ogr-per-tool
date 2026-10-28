# -*- coding: utf-8 -*-
"""Supplementary label-based SPARQL queries for Bolivia GOV/SOE/MIL."""
import json
import os
import subprocess
import time

PROXY = "http://127.0.0.1:7890"
ENDPOINT = "https://query.wikidata.org/sparql"
OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sparql")
SLEEP_BETWEEN = 14

COMMON = """
  ?org wdt:P17 wd:Q750 .
  ?org wdt:P31 ?type .
  ?org rdfs:label ?nameEs .
  FILTER(LANG(?nameEs) = "es")
  OPTIONAL { ?org wdt:P159 ?hq . }
  OPTIONAL { ?org wdt:P571 ?inception . }
  OPTIONAL { ?org wdt:P856 ?website . }
  OPTIONAL { ?org rdfs:label ?nameEn . FILTER(LANG(?nameEn) = "en") }
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en,zh". }
"""

QUERIES = {
    "supp_ministries": f"""SELECT DISTINCT ?org ?nameEs ?nameEn ?orgDescription ?type ?typeLabel ?hqLabel ?inception ?website WHERE {{
  {COMMON}
  FILTER(STRSTARTS(?nameEs, "Ministerio"))
}} LIMIT 100""",
    "supp_state_enterprises": f"""SELECT DISTINCT ?org ?nameEs ?nameEn ?orgDescription ?type ?typeLabel ?hqLabel ?inception ?website WHERE {{
  {COMMON}
  FILTER(STRSTARTS(?nameEs, "Empresa") || CONTAINS(?nameEs, "Yacimientos") || STRSTARTS(?nameEs, "Corporaci") || STRSTARTS(?nameEs, "Servicio de") || STRSTARTS(?nameEs, "Autoridad de"))
}} LIMIT 150""",
    "supp_military": f"""SELECT DISTINCT ?org ?nameEs ?nameEn ?orgDescription ?type ?typeLabel ?hqLabel ?inception ?website WHERE {{
  {COMMON}
  FILTER(CONTAINS(?nameEs, "Fuerza") || CONTAINS(?nameEs, "Ej") || CONTAINS(?nameEs, "Polic") || CONTAINS(?nameEs, "Armada"))
}} LIMIT 100""",
}


def run_query(name: str, query: str) -> None:
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


def main() -> None:
    for i, (name, query) in enumerate(QUERIES.items()):
        if i > 0:
            time.sleep(SLEEP_BETWEEN)
        print(f"Running {name} ...", flush=True)
        run_query(name, query)
    print("Done.")


if __name__ == "__main__":
    main()
