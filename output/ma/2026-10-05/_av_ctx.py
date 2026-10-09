import sys,re,urllib.request
url=sys.argv[1]; kw=sys.argv[2:]
proxy=urllib.request.ProxyHandler({'http':'http://127.0.0.1:7890','https':'http://127.0.0.1:7890'})
op=urllib.request.build_opener(proxy)
op.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36'),('Accept-Language','fr,ar;q=0.8,en;q=0.5')]
html=op.open(url,timeout=40).read().decode('utf-8','replace')
for k in kw:
    for m in re.finditer(k,html,re.I):
        s=max(0,m.start()-400); seg=html[s:m.end()+400]
        seg=re.sub(r'\s+',' ',seg)
        print('---',k,':',seg[:700]); break
    else: print('---',k,': NOT FOUND')
