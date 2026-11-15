"""Read-only global exact-name recall for current batch's unknown people links."""
import json,pathlib,re,collections,unicodedata
import zhconv
R=pathlib.Path(__file__).resolve().parents[1];B=R/'output/tw/2026-07-27';O=R/'tmp/tw_batch5_20261115'
def load(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def norm(s):return re.sub(r'\s+','',zhconv.convert(unicodedata.normalize('NFKC',s),'zh-cn')).lower()
needed=collections.defaultdict(list)
for pid in load(B/'_batch5_progress.json')['completed']:
 for field,key in [('person_relationships','person_name'),('family_members','name')]:
  for i,row in enumerate(load(B/'persons'/f'{pid}.json').get(field,[])):
   if row.get('person_id'):continue
   for part in [p.strip() for p in re.split('[()（）]',row[key]) if p.strip()]:needed[norm(part)].append({'source':pid,'field':field,'index':i,'reference':row})
found=[];scanned=0
for cc in (R/'output').iterdir():
 if not cc.is_dir() or not re.fullmatch('[a-z]{2}',cc.name):continue
 dates=[p for p in cc.iterdir() if p.is_dir() and re.fullmatch('20[0-9]{2}-[0-9]{2}-[0-9]{2}',p.name)]
 if not dates:continue
 for f in (max(dates,key=lambda p:p.name)/'persons').glob('*-PERSON-*.json'):
  d=load(f);scanned+=1
  names={norm(n) for n in [d.get('name'),d.get('name_zh'),d.get('name_en')] if n}
  refs={(r['source'],r['field'],r['index']):r for n in names for r in needed.get(n,[]) if r['source']!=d.get('person_id')}
  for r in refs.values():found.append({**r,'target':{'person_id':d['person_id'],'name':d.get('name'),'name_zh':d.get('name_zh'),'positions':d.get('current_positions'), 'file':f.relative_to(R).as_posix()}})
(O/'global_null_person_candidates.json').write_text(json.dumps(found,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'profiles_scanned':scanned,'candidates':found},ensure_ascii=False))
