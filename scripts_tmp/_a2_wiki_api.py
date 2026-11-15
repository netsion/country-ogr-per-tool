# A2 batch helper: query en.wikipedia pageimages -> imageinfo URLs
import json, sys, urllib.request, urllib.parse

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
PROXY = {"http": "http://127.0.0.1:7897", "https": "http://127.0.0.1:7897"}

def opener():
    op = urllib.request.build_opener(urllib.request.ProxyHandler(PROXY))
    op.addheaders = [("User-Agent", UA)]
    return op

OP = opener()

def api(host, params):
    url = "https://%s/w/api.php?%s" % (host, urllib.parse.urlencode(params))
    return json.load(OP.open(url, timeout=60))

def get_pageimage_urls(titles):
    """Return {article_title: {filename, url, mime, size}}"""
    out = {}
    data = api("en.wikipedia.org", {
        "action": "query", "format": "json", "prop": "pageimages",
        "piprop": "filename", "redirects": 1, "titles": "|".join(titles)})
    files = {}
    for r in data.get("query", {}).get("pages", {}).values():
        fn = r.get("pageimage")
        if fn:
            files[r["title"]] = fn
    if files:
        ftitles = "|".join("File:" + v for v in files.values())
        d2 = api("en.wikipedia.org", {
            "action": "query", "format": "json", "prop": "imageinfo",
            "iiprop": "url|mime|size", "titles": ftitles})
        url_by_fn = {}
        for r in d2.get("query", {}).get("pages", {}).values():
            ii = r.get("imageinfo")
            if ii:
                fn = r["title"].split("File:", 1)[-1]
                url_by_fn[fn] = (ii[0].get("url"), ii[0].get("mime"), ii[0].get("width"), ii[0].get("height"))
        for art, fn in files.items():
            u = url_by_fn.get(fn)
            out[art] = {"filename": fn, "url": u[0] if u else None,
                        "mime": u[1] if u else None,
                        "size": (u[2], u[3]) if u else None}
    return out

if __name__ == "__main__":
    articles = {
        "000317": "David Bird",
        "000321": "Karl Toriola",
        "000380": "Adamu Ahmed",
        "000445": "Innocent Chukwuma",
        "000459": "Segun Agbaje",
        "000460": "Miriam Olusanya",
        "000474": "Oliver Alawuba",
        "000488": "Hadja Memounatou Ibrahima",
        "000498": "Alex Ibru",
        "000524": "Nenadi Usman",
        "000584": "Subomi Balogun",
    }
    res = get_pageimage_urls(list(articles.values()))
    for art, info in res.items():
        print(art, "|", art_title := [k for k, v in articles.items() if v == art],
              "|", info["filename"], "|", info["url"], "|", info["mime"], "|", info["size"])
