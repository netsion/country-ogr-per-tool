# A2 batch helper: find image candidates via Wikidata P18 and Commons file search
import json, sys, urllib.request, urllib.parse

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
PROXY = {"http": "http://127.0.0.1:7897", "https": "http://127.0.0.1:7897"}
OP = urllib.request.build_opener(urllib.request.ProxyHandler(PROXY))
OP.addheaders = [("User-Agent", UA)]

def api(host, params):
    url = "https://%s/w/api.php?%s" % (host, urllib.parse.urlencode(params))
    return json.load(OP.open(url, timeout=60))

def wikidata_p18(search_names):
    """Search wikidata entities by name, return (qid, label, p18_filename) list."""
    out = []
    for nm in search_names:
        try:
            d = api("www.wikidata.org", {
                "action": "wbsearchentities", "search": nm, "language": "en",
                "limit": 5, "format": "json"})
        except Exception as e:
            print("  search err", nm, e)
            continue
        for r in d.get("search", []):
            qid = r.get("id")
            if not qid or not qid.startswith("Q"):
                continue
            desc = (r.get("description") or "").lower()
            try:
                de = api("www.wikidata.org", {
                    "action": "wbgetentities", "ids": qid,
                    "props": "claims|labels", "languages": "en", "format": "json"})
                ent = de.get("entities", {}).get(qid, {})
                label = (ent.get("labels", {}).get("en", {}) or {}).get("value", "")
                claims = ent.get("claims", {})
                p18 = claims.get("P18", [])
                fn = None
                if p18:
                    mv = p18[0].get("mainsnak", {}).get("datavalue", {}).get("value", {})
                    fn = mv.get("filename") if isinstance(mv, dict) else mv
                out.append((nm, qid, label, desc, fn))
            except Exception as e:
                print("  entity err", qid, e)
    return out

def commons_search(query, limit=10):
    try:
        d = api("commons.wikimedia.org", {
            "action": "query", "format": "json", "generator": "search",
            "gsrsearch": query, "gsrnamespace": 6, "gsrlimit": limit,
            "prop": "imageinfo", "iiprop": "url|mime|size"})
        pages = d.get("query", {}).get("pages", {})
        res = []
        for p in pages.values():
            ii = (p.get("imageinfo") or [{}])[0]
            res.append({
                "title": p.get("title"),
                "url": ii.get("url"),
                "mime": ii.get("mime"),
                "w": ii.get("width"), "h": ii.get("height"),
                "index": p.get("index"),
            })
        res.sort(key=lambda x: x.get("index") or 99)
        return res
    except Exception as e:
        print("  commons err", query, e)
        return []

def commons_fileinfo(filenames):
    """Given Commons filenames (without File:), return original upload.wikimedia.org URLs."""
    out = {}
    if not filenames:
        return out
    try:
        d = api("commons.wikimedia.org", {
            "action": "query", "format": "json", "prop": "imageinfo",
            "iiprop": "url|mime|size", "titles": "|".join("File:" + f for f in filenames)})
        for p in d.get("query", {}).get("pages", {}).values():
            ii = (p.get("imageinfo") or [{}])[0]
            if ii.get("url"):
                out[p.get("title")] = ii
    except Exception as e:
        print("  fileinfo err", e)
    return out

if __name__ == "__main__":
    # persons with candidate search names
    persons = json.load(open(sys.argv[1], encoding="utf-8"))
    mode = sys.argv[2] if len(sys.argv) > 2 else "wikidata"
    for pid, names in persons.items():
        print("=" * 70)
        print(pid, names)
        if mode == "wikidata":
            for nm, qid, label, desc, fn in wikidata_p18(names):
                print("  WD:", qid, "|", label, "|", desc, "| P18:", fn)
        elif mode == "commons":
            for nm in names:
                print(" -- query:", nm)
                for r in commons_search(nm):
                    print("   CS:", r["title"], "|", r["mime"], "| %sx%s" % (r["w"], r["h"]), "|", r["url"])
