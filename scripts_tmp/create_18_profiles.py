# -*- coding: utf-8 -*-
"""Create profiles for the 18 high-reference new identities."""
import glob, json, os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
from id_integrity_audit2 import BASE, OUT, load_datasets

# id: (name_zh, name_original, name_en, type, subtype, country, founded, website, qid,
#      aliases, industries, core, note)
D = {
"JP-FIN-050": ("三井住友银行","Sumitomo Mitsui Banking Corporation","Sumitomo Mitsui Banking Corporation","FIN","commercial_bank","JPN","2001-04-01","https://www.smbc.co.jp/","Q2660418",["SMBC","三井住友銀行"],["banking","financial_services"],"日本大型商业银行，三井住友金融集团核心子公司。","高引用补建"),
"JP-FIN-051": ("SMBC日兴证券","SMBC Nikko Securities Inc.","SMBC Nikko Securities Inc.","FIN","investment_bank","JPN",None,"https://www.smbcnikko.co.jp/","Q17227817",["SMBC Nikko","SMBC日興証券"],["financial_services","investment"],"日本大型证券公司，SMBC 集团旗下。","高引用补建"),
"JP-PARTY-010": ("中道改革联合","中道改革連合","Centrist Reform Alliance","PARTY","coalition","JPN",None,None,"Q137787102",["中道改革連合"],["public_administration"],"日本中道改革派政治联合/政党。","高引用补建；类别按 PARTY/coalition 处理"),
"JP-ACAD-031": ("量子科学技术研究开发机构","National Institutes for Quantum Science and Technology","National Institutes for Quantum Science and Technology","ACAD","research_institute","JPN","2016-04-01","https://www.qst.go.jp/",None,["QST","量子科学技術研究開発機構"],["research_development"],"日本量子科学技术研究开发机构，2016 年成立。","高引用补建"),
"JP-GOV-867": ("日本学术振兴会","Japan Society for the Promotion of Science","Japan Society for the Promotion of Science","GOV","independent_organ","JPN","1932-12-01","https://www.jsps.go.jp/","Q199781",["JSPS","日本学術振興会"],["research_development","public_administration"],"日本学术振兴会，资助科研与国际交流的独立行政法人。","高引用补建"),
"MX-GOV-878": ("联邦区立法议会","Asamblea Legislativa del Distrito Federal","Legislative Assembly of the Federal District","GOV","legislature","MEX",None,None,None,["ALDF"],["legislative"],"墨西哥联邦区（旧墨西哥城）立法议会，2018 年宪制改革后由墨西哥城议会取代。","高引用补建；历史机构"),
"MX-GOV-896": ("联邦区政府","Gobierno del Distrito Federal","Government of the Federal District","GOV","local_government","MEX",None,None,None,["GDF"],["public_administration"],"墨西哥联邦区（旧墨西哥城）政府，2018 年宪制改革后由墨西哥城政府取代。","高引用补建；历史机构"),
"MX-GOV-891": ("韦拉克鲁斯州政府","Gobierno del Estado de Veracruz","Government of the State of Veracruz","GOV","local_government","MEX",None,"https://www.veracruz.gob.mx/",None,["Veracruz"],["public_administration"],"墨西哥韦拉克鲁斯州政府。","高引用补建"),
"KR-FIN-016": ("新韩金融集团","Shinhan Financial Group","Shinhan Financial Group","FIN","holding_company","KOR","2001-09-01","https://www.shinhangroup.com/","Q491325",["Shinhan","신한금융지주"],["banking","financial_services"],"韩国大型金融控股公司，旗下包括新韩银行等。","高引用补建"),
"KR-MEDIA-021": ("中央日报","The JoongAng Ilbo","The JoongAng Ilbo","MEDIA","newspaper","KOR","1965-09-22","https://www.joongang.co.kr/","Q483903",["JoongAng Ilbo","중앙일보"],["media_publishing"],"韩国主要日报，中央日报集团旗下。","高引用补建"),
"KR-ACAD-024": ("高丽大学","Korea University","Korea University","ACAD","university","KOR","1905-05-05","https://www.korea.ac.kr/","Q39997",["Korea Univ","고려대학교"],["higher_education"],"韩国首尔私立综合大学。","高引用补建"),
"KR-ACAD-025": ("延世大学","Yonsei University","Yonsei University","ACAD","university","KOR","1885-04-10","https://www.yonsei.ac.kr/","Q39988",["Yonsei","연세대학교"],["higher_education"],"韩国首尔私立综合大学。","高引用补建"),
"KR-ACAD-026": ("韩国科学技术院","Korea Advanced Institute of Science and Technology","Korea Advanced Institute of Science and Technology","ACAD","university","KOR","1971-02-16","https://www.kaist.ac.kr/","Q39949",["KAIST","한국과학기술원"],["higher_education","research_development"],"韩国科学技术院（KAIST），大田的研究型大学。","高引用补建"),
"KR-SOE-021": ("韩国水力核电公司","Korea Hydro & Nuclear Power","Korea Hydro & Nuclear Power","SOE","state_owned_enterprise","KOR","2001-04-02","https://www.khnp.co.kr/","Q6431646",["KHNP","한국수력원자력"],["nuclear_energy","electricity_gas"],"韩国水力核电公司，负责核电与水电。","高引用补建"),
"KR-ACAD-027": ("浦项工科大学","Pohang University of Science and Technology","Pohang University of Science and Technology","ACAD","university","KOR","1986-12-03","https://www.postech.ac.kr/","Q40018",["POSTECH","포스텍"],["higher_education","research_development"],"韩国浦项私立研究型大学。","高引用补建"),
"NZ-GOV-152": ("新西兰商务委员会","Commerce Commission","Commerce Commission","GOV","regulatory_agency","NZL","1986-12-01","https://comcom.govt.nz/",None,["Commerce Commission NZ"],["regulatory"],"新西兰竞争、消费者与市场规制机构。","高引用补建"),
"NZ-GOV-134": ("新西兰广播资助局","NZ On Air","NZ On Air","GOV","independent_organ","NZL","1989-07-01","https://www.nzonair.govt.nz/","Q17056081",["NZ On Air","新西兰广播基金"],["media_publishing","public_administration"],"新西兰独立广播与内容资助机构。","高引用补建"),
"NZ-GOV-148": ("新西兰民航局","Civil Aviation Authority of New Zealand","Civil Aviation Authority of New Zealand","GOV","regulatory_agency","NZL","1992-07-01","https://www.caa.govt.nz/","Q5124421",["CAA NZ","Civil Aviation Authority"],["regulatory","transportation"],"新西兰民航监管机构。","高引用补建"),
}


