import re, sys, string

def decode(html):
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
    open('_sucuri_script.js','w',encoding='utf-8').write(script)
    # u value: parse token stream after "u=" (direct or empty init)
    mu = re.search(r"\bu='';", script)
    if mu:
        seg = script[mu.end():]
    else:
        mu2 = re.search(r"\bu='4' \+", script) or re.search(r"\bu='[0-9a-f]' \+", script)
        seg = script[mu2.start():] if mu2 else ''
    # take until 'document.cookie'
    seg = seg.split('document.cookie')[0]
    # drop the leading init fragment like "u='4' + "
    seg = re.sub(r"^u='[^']*' \+ ", "", seg)
    parts = re.findall(r"'([^']*)'|\"([^\"]*)\"|String\.fromCharCode\((\d+)\)", seg)
    u = ''.join(a or b or (chr(int(c)) if c else '') for a, b, c in parts)
    # cookie name: tokens in document.cookie='...' before " = "
    mc = re.search(r"document\.cookie=([^;]+);", script)
    nameexpr = mc.group(1)
    pre = nameexpr.split('+ u +')[0].split('+u+')[0]
    toks = re.findall(r"'([^']*)'|\"([^\"]*)\"", pre)
    name = ''.join(a or b for a, b in toks)
    return u, name

html = open(sys.argv[1], encoding='utf-8', errors='ignore').read()
u, name = decode(html)
print(f"{name}={u}")
