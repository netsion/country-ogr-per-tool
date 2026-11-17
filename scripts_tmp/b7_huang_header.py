import json
x=json.load(open('tmp/social_xlsx_20261116/workbook_raw.json',encoding='utf-8'))
s=next(s for s in x if s['sheet']=='2026-03-16')
for r in s['rows']:
 if r['row'] in [1,2,3,500,501,502,503,504,505,506,507,508,509,510]:print(r)
