import sys,re,urllib.request,urllib.parse
url=sys.argv[1]
proxy=urllib.request.ProxyHandler({'http':'http://127.0.0.1:7890','https':'http://127.0.0.1:7890'})
op=urllib.request.build_opener(proxy)
op.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36'),('Accept-Language','fr,ar;q=0.8,en;q=0.5')]
try:
    html=op.open(url,timeout=40).read().decode('utf-8','replace')
except Exception as e:
    print('ERR',e); sys.exit(1)
base=urllib.parse.urlparse(url)
for m in re.finditer(r'<img[^>]+>',html,re.I):
    tag=m.group(0)
    src=re.search(r'src=["\']([^"\']+)["\']',tag,re.I)
    alt=re.search(r'alt=["\']([^"\']*)["\']',tag,re.I)
    if not src: continue
    u=urllib.parse.urljoin(url,src.group(1))
    # context: text around
    s=max(0,m.start()-120); ctx=re.sub(r'\s+',' ',re.sub(r'<[^>]+>',' ',html[s:m.end()+150]))
    print(u,'| alt:',(alt.group(1) if alt else ''),'| ctx:',ctx[:160])
