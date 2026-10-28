import re, sys, string, urllib.request, urllib.error, urllib.parse, ssl, time

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
PROXY = "http://127.0.0.1:7890"
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
opener = urllib.request.build_opener(urllib.request.ProxyHandler({'http': PROXY, 'https': PROXY}), urllib.request.HTTPSHandler(context=ctx))

def fetch(url, cookie=None, binary=False):
    req = urllib.request.Request(url, headers={'User-Agent': UA, 'Accept': 'text/html,application/xhtml+xml,application/pdf,*/*', 'Accept-Language': 'es-ES,es;q=0.9,en;q=0.8'})
    if cookie:
        req.add_header('Cookie', cookie)
    for attempt in range(3):
        try:
            with opener.open(req, timeout=45) as r:
                data = r.read()
            return data if binary else data.decode('utf-8', errors='ignore')
        except urllib.error.HTTPError as e:
            if e.code in (301, 302, 303, 307, 308) and attempt < 2:
                loc = e.headers.get('Location', url)
                req = urllib.request.Request(loc if loc.startswith('http') else urllib.parse.urljoin(url, loc), headers={'User-Agent': UA, 'Accept': 'text/html,application/xhtml+xml,application/pdf,*/*', 'Accept-Language': 'es-ES,es;q=0.9,en;q=0.8'})
                if cookie:
                    req.add_header('Cookie', cookie)
                continue
            raise

def decode_challenge(html):
    m = re.search(r"S='([^']+)'", html)
    if not m: return None, None
    S = m.group(1)
    A = string.ascii_uppercase + string.ascii_lowercase + '0123456789+/'
    tbl = {A[i]: i for i in range(64)}
    U = 0; l = 0; r = []
    for i, ch in enumerate(S):
        c = tbl.get(ch)
        if c is None: continue
        U = (U << 6) + c; l += 6
        while l >= 8:
            l -= 8
            a = (U >> l) & 0xff
            if a or i < len(S) - 2:
                r.append(chr(a))
    script = ''.join(r)
    mu = re.search(r"\bu='';", script)
    if mu:
        seg = script[mu.end():]
    else:
        mu2 = re.search(r"\bu='[0-9a-f]' \+", script)
        seg = script[mu2.start():] if mu2 else ''
    seg = seg.split('document.cookie')[0]
    seg = re.sub(r"^u='[^']*' \+ ", "", seg)
    parts = re.findall(r"'([^']*)'|\"([^\"]*)\"|String\.fromCharCode\((\d+)\)", seg)
    u = ''.join(a or b or (chr(int(c)) if c else '') for a, b, c in parts)
    mc = re.search(r"document\.cookie=([^;]+);", script)
    name = ''
    if mc:
        pre = mc.group(1).split('+ u +')[0].split('+u+')[0]
        toks = re.findall(r"'([^']*)'|\"([^\"]*)\"", pre)
        name = ''.join(a or b for a, b in toks).rstrip('=')
    return name, u

def smart_fetch(url, outfile):
    html = fetch(url)
    if "sucuri_cloudproxy" in html or "You are being redirected" in html:
        name, u = decode_challenge(html)
        if name and u:
            cookie = f"{name}={u}"
            print("challenge cookie:", cookie)
            time.sleep(1)
            html = fetch(url, cookie=cookie)
    with open(outfile, 'w', encoding='utf-8') as f:
        f.write(html)
    print("saved", outfile, len(html), "chars")

if __name__ == '__main__':
    smart_fetch(sys.argv[1], sys.argv[2])
