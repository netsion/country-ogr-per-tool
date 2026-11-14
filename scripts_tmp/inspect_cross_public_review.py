"""Snapshot current source pointers and both ID targets for 491 read-only reviews."""
import csv,json,pathlib,re,hashlib,sys
from collections import Counter
ROOT=pathlib.Path(__file__).resolve().parents[1];OUT=ROOT/'output/_id_audit'
sys.stdout.reconfigure(encoding='utf-8')
cache={};manifest={}
def read(p):
 p=p.resolve();key=str(p)
 if key not in cache:
  cache[key]=json.loads(p.read_text(encoding='utf-8-sig'))
  manifest[str(p.relative_to(ROOT))]=hashlib.sha256(p.read_bytes()).hexdigest()
 return cache[key]
latest={}
for cc in (ROOT/'output').iterdir():
 if cc.is_dir() and re.fullmatch('[a-z]{2}',cc.name):
  ds=[p for p in cc.iterdir() if p.is_dir() and re.fullmatch(r'20\d\d-\d\d-\d\d',p.name)]
  if ds:latest[cc.name]=max(ds,key=lambda p:p.name)
def target(eid):
 if not eid:return None
 base=latest.get(eid[:2].lower());folder='persons' if '-PERSON-' in eid else 'orgs'
 if not base:return {'id':eid,'file':None,'registry':[]}
 f=base/folder/(eid+'.json');rp=base/'id_registry.json';reg=[]
 if rp.exists():
  data=read(rp)
  reg=[r for r in (data.get('registry') or [])+(data.get('person_registry') or []) if r.get('org_id')==eid or r.get('person_id')==eid]
 return {'id':eid,'file':str(f.relative_to(ROOT)) if f.exists() else None,'profile':read(f) if f.exists() else None,'registry':reg}
rows=list(csv.DictReader((OUT/'step1b_cross_public_review.csv').open(encoding='utf-8-sig',newline='')))
priority=list(csv.DictReader((OUT/'step1b_cross_public_priority.csv').open(encoding='utf-8-sig',newline='')))
pk={(r['原始引用位置'],r['原ID'],r['新ID'],r['引用名称']) for r in priority}
result=[]
for n,row in enumerate(rows,1):
 path,pointer=row['原始引用位置'].split('#',1);m=re.fullmatch(r'(\w+)\[(\d+)\]\.(\w+)',pointer)
 assert m,pointer
 array,num,field=m.group(1),int(m.group(2)),m.group(3);source=read(ROOT/path)
 arr=source.get(array) or [];entry=arr[num] if num<len(arr) else None
 refname=(entry.get('organization') or entry.get('org_name') or entry.get('person_name') or entry.get('name')) if entry else None
 actual=entry.get(field) if entry else None
 status='unchanged' if entry and actual==row['新ID'] and refname==row['引用名称'] else 'stale'
 rr={'review_row':n,'priority_sample':(row['原始引用位置'],row['原ID'],row['新ID'],row['引用名称']) in pk,'row':row,
     'source_file':path,'pointer':pointer,'entry':entry,'current_id':actual,'current_reference':refname,'snapshot_status':status,
     'owner_id':source.get('person_id') or source.get('org_id'),'owner_names':{k:source.get(k) for k in ['name','name_zh','name_en','nationality']},
     'source_quotes':source.get('collection_meta',{}).get('quotes',[]),'source_biography':source.get('biography_summary'),
     'old_target':target(row['原ID']),'new_target':target(row['新ID'])}
 result.append(rr)
(OUT/'cross_public_491_context.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(OUT/'cross_public_491_read_manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Rows',len(rows),'priority',sum(r['priority_sample'] for r in result),'snapshot states',dict(Counter(r['snapshot_status'] for r in result)))
for r in result:
 if r['review_row']<=54 or r['snapshot_status']!='unchanged':
  print(r['review_row'],r['row']['引用国家'],r['row']['引用方'],r['row']['引用名称'],'old',r['row']['原ID'],r['row']['原指向'],'new',r['row']['新ID'],r['row']['新指向'],'now',r['current_id'],r['snapshot_status'],str(r['entry'])[:450])
