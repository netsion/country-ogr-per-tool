"""Read-only contextual extraction for a 200-row reference review. Never edits profiles."""
import csv,json,pathlib,re,sys,hashlib,unicodedata
from collections import defaultdict
import zhconv
ROOT=pathlib.Path(__file__).resolve().parents[1];OUT=ROOT/'output/_id_audit'
sys.stdout.reconfigure(encoding='utf-8')
def load(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def norm(s):return re.sub(r'[^\w\u4e00-\u9fff]','',zhconv.convert(unicodedata.normalize('NFKD',str(s)).lower(),'zh-cn'))
def parts(s):return {norm(p) for p in re.split(r'[()（）]',s) if len(norm(p))>3}|{norm(s)}
def names(d,kind):
 b=d.get('basic_info',{}) if kind=='org' else d
 return [b[k] for k in (['name_original','name_en','name_zh'] if kind=='org' else ['name','name_en','name_zh']) if isinstance(b.get(k),str) and b[k]]
profiles={};index=defaultdict(set);registry=defaultdict(list);sources=defaultdict(list);manifest={}
latest={}
for cc in (ROOT/'output').iterdir():
 if not cc.is_dir() or not re.fullmatch('[a-z]{2}',cc.name):continue
 dirs=[x for x in cc.iterdir() if x.is_dir() and re.fullmatch(r'20\d\d-\d\d-\d\d',x.name)]
 if dirs:latest[cc.name]=max(dirs,key=lambda x:x.name)
config={'work_org':('work_experience','organization','org_id'),'person_rel':('person_relationships','person_name','person_id'),'family':('family_members','name','person_id'),'key_people':('key_people','name','person_id'),'related_org':('related_entities','org_name','org_id')}
for cc,base in latest.items():
 rp=base/'id_registry.json'
 if rp.exists():
  r=load(rp)
  for item in (r.get('registry') or [])+(r.get('person_registry') or []):
   eid=item.get('person_id') or item.get('org_id')
   if eid:registry[eid].append({'entry':item,'file':str(rp.relative_to(ROOT))})
 for folder,kind,idkey in [('persons','person','person_id'),('orgs','org','org_id')]:
  for f in (base/folder).glob('*.json'):
   if f.name.startswith('_'):continue
   d=load(f);eid=d.get(idkey)
   if not eid:continue
   ns=names(d,kind);profiles[eid]={'file':str(f.relative_to(ROOT)),'names':ns,'aliases':(d.get('basic_info',{}) if kind=='org' else d).get('aliases',[]),'qid':d.get('wikidata_qid'),'kind':kind,'data':d}
   for n in ns:
    for part in parts(n):index[(kind,part)].add(eid)
   for cat,(array,nkey,rkey) in config.items():
    for i,item in enumerate(d.get(array) or []):
     key=(cat,cc,str(item.get(nkey) or ''))
     sources[key].append({'file':str(f.relative_to(ROOT)),'owner_id':eid,'owner_names':ns,'array':array,'index':i,'entry':item})
rows=list(csv.DictReader((OUT/'null_review_200.csv').open(encoding='utf-8-sig',newline='')));results=[]
for row in rows:
 cat=row['类型'];cc=row['国家'];ref=row['引用名称'];oldid=row['当前ID'];kind='org' if cat in ['work_org','related_org'] else 'person'
 src=sources.get((cat,cc,ref),[])
 if row['引用方']:
  narrowed=[s for s in src if row['引用方'] in s['owner_names']]
  if narrowed:src=narrowed
 tgt=profiles.get(oldid);candidates=set()
 for part in parts(ref):candidates|=index[(kind,part)]
 def brief(t):return {k:v for k,v in t.items() if k!='data'}
 result={'row':row,'sources':src,'target':brief(tgt) if tgt else None,'registry':registry.get(oldid,[]),'candidates':[{'id':i,**brief(profiles[i])} for i in sorted(candidates)]}
 results.append(result)
 for f in {s['file'] for s in src}|({tgt['file']} if tgt else set())|{r['file'] for r in registry.get(oldid,[])}:
  manifest[f]=hashlib.sha256((ROOT/f).read_bytes()).hexdigest()
(OUT/'sample_200_context.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(OUT/'sample_200_read_manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
for r in results:
 n=r['row']['序号'];curr=[s['entry'].get(config[r['row']['类型']][2]) for s in r['sources']]
 print(n,'src',len(r['sources']),'now',curr,'target',r['target']['names'] if r['target'] else None,'reg',[(e['entry'].get('name'),e['entry'].get('status')) for e in r['registry']], 'candidates',[(c['id'],c['names']) for c in r['candidates']])
