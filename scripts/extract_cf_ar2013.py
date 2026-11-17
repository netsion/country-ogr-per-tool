import json, re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
try:
    from pypdf import PdfReader
except ImportError:
    from PyPDF2 import PdfReader

path = r'C:\Users\R4314\AppData\Local\Temp\cf_AR2013.pdf'
r = PdfReader(path)
out = {'pages': len(r.pages), 'hits': {}, 'contexts': []}
kws = ['Mashimo', 'Mashiki', 'Yasuo', 'Yasoo', 'Director', 'Board', '理事', '真下', '益子', '八十雄', '八十夫', 'Controller', 'Auditor', 'Directors']
full = ''
for p in r.pages:
    full += (p.extract_text() or '') + '\n'

out['total_len'] = len(full)
for kw in kws:
    snippets = []
    for m in re.finditer(kw, full):
        s = max(0, m.start()-80); e = min(len(full), m.end()+200)
        snippets.append(full[s:e].replace('\n', ' / '))
    out['hits'][kw] = snippets

# also dump 'Board of Directors' context
for m in re.finditer(r'(?i)board of directors|directors', full):
    s = max(0, m.start()-50); e = min(len(full), m.end()+600)
    out['contexts'].append(full[s:e].replace('\n', ' / '))

print(json.dumps(out, ensure_ascii=False, indent=2))
