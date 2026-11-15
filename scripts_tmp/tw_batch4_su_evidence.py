"""Clarify post-expiry current appointment evidence without inventing renewal dates."""
import pathlib,json
R=pathlib.Path(__file__).resolve().parents[1];p=R/'output/tw/2026-07-27/persons/TW-PERSON-000014.json';d=json.loads(p.read_text(encoding='utf-8'))
more=[('中央社2026-06-16新任资政名单：上届届满与苏贞昌列名','https://www.cna.com.tw/news/aipl/202606160038.aspx'),('总统府2026-07-09活动原文仍称苏贞昌资政','https://www.president.gov.tw/NEWS/40182')]
for title,url in more:
 if not any(q['url']==url for q in d['collection_meta']['quotes']):d['collection_meta']['quotes'].append({'title':title,'url':url})
note=' 续聘补证：中央社2026-06-16公布旧聘期届满后的新资政名单并列苏贞昌，且总统府2026-07-09活动原文仍称资政，与现任官网名单交叉；新一轮个人聘期起止日仍未见，不从旧聘书推算。'
if note.strip() not in d['collection_meta']['notes']:d['collection_meta']['notes']+=note
for target in [p,R/'tmp/tw_batch4_enriched'/p.name]:target.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
print('Added current-role corroboration after old term expiry; no renewal date guessed')
