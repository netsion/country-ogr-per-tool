import sys,re,urllib.request,urllib.parse
url=sys.argv[1]
proxy=urllib.request.ProxyHandler({'http':'http://127.0.0.1:7890','https':'http://127.0.0.1:7890'})
op=urllib.request.build_opener(proxy)
op.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36'),('Accept-Language','fr,ar;q=0.8,en;q=0.5')]
html=op.open(url,timeout=40).read().decode('utf-8','replace')
seen=set()
for m in re.finditer(r'href=["\']([^"\']+)["\'][^>]*>(.*?)</a>',html,re.I|re.S):
    u=urllib.parse.urljoin(url,m.group(1)); t=re.sub(r'\s+',' ',re.sub(r'<[^>]+>',' ',m.group(2))).strip()
    if u in seen: continue
    seen.add(u)
    print(u,'|',t[:80])
