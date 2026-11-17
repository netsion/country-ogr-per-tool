import json, re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
try:
    from pypdf import PdfReader
except ImportError:
    from PyPDF2 import PdfReader

path = r'C:\Users\R4314\AppData\Local\Temp\cf_2024_jigyo.pdf'
r = PdfReader(path)
text = ''
for p in r.pages:
    text += (p.extract_text() or '') + '\n'

kws = ['役員', '理事', '監事', '代表理事', '益子', '真下', '八十雄', '根木', '阪本', '平尾', '荒木', '神谷']
out = {'len': len(text), 'hits': {}}
for kw in kws:
    snippets = []
    for m in re.finditer(kw, text):
        s = max(0, m.start()-50); e = min(len(text), m.end()+100)
        snippets.append(text[s:e].replace('\n', ' / '))
    out['hits'][kw] = snippets

# Also dump a chunk around "役員" if present
m = re.search(r'役員', text)
if m:
    out['around_yakuin'] = text[max(0,m.start()-200):m.end()+800]

# Dump first 2000 chars
out['head'] = text[:2000]

print(json.dumps(out, ensure_ascii=False, indent=2))
