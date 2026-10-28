# -*- coding: utf-8 -*-
"""Verify top Bolivia orgs via Wikipedia REST API summary (es, fallback en).
Stores title, description, extract, wikibase_item for each."""
import json
import os
import subprocess
import time

PROXY = "http://127.0.0.1:7890"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "verify_results.json")
DELAY = 3.5

# (key, category, [es_title, en_title, ...fallbacks])
PAGES = [
    ("ALP_gov", "GOV", ["Asamblea Legislativa Plurinacional"]),
    ("TSE_gov", "GOV", ["Tribunal Supremo Electoral (Bolivia)"]),
    ("Contraloria_gov", "GOV", ["Contraloría General del Estado (Bolivia)", "Contraloría General del Estado"]),
    ("INE_gov", "GOV", ["Instituto Nacional de Estadística (Bolivia)"]),
    ("Presidente_gov", "GOV", ["Presidente de Bolivia"]),
    ("Defensoria_gov", "GOV", ["Defensoría del Pueblo de Bolivia"]),
    ("SIN_gov", "GOV", ["Servicio de Impuestos Nacionales"]),
    ("ATT_gov", "GOV", ["Autoridad de Regulación y Fiscalización de Telecomunicaciones y Transportes"]),
    ("YPFB_soe", "SOE", ["Yacimientos Petrolíferos Fiscales Bolivianos", "YPFB"]),
    ("ENDE_soe", "SOE", ["Empresa Nacional de Electricidad (Bolivia)"]),
    ("BoA_soe", "SOE", ["Boliviana de Aviación", "Boliviana de Aviación S.A."]),
    ("MiTelesferico_soe", "SOE", ["Mi Teleférico"]),
    ("Emapa_soe", "SOE", ["Empresa de Apoyo a la Producción de Alimentos", "Emapa"]),
    ("Entel_soe", "SOE", ["Entel (Bolivia)", "Entel Bolivia"]),
    ("CBN_corp", "CORP", ["Cervecería Boliviana Nacional"]),
    ("EMBOL_corp", "CORP", ["Embol"]),
    ("Farmacorp_corp", "CORP", ["Farmacorp"]),
    ("Hipermaxi_corp", "CORP", ["Hipermaxi"]),
    ("Soboce_corp", "CORP", ["Soboce", "SOBOCE"]),
    ("MSC_corp", "CORP", ["Minera San Cristóbal"]),
    ("COB_ngo", "NGO", ["Central Obrera Boliviana"]),
    ("CEPB_ngo", "NGO", ["Confederación de Empresarios Privados de Bolivia"]),
    ("CIPCA_ngo", "NGO", ["Centro de investigación y promoción del campesinado"]),
    ("Tierra_ngo", "NGO", ["Fundación Tierra"]),
    ("ElDeber_media", "MEDIA", ["El Deber"]),
    ("LosTiempos_media", "MEDIA", ["Los Tiempos"]),
    ("LaRazon_media", "MEDIA", ["La Razón (Bolivia)", "La Razón"]),
    ("Unitel_media", "MEDIA", ["Unitel (Bolivia)", "Unitel"]),
    ("Bolivision_media", "MEDIA", ["Bolivisión"]),
    ("RedUno_media", "MEDIA", ["Red Uno"]),
    ("ATB_media", "MEDIA", ["Red ATB", "ATB (Bolivia)"]),
    ("BoliviaTV_media", "MEDIA", ["Bolivia TV"]),
    ("ERBOL_media", "MEDIA", ["ERBOL"]),
    ("ABI_media", "MEDIA", ["Agencia Boliviana de Información"]),
    ("BCB_fin", "FIN", ["Banco Central de Bolivia"]),
    ("ASFI_fin", "FIN", ["Autoridad de Supervisión del Sistema Financiero", "ASFI (Bolivia)"]),
    ("BCP_fin", "FIN", ["Banco de Crédito de Bolivia", "Banco de Crédito de Bolivia (Bolivia)"]),
    ("Unidad_party", "PARTY", ["Unidad (Bolivia)", "Alianza Unidad"]),
    ("PDC_party", "PARTY", ["Partido Demócrata Cristiano (Bolivia)"]),
    ("Libre_party", "PARTY", ["Libre (Bolivia)", "Frente para la Victoria (Bolivia)"]),
    ("CAN_intl", "INTL", ["Comunidad Andina"]),
    ("ALADI_intl", "INTL", ["Asociación Latinoamericana de Integración"]),
    ("CAF_intl", "INTL", ["Corporación Andina de Fomento", "CAF (banco de desarrollo)"]),
]


def fetch(lang: str, title: str):
    url = f"https://{lang}.wikipedia.org/api/rest_v1/page/summary/{title.replace(' ', '_')}"
    for attempt in range(3):
        cmd = [
            "curl", "--proxy", PROXY, "-s", "-L",
            "-H", "User-Agent: ApecOsintResearch/1.0 (contact: research@example.org)",
            "-w", "\n%{http_code}", url, "--max-time", "40",
        ]
        r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
        out = r.stdout
        if "\n" in out:
            body, _, code = out.rpartition("\n")
            if code.strip() == "200":
                try:
                    return json.loads(body)
                except json.JSONDecodeError:
                    pass
        time.sleep(2.0 + attempt * 2.0)
    return None


def main() -> None:
    results = {}
    if os.path.exists(OUT):
        with open(OUT, "r", encoding="utf-8") as f:
            results = json.load(f)
    for key, cat, titles in PAGES:
        if key in results and results[key].get("wikibase_item"):
            continue
        got = None
        used = ""
        for t in titles:
            for lang in ("es", "en"):
                got = fetch(lang, t)
                if got and got.get("type") != "https://mediawiki.org/wiki/HyperSwitch/errors/not_found":
                    used = f"{lang}:{t}"
                    break
                got = None
                time.sleep(1.0)
            if got:
                break
            time.sleep(1.0)
        if got:
            results[key] = {
                "category": cat,
                "source_page": used,
                "title": got.get("title"),
                "description": got.get("description"),
                "extract": (got.get("extract") or "")[:600],
                "wikibase_item": got.get("wikibase_item"),
            }
            print(f"[OK] {key} -> {got.get('wikibase_item')} | {got.get('title')} | {(got.get('description') or '')[:60]}")
        else:
            results[key] = {"category": cat, "source_page": None, "title": None, "description": None, "extract": None, "wikibase_item": None}
            print(f"[MISS] {key} ({titles})", flush=True)
        time.sleep(DELAY)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print("Saved.")


if __name__ == "__main__":
    main()
