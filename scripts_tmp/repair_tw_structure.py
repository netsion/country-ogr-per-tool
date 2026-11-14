import json, pathlib, shutil, datetime, collections
P=pathlib.Path('output/tw/2026-07-27'); S=pathlib.Path('.agents/skills/country-org-collector')
B=pathlib.Path('tmp')/('tw_before_repair_'+datetime.datetime.now().strftime('%Y%m%d_%H%M%S'))
shutil.copytree(P,B); (P/'.inflight').write_text('TW repair and enrichment in progress',encoding='utf-8')
def load(p): return json.loads(p.read_text(encoding='utf-8-sig'))
def save(p,x): p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
audit={'backup':str(B),'removed_fields':[],'removed_relationships':[],'removed_key_people':[],'quarantined':[]}
quarantine={'TW-ACAD-004':'Vietnam historical era, not an organization','TW-MEDIA-008':'Indonesian audit institution, wrong jurisdiction','TW-MIL-006':'Pedialyte product, not military institution','TW-GOV-016':'Jinguashi shrine heritage site, not government institution; https://www.gep.ntpc.gov.tw/xmdoc/cont?sid=0G252559441265222233&xsmsid=0G246378033877603476'}
old=load(P/'tw_registry.json'); reg={'country':'TW','registry':[],'person_registry':[],'counters':{},'person_counters':{'TW-PERSON':527}}
for f in (P/'orgs').glob('TW-*.json'):
 x=load(f); ident=x['org_id']; typ=ident.split('-')[1]; reg['counters']['TW-'+typ]=max(reg['counters'].get('TW-'+typ,0),int(ident.split('-')[-1]))
 if ident in quarantine:
  audit['quarantined'].append({'id':ident,'reason':quarantine[ident]}); (B/'quarantined').mkdir(exist_ok=True); shutil.move(str(f),str(B/'quarantined'/f.name)); continue
 schema=load(S/'org_profile_schema.json'); allowed=schema['properties']; basic=x['basic_info']; basic.setdefault('name_original',basic.get('name_local') or basic.get('name_zh') or basic.get('name_en','')); basic.setdefault('hq_country_iso3','TWN'); basic.setdefault('org_subtype','')
 basic={k:v for k,v in basic.items() if k in allowed['basic_info']['properties']};x['basic_info']=basic
 kept=[]
 for k in x.get('key_people',[]):
  if k.get('title') in ['附属','Affiliated','Affiliated (name match)']:
   audit['removed_key_people'].append({'org_id':ident,'entry':k})
  else: kept.append(k)
 x['key_people']=kept
 for k in list(x):
  if k not in allowed: audit['removed_fields'].append({'id':ident,'field':k});del x[k]
 save(f,x); reg['registry'].append({'org_id':ident,'name':basic.get('name_original'),'name_zh':basic.get('name_zh'),'name_en':basic.get('name_en'),'org_type':typ,'wikidata_qid':x.get('wikidata_qid'),'status':'profiled'})
persons=[]
for f in sorted((P/'persons').glob('TW-*.json')):
 x=load(f); ident=x['person_id']; priority=x.get('importance_level') or 'low'; reason=x.get('importance_reason'); allowed=load(S/'person_profile_schema.json')['properties']; rel=[]
 for r in x.get('person_relationships',[]):
  if 'org_id' in r or 'org_name' in r: audit['removed_relationships'].append({'person_id':ident,'entry':r})
  else: rel.append(r)
 x['person_relationships']=rel
 if x.get('name_local') and x['name_local']!=x.get('name'):
  x.setdefault('aliases',[])
  if x['name_local'] not in x['aliases']:x['aliases'].append(x['name_local'])
 for k in list(x):
  if k not in allowed: audit['removed_fields'].append({'id':ident,'field':k});del x[k]
 save(f,x);reg['person_registry'].append({'person_id':ident,'name':x['name'],'name_zh':x.get('name_zh'),'name_en':x.get('name_en'),'wikidata_qid':x.get('wikidata_qid'),'status':'profiled'})
 persons.append({'person_id':ident,'name':x['name'],'name_zh':x.get('name_zh'),'name_en':x.get('name_en'),'wikidata_qid':x.get('wikidata_qid'),'importance_level':priority,'importance_reason':reason,'source_orgs':[],'discovery_source':'other','nationality':'TW','notes':'历史候选档案；优先级、现职、组织关系待复核，非已核验领导名录。'})
for typ,n in old.get('counters',{}).items():
 if typ!='PERSON':reg['counters']['TW-'+typ]=max(n,reg['counters'].get('TW-'+typ,0))
save(P/'id_registry.json',reg)
priority=['000001','000012','000018','000032','000011','000035','000023','000026','000508','000526']
persons.sort(key=lambda x:(priority.index(x['person_id'][-6:]) if x['person_id'][-6:] in priority else 1000,int(x['person_id'][-6:])))
save(P/'person_list.json',{'metadata':{'country':'Chinese Taipei','country_iso':'TW','collection_date':'2026-11-13','phase':'phase4_person_list','source_org_count':len(reg['registry']),'total_persons':len(persons)},'persons':persons,'summary':{'by_importance_level':dict(collections.Counter(x['importance_level'] for x in persons)),'by_discovery_source':{'other':len(persons)},'data_quality':{'with_person_id':len(persons),'with_wikidata_qid':sum(bool(x['wikidata_qid']) for x in persons),'without_person_id':0}}})
save(B/'repair_audit.json',audit)
print(json.dumps({'backup':str(B),'orgs':len(reg['registry']),'persons':len(persons),'removed_rel':len(audit['removed_relationships']),'removed_key_people':len(audit['removed_key_people'])}))
