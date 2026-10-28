# -*- coding: utf-8 -*-
"""Retry remaining supplementary queries with backoff."""
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
    "supp_state_enterprises": f"""SELECT DISTINCT ?org ?nameEs ?nameEn ?orgDescription ?type ?typeLabel ?hqLabel ?inception ?website WHERE {{
  {COMMON}
  FILTER(STRSTARTS(?nameEs, "Empresa") || STRSTARTS(?nameEs, "Corporaci") || STRSTARTS(?nameEs, "Servicio de") || STRSTARTS(?nameEs, "Autoridad de") || STRSTARTS(?nameEs, "Yacimientos"))
}} LIMIT 150""",
    "supp_military": f"""SELECT DISTINCT ?org ?nameEs ?nameEn ?orgDescription ?type ?typeLabel ?hqLabel ?inception ?website WHERE {{
  {COMMON}
  FILTER(STRSTARTS(?nameEs, "Fuerza") || STRSTARTS(?nameEs, "Ej") || STRSTARTS(?nameEs, "Polic") || STRSTARTS(?nameEs, "Armada"))
}} LIMIT 100""",
}


def run_query(name: str, query: str, retries: int = 3) -> None:
    out_path = os.path.join(OUT_DIR, f"{name}.json")
    cmd = [
        "curl", "--proxy", PROXY, "-s", "-L",
        "-H", "User-Agent: ApecOsintResearch/1.0 (contact: research@example.org)",
        "-H", "Accept: application/sparql-results+json",
        "-G", "--data-urlencode", f"query={query}",
        "--data-urlencode", "format=json",
        ENDPOINT, "-o", out_path, "--max-time", "150",
    ]
    for attempt in range(1, retries + 1):
        try:
            subprocess.run(cmd, check=True, timeout=170)
            with open(out_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            n = len(data.get("results", {}).get("bindings", []))
            print(f"[OK] {name}: {n} bindings", flush=True)
            return
        except Exception as exc:  # noqa: BLE001
            print(f"[RETRY {attempt}] {name}: {exc}", flush=True)
            time.sleep(20)
    print(f"[FAIL] {name}", flush=True)


def main() -> None:
    for i, (name, query) in enumerate(QUERIES.items()):
        if i > 0:
            time.sleep(SLEEP_BETWEEN)
        print(f"Running {name} ...", flush=True)
        run_query(name, query)
    print("Done.")


if __name__ == "__main__":
    main()
