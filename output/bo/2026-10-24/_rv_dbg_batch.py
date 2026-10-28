import re, json, urllib.request, urllib.parse
PROXY = 'http://127.0.0.1:7890'
opener = urllib.request.build_opener(urllib.request.ProxyHandler({'http': PROXY, 'https': PROXY}))
opener.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/126.0 Safari/537.36'), ('Content-Type', 'application/x-www-form-urlencoded;charset=UTF-8')]
gid = 'CBMiugFBVV95cUxPdmxYMTJqX0lSYkdlT2tTU1E5dnhOMU5WSmpHUEhycm5iTzdhX0ZrUDhvZXc2dFlva2M3dXh4VFlvcV9yZndkX0ViZTYxTmNySVJJaWx6MnUzLW4zb3NLUXUzWEs2MGlPT1pSX2pwM2dubWZhanlFa0g2SUtpc0huaS1BMlFLMDU3NmI5UkJXYlo5NnpRNjFwOEE5TU5VZTlKT0NHNVdLakR1dGtfRTZkZS13SVBBNFNDRHc'
inner = json.dumps(["garturlreq",[["X","X",["X","X"],null,null,1,1,1,1,null,null,1,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,[]]] , gid, null]) if False else '["garturlreq",[["X","X",["X","X"],null,null,1,1,1,1,null,null,1,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,[]]],"' + gid + '"]'
payload = '[[["Fbv4je","' + inner.replace('"','\\"') + '",null,"generic"]]]'
data = urllib.parse.urlencode({'f.req': payload}).encode()
req = urllib.request.Request('https://news.google.com/_/DotsSplashUi/data/batchexecute', data=data)
body = opener.open(req, timeout=30).read().decode('utf-8', 'ignore')
print('LEN', len(body))
print(body[:1200])
