import json
p='tmp/tw_batch8_enriched/TW-PERSON-000585.json'
d=json.load(open(p,encoding='utf-8'))
for a in d['social_accounts']:
 if a['platform']=='line': a['source_note']='本人官網https://a-chun.tw/頁尾直接外鏈至https://page.line.me/beu1231o；LINE頁面署名何欣純，顯示@achun。未獨立核實實時官方認證。'
d['collection_meta']['notes']=d['collection_meta']['notes'].replace('配偶姓名僅民間公報單源','配偶謝俊雄另經中央社2026-11-13及聯合報2026-11-12全文交叉確認；僅收配偶身份，不採選戰指控為既定事實').replace('完整當期專訪至2026-10-06','完整當期專訪至2026-10-06，另讀中央社2026-11-13競總回應報導').replace('未新增QID。','未新增QID。檢索林昶佐僅命中游錫堃画像中的關聯文本，已讀TW-PERSON-000022確認非同人，故林昶佐ID保持null。')
for title,url in [('中央社夫婿遭質疑、何欣純競總回應（僅核配偶及當期身份）','https://www.cna.com.tw/news/aloc/202611130093.aspx'),('聯合報2026年11月12日報導（僅核配偶身份）','https://udn.com/news/story/124652/9873974')]:d['collection_meta']['quotes'].append(dict(title=title,url=url))
open(p,'w',encoding='utf-8').write(json.dumps(d,ensure_ascii=False,indent=2))
import jsonschema
jsonschema.validate(d,json.load(open('.agents/skills/country-org-collector/person_profile_schema.json',encoding='utf-8')))
print('jsonschema PASS')
