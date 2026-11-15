"""Apply only manually reviewed same-country exact-primary-name profile links."""
import pathlib,json,sys,subprocess
R=pathlib.Path(__file__).resolve().parents[1];B=R/'output/tw/2026-07-27';O=R/'tmp/tw_batch4_20261115'
def load(p):return json.loads(p.read_text(encoding='utf-8'))
allowed={'TW-ACAD-019','TW-ACAD-015','TW-GOV-019','TW-GOV-020','TW-GOV-023','TW-GOV-024','TW-GOV-026','TW-PARTY-012','TW-MEDIA-014'}
changes=[];files={}
for c in load(O/'null_org_candidates.json'):
 if len(c['candidates'])!=1 or c['candidates'][0]['id'] not in allowed:continue
 pid=c['person_id'];p=B/'persons'/f'{pid}.json';d=files.setdefault(pid,load(p));row=d['work_experience'][c['index']];target=c['candidates'][0]
 assert row==c['reference'] and row.get('org_id') is None
 assert target['info'].get('hq_country_iso3')=='TWN'
 row['org_id']=target['id'];changes.append({'person_id':pid,'index':c['index'],'organization':row['organization'],'old_id':None,'new_id':row['org_id']})
for pid,d in files.items():
 if not any(x['person_id']==pid for x in changes):continue
 p=B/'persons'/f'{pid}.json';p.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
 result=subprocess.run([sys.executable,str(R/'.agents/skills/country-org-collector/scripts/validate_schema.py'),str(B),'--file',f'persons/{pid}.json','--score'],capture_output=True,text=True,encoding='utf-8');assert 'Errors: 0' in result.stdout,(pid,result.stdout,result.stderr)
 (R/'tmp/tw_batch4_enriched'/p.name).write_bytes(p.read_bytes())
log=O/'verified_org_links.json';prior=load(log) if log.exists() else [];log.write_text(json.dumps(prior+changes,ensure_ascii=False,indent=2),encoding='utf-8')
print('Applied',len(changes),'reviewed null org links in',len({x['person_id'] for x in changes}),'profiles')
