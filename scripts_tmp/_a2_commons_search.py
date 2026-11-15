# A2 helper: Commons file search with rate-limit backoff
import json, re, sys, time, urllib.request, urllib.parse

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
PROXY = {"http": "http://127.0.0.1:7897", "https": "http://127.0.0.1:7897"}
OP = urllib.request.build_opener(urllib.request.ProxyHandler(PROXY))
OP.addheaders = [("User-Agent", UA)]

def api(host, params, tries=5):
    url = "https://%s/w/api.php?%s" % (host, urllib.parse.urlencode(params))
    for i in range(tries):
        try:
            return json.load(OP.open(url, timeout=60))
        except urllib.error.HTTPError as e:
            if e.code == 429:
                wait = 30 * (i + 1)
                print("   429, sleep", wait)
                time.sleep(wait)
            else:
                print("   err", e.code, "sleep", 10 * (i + 1))
                time.sleep(10 * (i + 1))
        except Exception as e:
            print("   err", e, "sleep", 10 * (i + 1))
            time.sleep(10 * (i + 1))
    return None

SKIP = re.compile(r"(Lock-|logo|icon|Wiki|flag|Edit-|Ambox|Symbol|question|Disambig|Blank|Placeholder|No_image|Silhouette|Default|BSicon|insignia|OL[A-Z]|svg$|ogv$|webm$|pdf$|tiff?$|gif$)", re.I)

def commons_files(query, limit=12):
    d = api("commons.wikimedia.org", {
        "action": "query", "format": "json", "generator": "search",
        "gsrsearch": query, "gsrnamespace": 6, "gsrlimit": limit,
        "prop": "imageinfo", "iiprop": "url|mime|size"})
    if not d:
        return []
    pages = d.get("query", {}).get("pages", {})
    res = []
    for p in pages.values():
        ii = (p.get("imageinfo") or [{}])[0]
        title = p.get("title", "")
        fn = title.replace("File:", "")
        if SKIP.search(fn):
            continue
        res.append({
            "title": title, "url": ii.get("url"), "mime": ii.get("mime"),
            "w": ii.get("width"), "h": ii.get("height"), "idx": p.get("index")})
    res.sort(key=lambda x: x.get("idx") or 99)
    return res

if __name__ == "__main__":
    persons = json.load(open(sys.argv[1], encoding="utf-8"))
    out = {}
    for pid, queries in persons.items():
        print("=" * 60)
        print(pid, queries)
        found = []
        for q in queries:
            for r in commons_files(q):
                print("   CS:", r["title"], "|", r["mime"], "| %sx%s" % (r["w"], r["h"]), "|", r["url"])
                found.append(r)
            time.sleep(6)
        out[pid] = found
    json.dump(out, open(sys.argv[2], "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("saved ->", sys.argv[2])
