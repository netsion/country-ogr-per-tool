import re, html, glob, os

d = r"D:/claude-workspace/apec-osint-tool/output/bo/2026-10-24/_tmp330"
for p in sorted(glob.glob(os.path.join(d, "bw_*.xml"))):
    with open(p, encoding="utf-8", errors="ignore") as f:
        s = f.read()
    items = re.findall(r"<item>(.*?)</item>", s, re.S)
    print("==", os.path.basename(p), "items:", len(items))
    for it in items[:8]:
        t = re.search(r"<title>(.*?)</title>", it, re.S)
        l = re.search(r"<link>(.*?)</link>", it, re.S)
        de = re.search(r"<description>(.*?)</description>", it, re.S)
        print(" -", html.unescape(t.group(1))[:130] if t else "")
        print("   ", html.unescape(l.group(1))[:170] if l else "")
        if de:
            print("   D>", html.unescape(re.sub(r"<[^>]+>", "", de.group(1)))[:220])
