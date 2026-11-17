import json, re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
try:
    from pypdf import PdfReader
except ImportError:
    from PyPDF2 import PdfReader

path = r'C:\Users\R4314\AppData\Local\Temp\cf_2017_jigyo.pdf'
r = PdfReader(path)
text = ''
for p in r.pages:
    text += (p.extract_text() or '') + '\n'

out = {'len': len(text)}
# Search a wider set
kws = ['役員', '理事', '監事', '代表', '益子', '真下', '八十雄', '根木', '阪本', '平尾', '荒木', '神谷', '前田', 'Mashimo', 'Mashiki']
out['hits'] = {}
for kw in kws:
    snippets = []
    for m in re.finditer(kw, text):
        s = max(0, m.start()-60); e = min(len(text), m.end()+120)
        snippets.append(text[s:e].replace('\n', ' / '))
    out['hits'][kw] = snippets

# Print all text chunks containing personnel info
m = re.search(r'役員', text)
if m:
    out['around_yakuin'] = text[max(0,m.start()-100):m.end()+1500]

print(json.dumps(out, ensure_ascii=False, indent=2))
