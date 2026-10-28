# -*- coding: utf-8 -*-
import io, re, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
h = open('_dg_yt.html', encoding='utf-8', errors='ignore').read()
# extract title contents near videoId blocks
seen = set()
for m in re.finditer(r'"videoId":"([A-Za-z0-9_-]{11})"', h):
    vid = m.group(1)
    if vid in seen: continue
    seen.add(vid)
    # look for a title content after this id
    seg = h[m.end():m.end()+4000]
    t = re.search(r'"title":\{"content":"([^"]+)"', seg) or re.search(r'"title":\{"runs":\[\{"text":"([^"]+)"', seg)
    print(vid, '|', t.group(1)[:110] if t else '(no title)')
