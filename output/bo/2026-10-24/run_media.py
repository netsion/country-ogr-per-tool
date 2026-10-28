# -*- coding: utf-8 -*-
"""Media-specific SPARQL: newspapers, radio, TV, news agencies for Bolivia."""
import json
import os
import subprocess

PROXY = "http://127.0.0.1:7890"
ENDPOINT = "https://query.wikidata.org/sparql"
OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sparql")

QUERY = """SELECT DISTINCT ?org ?nameEs ?nameEn ?orgDescription ?typeLabel ?hqLabel ?founded ?website WHERE {
  ?org wdt:P17 wd:Q750 .
  ?org wdt:P31 ?type .
  VALUES ?type { wd:Q11032 wd:Q192621 wd:Q14350 wd:Q192283 wd:Q1191058 wd:Q488383 wd:Q111444827 wd:Q2085381 wd:Q1153192 wd:Q1979417 }
  OPTIONAL { ?org rdfs:label ?nameEs . FILTER(LANG(?nameEs) = "es") }
  OPTIONAL { ?org rdfs:label ?nameEn . FILTER(LANG(?nameEn) = "en") }
  OPTIONAL { ?org wdt:P159 ?hq . }
  OPTIONAL { ?org wdt:P571 ?founded . }
  OPTIONAL { ?org wdt:P856 ?website . }
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en,zh". }
} LIMIT 200"""


def main() -> None:
    out_path = os.path.join(OUT_DIR, "supp_media.json")
    cmd = [
        "curl", "--proxy", PROXY, "-s", "-L",
        "-H", "User-Agent: ApecOsintResearch/1.0 (contact: research@example.org)",
        "-H", "Accept: application/sparql-results+json",
        "-G", "--data-urlencode", f"query={QUERY}",
        "--data-urlencode", "format=json",
        ENDPOINT, "-o", out_path, "--max-time", "150",
    ]
    subprocess.run(cmd, check=True, timeout=170)
    with open(out_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    for b in data["results"]["bindings"]:
        qid = b["org"]["value"].rsplit("/", 1)[-1]
        name = b.get("nameEs", {}).get("value") or b.get("orgLabel", {}).get("value", "?")
        print(qid, "|", name, "|", b.get("typeLabel", {}).get("value", ""), "|", (b.get("orgDescription", {}).get("value") or "")[:50])


if __name__ == "__main__":
    main()
