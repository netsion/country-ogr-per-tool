import json
x=json.load(open('tmp/social_xlsx_20261116/workbook_raw.json',encoding='utf-8'))
for s in x:
 for r in s['rows']:
  if any(str(c.get('value','')) in ['黄伟哲','黃偉哲'] for c in r['cells']):
   print(s['sheet'],r['row'],[(c['col'],c['value']) for c in r['cells']])
