# -*- coding: utf-8 -*-
import io, re, html, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
h = open('_dg_ytv.html', encoding='utf-8', errors='ignore').read()

BS = chr(92)
key = '"attributedDescription":{"content":"'
i = h.find(key)
if i > 0:
    j = i + len(key)
    out = []
    while j < len(h):
        c = h[j]
        if c == '"':
            break
        if c == BS:
            out.append(h[j:j+2]); j += 2
        else:
            out.append(c); j += 1
    raw = ''.join(out)
    desc = raw.replace(BS+'n', '\n').replace(BS+'"'.replace(BS,''), '"').replace(BS+'u0026', '&')
    print('DESC_START')
    print(desc[:1200])
    print('DESC_END')
else:
    print('no attributedDescription')

i = h.find('"ownerChannelName":"')
if i > 0:
    print('OWNER:', h[i+20:i+120])
i = h.find('"dateText":{"simpleText":"')
if i > 0:
    print('DATE:', h[i+26:i+120])
i = h.find('"viewCount":{"videoViewCountRenderer":{"viewCount":{"simpleText":"')
if i > 0:
    print('VIEWS:', h[i+67:i+140])
print('Dante count:', h.count('Dante'))
# search any Gonz in description area
for m in re.finditer('Gonz', h):
    s = max(0, m.start()-200)
    seg = html.unescape(re.sub(r' +', ' ', h[s:m.end()+200]))
    print('GONZ CTX:', seg[:350])
    break
