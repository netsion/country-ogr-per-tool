import pathlib,json,collections
from jsonschema import Draft7Validator
P=pathlib.Path('output/tw/2026-07-27');S=pathlib.Path('.agents/skills/country-org-collector');B=pathlib.Path('tmp/tw_before_repair_20261113_021320')
def load(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def save(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
skip={'TW-PERSON-'+i for i in ['000001','000012','000018','000032','000011','000035','000023','000026','000508','000526']}
skip.update('TW-GOV-'+i for i in ['023','024','025','026'])
audit=[]
for folder,stype in [('orgs','org'),('persons','person')]:
 schema=load(S/(stype+'_profile_schema.json'))
 for f in (P/folder).glob('TW-*.json'):
  if f.stem in skip:continue
  x=load(f); old=load(B/folder/f.name); meta=x.get('collection_meta',{});phase=meta.get('phase');target='phase2_skeleton' if folder=='orgs' else 'phase4_person_profile'
  if phase not in (['phase2_skeleton','phase3_enriched'] if folder=='orgs' else ['phase4_person_profile']):
   meta['phase']=target;meta['notes']=(meta.get('notes') or '')+'；仅Schema规范化，旧phase='+str(phase)+'；仍为未研究骨架，不代表深采完成。'
  sources=[];quotes=meta.setdefault('quotes',[])
  for source in meta.get('data_sources',[]):
   if source.startswith(('http://','https://')):
    if not any(q.get('url')==source for q in quotes):quotes.append({'title':'历史来源链接（本次未重新读取）','url':source})
    source='wikidata' if 'wikidata.org/' in source else 'wikipedia' if 'wikipedia.org/' in source else 'other'
   if source not in sources:sources.append(source)
  meta['data_sources']=sources
  if isinstance(x.get('profile'),dict):
   for k in list(x['profile']):
    if k not in schema['properties']['profile']['properties']:audit.append({'id':f.stem,'path':'profile.'+k,'value':x['profile'].pop(k)})
  if folder=='orgs' and not x['basic_info'].get('org_subtype'):
   bi=x['basic_info']; names=' '.join(str(bi.get(k) or '') for k in ['name_original','name_zh','name_en']); sub=None
   if '大学' in names or '大學' in names or 'University' in names:sub='university'
   if f.stem=='TW-GOV-019':sub='cabinet'
   if f.stem=='TW-GOV-020':sub='legislature'
   if f.stem=='TW-GOV-021':sub='judiciary'
   if f.stem=='TW-GOV-018':sub='regulatory_agency'
   if f.stem in ['TW-GOV-017','TW-GOV-022']:sub='independent_organ'
   if sub:bi['org_subtype']=sub
  save(f,x)
reg=load(P/'id_registry.json');reg['counters']['TW-PERSON']=527;reg['person_counters']['TW-PERSON']=527;save(P/'id_registry.json',reg)
save(B/'schema_followup_audit.json',audit)
errors=[];counts={}
for folder,stype in [('orgs','org'),('persons','person')]:
 validator=Draft7Validator(load(S/(stype+'_profile_schema.json'))); start=len(errors)
 for f in sorted((P/folder).glob('TW-*.json')):
  for e in validator.iter_errors(load(f)):errors.append({'file':str(f),'path':'.'.join(map(str,e.absolute_path)),'message':e.message})
 counts[folder]=len(errors)-start
save(pathlib.Path('tmp/tw_jsonschema_validation.json'),{'counts':counts,'errors':errors});print(counts);print(collections.Counter(e['path'] for e in errors))
