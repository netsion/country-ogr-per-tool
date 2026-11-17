import json, re, sys, io, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
try:
    from pypdf import PdfReader
except ImportError:
    from PyPDF2 import PdfReader

base = r'C:\Users\R4314\AppData\Local\Temp'
years = [2019, 2020, 2021, 2022, 2023]
out = {}
kws = ['理事', '監事', '代表理事', '益子', '真下', '八十雄', '根木', '阪本', '平尾', '荒木', '神谷', '大西', '前田', '事務局長']

try:
    from pypdf.errors import PdfReadError
except ImportError:
    from PyPDF2.errors import PdfReadError

for y in years:
    p = os.path.join(base, f'cf_{y}_jigyo.pdf')
    if not os.path.exists(p):
        continue
    try:
        r = PdfReader(p)
    except Exception as e:
        out[str(y)] = {'error': str(e)}
        continue
    text = ''
    for pg in r.pages:
        text += (pg.extract_text() or '') + '\n'
    year_info = {'len': len(text), 'hits': {}}
    for kw in kws:
        snippets = []
        for m in re.finditer(kw, text):
            s = max(0, m.start()-40); e = min(len(text), m.end()+120)
            snippets.append(text[s:e].replace('\n', ' / '))
        year_info['hits'][kw] = snippets
    out[str(y)] = year_info

print(json.dumps(out, ensure_ascii=False, indent=2))
