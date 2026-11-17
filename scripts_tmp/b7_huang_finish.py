import json,pathlib
p=pathlib.Path('tmp/tw_batch7_enriched/TW-PERSON-000572.json');d=json.loads(p.read_text(encoding='utf-8')); x=json.load(open('tmp/social_xlsx_20261116/workbook_raw.json',encoding='utf-8'));s=next(s for s in x if s['sheet']=='2026-03-16')
for r in s['rows']:
 c={c['col']:c['value'] for c in r['cells']}
 if c.get(2) not in ['黄伟哲','黃偉哲']:continue
 platform={'x':'twitter'}.get(c[3],c[3]);url=c[4];existing=next((a for a in d['social_accounts'] if a['platform']==platform),None)
 note=f'用户授权社交.xlsx工作表2026-03-16第{r["row"]}行；姓名黄伟哲、C5市长/Q52重复列关联；USER-ID取第5列；未独立核实实时官方认证。'
 if c.get(6):note+='第6列PAGE-ID='+str(c[6])+'，不填入user_id。'
 if existing:
  existing['source_note']+=' '+note
  if existing.get('user_id') not in [None,c.get(5)]: existing['user_id']=None;existing['source_note']+='USER-ID冲突留空。'
  else:existing['user_id']=c.get(5)
 else:d['social_accounts'].append({'platform':platform,'url':url,'source':{'twitter':3,'youtube':9,'instagram':8,'threads':24}[platform],'nickname':'黃偉哲','username':url.rstrip('/').split('/')[-1].lstrip('@'),'user_id':c.get(5),'source_note':note})
d['collection_meta']['quotes'].append({'title':'媽媽和太太都是老師 黃偉哲貼文賀教師節','url':'https://www.cna.com.tw/news/aloc/202209280230.aspx'})
d['family_members'][0]['industry_or_organization']='教師（中央社确认其妻职业，未载任教机构）'
d['collection_meta']['notes']=d['collection_meta']['notes'].replace('家庭配偶目前僅維基可讀正文確認；鏡週刊小檔案為圖片未據搜索摘要補事實。未核家庭雙來源，請覆核。','家庭配偶劉育菁实名仍仅维基正文；已读中央社2022-09-28原文确认其妻为教师，但该稿未载姓名，实名保留单源标记。').replace('社交表候選未完成USER-ID逐欄覆核，故不填數字ID。','已逐行核用户表本人10条记录，去重5平台；全部USER-ID取第5列，第6列PAGE-ID仅来源说明；另保留本人LINE及其直接Facebook外链。')
p.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
import jsonschema
jsonschema.validate(d,json.load(open('.agents/skills/country-org-collector/person_profile_schema.json',encoding='utf-8')))
