"""Install evidence-only clarifications after scoped review."""
import json,pathlib
R=pathlib.Path(__file__).resolve().parents[1];B=R/'output/tw/2026-07-27';S=R/'tmp/tw_batch2_enriched'
pid='TW-PERSON-000148'
x=json.loads((B/'persons'/f'{pid}.json').read_text(encoding='utf-8'))
notes=x['collection_meta']['notes']
notes=notes.replace('配偶依据维基及华视新闻搜索摘要交叉，华视正文403，未扩展子女资料。','配偶身份由自由时报2018-11-24现场报道及台视2024-09-10原文交叉确认；华视正文403摘要不再作为事实依据。未扩展子女、婚礼或未确认私人活动。')
x['collection_meta']['notes']=notes
x['family_members'][0]['industry_or_organization']='仅记录两家独立媒体原文确认的公开配偶身份。'
q=x['collection_meta']['quotes'];q[:]=[e for e in q if 'news.cts.com.tw' not in e['url']]
for title,url in [('自由时报：卢秀燕与丈夫廖述嘉连袂投票','https://election.ltn.com.tw/2018/print/New/breakingnews/2622893'),('台视：卢秀燕请假报道，正文确认配偶廖述嘉','https://news.ttv.com.tw/news/11309100030900N')]:
 if not any(e['url']==url for e in q):q.append({'title':title,'url':url})
for p in [B/'persons'/f'{pid}.json',S/f'{pid}.json']:p.write_text(json.dumps(x,ensure_ascii=False,indent=2),encoding='utf-8')
print('Updated Lu spouse evidence; no added private details')
pid='TW-PERSON-000039'
x=json.loads((B/'persons'/f'{pid}.json').read_text(encoding='utf-8'))
x['collection_meta']['notes']=x['collection_meta']['notes'].replace('早期精确任期与配偶仍维基单源。配偶非双来源确认，保持最小信息；未扩展子女。','早期精确任期仍有维基单源边界。配偶林道春另经监察院廉政专刊第299期中本人2025-11-01申报表确认；仅提取配偶姓名与关系，未采财产、地址及其他私人资料。未扩展子女。')
x['family_members'][0]['industry_or_organization']='仅记录监察院公开申报及维基确认的配偶身份。'
url='https://www-ws.cy.gov.tw/Download.ashx?icon=..pdf&n=44CQ5buJ5pS%2F5bCI5YiK56ysMjk55pyf44CRLnBkZg%3D%3D&u=LzAwMS9VcGxvYWQvMS9yZWxmaWxlLzg4NjEvMzY5ODYvOWMwMzA0ZGItNWM1Zi00YzE0LTgzOTQtZmYwZjNmYmMyM2MwLnBkZg%3D%3D'
if not any(e['url']==url for e in x['collection_meta']['quotes']):x['collection_meta']['quotes'].append({'title':'监察院廉政专刊第299期：柯建铭申报表，仅核配偶姓名林道春','url':url})
for p in [B/'persons'/f'{pid}.json',S/f'{pid}.json']:p.write_text(json.dumps(x,ensure_ascii=False,indent=2),encoding='utf-8')
print('Updated Ker spouse evidence from public declaration; no financial/private data collected')
