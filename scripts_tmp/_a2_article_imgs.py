# A2 helper: fetch en.wikipedia article HTML, extract infobox image
import json, re, sys, time, urllib.request, urllib.parse

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
PROXY = {"http": "http://127.0.0.1:7897", "https": "http://127.0.0.1:7897"}
OP = urllib.request.build_opener(urllib.request.ProxyHandler(PROXY))
OP.addheaders = [("User-Agent", UA)]

def fetch(url, tries=3):
    for i in range(tries):
        try:
            return OP.open(url, timeout=60).read().decode("utf-8", "replace")
        except Exception as e:
            code = getattr(e, "code", None)
            print("   fetch err", code or e, "retry", i)
            time.sleep(15 * (i + 1))
    return None

SKIP = re.compile(r"(Lock-|logo|icon|Wiki|flag|Edit-|Ambox|Symbol|question|Disambig|Blank|Placeholder|Portrait_placeholder|No_image|Male_Portrait|Female_Portrait|Image_placeholder|Ghost|Silhouette|Default|UserAnon|Commons-|Wikidata|Wikisource|Wikiquote|Translation|arrow|incre|decre|P_vip|Crystal|BSicon|Rank|Army|Navy|Air_Force|insignia|OL.*svg|Flag_of)", re.I)

def article_images(title):
    url = "https://en.wikipedia.org/wiki/" + urllib.parse.quote(title.replace(" ", "_"))
    html = fetch(url)
    if not html:
        return []
    # grab infobox section
    m = re.search(r'class="infobox(.*?)(?:<table|</table>)', html, re.S)
    box = m.group(1) if m else html
    imgs = re.findall(r'(?:src|srcset)="(//upload\.wikimedia\.org/wikipedia/[^"\s|]+)"', box)
    seen, out = set(), []
    for u in imgs:
        u = "https:" + u if u.startswith("//") else u
        u = re.sub(r"\d+px-", "", u.split("|")[0])
        u = u.replace("/commons/thumb/", "/commons/").rsplit("/", 2)[0] + "/" + u.rsplit("/", 1)[-1] if "/thumb/" in u else u
        if u in seen:
            continue
        seen.add(u)
        fn = u.rsplit("/", 1)[-1]
        if SKIP.search(fn):
            continue
        out.append(u)
    return out

if __name__ == "__main__":
    arts = json.load(open(sys.argv[1], encoding="utf-8"))
    for pid, titles in arts.items():
        print("=" * 60)
        for t in titles:
            print(pid, "|", t)
            for u in article_images(t)[:4]:
                print("   IMG:", u)
            time.sleep(2)
