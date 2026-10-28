import re, time, urllib.request, urllib.parse

PROXY = 'http://127.0.0.1:7890'
opener = urllib.request.build_opener(urllib.request.ProxyHandler({'http': PROXY, 'https': PROXY}))
opener.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/126.0 Safari/537.36')]

def resolve(gnews_url):
    m = re.search(r'/articles/([^?]+)', gnews_url)
    gid = m.group(1)
    inner = '["garturlreq",[["es-419","BO",["FINANCE_TOP_INDICES","FINANCE_TOP_INDICES_WEB","TEST_79"],null,null,1,1,1,1,null,null,1,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,["es-419"]]]' + ',"' + gid + '"]'
    payload = '[[["Fbv4je",' + json_str(inner) + ',null,"generic"]]]'
    data = urllib.parse.urlencode({'f.req': payload}).encode()
    req = urllib.request.Request('https://news.google.com/_/DotsSplashUi/data/batchexecute', data=data)
    body = opener.open(req, timeout=30).read().decode('utf-8', 'ignore')
    i = body.find('garturlres')
    if i == -1:
        return None
    j = body.find('https', i)
    k = body.find('"', j)
    url = body[j:k]
    return url.replace('\x22','').strip()

def json_str(s):
    return '"' + s.replace('"', '\\"') + '"'

links = {
 'sello_propio': 'https://news.google.com/rss/articles/CBMiugFBVV95cUxPdmxYMTJqX0lSYkdlT2tTU1E5dnhOMU5WSmpHUEhycm5iTzdhX0ZrUDhvZXc2dFlva2M3dXh4VFlvcV9yZndkX0ViZTYxTmNySVJJaWx6MnUzLW4zb3NLUXUzWEs2MGlPT1pSX2pwM2dubWZhanlFa0g2SUtpc0huaS1BMlFLMDU3NmI5UkJXYlo5NnpRNjFwOEE5TU5VZTlKT0NHNVdLakR1dGtfRTZkZS13SVBBNFNDRHc?oc=5',
 'deficit240': 'https://news.google.com/rss/articles/CBMiygFBVV95cUxPWHRYWmRZWXlYTlhJb1pyTWpjaEYwdVRjdm9kVWdMdUQ2eVVPcGR1ckpDQ0dwOGwxQkhneTQ0Rkc0cUVwYnRtWmR5SzY2blVpR0N0Y2l2S3d0YTZKYmRQdnpMcTA1RTRlUTdhOUpxWGJZU2t6Z01idTNVYlhvZTIyLTRTZEMtanVoeEhuaTNHV1ZSaEJHTERNbFRaRTNPUEkzcEN6aGZaRlpjQlVuYllXd3ByX1EzdXdFanpxWXg1UFgxTC1adzBGc2NB?oc=5',
 'pragmatico': 'https://news.google.com/rss/articles/CBMi2gFBVV95cUxNWmZWWlIzaERmZDlWb25HN1F4aHJJaDVNSnVuWVByN3BScmFHdkJzTlFaNVF3aTBmUzU0UHhFa1VxWnNuQTRfeDNHVmwyVFk3TVVtWERSdWlVNzFCUV9jdk9lVjd0Z2RWNlJmVG0zMFprNWd2TFZ5MGNqakViY0UxOThmaTJjZ1ZieUQ0OVBRUzMzcGNlRkFqNGdQV2htQ1JpMTJfZjBlVnVxcGpoeVRIS3ZwaDhSRmxlZUNNLTZPWGFuTFhOOXRqcy0tZjhTSjZ3SG93SDJnQmJodw?oc=5',
 'anf_fiscalia': 'https://news.google.com/rss/articles/CBMi5AFBVV95cUxQckJST1lVeXRaSkJkU3RvdU5QV09XZGZjcG1nRFI1V0laS1VBR0V3SHROaS10TXlrQVB3X1AwUFZJSnktNVB6NFp5V3FOdXNrUnBLV3c5ZUUyaE9GRGMxQnVBb3doWHE3eTEwengzUVhUczVUTTVmdXc4Q0pmVnVsbXh4VHdiazNRYm1DUFJzUW5Ra2JxZkF4aS1Td3F2RmFINFN2V3dpeEVnRzVadWZrcTd3LWhwZWs1dU96cXM3Sk1uWXVSSGVSektDemNHUTN3M3VEalU1M2dwRXFLYlE1TTRjbjU?oc=5',
 'democracia': 'https://news.google.com/rss/articles/CBMiqgFBVV95cUxPS19uNTktUTF5MGowUU1qV0FVN1JNNVg1Rzk3Vnp3NGttTEQxT0pNb2d3aWwtbHdrX2xCVVpvV0dxOTRWRERZclYwRGVFOFdWbkkySUdNQk16eHU1Y3RxQzJLR1YycUdHNFhwZGZza0NnazZGdnVtNURZMlVBV2NyWmFQMjU4aFgwbHNRUEJoVEYwenhvVWF5V2N0aVNDSDctWUQwekE3MDNxdw?oc=5',
 'energetica': 'https://news.google.com/rss/articles/CBMizAFBVV95cUxPLVRTMk5EbmwyQ29EcGpxTnpzVGgydVgwSVRkV3JjVkJURVFPbnROYlZNM1hoUS1jSHROT0VQcV9jd29fZDR5b1ZIanB4NVlQbVFoa1ZHMW1GWVRvUWc1Z1pTN3pCSUFwLTNxLThqbTlTU1IwZ0lGbDVfcTJPNUZwcEloZ01zdmJHTTh4N1lUN1M4SnpZNDU4UGZ2cEhvSmphQTBhSXhJVERaU25OM3lYWnc1SUJockN5Z2djcG9KZTlxUVNEamJGbVFzNHE?oc=5',
 'callar': 'https://news.google.com/rss/articles/CBMi0AFBVV95cUxPTXlHMEJFTnFWSzdhblozUGxKblBpMjl2YzZ5OHp3Y3U1ZE1jY2FfRFVzUTZRMlNMZ21WQkFtQW5sUEFTWUExOUhNc3hDMEpjdGIzMXpzVkNWdzRRZlk5YTc2TjhsM3J5NU9tWUdYZGw4WW04c2VCVF9xaHpnbzFHcnl5Ym5tck1xamZEcWIzX3BsaldpSWZYdS01T3lWWEhjR0N2WGhaVEgyUTJLSmM3VmFTZEJkMEZObjFLazMzeVhiSjRUaF9SRlNnN3UyWU1t?oc=5',
}
out = {}
for k, u in links.items():
    for attempt in range(2):
        try:
            r = resolve(u)
            out[k] = r
            print(k, '=>', r)
            break
        except Exception as e:
            if attempt == 1:
                out[k] = None
                print(k, 'ERR', e)
            time.sleep(2)
    time.sleep(1)

with open('_rv_resolved.json', 'w', encoding='utf-8') as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
