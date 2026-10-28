# -*- coding: utf-8 -*-
"""Second-pass targeted Wikidata search for remaining orgs."""
import json
import os
import subprocess
import time

PROXY = "http://127.0.0.1:7890"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "wd_search2.json")

SEARCHES = {
    "TSE_gov": [("Órgano Electoral Plurinacional", "es"), ("Supreme Electoral Tribunal of Bolivia", "en"), ("Tribunal Supremo Electoral de Bolivia", "es")],
    "SIN_gov": [("Servicio de Impuestos Nacionales de Bolivia", "es"), ("National Tax Service Bolivia", "en"), ("Servicio de Impuestos Nacionales", "en")],
    "ATT_gov": [("Autoridad de Regulación y Fiscalización de Telecomunicaciones y Transportes", "en"), ("ATT telecommunications Bolivia", "en")],
    "Emapa_soe": [("Emapa", "en"), ("Empresa de Apoyo a la Producción de Alimentos", "en")],
    "EMBOL_corp": [("EMBOL", "en"), ("Embol", "en")],
    "Soboce_corp": [("SOBOCE", "en"), ("Sociedad Boliviana de Cemento", "es")],
    "CEPB_ngo": [("Confederación de Empresarios Privados de Bolivia", "en"), ("Confederation of Private Entrepreneurs of Bolivia", "en")],
    "ERBOL_media": [("ERBOL", "en"), ("Red ERBOL", "es")],
    "CBN_extra": [("Cervecería Boliviana Nacional", "en")],
}


def curl_json(url: str):
    for attempt in range(3):
        cmd = [
            "curl", "--proxy", PROXY, "-s", "-L",
            "-H", "User-Agent: ApecOsintResearch/1.0 (contact: research@example.org)",
            url, "--max-time", "40",
        ]
        r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
        try:
            return json.loads(r.stdout)
        except json.JSONDecodeError:
            time.sleep(3.0 + attempt * 3.0)
    return None


def search(term: str, lang: str):
    url = ("https://www.wikidata.org/w/api.php?action=wbsearchentities&format=json"
           f"&language={lang}&uselang={lang}&limit=5&search=" + term.replace(" ", "%20"))
    return curl_json(url)


def main() -> None:
    results = {}
    for key, candidates in SEARCHES.items():
        found = None
        for term, lang in candidates:
            data = search(term, lang)
            time.sleep(2.0)
            if data and data.get("search"):
                for hit in data["search"]:
                    desc = (hit.get("description") or "").lower()
                    if "bolivia" in desc or "bolivian" in desc or key.endswith("_extra") or "andina" in desc:
                        found = {"qid": hit.get("id"), "label": hit.get("label"), "description": hit.get("description"), "query": term, "lang": lang}
                        break
                if not found and data["search"]:
                    hit = data["search"][0]
                    found = {"qid": hit.get("id"), "label": hit.get("label"), "description": hit.get("description"), "query": term, "lang": lang, "caveat": "no bolivia keyword in description"}
            if found:
                break
        results[key] = found
        print(key, "->", found, flush=True)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print("Saved.")


if __name__ == "__main__":
    main()
