# -*- coding: utf-8 -*-
"""Find QIDs via Wikidata wbsearchentities for remaining orgs, then pull entity labels/descriptions."""
import json
import os
import subprocess
import time

PROXY = "http://127.0.0.1:7890"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "wd_search_results.json")

SEARCHES = {
    "TSE_gov": ["Tribunal Supremo Electoral Bolivia", "Tribunal Supremo Electoral"],
    "SIN_gov": ["Servicio de Impuestos Nacionales"],
    "ATT_gov": ["Autoridad de Regulación y Fiscalización de Telecomunicaciones y Transportes", "ATT Bolivia"],
    "Emapa_soe": ["Empresa de Apoyo a la Producción de Alimentos", "Emapa Bolivia"],
    "EMBOL_corp": ["Embol Bolivia"],
    "Farmacorp_corp": ["Farmacorp"],
    "Soboce_corp": ["Soboce", "SOBOCE"],
    "CEPB_ngo": ["Confederación de Empresarios Privados de Bolivia"],
    "CIPCA_ngo": ["CIPCA", "Centro de investigación y promoción del campesinado"],
    "Tierra_ngo": ["Fundación Tierra", "Fundación TIERRA"],
    "LosTiempos_media": ["Los Tiempos Bolivia", "Los Tiempos"],
    "BoA_soe_extra": ["Boliviana de Aviación"],
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


def main() -> None:
    results = {}
    for key, candidates in SEARCHES.items():
        found = None
        for q in candidates:
            url = ("https://www.wikidata.org/w/api.php?action=wbsearchentities&format=json&language=es&uselang=es&limit=5&search="
                   + q.replace(" ", "%20"))
            data = curl_json(url)
            time.sleep(2.0)
            if data and data.get("search"):
                for hit in data["search"]:
                    found = {"qid": hit.get("id"), "label": hit.get("label"), "description": hit.get("description"), "query": q}
                    break
            if found:
                break
        results[key] = found
        print(key, "->", found, flush=True)
    # pull descriptions via entitydata for found qids
    for key, found in results.items():
        if not found or not found.get("qid"):
            continue
        qid = found["qid"]
        data = curl_json(f"https://www.wikidata.org/wiki/Special/EntityData/{qid}.json")
        time.sleep(2.0)
        if data and "entities" in data and qid in data["entities"]:
            ent = data["entities"][qid]
            found["desc_en"] = ent.get("descriptions", {}).get("en", {}).get("value")
            found["desc_es"] = ent.get("descriptions", {}).get("es", {}).get("value")
            labels = ent.get("labels", {})
            found["label_es"] = labels.get("es", {}).get("value")
            found["label_en"] = labels.get("en", {}).get("value")
            claims = ent.get("claims", {})
            def first_val(prop):
                c = claims.get(prop)
                if not c:
                    return None
                try:
                    return c[0]["mainsnak"]["datavalue"]["value"]
                except (KeyError, IndexError, TypeError):
                    return None
            def first_str(prop):
                c = claims.get(prop)
                if not c:
                    return None
                try:
                    dv = c[0]["mainsnak"]["datavalue"]["value"]
                    if isinstance(dv, dict):
                        return dv.get("id") or dv.get("time") or dv.get("text")
                    return dv
                except (KeyError, IndexError, TypeError):
                    return None
            found["website"] = first_val("P856")
            found["inception"] = first_str("P571")
            found["hq_qid"] = first_str("P159")
            found["p31"] = first_str("P31")
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print("Saved.")


if __name__ == "__main__":
    main()
