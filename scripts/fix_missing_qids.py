#!/usr/bin/env python3
"""
fix_missing_qids.py — Search Wikidata for persons missing QIDs and update registry
"""
import sys; sys.stdout.reconfigure(encoding='utf-8'); sys.stderr.reconfigure(encoding='utf-8')
import json
import os
import time
import urllib.request
import ssl

PROXY_HOST = "127.0.0.1"
PROXY_PORT = 1080

def setup_proxy():
    proxy_url = f"http://{PROXY_HOST}:{PROXY_PORT}"
    proxy_handler = urllib.request.ProxyHandler({'http': proxy_url, 'https': proxy_url})
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    opener = urllib.request.build_opener(proxy_handler, urllib.request.HTTPSHandler(context=ctx))
    urllib.request.install_opener(opener)

def search_wikidata(name_en):
    url = f"https://www.wikidata.org/w/api.php?action=wbsearchentities&search={urllib.parse.quote(name_en)}&language=en&format=json&limit=5"
    req = urllib.request.Request(url, headers={"User-Agent": "ApecOsintTool/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read())
        results = data.get("search", [])
        for r in results:
            desc = r.get("description", "").lower()
            if any(kw in desc for kw in ["singapore", "politician", "minister", "executive", "business", "banker", "ceo", "chief"]):
                return r["id"], r.get("label", ""), r.get("description", "")
        if results:
            return results[0]["id"], results[0].get("label", ""), results[0].get("description", "")
    except Exception as e:
        print(f"    ERROR: {e}")
    return None, None, None

import urllib.parse

def main():
    base_dir = r"D:\claude-workspace\apec-osint-tool\output\sg\2026-04-15"
    registry_file = os.path.join(base_dir, "id_registry.json")

    setup_proxy()

    with open(registry_file, encoding="utf-8") as f:
        reg = json.load(f)

    missing = [p for p in reg["person_registry"] if not p.get("wikidata_qid") and p.get("status") in ("listed", "profiled")]
    print(f"Persons missing QID: {len(missing)}")

    for p in missing:
        pid = p["person_id"]
        name = p["name"]
        # Extract English name from parenthetical
        name_en = name
        if "(" in name and ")" in name:
            name_en = name.split("(")[-1].rstrip(")")
        elif not any('\u4e00' <= c <= '\u9fff' for c in name):
            name_en = name

        print(f"  Searching: {name_en} ...", end=" ")
        qid, label, desc = search_wikidata(name_en)
        if qid:
            p["wikidata_qid"] = qid
            print(f"-> {qid} ({label}: {desc[:50]})")
        else:
            print("NOT FOUND")
        time.sleep(2)

    with open(registry_file, "w", encoding="utf-8") as f:
        json.dump(reg, f, ensure_ascii=False, indent=2)
    print(f"\nSaved registry with updated QIDs")


if __name__ == "__main__":
    main()