def save_json(f, d):
    payload = json.dumps(d, ensure_ascii=False, indent=2) + "\n"
    tmp = f + ".tmp"; last = None
    for _ in range(6):
        try:
            with open(tmp, "w", encoding="utf-8", newline="\n") as fh: fh.write(payload)
            os.replace(tmp, f); return
        except PermissionError as e: last = e; time.sleep(0.5)
    for _ in range(3):
        try:
            with open(f, "w", encoding="utf-8", newline="\n") as fh: fh.write(payload)
            try: os.unlink(tmp)
            except OSError: pass
            return
        except PermissionError as e: last = e; time.sleep(1.0)
    raise last


def make(d):
    oid = d["id"]
    return {
        "org_id": oid,
        "basic_info": {
            "name_original": d["orig"], "name_zh": d["zh"], "name_en": d["en"],
            "aliases": d["aliases"], "org_type": d["type"], "org_subtype": d["sub"],
            "country_iso3": d["country"], "hq_country_iso3": d["country"],
            "founded_date": d["founded"], "website": d["website"], "wikidata_qid": d["qid"],
        },
        "social_accounts": [], "digital_assets": [], "key_people": [],
        "departments": [], "recent_events": [], "related_entities": [],
        "core_business": d["core"], "industries": d["inds"], "apec_stance": None,
        "profile": None,
        "collection_meta": {"collection_date": "2026-11-13", "phase": "phase3_enriched",
                            "data_sources": ["official_website"] + (["wikidata"] if d["qid"] else []),
                            "completeness_score": 55, "notes": d["note"], "quotes": []},
    }


def main():
    apply = "--apply" in sys.argv
    latest, _ = load_datasets()
    undo = []
    for oid, tup in D.items():
        zh, orig, en, typ, sub, country, founded, web, qid, aliases, inds, core, note = tup
        cc = oid[:2].lower()
        if cc not in latest:
            print("missing dataset", cc); continue
        folder = latest[cc][1]
        prof = make({"id": oid, "zh": zh, "orig": orig, "en": en, "type": typ, "sub": sub,
                     "country": country, "founded": founded, "website": web, "qid": qid,
                     "aliases": aliases, "inds": inds, "core": core, "note": note})
        fp = os.path.join(folder, "orgs", oid + ".json")
        if os.path.exists(fp):
            print("exists, skip", oid); continue
        regp = os.path.join(folder, "id_registry.json")
        idxp = os.path.join(folder, "orgs", "_index.json")
        reg = json.load(open(regp, encoding="utf-8"))
        e = next((x for x in reg.get("registry") or [] if x.get("org_id") == oid), None)
        if e is None:
            print("registry entry missing", oid); continue
        old = dict(e)
        e["status"] = "profiled"
        if qid: e["wikidata_qid"] = qid
        idx = None
        if os.path.exists(idxp):
            idx = json.load(open(idxp, encoding="utf-8"))
            if not any(x.get("org_id") == oid for x in idx.get("profiles") or []):
                idx["profiles"].append({"org_id": oid, "name": f"{zh} ({orig})",
                                        "category": typ, "subcategory": sub, "completeness": 55})
            idx["profiles"].sort(key=lambda x: x.get("org_id", ""))
            idx["total_profiles"] = len(idx["profiles"])
        if apply:
            save_json(fp, prof); save_json(regp, reg)
            if idx is not None: save_json(idxp, idx)
        undo.append({"id": oid, "file": fp, "registry_old": old})
        print("prepared", oid)
    print(json.dumps({"count": len(undo)}, ensure_ascii=False))
    if apply:
        json.dump(undo, open(os.path.join(OUT, "newid_18_profiles_undo.json"), "w", encoding="utf-8"),
                  ensure_ascii=False, indent=1)
        print("undo ->", os.path.join(OUT, "newid_18_profiles_undo.json"))
    else:
        print("DRY")


if __name__ == "__main__":
    main()
